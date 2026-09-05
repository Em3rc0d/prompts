#!/usr/bin/env python3
"""Prompt Machine Starter N09 — Gemini provider/model visibility diagnostic.

This script performs metadata GET requests only. It never calls generateContent,
never sends the frozen runtime envelope, and never creates behavioral evidence.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODELS = ["gemini-3.8-flash", "gemini-3.5-flash"]
REPORT = Path.home() / ".local/share/prompt-machine/n09/provider-visibility-diagnostic-v1.json"
BASE = "https://generativelanguage.googleapis.com/v1beta/models/"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def is_wsl() -> bool:
    p = Path("/proc/version")
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8", errors="ignore").lower()
    return "microsoft" in text or "wsl" in text


def probe(model: str, key: str) -> dict:
    url = BASE + urllib.parse.quote(model, safe="")
    req = urllib.request.Request(url, method="GET", headers={"x-goog-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            payload = json.loads(raw.decode("utf-8")) if raw else {}
            return {
                "model": model,
                "http_status": response.status,
                "resource_name": payload.get("name"),
                "display_name": payload.get("displayName"),
                "supported_generation_methods": payload.get("supportedGenerationMethods"),
                "provider_request_made": True,
                "model_inference_made": False,
            }
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            payload = {}
        error = payload.get("error") or {}
        return {
            "model": model,
            "http_status": exc.code,
            "provider_error_status": error.get("status"),
            "provider_error_message": error.get("message"),
            "provider_request_made": True,
            "model_inference_made": False,
        }
    except Exception as exc:
        return {
            "model": model,
            "transport_error": type(exc).__name__,
            "provider_request_made": True,
            "model_inference_made": False,
        }


def main() -> int:
    if not is_wsl():
        raise SystemExit("blocked: WSL could not be verified")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("blocked: GEMINI_API_KEY missing")

    results = [probe(model, key) for model in MODELS]
    statuses = [item.get("http_status") for item in results]
    if statuses == [200, 200]:
        classification = "MODELS_VISIBLE_GENERATION_PATH_STILL_UNPROVEN"
    elif any(status == 403 for status in statuses):
        classification = "PROJECT_OR_KEY_ACCESS_DIAGNOSTIC_REQUIRED"
    elif any(status == 404 for status in statuses):
        classification = "MODEL_VISIBILITY_DIAGNOSTIC_REQUIRED"
    elif any(status == 429 for status in statuses):
        classification = "PROJECT_RATE_OR_QUOTA_DIAGNOSTIC_REQUIRED"
    elif any(isinstance(status, int) and status >= 500 for status in statuses):
        classification = "PROVIDER_METADATA_SERVICE_UNAVAILABLE"
    else:
        classification = "MIXED_PROVIDER_DIAGNOSTIC_RESULT"

    report = {
        "schema": "prompt-machine-starter-n09-gemini-provider-visibility-result-v1",
        "recorded_at": now(),
        "execution_location": "USER_WSL",
        "provider": "GOOGLE_GEMINI_API",
        "metadata_requests_attempted": len(results),
        "generate_content_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "runtime_envelope_sent": False,
        "credential_value_recorded": False,
        "automatic_retries": 0,
        "results": results,
        "classification": classification,
        "behavioral_observations": 0,
        "g05_claim": "NONE",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
