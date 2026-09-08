#!/usr/bin/env python3
"""Zero-model preflight for the first G08 v2 regression case."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001"
WORKFLOW_ID = "pm-starter-evidence-first-code-review-v2"
EXPECTED_MODEL = "gemini-3.5-flash"
EXPECTED_BYTES = 12008
EXPECTED_SHA = "72cfc51bca3b09d88f6230f51a706735ecb985b4c541093833c2ea64a10b6b92"
CASE_PATH = ROOT / "product/starter-collection-v2/evaluation/cases/PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001.json"
EVAL_PATH = ROOT / "product/starter-collection-v2/evaluation/reviews/PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001.evaluation.json"
WORKFLOW_PATH = ROOT / "product/starter-collection-v2/workflows/evidence-first-code-review.md"
DESIGN_PATH = ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_DESIGN_V1.json"
FREEZE_PATH = ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_FREEZE_RECEIPT_2026-09-07.json"
PLAN_PATH = ROOT / "commercial/STARTER_N09_G08_V2_BOUNDARY_UNKNOWN_001_PLAN.json"
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
EXECUTOR_PATH = ROOT / "tools/execute_starter_code_review_v2_g08_boundary_unknown_001.py"
OUT = Path.home() / ".local/share/prompt-machine/n09/g08-v2-boundary-unknown-001"
REPORT = Path.home() / ".local/share/prompt-machine/n09/g08-v2-boundary-unknown-001-preflight.json"


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


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    evaluation = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    design = json.loads(DESIGN_PATH.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    envelope = render(workflow, case["instance_data_markdown"])
    frozen = [x for x in freeze.get("frozen_cases", []) if x.get("case_id") == CASE_ID]
    proc = Path("/proc/version").read_text(errors="ignore").lower() if Path("/proc/version").exists() else ""
    order = design.get("execution_order") or []
    frozen_case = frozen[0] if len(frozen) == 1 else {}

    checks = {
        "wsl_detected": "microsoft" in proc or "wsl" in proc,
        "gemini_api_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "case_identity_exact": case.get("case_id") == CASE_ID,
        "workflow_identity_exact": case.get("workflow_id") == WORKFLOW_ID,
        "evaluation_contract_excluded": case.get("evaluation_contract_is_runtime_input") is False and evaluation.get("evaluation_contract_is_runtime_input") is False,
        "expected_result_excluded": evaluation.get("expected_result_is_runtime_input") is False,
        "evaluation_predeclared": evaluation.get("predeclared_before_runtime") is True,
        "freeze_receipt_pass": freeze.get("verdict") == "PASS",
        "freeze_zero_model": freeze.get("provider_requests_attempted") == 0 and freeze.get("model_inference_requests_attempted") == 0 and freeze.get("runtime_executions_attempted") == 0,
        "frozen_case_unique": len(frozen) == 1,
        "frozen_envelope_bytes_exact": frozen_case.get("runtime_envelope_bytes") == EXPECTED_BYTES,
        "frozen_envelope_sha_exact": frozen_case.get("runtime_envelope_sha256") == EXPECTED_SHA,
        "rendered_envelope_bytes_exact": len(envelope) == EXPECTED_BYTES,
        "rendered_envelope_sha_exact": sha(envelope) == EXPECTED_SHA,
        "evaluation_markers_absent": not any(x in envelope for x in (b'"expected"', b'"blocking_dimensions"', b'expected_result_is_runtime_input')),
        "execution_order_first_case": len(order) >= 1 and order[0] == CASE_ID,
        "design_fresh_auth_per_case": design.get("runtime_governance", {}).get("fresh_explicit_authorization_required_per_case") is True,
        "design_single_request": design.get("runtime_governance", {}).get("maximum_provider_requests_per_authorization") == 1,
        "design_zero_retries": design.get("runtime_governance", {}).get("automatic_retries") == 0,
        "design_no_automatic_next_case": design.get("runtime_governance", {}).get("automatic_next_case") is False,
        "plan_state_preflight_required": plan.get("state") == "PREPARED_ZERO_MODEL_PREFLIGHT_REQUIRED",
        "plan_model_frozen": plan.get("model") == EXPECTED_MODEL,
        "plan_single_request": plan.get("maximum_provider_requests") == 1,
        "plan_zero_retries": plan.get("automatic_retries") == 0,
        "plan_no_automatic_next_case": plan.get("automatic_next_case") is False,
        "human_review_required": plan.get("human_review_required") is True,
        "local_only_policy_active": policy.get("policy_state") == "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER",
        "provider_is_google_gemini_api": policy.get("inference_provider") == "GOOGLE_GEMINI_API",
        "executor_present": EXECUTOR_PATH.exists(),
        "output_dir_absent": not OUT.exists(),
    }
    report = {
        "schema": "prompt-machine-starter-n09-g08-v2-boundary-unknown-001-preflight-v1",
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "case_id": CASE_ID,
        "workflow_id": WORKFLOW_ID,
        "provider": "GOOGLE_GEMINI_API",
        "model": EXPECTED_MODEL,
        "generation_config": {"maxOutputTokens": 4096},
        "runtime_envelope_bytes": len(envelope),
        "runtime_envelope_sha256": sha(envelope),
        "provider_request_made": False,
        "model_inference_made": False,
        "runtime_execution_made": False,
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "next_gate_if_pass": "FRESH_EXPLICIT_AUTHORIZATION_FOR_PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001",
        "authorization_format": "AUTORIZO PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001: 1 ejecución, 0 reintentos.",
        "truth_boundary": "ZERO_MODEL_PREFLIGHT_ONLY_NO_G08_RUNTIME_OBSERVATION",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={REPORT}")
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
