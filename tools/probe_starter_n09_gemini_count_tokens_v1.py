#!/usr/bin/env python3
"""Prompt Machine Starter N09 — non-generative Gemini countTokens diagnostic.

Sends the exact frozen 8100-byte runtime envelope to countTokens for two models.
Never calls generateContent, never records GEMINI_API_KEY, creates no behavioral evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "product/starter-collection-v1/evaluation/cases/PM-STARTER-CR-NORMAL-0001.json"
EXPECTED_BYTES = 8100
EXPECTED_SHA = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
MODELS = ["gemini-3.8-flash", "gemini-3.5-flash"]
REPORT = Path.home() / ".local/share/prompt-machine/n09/count-tokens-diagnostic-v1.json"


def norm(value: str) -> str:
    return value.rstrip("\n") + "\n"


def render(surface: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + norm(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + norm(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def is_wsl() -> bool:
    p = Path("/proc/version")
    text = p.read_text(errors="ignore").lower() if p.exists() else ""
    return "microsoft" in text or "wsl" in text


def main() -> int:
    if not is_wsl():
        raise SystemExit("blocked: WSL could not be verified")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("blocked: GEMINI_API_KEY missing")

    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    workflow = (ROOT / case["workflow_surface_path"]).read_text(encoding="utf-8")
    envelope = render(workflow, case["instance_data_markdown"])
    if len(envelope) != EXPECTED_BYTES or digest(envelope) != EXPECTED_SHA:
        raise SystemExit("blocked: frozen runtime envelope drifted")
    if any(marker in envelope for marker in (b"expected_state", b"blocking_dimensions", b"assessment_answer_key")):
        raise SystemExit("blocked: evaluation-only material leaked into diagnostic input")

    body = {
        "contents": [{"role": "user", "parts": [{"text": envelope.decode("utf-8")}]}]
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    results = []

    for model in MODELS:
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + urllib.parse.quote(model, safe="")
            + ":countTokens"
        )
        req = urllib.request.Request(
            endpoint,
            data=encoded,
            method="POST",
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                raw = response.read()
                payload = json.loads(raw.decode("utf-8"))
                results.append({
                    "model": model,
                    "http_status": response.status,
                    "total_tokens": payload.get("totalTokens"),
                    "provider_request_made": True,
                    "generate_content_made": False,
                    "model_inference_made": False,
                    "response_body_sha256": digest(raw),
                })
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            results.append({
                "model": model,
                "http_status": exc.code,
                "total_tokens": None,
                "provider_request_made": True,
                "generate_content_made": False,
                "model_inference_made": False,
                "response_body_sha256": digest(raw),
            })
        except Exception as exc:
            results.append({
                "model": model,
                "http_status": None,
                "error_type": type(exc).__name__,
                "total_tokens": None,
                "provider_request_made": True,
                "generate_content_made": False,
                "model_inference_made": False,
            })

    statuses = [r.get("http_status") for r in results]
    if statuses == [200, 200]:
        classification = "EXACT_ENVELOPE_TOKENIZATION_PATH_ACCEPTED_GENERATION_PATH_REMAINS_ISOLATED_FAILURE"
    elif any(isinstance(s, int) and 500 <= s <= 599 for s in statuses):
        classification = "BROADER_PROVIDER_BACKEND_UNAVAILABLE_SIGNAL"
    elif any(isinstance(s, int) and 400 <= s <= 499 for s in statuses):
        classification = "REQUEST_OR_ACCESS_PATH_REQUIRES_REVIEW_BEFORE_NEW_GENERATION"
    else:
        classification = "MIXED_OR_TRANSPORT_RESULT_REQUIRES_REVIEW"

    report = {
        "schema": "prompt-machine-starter-n09-gemini-count-tokens-result-v1",
        "recorded_at": now(),
        "case_id": case["case_id"],
        "execution_location": "USER_WSL",
        "provider": "GOOGLE_GEMINI_API",
        "runtime_envelope_bytes": len(envelope),
        "runtime_envelope_sha256": digest(envelope),
        "provider_requests_attempted": len(results),
        "automatic_retries": 0,
        "generate_content_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "behavioral_observations": 0,
        "credential_value_recorded": False,
        "results": results,
        "classification": classification,
        "g05_claim": "NONE",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={REPORT}")
    return 0 if statuses == [200, 200] else 2


if __name__ == "__main__":
    raise SystemExit(main())
