#!/usr/bin/env python3
"""Read-only Lemon Squeezy G14 discovery/custody probe for Starter Code Review RC2.

The probe never creates products, variants, files, checkouts, orders, or webhooks.
It discovers the current test-mode provider objects from a locally supplied API
key and returns a bounded state: PASS, ACTION_REQUIRED, or BLOCKED.

Secrets are never written to stdout or receipts. If LEMONSQUEEZY_API_KEY is not
present, interactive use prompts with getpass so the key does not echo.
"""
from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, NoReturn

API_BASE = "https://api.lemonsqueezy.com/v1"
STORE_NAME = "Prompt Quarry"
PRODUCT_NAME = "Prompt Machine Starter — Code Review Edition"
PRODUCT_PRICE_CENTS = 900
ARCHIVE_NAME = "prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip"
ARCHIVE_VERSION = "1.0.0-rc2"
ARCHIVE_BYTES = 19161
ARCHIVE_SHA256 = "1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88"


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def api_key(interactive: bool) -> str:
    value = os.environ.get("LEMONSQUEEZY_API_KEY", "").strip()
    if value:
        return value
    if not interactive:
        fail("ACTION_REQUIRED: LEMONSQUEEZY_API_KEY is not loaded locally")
    value = getpass.getpass("Lemon Squeezy API key (hidden, not persisted): ").strip()
    if not value:
        fail("ACTION_REQUIRED: no API key supplied")
    return value


def api_get(path: str, key: str) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{API_BASE}{path}",
        headers={
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {key}",
            "User-Agent": "Prompt-Machine-G14-Discovery/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        fail(f"BLOCKED: Lemon Squeezy API HTTP {exc.code}: {body[:500]}")
    except urllib.error.URLError as exc:
        fail(f"BLOCKED: Lemon Squeezy API unavailable: {exc.reason}")


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Prompt-Machine-G14-Custody/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        fail(f"BLOCKED: provider file download HTTP {exc.code}: {body[:500]}")
    except urllib.error.URLError as exc:
        fail(f"BLOCKED: provider file download unavailable: {exc.reason}")


def list_data(payload: dict[str, Any], expected_type: str) -> list[dict[str, Any]]:
    data = payload.get("data")
    if not isinstance(data, list):
        fail(f"BLOCKED: unexpected {expected_type} list response")
    return [item for item in data if isinstance(item, dict) and item.get("type") == expected_type]


def attr(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("attributes")
    return value if isinstance(value, dict) else {}


def exact(items: list[dict[str, Any]], predicate, label: str) -> dict[str, Any] | None:
    matches = [item for item in items if predicate(item)]
    if not matches:
        return None
    if len(matches) != 1:
        fail(f"BLOCKED: expected one {label}; observed {len(matches)}")
    return matches[0]


def classify_snapshot(
    *,
    stores: list[dict[str, Any]],
    products: list[dict[str, Any]],
    variants: list[dict[str, Any]],
    files: list[dict[str, Any]],
    store_id: str | None = None,
) -> dict[str, Any]:
    store = None
    if store_id:
        store = exact(stores, lambda item: str(item.get("id")) == store_id, "store ID")
    if store is None:
        store = exact(stores, lambda item: attr(item).get("name") == STORE_NAME, f"store named {STORE_NAME!r}")
    if store is None:
        return {
            "state": "ACTION_REQUIRED",
            "stage": "STORE_DISCOVERY",
            "next": f"Use the Lemon Squeezy store named {STORE_NAME!r} or provide --store-id.",
        }

    sid = str(store.get("id"))
    product = exact(
        products,
        lambda item: attr(item).get("name") == PRODUCT_NAME and str(attr(item).get("store_id")) == sid,
        "Code Review Edition product",
    )
    if product is None:
        return {
            "state": "ACTION_REQUIRED",
            "stage": "CREATE_TEST_PRODUCT",
            "store_id": sid,
            "next": f"Create {PRODUCT_NAME!r} in Test mode at $9 one-time, then run this probe again.",
        }

    product_attrs = attr(product)
    if product_attrs.get("test_mode") is not True:
        return {"state": "BLOCKED", "stage": "PRODUCT_MODE", "reason": "product is not test_mode=true"}

    pid = str(product.get("id"))
    candidates = [
        item
        for item in variants
        if str(attr(item).get("product_id")) == pid
        and attr(item).get("test_mode") is True
        and attr(item).get("is_subscription") is False
        and int(attr(item).get("price", -1)) == PRODUCT_PRICE_CENTS
    ]
    if not candidates:
        return {
            "state": "ACTION_REQUIRED",
            "stage": "CREATE_TEST_VARIANT",
            "store_id": sid,
            "product_id": pid,
            "next": "Create a non-subscription $9.00 test-mode variant, then run this probe again.",
        }
    if len(candidates) != 1:
        return {
            "state": "BLOCKED",
            "stage": "VARIANT_AMBIGUITY",
            "reason": f"expected one $9 non-subscription test variant; observed {len(candidates)}",
        }

    variant = candidates[0]
    vid = str(variant.get("id"))
    file_item = exact(
        files,
        lambda item: str(attr(item).get("variant_id")) == vid and attr(item).get("name") == ARCHIVE_NAME,
        "RC2 provider file",
    )
    if file_item is None:
        return {
            "state": "ACTION_REQUIRED",
            "stage": "UPLOAD_RC2",
            "store_id": sid,
            "product_id": pid,
            "variant_id": vid,
            "next": f"Upload exact {ARCHIVE_NAME} to this variant and publish the file, then run this probe again.",
        }

    file_attrs = attr(file_item)
    observed = {
        "name": file_attrs.get("name"),
        "version": str(file_attrs.get("version")),
        "size": int(file_attrs.get("size", -1)),
        "status": file_attrs.get("status"),
        "test_mode": file_attrs.get("test_mode") is True,
    }
    expected = {
        "name": ARCHIVE_NAME,
        "version": ARCHIVE_VERSION,
        "size": ARCHIVE_BYTES,
        "status": "published",
        "test_mode": True,
    }
    if observed != expected:
        return {
            "state": "BLOCKED",
            "stage": "PROVIDER_FILE_METADATA",
            "reason": "provider file metadata differs from frozen RC2 identity",
            "expected": expected,
            "observed": observed,
        }

    return {
        "state": "PASS",
        "stage": "PROVIDER_METADATA",
        "store_id": sid,
        "product_id": pid,
        "variant_id": vid,
        "file_id": str(file_item.get("id")),
        "download_url": file_attrs.get("download_url"),
        "provider_file_metadata": observed,
    }


def self_test() -> int:
    store = {"type": "stores", "id": "1", "attributes": {"name": STORE_NAME}}
    product = {
        "type": "products",
        "id": "2",
        "attributes": {"store_id": 1, "name": PRODUCT_NAME, "test_mode": True},
    }
    variant = {
        "type": "variants",
        "id": "3",
        "attributes": {
            "product_id": 2,
            "test_mode": True,
            "is_subscription": False,
            "price": PRODUCT_PRICE_CENTS,
        },
    }
    file_item = {
        "type": "files",
        "id": "4",
        "attributes": {
            "variant_id": 3,
            "name": ARCHIVE_NAME,
            "version": ARCHIVE_VERSION,
            "size": ARCHIVE_BYTES,
            "status": "published",
            "test_mode": True,
            "download_url": "https://example.invalid/signed",
        },
    }
    a = classify_snapshot(stores=[store], products=[], variants=[], files=[])
    b = classify_snapshot(stores=[store], products=[product], variants=[variant], files=[file_item])
    bad_file = json.loads(json.dumps(file_item))
    bad_file["attributes"]["size"] = ARCHIVE_BYTES + 1
    c = classify_snapshot(stores=[store], products=[product], variants=[variant], files=[bad_file])
    if a.get("stage") != "CREATE_TEST_PRODUCT":
        fail("SELF TEST FAIL: missing-product state")
    if b.get("state") != "PASS":
        fail("SELF TEST FAIL: passing snapshot")
    if c.get("stage") != "PROVIDER_FILE_METADATA":
        fail("SELF TEST FAIL: identity mismatch state")
    print("PM G14 LEMON SQUEEZY PROBE SELF TEST: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Lemon Squeezy G14 discovery/custody probe")
    parser.add_argument("--store-id")
    parser.add_argument("--verify-bytes", action="store_true")
    parser.add_argument("--out", type=pathlib.Path)
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    key = api_key(interactive=not args.non_interactive)
    stores = list_data(api_get("/stores?page[size]=100", key), "stores")

    selected_store_id = args.store_id
    if not selected_store_id:
        selected = exact(stores, lambda item: attr(item).get("name") == STORE_NAME, f"store named {STORE_NAME!r}")
        if selected is not None:
            selected_store_id = str(selected.get("id"))

    products: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    if selected_store_id:
        q = urllib.parse.urlencode({"filter[store_id]": selected_store_id, "page[size]": 100})
        products = list_data(api_get(f"/products?{q}", key), "products")
        selected_product = exact(
            products,
            lambda item: attr(item).get("name") == PRODUCT_NAME,
            "Code Review Edition product",
        )
        if selected_product is not None:
            pid = str(selected_product.get("id"))
            q = urllib.parse.urlencode({"filter[product_id]": pid, "page[size]": 100})
            variants = list_data(api_get(f"/variants?{q}", key), "variants")
            matching_variants = [
                item
                for item in variants
                if attr(item).get("test_mode") is True
                and attr(item).get("is_subscription") is False
                and int(attr(item).get("price", -1)) == PRODUCT_PRICE_CENTS
            ]
            if len(matching_variants) == 1:
                vid = str(matching_variants[0].get("id"))
                q = urllib.parse.urlencode({"filter[variant_id]": vid, "page[size]": 100})
                files = list_data(api_get(f"/files?{q}", key), "files")

    result = classify_snapshot(
        stores=stores,
        products=products,
        variants=variants,
        files=files,
        store_id=args.store_id,
    )

    result.update(
        {
            "schema": "prompt-machine-g14-lemonsqueezy-probe-v1",
            "mode": "test",
            "product_name": PRODUCT_NAME,
            "expected_price_cents": PRODUCT_PRICE_CENTS,
            "expected_archive": {
                "name": ARCHIVE_NAME,
                "version": ARCHIVE_VERSION,
                "bytes": ARCHIVE_BYTES,
                "sha256": ARCHIVE_SHA256,
            },
            "api_key_recorded": False,
            "provider_side_effects": 0,
        }
    )

    if result.get("state") == "PASS" and args.verify_bytes:
        url = result.pop("download_url", None)
        if not isinstance(url, str) or not url.startswith("https://"):
            result.update({"state": "BLOCKED", "stage": "CUSTODY_DOWNLOAD", "reason": "missing HTTPS provider download URL"})
        else:
            body = download_bytes(url)
            observed_sha = hashlib.sha256(body).hexdigest()
            observed_bytes = len(body)
            if observed_bytes != ARCHIVE_BYTES or observed_sha != ARCHIVE_SHA256:
                result.update(
                    {
                        "state": "BLOCKED",
                        "stage": "CUSTODY_BYTES",
                        "reason": "provider-retrieved bytes differ from frozen RC2",
                        "observed_bytes": observed_bytes,
                        "observed_sha256": observed_sha,
                    }
                )
            else:
                result.update(
                    {
                        "stage": "PROVIDER_CUSTODY",
                        "custody_evidence": True,
                        "observed_bytes": observed_bytes,
                        "observed_sha256": observed_sha,
                    }
                )
    else:
        result.pop("download_url", None)
        result["custody_evidence"] = False

    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if result.get("state") in {"PASS", "ACTION_REQUIRED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
