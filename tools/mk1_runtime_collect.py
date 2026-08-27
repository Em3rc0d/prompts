from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote

import httpx

from mk1_behavioral_runner import find_fixture_set, load, sha256_json, sha256_text


PROVIDERS = {
    "openai": {"key_env": "OPENAI_API_KEY", "family": "openai"},
    "anthropic": {"key_env": "ANTHROPIC_API_KEY", "family": "anthropic"},
    "gemini": {"key_env": "GEMINI_API_KEY", "family": "google-gemini"},
}
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def render_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def render_prompt(prompt_body: str, fixture: dict) -> str:
    """Substitute only variables actually supplied by the fixture.

    Missing variables intentionally remain as literal placeholders. This keeps
    missing-required and missing-optional cases faithful to the frozen fixture
    instead of inserting a post-hoc sentinel the prompt was never designed for.
    """
    rendered = prompt_body
    variables = (fixture.get("input") or {}).get("variables") or {}
    for name, value in variables.items():
        rendered = rendered.replace("{" + str(name) + "}", render_value(value))
    return rendered


def parse_openai_response(payload: dict) -> tuple[str, dict]:
    texts: list[str] = []
    top = payload.get("output_text")
    if isinstance(top, str) and top:
        texts.append(top)
    if not texts:
        for item in payload.get("output") or []:
            if not isinstance(item, dict):
                continue
            for part in item.get("content") or []:
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                    texts.append(part["text"])
    text = "\n".join(texts)
    metadata = {
        "response_id": payload.get("id"),
        "resolved_model": payload.get("model"),
        "status": payload.get("status"),
        "usage": payload.get("usage"),
    }
    return text, metadata


def parse_anthropic_response(payload: dict) -> tuple[str, dict]:
    texts = [
        part.get("text", "")
        for part in payload.get("content") or []
        if isinstance(part, dict) and part.get("type") == "text" and isinstance(part.get("text"), str)
    ]
    text = "\n".join(texts)
    metadata = {
        "response_id": payload.get("id"),
        "resolved_model": payload.get("model"),
        "stop_reason": payload.get("stop_reason"),
        "usage": payload.get("usage"),
    }
    return text, metadata


def parse_gemini_response(payload: dict) -> tuple[str, dict]:
    texts: list[str] = []
    candidates = payload.get("candidates") or []
    for candidate in candidates[:1]:
        if not isinstance(candidate, dict):
            continue
        content = candidate.get("content") or {}
        for part in content.get("parts") or []:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                texts.append(part["text"])
    first = candidates[0] if candidates and isinstance(candidates[0], dict) else {}
    text = "\n".join(texts)
    metadata = {
        "response_id": payload.get("responseId"),
        "resolved_model": payload.get("modelVersion"),
        "finish_reason": first.get("finishReason"),
        "usage": payload.get("usageMetadata"),
        "prompt_feedback": payload.get("promptFeedback"),
    }
    return text, metadata


def _post_json(
    client: httpx.Client,
    url: str,
    headers: dict[str, str],
    body: dict,
    attempts: int = 4,
) -> dict:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = client.post(url, headers=headers, json=body)
        except httpx.RequestError as exc:
            last_error = exc
            if attempt == attempts:
                raise RuntimeError(f"Provider request failed after {attempts} attempts: {type(exc).__name__}") from exc
            time.sleep(2 ** (attempt - 1))
            continue

        if response.status_code in RETRYABLE_STATUS and attempt < attempts:
            time.sleep(2 ** (attempt - 1))
            continue
        if response.status_code >= 400:
            raise RuntimeError(f"Provider request failed with HTTP {response.status_code}; response body intentionally omitted from CI logs")
        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError("Provider returned a non-JSON response") from exc

    raise RuntimeError(f"Provider request failed: {last_error!r}")


def call_openai(client: httpx.Client, api_key: str, model: str, prompt: str, max_output_tokens: int) -> tuple[str, dict]:
    payload = _post_json(
        client,
        "https://api.openai.com/v1/responses",
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        {
            "model": model,
            "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
            "max_output_tokens": max_output_tokens,
            "store": False,
        },
    )
    return parse_openai_response(payload)


def call_anthropic(client: httpx.Client, api_key: str, model: str, prompt: str, max_output_tokens: int) -> tuple[str, dict]:
    payload = _post_json(
        client,
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        {
            "model": model,
            "max_tokens": max_output_tokens,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    return parse_anthropic_response(payload)


def call_gemini(client: httpx.Client, api_key: str, model: str, prompt: str, max_output_tokens: int) -> tuple[str, dict]:
    clean_model = model.removeprefix("models/")
    encoded_model = quote(clean_model, safe="-._")
    payload = _post_json(
        client,
        f"https://generativelanguage.googleapis.com/v1beta/models/{encoded_model}:generateContent",
        {"x-goog-api-key": api_key, "Content-Type": "application/json"},
        {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_output_tokens},
        },
    )
    return parse_gemini_response(payload)


PROVIDER_CALLS: dict[str, Callable[[httpx.Client, str, str, str, int], tuple[str, dict]]] = {
    "openai": call_openai,
    "anthropic": call_anthropic,
    "gemini": call_gemini,
}


def collect_execution(
    artifact: dict,
    fixture_set: dict,
    provider: str,
    model: str,
    execution_id: str,
    caller: Callable[[str], tuple[str, dict]],
    run_at: str | None = None,
) -> dict:
    if provider not in PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")
    if artifact.get("state") != "VALID":
        raise ValueError(f"Runtime collector accepts VALID F2 artifacts only; got {artifact.get('state')!r}")
    if fixture_set.get("artifact_id") != artifact.get("id") or fixture_set.get("artifact_version") != artifact.get("version"):
        raise ValueError("Runtime collector artifact/fixture identity mismatch")
    prompt_body = artifact.get("prompt_body")
    if not isinstance(prompt_body, str) or not prompt_body.strip():
        raise ValueError("Runtime collector requires non-empty prompt_body")
    if not str(model).strip():
        raise ValueError("Runtime collector requires an explicit model id")
    if not str(execution_id).strip():
        raise ValueError("Runtime collector requires execution_id")

    responses: dict[str, dict] = {}
    for fixture in fixture_set.get("cases", []):
        rendered = render_prompt(prompt_body, fixture)
        output, metadata = caller(rendered)
        if not isinstance(output, str) or not output.strip():
            raise RuntimeError(f"Provider returned empty text for fixture {fixture['fixture_id']}")
        responses[fixture["fixture_id"]] = {
            "fixture_input": fixture.get("input", {}),
            "rendered_prompt_fingerprint": sha256_text(rendered),
            "output": output,
            "human_checks": {
                check: {"status": "UNRESOLVED", "note": ""}
                for check in fixture.get("expected", {}).get("human_checks", [])
            },
            "provider_metadata": metadata,
        }

    return {
        "execution_id": execution_id,
        "mode": "api",
        "collection_status": "OBSERVED_OUTPUTS_PENDING_HUMAN_REVIEW",
        "runtime": {
            "provider": provider,
            "model": model,
            "family": PROVIDERS[provider]["family"],
            "run_at": run_at or utc_now(),
        },
        "review": {
            "reviewer_type": "human",
            "reviewer_ref": "",
            "reviewed_at": "",
        },
        "artifact_id": artifact["id"],
        "artifact_version": artifact["version"],
        "artifact_prompt_fingerprint": sha256_text(prompt_body),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version", "1"),
        "fixture_set_fingerprint": sha256_json(fixture_set),
        "responses": responses,
        "instructions": [
            "Outputs in this envelope were collected from the declared provider/model runtime and are not human-reviewed yet.",
            "Do not change prompt, fixture input, provider output or frozen identity fields after collection.",
            "Resolve every declared human check as PASS or FAIL with a concrete evidence note.",
            "Fill reviewer_ref and reviewed_at only when a human has actually completed the review.",
            "A model self-judgment must not be relabeled as human review.",
            "Only after review may mk1_behavioral_runner.py produce an F4 receipt; only a real BEHAVIORAL_PASS receipt can promote TESTED.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--fixture-set", required=True)
    parser.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    args = parser.parse_args()

    if args.max_output_tokens < 64:
        raise SystemExit("--max-output-tokens must be >= 64")
    provider_config = PROVIDERS[args.provider]
    api_key = os.environ.get(provider_config["key_env"], "")
    if not api_key:
        raise SystemExit(f"Missing required environment variable {provider_config['key_env']}; do not pass API keys on the command line")

    artifact = load(Path(args.artifact))
    fixture_document = load(Path(args.fixtures))
    fixture_set = find_fixture_set(fixture_document, args.fixture_set)

    with httpx.Client(timeout=httpx.Timeout(args.timeout_seconds)) as client:
        provider_call = PROVIDER_CALLS[args.provider]

        def caller(prompt: str) -> tuple[str, dict]:
            return provider_call(client, api_key, args.model, prompt, args.max_output_tokens)

        envelope = collect_execution(
            artifact,
            fixture_set,
            args.provider,
            args.model,
            args.execution_id,
            caller,
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "mk1_runtime_collection": "OBSERVED_OUTPUTS_PENDING_HUMAN_REVIEW",
        "artifact_id": envelope["artifact_id"],
        "fixture_set_id": envelope["fixture_set_id"],
        "provider": envelope["runtime"]["provider"],
        "model": envelope["runtime"]["model"],
        "family": envelope["runtime"]["family"],
        "fixture_outputs": len(envelope["responses"]),
        "output": output.as_posix(),
        "secret_policy": "API keys are read only from provider-specific environment variables and are never serialized or printed.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
