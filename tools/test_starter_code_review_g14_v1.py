#!/usr/bin/env python3
"""Offline G14 regression for Starter — Code Review Edition v1.

No network/provider/model calls are performed. The test validates that the
licensed RC2 has isolated commerce identity/configuration and that all
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
SOURCE_MANIFEST = ROOT / "product/starter-code-review-edition-v1/MANIFEST.source.json"

PRODUCT_ID = "prompt-machine-starter-code-review-edition"
VERSION = "1.0.0-rc2"
ARCHIVE = "prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip"
ARCHIVE_BYTES = "19161"
ARCHIVE_SHA = "1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88"
SOURCE_COMMIT = "c2e9667f4382e589d1430db609215d369486bbfe"
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
    # The web release adapter intentionally contains only generic commerce
    # release identity. Certification/model scope belongs in the governed
    # provider verifier and receipts, not CommerceReleaseIdentity.
    release = require(
        RELEASE,
        (
            f'productId: "{PRODUCT_ID}"',
            f'version: "{VERSION}"',
            f'archiveName: "{ARCHIVE}"',
            f"archiveSize: {ARCHIVE_BYTES}",
            ARCHIVE_SHA,
            SOURCE_COMMIT,
            "CommerceReleaseIdentity",
        ),
    )

    source_manifest = require(
        SOURCE_MANIFEST,
        (
            f'"version": "{VERSION}"',
            '"customer_license_frozen": true',
            '"customer_license_version": "1.0"',
            '"sale_terms_version": "1.0"',
            '"CUSTOMER-LICENSE.md"',
            '"SALE-TERMS.md"',
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
            'mode === "off"',
            'gate = "provider_test"',
            'gate = "live_canary"',
            'gate = "live"',
            "starterCodeReviewCheckoutCustomData",
            'request.headers.get("x-pm-starter-code-review-provider-test-token")',
            'request.headers.get("x-pm-starter-code-review-live-canary-token")',
        ),
    )

    webhook = require(
        WEBHOOK,
        (
            "currentStarterCodeReviewCommerceMode",
            "STARTER_CODE_REVIEW_RELEASE",
            "evaluateLemonSqueezyWebhook",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_WEBHOOK_SECRET",
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
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_WEBHOOK_SECRET=",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID=",
            "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID=",
        ),
    )

    verifier = require(
        VERIFIER,
        (
            'PRODUCT_KEY = "starter-code-review"',
            f'"customer_product_id": "{PRODUCT_ID}"',
            f'"version": "{VERSION}"',
            f'"archive_name": "{ARCHIVE}"',
            f'"archive_size": {ARCHIVE_BYTES}',
            f'"archive_sha256": "{ARCHIVE_SHA}"',
            f'"source_commit": "{SOURCE_COMMIT}"',
            f'"certification_id": "{CERT_ID}"',
            '"portability_classification": "MODEL_SPECIFIC"',
            '"validated_model": "gemini-3.5-flash"',
            '"customer_license_frozen": True',
            '"customer_license_version": "1.0"',
            '"sale_terms_version": "1.0"',
            '"product_env": "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID"',
            '"variant_env": "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID"',
        ),
    )

    forbidden_old_identity = (
        "prompt-machine-starter-collection-v1.zip",
        "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97",
        "prompt-machine-starter-code-review-edition-v1.0.0-rc1.zip",
        "7ec282ea1766679f425fd5aad526d6382e6a3c5af2caab9ded07e55b9a773cde",
    )
    for token in forbidden_old_identity:
        if token in release or token in checkout or token in webhook or token in verifier:
            raise SystemExit(
                f"G14 OFFLINE: FAIL — superseded release identity leaked into Code Review Edition: {token}"
            )

    if '"customer_license_frozen": false' in source_manifest:
        raise SystemExit("G14 OFFLINE: FAIL — rc2 customer license unexpectedly not frozen")

    for source_name, source in (("checkout", checkout), ("webhook", webhook)):
        lowered = source.lower()
        for pii in ("user_email", "user_name", "payment_details"):
            if pii in lowered:
                raise SystemExit(
                    f"G14 OFFLINE: FAIL — {source_name} references PII/payment field: {pii}"
                )

    print("STARTER CODE REVIEW G14 OFFLINE V1: PASS")
    print(f"product_id={PRODUCT_ID}")
    print(f"version={VERSION}")
    print(f"archive={ARCHIVE}")
    print(f"archive_bytes={ARCHIVE_BYTES}")
    print(f"archive_sha256={ARCHIVE_SHA}")
    print("customer_license_frozen=true")
    print("commerce_mode_default=off")
    print("public_sale_default=NOT_FOR_SALE")
    print("dedicated_webhook_secret=true")
    print("certification_scope_bound_in_provider_verifier=true")
    print("superseded_release_identity_leak=false")
    print("provider_calls=0")
    print("model_calls=0")
    print("commerce_effects=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
