#!/usr/bin/env python3
"""Deterministic fail-closed validation for Prompt Machine Trust History v1.

This validator checks consistency between the Trust History policy, the manual
campaign ledger, the internal Trust Card, and the human-readable Trust History.
It performs no model calls and creates no behavioral, certification, customer,
or revenue evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "quarry" / "learning-loop" / "TRUST_HISTORY_POLICY_V1.json"
CONTRACT_PATH = ROOT / "commercial" / "TRUST_CARD_CONTRACT_V1.json"
CAMPAIGN_DIR = ROOT / "quarry" / "etl" / "prompt-library-v1" / "manual-canary-campaign-v1"
LEDGER_PATH = CAMPAIGN_DIR / "ledger.json"
CARD_PATH = CAMPAIGN_DIR / "TRUST_CARD_INTERNAL_V1.json"
HISTORY_PATH = CAMPAIGN_DIR / "TRUST_HISTORY.md"

FORBIDDEN_SUPPORTED_CLAIM_FRAGMENTS = {
    "always works",
    "guaranteed",
    "fully reliable",
    "works on every model",
    "certified",
    "prompt-injection immunity",
    "prompt injection immunity",
    "ready to sell",
    "customer value proven",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    policy = load_json(POLICY_PATH)
    contract = load_json(CONTRACT_PATH)
    ledger = load_json(LEDGER_PATH)
    card = load_json(CARD_PATH)
    history_text = HISTORY_PATH.read_text(encoding="utf-8")

    assert policy["schema"] == "prompt-machine-trust-history-policy-v1"
    assert policy["version"] == "1.0.0"
    assert policy["state"] == "GOVERNED_POLICY_PUBLICATION_NOT_YET_ENABLED"

    principles = policy["principles"]
    assert principles["append_only_after_behavioral_observation"] is True
    assert principles["preserve_material_failures"] is True
    assert principles["preserve_inconclusive_results"] is True
    assert principles["overwrite_observed_versions"] is False
    assert principles["inherit_predecessor_evidence"] is False
    assert principles["rewrite_evaluation_contract_after_result"] is False
    assert principles["cherry_pick_material_campaign_results"] is False
    assert principles["automatic_publication"] is False
    assert principles["automatic_marketing_claim_generation"] is False
    assert principles["automatic_certification"] is False

    assert policy["public_projection"]["source_of_truth"] == "INTERNAL_EVIDENCE_LEDGER"
    assert policy["public_projection"]["material_failures_must_remain_represented"] is True
    assert policy["public_projection"]["unknowns_must_remain_unknown"] is True
    assert policy["master_rule"] == "MARKETING CLAIM <= OBSERVED EVIDENCE"

    assert contract["schema"] == "prompt-machine-trust-card-contract-v1"
    assert contract["version"] == "1.0.0"
    assert contract["state"] == "STATIC_CONTRACT_PUBLICATION_DISABLED"
    assert contract["projection_rules"]["automatic_publication"] is False
    assert contract["projection_rules"]["automatic_claim_strengthening"] is False
    assert contract["projection_rules"]["human_review_required_before_publication"] is True
    assert contract["projection_rules"]["material_campaign_failures_must_be_included"] is True
    assert contract["projection_rules"]["pre_runtime_issue_must_not_be_relabelled_runtime_fail"] is True
    assert contract["projection_rules"]["claim_ceiling_rule"] == "MARKETING CLAIM <= OBSERVED EVIDENCE"
    assert contract["current_publication_gate"]["enabled"] is False

    assert ledger["campaign_id"] == "PM-MANUAL-CANARY-CAMPAIGN-V1"
    assert card["schema"] == "prompt-machine-trust-card-v1"
    assert card["scope_type"] == "BOUNDED_CAMPAIGN"
    assert card["subject_id"] == ledger["campaign_id"]
    assert card["publication_state"] == "INTERNAL_DRAFT_NOT_PUBLIC"

    snapshot = card["evidence_snapshot"]
    assert snapshot["prepared_invocations"] == ledger["total_prepared_invocations"]
    assert snapshot["behavioral_observations"] == ledger["observations_completed"]
    assert snapshot["remaining_invocations"] == ledger["observations_remaining"]
    assert snapshot["expected_state_matches"] == ledger["expected_state_matches"]
    assert snapshot["blocking_review_failures"] == ledger["blocking_review_failures"]
    assert snapshot["automatic_promotions"] == ledger["automatic_promotions"]
    assert snapshot["campaign_decision"] == ledger["campaign_decision"]
    assert snapshot["campaign_state"] == ledger["campaign_state"]
    assert snapshot["ready_to_sell"] == ledger["ready_to_sell"] is False

    ledger_cases = {o["invocation_id"]: o for o in ledger["observations"]}
    card_cases = {o["invocation_id"]: o for o in card["observed_cases"]}
    assert set(card_cases) == set(ledger_cases)

    embedded_count = 0
    for invocation_id, observed in ledger_cases.items():
        projected = card_cases[invocation_id]
        assert projected["mode"] == observed["mode"]
        assert projected["variant"] == observed["variant"]
        assert projected["expected_state"] == observed["expected_state"]
        assert projected["observed_state"] == observed["observed_state"]
        assert observed["expected_state"] == observed["observed_state"]
        assert observed["blocking_dimensions"] == "PASS"
        assert invocation_id in history_text
        if observed["variant"] == "EMBEDDED_OVERRIDE":
            embedded_count += 1

    assert embedded_count == snapshot["embedded_override_observations"] == 3
    assert snapshot["embedded_override_authority_escalations"] == 0

    current_truth = policy["current_campaign_truth"]
    assert current_truth["behavioral_observations"] == ledger["observations_completed"]
    assert current_truth["expected_state_matches"] == ledger["expected_state_matches"]
    assert current_truth["blocking_review_failures"] == ledger["blocking_review_failures"]
    assert current_truth["certification_claim"] is False
    assert current_truth["portability_claim"] is False
    assert current_truth["ready_to_sell"] is False
    assert current_truth["public_trust_story_enabled"] is False

    # There are currently no runtime failures in the seven-case campaign. A
    # pre-runtime static semantic issue is preserved separately and must not be
    # relabelled as a runtime failure.
    assert card["historical_failures"] == []
    assert len(card["historical_pre_runtime_issues"]) == 1
    issue = card["historical_pre_runtime_issues"][0]
    assert issue["class"] == "STATIC_SEMANTIC_ISSUE"
    assert issue["runtime_failure"] is False
    assert "answer key" in issue["summary"].lower() or "ground truth" in issue["summary"].lower()
    for follow_up in issue["runtime_follow_up"]:
        assert follow_up in ledger_cases
        assert follow_up in history_text

    supported = "\n".join(card["supported_statements"]).lower()
    for fragment in FORBIDDEN_SUPPORTED_CLAIM_FRAGMENTS:
        assert fragment not in supported, f"unsupported public-style claim fragment: {fragment}"

    non_claims = set(card["explicit_non_claims"])
    required_non_claims = {
        "NOT_CERTIFIED",
        "NOT_UNIVERSALLY_RELIABLE",
        "NO_PROMPT_INJECTION_IMMUNITY_CLAIM",
        "NO_PORTABILITY_CLAIM",
        "NO_CUSTOMER_VALUE_CLAIM",
        "NO_REVENUE_CLAIM",
        "NOT_READY_TO_SELL",
    }
    assert required_non_claims <= non_claims

    truth = card["truth_boundary"]
    assert truth["campaign_card_is_not_single_workflow_certification"] is True
    assert truth["pre_runtime_issue_is_not_runtime_failure"] is True
    assert truth["material_failures_would_be_preserved_if_observed"] is True
    assert truth["unknowns_preserved"] is True
    assert truth["automatic_publication"] is False
    assert truth["marketing_claim_lte_observed_evidence"] is True

    required_refs = {
        "quarry/etl/prompt-library-v1/manual-canary-campaign-v1/ledger.json",
        "quarry/etl/prompt-library-v1/manual-canary-campaign-v1/TRUST_HISTORY.md",
        "quarry/learning-loop/TRUST_HISTORY_POLICY_V1.json",
        "commercial/TRUST_CARD_CONTRACT_V1.json",
    }
    assert required_refs <= set(card["provenance_refs"])
    for ref in card["provenance_refs"]:
        assert (ROOT / ref).exists(), f"missing provenance ref: {ref}"

    assert "INTERNAL EVIDENCE NARRATIVE / NOT PUBLIC MARKETING COPY" in history_text
    assert "READY_TO_SELL                      NO" in history_text
    assert "7/7 expected-state matches != certification" in history_text

    print("TRUST HISTORY V1: PASS")
    print(f"behavioral_observations={ledger['observations_completed']}")
    print(f"expected_state_matches={ledger['expected_state_matches']}/{ledger['observations_completed']}")
    print(f"blocking_review_failures={ledger['blocking_review_failures']}")
    print(f"embedded_override_cases={embedded_count}")
    print("public_trust_card=BLOCKED")
    print("automatic_publication=BLOCKED")
    print("automatic_claim_strengthening=BLOCKED")
    print("external_model_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
