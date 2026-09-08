#!/usr/bin/env python3
"""Lemon Squeezy custody verifier for Starter — Code Review Edition v1.

This wrapper reuses the generic fail-closed Lemon Squeezy verifier while binding
it to the exact licensed RC2 archive identity that passed G12/G13. It performs
no provider action unless explicitly invoked with provider credentials.
"""
from __future__ import annotations

import sys
from typing import Any

import verify_lemonsqueezy_provider_file as generic

PRODUCT_KEY = "starter-code-review"
RELEASE: dict[str, Any] = {
    "component": "starter-code-review-edition-v1",
    "customer_product_id": "prompt-machine-starter-code-review-edition",
    "version": "1.0.0-rc2",
    "archive_name": "prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip",
    "archive_size": 19161,
    "archive_sha256": "1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88",
    "source_commit": "c2e9667f4382e589d1430db609215d369486bbfe",
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
