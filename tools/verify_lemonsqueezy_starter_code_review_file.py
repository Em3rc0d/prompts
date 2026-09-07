#!/usr/bin/env python3
"""Lemon Squeezy custody verifier for Starter — Code Review Edition v1.

This wrapper reuses the generic fail-closed Lemon Squeezy verifier while binding
it to the exact G12/G13 release-candidate archive identity. It performs no
provider action unless explicitly invoked with provider credentials.
"""
from __future__ import annotations

import sys
from typing import Any

import verify_lemonsqueezy_provider_file as generic

PRODUCT_KEY = "starter-code-review"
RELEASE: dict[str, Any] = {
    "component": "starter-code-review-edition-v1",
    "customer_product_id": "prompt-machine-starter-code-review-edition",
    "version": "1.0.0-rc1",
    "archive_name": "prompt-machine-starter-code-review-edition-v1.0.0-rc1.zip",
    "archive_size": 14667,
    "archive_sha256": "7ec282ea1766679f425fd5aad526d6382e6a3c5af2caab9ded07e55b9a773cde",
    "source_commit": "010bc9400c7804160644d7f60ee9134c8546f63b",
    "certification_id": "PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001",
    "portability_classification": "MODEL_SPECIFIC",
    "validated_model": "gemini-3.5-flash",
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
