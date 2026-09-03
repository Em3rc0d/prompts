#!/usr/bin/env python3
"""Fail-closed validation for Prompt Machine Starter Release Gate v1.

Static/package checks only. This validator creates no model, provider, checkout,
customer-value, delivery, certification, custody, purchase, or revenue evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "product" / "starter-collection-v1"
GATE_PATH = ROOT / "commercial" / "STARTER_RELEASE_GATE_V1.json"
STARTER_PAGE = ROOT / "web" / "app" / "starter-collection" / "page.tsx"
STARTER_CHECKOUT_ROUTE = ROOT / "web" / "app" / "api" / "commerce" / "starter-collection" / "checkout" / "route.ts"

CONTRACT_FREEZE = BASE / "CONTRACT_FREEZE_V1.json"
SURFACE_FREEZE = BASE / "SURFACE_FREEZE_V1.json"
PAYLOAD_FREEZE = BASE / "PAYLOAD_FREEZE_V1.json"
ARCHIVE_RECEIPT = BASE / "ARCHIVE_BUILD_RECEIPT_V1.json"
CANARY_FREEZE = BASE / "evaluation" / "STARTER_CANARY_FREEZE_V1.json"
CODE_REVIEW_CONTRACT = BASE / "contracts" / "code-review.workflow-contract.json"
BUG_DIAGNOSIS_CONTRACT = BASE / "contracts" / "bug-diagnosis.workflow-contract.json"
CODE_REVIEW_SURFACE = BASE / "workflows" / "evidence-first-code-review.md"
BUG_DIAGNOSIS_SURFACE = BASE / "workflows" / "evidence-first-bug-diagnosis.md"
CODE_TRUST = BASE / "trust" / "code-review.trust-context.json"
BUG_TRUST = BASE / "trust" / "bug-diagnosis.trust-context.json"

ACTIVATION = ROOT / "commercial" / "STARTER_ACTIVATION_EVIDENCE_V1.json"
COPY_AUDIT_RECEIPT = ROOT / "commercial" / "STARTER_PUBLIC_COPY_AUDIT_RECEIPT_V1.json"
PROVIDER_CUSTODY = ROOT / "commercial" / "STARTER_PROVIDER_CUSTODY_V1.json"
PROVIDER_INTEGRATION_PREP = ROOT / "commercial" / "STARTER_PROVIDER_INTEGRATION_PREP_V1.json"
DELIVERY_SCHEMA = ROOT / "commercial" / "STARTER_DELIVERY_RECEIPT_V1.schema.json"
PRODUCT_IDENTITY = BASE / "PRODUCT_IDENTITY_V1.json"
STARTER_RELEASE_ADAPTER = ROOT / "web" / "lib" / "starter-collection-release.ts"
COMMERCE_CORE = ROOT / "web" / "lib" / "commerce-release.ts"
CUSTODY_VERIFIER = ROOT / "tools" / "verify_lemonsqueezy_provider_file.py"
CUSTODY_OFFLINE_TEST = ROOT / "tools" / "test_provider_custody_verifier_v1.py"

CANONICAL_PRODUCT_ID = "prompt-machine-starter-collection"
LEGACY_PRODUCT_ID = "pq-developer-starter-collection"
CANONICAL_ARCHIVE_SHA256 = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"
CANONICAL_ARCHIVE_SIZE = 50918

CANARY_ENVELOPES = {
    "PM-STARTER-CR-NORMAL-0001": (8100, "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"),
    "PM-STARTER-CR-EMBEDDED-OVERRIDE-0001": (8278, "727b0b20085265273ad5ed72078e6a5e14031b8ee3058eed11c4825d9f56e632"),
    "PM-STARTER-BD-NORMAL-0001": (10181, "e538823d529f5f56fbe4ad20fdd63b682ff7c8d533d53ffd2c976bcf0d44b3cc"),
    "PM-STARTER-BD-EMBEDDED-OVERRIDE-0001": (10327, "7e257bdf2dae640ae4d9e91ee5b599f34f7136b4270ee494f9c2fe1e1787e9fe"),
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

REQUIRED_BOUNDARIES = {
    "contract_freeze_implies_runtime_evidence": False,
    "surface_freeze_implies_runtime_evidence": False,
    "payload_complete_implies_product_ready": False,
    "archive_build_implies_provider_custody": False,
    "archive_build_implies_delivery": False,
    "static_canary_freeze_implies_runtime_evidence": False,
    "generated_envelope_implies_behavioral_pass": False,
    "public_copy_audit_pass_implies_product_ready": False,
    "public_copy_audit_pass_implies_public_sale_authorized": False,
    "static_provider_integration_prep_implies_provider_integration_pass": False,
    "offline_provider_simulation_implies_provider_custody": False,
    "provider_custody_contract_implies_provider_custody": False,
    "architecture_observations_imply_starter_sku_evidence": False,
    "scope_frozen_implies_product_ready": False,
    "skill_candidate_implies_supported_skill": False,
    "provider_test_implies_revenue": False,
    "live_canary_implies_public_revenue": False,
    "runtime_pass_implies_certification": False,
    "public_checkout_may_bypass_requirements": False,
    "automatic_sale_enablement": False,
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_contract(contract: dict, workflow_id: str) -> None:
    assert contract["schema"] == "prompt-machine-workflow-contract-v1"
    assert contract["workflow_id"] == workflow_id
    assert contract["state"] == "CONTRACT_FROZEN_STATIC_ONLY_BEHAVIORAL_EVIDENCE_OPEN"
    assert contract["authority"] == "ADVISORY_ONLY"
    assert {row["blob_sha"] for row in contract["source_provenance"]} == EXPECTED_SOURCE_SHAS[workflow_id]
    assert contract["input_contract"]["required"]
    assert contract["input_contract"]["minimum_preflight"]
    assert contract["output_contract"]
    assert contract["verification_contract"]
    assert contract["known_limitations"]
    boundary = contract["evidence_boundary"]
    assert boundary["static_contract_freeze_is_runtime_evidence"] is False
    assert boundary["architecture_campaign_is_starter_sku_evidence"] is False
    assert boundary["runtime_pass_is_certification"] is False
    assert boundary["skill_candidate_is_supported_skill"] is False
    assert boundary["ready_to_sell"] is False


def validate_trust_context(path: Path, workflow_id: str) -> None:
    trust = read_json(path)
    assert trust["schema"] == "prompt-machine-workflow-trust-context-v1"
    assert trust["workflow_id"] == workflow_id
    assert trust["current_evidence_state"] == "STATIC_CONTRACT_AND_SURFACE_FROZEN_RUNTIME_UNOBSERVED"
    assert trust["publication_state"] == "NOT_PUBLIC_NOT_ELIGIBLE"
    assert trust["runtime_evidence"]["observations"] == []
    assert trust["runtime_evidence"]["passes"] == 0
    assert trust["runtime_evidence"]["fails"] == 0
    assert trust["runtime_evidence"]["inconclusive"] == 0
    assert trust["next_evidence"]["armed"] is False
    assert trust["truth_boundary"]["zero_failures_with_zero_runtime_observations_means_reliable"] is False
    assert trust["truth_boundary"]["automatic_publication"] is False


def main() -> int:
    gate = read_json(GATE_PATH)
    assert gate["schema"] == "prompt-machine-starter-release-gate-v1"
    assert gate["version"] == "1.0.6"

    assert gate["product"] == {
        "product_id": CANONICAL_PRODUCT_ID,
        "price_hypothesis_usd": 9,
        "billing_model": "ONE_TIME",
        "scope_state": "FROZEN",
        "sale_state": "NOT_FOR_SALE",
    }

    truth = gate["truth"]
    expected_truth = {
        "architecture_behavioral_observations": 7,
        "architecture_expected_state_matches": 7,
        "architecture_blocking_review_failures": 0,
        "starter_workflow_contracts_frozen": 2,
        "starter_executable_prompt_surfaces_frozen": 2,
        "starter_required_customer_assets_present": 9,
        "starter_required_customer_assets_total": 9,
        "starter_reproducible_archive_builds_observed": 1,
        "starter_canary_cases_prepared": 4,
        "starter_evaluation_contracts_frozen": 4,
        "starter_exact_runtime_envelopes_frozen": 4,
        "starter_canary_cases_armed": 0,
        "starter_sku_workflow_runtime_observations": 0,
        "starter_skill_behavioral_observations": 0,
        "public_copy_audit_passes": 1,
        "public_copy_material_failures_found_before_fix": 3,
        "public_copy_material_failures_open": 0,
        "provider_integration_static_preparation_passes": 1,
        "provider_custody_observations": 0,
        "real_customer_outcomes": 0,
        "real_purchases": 0,
        "public_checkout_enabled": False,
        "ready_to_sell": False,
    }
    assert truth == expected_truth

    contract_freeze = read_json(CONTRACT_FREEZE)
    assert contract_freeze["state"] == "STATIC_CONTRACT_FREEZE_PASS"
    assert contract_freeze["truth"]["external_model_calls"] == 0
    assert contract_freeze["truth"]["starter_sku_runtime_observations"] == 0

    surface_freeze = read_json(SURFACE_FREEZE)
    assert surface_freeze["state"] == "STATIC_SURFACE_CONTRACT_PARITY_PASS"
    assert surface_freeze["truth"]["external_model_calls"] == 0
    assert surface_freeze["truth"]["starter_sku_runtime_observations"] == 0

    payload_freeze = read_json(PAYLOAD_FREEZE)
    assert payload_freeze["state"] == "CUSTOMER_PAYLOAD_STATIC_COMPLETE_ARCHIVE_NOT_BUILT"
    assert payload_freeze["required_customer_assets_present"] == 9
    assert payload_freeze["truth"]["archive_built"] is False

    archive = read_json(ARCHIVE_RECEIPT)
    assert archive["state"] == "DETERMINISTIC_ARCHIVE_BUILD_PASS"
    assert archive["customer_archive"]["size_bytes"] == CANONICAL_ARCHIVE_SIZE
    assert archive["customer_archive"]["sha256"] == CANONICAL_ARCHIVE_SHA256
    assert archive["customer_archive"]["reproducibility_check"] == "PASS_BYTE_FOR_BYTE_TWO_BUILDS"
    assert archive["validation"]["model_calls"] == 0
    assert archive["validation"]["provider_calls"] == 0
    assert archive["evidence_boundary"]["github_actions_artifact_is_commerce_provider_custody"] is False
    assert archive["evidence_boundary"]["archive_build_is_customer_delivery_evidence"] is False
    assert archive["evidence_boundary"]["archive_build_is_ready_to_sell"] is False

    canary = read_json(CANARY_FREEZE)
    assert canary["schema"] == "prompt-machine-starter-canary-freeze-v1"
    assert canary["receipt_id"] == "PM-STARTER-CANARY-FREEZE-V1-0001"
    assert canary["state"] == "STATIC_CANARY_ENVELOPE_FREEZE_PASS_RUNTIME_UNEXECUTED"
    assert canary["evaluation_contract_is_runtime_input"] is False
    assert canary["expected_result_is_runtime_input"] is False
    assert len(canary["cases"]) == 4
    for row in canary["cases"]:
        size, sha = CANARY_ENVELOPES[row["case_id"]]
        assert row["runtime_envelope_size_bytes"] == size
        assert row["runtime_envelope_sha256"] == sha
        assert row["armed"] is False
        assert row["runtime_executed"] is False
    assert canary["truth"]["runtime_observations"] == 0
    assert canary["truth"]["model_calls"] == 0
    assert canary["next_permitted_runtime_sequence"]["authorized_now"] is False

    copy_audit = read_json(COPY_AUDIT_RECEIPT)
    assert copy_audit["schema"] == "prompt-machine-starter-public-copy-audit-receipt-v1"
    assert copy_audit["receipt_id"] == "PM-STARTER-PUBLIC-COPY-AUDIT-V1-0001"
    assert copy_audit["final_state"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert len(copy_audit["history"][0]["material_findings"]) == 3
    assert copy_audit["history"][0]["state"] == "FAIL_EVIDENCE_SCOPE_AMBIGUOUS"
    assert copy_audit["history"][-1]["run_id"] == 33799072926
    assert copy_audit["model_calls"] == 0
    assert copy_audit["provider_calls"] == 0
    assert copy_audit["ready_to_sell"] is False

    identity = read_json(PRODUCT_IDENTITY)
    assert identity["product"]["canonical_product_id"] == CANONICAL_PRODUCT_ID
    assert identity["product"]["product_version"] == "1.0.0-candidate"
    assert identity["legacy_aliases"][0]["product_id"] == LEGACY_PRODUCT_ID
    assert identity["legacy_aliases"][0]["provider_identity_allowed"] is False
    assert identity["rules"]["provider_custom_data_uses_canonical_id"] is True
    assert identity["rules"]["historical_records_rewritten"] is False

    custody = read_json(PROVIDER_CUSTODY)
    assert custody["schema"] == "prompt-machine-starter-provider-custody-contract-v1"
    assert custody["state"] == "CONTRACT_DEFINED_PROVIDER_NOT_PROVISIONED"
    assert custody["canonical_artifact"]["size_bytes"] == CANONICAL_ARCHIVE_SIZE
    assert custody["canonical_artifact"]["sha256"] == CANONICAL_ARCHIVE_SHA256
    assert custody["custody_evidence"]["provider_dashboard_screenshot_alone_is_sufficient"] is False
    assert custody["custody_evidence"]["provider_signed_order_alone_is_sufficient"] is False
    assert custody["delivery_boundary"]["provider_custody_pass_implies_delivery_pass"] is False
    assert custody["current_truth"]["canonical_artifact_in_provider_custody"] is False
    assert custody["current_truth"]["provider_retrieval_hash_verified"] is False
    assert custody["current_truth"]["public_checkout"] is False
    assert custody["current_truth"]["ready_to_sell"] is False

    integration = read_json(PROVIDER_INTEGRATION_PREP)
    assert integration["schema"] == "prompt-machine-starter-provider-integration-prep-v1"
    assert integration["state"] == "STATIC_PREPARED_PROVIDER_NOT_PROVISIONED"
    assert integration["product_id"] == CANONICAL_PRODUCT_ID
    assert integration["provider_candidate"] == "LEMON_SQUEEZY"
    assert integration["canonical_release"]["size_bytes"] == CANONICAL_ARCHIVE_SIZE
    assert integration["canonical_release"]["sha256"] == CANONICAL_ARCHIVE_SHA256
    assert integration["offline_regression_evidence"]["run_id"] == 33803931478
    assert integration["offline_regression_evidence"]["conclusion"] == "success"
    assert integration["offline_regression_evidence"]["provider_calls"] == 0
    assert integration["offline_regression_evidence"]["model_calls"] == 0
    assert integration["fail_closed_surface"]["starter_commerce_mode_default"] == "off"
    assert integration["fail_closed_surface"]["starter_public_sale_status_default"] == "NOT_FOR_SALE"
    assert integration["fail_closed_surface"]["starter_checkout_route_exists"] is False
    assert integration["current_truth"]["provider_custody_evidence_observed"] is False
    assert integration["current_truth"]["provider_integration_pass"] is False
    assert integration["current_truth"]["ready_to_sell"] is False
    assert integration["evidence_boundary"]["static_integration_code_is_provider_integration_pass"] is False
    assert integration["evidence_boundary"]["offline_provider_simulation_is_real_provider_custody"] is False

    for path in (DELIVERY_SCHEMA, STARTER_RELEASE_ADAPTER, COMMERCE_CORE, CUSTODY_VERIFIER, CUSTODY_OFFLINE_TEST):
        assert path.is_file(), path
    starter_adapter = STARTER_RELEASE_ADAPTER.read_text(encoding="utf-8")
    assert f'productId: "{CANONICAL_PRODUCT_ID}"' in starter_adapter
    assert f"archiveSize: {CANONICAL_ARCHIVE_SIZE}" in starter_adapter
    assert CANONICAL_ARCHIVE_SHA256 in starter_adapter
    assert "CommerceReleaseIdentity" in COMMERCE_CORE.read_text(encoding="utf-8")

    validate_contract(read_json(CODE_REVIEW_CONTRACT), "pm-starter-evidence-first-code-review")
    validate_contract(read_json(BUG_DIAGNOSIS_CONTRACT), "pm-starter-evidence-first-bug-diagnosis")
    assert "UNTRUSTED TASK DATA" in CODE_REVIEW_SURFACE.read_text(encoding="utf-8")
    assert "UNTRUSTED TASK DATA" in BUG_DIAGNOSIS_SURFACE.read_text(encoding="utf-8")
    validate_trust_context(CODE_TRUST, "pm-starter-evidence-first-code-review")
    validate_trust_context(BUG_TRUST, "pm-starter-evidence-first-bug-diagnosis")

    activation = read_json(ACTIVATION)
    assert activation["state"] == "DESIGNED_NOT_LIVE"
    assert activation["product_id"] == CANONICAL_PRODUCT_ID
    assert activation["current_truth"]["instrumentation_live"] is False
    assert activation["current_truth"]["activated_users"] == 0
    assert activation["current_truth"]["real_customer_task_outcomes"] == 0
    assert activation["current_truth"]["real_starter_purchases"] == 0
    assert activation["real_task_evidence_rule"]["synthetic_fixture_counts_as_real_task"] is False

    assert gate["launch_requirements"] == {
        "STARTER_PRODUCT_READY": False,
        "DETERMINISTIC_STARTER_ARCHIVE": True,
        "PROVIDER_CUSTODY": False,
        "PROVIDER_INTEGRATION": False,
        "LIVE_DELIVERY_CANARY": False,
        "PUBLIC_COPY_EVIDENCE_AUDIT": True,
    }

    for key, expected in REQUIRED_BOUNDARIES.items():
        assert gate["boundaries"][key] is expected

    gates = gate["gates"]
    assert gates["current_product_truth"] == "PASS"
    assert gates["final_starter_workflow_contracts"] == "PASS_STATIC_ONLY"
    assert gates["final_executable_starter_prompt_surfaces"] == "PASS_STATIC_ONLY"
    assert gates["required_customer_payload"] == "PASS_STATIC_9_OF_9"
    assert gates["deterministic_starter_artifact"] == "PASS_PACKAGING_ONLY"
    assert gates["starter_specific_behavioral_canary_readiness"] == "PASS_STATIC_PREPARED_DISARMED"
    assert gates["starter_specific_behavioral_evidence"] == "OPEN_ZERO_OBSERVATIONS"
    assert gates["starter_skill_evidence"] == "OPEN_ZERO_OBSERVATIONS"
    assert gates["customer_activation_instrumentation"] == "DESIGNED_NOT_LIVE"
    assert gates["workflow_level_trust_cards"] == "CONTEXTS_SEEDED_PUBLICATION_BLOCKED"
    assert gates["public_copy_evidence_audit"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert gates["provider_test_custody"] == "CONTRACT_DEFINED_NOT_PROVISIONED"
    assert gates["provider_integration"] == "STATIC_PREPARED_PROVIDER_NOT_PROVISIONED"
    assert gates["live_delivery_canary"] == "NOT_STARTED"
    assert gates["public_checkout"] == "BLOCKED"
    assert gates["pq_dollar_one"] == "NOT_OBSERVED"

    spend = gate["next_model_spend_gate"]
    assert spend["authorized_now"] is False
    assert spend["preferred_first_case_when_reopened"] == "PM-STARTER-CR-NORMAL-0001"
    assert spend["maximum_submissions_before_human_review"] == 1
    assert spend["automatic_wave"] is False
    assert spend["automatic_retries"] == 0
    assert spend["automatic_second_case"] is False

    page = STARTER_PAGE.read_text(encoding="utf-8")
    assert "NOT FOR SALE" in page
    assert "$9 PRICE HYPOTHESIS" in page
    assert "0</strong><span>Starter runtime observations" in page
    assert not STARTER_CHECKOUT_ROUTE.exists(), (
        "Starter checkout route exists while STARTER_RELEASE_GATE_V1 blocks public checkout"
    )

    print("STARTER RELEASE GATE V1: PASS")
    print(f"product={CANONICAL_PRODUCT_ID}")
    print("price_hypothesis_usd=9")
    print("contracts=2/2")
    print("surfaces=2/2")
    print("required_customer_payload=9/9")
    print("deterministic_archive=true")
    print(f"archive_sha256={CANONICAL_ARCHIVE_SHA256}")
    print("starter_canary_cases_prepared=4")
    print("starter_sku_runtime_observations=0")
    print("public_copy_audit=PASS_CURRENT_EVIDENCE_BOUNDARY")
    print("provider_integration=STATIC_PREPARED_PROVIDER_NOT_PROVISIONED")
    print("provider_custody=CONTRACT_DEFINED_NOT_PROVISIONED")
    print("provider_custody_observations=0")
    print("activated_users=0")
    print("public_checkout=BLOCKED")
    print("ready_to_sell=false")
    print("provider_calls=0")
    print("model_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
