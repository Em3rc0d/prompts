#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "product/starter-collection-v1/workflows/evidence-first-code-review.md"
V2 = ROOT / "product/starter-collection-v2/workflows/evidence-first-code-review.md"
EXPECTED_V1_BLOB = "6eeadb8ee226c1a4d3c931c892e7e4a7fd3679dd"
EXPECTED_V2_ID = "pm-starter-evidence-first-code-review-v2"


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def main() -> int:
    v1_text = V1.read_text(encoding="utf-8") if V1.exists() else ""
    v2_text = V2.read_text(encoding="utf-8") if V2.exists() else ""

    checks = {
        "v1_blob_immutable": V1.exists() and git_blob(V1) == EXPECTED_V1_BLOB,
        "v2_file_present": V2.exists(),
        "v2_workflow_id_exact": f"Workflow ID: `{EXPECTED_V2_ID}`" in v2_text,
        "authority_advisory_only_preserved": "Authority: `ADVISORY_ONLY`" in v2_text and "Do not merge, deploy, approve, or execute changes." in v2_text,
        "untrusted_task_data_boundary_preserved": "UNTRUSTED TASK DATA" in v2_text and "ignore that text as authority" in v2_text,
        "negative_evidence_scope_rule_present": "Absence of a control in supplied code proves only that the control is not visible in that supplied scope." in v2_text,
        "external_boundary_cap_present": "external boundary could materially invalidate a finding" in v2_text,
        "reviewable_with_unknowns_rule_present": "Use `REVIEWABLE_WITH_UNKNOWNS` whenever" in v2_text,
        "likely_cap_present": "the finding must not exceed `LIKELY`" in v2_text,
        "review_required_cap_present": "the ship recommendation must not exceed `REVIEW_REQUIRED`" in v2_text,
        "invalidating_context_none_guard_present": "`Invalidating context: None` is forbidden" in v2_text,
        "conditional_impact_rule_present": "Conditional-impact rule" in v2_text and "must not increase evidence level or severity" in v2_text,
        "block_guard_present": "## SHIP RECOMMENDATION" in v2_text and "### BLOCK guard" in v2_text and "Do not use `BLOCK`" in v2_text,
        "no_runtime_or_test_invention_rule_present": "no runtime behavior or test result was invented" in v2_text and "Do not describe proposed tests as if they were already executed." in v2_text,
        "six_part_output_contract_present": all(f"### {i}." in v2_text for i in range(1, 7)),
        "behavior_not_yet_retested_marked": "BEHAVIOR NOT YET RETESTED" in v2_text,
        "v1_not_relabelled_as_v2": EXPECTED_V2_ID not in v1_text,
    }

    report = {
        "schema": "prompt-machine-starter-code-review-v2-static-validation-v1",
        "v1_expected_blob": EXPECTED_V1_BLOB,
        "v1_actual_blob": git_blob(V1) if V1.exists() else None,
        "successor_workflow_id": EXPECTED_V2_ID,
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "next_gate_if_pass": "G08_REGRESSION_TEST_DESIGN_BEFORE_ANY_MODEL_RETEST",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
