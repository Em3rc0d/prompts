#!/usr/bin/env python3
"""Fail-closed validation for Prompt Machine Workflow Learning Loop v1.

This validator is deterministic. It does not execute a model and cannot create
behavioral, certification, product-readiness, or revenue evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "quarry" / "learning-loop" / "LEARNING_LOOP_POLICY_V1.json"

EXPECTED_EVIDENCE_CLASSES = {
    "UNTRUSTED_CLIENT_INTENT",
    "USER_REPORTED_OUTCOME",
    "RUNTIME_OBSERVATION",
    "HUMAN_REVIEW",
    "REGRESSION_EVIDENCE",
    "PROVIDER_SIGNED_PURCHASE_EVIDENCE",
    "DELIVERY_EVIDENCE",
    "RETURN_USE_EVIDENCE",
}

EXPECTED_DECISIONS = {"RETAIN", "REWORK", "RETIRE", "EXPAND_EVIDENCE"}

REQUIRED_FAILURES = {
    "INSTRUCTION_DATA_BOUNDARY_FAILURE",
    "UNSUPPORTED_MATERIAL_CLAIM",
    "MISSING_REQUIRED_INPUT_NOT_BLOCKED",
    "WRONG_STATE",
    "OUTPUT_CONTRACT_FAILURE",
    "AUTHORITY_ESCALATION",
    "UNCERTAINTY_COLLAPSE",
    "CONTRADICTION_MISHANDLED",
    "VERIFICATION_GAP",
    "TASK_FAILURE",
    "UX_FRICTION",
    "NO_FAILURE_OBSERVED",
}


def main() -> int:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))

    assert policy["schema"] == "prompt-machine-learning-loop-policy-v1"
    assert policy["version"] == "1.0.0"
    assert policy["state"] == "STATIC_POLICY_DEFINED_BEHAVIOR_UNEXECUTED"

    # No unattended maturity or spend escalation.
    assert policy["automatic_promotion"] is False
    assert policy["automatic_wave_execution"] is False
    assert policy["overwrite_observed_versions"] is False

    assert set(policy["evidence_classes"]) == EXPECTED_EVIDENCE_CLASSES
    assert set(policy["review_decisions"]) == EXPECTED_DECISIONS
    assert set(policy["failure_taxonomy"]) == REQUIRED_FAILURES

    successor = policy["successor_rules"]
    assert successor["predecessor_must_remain_immutable"] is True
    assert successor["must_record_change_hypothesis"] is True
    assert successor["must_record_changed_semantics"] is True
    assert successor["must_record_target_failure"] is True
    assert successor["must_record_possible_regressions"] is True
    assert successor["must_define_regression_set"] is True

    regression = policy["regression_rules"]
    assert regression["predecessor_evidence_inheritance"] is False
    assert set(regression["required_case_classes"]) == {"TRIGGERING_FAILURE", "NORMAL"}
    assert set(regression["allowed_results"]) == {"PASS", "FAIL", "INCONCLUSIVE"}
    assert regression["evidence_eligibility_requires"] == "PASS"

    boundaries = policy["promotion_boundaries"]
    assert boundaries["runtime_observation_implies_certification"] is False
    assert boundaries["regression_pass_implies_ready_to_sell"] is False
    assert boundaries["product_eligible_implies_ready_to_sell"] is False
    assert boundaries["client_intent_implies_customer_value"] is False
    assert boundaries["user_report_implies_runtime_reliability"] is False
    assert boundaries["purchase_implies_retention"] is False

    canary = policy["current_canary"]
    assert canary["invocation_id"] == "PM-INV-CHECKLIST-NORMAL-0003"
    assert canary["state"] == "PREPARED_NOT_EXECUTED"
    assert canary["maximum_calls_before_review"] == 1
    assert canary["next_step_after_observation"] == "HUMAN_REVIEW"
    assert set(canary["allowed_post_review_decisions"]) == EXPECTED_DECISIONS

    truth = policy["truth"]
    assert truth["behavioral_observations"] == 0
    assert truth["real_customer_outcomes"] == 0
    assert truth["real_purchases"] == 0
    assert truth["ready_to_sell"] is False

    print("WORKFLOW LEARNING LOOP POLICY V1: PASS")
    print("external_model_calls=0")
    print("behavioral_claims_created=0")
    print("automatic_promotion=BLOCKED")
    print("automatic_wave_execution=BLOCKED")
    print("current_canary=PM-INV-CHECKLIST-NORMAL-0003")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
