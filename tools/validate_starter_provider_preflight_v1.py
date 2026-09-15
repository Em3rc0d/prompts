#!/usr/bin/env python3
"""Validate Starter provider/custody/delivery plans without contacting a provider."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "commercial/STARTER_PROVIDER_INTEGRATION_PREP_V1.json"
CUSTODY = ROOT / "commercial/STARTER_PROVIDER_CUSTODY_V1.json"
CUSTODY_PACKET = ROOT / "commercial/STARTER_PROVIDER_CUSTODY_EXECUTION_PACKET_V1.json"
DELIVERY_PLAN = ROOT / "commercial/STARTER_LIVE_DELIVERY_CANARY_PLAN_V1.json"
DELIVERY_SCHEMA = ROOT / "commercial/STARTER_DELIVERY_RECEIPT_V1.schema.json"
IDENTITY = ROOT / "product/starter-collection-v1/PRODUCT_IDENTITY_V1.json"
STARTER_CHECKOUT = ROOT / "web/app/api/commerce/starter-collection/checkout/route.ts"
STARTER_WEBHOOK = ROOT / "web/app/api/commerce/lemonsqueezy/starter-webhook/route.ts"

PRODUCT_ID = "prompt-machine-starter-collection"
ARCHIVE_NAME = "prompt-machine-starter-collection-v1.zip"
ARCHIVE_SIZE = 50918
ARCHIVE_SHA = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (INTEGRATION, CUSTODY, CUSTODY_PACKET, DELIVERY_PLAN, DELIVERY_SCHEMA, IDENTITY, STARTER_WEBHOOK):
        assert path.is_file(), path
    assert not STARTER_CHECKOUT.exists(), "Starter checkout route must remain absent before release authorization"

    identity = read(IDENTITY)
    assert identity["product"]["canonical_product_id"] == PRODUCT_ID
    assert identity["product"]["sale_status"] == "NOT_FOR_SALE"
    assert identity["rules"]["provider_custom_data_uses_canonical_id"] is True
    assert identity["rules"]["purchase_receipts_use_canonical_id"] is True
    assert identity["rules"]["delivery_receipts_use_canonical_id"] is True

    integration = read(INTEGRATION)
    assert integration["state"] == "STATIC_PREPARED_PROVIDER_NOT_PROVISIONED"
    assert integration["product_id"] == PRODUCT_ID
    assert integration["canonical_release"]["filename"] == ARCHIVE_NAME
    assert integration["canonical_release"]["size_bytes"] == ARCHIVE_SIZE
    assert integration["canonical_release"]["sha256"] == ARCHIVE_SHA
    assert integration["fail_closed_surface"]["starter_commerce_mode_default"] == "off"
    assert integration["fail_closed_surface"]["starter_public_sale_status_default"] == "NOT_FOR_SALE"
    assert integration["fail_closed_surface"]["starter_signed_webhook_adapter_present"] is True
    assert integration["fail_closed_surface"]["starter_checkout_route_exists"] is False
    assert integration["current_truth"]["provider_integration_pass"] is False
    assert integration["current_truth"]["provider_custody_evidence_observed"] is False
    assert integration["current_truth"]["real_purchase_observed"] is False
    assert integration["current_truth"]["ready_to_sell"] is False

    custody = read(CUSTODY)
    assert custody["state"] == "CONTRACT_DEFINED_PROVIDER_NOT_PROVISIONED"
    assert custody["product_id"] == PRODUCT_ID
    assert custody["canonical_artifact"]["filename"] == ARCHIVE_NAME
    assert custody["canonical_artifact"]["size_bytes"] == ARCHIVE_SIZE
    assert custody["canonical_artifact"]["sha256"] == ARCHIVE_SHA
    assert custody["custody_evidence"]["minimum_observation"] == "AUTHORIZED_PROVIDER_RETRIEVAL_PLUS_LOCAL_HASH_VERIFICATION"
    assert custody["custody_evidence"]["provider_dashboard_screenshot_alone_is_sufficient"] is False
    assert custody["custody_evidence"]["configured_filename_alone_is_sufficient"] is False
    assert custody["custody_evidence"]["provider_signed_order_alone_is_sufficient"] is False
    assert custody["delivery_boundary"]["provider_custody_pass_implies_delivery_pass"] is False

    packet = read(CUSTODY_PACKET)
    assert packet["state"] == "PREPARED_DISARMED_PROVIDER_SIDE_EFFECTS_NOT_AUTHORIZED"
    assert packet["product_id"] == PRODUCT_ID
    assert packet["arm_contract"] == {
        "required_explicit_arm": "EXECUTE_STARTER_PROVIDER_CUSTODY_TEST",
        "armed_now": False,
        "automatic_execution": False,
        "automatic_retries": 0,
        "automatic_next_gate": False,
    }
    assert packet["canonical_artifact"]["filename"] == ARCHIVE_NAME
    assert packet["canonical_artifact"]["size_bytes"] == ARCHIVE_SIZE
    assert packet["canonical_artifact"]["sha256"] == ARCHIVE_SHA
    assert packet["verification"]["verify_bytes_required_for_custody"] is True
    assert packet["verification"]["maximum_verification_attempts_before_review"] == 1
    assert packet["verification"]["downloaded_size_must_equal"] == ARCHIVE_SIZE
    assert packet["verification"]["downloaded_sha256_must_equal"] == ARCHIVE_SHA
    assert packet["current_truth"]["provider_side_effects_executed"] is False
    assert packet["current_truth"]["provider_calls"] == 0
    assert packet["current_truth"]["provider_custody_observations"] == 0
    assert packet["current_truth"]["purchases"] == 0
    assert packet["current_truth"]["deliveries"] == 0
    assert packet["current_truth"]["model_calls"] == 0
    assert packet["current_truth"]["ready_to_sell"] is False
    forbidden = set(packet["forbidden_promotions"])
    for required in ("STARTER_PRODUCT_READY", "READY_TO_SELL", "PUBLIC_CHECKOUT_ENABLED", "PQ_DOLLAR_ONE"):
        assert required in forbidden

    plan = read(DELIVERY_PLAN)
    assert plan["state"] == "DESIGNED_DISARMED_PREREQUISITES_OPEN"
    assert plan["product_id"] == PRODUCT_ID
    assert plan["arm_contract"]["required_explicit_arm"] == "EXECUTE_ONE_STARTER_LIVE_DELIVERY_CANARY"
    assert plan["arm_contract"]["armed_now"] is False
    assert plan["arm_contract"]["automatic_execution"] is False
    assert plan["arm_contract"]["maximum_live_transactions"] == 1
    assert plan["arm_contract"]["automatic_retries"] == 0
    assert plan["arm_contract"]["automatic_public_launch"] is False
    assert plan["prerequisites"]["provider_artifact_custody_pass"] is False
    assert plan["prerequisites"]["provider_integration_pass"] is False
    assert plan["prerequisites"]["starter_checkout_public"] is False
    assert plan["prerequisites"]["signed_starter_webhook_adapter_present"] is True
    assert plan["canonical_artifact"] == {
        "filename": ARCHIVE_NAME,
        "size_bytes": ARCHIVE_SIZE,
        "sha256": ARCHIVE_SHA,
    }
    order = plan["required_order_observation"]
    assert order["commerce_gate"] == "live_canary"
    assert order["test_mode"] is False
    assert order["release_product_id"] == PRODUCT_ID
    assert order["release_archive_size"] == ARCHIVE_SIZE
    assert order["release_archive_sha256"] == ARCHIVE_SHA
    delivery = plan["required_delivery_observation"]
    assert delivery["retrieved_bytes_verified_locally"] is True
    assert delivery["observed_size_bytes"] == ARCHIVE_SIZE
    assert delivery["observed_sha256"] == ARCHIVE_SHA
    boundary = plan["revenue_and_customer_boundary"]
    assert boundary["live_canary_automatically_counts_as_pq_dollar_one"] is False
    assert boundary["live_canary_automatically_counts_as_real_customer_demand"] is False
    assert boundary["internal_founder_or_controlled_purchase_counts_as_customer_conversion"] is False
    assert boundary["customer_value_observed"] is False
    assert plan["post_canary_decision"]["automatic_public_checkout"] is False
    assert plan["post_canary_decision"]["human_review_required"] is True
    assert plan["current_truth"]["live_transactions_executed"] == 0
    assert plan["current_truth"]["verified_deliveries_observed"] == 0
    assert plan["current_truth"]["pq_dollar_one_observed"] is False
    assert plan["current_truth"]["public_checkout"] is False
    assert plan["current_truth"]["ready_to_sell"] is False

    schema = read(DELIVERY_SCHEMA)
    artifact = schema["properties"]["artifact"]["properties"]
    assert artifact["filename"]["const"] == ARCHIVE_NAME
    assert artifact["expected_size_bytes"]["const"] == ARCHIVE_SIZE
    assert artifact["expected_sha256"]["const"] == ARCHIVE_SHA
    assert schema["properties"]["evidence_boundary"]["properties"]["contains_customer_pii"]["const"] is False

    webhook = STARTER_WEBHOOK.read_text(encoding="utf-8")
    assert "STARTER_COLLECTION_RELEASE" in webhook
    assert "currentStarterCommerceMode" in webhook
    assert "PM_STARTER_COMMERCE_EVENT" in webhook

    print("STARTER PROVIDER PREFLIGHT V1: PASS")
    print("provider_calls=0")
    print("model_calls=0")
    print("provider_side_effects=0")
    print("custody_packet=PREPARED_DISARMED")
    print("live_delivery_canary=DESIGNED_DISARMED")
    print("maximum_live_transactions=1")
    print("automatic_retries=0")
    print("public_checkout=false")
    print("pq_dollar_one=false")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
