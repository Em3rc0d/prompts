#!/usr/bin/env python3
"""Validate zero-side-effect execution decision governance for Starter v1.

Checks the provider integration pass decision, provider failure receipt contract,
and runtime-to-Trust-History transaction against already frozen product evidence.
No provider or model execution occurs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMERCIAL = ROOT / "commercial"
BASE = ROOT / "product" / "starter-collection-v1"

INTEGRATION = COMMERCIAL / "STARTER_PROVIDER_INTEGRATION_DECISION_V1.json"
FAILURE_SCHEMA = COMMERCIAL / "STARTER_PROVIDER_FAILURE_RECEIPT_V1.schema.json"
RUNTIME_PROTOCOL = COMMERCIAL / "STARTER_RUNTIME_TRUST_UPDATE_PROTOCOL_V1.json"
PROVIDER_SCHEMA_FREEZE = COMMERCIAL / "STARTER_PROVIDER_RECEIPT_SCHEMA_FREEZE_V1.json"
PROVIDER_PREFLIGHT = COMMERCIAL / "STARTER_PROVIDER_PREFLIGHT_FREEZE_V1.json"
CANARY_FREEZE = BASE / "evaluation" / "STARTER_CANARY_FREEZE_V1.json"
CODE_TRUST = BASE / "trust" / "code-review.trust-context.json"
OBSERVATION = BASE / "evaluation" / "observations" / "PM-STARTER-CR-NORMAL-0001.observation.json"
RAW_OUTPUT = BASE / "evaluation" / "observations" / "PM-STARTER-CR-NORMAL-0001.raw-output.md"
HUMAN_REVIEW = BASE / "evaluation" / "human-reviews" / "PM-STARTER-CR-NORMAL-0001.human-review.json"
RUNTIME_FAILURE = BASE / "evaluation" / "failures" / "PM-STARTER-CR-NORMAL-0001.failure.json"

PRODUCT_ID = "prompt-machine-starter-collection"
CASE_ID = "PM-STARTER-CR-NORMAL-0001"
WORKFLOW_ID = "pm-starter-evidence-first-code-review"
ENVELOPE_SIZE = 8100
ENVELOPE_SHA = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
ARCHIVE_SIZE = 50918
ARCHIVE_SHA = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"


def load(path: Path) -> dict:
    assert path.is_file(), path
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    integration = load(INTEGRATION)
    failure = load(FAILURE_SCHEMA)
    runtime = load(RUNTIME_PROTOCOL)
    schema_freeze = load(PROVIDER_SCHEMA_FREEZE)
    preflight = load(PROVIDER_PREFLIGHT)
    canary = load(CANARY_FREEZE)
    trust = load(CODE_TRUST)
    observation = load(OBSERVATION)
    human_review = load(HUMAN_REVIEW)
    runtime_failure = load(RUNTIME_FAILURE)

    # Provider integration PASS must require all external layers rather than a
    # configuration-only or metadata-only shortcut.
    assert integration["state"] == "DECISION_RULE_FROZEN_EXTERNAL_EVIDENCE_OPEN"
    assert integration["product_id"] == PRODUCT_ID
    assert integration["provider"] == "LEMON_SQUEEZY"
    assert integration["target_state"] == "PROVIDER_INTEGRATION_PASS"
    required = integration["required_evidence"]
    assert required["provisioning"]["required"] is True
    assert required["custody"]["required"] is True
    assert required["signed_provider_test_event"]["required"] is True
    signed = required["signed_provider_test_event"]
    assert signed["commerce_gate"] == "provider_test"
    assert signed["test_mode"] is True
    assert signed["provider_event"] == "order_created"
    assert signed["order_status"] == "paid"
    assert signed["signed_webhook_accepted"] is True
    assert signed["canonical_release"]["product_id"] == PRODUCT_ID
    assert signed["canonical_release"]["archive_size"] == ARCHIVE_SIZE
    assert signed["canonical_release"]["archive_sha256"] == ARCHIVE_SHA
    assert signed["must_not_use_public_prompt_machine_checkout"] is True
    assert signed["counts_as_revenue"] is False
    assert signed["counts_as_customer_demand"] is False
    assert signed["counts_as_delivery"] is False

    claims = integration["claim_boundary"]
    assert claims["provider_integration_pass_implies_provider_custody"] is True
    assert claims["provider_integration_pass_implies_delivery"] is False
    assert claims["provider_integration_pass_implies_real_purchase"] is False
    assert claims["provider_integration_pass_implies_revenue"] is False
    assert claims["provider_integration_pass_implies_customer_value"] is False
    assert claims["provider_integration_pass_implies_product_ready"] is False
    assert claims["provider_integration_pass_authorizes_public_checkout"] is False
    assert claims["provider_test_order_counts_as_pq_dollar_one"] is False
    assert integration["retry_policy"]["automatic_retries"] == 0
    assert integration["retry_policy"]["human_review_after_any_failed_or_inconclusive_external_attempt"] is True
    assert integration["execution_authorization"]["authorized_now"] is False
    assert integration["current_truth"]["provider_integration_pass"] is False

    # Provider failure receipts must preserve the failed observation and forbid
    # automatic retry/promotion. This is a schema, not a fabricated failure.
    assert failure["$id"] == "prompt-machine-starter-provider-failure-receipt-v1"
    assert failure["type"] == "object"
    assert failure["additionalProperties"] is False
    fp = failure["properties"]
    assert fp["provider"]["const"] == "LEMON_SQUEEZY"
    assert fp["product_id"]["const"] == PRODUCT_ID
    attempt = fp["attempt"]["properties"]
    assert attempt["automatic_retry"]["const"] is False
    fail_boundary = fp["evidence_boundary"]["properties"]
    assert fail_boundary["counts_as_external_failure_observation"]["const"] is True
    for key in (
        "counts_as_provider_integration_pass",
        "counts_as_custody_pass",
        "counts_as_delivery_pass",
        "counts_as_purchase",
        "counts_as_revenue",
        "contains_customer_pii",
        "contains_provider_secrets",
    ):
        assert fail_boundary[key]["const"] is False
    next_decision = fp["next_decision"]["properties"]
    assert next_decision["human_review_required"]["const"] is True
    assert next_decision["automatic_retry_allowed"]["const"] is False
    assert next_decision["repeat_requires_documented_change"]["const"] is True

    # Runtime-to-Trust update is anchored to the exact first frozen Starter case.
    assert runtime["state"] == "PROTOCOL_FROZEN_RUNTIME_UNEXECUTED"
    first = runtime["first_transaction"]
    assert first["case_id"] == CASE_ID
    assert first["workflow_id"] == WORKFLOW_ID
    assert first["runtime_envelope_size_bytes"] == ENVELOPE_SIZE
    assert first["runtime_envelope_sha256"] == ENVELOPE_SHA
    assert first["armed_now"] is False
    assert first["current_runtime_observations"] == 0

    frozen_case = next(row for row in canary["cases"] if row["case_id"] == CASE_ID)
    assert frozen_case["runtime_envelope_size_bytes"] == ENVELOPE_SIZE
    assert frozen_case["runtime_envelope_sha256"] == ENVELOPE_SHA
    assert frozen_case["armed"] is False
    assert frozen_case["runtime_executed"] is False
    assert canary["next_permitted_runtime_sequence"]["authorized_now"] is False
    assert canary["next_permitted_runtime_sequence"]["maximum_submissions_before_human_review"] == 1
    assert canary["next_permitted_runtime_sequence"]["automatic_retries"] == 0
    assert canary["next_permitted_runtime_sequence"]["automatic_second_case"] is False

    assert trust["workflow_id"] == WORKFLOW_ID
    assert trust["current_evidence_state"] == "ONE_RUNTIME_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"
    assert len(trust["runtime_evidence"]["observations"]) == 1
    assert len(trust["runtime_evidence"]["human_reviews"]) == 1
    assert trust["runtime_evidence"]["passes"] == 0
    assert trust["runtime_evidence"]["fails"] == 0
    assert trust["runtime_evidence"]["inconclusive"] == 1
    assert observation["case_id"] == CASE_ID
    assert observation["runtime_envelope_sha256"] == ENVELOPE_SHA
    assert observation["execution_status"] == "COMPLETED"
    assert observation["automatic_retries_observed"] == 0
    assert observation["submissions_observed"] == 1
    assert hashlib.sha256(RAW_OUTPUT.read_bytes()).hexdigest() == observation["raw_output_sha256"]
    assert human_review["observation_id"] == observation["observation_id"]
    assert human_review["result"] == "FAIL"
    assert human_review["decision"] == "REWORK"
    assert human_review["dimensions"]["material_authorization_risk_detected"]["result"] == "PASS"
    assert human_review["dimensions"]["evidence_uncertainty_preserved"]["result"] == "FAIL"
    assert runtime_failure["observation_id"] == observation["observation_id"]
    assert runtime_failure["successor_requires_new_version"] is True
    assert runtime_failure["observed_workflow_version_mutated"] is False
    correction_ref = trust["runtime_evidence"]["review_corrections"][0]
    assert correction_ref["historical_review_id"] == human_review["review_id"]
    assert correction_ref["historical_result"] == "FAIL"
    assert correction_ref["effective_result"] == "INCONCLUSIVE"
    assert correction_ref["effective_decision"] == "EXPAND_EVIDENCE"
    assert correction_ref["reason"] == "PROTOCOL_CONTAMINATION"
    correction_path = ROOT / correction_ref["path"]
    correction = load(correction_path)
    assert correction["correction_class"] == "PROTOCOL_CONTAMINATION"
    assert correction["historical_classification"]["review_result"] == "FAIL"
    assert correction["historical_classification"]["decision"] == "REWORK"
    assert correction["historical_classification"]["status"] == "PRESERVED_AS_HISTORICAL_MISCLASSIFICATION"
    assert correction["effective_classification"]["review_result"] == "INCONCLUSIVE"
    assert correction["effective_classification"]["decision"] == "EXPAND_EVIDENCE"
    assert correction["effective_classification"]["workflow_pass_count"] == 0
    assert correction["effective_classification"]["workflow_fail_count"] == 0
    assert correction["effective_classification"]["workflow_inconclusive_count"] == 1
    assert correction["workflow_mutation"]["observed_candidate_mutated"] is False
    assert correction["workflow_mutation"]["successor_required_by_this_observation"] is False
    assert correction["next_evidence"]["candidate"] == "SAME_FROZEN_1.0.0_CANDIDATE"
    assert correction["next_evidence"]["requires_clean_independent_surface"] is True
    assert correction["next_evidence"]["requires_fresh_explicit_authorization"] is True
    assert correction["next_evidence"]["automatic_retries"] == 0
    historical_failure = next(row for row in trust["historical_failures"] if row["failure_id"] == runtime_failure["failure_id"])
    assert historical_failure["historical_classification_artifact"] is True
    assert historical_failure["effective_workflow_failure"] is False
    assert historical_failure["superseded_by_correction"] == correction_ref["path"]
    assert trust["publication_state"] == "NOT_PUBLIC_NOT_ELIGIBLE"

    review = runtime["human_review_transaction"]
    assert review["starts_only_after_observation_receipt_is_frozen"] is True
    assert review["evaluation_contract_loaded_after_runtime"] is True
    assert review["expected_result_loaded_after_runtime"] is True
    assert review["no_decision_may_rewrite_raw_observation"] is True
    assert set(review["allowed_decisions"]) == {"RETAIN", "REWORK", "RETIRE", "EXPAND_EVIDENCE"}
    assert set(review["review_result_states"]) == {"PASS", "FAIL", "INCONCLUSIVE"}

    commit = runtime["trust_history_commit"]
    assert commit["allowed_only_after_human_review"] is True
    assert commit["new_failures_are_append_only"] is True
    assert commit["observed_workflow_version_may_not_be_overwritten"] is True
    assert commit["successor_requires_new_version"] is True
    assert commit["successor_inherits_predecessor_behavioral_evidence"] is False
    assert commit["public_trust_card_publication"] == "BLOCKED_UNTIL_SEPARATE_ELIGIBILITY_REVIEW"

    release = runtime["release_gate_update"]
    assert release["pass_fail_counts_require_human_review"] is True
    assert release["one_pass_may_set_starter_product_ready"] is False
    assert release["one_pass_may_enable_public_checkout"] is False
    assert release["one_pass_may_claim_certification"] is False
    assert release["one_pass_may_claim_portability"] is False
    assert release["one_pass_may_claim_customer_value"] is False
    assert runtime["execution_authorization"]["authorized_now"] is False
    # The protocol is an immutable pre-execution snapshot; current evidence lives in Trust History.
    assert runtime["current_truth"]["starter_runtime_observations"] == 0

    # Existing provider freezes must still state zero external evidence.
    assert schema_freeze["state"] == "STATIC_PROVIDER_RECEIPT_SCHEMAS_PASS_EXTERNAL_EVIDENCE_UNOBSERVED"
    assert schema_freeze["current_truth"]["provider_provisioning_receipts_observed"] == 0
    assert schema_freeze["current_truth"]["provider_custody_receipts_observed"] == 0
    assert schema_freeze["current_truth"]["delivery_receipts_observed"] == 0
    assert preflight["execution_limits"]["custody_packet_armed"] is False
    assert preflight["execution_limits"]["delivery_canary_armed"] is False
    assert preflight["current_truth"]["provider_side_effects_executed"] is False

    print("STARTER EXECUTION DECISIONS V1: PASS")
    print("provider_integration_rule=FROZEN_EXTERNAL_EVIDENCE_OPEN")
    print("provider_integration_requires=provisioning+exact_custody+signed_provider_test_event")
    print("provider_failure_receipt=APPEND_ONLY_NO_AUTO_RETRY")
    print(f"first_runtime_case={CASE_ID}")
    print(f"first_runtime_envelope_sha256={ENVELOPE_SHA}")
    print("trust_update=RAW_OBSERVATION_THEN_HUMAN_REVIEW_THEN_APPEND")
    print("starter_runtime_observations=1")
    print("starter_runtime_passes=0")
    print("starter_runtime_fails=0")
    print("starter_runtime_inconclusive=1")
    print("starter_runtime_decision=EXPAND_EVIDENCE")
    print("runtime_authorized_now=false")
    print("provider_authorized_now=false")
    print("provider_calls=0")
    print("additional_model_calls_after_canary=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
