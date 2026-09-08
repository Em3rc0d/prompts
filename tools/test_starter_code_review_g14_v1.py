#!/usr/bin/env python3
"""Offline G14 regression for Starter — Code Review Edition v1.

No network/provider/model calls are performed. The test validates that the new
release candidate has isolated commerce identity/configuration and that all
provider-facing surfaces stay fail closed by default.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

RELEASE = WEB / "lib/starter-code-review-release.ts"
MODE = WEB / "lib/commerce-mode.ts"
CHECKOUT = WEB / "app/api/commerce/starter-code-review/checkout/route.ts"
WEBHOOK = WEB / "app/api/commerce/lemonsqueezy/starter-code-review-webhook/route.ts"
ENV = WEB / ".env.example"
VERIFIER = ROOT / "tools/verify_lemonsqueezy_starter_code_review_file.py"

PRODUCT_ID = "prompt-machine-starter-code-review-edition"
ARCHIVE = "prompt-machine-starter-code-review-edition-v1.0.0-rc1.zip"
ARCHIVE_BYTES = "14667"
ARCHIVE_SHA = "7ec282ea1766679f425fd5aad526d6382e6a3c5af2caab9ded07e55b9a773cde"
CERT_ID = "PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001"


def require(path: Path, tokens: tuple[str, ...]) -> str:
    if not path.is_file():
        raise SystemExit(f"G14 OFFLINE: FAIL — missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise SystemExit(
                f"G14 OFFLINE: FAIL — {path.relative_to(ROOT)} missing token: {token}"
            )
    return text


def main() -> int:
    release = require(
        RELEASE,
        (
            f'productId: "{PRODUCT_ID}"',
            'version: "1.0.0-rc1"',
            f'archiveName: "{ARCHIVE}"',
            f"archiveSize: {ARCHIVE_BYTES}",
            ARCHIVE_SHA,
            CERT_ID,
            'validatedModel: "gemini-3.5-flash"',
            'portabilityClassification: "MODEL_SPECIFIC"',
        ),
    )

    require(
        MODE,
        (
            "currentStarterCodeReviewCommerceMode",
            'currentCommerceMode("STARTER_CODE_REVIEW_COMMERCE_MODE")',
            'return "off"',
        ),
    )

    checkout = require(
        CHECKOUT,
        (
            "currentStarterCodeReviewCommerceMode",
            "STARTER_CODE_REVIEW_RELEASE",
            'NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS === "LIVE"',
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_PROVIDER_TEST_TOKEN",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_LIVE_CANARY_TOKEN",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_TEST_CHECKOUT_URL",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_LIVE_CHECKOUT_URL",
            'commerceMode === "off"',
            'gate = "provider_test"',
            'gate = "live_canary"',
            'gate = "live"',
            "releaseCheckoutCustomData",
        ),
    )

    webhook = require(
        WEBHOOK,
        (
            "currentStarterCodeReviewCommerceMode",
            "STARTER_CODE_REVIEW_RELEASE",
            "evaluateLemonSqueezyWebhook",
            "LEMONSQUEEZY_WEBHOOK_SECRET",
            "LEMONSQUEEZY_STORE_ID",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID",
            'commerceMode === "off"',
            'request.headers.get("x-signature")',
            'request.headers.get("x-event-name")',
            "invalid_signature",
            "provider_order_id",
        ),
    )

    require(
        ENV,
        (
            "NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS=NOT_FOR_SALE",
            "STARTER_CODE_REVIEW_COMMERCE_MODE=off",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_TEST_CHECKOUT_URL=",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_LIVE_CHECKOUT_URL=",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_PROVIDER_TEST_TOKEN=",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_LIVE_CANARY_TOKEN=",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID=",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID=",
        ),
    )

    verifier = require(
        VERIFIER,
        (
            'PRODUCT_KEY = "starter-code-review"',
            f'"customer_product_id": "{PRODUCT_ID}"',
            f'"archive_name": "{ARCHIVE}"',
            f'"archive_size": {ARCHIVE_BYTES}',
            f'"archive_sha256": "{ARCHIVE_SHA}"',
            f'"certification_id": "{CERT_ID}"',
            '"portability_classification": "MODEL_SPECIFIC"',
            '"validated_model": "gemini-3.5-flash"',
            '"product_env": "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID"',
            '"variant_env": "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID"',
        ),
    )

    forbidden_old_identity = (
        "prompt-machine-starter-collection-v1.zip",
        "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97",
    )
    for token in forbidden_old_identity:
        if token in release or token in checkout or token in webhook or token in verifier:
            raise SystemExit(
                f"G14 OFFLINE: FAIL — historical Starter identity leaked into Code Review Edition: {token}"
            )

    for source_name, source in (("checkout", checkout), ("webhook", webhook)):
        lowered = source.lower()
        for pii in ("user_email", "user_name", "payment_details"):
            if pii in lowered:
                raise SystemExit(
                    f"G14 OFFLINE: FAIL — {source_name} references PII/payment field: {pii}"
                )

    print("STARTER CODE REVIEW G14 OFFLINE V1: PASS")
    print(f"product_id={PRODUCT_ID}")
    print(f"archive={ARCHIVE}")
    print(f"archive_bytes={ARCHIVE_BYTES}")
    print(f"archive_sha256={ARCHIVE_SHA}")
    print("commerce_mode_default=off")
    print("public_sale_default=NOT_FOR_SALE")
    print("historical_starter_identity_leak=false")
    print("provider_calls=0")
    print("model_calls=0")
    print("commerce_effects=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
