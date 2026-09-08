#!/usr/bin/env python3
"""Read-only Lemon Squeezy G14 discovery probe for Verlune Code Review 1.0.0.

This probe is intentionally test-mode only. Lemon Squeezy disables file downloads
for test-mode purchases, so this probe can establish provider metadata, product,
variant and checkout identity, but never byte custody. Byte custody belongs to the
separate live-canary verifier.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, NoReturn

API_BASE = "https://api.lemonsqueezy.com/v1"
CANONICAL_TEST_STORE_ID = "462419"
STORE_NAME = "Verlune"
PRODUCT_NAME = "Verlune Code Review"
PRODUCT_PRICE_CENTS = 900
ARCHIVE_NAME = "verlune-code-review-v1.0.0.zip"
ARCHIVE_VERSION = "1.0.0"
ARCHIVE_BYTES = 18859
ARCHIVE_SHA256 = "4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649"


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
            "User-Agent": "Prompt-Machine-G14-Discovery/1.4",
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


def classify_snapshot(*, stores: list[dict[str, Any]], products: list[dict[str, Any]], variants: list[dict[str, Any]], files: list[dict[str, Any]], store_id: str | None = None) -> dict[str, Any]:
    target_store_id = store_id or CANONICAL_TEST_STORE_ID
    store = exact(stores, lambda item: str(item.get("id")) == target_store_id, "canonical Test store ID")
    if store is None:
        return {"state": "ACTION_REQUIRED", "stage": "STORE_DISCOVERY", "next": f"Use Lemon Test store id {target_store_id}."}
    if attr(store).get("name") != STORE_NAME:
        return {
            "state": "ACTION_REQUIRED",
            "stage": "STORE_BRANDING",
            "store_id": target_store_id,
            "expected_store_name": STORE_NAME,
            "observed_store_name": attr(store).get("name"),
            "next": "Rename the customer-visible Lemon store to Verlune before final Test validation.",
        }

    sid = str(store.get("id"))
    product = exact(products, lambda item: attr(item).get("name") == PRODUCT_NAME and str(attr(item).get("store_id")) == sid, "Verlune Code Review product")
    if product is None:
        return {"state": "ACTION_REQUIRED", "stage": "RENAME_OR_CREATE_TEST_PRODUCT", "store_id": sid, "next": f"Use product name {PRODUCT_NAME!r} in Test mode at $9 one-time."}

    pa = attr(product)
    if pa.get("test_mode") is not True:
        return {"state": "BLOCKED", "stage": "PRODUCT_MODE", "reason": "product is not test_mode=true"}
    if pa.get("status") != "published":
        return {"state": "ACTION_REQUIRED", "stage": "PUBLISH_TEST_PRODUCT", "reason": "product must be published inside Test mode"}

    pid = str(product.get("id"))
    candidates = [item for item in variants if str(attr(item).get("product_id")) == pid and attr(item).get("test_mode") is True and attr(item).get("is_subscription") is False and int(attr(item).get("price", -1)) == PRODUCT_PRICE_CENTS]
    if not candidates:
        return {"state": "ACTION_REQUIRED", "stage": "CREATE_TEST_VARIANT", "store_id": sid, "product_id": pid}
    if len(candidates) != 1:
        return {"state": "BLOCKED", "stage": "VARIANT_AMBIGUITY", "reason": f"expected one $9 test variant; observed {len(candidates)}"}
    variant = candidates[0]
    vid = str(variant.get("id"))

    file_item = exact(files, lambda item: str(attr(item).get("variant_id")) == vid and attr(item).get("name") == ARCHIVE_NAME, "Verlune final 1.0.0 provider file")
    if file_item is None:
        return {"state": "ACTION_REQUIRED", "stage": "UPLOAD_VERLUNE_1_0_0", "store_id": sid, "product_id": pid, "variant_id": vid}

    fa = attr(file_item)
    raw_version = fa.get("version")
    version = None if raw_version in {None, ""} else str(raw_version)
    if version is not None and version != ARCHIVE_VERSION:
        return {"state": "BLOCKED", "stage": "PROVIDER_FILE_VERSION", "expected_version": ARCHIVE_VERSION, "observed_version": version}

    observed = {"name": fa.get("name"), "size": int(fa.get("size", -1)), "status": fa.get("status"), "test_mode": fa.get("test_mode") is True}
    expected = {"name": ARCHIVE_NAME, "size": ARCHIVE_BYTES, "status": "published", "test_mode": True}
    if observed != expected:
        return {"state": "BLOCKED", "stage": "PROVIDER_FILE_METADATA", "expected": expected, "observed": observed}

    buy_now = pa.get("buy_now_url")
    checkout_url = buy_now if isinstance(buy_now, str) and buy_now.startswith("https://") and "/checkout/buy/" in buy_now else None
    return {
        "state": "PASS",
        "stage": "PROVIDER_METADATA_TEST_MODE",
        "brand": STORE_NAME,
        "product_name": PRODUCT_NAME,
        "store_id": sid,
        "product_id": pid,
        "variant_id": vid,
        "file_id": str(file_item.get("id")),
        "provider_checkout_url": checkout_url,
        "provider_file_metadata": {**observed, "version": version, "version_required_for_custody": False},
    }


def self_test() -> int:
    store = {"type": "stores", "id": CANONICAL_TEST_STORE_ID, "attributes": {"name": STORE_NAME}}
    product = {"type": "products", "id": "2", "attributes": {"store_id": int(CANONICAL_TEST_STORE_ID), "name": PRODUCT_NAME, "status": "published", "test_mode": True, "buy_now_url": "https://verlune.lemonsqueezy.com/checkout/buy/test"}}
    variant = {"type": "variants", "id": "3", "attributes": {"product_id": 2, "test_mode": True, "is_subscription": False, "price": PRODUCT_PRICE_CENTS}}
    file_item = {"type": "files", "id": "4", "attributes": {"variant_id": 3, "name": ARCHIVE_NAME, "size": ARCHIVE_BYTES, "version": None, "status": "published", "test_mode": True}}
    ok = classify_snapshot(stores=[store], products=[product], variants=[variant], files=[file_item])
    if ok.get("state") != "PASS" or ok.get("stage") != "PROVIDER_METADATA_TEST_MODE":
        fail("SELF TEST FAIL: passing Verlune test-mode snapshot")
    old_brand = json.loads(json.dumps(store))
    old_brand["attributes"]["name"] = "Prompt Quarry"
    brand = classify_snapshot(stores=[old_brand], products=[product], variants=[variant], files=[file_item])
    if brand.get("stage") != "STORE_BRANDING":
        fail("SELF TEST FAIL: old store brand must not pass")
    wrong = json.loads(json.dumps(file_item))
    wrong["attributes"]["size"] = ARCHIVE_BYTES + 1
    bad = classify_snapshot(stores=[store], products=[product], variants=[variant], files=[wrong])
    if bad.get("stage") != "PROVIDER_FILE_METADATA":
        fail("SELF TEST FAIL: size mismatch")
    print("PM G14 LEMON SQUEEZY VERLUNE PROBE SELF TEST: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Lemon Squeezy G14 Test discovery probe for Verlune")
    parser.add_argument("--store-id", default=CANONICAL_TEST_STORE_ID)
    parser.add_argument("--verify-bytes", action="store_true", help="deprecated in Test mode; records byte custody as unavailable")
    parser.add_argument("--out", type=pathlib.Path)
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    key = api_key(interactive=not args.non_interactive)
    stores = list_data(api_get("/stores?page[size]=100", key), "stores")
    selected_store_id = args.store_id

    products: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    if selected_store_id:
        q = urllib.parse.urlencode({"filter[store_id]": selected_store_id, "page[size]": 100})
        products = list_data(api_get(f"/products?{q}", key), "products")
        selected_product = exact(products, lambda item: attr(item).get("name") == PRODUCT_NAME, "Verlune Code Review product")
        if selected_product is not None:
            pid = str(selected_product.get("id"))
            q = urllib.parse.urlencode({"filter[product_id]": pid, "page[size]": 100})
            variants = list_data(api_get(f"/variants?{q}", key), "variants")
            matching = [item for item in variants if attr(item).get("test_mode") is True and attr(item).get("is_subscription") is False and int(attr(item).get("price", -1)) == PRODUCT_PRICE_CENTS]
            if len(matching) == 1:
                vid = str(matching[0].get("id"))
                q = urllib.parse.urlencode({"filter[variant_id]": vid, "page[size]": 100})
                files = list_data(api_get(f"/files?{q}", key), "files")

    result = classify_snapshot(stores=stores, products=products, variants=variants, files=files, store_id=selected_store_id)
    result.update({
        "schema": "prompt-machine-g14-lemonsqueezy-probe-v1.4",
        "mode": "test",
        "expected_brand": STORE_NAME,
        "expected_product_name": PRODUCT_NAME,
        "expected_price_cents": PRODUCT_PRICE_CENTS,
        "expected_archive": {"name": ARCHIVE_NAME, "version": ARCHIVE_VERSION, "bytes": ARCHIVE_BYTES, "sha256": ARCHIVE_SHA256},
        "api_key_recorded": False,
        "provider_side_effects": 0,
        "byte_custody_evidence": False,
        "byte_custody_test_mode": "NOT_OBSERVABLE_BY_PROVIDER_DESIGN",
        "verify_bytes_requested": bool(args.verify_bytes),
        "live_byte_verification_tool": "tools/verify_lemonsqueezy_starter_code_review_file.py",
    })
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if result.get("state") in {"PASS", "ACTION_REQUIRED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
