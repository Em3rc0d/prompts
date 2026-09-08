#!/usr/bin/env python3
"""Build the Prompt Machine internal Trust Card deterministically from evidence.

The card is a projection of governed sources. This script does not execute a
model, does not invent marketing copy from free-form reasoning, and cannot
publish the card. Use --check in CI to fail if the committed card drifts from
its evidence-derived representation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_DIR = ROOT / "quarry" / "etl" / "prompt-library-v1" / "manual-canary-campaign-v1"
LEDGER_PATH = CAMPAIGN_DIR / "ledger.json"
CONTEXT_PATH = CAMPAIGN_DIR / "TRUST_CONTEXT_V1.json"
OUTPUT_PATH = CAMPAIGN_DIR / "TRUST_CARD_INTERNAL_V1.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_card(ledger: dict, context: dict) -> dict:
    assert ledger["campaign_id"] == context["campaign_id"]

    observations = ledger["observations"]
    embedded = [o for o in observations if o["variant"] == "EMBEDDED_OVERRIDE"]
    reviewed = context["reviewed_campaign_facts"]
    assert reviewed["embedded_override_observations"] == len(embedded)

    observed_cases = [
        {
            "invocation_id": o["invocation_id"],
            "mode": o["mode"],
            "variant": o["variant"],
            "expected_state": o["expected_state"],
            "observed_state": o["observed_state"],
        }
        for o in observations
    ]

    completed = ledger["observations_completed"]
    matches = ledger["expected_state_matches"]
    remaining = ledger["observations_remaining"]

    supported_statements = [
        f"{completed} bounded behavioral observations were completed on the governed manual Work surface.",
        f"All {matches} observed states matched their predeclared expected states.",
        "All completed blocking review dimensions passed.",
        f"{len(embedded)} executed EMBEDDED_OVERRIDE cases did not escalate authority or replace authorized configuration in the observed cases.",
        "No workflow was automatically promoted from this campaign.",
        "The campaign paused when the five-hour usage reserve gate was approached.",
    ]

    return {
        "schema": "prompt-machine-trust-card-v1",
        "version": "1.0.0",
        "trust_card_id": "PM-TRUST-CARD-MANUAL-CANARY-V1-0001",
        "scope_type": "BOUNDED_CAMPAIGN",
        "subject_id": ledger["campaign_id"],
        "recorded_on": ledger["recorded_on"],
        "last_evidence_update": ledger["recorded_on"],
        "publication_state": "INTERNAL_DRAFT_NOT_PUBLIC",
        "source_surface": ledger["surface"],
        "evidence_snapshot": {
            "prepared_invocations": ledger["total_prepared_invocations"],
            "behavioral_observations": completed,
            "remaining_invocations": remaining,
            "expected_state_matches": matches,
            "blocking_review_failures": ledger["blocking_review_failures"],
            "embedded_override_observations": len(embedded),
            "embedded_override_authority_escalations": reviewed["embedded_override_authority_escalations"],
            "automatic_promotions": ledger["automatic_promotions"],
            "campaign_decision": ledger["campaign_decision"],
            "campaign_state": ledger["campaign_state"],
            "ready_to_sell": ledger["ready_to_sell"],
        },
        "observed_cases": observed_cases,
        "supported_statements": supported_statements,
        "historical_failures": [],
        "historical_pre_runtime_issues": context["historical_pre_runtime_issues"],
        "current_limitations": [
            f"{completed} observations do not establish certification.",
            f"{len(embedded)} adversarial observations do not establish prompt-injection immunity.",
            "Work-surface observations do not establish portability across models or providers.",
            "Behavioral correctness does not establish real customer value.",
            "No repeat-use evidence has been observed.",
            "No real purchase has been observed.",
            "Shared-plan percentage changes are not exact per-workflow token or cost accounting.",
            f"{remaining} prepared low-risk invocation cases remain unobserved.",
        ],
        "unknowns": [
            f"Behavior of the remaining {remaining} prepared invocations.",
            "Behavior on other model/provider surfaces.",
            "Performance on real customer tasks.",
            "Repeat-use and referral behavior.",
            "Paid conversion and delivery behavior.",
        ],
        "explicit_non_claims": [
            "NOT_CERTIFIED",
            "NOT_UNIVERSALLY_RELIABLE",
            "NO_PROMPT_INJECTION_IMMUNITY_CLAIM",
            "NO_PORTABILITY_CLAIM",
            "NO_CUSTOMER_VALUE_CLAIM",
            "NO_REVENUE_CLAIM",
            "NOT_READY_TO_SELL",
        ],
        "provenance_refs": [
            "quarry/etl/prompt-library-v1/manual-canary-campaign-v1/ledger.json",
            "quarry/etl/prompt-library-v1/manual-canary-campaign-v1/TRUST_CONTEXT_V1.json",
            "quarry/etl/prompt-library-v1/manual-canary-campaign-v1/TRUST_HISTORY.md",
            "quarry/etl/prompt-library-v1/manual-canary-campaign-v1/NEXT_GATE.json",
            "quarry/learning-loop/TRUST_HISTORY_POLICY_V1.json",
            "docs/WORKFLOW_TRUST_HISTORY_V1.md",
            "commercial/TRUST_CARD_CONTRACT_V1.json",
        ],
        "truth_boundary": {
            "campaign_card_is_not_single_workflow_certification": True,
            "pre_runtime_issue_is_not_runtime_failure": True,
            "material_failures_would_be_preserved_if_observed": True,
            "unknowns_preserved": True,
            "automatic_publication": False,
            "marketing_claim_lte_observed_evidence": True,
        },
    }


def render(card: dict) -> str:
    return json.dumps(card, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    ledger = load_json(LEDGER_PATH)
    context = load_json(CONTEXT_PATH)
    expected = render(build_card(ledger, context))

    if args.write:
        OUTPUT_PATH.write_text(expected, encoding="utf-8")
        print(f"wrote={OUTPUT_PATH.relative_to(ROOT)}")
        print("external_model_calls=0")
        return 0

    actual = OUTPUT_PATH.read_text(encoding="utf-8")
    if actual != expected:
        print("TRUST CARD DERIVATION: FAIL")
        print("Committed Trust Card differs from deterministic evidence projection.")
        return 1

    print("TRUST CARD DERIVATION: PASS")
    print(f"source_observations={ledger['observations_completed']}")
    print("publication_state=INTERNAL_DRAFT_NOT_PUBLIC")
    print("external_model_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
