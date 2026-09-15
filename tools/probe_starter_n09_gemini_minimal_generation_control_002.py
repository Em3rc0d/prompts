#!/usr/bin/env python3
"""Zero-model preflight for PM-GEMINI-MINIMAL-GEN-CTRL-002.

No provider request and no model inference are made. The tool verifies the frozen
control, local WSL/key prerequisites, one-request/zero-retry budget, and that the
corrected thinking/output configuration is present before fresh authorization.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "commercial/STARTER_N09_GEMINI_MINIMAL_GENERATION_CONTROL_002_PLAN.json"
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
EXECUTOR_PATH = ROOT / "tools/execute_starter_n09_gemini_minimal_generation_control_002.py"
CONTROL_ID = "PM-GEMINI-MINIMAL-GEN-CTRL-002"
MODEL = "gemini-3.5-flash"
PROMPT = "Return exactly: OK"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def is_wsl() -> bool:
    p = Path("/proc/version")
    text = p.read_text(encoding="utf-8", errors="ignore").lower() if p.exists() else ""
    return "microsoft" in text or "wsl" in text


def main() -> int:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    config = plan.get("generation_config") or {}
    thinking = config.get("thinkingConfig") or {}
    auth_state = str(policy.get("current_authorization_state", ""))
    out = Path(os.path.expandvars(os.path.expanduser(plan.get("output_directory", "")))).resolve()

    checks = {
        "control_id_exact": plan.get("control_id") == CONTROL_ID,
        "control_is_not_g05": plan.get("g05_claim") == "NONE",
        "plan_state_preflight_required": plan.get("state") == "PREPARED_ZERO_MODEL_PREFLIGHT_REQUIRED",
        "model_frozen": plan.get("model") == MODEL,
        "minimal_prompt_exact": plan.get("prompt") == PROMPT,
        "thinking_level_minimal": thinking.get("thinkingLevel") == "minimal",
        "max_output_tokens_64": config.get("maxOutputTokens") == 64,
        "single_request": plan.get("maximum_provider_requests") == 1,
        "zero_retries": plan.get("automatic_retries") == 0,
        "fresh_authorization_required": plan.get("fresh_explicit_authorization_required") is True,
        "workflow_candidate_not_sent": plan.get("workflow_candidate_sent") is False,
        "evaluation_contract_not_sent": plan.get("evaluation_contract_sent") is False,
        "behavioral_observation_forbidden": plan.get("behavioral_observation_allowed") is False,
        "local_only_policy_active": policy.get("policy_state") == "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER",
        "repository_authorization_disarmed": auth_state.startswith("DISARMED_") and auth_state.endswith("_CONSUMED"),
        "gemini_api_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "wsl_detected": is_wsl(),
        "executor_present": EXECUTOR_PATH.exists(),
        "output_dir_absent": not out.exists(),
    }
    verdict = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "schema": "prompt-machine-starter-n09-gemini-minimal-generation-control-preflight-v2",
        "control_id": CONTROL_ID,
        "provider": "GOOGLE_GEMINI_API",
        "model": MODEL,
        "prompt": PROMPT,
        "generation_config": config,
        "checks": checks,
        "provider_request_made": False,
        "model_inference_made": False,
        "g05_claim": "NONE",
        "recorded_at": now(),
        "verdict": verdict,
        "next_gate_if_pass": "FRESH_EXPLICIT_AUTHORIZATION_FOR_PM_GEMINI_MINIMAL_GEN_CTRL_002",
    }
    report = Path.home() / ".local/share/prompt-machine/n09/provider-min-gen-002-preflight.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={report}")
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
