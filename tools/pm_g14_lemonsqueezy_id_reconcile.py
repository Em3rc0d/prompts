#!/usr/bin/env python3
"""Reconcile Prompt Machine G14 Lemon Squeezy Test provider identity.

Read-only operator. It compares the provider-signed accepted Test order with the
current Product and Variant objects returned by the Lemon API, and inspects the
earlier dashboard URL product id without printing customer PII or the API key.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, NoReturn

API_BASE = "https://api.lemonsqueezy.com/v1"
STORE_ID = 462419
PRODUCT_NAME = "Prompt Machine Starter — Code Review Edition"
SIGNED_ORDER_ID = "9415856"
SIGNED_ORDER_NUMBER = 4624191
SIGNED_PRODUCT_ID = "1347720"
SIGNED_VARIANT_ID = "2105176"
EARLIER_DASHBOARD_PRODUCT_ID = "1347702"
PRICE_CENTS = 900
ARCHIVE_NAME = "prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip"
ARCHIVE_BYTES = 19161


def emit(state: str, stage: str, **extra: object) -> None:
    print(json.dumps({"state": state, "stage": stage, **extra}, indent=2))


def fail(stage: str, reason: str, code: int = 2) -> NoReturn:
    emit("BLOCKED", stage, reason=reason, api_key_recorded=False, provider_side_effects=0)
    raise SystemExit(code)


def api_key(non_interactive: bool) -> str:
    value = os.environ.get("LEMONSQUEEZY_API_KEY", "").strip()
    if value:
        return value
    if non_interactive:
        fail("API_KEY", "LEMONSQUEEZY_API_KEY is not loaded")
    value = getpass.getpass("Lemon Squeezy API key (hidden, not persisted): ").strip()
    if not value:
        fail("API_KEY", "no API key supplied")
    return value


def request(path: str, key: str, *, allow_404: bool = False) -> dict[str, Any] | None:
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        method="GET",
        headers={
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {key}",
            "User-Agent": "Prompt-Machine-G14-ID-Reconcile/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if allow_404 and exc.code == 404:
            return None
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        fail("LEMON_API", f"HTTP {exc.code}: {detail}")
    except urllib.error.URLError as exc:
        fail("LEMON_API", f"unavailable: {exc.reason}")
    raise AssertionError("unreachable")


def data(payload: dict[str, Any] | None, expected_type: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        fail("API_SHAPE", f"missing {expected_type} payload")
    item = payload.get("data")
    if not isinstance(item, dict) or item.get("type") != expected_type:
        fail("API_SHAPE", f"expected {expected_type} object")
    return item


def attrs(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("attributes")
    if not isinstance(value, dict):
        fail("API_SHAPE", "object has no attributes")
    return value


def list_data(payload: dict[str, Any] | None, expected_type: str) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        fail("API_SHAPE", f"missing {expected_type} list")
    raw = payload.get("data")
    if not isinstance(raw, list):
        fail("API_SHAPE", f"expected {expected_type} list")
    return [x for x in raw if isinstance(x, dict) and x.get("type") == expected_type]


def inspect_old_product(key: str) -> dict[str, Any]:
    payload = request(f"/products/{EARLIER_DASHBOARD_PRODUCT_ID}", key, allow_404=True)
    if payload is None:
        return {"id": EARLIER_DASHBOARD_PRODUCT_ID, "api_state": "NOT_FOUND"}
    item = data(payload, "products")
    a = attrs(item)
    return {
        "id": str(item.get("id")),
        "api_state": "FOUND",
        "name_matches": a.get("name") == PRODUCT_NAME,
        "status": a.get("status"),
        "test_mode": a.get("test_mode"),
        "store_id": a.get("store_id"),
    }


def reconcile(key: str) -> dict[str, Any]:
    order = data(request(f"/orders/{SIGNED_ORDER_ID}", key), "orders")
    oa = attrs(order)
    item = oa.get("first_order_item")
    if not isinstance(item, dict):
        fail("ORDER", "order has no first_order_item")

    product = data(request(f"/products/{SIGNED_PRODUCT_ID}", key), "products")
    pa = attrs(product)
    variant = data(request(f"/variants/{SIGNED_VARIANT_ID}", key), "variants")
    va = attrs(variant)

    q = urllib.parse.urlencode({"filter[store_id]": str(STORE_ID), "page[size]": 100})
    products = list_data(request(f"/products?{q}", key), "products")
    same_name = [
        {
            "id": str(p.get("id")),
            "status": attrs(p).get("status"),
            "test_mode": attrs(p).get("test_mode"),
        }
        for p in products
        if attrs(p).get("name") == PRODUCT_NAME
    ]

    checks = {
        "order_id": str(order.get("id")) == SIGNED_ORDER_ID,
        "order_number": int(oa.get("order_number", -1)) == SIGNED_ORDER_NUMBER,
        "order_store": int(oa.get("store_id", -1)) == STORE_ID,
        "order_paid": oa.get("status") == "paid",
        "order_test_mode": oa.get("test_mode") is True,
        "order_total": int(oa.get("total", -1)) == PRICE_CENTS,
        "order_item_product": str(item.get("product_id")) == SIGNED_PRODUCT_ID,
        "order_item_variant": str(item.get("variant_id")) == SIGNED_VARIANT_ID,
        "order_item_name": item.get("product_name") == PRODUCT_NAME,
        "order_item_test_mode": item.get("test_mode") is True,
        "product_id": str(product.get("id")) == SIGNED_PRODUCT_ID,
        "product_store": int(pa.get("store_id", -1)) == STORE_ID,
        "product_name": pa.get("name") == PRODUCT_NAME,
        "product_published": pa.get("status") == "published",
        "product_test_mode": pa.get("test_mode") is True,
        "variant_id": str(variant.get("id")) == SIGNED_VARIANT_ID,
        "variant_product": str(va.get("product_id")) == SIGNED_PRODUCT_ID,
        "variant_price": int(va.get("price", -1)) == PRICE_CENTS,
        "variant_one_time": va.get("is_subscription") is False,
        "variant_test_mode": va.get("test_mode") is True,
        "one_canonical_same_name_product": len(same_name) == 1 and same_name[0]["id"] == SIGNED_PRODUCT_ID,
    }
    failed = [name for name, ok in checks.items() if not ok]
    old = inspect_old_product(key)
    return {
        "checks": checks,
        "failed": failed,
        "canonical": {
            "store_id": STORE_ID,
            "product_id": SIGNED_PRODUCT_ID,
            "variant_id": SIGNED_VARIANT_ID,
            "product_name": PRODUCT_NAME,
            "order_id": SIGNED_ORDER_ID,
            "order_number": SIGNED_ORDER_NUMBER,
            "price_cents": PRICE_CENTS,
            "archive_name": ARCHIVE_NAME,
            "archive_bytes": ARCHIVE_BYTES,
        },
        "same_name_products": same_name,
        "earlier_dashboard_observation": old,
    }


def self_test() -> int:
    assert SIGNED_PRODUCT_ID != EARLIER_DASHBOARD_PRODUCT_ID
    assert PRICE_CENTS == 900
    assert ARCHIVE_BYTES == 19161
    assert PRODUCT_NAME.startswith("Prompt Machine Starter")
    print("PM G14 LEMON ID RECONCILE SELF TEST: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconcile Lemon Test provider IDs for Prompt Machine G14")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    result = reconcile(api_key(args.non_interactive))
    if result["failed"]:
        emit(
            "BLOCKED",
            "PROVIDER_ID_RECONCILIATION",
            mode="test",
            reason="one or more provider identity checks failed",
            failed=result["failed"],
            canonical=result["canonical"],
            same_name_products=result["same_name_products"],
            earlier_dashboard_observation=result["earlier_dashboard_observation"],
            api_key_recorded=False,
            customer_pii_recorded=False,
            provider_side_effects=0,
        )
        return 2

    emit(
        "PASS",
        "PROVIDER_ID_RECONCILIATION",
        mode="test",
        canonical=result["canonical"],
        same_name_products=result["same_name_products"],
        earlier_dashboard_observation=result["earlier_dashboard_observation"],
        resolution="API product + variant + paid Test order agree on the signed provider identity",
        api_key_recorded=False,
        customer_pii_recorded=False,
        provider_side_effects=0,
        next="freeze canonical Test IDs; do not reuse them for Live because Lemon Test and Live data are separate",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
