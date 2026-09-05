#!/usr/bin/env python3
"""Governed one-shot minimal Gemini generateContent diagnostic.

This is NOT a G05 workflow execution. It sends only the fixed prompt
"Return exactly: OK" to gemini-3.5-flash, performs at most one provider request,
and never retries automatically.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "commercial/STARTER_N09_GEMINI_MINIMAL_GENERATION_CONTROL_001_PLAN.json"
CONTROL_ID = "PM-GEMINI-MINIMAL-GEN-CTRL-001"
MODEL = "gemini-3.5-flash"
PROMPT = "Return exactly: OK"
EXACT_AUTH = "AUTORIZO PM-GEMINI-MINIMAL-GEN-CTRL-001: 1 ejecución, 0 reintentos."


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def is_wsl() -> bool:
    p = Path("/proc/version")
    text = p.read_text(errors="ignore").lower() if p.exists() else ""
    return "microsoft" in text or "wsl" in text


def extract_text(payload: dict) -> str:
    chunks: list[str] = []
    for candidate in payload.get("candidates") or []:
        for part in (candidate.get("content") or {}).get("parts") or []:
            if isinstance(part.get("text"), str):
                chunks.append(part["text"])
    return "\n".join(chunks).strip()


def main() -> int:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--authorization", required=True)
    p.add_argument("--output-dir", required=True, type=Path)
    args = p.parse_args()

    if not is_wsl():
        raise SystemExit("blocked: WSL could not be verified")
    if args.authorization.strip() != EXACT_AUTH:
        raise SystemExit("blocked: fresh exact diagnostic authorization missing")

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("blocked before provider use: GEMINI_API_KEY missing")

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    if plan.get("control_id") != CONTROL_ID:
        raise SystemExit("blocked: control id drift")
    if plan.get("state") != "PREPARED_ZERO_MODEL_PREFLIGHT_REQUIRED":
        raise SystemExit("blocked: unexpected control plan state")
    if plan.get("model") != MODEL or plan.get("prompt") != PROMPT:
        raise SystemExit("blocked: frozen minimal control drift")
    if plan.get("maximum_provider_requests") != 1 or plan.get("automatic_retries") != 0:
        raise SystemExit("blocked: request budget drift")
    if plan.get("workflow_candidate_sent") is not False or plan.get("behavioral_observation_allowed") is not False:
        raise SystemExit("blocked: diagnostic/G05 boundary drift")

    out = args.output_dir.expanduser().resolve()
    planned = Path(os.path.expandvars(os.path.expanduser(plan["output_directory"]))).resolve()
    if out != planned:
        raise SystemExit("blocked: output directory differs from frozen control plan")
    if out.exists():
        raise SystemExit("blocked: output directory already exists")
    out.mkdir(parents=True)

    body = {
        "contents": [{"role": "user", "parts": [{"text": PROMPT}]}],
        "generationConfig": {"maxOutputTokens": 8},
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + urllib.parse.quote(MODEL, safe="")
        + ":generateContent"
    )
    req = urllib.request.Request(
        endpoint,
        data=encoded,
        method="POST",
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
    )

    execution_id = f"{CONTROL_ID}-{secrets.token_hex(6).upper()}"
    started_at = now()

    # Exactly one provider transport attempt. There is intentionally no retry loop.
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            raw = response.read()
            status = response.status
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        code = exc.code
        if code == 503:
            classification = "MINIMAL_GENERATION_PATH_UNAVAILABLE_503_PROVIDER_GENERATION_BACKEND_SIGNAL"
        elif code == 429:
            classification = "MINIMAL_GENERATION_RATE_OR_QUOTA_SIGNAL_429"
        elif 400 <= code < 500:
            classification = "MINIMAL_GENERATION_REQUEST_OR_ACCESS_4XX"
        else:
            classification = "MINIMAL_GENERATION_PROVIDER_5XX"
        receipt = {
            "schema": "prompt-machine-starter-n09-gemini-minimal-generation-control-result-v1",
            "control_id": CONTROL_ID,
            "execution_id": execution_id,
            "provider": "GOOGLE_GEMINI_API",
            "model": MODEL,
            "started_at": started_at,
            "completed_at": now(),
            "http_status": code,
            "provider_requests_attempted": 1,
            "model_inference_requests_attempted": 1,
            "automatic_retries": 0,
            "workflow_candidate_sent": False,
            "runtime_envelope_sent": False,
            "evaluation_contract_sent": False,
            "behavioral_observations": 0,
            "g05_claim": "NONE",
            "request_body_sha256": sha(encoded),
            "response_body_sha256": sha(raw),
            "credential_value_recorded": False,
            "classification": classification,
        }
        (out / "raw-provider-error.bin").write_bytes(raw)
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 2
    except Exception as exc:
        receipt = {
            "schema": "prompt-machine-starter-n09-gemini-minimal-generation-control-result-v1",
            "control_id": CONTROL_ID,
            "execution_id": execution_id,
            "provider": "GOOGLE_GEMINI_API",
            "model": MODEL,
            "started_at": started_at,
            "completed_at": now(),
            "provider_requests_attempted": 1,
            "model_inference_requests_attempted": 1,
            "automatic_retries": 0,
            "workflow_candidate_sent": False,
            "runtime_envelope_sent": False,
            "behavioral_observations": 0,
            "g05_claim": "NONE",
            "credential_value_recorded": False,
            "error_type": type(exc).__name__,
            "classification": "MINIMAL_GENERATION_TRANSPORT_FAILURE",
        }
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 2

    try:
        payload = json.loads(raw.decode("utf-8"))
        text = extract_text(payload)
    except Exception:
        payload = None
        text = ""

    (out / "raw-provider-response.bin").write_bytes(raw)
    if text:
        (out / "raw-output.txt").write_text(text + "\n", encoding="utf-8")

    receipt = {
        "schema": "prompt-machine-starter-n09-gemini-minimal-generation-control-result-v1",
        "control_id": CONTROL_ID,
        "execution_id": execution_id,
        "provider": "GOOGLE_GEMINI_API",
        "model": MODEL,
        "started_at": started_at,
        "completed_at": now(),
        "http_status": status,
        "provider_requests_attempted": 1,
        "model_inference_requests_attempted": 1,
        "automatic_retries": 0,
        "workflow_candidate_sent": False,
        "runtime_envelope_sent": False,
        "evaluation_contract_sent": False,
        "behavioral_observations": 0,
        "g05_claim": "NONE",
        "request_body_sha256": sha(encoded),
        "response_body_sha256": sha(raw),
        "credential_value_recorded": False,
        "response_text_present": bool(text),
        "response_text_exact_ok": text.strip() == "OK",
        "classification": "MINIMAL_GENERATION_PATH_AVAILABLE" if status == 200 else "MINIMAL_GENERATION_UNEXPECTED_SUCCESS_STATUS",
    }
    write_json(out / "receipt.json", receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
