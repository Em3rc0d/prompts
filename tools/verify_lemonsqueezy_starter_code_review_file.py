#!/usr/bin/env python3
"""Lemon Squeezy custody verifier for Verlune Code Review 1.0.0.

This wrapper reuses the generic fail-closed Lemon Squeezy verifier while binding
it to the exact Verlune-branded final customer archive identity that passed
deterministic build and pack QA. It performs no provider action unless explicitly
invoked with provider credentials.
"""
from __future__ import annotations

import sys
from typing import Any

import verify_lemonsqueezy_provider_file as generic

PRODUCT_KEY = "starter-code-review"
RELEASE: dict[str, Any] = {
    "component": "starter-code-review-edition-v1",
    "customer_product_id": "prompt-machine-starter-code-review-edition",
    "provider_product_name": "Verlune Code Review",
    "provider_product_status": "published",
    "price_cents": 900,
    "is_subscription": False,
    "version": "1.0.0",
    "archive_name": "verlune-code-review-v1.0.0.zip",
    "archive_size": 18859,
    "archive_sha256": "4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649",
    "source_commit": "a6c6b4c79606bdc1b386980da34675a66feb4b4a",
    "certification_id": "PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001",
    "portability_classification": "MODEL_SPECIFIC",
    "validated_model": "gemini-3.5-flash",
    "customer_license_frozen": True,
    "customer_license_version": "1.0",
    "sale_terms_version": "1.0",
    "product_env": "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID",
    "variant_env": "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID",
}

generic.RELEASES[PRODUCT_KEY] = RELEASE


def main() -> int:
    if "--product" not in sys.argv[1:]:
        sys.argv[1:1] = ["--product", PRODUCT_KEY]
    return generic.main()


if __name__ == "__main__":
    raise SystemExit(main())
