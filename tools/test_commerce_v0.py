#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

LIB = WEB / "lib" / "lemonsqueezy.ts"
RELEASE = WEB / "lib" / "developer-pack-release.ts"
MODE = WEB / "lib" / "commerce-mode.ts"
WEBHOOK_ROUTE = WEB / "app" / "api" / "commerce" / "lemonsqueezy" / "webhook" / "route.ts"
CHECKOUT_ROUTE = WEB / "app" / "api" / "commerce" / "developer-pack" / "checkout" / "route.ts"
ENV = WEB / ".env.example"
COMMERCE_LINK = WEB / "components" / "commerce-link.tsx"
TRACKER = WEB / "components" / "funnel-tracker.tsx"
PROVIDER_FILE_VERIFIER = ROOT / "tools" / "verify_lemonsqueezy_provider_file.py"


def fail(message: str) -> None:
    raise SystemExit(f"COMMERCE V0: FAIL — {message}")


def require_tokens(label: str, source: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in source:
            fail(f"{label} missing: {token}")


def main() -> None:
    required_files = (
        LIB,
        RELEASE,
        MODE,
        WEBHOOK_ROUTE,
        CHECKOUT_ROUTE,
        ENV,
        COMMERCE_LINK,
        TRACKER,
        PROVIDER_FILE_VERIFIER,
    )
    for path in required_files:
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")

    lib = LIB.read_text(encoding="utf-8")
    release = RELEASE.read_text(encoding="utf-8")
    mode = MODE.read_text(encoding="utf-8")
    webhook = WEBHOOK_ROUTE.read_text(encoding="utf-8")
    checkout = CHECKOUT_ROUTE.read_text(encoding="utf-8")
    env = ENV.read_text(encoding="utf-8")
    link = COMMERCE_LINK.read_text(encoding="utf-8")
    tracker = TRACKER.read_text(encoding="utf-8")
    provider_verifier = PROVIDER_FILE_VERIFIER.read_text(encoding="utf-8")

    require_tokens(
        "signed-order evidence contract",
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
            "commerce_gate",
            "custom_data",
            "cleanAttribution",
            "releaseCheckoutCustomData",
        ),
    )

    require_tokens(
        "release binding contract",
        release,
        (
            'export type CommerceGate = "provider_test" | "live_canary" | "live"',
            'productId: "pq-developer-pack"',
            'version: "1.1.0"',
            "archiveSize: 86763",
            'archiveSha256: "546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009"',
            "pq_product_id",
            "pq_product_version",
            "pq_archive_sha256",
            "pq_archive_size",
            "pq_gate",
        ),
    )

    require_tokens(
        "commerce mode contract",
        mode,
        (
            'export type CommerceMode = "off" | "test" | "live"',
            'if (value === "test" || value === "live") return value',
            'return "off"',
            "DEVELOPER_PACK_COMMERCE_MODE",
        ),
    )

    require_tokens(
        "webhook route contract",
        webhook,
        (
            'request.headers.get("x-signature")',
            'request.headers.get("x-event-name")',
            "commerce_not_configured",
            "invalid_signature",
            "PQ_COMMERCE_EVENT",
            "commerce_gate",
            'commerceMode === "test"',
            "const commerceGate: CommerceGate",
            '"provider_test"',
            '"live_canary"',
            '"live"',
            'NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS === "LIVE"',
        ),
    )

    require_tokens(
        "checkout contract",
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
            'request.headers.get("x-pq-provider-test-token")',
            'request.headers.get("x-pq-live-canary-token")',
        ),
    )

    for field in ("source", "medium", "campaign", "content"):
        if field not in checkout or field not in lib:
            fail(f"attribution field is not reconciled through checkout/webhook: {field}")

    for key in (
        "NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE",
        "DEVELOPER_PACK_COMMERCE_MODE=off",
        "LEMONSQUEEZY_DEVELOPER_PACK_TEST_CHECKOUT_URL=",
        "LEMONSQUEEZY_DEVELOPER_PACK_LIVE_CHECKOUT_URL=",
        "LEMONSQUEEZY_PROVIDER_TEST_TOKEN=",
        "LEMONSQUEEZY_LIVE_CANARY_TOKEN=",
        "LEMONSQUEEZY_WEBHOOK_SECRET=",
        "LEMONSQUEEZY_STORE_ID=",
        "LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID=",
        "LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID=",
    ):
        if key not in env:
            fail(f"environment contract missing: {key}")

    for legacy_key in (
        "NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL",
        "LEMONSQUEEZY_ALLOW_TEST_MODE",
    ):
        if legacy_key in env:
            fail(f"legacy environment contract still present: {legacy_key}")

    require_tokens(
        "paid CTA fail-closed contract",
        link,
        (
            'NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS === "LIVE"',
            '"/api/commerce/developer-pack/checkout"',
            '"/developer-pack"',
            "event.preventDefault()",
        ),
    )
    if "NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL" in link:
        fail("paid CTA still bypasses the server commerce gate with a public checkout URL")

    require_tokens(
        "provider file verifier",
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

    # PII from provider payload must not be copied into our commerce evidence/log path.
    commerce_source = (lib + "\n" + webhook + "\n" + checkout).lower()
    for pii in ("user_email", "user_name"):
        if pii in commerce_source:
            fail(f"PII field referenced in commerce evidence path: {pii}")

    # Client telemetry must not manufacture provider evidence or revenue.
    for forbidden_client_event in (
        'event: "provider_test_order_accepted"',
        'event: "live_delivery_canary_order_accepted"',
        'event: "purchase_completed"',
    ):
        if forbidden_client_event in tracker:
            fail(f"client tracker is manufacturing provider evidence: {forbidden_client_event}")

    print("COMMERCE V0: PASS")
    print("provider=lemon-squeezy")
    print("release_binding=exact version + archive size/hash + commerce gate")
    print("provider_test=private checkout + signed test order; never revenue")
    print("live_canary=private live checkout + signed canary order; never public revenue")
    print("public_live=only state allowed to emit purchase_completed")
    print("test_mode_customer_download=false")
    print("attribution=source/medium/campaign/content via provider custom_data")
    print("pii=excluded from commerce evidence path")
    print("client_clicks_do_not_equal_revenue=true")
    print("external_blocker=full web build + provider custody + controlled provider gates")


if __name__ == "__main__":
    main()
