#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
ROUTE = WEB / "app/api/commerce/lemonsqueezy/starter-webhook/route.ts"
STARTER_RELEASE = WEB / "lib/starter-collection-release.ts"
MODE = WEB / "lib/commerce-mode.ts"
ENV = WEB / ".env.example"
LINK = WEB / "components/commerce-link.tsx"
STARTER_CHECKOUT = WEB / "app/api/commerce/starter-collection/checkout/route.ts"

CANONICAL_ID = "prompt-machine-starter-collection"
LEGACY_ID = "pq-developer-starter-collection"


def require(label: str, source: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in source:
            raise SystemExit(f"STARTER WEBHOOK ADAPTER V1: FAIL — {label} missing: {token}")


def main() -> int:
    for path in (ROUTE, STARTER_RELEASE, MODE, ENV, LINK):
        if not path.is_file():
            raise SystemExit(f"STARTER WEBHOOK ADAPTER V1: FAIL — missing {path.relative_to(ROOT)}")

    route = ROUTE.read_text(encoding="utf-8")
    release = STARTER_RELEASE.read_text(encoding="utf-8")
    mode = MODE.read_text(encoding="utf-8")
    env = ENV.read_text(encoding="utf-8")
    link = LINK.read_text(encoding="utf-8")

    require(
        "signed Starter webhook",
        route,
        (
            "currentStarterCommerceMode",
            "STARTER_COLLECTION_RELEASE",
            "evaluateLemonSqueezyWebhook",
            'commerceMode === "off"',
            'NEXT_PUBLIC_STARTER_COLLECTION_SALE_STATUS === "LIVE"',
            "LEMONSQUEEZY_WEBHOOK_SECRET",
            "LEMONSQUEEZY_STORE_ID",
            "LEMONSQUEEZY_STARTER_PRODUCT_ID",
            "LEMONSQUEEZY_STARTER_VARIANT_ID",
            "release: STARTER_COLLECTION_RELEASE",
            "starter_commerce_not_configured",
            'request.headers.get("x-signature")',
            'request.headers.get("x-event-name")',
            "invalid_signature",
            "PM_STARTER_COMMERCE_EVENT",
            "provider_order_id",
        ),
    )
    for pii in ("user_email", "user_name", "payment_details"):
        if pii in route.lower():
            raise SystemExit(f"STARTER WEBHOOK ADAPTER V1: FAIL — PII/payment field referenced: {pii}")

    require(
        "Starter release identity",
        release,
        (
            f'productId: "{CANONICAL_ID}"',
            'version: "1.0.0-candidate"',
            "archiveSize: 50918",
            "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97",
        ),
    )
    if LEGACY_ID in release or LEGACY_ID in route:
        raise SystemExit("STARTER WEBHOOK ADAPTER V1: FAIL — legacy Starter id used by new provider path")

    require(
        "Starter commerce mode",
        mode,
        (
            "currentStarterCommerceMode",
            'currentCommerceMode("STARTER_COLLECTION_COMMERCE_MODE")',
            'return "off"',
        ),
    )
    require(
        "Starter environment defaults",
        env,
        (
            "NEXT_PUBLIC_STARTER_COLLECTION_SALE_STATUS=NOT_FOR_SALE",
            "STARTER_COLLECTION_COMMERCE_MODE=off",
            "LEMONSQUEEZY_STARTER_PRODUCT_ID=",
            "LEMONSQUEEZY_STARTER_VARIANT_ID=",
        ),
    )

    if STARTER_CHECKOUT.exists():
        raise SystemExit("STARTER WEBHOOK ADAPTER V1: FAIL — Starter checkout route exists before release authorization")
    if "/api/commerce/starter-collection/checkout" in link:
        raise SystemExit("STARTER WEBHOOK ADAPTER V1: FAIL — customer CTA exposes a Starter checkout path")
    require("Starter CTA hold", link, ('kind === "starter"', '"/starter-collection"'))

    print("STARTER WEBHOOK ADAPTER V1: PASS")
    print(f"product_id={CANONICAL_ID}")
    print("commerce_mode_default=off")
    print("public_sale_default=NOT_FOR_SALE")
    print("signed_webhook_adapter=present")
    print("starter_checkout_route=absent")
    print("provider_calls=0")
    print("purchase_observations=0")
    print("delivery_observations=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
