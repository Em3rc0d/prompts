#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

LIB = WEB / "lib" / "lemonsqueezy.ts"
CORE_RELEASE = WEB / "lib" / "commerce-release.ts"
DEVELOPER_RELEASE = WEB / "lib" / "developer-pack-release.ts"
STARTER_RELEASE = WEB / "lib" / "starter-collection-release.ts"
MODE = WEB / "lib" / "commerce-mode.ts"
WEBHOOK_ROUTE = WEB / "app" / "api" / "commerce" / "lemonsqueezy" / "webhook" / "route.ts"
DEVELOPER_CHECKOUT_ROUTE = WEB / "app" / "api" / "commerce" / "developer-pack" / "checkout" / "route.ts"
STARTER_CHECKOUT_ROUTE = WEB / "app" / "api" / "commerce" / "starter-collection" / "checkout" / "route.ts"
ENV = WEB / ".env.example"
COMMERCE_LINK = WEB / "components" / "commerce-link.tsx"
TRACKER = WEB / "components" / "funnel-tracker.tsx"
PROVIDER_FILE_VERIFIER = ROOT / "tools" / "verify_lemonsqueezy_provider_file.py"
STARTER_IDENTITY = ROOT / "product" / "starter-collection-v1" / "PRODUCT_IDENTITY_V1.json"
STARTER_CUSTODY = ROOT / "commercial" / "STARTER_PROVIDER_CUSTODY_V1.json"

CANONICAL_STARTER_ID = "prompt-machine-starter-collection"
LEGACY_STARTER_ID = "pq-developer-starter-collection"
STARTER_ARCHIVE_SIZE = 50918
STARTER_ARCHIVE_SHA256 = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"


def fail(message: str) -> None:
    raise SystemExit(f"COMMERCE V0: FAIL — {message}")


def require_tokens(label: str, source: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in source:
            fail(f"{label} missing: {token}")


def main() -> None:
    required_files = (
        LIB,
        CORE_RELEASE,
        DEVELOPER_RELEASE,
        STARTER_RELEASE,
        MODE,
        WEBHOOK_ROUTE,
        DEVELOPER_CHECKOUT_ROUTE,
        ENV,
        COMMERCE_LINK,
        TRACKER,
        PROVIDER_FILE_VERIFIER,
        STARTER_IDENTITY,
        STARTER_CUSTODY,
    )
    for path in required_files:
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")

    lib = LIB.read_text(encoding="utf-8")
    core_release = CORE_RELEASE.read_text(encoding="utf-8")
    developer_release = DEVELOPER_RELEASE.read_text(encoding="utf-8")
    starter_release = STARTER_RELEASE.read_text(encoding="utf-8")
    mode = MODE.read_text(encoding="utf-8")
    webhook = WEBHOOK_ROUTE.read_text(encoding="utf-8")
    checkout = DEVELOPER_CHECKOUT_ROUTE.read_text(encoding="utf-8")
    env = ENV.read_text(encoding="utf-8")
    link = COMMERCE_LINK.read_text(encoding="utf-8")
    tracker = TRACKER.read_text(encoding="utf-8")
    provider_verifier = PROVIDER_FILE_VERIFIER.read_text(encoding="utf-8")
    identity = json.loads(STARTER_IDENTITY.read_text(encoding="utf-8"))
    custody = json.loads(STARTER_CUSTODY.read_text(encoding="utf-8"))

    require_tokens(
        "generic release identity contract",
        core_release,
        (
            'export type CommerceGate = "provider_test" | "live_canary" | "live"',
            "export type CommerceReleaseIdentity",
            "productId: string",
            "archiveSize: number",
            "archiveSha256: string",
            "sourceCommit: string",
            "releaseCheckoutCustomData",
            "pq_product_id",
            "pq_product_version",
            "pq_archive_sha256",
            "pq_archive_size",
            "pq_gate",
        ),
    )

    require_tokens(
        "Developer Pack release adapter",
        developer_release,
        (
            'productId: "pq-developer-pack"',
            'version: "1.1.0"',
            "archiveSize: 86763",
            'archiveSha256: "546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009"',
            "CommerceReleaseIdentity",
            "buildReleaseCheckoutCustomData(DEVELOPER_PACK_RELEASE, gate)",
        ),
    )

    require_tokens(
        "Starter release adapter",
        starter_release,
        (
            f'productId: "{CANONICAL_STARTER_ID}"',
            'version: "1.0.0-candidate"',
            'archiveName: "prompt-machine-starter-collection-v1.zip"',
            f"archiveSize: {STARTER_ARCHIVE_SIZE}",
            f'archiveSha256: "{STARTER_ARCHIVE_SHA256}"',
            "CommerceReleaseIdentity",
            "starterReleaseCheckoutCustomData",
            "buildReleaseCheckoutCustomData(STARTER_COLLECTION_RELEASE, gate)",
        ),
    )

    require_tokens(
        "signed-order evidence core",
        lib,
        (
            'createHmac("sha256"',
            "timingSafeEqual",
            'eventName !== "order_created"',
            'attributes.status !== "paid"',
            "store_mismatch",
            "product_mismatch",
            "variant_mismatch",
            "live_order_not_allowed_during_provider_test",
            "test_order_not_allowed_in_live_mode",
            "release_identity_mismatch",
            "commerce_gate_configuration_mismatch",
            '"provider_test_order_accepted"',
            '"live_delivery_canary_order_accepted"',
            '"purchase_completed"',
            'evidence: "provider_signed_order_created"',
            "config.release",
            "releaseCheckoutCustomData(release, commerceGate)",
        ),
    )

    require_tokens(
        "commerce mode contract",
        mode,
        (
            'export type CommerceMode = "off" | "test" | "live"',
            'if (value === "test" || value === "live") return value',
            'return "off"',
            'envKey = "DEVELOPER_PACK_COMMERCE_MODE"',
            'currentCommerceMode("STARTER_COLLECTION_COMMERCE_MODE")',
        ),
    )

    require_tokens(
        "Developer Pack webhook adapter",
        webhook,
        (
            'request.headers.get("x-signature")',
            'request.headers.get("x-event-name")',
            "commerce_not_configured",
            "invalid_signature",
            "PQ_COMMERCE_EVENT",
            "commerce_gate",
            "DEVELOPER_PACK_RELEASE",
            "release: DEVELOPER_PACK_RELEASE",
            'NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS === "LIVE"',
        ),
    )

    require_tokens(
        "Developer Pack checkout contract",
        checkout,
        (
            "commerce_disabled",
            "commerce_configuration_conflict",
            "provider_test_token_not_configured",
            "provider_test_not_authorized",
            "live_canary_token_not_configured",
            "live_canary_not_authorized",
            "checkout_not_configured",
            "checkout_url_must_use_https",
            '"provider_test_checkout_started"',
            '"live_delivery_canary_checkout_started"',
            '"checkout_started"',
            "checkout[custom][",
            "releaseCheckoutCustomData(gate)",
            "PQ_FUNNEL_EVENT",
            'NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS === "LIVE"',
        ),
    )

    for field in ("source", "medium", "campaign", "content"):
        if field not in checkout or field not in lib:
            fail(f"attribution field is not reconciled through checkout/webhook: {field}")

    for key in (
        "NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE",
        "NEXT_PUBLIC_STARTER_COLLECTION_SALE_STATUS=NOT_FOR_SALE",
        "DEVELOPER_PACK_COMMERCE_MODE=off",
        "STARTER_COLLECTION_COMMERCE_MODE=off",
        "LEMONSQUEEZY_DEVELOPER_PACK_TEST_CHECKOUT_URL=",
        "LEMONSQUEEZY_DEVELOPER_PACK_LIVE_CHECKOUT_URL=",
        "LEMONSQUEEZY_STARTER_TEST_CHECKOUT_URL=",
        "LEMONSQUEEZY_STARTER_LIVE_CHECKOUT_URL=",
        "LEMONSQUEEZY_PROVIDER_TEST_TOKEN=",
        "LEMONSQUEEZY_LIVE_CANARY_TOKEN=",
        "LEMONSQUEEZY_STARTER_PROVIDER_TEST_TOKEN=",
        "LEMONSQUEEZY_STARTER_LIVE_CANARY_TOKEN=",
        "LEMONSQUEEZY_WEBHOOK_SECRET=",
        "LEMONSQUEEZY_STORE_ID=",
        "LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID=",
        "LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID=",
        "LEMONSQUEEZY_STARTER_PRODUCT_ID=",
        "LEMONSQUEEZY_STARTER_VARIANT_ID=",
    ):
        if key not in env:
            fail(f"environment contract missing: {key}")

    for legacy_key in ("NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL", "LEMONSQUEEZY_ALLOW_TEST_MODE"):
        if legacy_key in env:
            fail(f"legacy environment contract still present: {legacy_key}")

    require_tokens(
        "public CTA fail-closed contract",
        link,
        (
            'kind: "free" | "starter" | "paid"',
            'NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS === "LIVE"',
            '"/api/commerce/developer-pack/checkout"',
            '"/developer-pack"',
            '"/starter-collection"',
            f'product_id: "{CANONICAL_STARTER_ID}"',
            "event.preventDefault()",
        ),
    )
    if LEGACY_STARTER_ID in link or LEGACY_STARTER_ID in tracker:
        fail("new customer telemetry still emits the legacy Starter product id")

    # Starter remains physically incapable of checkout until its release gate explicitly changes.
    if STARTER_CHECKOUT_ROUTE.exists():
        fail("Starter checkout route exists before provider/runtime/delivery release gates are closed")

    product = identity.get("product", {})
    aliases = identity.get("legacy_aliases", [])
    rules = identity.get("rules", {})
    if product.get("canonical_product_id") != CANONICAL_STARTER_ID:
        fail("Starter identity contract canonical product id mismatch")
    if not any(row.get("product_id") == LEGACY_STARTER_ID for row in aliases):
        fail("Starter legacy alias is not preserved explicitly")
    if any(row.get("provider_identity_allowed") is not False for row in aliases):
        fail("legacy Starter alias may not be accepted as provider identity")
    for rule in (
        "provider_custom_data_uses_canonical_id",
        "new_analytics_events_use_canonical_id",
        "purchase_receipts_use_canonical_id",
        "delivery_receipts_use_canonical_id",
    ):
        if rules.get(rule) is not True:
            fail(f"Starter canonical identity rule not enforced: {rule}")
    if rules.get("historical_records_rewritten") is not False:
        fail("historical Starter records may not be rewritten during identity migration")

    if custody.get("state") != "CONTRACT_DEFINED_PROVIDER_NOT_PROVISIONED":
        fail("Starter provider custody contract unexpectedly claims provider provisioning")
    artifact = custody.get("canonical_artifact", {})
    if artifact.get("size_bytes") != STARTER_ARCHIVE_SIZE or artifact.get("sha256") != STARTER_ARCHIVE_SHA256:
        fail("Starter custody contract is not bound to the canonical archive")
    current = custody.get("current_truth", {})
    for field in (
        "provider_store_provisioned_for_starter",
        "provider_product_provisioned_for_starter",
        "provider_variant_provisioned_for_starter",
        "canonical_artifact_in_provider_custody",
        "provider_retrieval_hash_verified",
        "provider_test_order_observed",
        "delivery_observed",
        "public_checkout",
        "real_purchase",
        "ready_to_sell",
    ):
        if current.get(field) is not False:
            fail(f"Starter custody truth must remain false before external provisioning: {field}")
    automatic = custody.get("automatic_actions", {})
    if any(automatic.values()):
        fail("Starter custody contract permits an automatic provider/sale action")

    require_tokens(
        "historical Developer Pack provider file verifier",
        provider_verifier,
        (
            '"archive_size": 86763',
            '"archive_sha256": "546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009"',
            'choices=("test", "live")',
            '"customer_delivery_observed": False',
            "download_url",
            "test_mode",
        ),
    )

    commerce_source = (lib + "\n" + webhook + "\n" + checkout).lower()
    for pii in ("user_email", "user_name"):
        if pii in commerce_source:
            fail(f"PII field referenced in commerce evidence path: {pii}")

    for forbidden_client_event in (
        'event: "provider_test_order_accepted"',
        'event: "live_delivery_canary_order_accepted"',
        'event: "purchase_completed"',
    ):
        if forbidden_client_event in tracker:
            fail(f"client tracker is manufacturing provider evidence: {forbidden_client_event}")

    print("COMMERCE V0: PASS")
    print("provider=lemon-squeezy candidate")
    print("commerce_core=generic release identity + signed order evaluator")
    print("developer_adapter=legacy Developer Pack behavior preserved")
    print(f"starter_identity={CANONICAL_STARTER_ID}; legacy alias historical only")
    print("starter_adapter=release identity prepared; commerce mode OFF")
    print("starter_checkout_route=ABSENT")
    print("starter_provider_custody=NOT_PROVISIONED")
    print("purchase_evidence=provider-signed paid order only")
    print("custody_evidence=authorized provider retrieval + local exact hash/size verification")
    print("delivery_evidence=separate receipt required")
    print("client_clicks_do_not_equal_revenue=true")


if __name__ == "__main__":
    main()
