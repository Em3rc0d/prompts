#!/usr/bin/env python3
"""Validate Prompt Machine Starter provider evidence receipt schemas.

Static schema/invariant validation only. No provider, model, checkout, purchase,
delivery, customer-value, custody, or revenue evidence is created here.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMERCIAL = ROOT / "commercial"

PROVISIONING = COMMERCIAL / "STARTER_PROVIDER_PROVISIONING_RECEIPT_V1.schema.json"
CUSTODY = COMMERCIAL / "STARTER_PROVIDER_CUSTODY_RECEIPT_V1.schema.json"
DELIVERY = COMMERCIAL / "STARTER_DELIVERY_RECEIPT_V1.schema.json"
CUSTODY_CONTRACT = COMMERCIAL / "STARTER_PROVIDER_CUSTODY_V1.json"
PREFLIGHT = COMMERCIAL / "STARTER_PROVIDER_PREFLIGHT_FREEZE_V1.json"

PRODUCT_ID = "prompt-machine-starter-collection"
ARCHIVE_NAME = "prompt-machine-starter-collection-v1.zip"
ARCHIVE_SIZE = 50918
ARCHIVE_SHA256 = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"


def load(path: Path) -> dict:
    assert path.is_file(), path
    return json.loads(path.read_text(encoding="utf-8"))


def prop(schema: dict, *path: str) -> dict:
    node = schema
    for part in path:
        node = node["properties"][part] if "properties" in node and part in node["properties"] else node[part]
    return node


def object_schema(node: dict) -> None:
    assert node["type"] == "object"
    assert node["additionalProperties"] is False
    assert node["required"]


def assert_no_sensitive_value_fields(schema: dict) -> None:
    """Reject fields that would persist customer/payment/provider-secret values.

    Boundary booleans such as contains_customer_pii are intentionally allowed.
    """
    forbidden_exact = {
        "customer_name",
        "customer_email",
        "email",
        "name",
        "card_number",
        "payment_details",
        "payment_method",
        "api_key",
        "webhook_secret",
        "access_token",
        "secret_value",
    }
    allowed_boundary_fields = {"contains_customer_pii", "contains_provider_secrets"}

    def walk(node: object) -> None:
        if isinstance(node, dict):
            properties = node.get("properties")
            if isinstance(properties, dict):
                for key, child in properties.items():
                    if key not in allowed_boundary_fields:
                        assert key.lower() not in forbidden_exact, f"sensitive receipt field forbidden: {key}"
                    walk(child)
            for key, value in node.items():
                if key != "properties":
                    walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(schema)


def main() -> int:
    provisioning = load(PROVISIONING)
    custody = load(CUSTODY)
    delivery = load(DELIVERY)
    custody_contract = load(CUSTODY_CONTRACT)
    preflight = load(PREFLIGHT)

    # Top-level schemas are fail-closed objects.
    for schema in (provisioning, custody, delivery):
        object_schema(schema)
        assert_no_sensitive_value_fields(schema)

    assert provisioning["$id"] == "prompt-machine-starter-provider-provisioning-receipt-v1"
    assert custody["$id"] == "prompt-machine-starter-provider-custody-receipt-v1"
    assert delivery["$id"] == "prompt-machine-starter-delivery-receipt-v1"

    # Canonical product/release identity must not drift across provider receipts.
    assert prop(provisioning, "product_id")["const"] == PRODUCT_ID
    assert prop(custody, "product_id")["const"] == PRODUCT_ID

    prov_artifact = prop(provisioning, "artifact_binding")
    custody_artifact = prop(custody, "artifact")
    delivery_artifact = prop(delivery, "artifact")
    for artifact in (prov_artifact, custody_artifact, delivery_artifact):
        object_schema(artifact)
        assert artifact["properties"]["filename"]["const"] == ARCHIVE_NAME
        assert artifact["properties"]["expected_size_bytes"]["const"] == ARCHIVE_SIZE
        assert artifact["properties"]["expected_sha256"]["const"] == ARCHIVE_SHA256

    # Provisioning is configuration observation only — never custody/delivery/revenue.
    prov_boundary = prop(provisioning, "evidence_boundary")
    object_schema(prov_boundary)
    prov_props = prov_boundary["properties"]
    assert prov_props["counts_as_provider_provisioning_observation"]["const"] is True
    assert prov_props["counts_as_provider_custody"]["const"] is False
    assert prov_props["counts_as_delivery_evidence"]["const"] is False
    assert prov_props["counts_as_purchase_evidence"]["const"] is False
    assert prov_props["counts_as_revenue"]["const"] is False
    assert prov_props["contains_customer_pii"]["const"] is False
    assert prov_props["contains_provider_secrets"]["const"] is False
    assert prop(provisioning, "public_surface")["properties"]["prompt_machine_public_checkout_enabled"]["const"] is False

    # Custody requires exact provider-retrieved bytes, not metadata alone.
    custody_props = custody_artifact["properties"]
    assert custody_props["observed_size_bytes"]["const"] == ARCHIVE_SIZE
    assert custody_props["observed_sha256"]["const"] == ARCHIVE_SHA256
    assert custody_props["identity_match"]["const"] is True
    retrieval = prop(custody, "retrieval")
    object_schema(retrieval)
    assert retrieval["properties"]["retrieval_completed"]["const"] is True
    assert retrieval["properties"]["retrieved_bytes_verified_locally"]["const"] is True
    assert retrieval["properties"]["metadata_only"]["const"] is False
    assert prop(custody, "public_surface")["properties"]["prompt_machine_public_checkout_enabled"]["const"] is False

    custody_boundary = prop(custody, "evidence_boundary")
    object_schema(custody_boundary)
    cb = custody_boundary["properties"]
    assert cb["evidence_class"]["const"] == "PROVIDER_ARTIFACT_CUSTODY_EVIDENCE"
    assert cb["counts_as_provider_custody"]["const"] is True
    assert cb["counts_as_delivery_evidence"]["const"] is False
    assert cb["counts_as_purchase_evidence"]["const"] is False
    assert cb["counts_as_revenue"]["const"] is False
    assert cb["counts_as_customer_value"]["const"] is False
    assert cb["counts_as_ready_to_sell"]["const"] is False
    assert cb["contains_customer_pii"]["const"] is False
    assert cb["contains_provider_secrets"]["const"] is False

    # Delivery remains a distinct receipt. Its artifact observations may vary in
    # schema shape, but success is not implied by provisioning/custody.
    delivery_boundary = prop(delivery, "evidence_boundary")
    object_schema(delivery_boundary)
    db = delivery_boundary["properties"]
    assert db["counts_as_provider_custody"]["type"] == "boolean"
    assert db["counts_as_delivery_evidence"]["type"] == "boolean"
    assert db["counts_as_real_revenue"]["type"] == "boolean"
    assert db["contains_customer_pii"]["const"] is False

    # The schemas must agree with the already-frozen execution philosophy.
    assert custody_contract["canonical_artifact"]["size_bytes"] == ARCHIVE_SIZE
    assert custody_contract["canonical_artifact"]["sha256"] == ARCHIVE_SHA256
    assert custody_contract["custody_evidence"]["provider_dashboard_screenshot_alone_is_sufficient"] is False
    assert custody_contract["custody_evidence"]["configured_filename_alone_is_sufficient"] is False
    assert custody_contract["custody_evidence"]["provider_signed_order_alone_is_sufficient"] is False
    assert custody_contract["delivery_boundary"]["provider_custody_pass_implies_delivery_pass"] is False

    assert preflight["state"] == "STATIC_PROVIDER_EXECUTION_PRECONDITIONS_PASS_DISARMED"
    assert preflight["execution_limits"]["custody_packet_armed"] is False
    assert preflight["execution_limits"]["delivery_canary_armed"] is False
    assert preflight["execution_limits"]["maximum_live_transactions"] == 1
    assert preflight["current_truth"]["provider_side_effects_executed"] is False
    assert preflight["current_truth"]["provider_custody_observations"] == 0
    assert preflight["current_truth"]["verified_deliveries"] == 0
    assert preflight["current_truth"]["real_customer_purchases"] == 0

    print("STARTER PROVIDER RECEIPT SCHEMAS V1: PASS")
    print(f"product_id={PRODUCT_ID}")
    print(f"archive_size_bytes={ARCHIVE_SIZE}")
    print(f"archive_sha256={ARCHIVE_SHA256}")
    print("provisioning_is_custody=false")
    print("custody_requires_exact_provider_retrieved_bytes=true")
    print("custody_is_delivery=false")
    print("custody_is_revenue=false")
    print("customer_pii_allowed=false")
    print("provider_secrets_allowed=false")
    print("provider_side_effects=0")
    print("provider_calls=0")
    print("model_calls=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
