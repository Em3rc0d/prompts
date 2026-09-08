#!/usr/bin/env python3
"""Execute exactly one clean Starter N09 observation from the user's WSL via Gemini API.

Properties:
- exact case PM-STARTER-CR-NORMAL-0001
- exact 8,100-byte frozen envelope + SHA-256 gate
- GEMINI_API_KEY is read only from the local WSL environment
- one generateContent transport attempt maximum; zero application retries
- no evaluation contract / answer key in runtime input
- evidence written only to a caller-supplied local WSL directory
- no GitHub Actions trigger, no GitHub artifact upload, no Vercel deployment
- runtime output is evidence only; never automatic certification or promotion
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PM-STARTER-CR-NORMAL-0001"
CASE_PATH = ROOT / "product/starter-collection-v1/evaluation/cases/PM-STARTER-CR-NORMAL-0001.json"
CLEAN_SURFACE_PATH = ROOT / "commercial/STARTER_CLEAN_RUNTIME_SURFACE_REQUIREMENTS_V1.json"
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
PIPELINE_PATH = ROOT / "commercial/PROMPT_MACHINE_14_GATE_PIPELINE_V1.json"
EXPECTED_SHA = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
EXPECTED_BYTES = 8100
SURFACE = "WSL_LOCAL_GEMINI_GENERATE_CONTENT_API"
PROVIDER = "GOOGLE_GEMINI_API"
AUTH_ENV = "GEMINI_API_KEY"
EXACT_AUTH = "AUTORIZO PM-STARTER-CR-NORMAL-0001: 1 ejecución, 0 reintentos."
MODEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize(text: str) -> str:
    return text.rstrip("\n") + "\n"


def render(surface: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + normalize(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + normalize(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def assert_wsl() -> None:
    version_path = Path("/proc/version")
    if not version_path.exists():
        raise RuntimeError("blocked: /proc/version missing; WSL could not be verified")
    version = version_path.read_text(encoding="utf-8", errors="ignore").lower()
    if "microsoft" not in version and "wsl" not in version:
        raise RuntimeError("blocked: this executor is WSL-local only")


def load_contracts() -> tuple[bytes, dict, dict, dict, dict]:
    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    clean = json.loads(CLEAN_SURFACE_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    pipeline = json.loads(PIPELINE_PATH.read_text(encoding="utf-8"))

    if case.get("case_id") != CASE_ID:
        raise RuntimeError("case identity mismatch")
    if case.get("evaluation_contract_is_runtime_input") is not False:
        raise RuntimeError("evaluation contract boundary drifted")
    if clean.get("automatic_retries") != 0:
        raise RuntimeError("clean-surface retry boundary drifted")
    if policy.get("policy_state") != "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER":
        raise RuntimeError("local-only policy is not active")
    if policy.get("execution_location") != "USER_WSL":
        raise RuntimeError("execution-location boundary drifted")
    if policy.get("inference_provider") != PROVIDER:
        raise RuntimeError("provider boundary drifted")
    if policy.get("credential_environment_variable") != AUTH_ENV:
        raise RuntimeError("credential boundary drifted")
    if policy.get("github_actions_runtime_trigger_allowed") is not False:
        raise RuntimeError("GitHub Actions runtime trigger must remain disabled")
    if policy.get("github_artifact_upload_of_runtime_output_allowed") is not False:
        raise RuntimeError("GitHub artifact runtime upload must remain disabled")
    if policy.get("current_authorization_state") != "DISARMED_PREVIOUS_V3_AUTHORIZATION_CONSUMED":
        raise RuntimeError("repository policy must remain disarmed; fresh authorization is supplied per invocation")
    if pipeline.get("master_invariant") != "NO PROMPT MAY ENTER A RELEASE WITHOUT A PROMPT_ID + SPEC + TEST EVIDENCE + CERTIFICATION DECISION":
        raise RuntimeError("14-gate pipeline invariant drifted")
    gates = pipeline.get("gates") or []
    if len(gates) != 14 or gates[4].get("id") != "G05_BASELINE_EXECUTION":
        raise RuntimeError("14-gate certification pipeline drifted")

    workflow = (ROOT / case["workflow_surface_path"]).read_text(encoding="utf-8")
    envelope = render(workflow, case["instance_data_markdown"])
    if len(envelope) != EXPECTED_BYTES:
        raise RuntimeError(f"envelope byte mismatch: {len(envelope)}")
    if sha256(envelope) != EXPECTED_SHA:
        raise RuntimeError("envelope SHA-256 mismatch")

    forbidden = [b"expected_state", b"blocking_dimensions", b"assessment_answer_key"]
    if any(marker in envelope for marker in forbidden):
        raise RuntimeError("evaluation-only material leaked into runtime input")
    return envelope, case, clean, policy, pipeline


def extract_text(payload: dict) -> str:
    chunks: list[str] = []
    for candidate in payload.get("candidates") or []:
        content = candidate.get("content") or {}
        for part in content.get("parts") or []:
            text = part.get("text")
            if isinstance(text, str) and text:
                chunks.append(text)
    return "\n".join(chunks).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Exact Gemini model ID to record for this execution")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    args = parser.parse_args()

    assert_wsl()
    if args.authorization.strip() != EXACT_AUTH:
        raise SystemExit("blocked: fresh exact runtime authorization missing")
    if not MODEL_RE.fullmatch(args.model):
        raise SystemExit("blocked: invalid Gemini model ID syntax")
    if args.max_output_tokens < 1:
        raise SystemExit("blocked: max-output-tokens must be positive")

    key = os.environ.get(AUTH_ENV)
    if not key:
        raise SystemExit(f"blocked before model use: {AUTH_ENV} is not present in the local WSL environment")

    envelope, case, clean, policy, pipeline = load_contracts()
    out = args.output_dir.expanduser().resolve()
    if out.exists():
        raise SystemExit("blocked: output directory already exists")
    out.mkdir(parents=True)

    execution_id = f"PM-STARTER-CR-NORMAL-0001-GEMINI-WSL-{secrets.token_hex(6).upper()}"
    started_at = utc_now()

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": envelope.decode("utf-8")}],
            }
        ],
        "generationConfig": {
            "maxOutputTokens": args.max_output_tokens,
        },
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    request_body_sha256 = sha256(encoded)

    model_path = urllib.parse.quote(args.model, safe="")
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_path}:generateContent"
    request = urllib.request.Request(
        endpoint,
        data=encoded,
        method="POST",
        headers={
            "x-goog-api-key": key,
            "Content-Type": "application/json",
        },
    )

    # Exactly one transport attempt. No application retry loop exists below.
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            raw = response.read()
            http_status = response.status
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        failure = {
            "schema": "prompt-machine-starter-n09-gemini-wsl-failure-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "provider": PROVIDER,
            "execution_surface": SURFACE,
            "execution_location": "USER_WSL",
            "model_requested": args.model,
            "started_at": started_at,
            "failed_at": utc_now(),
            "surface_submissions": 1,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "http_status": exc.code,
            "runtime_envelope_bytes": EXPECTED_BYTES,
            "runtime_envelope_sha256": EXPECTED_SHA,
            "request_body_sha256": request_body_sha256,
            "response_body_sha256": sha256(raw),
            "certification_gate": "G05_BASELINE_EXECUTION",
            "state": "LOCAL_WSL_GEMINI_PROVIDER_FAILURE_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        (out / "raw-provider-error.bin").write_bytes(raw)
        write_json(out / "receipt.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2
    except Exception as exc:
        failure = {
            "schema": "prompt-machine-starter-n09-gemini-wsl-failure-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "provider": PROVIDER,
            "execution_surface": SURFACE,
            "execution_location": "USER_WSL",
            "model_requested": args.model,
            "started_at": started_at,
            "failed_at": utc_now(),
            "surface_submissions": 1,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "runtime_envelope_bytes": EXPECTED_BYTES,
            "runtime_envelope_sha256": EXPECTED_SHA,
            "request_body_sha256": request_body_sha256,
            "error_type": type(exc).__name__,
            "certification_gate": "G05_BASELINE_EXECUTION",
            "state": "LOCAL_WSL_GEMINI_TRANSPORT_FAILURE_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "receipt.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2

    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        failure = {
            "schema": "prompt-machine-starter-n09-gemini-wsl-invalid-response-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "provider": PROVIDER,
            "execution_surface": SURFACE,
            "model_requested": args.model,
            "http_status": http_status,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "raw_provider_response_sha256": sha256(raw),
            "state": "INVALID_PROVIDER_RESPONSE_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        (out / "raw-provider-response.bin").write_bytes(raw)
        write_json(out / "receipt.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 3

    output = extract_text(payload)
    if not output:
        failure = {
            "schema": "prompt-machine-starter-n09-gemini-wsl-empty-output-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "provider": PROVIDER,
            "execution_surface": SURFACE,
            "model_requested": args.model,
            "http_status": http_status,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "raw_provider_response_sha256": sha256(raw),
            "finish_reasons": [c.get("finishReason") for c in payload.get("candidates") or []],
            "state": "EMPTY_OUTPUT_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        (out / "raw-provider-response.json").write_bytes(raw)
        write_json(out / "receipt.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 3

    raw_output = output.encode("utf-8")
    (out / "raw-provider-response.json").write_bytes(raw)
    (out / "raw-output.md").write_bytes(raw_output)

    evidence = {
        "schema": "prompt-machine-starter-n09-gemini-wsl-observation-v1",
        "version": "1.0.0",
        "execution_id": execution_id,
        "case_id": CASE_ID,
        "workflow_id": case["workflow_id"],
        "provider": PROVIDER,
        "execution_surface": SURFACE,
        "execution_location": "USER_WSL",
        "credential_source": "LOCAL_ENVIRONMENT_ONLY",
        "credential_value_recorded": False,
        "fresh_independent_surface": True,
        "evaluation_contract_is_runtime_input": False,
        "expected_result_is_runtime_input": False,
        "model_requested": args.model,
        "provider_model_version": payload.get("modelVersion"),
        "provider_response_id": payload.get("responseId"),
        "runtime_envelope_bytes": EXPECTED_BYTES,
        "runtime_envelope_sha256": EXPECTED_SHA,
        "request_body_sha256": request_body_sha256,
        "max_output_tokens": args.max_output_tokens,
        "started_at": started_at,
        "completed_at": utc_now(),
        "http_status": http_status,
        "request_id": headers.get("x-request-id") or headers.get("X-Request-Id"),
        "surface_submissions": 1,
        "provider_requests_attempted": 1,
        "automatic_retries": 0,
        "automatic_second_case": False,
        "raw_output_sha256": sha256(raw_output),
        "raw_output_bytes": len(raw_output),
        "raw_provider_response_sha256": sha256(raw),
        "usage_metadata": payload.get("usageMetadata"),
        "github_artifact_uploaded": False,
        "github_actions_used_for_runtime": False,
        "vercel_deployment_created": False,
        "human_review_required": True,
        "automatic_promotion": False,
        "certification_pipeline_version": pipeline["version"],
        "certification_gate": "G05_BASELINE_EXECUTION",
        "certification_claim": "NONE",
        "release_claim": "NONE",
        "state": "CLEAN_LOCAL_WSL_GEMINI_RUNTIME_OBSERVED_HUMAN_REVIEW_REQUIRED",
        "clean_surface_contract_version": clean["version"],
        "local_policy_version": policy["version"],
    }
    write_json(out / "runtime-evidence.json", evidence)
    write_json(
        out / "review-packet.json",
        {
            "schema": "prompt-machine-starter-n09-gemini-wsl-review-packet-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "certification_gate": "G05_BASELINE_EXECUTION",
            "review_status": "HUMAN_REVIEW_REQUIRED",
            "automatic_retry": False,
            "automatic_next_case": False,
            "automatic_certification": False,
            "automatic_pack_rebuild": False,
            "automatic_provider_gate": False,
            "promotion_claim": "NONE",
        },
    )

    # Metadata only. Raw model output remains on the local WSL filesystem.
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
