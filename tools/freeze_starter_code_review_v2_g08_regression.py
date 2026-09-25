#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_DESIGN_V1.json"
G07 = ROOT / "commercial/STARTER_N09_G07_SUCCESSOR_STATIC_AUDIT_PASS_2026-09-07.json"
REPORT = Path.home() / ".local/share/prompt-machine/n09/g08-v2-regression-freeze.json"
EXPECTED_WORKFLOW_ID = "pm-starter-evidence-first-code-review-v2"
EXPECTED_CASES = [
    "PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001",
    "PM-STARTER-CR-V2-EMBEDDED-OVERRIDE-0001",
    "PM-STARTER-CR-V2-UPSTREAM-GUARD-0001",
    "PM-STARTER-CR-V2-FULL-CHAIN-NO-GUARD-0001",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(text: str) -> str:
    return text.rstrip("\n") + "\n"


def render(surface: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + norm(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + norm(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def main() -> int:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    g07 = json.loads(G07.read_text(encoding="utf-8"))
    workflow_path = ROOT / design["workflow_surface_path"]
    workflow_text = workflow_path.read_text(encoding="utf-8") if workflow_path.exists() else ""

    rows = design.get("regression_cases") or []
    case_ids = [row.get("case_id") for row in rows]
    checks = {
        "g07_pass_recorded": g07.get("verdict") == "PASS",
        "design_state_zero_model_freeze_required": design.get("state") == "PREPARED_ZERO_MODEL_FREEZE_REQUIRED",
        "workflow_id_exact": design.get("workflow_id") == EXPECTED_WORKFLOW_ID,
        "workflow_surface_present": workflow_path.exists(),
        "workflow_surface_id_exact": f"Workflow ID: `{EXPECTED_WORKFLOW_ID}`" in workflow_text,
        "four_cases_exact": case_ids == EXPECTED_CASES,
        "execution_order_exact": design.get("execution_order") == EXPECTED_CASES,
        "fresh_auth_per_case": design.get("runtime_governance", {}).get("fresh_explicit_authorization_required_per_case") is True,
        "single_request_per_auth": design.get("runtime_governance", {}).get("maximum_provider_requests_per_authorization") == 1,
        "zero_retries": design.get("runtime_governance", {}).get("automatic_retries") == 0,
        "automatic_next_case_false": design.get("runtime_governance", {}).get("automatic_next_case") is False,
        "human_review_after_each": design.get("runtime_governance", {}).get("human_review_required_after_each_case") is True,
    }

    frozen_cases = []
    for row in rows:
        case_path = ROOT / row["case_path"]
        evaluation_path = ROOT / row["evaluation_path"]
        case = json.loads(case_path.read_text(encoding="utf-8")) if case_path.exists() else {}
        evaluation = json.loads(evaluation_path.read_text(encoding="utf-8")) if evaluation_path.exists() else {}
        envelope = render(workflow_text, case.get("instance_data_markdown", "")) if case_path.exists() and workflow_path.exists() else b""
        per_case_checks = {
            "case_present": case_path.exists(),
            "evaluation_present": evaluation_path.exists(),
            "case_id_exact": case.get("case_id") == row["case_id"],
            "case_workflow_id_exact": case.get("workflow_id") == EXPECTED_WORKFLOW_ID,
            "case_workflow_path_exact": case.get("workflow_surface_path") == design.get("workflow_surface_path"),
            "case_eval_not_runtime_input": case.get("evaluation_contract_is_runtime_input") is False,
            "evaluation_case_exact": evaluation.get("case_id") == row["case_id"],
            "evaluation_workflow_exact": evaluation.get("workflow_id") == EXPECTED_WORKFLOW_ID,
            "evaluation_not_runtime_input": evaluation.get("evaluation_contract_is_runtime_input") is False,
            "expected_result_not_runtime_input": evaluation.get("expected_result_is_runtime_input") is False,
            "predeclared_before_runtime": evaluation.get("predeclared_before_runtime") is True,
            "human_review_required": evaluation.get("human_review_required_after_runtime") is True,
            "automatic_promotion_false": evaluation.get("automatic_promotion") is False,
            "runtime_not_executed": case.get("runtime_executed") is False,
            "envelope_nonempty": len(envelope) > 0,
        }
        checks[f"case_{row['case_id']}_contract_pass"] = all(per_case_checks.values())
        frozen_cases.append({
            "case_id": row["case_id"],
            "target": row["target"],
            "case_path": row["case_path"],
            "evaluation_path": row["evaluation_path"],
            "case_file_sha256": sha(file_bytes(case_path)) if case_path.exists() else None,
            "evaluation_file_sha256": sha(file_bytes(evaluation_path)) if evaluation_path.exists() else None,
            "instance_data_bytes": len(case.get("instance_data_markdown", "").encode("utf-8")),
            "instance_data_sha256": sha(case.get("instance_data_markdown", "").encode("utf-8")),
            "runtime_envelope_bytes": len(envelope),
            "runtime_envelope_sha256": sha(envelope),
            "checks": per_case_checks,
        })

    report = {
        "schema": "prompt-machine-starter-n09-g08-v2-regression-freeze-receipt-v1",
        "recorded_at": now(),
        "workflow_id": EXPECTED_WORKFLOW_ID,
        "workflow_surface_path": design.get("workflow_surface_path"),
        "workflow_surface_bytes": len(workflow_text.encode("utf-8")),
        "workflow_surface_sha256": sha(workflow_text.encode("utf-8")),
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "runtime_executions_attempted": 0,
        "checks": checks,
        "frozen_cases": frozen_cases,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "next_gate_if_pass": "PREPARE_FIRST_G08_CASE_EXECUTOR_AND_ZERO_MODEL_PREFLIGHT_NO_RUNTIME_AUTHORIZATION_YET",
        "truth_boundary": "ZERO_MODEL_REGRESSION_FREEZE_ONLY_NO_V2_RUNTIME_EVIDENCE",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={REPORT}")
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
