from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import httpx


PLACEHOLDER = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
PROVIDERS = {"openai", "anthropic", "gemini"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def render_prompt(prompt_body: str, variables: dict[str, Any]) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in variables or variables[key] is None or (isinstance(variables[key], str) and not variables[key].strip()):
            return f"[NOT PROVIDED: {key}]"
        value = variables[key]
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        return str(value)
    return PLACEHOLDER.sub(replace, prompt_body)


def _openai_text(response: dict) -> str:
    chunks: list[str] = []
    for item in response.get("output") or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content") or []:
            if content.get("type") == "output_text" and content.get("text"):
                chunks.append(str(content["text"]))
    return "\n".join(chunks).strip()


def _anthropic_text(response: dict) -> str:
    return "\n".join(str(item.get("text")) for item in response.get("content") or [] if item.get("type") == "text" and item.get("text")).strip()


def _gemini_text(response: dict) -> str:
    chunks: list[str] = []
    for candidate in response.get("candidates") or []:
        for part in (candidate.get("content") or {}).get("parts") or []:
            if part.get("text"):
                chunks.append(str(part["text"]))
    return "\n".join(chunks).strip()


def call_provider(provider: str, model: str, prompt: str, timeout: float = 120.0, max_output_tokens: int = 4096) -> tuple[str, dict, dict]:
    provider = provider.casefold().strip()
    if provider not in PROVIDERS:
        raise ValueError(f"Unsupported provider {provider!r}; expected one of {sorted(PROVIDERS)}")

    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        if provider == "openai":
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("OPENAI_API_KEY is not configured")
            request_body = {"model": model, "input": prompt, "store": False, "max_output_tokens": max_output_tokens}
            response = client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json=request_body,
            )
            response.raise_for_status()
            payload = response.json()
            text = _openai_text(payload)
        elif provider == "anthropic":
            key = os.environ.get("ANTHROPIC_API_KEY")
            if not key:
                raise RuntimeError("ANTHROPIC_API_KEY is not configured")
            request_body = {"model": model, "max_tokens": max_output_tokens, "messages": [{"role": "user", "content": prompt}]}
            response = client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
                json=request_body,
            )
            response.raise_for_status()
            payload = response.json()
            text = _anthropic_text(payload)
        else:
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                raise RuntimeError("GEMINI_API_KEY is not configured")
            request_body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": max_output_tokens}}
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{quote(model, safe='')}:generateContent"
            response = client.post(endpoint, headers={"x-goog-api-key": key, "Content-Type": "application/json"}, json=request_body)
            response.raise_for_status()
            payload = response.json()
            text = _gemini_text(payload)

    if not text:
        raise RuntimeError(f"{provider} returned no observable text output")
    transport = {
        "http_status": response.status_code,
        "request_id": response.headers.get("x-request-id") or response.headers.get("request-id") or response.headers.get("x-goog-request-id"),
        "response_content_type": response.headers.get("content-type"),
    }
    return text, payload, transport


def execute_observation(provider: str, model: str, family: str, prompt: str, evidence_dir: Path, observation_id: str) -> dict:
    started_at = utc_now()
    text, raw_response, transport = call_provider(provider, model, prompt)
    completed_at = utc_now()
    evidence = {
        "evidence_schema": "mk1-runtime-observation-v1",
        "observation_id": observation_id,
        "provider": provider,
        "model": model,
        "family": family,
        "started_at": started_at,
        "completed_at": completed_at,
        "rendered_prompt_sha256": "sha256:" + hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "transport": transport,
        "raw_response": raw_response,
        "observed_output": text,
    }
    evidence["evidence_sha256"] = sha256_json(evidence)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    path = evidence_dir / f"{observation_id}.json"
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "output": text,
        "identity_evidence_ref": f"{path.as_posix()}#{evidence['evidence_sha256']}",
        "observation_id": observation_id,
        "observed_at": completed_at,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute one frozen MK1 prompt observation and retain raw provider evidence.")
    parser.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    parser.add_argument("--model", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--variables-file", required=True)
    parser.add_argument("--evidence-dir", default="mk1/evidence/runtime")
    parser.add_argument("--observation-id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    variables = json.loads(Path(args.variables_file).read_text(encoding="utf-8"))
    prompt_body = Path(args.prompt_file).read_text(encoding="utf-8")
    rendered = render_prompt(prompt_body, variables)
    result = execute_observation(args.provider, args.model, args.family, rendered, Path(args.evidence_dir), args.observation_id)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "OBSERVED", "observation_id": args.observation_id, "identity_evidence_ref": result["identity_evidence_ref"]}, indent=2))


if __name__ == "__main__":
    main()
