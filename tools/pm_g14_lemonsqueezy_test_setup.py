#!/usr/bin/env python3
"""Prompt Machine G14 Lemon Squeezy test-mode setup operator.

Default mode is read-only. With --apply-webhook it creates exactly one test-mode
order_created webhook, generates isolated secrets, and writes a chmod-0600 Vercel
environment handoff. The Lemon API key is never persisted or printed.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import pathlib
import secrets
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API_BASE = "https://api.lemonsqueezy.com/v1"
STORE_NAME = "Prompt Quarry"
PRODUCT_NAME = "Prompt Machine Starter — Code Review Edition"
PRICE_CENTS = 900
ARCHIVE_NAME = "prompt-machine-starter-code-review-edition-v1.0.0.zip"
ARCHIVE_BYTES = 18955
WEBHOOK_URL = "https://prompt-quarry-stage.vercel.app/api/commerce/lemonsqueezy/starter-code-review-webhook"
EVENTS = ["order_created"]


def fail(stage: str, reason: str, code: int = 2) -> None:
    print(json.dumps({"state": "BLOCKED", "stage": stage, "reason": reason}, indent=2))
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


def request(method: str, path: str, key: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{path}", method=method, data=body,
        headers={
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {key}",
            "User-Agent": "Prompt-Machine-G14-Test-Setup/1.1",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        fail("LEMON_API", f"HTTP {exc.code}: {detail}")
    except urllib.error.URLError as exc:
        fail("LEMON_API", f"unavailable: {exc.reason}")
    raise AssertionError("unreachable")


def attrs(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("attributes")
    return value if isinstance(value, dict) else {}


def data_list(payload: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    data = payload.get("data")
    if not isinstance(data, list):
        fail("API_SHAPE", f"expected list for {kind}")
    return [x for x in data if isinstance(x, dict) and x.get("type") == kind]


def one(items: list[dict[str, Any]], predicate, label: str) -> dict[str, Any]:
    matches = [item for item in items if predicate(item)]
    if len(matches) != 1:
        fail("DISCOVERY", f"expected exactly one {label}; observed {len(matches)}")
    return matches[0]


def validate_snapshot(store: dict[str, Any], product: dict[str, Any], variant: dict[str, Any], file_item: dict[str, Any]) -> dict[str, str]:
    sa, pa, va, fa = attrs(store), attrs(product), attrs(variant), attrs(file_item)
    checks = {
        "store_name": sa.get("name") == STORE_NAME,
        "product_name": pa.get("name") == PRODUCT_NAME,
        "product_published": pa.get("status") == "published",
        "product_test_mode": pa.get("test_mode") is True,
        "variant_test_mode": va.get("test_mode") is True,
        "variant_one_time": va.get("is_subscription") is False,
        "variant_price": int(va.get("price", -1)) == PRICE_CENTS,
        "file_name": fa.get("name") == ARCHIVE_NAME,
        "file_size": int(fa.get("size", -1)) == ARCHIVE_BYTES,
        "file_published": fa.get("status") == "published",
        "file_test_mode": fa.get("test_mode") is True,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        fail("PROVIDER_METADATA", "failed: " + ", ".join(failed))
    buy_now = pa.get("buy_now_url")
    if not isinstance(buy_now, str) or not buy_now.startswith("https://") or "/checkout/buy/" not in buy_now:
        fail("CHECKOUT_URL", "published product has no reusable HTTPS buy_now_url")
    return {
        "store_id": str(store.get("id")),
        "product_id": str(product.get("id")),
        "variant_id": str(variant.get("id")),
        "file_id": str(file_item.get("id")),
        "checkout_url": buy_now,
    }


def discover(key: str) -> dict[str, str]:
    stores = data_list(request("GET", "/stores?page[size]=100", key), "stores")
    store = one(stores, lambda x: attrs(x).get("name") == STORE_NAME, "Prompt Quarry store")
    sid = str(store.get("id"))
    q = urllib.parse.urlencode({"filter[store_id]": sid, "page[size]": 100})
    products = data_list(request("GET", f"/products?{q}", key), "products")
    product = one(products, lambda x: attrs(x).get("name") == PRODUCT_NAME, "Code Review Edition product")
    pid = str(product.get("id"))
    q = urllib.parse.urlencode({"filter[product_id]": pid, "page[size]": 100})
    variants = data_list(request("GET", f"/variants?{q}", key), "variants")
    variant = one(variants, lambda x: attrs(x).get("test_mode") is True and attrs(x).get("is_subscription") is False and int(attrs(x).get("price", -1)) == PRICE_CENTS, "$9 test variant")
    vid = str(variant.get("id"))
    q = urllib.parse.urlencode({"filter[variant_id]": vid, "page[size]": 100})
    files = data_list(request("GET", f"/files?{q}", key), "files")
    file_item = one(files, lambda x: attrs(x).get("name") == ARCHIVE_NAME, "final 1.0.0 file")
    return validate_snapshot(store, product, variant, file_item)


def create_webhook(key: str, store_id: str, secret: str) -> str:
    q = urllib.parse.urlencode({"filter[store_id]": store_id, "page[size]": 100})
    hooks = data_list(request("GET", f"/webhooks?{q}", key), "webhooks")
    existing = [h for h in hooks if attrs(h).get("url") == WEBHOOK_URL and attrs(h).get("test_mode") is True]
    if existing:
        fail("WEBHOOK_EXISTS", "test webhook already exists at target URL; its signing secret cannot be recovered via API")
    payload = {
        "data": {
            "type": "webhooks",
            "attributes": {"url": WEBHOOK_URL, "events": EVENTS, "secret": secret, "test_mode": True},
            "relationships": {"store": {"data": {"type": "stores", "id": store_id}}},
        }
    }
    created = request("POST", "/webhooks", key, payload).get("data")
    if not isinstance(created, dict) or created.get("type") != "webhooks":
        fail("WEBHOOK_CREATE", "unexpected create response")
    return str(created.get("id"))


def write_handoff(ids: dict[str, str], webhook_secret: str, provider_token: str, webhook_id: str) -> pathlib.Path:
    root = pathlib.Path(os.environ.get("XDG_DATA_HOME", pathlib.Path.home() / ".local/share")) / "prompt-machine/g14"
    root.mkdir(parents=True, exist_ok=True)
    path = root / "starter-code-review-test-vercel.env"
    values = {
        "STARTER_CODE_REVIEW_COMMERCE_MODE": "test",
        "NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS": "NOT_FOR_SALE",
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_TEST_CHECKOUT_URL": ids["checkout_url"],
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_PROVIDER_TEST_TOKEN": provider_token,
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_WEBHOOK_SECRET": webhook_secret,
        "LEMONSQUEEZY_STORE_ID": ids["store_id"],
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID": ids["product_id"],
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID": ids["variant_id"],
    }
    path.write_text("".join(f"{k}={v}\n" for k, v in values.items()), encoding="utf-8")
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    receipt = root / "starter-code-review-test-provider.json"
    receipt.write_text(json.dumps({
        "schema": "prompt-machine-g14-test-provider-v1",
        "state": "ACTION_REQUIRED",
        "stage": "VERCEL_ENV_IMPORT",
        "mode": "test",
        "webhook_id": webhook_id,
        "webhook_url": WEBHOOK_URL,
        "events": EVENTS,
        "provider_ids": {k: ids[k] for k in ("store_id", "product_id", "variant_id", "file_id")},
        "checkout_url_present": True,
        "api_key_recorded": False,
        "secrets_recorded_in_receipt": False,
        "real_money_effect": False,
    }, indent=2) + "\n", encoding="utf-8")
    return path


def self_test() -> int:
    store = {"id": "1", "attributes": {"name": STORE_NAME}}
    product = {"id": "2", "attributes": {"name": PRODUCT_NAME, "status": "published", "test_mode": True, "buy_now_url": "https://prompt-quarry.lemonsqueezy.com/checkout/buy/test"}}
    variant = {"id": "3", "attributes": {"test_mode": True, "is_subscription": False, "price": PRICE_CENTS}}
    file_item = {"id": "4", "attributes": {"name": ARCHIVE_NAME, "size": ARCHIVE_BYTES, "status": "published", "test_mode": True}}
    got = validate_snapshot(store, product, variant, file_item)
    assert got["store_id"] == "1" and got["checkout_url"].startswith("https://")
    print("PM G14 TEST SETUP SELF TEST: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Prompt Machine Lemon Squeezy G14 test integration")
    parser.add_argument("--apply-webhook", action="store_true", help="create one test-mode order_created webhook")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    key = api_key(args.non_interactive)
    ids = discover(key)
    if not args.apply_webhook:
        print(json.dumps({
            "state": "PASS", "stage": "TEST_PROVIDER_DISCOVERY", "mode": "test",
            "provider_ids": {k: ids[k] for k in ("store_id", "product_id", "variant_id", "file_id")},
            "checkout_url_present": True, "provider_side_effects": 0, "api_key_recorded": False,
            "byte_custody": "NOT_OBSERVABLE_IN_TEST_MODE",
            "next": "existing webhook can be reused if its secret remains configured; otherwise create a fresh bounded test webhook",
        }, indent=2))
        return 0
    webhook_secret = secrets.token_urlsafe(24)[:40]
    provider_token = secrets.token_urlsafe(32)
    webhook_id = create_webhook(key, ids["store_id"], webhook_secret)
    handoff = write_handoff(ids, webhook_secret, provider_token, webhook_id)
    print(json.dumps({
        "state": "ACTION_REQUIRED", "stage": "VERCEL_ENV_IMPORT", "mode": "test",
        "webhook_created": True, "webhook_id": webhook_id, "webhook_url": WEBHOOK_URL,
        "env_file": str(handoff), "api_key_recorded": False, "real_money_effect": False,
        "next": "import the generated env file into prompt-quarry-stage Production and redeploy",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
