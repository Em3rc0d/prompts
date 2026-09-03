#!/usr/bin/env python3
"""Offline regressions for the Lemon Squeezy provider custody verifier.

No network/provider calls are allowed in this test. Provider API responses and
provider file downloads are simulated. The canonical Starter archive bytes are
built locally using the deterministic Starter builder.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = ROOT / "tools" / "verify_lemonsqueezy_provider_file.py"
BUILDER_PATH = ROOT / "tools" / "build_starter_collection_v1.py"

CANONICAL_ID = "prompt-machine-starter-collection"
LEGACY_ID = "pq-developer-starter-collection"
EXPECTED_SIZE = 50918
EXPECTED_SHA256 = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fake_api(path: str, _api_key: str) -> dict[str, Any]:
    if path == "/products/prod_starter":
        return {
            "data": {
                "type": "products",
                "id": "prod_starter",
                "attributes": {"store_id": 321, "test_mode": True},
            }
        }
    if path == "/variants/var_starter":
        return {
            "data": {
                "type": "variants",
                "id": "var_starter",
                "attributes": {"product_id":  "prod_starter", "test_mode": True},
            }
        }
    if path.startswith("/files?"):
        return {
            "data": [
                {
                    "type": "files",
                    "id": "file_starter",
                    "attributes": {
                        "identifier": "starter-fixture",
                        "variant_id": "var_starter",
                        "name": "prompt-machine-starter-collection-v1.zip",
                        "extension": "zip",
                        "version": "1.0.0-candidate",
                        "size": EXPECTED_SIZE,
                        "status": "published",
                        "test_mode": True,
                        "download_url": "https://provider.invalid/starter.zip",
                    },
                }
            ]
        }
    raise AssertionError(f"unexpected simulated provider path: {path}")


def fake_env(name: str) -> str:
    values = {
        "LEMONSQUEEZY_API_KEY": "offline-test-key",
        "LEMONSQUEEZY_STORE_ID": "321",
        "LEMONSQUEEZY_STARTER_PRODUCT_ID": "prod_starter",
        "LEMONSQUEEZY_STARTER_VARIANT_ID": "var_starter",
    }
    if name not in values:
        raise AssertionError(f"unexpected environment read: {name}")
    return values[name]


def invoke(verifier, argv: list[str]) -> dict[str, Any]:
    previous = sys.argv
    output = io.StringIO()
    try:
        sys.argv = [str(VERIFIER_PATH), *argv]
        with contextlib.redirect_stdout(output):
            result = verifier.main()
        assert result == 0
    finally:
        sys.argv = previous
    return json.loads(output.getvalue())


def main() -> int:
    verifier = load_module("provider_verifier", VERIFIER_PATH)
    builder = load_module("starter_builder", BUILDER_PATH)

    assert verifier.RELEASES["starter"]["customer_product_id"] == CANONICAL_ID
    assert LEGACY_ID not in json.dumps(verifier.RELEASES["starter"], sort_keys=True)
    assert verifier.RELEASES["starter"]["archive_size"] == EXPECTED_SIZE
    assert verifier.RELEASES["starter"]["archive_sha256"] == EXPECTED_SHA256

    verifier.api_get = fake_api
    verifier.env = fake_env

    # Metadata can validate provider configuration but MUST NOT become custody evidence.
    metadata = invoke(verifier, ["--product", "starter", "--mode", "test"])
    assert metadata["status"] == "PROVIDER_FILE_METADATA_PASS_NOT_CUSTODY_EVIDENCE"
    assert metadata["evidence_class"] == "PROVIDER_METADATA_OBSERVATION"
    assert metadata["customer_product_id"] == CANONICAL_ID
    assert metadata["provider_file_bytes"]["observed"] is False
    assert metadata["purchase_observed"] is False
    assert metadata["customer_delivery_observed"] is False
    assert metadata["real_revenue_observed"] is False
    assert metadata["ready_to_sell"] is False

    with tempfile.TemporaryDirectory() as tmp:
        archive_path, manifest = builder.build(Path(tmp))
        archive_bytes = archive_path.read_bytes()
        assert len(archive_bytes) == EXPECTED_SIZE
        assert manifest["archive_sha256"] == EXPECTED_SHA256

        verifier.download_bytes = lambda _url: archive_bytes
        custody = invoke(
            verifier,
            ["--product", "starter", "--mode", "test", "--verify-bytes"],
        )
        assert custody["status"] == "PROVIDER_FILE_BYTES_PASS"
        assert custody["evidence_class"] == "PROVIDER_ARTIFACT_CUSTODY_EVIDENCE"
        assert custody["provider_file_bytes"] == {
            "observed": True,
            "size": EXPECTED_SIZE,
            "sha256": EXPECTED_SHA256,
        }
        assert custody["purchase_observed"] is False
        assert custody["customer_delivery_observed"] is False
        assert custody["real_revenue_observed"] is False
        assert custody["ready_to_sell"] is False

        corrupted = bytearray(archive_bytes)
        corrupted[-1] ^= 0x01
        verifier.download_bytes = lambda _url: bytes(corrupted)
        previous = sys.argv
        try:
            sys.argv = [
                str(VERIFIER_PATH),
                "--product",
                "starter",
                "--mode",
                "test",
                "--verify-bytes",
            ]
            try:
                verifier.main()
            except SystemExit as exc:
                assert "downloaded SHA-256 mismatch" in str(exc)
            else:
                raise AssertionError("corrupted provider bytes did not fail closed")
        finally:
            sys.argv = previous

    print("PROVIDER CUSTODY VERIFIER V1: PASS")
    print("provider_calls=0")
    print("metadata_is_custody=false")
    print("exact_provider_bytes_is_custody=true")
    print("corrupted_bytes_fail_closed=true")
    print(f"starter_product_id={CANONICAL_ID}")
    print("legacy_alias_used_by_new_provider_evidence=false")
    print("delivery_observed=false")
    print("real_revenue_observed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
