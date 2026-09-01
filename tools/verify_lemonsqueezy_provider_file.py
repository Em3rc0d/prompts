#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API_BASE = "https://api.lemonsqueezy.com/v1"
EXPECTED = {
    "product_id": "pq-developer-pack",
    "version": "1.1.0",
    "archive_name": "prompt-quarry-developer-pack-v1.1.0.zip",
    "archive_size": 86763,
    "archive_sha256": "546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009",
    "source_fingerprint_sha256": "dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa",
}


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        fail(f"missing required environment variable: {name}")
    return value


def api_get(path: str, api_key: str) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{API_BASE}{path}",
        headers={
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "Prompt-Quarry-Provider-Gate/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        fail(f"Lemon Squeezy API HTTP {exc.code}: {body[:500]}")
    except urllib.error.URLError as exc:
        fail(f"Lemon Squeezy API unavailable: {exc.reason}")


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Prompt-Quarry-Provider-Gate/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        fail(f"provider file download HTTP {exc.code}: {body[:500]}")
    except urllib.error.URLError as exc:
        fail(f"provider file download unavailable: {exc.reason}")


def data_object(payload: dict[str, Any], expected_type: str) -> dict[str, Any]:
    data = payload.get("data")
    if not isinstance(data, dict) or data.get("type") != expected_type:
        fail(f"unexpected API object; expected {expected_type}")
    return data


def id_matches(observed: Any, expected: str, label: str) -> None:
    if str(observed) != expected:
        fail(f"{label} mismatch: expected {expected}, observed {observed}")


def verify_test_mode(attributes: dict[str, Any], expected: bool, label: str) -> None:
    observed = attributes.get("test_mode") is True
    if observed != expected:
        fail(f"{label} test_mode mismatch: expected {expected}, observed {observed}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify that Lemon Squeezy custody points to the exact Prompt Quarry Developer Pack v1.1.0 release artifact."
    )
    parser.add_argument("--mode", choices=("test", "live"), required=True)
    parser.add_argument("--verify-bytes", action="store_true", help="Download the provider file URL and verify exact bytes/SHA-256.")
    parser.add_argument("--out", type=pathlib.Path, help="Optional path for the JSON receipt.")
    args = parser.parse_args()

    api_key = env("LEMONSQUEEZY_API_KEY")
    store_id = env("LEMONSQUEEZY_STORE_ID")
    product_id = env("LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID")
    variant_id = env("LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID")
    expect_test = args.mode == "test"

    product = data_object(api_get(f"/products/{urllib.parse.quote(product_id)}", api_key), "products")
    product_attributes = product.get("attributes") or {}
    id_matches(product.get("id"), product_id, "product_id")
    id_matches(product_attributes.get("store_id"), store_id, "product.store_id")
    verify_test_mode(product_attributes, expect_test, "product")

    variant = data_object(api_get(f"/variants/{urllib.parse.quote(variant_id)}", api_key), "variants")
    variant_attributes = variant.get("attributes") or {}
    id_matches(variant.get("id"), variant_id, "variant_id")
    id_matches(variant_attributes.get("product_id"), product_id, "variant.product_id")
    verify_test_mode(variant_attributes, expect_test, "variant")

    query = urllib.parse.urlencode({"filter[variant_id]": variant_id})
    files_payload = api_get(f"/files?{query}", api_key)
    files = files_payload.get("data")
    if not isinstance(files, list):
        fail("unexpected files list response")

    matches = []
    for item in files:
        if not isinstance(item, dict) or item.get("type") != "files":
            continue
        attributes = item.get("attributes") or {}
        if attributes.get("name") == EXPECTED["archive_name"]:
            matches.append(item)

    if len(matches) != 1:
        fail(f"expected exactly one provider file named {EXPECTED['archive_name']}; observed {len(matches)}")

    file_object = matches[0]
    file_attributes = file_object.get("attributes") or {}
    id_matches(file_attributes.get("variant_id"), variant_id, "file.variant_id")
    verify_test_mode(file_attributes, expect_test, "file")

    if file_attributes.get("extension") != "zip":
        fail(f"file extension mismatch: {file_attributes.get('extension')}")
    if file_attributes.get("status") != "published":
        fail(f"file status must be published; observed {file_attributes.get('status')}")
    if str(file_attributes.get("version")) != EXPECTED["version"]:
        fail(f"file version mismatch: expected {EXPECTED['version']}, observed {file_attributes.get('version')}")
    if int(file_attributes.get("size", -1)) != EXPECTED["archive_size"]:
        fail(f"file size mismatch: expected {EXPECTED['archive_size']}, observed {file_attributes.get('size')}")

    bytes_receipt: dict[str, Any] = {
        "observed": False,
        "reason": "not_requested",
    }
    if args.verify_bytes:
        download_url = file_attributes.get("download_url")
        if not isinstance(download_url, str) or not download_url.startswith("https://"):
            fail("provider file has no HTTPS download_url")
        body = download_bytes(download_url)
        observed_sha256 = hashlib.sha256(body).hexdigest()
        if len(body) != EXPECTED["archive_size"]:
            fail(f"downloaded size mismatch: expected {EXPECTED['archive_size']}, observed {len(body)}")
        if observed_sha256 != EXPECTED["archive_sha256"]:
            fail(f"downloaded SHA-256 mismatch: expected {EXPECTED['archive_sha256']}, observed {observed_sha256}")
        bytes_receipt = {
            "observed": True,
            "size": len(body),
            "sha256": observed_sha256,
        }

    receipt = {
        "schema": "prompt-quarry-lemonsqueezy-provider-file-receipt-v1",
        "component": "developer-pack-v1.1",
        "mode": args.mode,
        "status": "PROVIDER_FILE_BYTES_PASS" if args.verify_bytes else "PROVIDER_FILE_METADATA_PASS",
        "store_id": store_id,
        "product_id": product_id,
        "variant_id": variant_id,
        "provider_file_id": str(file_object.get("id")),
        "provider_file_identifier": file_attributes.get("identifier"),
        "provider_file": {
            "name": file_attributes.get("name"),
            "extension": file_attributes.get("extension"),
            "version": file_attributes.get("version"),
            "size": file_attributes.get("size"),
            "status": file_attributes.get("status"),
            "test_mode": file_attributes.get("test_mode") is True,
        },
        "expected_release": EXPECTED,
        "provider_file_bytes": bytes_receipt,
        "customer_delivery_observed": False,
        "evidence_boundary": (
            "Provider custody/metadata and optional API download bytes only. "
            "This receipt does not prove a customer successfully downloaded the artifact after purchase."
        ),
    }

    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
