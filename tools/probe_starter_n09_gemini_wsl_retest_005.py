#!/usr/bin/env python3
"""Zero-model preflight for G05-RETEST-005 on local WSL."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PM-STARTER-CR-NORMAL-0001"
ATTEMPT_ID = "G05-RETEST-005"
EXPECTED_MODEL = "gemini-3.5-flash"
EXPECTED_BYTES = 8100
EXPECTED_SHA = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
CASE_PATH = ROOT / "product/starter-collection-v1/evaluation/cases/PM-STARTER-CR-NORMAL-0001.json"
CLEAN_PATH = ROOT / "commercial/STARTER_CLEAN_RUNTIME_SURFACE_REQUIREMENTS_V1.json"
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
PIPELINE_PATH = ROOT / "commercial/PROMPT_MACHINE_14_GATE_PIPELINE_V1.json"
PLAN_PATH = ROOT / "commercial/STARTER_N09_GEMINI_WSL_RETEST_005_PLAN.json"
CONTROL_RECEIPT_PATH = ROOT / "commercial/STARTER_N09_GEMINI_MINIMAL_GENERATION_CONTROL_002_RECEIPT_2026-09-07.json"
EXECUTOR_PATH = ROOT / "tools/execute_starter_n09_gemini_wsl_v5.py"
OUT = Path.home() / ".local/share/prompt-machine/n09/g05-retest-005"
REPORT = Path.home() / ".local/share/prompt-machine/n09/preflight-retest-005.json"


def norm(s: str) -> str:
    return s.rstrip("\n") + "\n"


def render(surface: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + norm(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + norm(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def main() -> int:
    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    clean = json.loads(CLEAN_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    pipeline = json.loads(PIPELINE_PATH.read_text(encoding="utf-8"))
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    control = json.loads(CONTROL_RECEIPT_PATH.read_text(encoding="utf-8"))
    workflow = (ROOT / case["workflow_surface_path"]).read_text(encoding="utf-8")
    envelope = render(workflow, case["instance_data_markdown"])
    auth_state = str(policy.get("current_authorization_state", ""))
    proc = Path("/proc/version").read_text(errors="ignore").lower() if Path("/proc/version").exists() else ""

    checks = {
        "wsl_detected": "microsoft" in proc or "wsl" in proc,
        "gemini_api_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "case_identity_exact": case.get("case_id") == CASE_ID,
        "evaluation_contract_excluded": case.get("evaluation_contract_is_runtime_input") is False,
        "clean_surface_zero_retries": clean.get("automatic_retries") == 0,
        "local_only_policy_active": policy.get("policy_state") == "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER",
        "provider_is_google_gemini_api": policy.get("inference_provider") == "GOOGLE_GEMINI_API",
        "repository_authorization_disarmed": auth_state.startswith("DISARMED_") and auth_state.endswith("_CONSUMED"),
        "pipeline_has_14_gates": len(pipeline.get("gates") or []) == 14,
        "pipeline_master_invariant_intact": pipeline.get("master_invariant") == "NO PROMPT MAY ENTER A RELEASE WITHOUT A PROMPT_ID + SPEC + TEST EVIDENCE + CERTIFICATION DECISION",
        "retest_plan_present": plan.get("attempt_id") == ATTEMPT_ID,
        "retest_plan_state_ready_for_auth": plan.get("state") == "PREPARED_FRESH_AUTH_REQUIRED",
        "retest_model_frozen": plan.get("model") == EXPECTED_MODEL,
        "retest_is_provider_recovery_scope": plan.get("experiment_class") == "GOVERNED_PROVIDER_RECOVERY_RETEST",
        "minimal_generation_control_002_pass": control.get("control_id") == "PM-GEMINI-MINIMAL-GEN-CTRL-002" and control.get("control_pass") is True and control.get("response_text_exact_ok") is True and control.get("http_status") == 200,
        "candidate_prompt_unchanged": plan.get("candidate_prompt_mutated") is False,
        "request_config_matches_004": plan.get("request_configuration_matches_g05_fallback_004") is True and plan.get("generation_config", {}).get("maxOutputTokens") == 4096,
        "single_request": plan.get("maximum_provider_requests") == 1,
        "zero_retries": plan.get("automatic_retries") == 0,
        "output_dir_absent": not OUT.exists(),
        "executor_present": EXECUTOR_PATH.exists(),
        "envelope_bytes_exact": len(envelope) == EXPECTED_BYTES,
        "envelope_sha256_exact": hashlib.sha256(envelope).hexdigest() == EXPECTED_SHA,
        "evaluation_markers_absent": not any(x in envelope for x in (b"expected_state", b"blocking_dimensions", b"assessment_answer_key")),
    }
    report = {
        "schema": "prompt-machine-starter-n09-gemini-wsl-retest-preflight-v1",
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "attempt_id": ATTEMPT_ID,
        "case_id": CASE_ID,
        "provider": "GOOGLE_GEMINI_API",
        "model": EXPECTED_MODEL,
        "runtime_envelope_bytes": len(envelope),
        "runtime_envelope_sha256": hashlib.sha256(envelope).hexdigest(),
        "generation_config": {"maxOutputTokens": 4096},
        "provider_request_made": False,
        "model_call_made": False,
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "next_gate_if_pass": "FRESH_EXPLICIT_RUNTIME_AUTHORIZATION_FOR_G05_RETEST_005",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={REPORT}")
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
