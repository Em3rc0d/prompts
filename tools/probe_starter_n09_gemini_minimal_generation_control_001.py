#!/usr/bin/env python3
"""Zero-model preflight for PM-GEMINI-MINIMAL-GEN-CTRL-001.

This script performs no provider request and no model inference. It validates that the
minimal generation control is ready for a separately authorized single request.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "commercial/STARTER_N09_GEMINI_MINIMAL_GENERATION_CONTROL_001_PLAN.json"
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
EXECUTOR_PATH = ROOT / "tools/execute_starter_n09_gemini_minimal_generation_control_001.py"
CONTROL_ID = "PM-GEMINI-MINIMAL-GEN-CTRL-001"
EXPECTED_MODEL = "gemini-3.5-flash"
EXPECTED_PROMPT = "Return exactly: OK"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def is_wsl() -> bool:
    p = Path("/proc/version")
    text = p.read_text(errors="ignore").lower() if p.exists() else ""
    return "microsoft" in text or "wsl" in text


def main() -> int:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    out = Path.home() / ".local/share/prompt-machine/n09/provider-min-gen-001"
    auth_state = str(policy.get("current_authorization_state", ""))

    checks = {
        "wsl_detected": is_wsl(),
        "gemini_api_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "control_id_exact": plan.get("control_id") == CONTROL_ID,
        "control_is_not_g05": plan.get("experiment_class") == "PROVIDER_GENERATION_PATH_DIAGNOSTIC_NOT_G05",
        "plan_state_preflight_required": plan.get("state") == "PREPARED_ZERO_MODEL_PREFLIGHT_REQUIRED",
        "model_frozen": plan.get("model") == EXPECTED_MODEL,
        "minimal_prompt_exact": plan.get("prompt") == EXPECTED_PROMPT,
        "workflow_candidate_not_sent": plan.get("workflow_candidate_sent") is False,
        "evaluation_contract_not_sent": plan.get("evaluation_contract_sent") is False,
        "single_request": plan.get("maximum_provider_requests") == 1,
        "zero_retries": plan.get("automatic_retries") == 0,
        "fresh_authorization_required": plan.get("fresh_explicit_authorization_required") is True,
        "behavioral_observation_forbidden": plan.get("behavioral_observation_allowed") is False,
        "local_only_policy_active": policy.get("policy_state") == "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER",
        "repository_authorization_disarmed": auth_state.startswith("DISARMED_") and auth_state.endswith("_CONSUMED"),
        "executor_present": EXECUTOR_PATH.is_file(),
        "output_dir_absent": not out.exists(),
    }

    report = {
        "schema": "prompt-machine-starter-n09-gemini-minimal-generation-control-preflight-v1",
        "recorded_at": now(),
        "control_id": CONTROL_ID,
        "provider": "GOOGLE_GEMINI_API",
        "model": EXPECTED_MODEL,
        "prompt": EXPECTED_PROMPT,
        "provider_request_made": False,
        "model_inference_made": False,
        "g05_claim": "NONE",
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "next_gate_if_pass": "FRESH_EXPLICIT_AUTHORIZATION_FOR_PM_GEMINI_MINIMAL_GEN_CTRL_001",
    }

    report_path = Path.home() / ".local/share/prompt-machine/n09/provider-min-gen-001-preflight.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={report_path}")
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
