#!/usr/bin/env python3
"""Apply the Prompt Machine G14 Test-mode Vercel handoff in one operator action.

Reads the local chmod-0600 handoff created by pm_g14_lemonsqueezy_test_setup.py,
upserts the exact Production environment variables for prompt-quarry-stage through
the Vercel CLI using stdin, redeploys the current production deployment, then
verifies the private provider-test checkout gate and emits the final Lemon Test
checkout URL. Secret values are never printed or embedded in command arguments.

This operator does not activate Lemon Live mode, does not make a purchase, and
does not change the public sale status to LIVE.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.request
from typing import NoReturn

PROJECT_ID = "prj_Srr2nUKq8fZWff6x9XMyrY3dkjJ7"
ORG_ID = "team_FTC62CRbJz9veMUDYeVzf7yI"
TEAM_SLUG = "faridmerinos-projects"
PROJECT_NAME = "prompt-quarry-stage"
STABLE_ORIGIN = "https://prompt-quarry-stage.vercel.app"
CHECKOUT_PATH = "/api/commerce/starter-code-review/checkout"
WEBHOOK_PATH = "/api/commerce/lemonsqueezy/starter-code-review-webhook"
DEFAULT_HANDOFF = pathlib.Path.home() / ".local/share/prompt-machine/g14/starter-code-review-test-vercel.env"
REQUIRED_KEYS = (
    "STARTER_CODE_REVIEW_COMMERCE_MODE",
    "NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS",
    "LEMONSQUEEZY_STARTER_CODE_REVIEW_TEST_CHECKOUT_URL",
    "LEMONSQUEEZY_STARTER_CODE_REVIEW_PROVIDER_TEST_TOKEN",
    "LEMONSQUEEZY_STARTER_CODE_REVIEW_WEBHOOK_SECRET",
    "LEMONSQUEEZY_STORE_ID",
    "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID",
    "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID",
)
SECRET_KEYS = {
    "LEMONSQUEEZY_STARTER_CODE_REVIEW_PROVIDER_TEST_TOKEN",
    "LEMONSQUEEZY_STARTER_CODE_REVIEW_WEBHOOK_SECRET",
}


def emit(state: str, stage: str, **extra: object) -> None:
    print(json.dumps({"state": state, "stage": stage, **extra}, indent=2))


def fail(stage: str, reason: str, code: int = 2) -> NoReturn:
    emit("BLOCKED", stage, reason=reason, real_money_effect=False)
    raise SystemExit(code)


def parse_env(path: pathlib.Path) -> dict[str, str]:
    if not path.is_file():
        fail("HANDOFF_FILE", f"missing handoff file: {path}")
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        fail("HANDOFF_PERMISSIONS", f"handoff must be owner-only (0600); observed {oct(mode)}")
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            fail("HANDOFF_PARSE", "invalid env line")
        key, value = line.split("=", 1)
        values[key.strip()] = value
    missing = [k for k in REQUIRED_KEYS if not values.get(k)]
    if missing:
        fail("HANDOFF_KEYS", "missing required keys: " + ", ".join(missing))
    if values["STARTER_CODE_REVIEW_COMMERCE_MODE"] != "test":
        fail("HANDOFF_MODE", "commerce mode must remain test")
    if values["NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS"] != "NOT_FOR_SALE":
        fail("HANDOFF_PUBLIC_SALE", "public sale must remain NOT_FOR_SALE")
    return values


def cli_prefix() -> list[str]:
    direct = shutil.which("vercel")
    if direct:
        return [direct]
    npx = shutil.which("npx")
    if npx:
        return [npx, "--yes", "vercel@latest"]
    fail("VERCEL_CLI", "neither vercel nor npx is available")


def cli_env() -> dict[str, str]:
    env = os.environ.copy()
    env["VERCEL_ORG_ID"] = ORG_ID
    env["VERCEL_PROJECT_ID"] = PROJECT_ID
    return env


def run_cli(prefix: list[str], args: list[str], *, stdin: str | None = None, quiet: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*prefix, *args, f"--scope={TEAM_SLUG}"],
        input=stdin,
        text=True,
        stdout=subprocess.PIPE if quiet else None,
        stderr=subprocess.PIPE if quiet else None,
        env=cli_env(),
        check=False,
    )


def ensure_auth(prefix: list[str]) -> None:
    probe = run_cli(prefix, ["whoami"], quiet=True)
    if probe.returncode == 0:
        return
    login = run_cli(prefix, ["login"])
    if login.returncode != 0:
        fail("VERCEL_AUTH", "Vercel CLI authentication did not complete")
    probe = run_cli(prefix, ["whoami"], quiet=True)
    if probe.returncode != 0:
        fail("VERCEL_AUTH", "Vercel CLI is still unauthenticated")


def upsert_env(prefix: list[str], key: str, value: str) -> None:
    # Values are sent over stdin so they never appear in argv/process listings.
    update_args = ["env", "update", key, "production"]
    if key in SECRET_KEYS:
        update_args.append("--sensitive")
    updated = run_cli(prefix, update_args, stdin=value + "\n", quiet=True)
    if updated.returncode == 0:
        return
    add_args = ["env", "add", key, "production"]
    if key in SECRET_KEYS:
        add_args.append("--sensitive")
    added = run_cli(prefix, add_args, stdin=value + "\n", quiet=True)
    if added.returncode != 0:
        detail = (added.stderr or updated.stderr or "env upsert failed")[-500:]
        fail("VERCEL_ENV_UPSERT", f"could not set {key}: {detail}")


def redeploy(prefix: list[str]) -> None:
    result = run_cli(prefix, ["redeploy", "prompt-quarry-stage.vercel.app", "--target=production", "--yes"], quiet=True)
    if result.returncode == 0:
        return
    # Some CLI versions do not accept --target for redeploy. Retry without it;
    # the source deployment is already the production deployment behind the alias.
    fallback = run_cli(prefix, ["redeploy", "prompt-quarry-stage.vercel.app", "--yes"], quiet=True)
    if fallback.returncode != 0:
        detail = (fallback.stderr or result.stderr or "redeploy failed")[-500:]
        fail("VERCEL_REDEPLOY", detail)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        return None


def http_status(url: str, headers: dict[str, str] | None = None) -> tuple[int, dict[str, str], bytes]:
    request = urllib.request.Request(url, headers=headers or {}, method="GET")
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=20) as response:
            return response.status, dict(response.headers.items()), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers.items()), exc.read()
    except urllib.error.URLError as exc:
        fail("VERCEL_HTTP", f"endpoint unavailable: {exc.reason}")


def wait_for_checkout(provider_token: str, attempts: int = 18) -> str:
    headers = {"x-pm-starter-code-review-provider-test-token": provider_token, "User-Agent": "Prompt-Machine-G14-Vercel-Apply/1.0"}
    last_status = 0
    last_body = ""
    for _ in range(attempts):
        status, response_headers, body = http_status(STABLE_ORIGIN + CHECKOUT_PATH, headers)
        last_status = status
        last_body = body.decode("utf-8", errors="replace")[:300]
        if status in {301, 302, 303, 307, 308}:
            location = response_headers.get("Location") or response_headers.get("location")
            if isinstance(location, str) and location.startswith("https://") and "lemonsqueezy.com" in location:
                return location
        if status == 403 and "provider_test_not_authorized" in last_body:
            fail("CHECKOUT_GATE", "deployed provider token does not match handoff token")
        time.sleep(5)
    fail("CHECKOUT_READINESS", f"checkout did not become ready; last status={last_status} body={last_body}")


def verify_webhook_route() -> None:
    status, _, _ = http_status(STABLE_ORIGIN + WEBHOOK_PATH)
    if status != 405:
        fail("WEBHOOK_ROUTE", f"expected POST-only route (GET 405); observed {status}")


def self_test() -> int:
    sample = {
        "STARTER_CODE_REVIEW_COMMERCE_MODE": "test",
        "NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS": "NOT_FOR_SALE",
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_TEST_CHECKOUT_URL": "https://prompt-quarry.lemonsqueezy.com/checkout/buy/test",
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_PROVIDER_TEST_TOKEN": "token",
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_WEBHOOK_SECRET": "secret",
        "LEMONSQUEEZY_STORE_ID": "1",
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_PRODUCT_ID": "2",
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_VARIANT_ID": "3",
    }
    assert tuple(sample) == REQUIRED_KEYS
    assert SECRET_KEYS <= set(REQUIRED_KEYS)
    assert STABLE_ORIGIN.startswith("https://")
    print("PM G14 VERCEL TEST APPLY SELF TEST: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply Prompt Machine G14 Test-mode Vercel handoff")
    parser.add_argument("--handoff", type=pathlib.Path, default=DEFAULT_HANDOFF)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    values = parse_env(args.handoff.expanduser())
    prefix = cli_prefix()
    ensure_auth(prefix)

    for key in REQUIRED_KEYS:
        upsert_env(prefix, key, values[key])

    redeploy(prefix)
    verify_webhook_route()
    checkout_url = wait_for_checkout(values["LEMONSQUEEZY_STARTER_CODE_REVIEW_PROVIDER_TEST_TOKEN"])

    emit(
        "ACTION_REQUIRED",
        "TEST_CHECKOUT_READY",
        mode="test",
        project=PROJECT_NAME,
        webhook_route_ready=True,
        checkout_url=checkout_url,
        api_key_recorded=False,
        secrets_printed=False,
        public_sale="NOT_FOR_SALE",
        real_money_effect=False,
        next="open checkout_url and complete one Lemon Squeezy Test-mode order; do not use a real payment card",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
