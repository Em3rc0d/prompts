#!/usr/bin/env python3
"""Read-only Lemon Squeezy discovery probe for the new Verlune Premium SKU.

The probe never persists or prints the API key and performs GET requests only.
Use a Test-mode Lemon Squeezy API key for staging discovery.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, NoReturn

API_BASE = "https://api.lemonsqueezy.com/v1"
DEFAULT_STORE_ID = "462419"
TARGET_PRODUCT_NAME = "Verlune Premium"
TARGET_PRICE_CENTS = 900
TARGET_ACTIVATION_LIMIT = 3


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
            "User-Agent": "Verlune-Premium-Provider-Probe/1.0",
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


def attrs(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("attributes")
    return value if isinstance(value, dict) else {}


def list_items(payload: dict[str, Any], expected_type: str) -> list[dict[str, Any]]:
    data = payload.get("data")
    if not isinstance(data, list):
        fail(f"BLOCKED: unexpected {expected_type} response")
    return [item for item in data if isinstance(item, dict) and item.get("type") == expected_type]


def get_list(path: str, key: str, filters: dict[str, str]) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode({**filters, "page[size]": "100"})
    return list_items(api_get(f"{path}?{query}", key), path.rsplit("/", 1)[-1])


def compact_variant(item: dict[str, Any]) -> dict[str, Any]:
    a = attrs(item)
    return {
        "variant_id": str(item.get("id")),
        "name": a.get("name"),
        "status": a.get("status"),
        "test_mode": a.get("test_mode"),
        "price_cents": a.get("price"),
        "is_subscription": a.get("is_subscription"),
        "has_license_keys": a.get("has_license_keys"),
        "license_activation_limit": a.get("license_activation_limit"),
        "is_license_limit_unlimited": a.get("is_license_limit_unlimited"),
        "license_length_value": a.get("license_length_value"),
        "license_length_unit": a.get("license_length_unit"),
        "is_license_length_unlimited": a.get("is_license_length_unlimited"),
    }


def evaluate_variant(v: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if v.get("is_subscription") is not False:
        problems.append("must_be_one_time_not_subscription")
    if v.get("price_cents") != TARGET_PRICE_CENTS:
        problems.append(f"price_must_be_{TARGET_PRICE_CENTS}_cents")
    if v.get("has_license_keys") is not True:
        problems.append("license_keys_must_be_enabled")
    if v.get("is_license_limit_unlimited") is not False:
        problems.append("activation_limit_must_not_be_unlimited")
    if v.get("license_activation_limit") != TARGET_ACTIVATION_LIMIT:
        problems.append(f"activation_limit_must_be_{TARGET_ACTIVATION_LIMIT}")
    if v.get("is_license_length_unlimited") is not True:
        problems.append("license_length_must_be_unlimited_for_one_time_v1")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Lemon Squeezy probe for Verlune Premium")
    parser.add_argument("--store-id", default=DEFAULT_STORE_ID)
    parser.add_argument("--product-name", default=TARGET_PRODUCT_NAME)
    parser.add_argument("--non-interactive", action="store_true")
    args = parser.parse_args()

    key = api_key(interactive=not args.non_interactive)
    products = get_list("/products", key, {"filter[store_id]": args.store_id})

    candidates = [
        item for item in products
        if str(attrs(item).get("name", "")).strip().casefold() == args.product_name.strip().casefold()
    ]

    product_summaries = [
        {
            "product_id": str(item.get("id")),
            "name": attrs(item).get("name"),
            "status": attrs(item).get("status"),
            "test_mode": attrs(item).get("test_mode"),
            "price": attrs(item).get("price"),
        }
        for item in products
        if "verlune" in str(attrs(item).get("name", "")).casefold()
    ]

    result: dict[str, Any] = {
        "schema": "verlune-premium-provider-probe-v1",
        "store_id": args.store_id,
        "target_product_name": args.product_name,
        "target_price_cents": TARGET_PRICE_CENTS,
        "target_activation_limit": TARGET_ACTIVATION_LIMIT,
        "api_key_recorded": False,
        "provider_side_effects": 0,
        "verlune_products_observed": product_summaries,
    }

    if not candidates:
        result.update({
            "state": "ACTION_REQUIRED",
            "stage": "CREATE_OR_RENAME_PREMIUM_PRODUCT",
            "reason": f"No exact product named {args.product_name!r} was observed in this API-key mode/store.",
            "required_dashboard_settings": {
                "product_name": args.product_name,
                "price": "USD 9 one-time",
                "license_keys": True,
                "activation_limit": TARGET_ACTIVATION_LIMIT,
                "license_length": "unlimited",
            },
        })
    elif len(candidates) > 1:
        result.update({
            "state": "BLOCKED",
            "stage": "PRODUCT_AMBIGUITY",
            "reason": f"Observed {len(candidates)} exact products named {args.product_name!r}.",
        })
    else:
        product = candidates[0]
        product_id = str(product.get("id"))
        variants = get_list("/variants", key, {"filter[product_id]": product_id})
        compact = [compact_variant(v) for v in variants]
        evaluated = [{**v, "problems": evaluate_variant(v)} for v in compact]
        passing = [v for v in evaluated if not v["problems"]]

        result.update({
            "product_id": product_id,
            "product_status": attrs(product).get("status"),
            "product_test_mode": attrs(product).get("test_mode"),
            "variants": evaluated,
        })

        if len(passing) == 1:
            chosen = passing[0]
            result.update({
                "state": "PASS",
                "stage": "PREMIUM_PROVIDER_IDENTITY_READY_TO_FREEZE",
                "variant_id": chosen["variant_id"],
                "env_candidate": {
                    "VERLUNE_PREMIUM_STORE_ID": args.store_id,
                    "VERLUNE_PREMIUM_PRODUCT_ID": product_id,
                    "VERLUNE_PREMIUM_VARIANT_ID": chosen["variant_id"],
                    "VERLUNE_PREMIUM_ACTIVATION_LIMIT": TARGET_ACTIVATION_LIMIT,
                },
            })
        elif len(passing) == 0:
            result.update({
                "state": "ACTION_REQUIRED",
                "stage": "CONFIGURE_PREMIUM_VARIANT",
                "reason": "No variant matches the frozen one-time/license policy.",
            })
        else:
            result.update({
                "state": "BLOCKED",
                "stage": "VARIANT_AMBIGUITY",
                "reason": f"Observed {len(passing)} variants matching the full Premium policy.",
            })

    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return 0 if result.get("state") in {"PASS", "ACTION_REQUIRED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
