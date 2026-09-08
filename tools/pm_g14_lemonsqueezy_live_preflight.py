#!/usr/bin/env python3
"""Prompt Machine G14 Live-mode Lemon Squeezy preflight.

Read-only. With a Live API key it discovers the canonical Live product/variant/file
and, optionally, verifies exact provider-held bytes. It never creates orders,
webhooks, products, discounts, or public checkout state.
"""
from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, NoReturn

API_BASE = "https://api.lemonsqueezy.com/v1"
STORE_NAME = "Prompt Quarry"
PRODUCT_NAME = "Prompt Machine Starter — Code Review Edition"
PRICE_CENTS = 900
VERSION = "1.0.0"
ARCHIVE_NAME = "prompt-machine-starter-code-review-edition-v1.0.0.zip"
ARCHIVE_BYTES = 18955
ARCHIVE_SHA256 = "9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3"


def emit(state: str, stage: str, **extra: object) -> None:
    print(json.dumps({"state": state, "stage": stage, **extra}, indent=2))


def fail(stage: str, reason: str, code: int = 2) -> NoReturn:
    emit("BLOCKED", stage, reason=reason, mode="live", api_key_recorded=False, provider_side_effects=0, real_money_effect=False)
    raise SystemExit(code)


def api_key(non_interactive: bool) -> str:
    value = os.environ.get("LEMONSQUEEZY_API_KEY", "").strip()
    if value:
        return value
    if non_interactive:
        fail("API_KEY", "LEMONSQUEEZY_API_KEY is not loaded")
    value = getpass.getpass("Lemon Squeezy LIVE API key (hidden, not persisted): ").strip()
    if not value:
        fail("API_KEY", "no API key supplied")
    return value


def request(path: str, key: str) -> dict[str, Any]:
    req = urllib.request.Request(
        f"{API_BASE}{path}", method="GET",
        headers={
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {key}",
            "User-Agent": "Prompt-Machine-G14-Live-Preflight/1.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        fail("LEMON_API", f"HTTP {exc.code}: {detail}")
    except urllib.error.URLError as exc:
        fail("LEMON_API", f"unavailable: {exc.reason}")
    raise AssertionError("unreachable")


def attrs(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("attributes")
    if not isinstance(value, dict):
        fail("API_SHAPE", "object has no attributes")
    return value


def list_data(payload: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    raw = payload.get("data")
    if not isinstance(raw, list):
        fail("API_SHAPE", f"expected list for {kind}")
    return [x for x in raw if isinstance(x, dict) and x.get("type") == kind]


def one(items: list[dict[str, Any]], predicate, label: str) -> dict[str, Any]:
    matches = [x for x in items if predicate(x)]
    if len(matches) != 1:
        fail("DISCOVERY", f"expected exactly one {label}; observed {len(matches)}")
    return matches[0]


def download_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Prompt-Machine-G14-Live-Preflight/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        fail("LIVE_FILE_DOWNLOAD", f"HTTP {exc.code}: {detail}")
    except urllib.error.URLError as exc:
        fail("LIVE_FILE_DOWNLOAD", f"unavailable: {exc.reason}")
    raise AssertionError("unreachable")


def discover(key: str) -> tuple[dict[str, str], dict[str, Any]]:
    stores = list_data(request("/stores?page[size]=100", key), "stores")
    store = one(stores, lambda x: attrs(x).get("name") == STORE_NAME, "Live store")
    store_id = str(store.get("id"))

    q = urllib.parse.urlencode({"filter[store_id]": store_id, "page[size]": 100})
    products = list_data(request(f"/products?{q}", key), "products")
    product = one(products, lambda x: attrs(x).get("name") == PRODUCT_NAME, "Live Code Review Edition product")
    pa = attrs(product)
    product_id = str(product.get("id"))
    if pa.get("test_mode") is not False:
        fail("LIVE_PRODUCT", "discovered product is not explicitly test_mode=false; do not reuse Test data")
    if pa.get("status") != "published":
        fail("LIVE_PRODUCT", f"product must be published; observed {pa.get('status')}")

    q = urllib.parse.urlencode({"filter[product_id]": product_id, "page[size]": 100})
    variants = list_data(request(f"/variants?{q}", key), "variants")
    variant = one(
        variants,
        lambda x: attrs(x).get("test_mode") is False and attrs(x).get("is_subscription") is False and int(attrs(x).get("price", -1)) == PRICE_CENTS,
        "$9 one-time Live variant",
    )
    va = attrs(variant)
    variant_id = str(variant.get("id"))
    if str(va.get("product_id")) != product_id:
        fail("LIVE_VARIANT", "variant product relationship mismatch")

    q = urllib.parse.urlencode({"filter[variant_id]": variant_id, "page[size]": 100})
    files = list_data(request(f"/files?{q}", key), "files")
    file_item = one(files, lambda x: attrs(x).get("name") == ARCHIVE_NAME, "Live final 1.0.0 file")
    fa = attrs(file_item)
    file_id = str(file_item.get("id"))

    if fa.get("test_mode") is not False:
        fail("LIVE_FILE", "discovered file is not explicitly test_mode=false")
    if fa.get("status") != "published":
        fail("LIVE_FILE", f"file must be published; observed {fa.get('status')}")
    if int(fa.get("size", -1)) != ARCHIVE_BYTES:
        fail("LIVE_FILE", f"size mismatch: expected {ARCHIVE_BYTES}, observed {fa.get('size')}")
    observed_version = fa.get("version")
    if observed_version not in (None, "", VERSION):
        fail("LIVE_FILE", f"version mismatch: expected {VERSION} or null, observed {observed_version}")

    ids = {"store_id": store_id, "product_id": product_id, "variant_id": variant_id, "file_id": file_id}
    metadata = {
        "product_name": pa.get("name"), "product_status": pa.get("status"),
        "price_cents": va.get("price"), "is_subscription": va.get("is_subscription"),
        "archive_name": fa.get("name"), "archive_size": fa.get("size"),
        "archive_version": observed_version, "archive_status": fa.get("status"),
        "download_url": fa.get("download_url"),
    }
    return ids, metadata


def self_test() -> int:
    assert PRICE_CENTS == 900
    assert ARCHIVE_BYTES == 18955
    assert len(ARCHIVE_SHA256) == 64
    assert VERSION == "1.0.0"
    assert ARCHIVE_NAME.endswith("v1.0.0.zip")
    print("PM G14 LEMON LIVE PREFLIGHT SELF TEST: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Prompt Machine G14 Lemon Live preflight")
    parser.add_argument("--verify-bytes", action="store_true")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    ids, metadata = discover(api_key(args.non_interactive))
    byte_evidence: dict[str, Any] = {"observed": False, "reason": "not_requested"}
    stage = "LIVE_PROVIDER_METADATA"
    if args.verify_bytes:
        url = metadata.get("download_url")
        if not isinstance(url, str) or not url.startswith("https://"):
            fail("LIVE_FILE_DOWNLOAD", "provider file has no HTTPS signed download_url")
        body = download_bytes(url)
        digest = hashlib.sha256(body).hexdigest()
        if len(body) != ARCHIVE_BYTES:
            fail("LIVE_PROVIDER_CUSTODY", f"downloaded size mismatch: {len(body)}")
        if digest != ARCHIVE_SHA256:
            fail("LIVE_PROVIDER_CUSTODY", f"downloaded SHA-256 mismatch: {digest}")
        byte_evidence = {"observed": True, "bytes": len(body), "sha256": digest}
        stage = "LIVE_PROVIDER_CUSTODY"

    public_metadata = {k: v for k, v in metadata.items() if k != "download_url"}
    emit(
        "PASS", stage, mode="live", canonical_live_ids=ids, metadata=public_metadata,
        provider_file_bytes=byte_evidence, api_key_recorded=False,
        signed_download_url_recorded=False, customer_pii_recorded=False,
        provider_side_effects=0, real_money_effect=False, public_sale_enabled=False,
        claim_boundary=(
            "Live provider byte verification proves provider-held final 1.0.0 custody only. "
            "It does not prove buyer delivery, customer value, real revenue, readiness to sell, or public-sale authorization."
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
