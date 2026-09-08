#!/usr/bin/env python3
"""Lemon Squeezy custody verifier for Starter — Code Review Edition v1.

This wrapper reuses the generic fail-closed Lemon Squeezy verifier while binding
it to the exact final 1.0.0 customer archive identity that passed deterministic
build and pack QA. It performs no provider action unless explicitly invoked with
provider credentials.
"""
from __future__ import annotations

import sys
from typing import Any

import verify_lemonsqueezy_provider_file as generic

PRODUCT_KEY = "starter-code-review"
RELEASE: dict[str, Any] = {
    "component": "starter-code-review-edition-v1",
    "customer_product_id": "prompt-machine-starter-code-review-edition",
    "provider_product_name": "Prompt Machine Starter — Code Review Edition",
    "provider_product_status": "published",
    "price_cents": 900,
    "is_subscription": False,
    "version": "1.0.0",
    "archive_name": "prompt-machine-starter-code-review-edition-v1.0.0.zip",
    "archive_size": 18955,
    "archive_sha256": "9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3",
    "source_commit": "04b8bceb4349bf79d8125f55592bbb6973edb3c1",
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
