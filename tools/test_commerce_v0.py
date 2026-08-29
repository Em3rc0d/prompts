#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

LIB = WEB / "lib" / "lemonsqueezy.ts"
ROUTE = WEB / "app" / "api" / "commerce" / "lemonsqueezy" / "webhook" / "route.ts"
ENV = WEB / ".env.example"
COMMERCE_LINK = WEB / "components" / "commerce-link.tsx"
TRACKER = WEB / "components" / "funnel-tracker.tsx"


def fail(message: str) -> None:
    raise SystemExit(f"COMMERCE V0: FAIL — {message}")


def main() -> None:
    for path in (LIB, ROUTE, ENV, COMMERCE_LINK, TRACKER):
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")

    lib = LIB.read_text(encoding="utf-8")
    route = ROUTE.read_text(encoding="utf-8")
    env = ENV.read_text(encoding="utf-8")
    link = COMMERCE_LINK.read_text(encoding="utf-8")
    tracker = TRACKER.read_text(encoding="utf-8")

    for token in (
        'createHmac("sha256"',
        "timingSafeEqual",
        'eventName !== "order_created"',
        'attributes.status !== "paid"',
        "store_mismatch",
        "product_mismatch",
        "variant_mismatch",
        "test_mode_not_allowed",
        'event: "purchase_completed"',
        'evidence: "provider_signed_order_created"',
    ):
        if token not in lib:
            fail(f"signed-order evidence contract missing: {token}")

    for token in (
        'request.headers.get("x-signature")',
        'request.headers.get("x-event-name")',
        "commerce_not_configured",
        "invalid_signature",
        "PQ_COMMERCE_EVENT",
        'event: "purchase_completed"',
    ):
        if token not in route:
            fail(f"webhook route contract missing: {token}")

    for key in (
        "NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL",
        "LEMONSQUEEZY_WEBHOOK_SECRET",
        "LEMONSQUEEZY_STORE_ID",
        "LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID",
        "LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID",
        "LEMONSQUEEZY_ALLOW_TEST_MODE=false",
    ):
        if key not in env:
            fail(f"environment contract missing: {key}")

    if "NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL" not in link:
        fail("paid CTA is not bound to checkout environment configuration")
    if "checkout-unavailable" not in link or "event.preventDefault()" not in link:
        fail("paid CTA does not fail closed when checkout is missing")

    # PII from provider payload must not be copied into our commerce evidence/log path.
    commerce_source = (lib + "\n" + route).lower()
    for pii in ("user_email", "user_name"):
        if pii in commerce_source:
            fail(f"PII field referenced in commerce evidence path: {pii}")

    # Client telemetry must not manufacture a purchase event.
    if 'event: "purchase_completed"' in tracker:
        fail("client tracker is manufacturing purchase_completed")

    print("COMMERCE V0: PASS")
    print("provider=lemon-squeezy")
    print("purchase_evidence=signed order_created + paid + store/product/variant match")
    print("pii=excluded from commerce evidence path")
    print("client_clicks_do_not_equal_revenue=true")
    print("external_blocker=real checkout URL + provider IDs + webhook secret must be provisioned")


if __name__ == "__main__":
    main()
