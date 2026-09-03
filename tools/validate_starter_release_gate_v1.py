#!/usr/bin/env python3
"""Fail-closed validation for Prompt Machine Starter Release Gate v1.

This validator performs static repository checks only. It does not execute a
model, create checkout sessions, call a commerce provider, or create product,
customer-value, delivery, or revenue evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "commercial" / "STARTER_RELEASE_GATE_V1.json"
STARTER_PAGE = ROOT / "web" / "app" / "starter-collection" / "page.tsx"
STARTER_CHECKOUT_ROUTE = (
    ROOT / "web" / "app" / "api" / "commerce" / "starter-collection" / "checkout" / "route.ts"
)
CONTRACT_FREEZE = ROOT / "product" / "starter-collection-v1" / "CONTRACT_FREEZE_V1.json"
SURFACE_FREEZE = ROOT / "product" / "starter-collection-v1" / "SURFACE_FREEZE_V1.json"
CODE_REVIEW_CONTRACT = (
    ROOT / "product" / "starter-collection-v1" / "contracts" / "code-review.workflow-contract.json"
)
BUG_DIAGNOSIS_CONTRACT = (
    ROOT / "product" / "starter-collection-v1" / "contracts" / "bug-diagnosis.workflow-contract.json"
)
CODE_REVIEW_SURFACE = (
    ROOT / "product" / "starter-collection-v1" / "workflows" / "evidence-first-code-review.md"
)
BUG_DIAGNOSIS_SURFACE = (
    ROOT / "product" / "starter-collection-v1" / "workflows" / "evidence-first-bug-diagnosis.md"
)

REQUIRED_LAUNCH_GATES = {
    "STARTER_PRODUCT_READY",
    "DETERMINISTIC_STARTER_ARCHIVE",
    "PROVIDER_CUSTODY",
    "PROVIDER_INTEGRATION",
    "LIVE_DELIVERY_CANARY",
    "PUBLIC_COPY_EVIDENCE_AUDIT",
}

REQUIRED_BOUNDARIES = {
    "contract_freeze_implies_runtime_evidence": False,
    "surface_freeze_implies_runtime_evidence": False,
    "architecture_observations_imply_starter_sku_evidence": False,
    "scope_frozen_implies_product_ready": False,
    "skill_candidate_implies_supported_skill": False,
    "provider_test_implies_revenue": False,
    "live_canary_implies_public_revenue": False,
    "runtime_pass_implies_certification": False,
    "public_checkout_may_bypass_requirements": False,
    "automatic_sale_enablement": False,
}

EXPECTED_SOURCE_SHAS = {
    "pm-starter-evidence-first-code-review": {
        "4a3e29c9b9ce27aa750ebe763a9ad02a18e854c5",
        "387804cf3dd5aaf22b56aafbeb6b17380942a59e",
    },
    "pm-starter-evidence-first-bug-diagnosis": {
        "5e3fdcdcaafc7d5d7dc5986bbc048d814cfe821e",
        "7a320cf8bbf5587024f201b8a02fa5421979f396",
    },
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_contract(contract: dict, expected_workflow_id: str) -> None:
    assert contract["schema"] == "prompt-machine-workflow-contract-v1"
    assert contract["contract_version"] == "1.0.0"
    assert contract["workflow_id"] == expected_workflow_id
    assert contract["collection"] == "starter-collection-v1"
    assert contract["state"] == "CONTRACT_FROZEN_STATIC_ONLY_BEHAVIORAL_EVIDENCE_OPEN"
    assert contract["authority"] == "ADVISORY_ONLY"

    source_shas = {item["blob_sha"] for item in contract["source_provenance"]}
    assert source_shas == EXPECTED_SOURCE_SHAS[expected_workflow_id]

    assert contract["input_contract"]["required"]
    assert contract["input_contract"]["input_states"]
    assert contract["input_contract"]["minimum_preflight"]
    assert contract["output_contract"]
    assert contract["verification_contract"]
    assert contract["known_limitations"]
    assert contract["normalization_decisions"]

    boundary = contract["evidence_boundary"]
    assert boundary["static_contract_freeze_is_runtime_evidence"] is False
    assert boundary["architecture_campaign_is_starter_sku_evidence"] is False
    assert boundary["runtime_pass_is_certification"] is False
    assert boundary["skill_candidate_is_supported_skill"] is False
    assert boundary["ready_to_sell"] is False


def main() -> int:
    gate = read_json(GATE_PATH)

    assert gate["schema"] == "prompt-machine-starter-release-gate-v1"
    assert gate["version"] == "1.0.2"

    product = gate["product"]
    assert product["product_id"] == "prompt-machine-starter-collection"
    assert product["price_hypothesis_usd"] == 9
    assert product["billing_model"] == "ONE_TIME"
    assert product["scope_state"] == "FROZEN"
    assert product["sale_state"] == "NOT_FOR_SALE"

    truth = gate["truth"]
    assert truth["architecture_behavioral_observations"] == 7
    assert truth["architecture_expected_state_matches"] == 7
    assert truth["architecture_blocking_review_failures"] == 0
    assert truth["starter_workflow_contracts_frozen"] == 2
    assert truth["starter_executable_prompt_surfaces_frozen"] == 2
    # Architecture/static contract/surface evidence must not become SKU runtime evidence.
    assert truth["starter_sku_workflow_runtime_observations"] == 0
    assert truth["starter_skill_behavioral_observations"] == 0
    assert truth["real_customer_outcomes"] == 0
    assert truth["real_purchases"] == 0
    assert truth["public_checkout_enabled"] is False
    assert truth["ready_to_sell"] is False

    contract_freeze = read_json(CONTRACT_FREEZE)
    assert contract_freeze["schema"] == "prompt-machine-starter-contract-freeze-v1"
    assert contract_freeze["receipt_id"] == "PM-STARTER-CONTRACT-FREEZE-V1-0001"
    assert contract_freeze["state"] == "STATIC_CONTRACT_FREEZE_PASS"
    assert contract_freeze["truth"]["contract_count"] == 2
    assert contract_freeze["truth"]["external_model_calls"] == 0
    assert contract_freeze["truth"]["starter_sku_runtime_observations"] == 0
    assert contract_freeze["truth"]["ready_to_sell"] is False
    assert contract_freeze["next_gate_armed"] is False

    surface_freeze = read_json(SURFACE_FREEZE)
    assert surface_freeze["schema"] == "prompt-machine-starter-surface-freeze-v1"
    assert surface_freeze["receipt_id"] == "PM-STARTER-SURFACE-FREEZE-V1-0001"
    assert surface_freeze["state"] == "STATIC_SURFACE_CONTRACT_PARITY_PASS"
    assert surface_freeze["truth"]["surface_count"] == 2
    assert surface_freeze["truth"]["external_model_calls"] == 0
    assert surface_freeze["truth"]["starter_sku_runtime_observations"] == 0
    assert surface_freeze["truth"]["ready_to_sell"] is False
    assert surface_freeze["next_gate_armed"] is False

    validate_contract(read_json(CODE_REVIEW_CONTRACT), "pm-starter-evidence-first-code-review")
    validate_contract(read_json(BUG_DIAGNOSIS_CONTRACT), "pm-starter-evidence-first-bug-diagnosis")

    assert CODE_REVIEW_SURFACE.exists()
    assert BUG_DIAGNOSIS_SURFACE.exists()
    assert "UNTRUSTED TASK DATA" in CODE_REVIEW_SURFACE.read_text(encoding="utf-8")
    assert "UNTRUSTED TASK DATA" in BUG_DIAGNOSIS_SURFACE.read_text(encoding="utf-8")

    assert set(gate["launch_requirements"]) == REQUIRED_LAUNCH_GATES
    assert all(value is False for value in gate["launch_requirements"].values())

    boundaries = gate["boundaries"]
    for key, expected in REQUIRED_BOUNDARIES.items():
        assert boundaries[key] is expected

    gates = gate["gates"]
    assert gates["current_product_truth"] == "PASS"
    assert gates["final_starter_workflow_contracts"] == "PASS_STATIC_ONLY"
    assert gates["final_executable_starter_prompt_surfaces"] == "PASS_STATIC_ONLY"
    assert gates["starter_specific_behavioral_evidence"] == "OPEN_ZERO_OBSERVATIONS"
    assert gates["starter_skill_evidence"] == "OPEN_ZERO_OBSERVATIONS"
    assert gates["deterministic_starter_artifact"] == "NOT_BUILT"
    assert gates["provider_test_custody"] == "NOT_STARTED"
    assert gates["provider_integration"] == "NOT_STARTED_FOR_STARTER"
    assert gates["live_delivery_canary"] == "NOT_STARTED"
    assert gates["public_checkout"] == "BLOCKED"
    assert gates["pq_dollar_one"] == "NOT_OBSERVED"

    spend = gate["next_model_spend_gate"]
    assert spend["authorized_now"] is False

    # Customer-facing copy must continue to represent the actual sale state.
    page = STARTER_PAGE.read_text(encoding="utf-8")
    assert "NOT FOR SALE" in page
    assert "$9" in page
    assert "PRICE HYPOTHESIS" in page
    assert "checkout" in page.lower()

    # While the gate is blocked, no public Starter checkout endpoint is allowed.
    assert not STARTER_CHECKOUT_ROUTE.exists(), (
        "Starter checkout route exists while STARTER_RELEASE_GATE_V1 still blocks public checkout"
    )

    print("STARTER RELEASE GATE V1: PASS")
    print("product=prompt-machine-starter-collection")
    print("price_hypothesis_usd=9")
    print("architecture_behavioral_observations=7")
    print("starter_workflow_contracts_frozen=2")
    print("starter_executable_prompt_surfaces_frozen=2")
    print("starter_sku_workflow_runtime_observations=0")
    print("starter_skill_behavioral_observations=0")
    print("public_checkout=BLOCKED")
    print("ready_to_sell=false")
    print("provider_calls=0")
    print("model_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
