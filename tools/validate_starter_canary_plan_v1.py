#!/usr/bin/env python3
"""Static validation for Starter-specific behavioral canaries.

No model or provider call is made. The validator checks that every planned case
is disarmed, has an out-of-band evaluation contract, preserves authority/data
boundaries, and has not been represented as runtime evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "product" / "starter-collection-v1" / "evaluation"
PLAN_PATH = BASE / "STARTER_CANARY_PLAN_V1.json"

EXPECTED_CASES = {
    "PM-STARTER-CR-NORMAL-0001": ("pm-starter-evidence-first-code-review", "NORMAL", 1),
    "PM-STARTER-CR-EMBEDDED-OVERRIDE-0001": ("pm-starter-evidence-first-code-review", "EMBEDDED_OVERRIDE", 2),
    "PM-STARTER-BD-NORMAL-0001": ("pm-starter-evidence-first-bug-diagnosis", "NORMAL", 3),
    "PM-STARTER-BD-EMBEDDED-OVERRIDE-0001": ("pm-starter-evidence-first-bug-diagnosis", "EMBEDDED_OVERRIDE", 4),
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    plan = read_json(PLAN_PATH)
    assert plan["schema"] == "prompt-machine-starter-canary-plan-v1"
    assert plan["version"] == "1.0.0"
    assert plan["state"] == "PREPARED_DISARMED_ZERO_RUNTIME_CALLS"
    assert plan["risk"] == "LOW_ONLY"
    assert plan["authority"] == "ADVISORY_ONLY"
    assert plan["runtime_protocol"]["evaluation_contract_is_runtime_input"] is False
    assert plan["runtime_protocol"]["expected_state_is_runtime_input"] is False
    assert plan["runtime_protocol"]["maximum_submissions_before_human_review"] == 1
    assert plan["runtime_protocol"]["automatic_retries"] == 0
    assert plan["runtime_protocol"]["automatic_wave"] is False
    assert plan["runtime_protocol"]["automatic_promotion"] is False

    observed = {}
    for item in plan["cases"]:
        case_id = item["case_id"]
        assert case_id in EXPECTED_CASES
        workflow_id, variant, priority = EXPECTED_CASES[case_id]
        assert item["workflow_id"] == workflow_id
        assert item["variant"] == variant
        assert item["priority"] == priority
        assert item["armed"] is False

        case = read_json(ROOT / item["spec_path"])
        review = read_json(ROOT / item["evaluation_path"])
        assert case["schema"] == "prompt-machine-starter-canary-case-v1"
        assert case["case_id"] == case_id
        assert case["workflow_id"] == workflow_id
        assert case["variant"] == variant
        assert case["risk"] == "LOW"
        assert case["authority"] == "ADVISORY_ONLY"
        assert case["runtime_executed"] is False
        assert case["evaluation_contract_is_runtime_input"] is False
        assert case["instance_data_markdown"].strip()
        assert case["non_runtime_metadata"]["customer_evidence"] is False
        assert case["non_runtime_metadata"]["expected_result_not_present_in_runtime_input"] is True

        assert review["schema"] == "prompt-machine-starter-evaluation-contract-v1"
        assert review["version"] == "1.0.0"
        assert review["case_id"] == case_id
        assert review["workflow_id"] == workflow_id
        assert review["variant"] == variant
        assert review["evaluation_contract_is_runtime_input"] is False
        assert review["expected_result_is_runtime_input"] is False
        assert review["predeclared_before_runtime"] is True
        assert review["automatic_promotion"] is False
        assert review["runtime_executed"] is False
        assert review["human_review_required_after_runtime"] is True
        assert review["expected"]
        assert review["blocking_dimensions"]

        if variant == "EMBEDDED_OVERRIDE":
            assert case["non_runtime_metadata"]["embedded_override_is_task_data"] is True
            assert review["expected"]["embedded_override_must_be_treated_as"] == "UNTRUSTED_TASK_DATA"
            assert "instruction_data_boundary_preserved" in review["blocking_dimensions"]

        observed[case_id] = True

    assert set(observed) == set(EXPECTED_CASES)
    assert plan["current_next_case"]["case_id"] == "PM-STARTER-CR-NORMAL-0001"
    assert plan["current_next_case"]["armed"] is False
    assert plan["truth"]["prepared_cases"] == 4
    assert plan["truth"]["runtime_observations"] == 0
    assert plan["truth"]["model_calls_created_by_plan"] == 0
    assert plan["truth"]["behavioral_claims_created_by_plan"] == 0
    assert plan["truth"]["ready_to_sell"] is False

    print("STARTER CANARY PLAN V1: PASS")
    print("prepared_cases=4")
    print("out_of_band_evaluation_contracts=4")
    print("armed_cases=0")
    print("runtime_observations=0")
    print("model_calls=0")
    print("provider_calls=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
