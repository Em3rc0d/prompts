#!/usr/bin/env python3
"""Zero-model preflight for Starter N09 on the user's local WSL.

This script never calls Gemini and never prints or persists GEMINI_API_KEY.
It validates local capability, frozen Prompt Machine contracts, and Attempt 002 readiness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PM-STARTER-CR-NORMAL-0001"
CASE_PATH = ROOT / "product/starter-collection-v1/evaluation/cases/PM-STARTER-CR-NORMAL-0001.json"
CLEAN_PATH = ROOT / "commercial/STARTER_CLEAN_RUNTIME_SURFACE_REQUIREMENTS_V1.json"
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
PIPELINE_PATH = ROOT / "commercial/PROMPT_MACHINE_14_GATE_PIPELINE_V1.json"
PLAN_PATH = ROOT / "commercial/STARTER_N09_GEMINI_WSL_ATTEMPT_002_PLAN.json"
EXECUTOR_PATH = ROOT / "tools/execute_starter_n09_gemini_wsl_v2.py"
EXPECTED_BYTES = 8100
EXPECTED_SHA = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
EXPECTED_MODEL = "gemini-3.8-flash"


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


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_wsl() -> bool:
    p = Path("/proc/version")
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8", errors="ignore").lower()
    return "microsoft" in text or "wsl" in text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.home() / ".local/share/prompt-machine/n09/preflight-attempt-002.json",
    )
    args = parser.parse_args()

    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    clean = json.loads(CLEAN_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    pipeline = json.loads(PIPELINE_PATH.read_text(encoding="utf-8"))
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    workflow = (ROOT / case["workflow_surface_path"]).read_text(encoding="utf-8")
    envelope = render(workflow, case["instance_data_markdown"])
    planned_output = Path.home() / ".local/share/prompt-machine/n09/g05-baseline-002"
    auth_state = str(policy.get("current_authorization_state", ""))

    checks = {
        "wsl_detected": is_wsl(),
        "gemini_api_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "case_identity_exact": case.get("case_id") == CASE_ID,
        "evaluation_contract_excluded": case.get("evaluation_contract_is_runtime_input") is False,
        "clean_surface_zero_retries": clean.get("automatic_retries") == 0,
        "local_only_policy_active": policy.get("policy_state") == "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER",
        "execution_location_is_user_wsl": policy.get("execution_location") == "USER_WSL",
        "provider_is_google_gemini_api": policy.get("inference_provider") == "GOOGLE_GEMINI_API",
        "credential_env_is_gemini_api_key": policy.get("credential_environment_variable") == "GEMINI_API_KEY",
        "github_actions_runtime_disabled": policy.get("github_actions_runtime_trigger_allowed") is False,
        "github_artifact_runtime_upload_disabled": policy.get("github_artifact_upload_of_runtime_output_allowed") is False,
        "repository_authorization_disarmed": auth_state.startswith("DISARMED_") and auth_state.endswith("_CONSUMED"),
        "pipeline_has_14_gates": len(pipeline.get("gates") or []) == 14,
        "pipeline_master_invariant_intact": pipeline.get("master_invariant") == "NO PROMPT MAY ENTER A RELEASE WITHOUT A PROMPT_ID + SPEC + TEST EVIDENCE + CERTIFICATION DECISION",
        "attempt_002_plan_present": plan.get("attempt_id") == "G05-BASELINE-002",
        "attempt_002_fresh_auth_required": plan.get("state") == "PREPARED_FRESH_AUTH_REQUIRED" and plan.get("fresh_explicit_authorization_required") is True,
        "attempt_002_same_candidate": plan.get("candidate_mutated_since_attempt_001") is False,
        "attempt_002_model_frozen": plan.get("model") == EXPECTED_MODEL,
        "attempt_002_zero_retries": plan.get("automatic_retries") == 0,
        "attempt_002_single_request": plan.get("maximum_provider_requests") == 1,
        "attempt_002_output_dir_absent": not planned_output.exists(),
        "attempt_002_executor_present": EXECUTOR_PATH.is_file(),
        "envelope_bytes_exact": len(envelope) == EXPECTED_BYTES,
        "envelope_sha256_exact": sha256(envelope) == EXPECTED_SHA,
        "evaluation_markers_absent": not any(
            marker in envelope
            for marker in [b"expected_state", b"blocking_dimensions", b"assessment_answer_key"]
        ),
    }

    report = {
        "schema": "prompt-machine-starter-n09-gemini-wsl-preflight-v2",
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "case_id": CASE_ID,
        "attempt_id": "G05-BASELINE-002",
        "execution_location": "USER_WSL",
        "provider": "GOOGLE_GEMINI_API",
        "model": EXPECTED_MODEL,
        "model_call_made": False,
        "provider_request_made": False,
        "credential_value_read_into_report": False,
        "runtime_envelope_bytes": len(envelope),
        "runtime_envelope_sha256": sha256(envelope),
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "next_gate_if_pass": "FRESH_EXPLICIT_RUNTIME_AUTHORIZATION_FOR_G05_BASELINE_002",
    }

    out = args.output.expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={out}")
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
