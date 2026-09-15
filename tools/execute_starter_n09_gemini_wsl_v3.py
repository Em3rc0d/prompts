#!/usr/bin/env python3
"""Prompt Machine Starter N09 — local WSL Gemini executor for G05-BASELINE-003.

Exactly one provider request maximum. No automatic retry. No cloud artifact upload.
A successful model response is G05 evidence only and always requires human review.
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

ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PM-STARTER-CR-NORMAL-0001"
ATTEMPT_ID = "G05-BASELINE-003"
CASE_PATH = ROOT / "product/starter-collection-v1/evaluation/cases/PM-STARTER-CR-NORMAL-0001.json"
CLEAN_PATH = ROOT / "commercial/STARTER_CLEAN_RUNTIME_SURFACE_REQUIREMENTS_V1.json"
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
PIPELINE_PATH = ROOT / "commercial/PROMPT_MACHINE_14_GATE_PIPELINE_V1.json"
PLAN_PATH = ROOT / "commercial/STARTER_N09_GEMINI_WSL_ATTEMPT_003_PLAN.json"
EXPECTED_BYTES = 8100
EXPECTED_SHA = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
EXACT_AUTH = "AUTORIZO PM-STARTER-CR-NORMAL-0001: 1 ejecución, 0 reintentos."
PROVIDER = "GOOGLE_GEMINI_API"
SURFACE = "WSL_LOCAL_GEMINI_GENERATE_CONTENT_API"
MODEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")
ALLOWED_PLAN_STATES = {"PREPARED_FRESH_AUTH_REQUIRED", "READY_FOR_FRESH_AUTHORIZATION"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize(text: str) -> str:
    return text.rstrip("\n") + "\n"


def render(workflow: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + normalize(workflow)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + normalize(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def assert_wsl() -> None:
    p = Path("/proc/version")
    text = p.read_text(encoding="utf-8", errors="ignore").lower() if p.exists() else ""
    if "microsoft" not in text and "wsl" not in text:
        raise SystemExit("blocked: WSL could not be verified")


def load_and_validate() -> tuple[bytes, dict, dict, dict, dict, dict]:
    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    clean = json.loads(CLEAN_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    pipeline = json.loads(PIPELINE_PATH.read_text(encoding="utf-8"))
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    auth_state = str(policy.get("current_authorization_state", ""))
    gates = pipeline.get("gates") or []
    checks = {
        "case": case.get("case_id") == CASE_ID,
        "evaluation_contract_excluded": case.get("evaluation_contract_is_runtime_input") is False,
        "zero_retries": clean.get("automatic_retries") == 0,
        "local_policy": policy.get("policy_state") == "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER",
        "user_wsl": policy.get("execution_location") == "USER_WSL",
        "gemini_provider": policy.get("inference_provider") == PROVIDER,
        "local_key": policy.get("credential_environment_variable") == "GEMINI_API_KEY",
        "github_runtime_disabled": policy.get("github_actions_runtime_trigger_allowed") is False,
        "artifact_upload_disabled": policy.get("github_artifact_upload_of_runtime_output_allowed") is False,
        "repository_disarmed": auth_state.startswith("DISARMED_") and auth_state.endswith("_CONSUMED"),
        "pipeline_14": len(gates) == 14,
        "g05_mapping": len(gates) >= 5 and gates[4].get("id") == "G05_BASELINE_EXECUTION",
        "attempt_plan": plan.get("attempt_id") == ATTEMPT_ID and plan.get("state") in ALLOWED_PLAN_STATES,
        "single_request": plan.get("maximum_provider_requests") == 1,
        "attempt_zero_retries": plan.get("automatic_retries") == 0,
        "same_candidate": plan.get("candidate_mutated_since_attempt_002") is False,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit("blocked: contract drift: " + ", ".join(failed))

    workflow = (ROOT / case["workflow_surface_path"]).read_text(encoding="utf-8")
    envelope = render(workflow, case["instance_data_markdown"])
    if len(envelope) != EXPECTED_BYTES or digest(envelope) != EXPECTED_SHA:
        raise SystemExit("blocked: frozen runtime envelope drifted")
    for marker in (b"expected_state", b"blocking_dimensions", b"assessment_answer_key"):
        if marker in envelope:
            raise SystemExit("blocked: evaluation-only material leaked into runtime input")

    return envelope, case, clean, policy, pipeline, plan


def extract_text(payload: dict) -> str:
    parts: list[str] = []
    for candidate in payload.get("candidates") or []:
        for part in (candidate.get("content") or {}).get("parts") or []:
            if isinstance(part.get("text"), str) and part["text"]:
                parts.append(part["text"])
    return "\n".join(parts).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
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

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("blocked before provider use: GEMINI_API_KEY missing")

    envelope, case, clean, policy, pipeline, plan = load_and_validate()
    if args.model != plan.get("model"):
        raise SystemExit("blocked: model differs from frozen Attempt 003 plan")

    out = args.output_dir.expanduser().resolve()
    planned_out = Path(os.path.expandvars(os.path.expanduser(str(plan.get("output_directory", ""))))).resolve()
    if out != planned_out:
        raise SystemExit("blocked: output directory differs from frozen Attempt 003 plan")
    if out.exists():
        raise SystemExit("blocked: output directory already exists")
    out.mkdir(parents=True)

    execution_id = f"{CASE_ID}-GEMINI-WSL-{secrets.token_hex(6).upper()}"
    started_at = now()
    body = {
        "contents": [{"role": "user", "parts": [{"text": envelope.decode("utf-8")}]}],
        "generationConfig": {"maxOutputTokens": args.max_output_tokens},
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + urllib.parse.quote(args.model, safe="")
        + ":generateContent"
    )
    request = urllib.request.Request(
        endpoint,
        data=encoded,
        method="POST",
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
    )

    # Exactly ONE provider transport attempt. No retry loop exists.
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            raw = response.read()
            http_status = response.status
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        receipt = {
            "schema": "prompt-machine-starter-n09-gemini-wsl-attempt-v3-failure",
            "attempt_id": ATTEMPT_ID,
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "provider": PROVIDER,
            "execution_surface": SURFACE,
            "model_requested": args.model,
            "started_at": started_at,
            "failed_at": now(),
            "http_status": exc.code,
            "surface_submissions": 1,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "runtime_envelope_bytes": EXPECTED_BYTES,
            "runtime_envelope_sha256": EXPECTED_SHA,
            "request_body_sha256": digest(encoded),
            "response_body_sha256": digest(raw),
            "state": "PROVIDER_FAILURE_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        (out / "raw-provider-error.bin").write_bytes(raw)
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 2
    except Exception as exc:
        receipt = {
            "schema": "prompt-machine-starter-n09-gemini-wsl-attempt-v3-transport-failure",
            "attempt_id": ATTEMPT_ID,
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "provider": PROVIDER,
            "execution_surface": SURFACE,
            "model_requested": args.model,
            "started_at": started_at,
            "failed_at": now(),
            "surface_submissions": 1,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "error_type": type(exc).__name__,
            "runtime_envelope_bytes": EXPECTED_BYTES,
            "runtime_envelope_sha256": EXPECTED_SHA,
            "state": "TRANSPORT_FAILURE_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 2

    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        (out / "raw-provider-response.bin").write_bytes(raw)
        receipt = {
            "schema": "prompt-machine-starter-n09-gemini-wsl-attempt-v3-invalid-response",
            "attempt_id": ATTEMPT_ID,
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "http_status": http_status,
            "raw_provider_response_sha256": digest(raw),
            "state": "INVALID_PROVIDER_RESPONSE_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 3

    output = extract_text(payload)
    if not output:
        (out / "raw-provider-response.json").write_bytes(raw)
        receipt = {
            "schema": "prompt-machine-starter-n09-gemini-wsl-attempt-v3-empty-output",
            "attempt_id": ATTEMPT_ID,
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "http_status": http_status,
            "raw_provider_response_sha256": digest(raw),
            "state": "EMPTY_OUTPUT_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 3

    raw_output = output.encode("utf-8")
    (out / "raw-provider-response.json").write_bytes(raw)
    (out / "raw-output.md").write_bytes(raw_output)
    evidence = {
        "schema": "prompt-machine-starter-n09-gemini-wsl-observation-v3",
        "version": "3.0.0",
        "attempt_id": ATTEMPT_ID,
        "execution_id": execution_id,
        "case_id": CASE_ID,
        "workflow_id": case["workflow_id"],
        "provider": PROVIDER,
        "execution_surface": SURFACE,
        "execution_location": "USER_WSL",
        "model_requested": args.model,
        "provider_model_version": payload.get("modelVersion"),
        "provider_response_id": payload.get("responseId"),
        "runtime_envelope_bytes": EXPECTED_BYTES,
        "runtime_envelope_sha256": EXPECTED_SHA,
        "started_at": started_at,
        "completed_at": now(),
        "http_status": http_status,
        "request_id": headers.get("x-request-id") or headers.get("X-Request-Id"),
        "surface_submissions": 1,
        "provider_requests_attempted": 1,
        "automatic_retries": 0,
        "automatic_second_case": False,
        "behavioral_observations": 1,
        "raw_output_sha256": digest(raw_output),
        "raw_output_bytes": len(raw_output),
        "raw_provider_response_sha256": digest(raw),
        "usage_metadata": payload.get("usageMetadata"),
        "credential_value_recorded": False,
        "github_actions_used_for_runtime": False,
        "github_artifact_uploaded": False,
        "vercel_deployment_created": False,
        "certification_gate": "G05_BASELINE_EXECUTION",
        "human_review_required": True,
        "automatic_certification": False,
        "automatic_promotion": False,
        "state": "CLEAN_LOCAL_WSL_GEMINI_RUNTIME_OBSERVED_HUMAN_REVIEW_REQUIRED",
        "clean_surface_contract_version": clean["version"],
        "local_policy_version": policy["version"],
        "pipeline_version": pipeline["version"],
    }
    write_json(out / "runtime-evidence.json", evidence)
    write_json(
        out / "review-packet.json",
        {
            "schema": "prompt-machine-starter-n09-gemini-wsl-review-packet-v3",
            "attempt_id": ATTEMPT_ID,
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "review_status": "HUMAN_REVIEW_REQUIRED",
            "automatic_retry": False,
            "automatic_next_case": False,
            "automatic_certification": False,
            "promotion_claim": "NONE",
        },
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
