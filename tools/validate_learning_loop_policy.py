#!/usr/bin/env python3
"""Fail-closed validation for the frozen Prompt Machine Learning Loop v1 baseline.

This validator intentionally checks the immutable pre-behavior policy snapshot.
Current behavioral campaign truth lives in the governed campaign ledger and must
not be confused with the frozen baseline. This validator is deterministic, makes
no model calls, and creates no behavioral, certification, product-readiness, or
revenue evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "quarry" / "learning-loop" / "LEARNING_LOOP_POLICY_V1.json"
LEDGER = ROOT / "quarry" / "etl" / "prompt-library-v1" / "manual-canary-campaign-v1" / "ledger.json"

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
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

    assert policy["schema"] == "prompt-machine-learning-loop-policy-v1"
    assert policy["version"] == "1.0.0"
    assert policy["state"] == "STATIC_POLICY_DEFINED_BEHAVIOR_UNEXECUTED"

    # No unattended maturity or spend escalation in the frozen baseline.
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

    baseline_canary = policy["current_canary"]
    assert baseline_canary["invocation_id"] == "PM-INV-CHECKLIST-NORMAL-0003"
    assert baseline_canary["state"] == "PREPARED_NOT_EXECUTED"
    assert baseline_canary["maximum_calls_before_review"] == 1
    assert baseline_canary["next_step_after_observation"] == "HUMAN_REVIEW"
    assert set(baseline_canary["allowed_post_review_decisions"]) == EXPECTED_DECISIONS

    baseline_truth = policy["truth"]
    assert baseline_truth["behavioral_observations"] == 0
    assert baseline_truth["real_customer_outcomes"] == 0
    assert baseline_truth["real_purchases"] == 0
    assert baseline_truth["ready_to_sell"] is False

    # Current campaign truth is deliberately separate from the frozen policy.
    assert ledger["campaign_id"] == "PM-MANUAL-CANARY-CAMPAIGN-V1"
    assert ledger["observations_completed"] == 7
    assert ledger["expected_state_matches"] == 7
    assert ledger["blocking_review_failures"] == 0
    assert ledger["ready_to_sell"] is False
    assert ledger["next_gate"]["armed"] is False

    print("WORKFLOW LEARNING LOOP FROZEN BASELINE V1: PASS")
    print("frozen_baseline_behavioral_observations=0")
    print("current_campaign_behavioral_observations=7")
    print("current_campaign_expected_state_matches=7/7")
    print("current_campaign_blocking_review_failures=0")
    print("external_model_calls_created=0")
    print("automatic_promotion=BLOCKED")
    print("automatic_wave_execution=BLOCKED")
    print("frozen_baseline_canary=PM-INV-CHECKLIST-NORMAL-0003")
    print("current_next_gate=PM-INV-PLAN-EMBEDDED_OVERRIDE-0003")
    print("current_next_gate_armed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
