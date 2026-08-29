#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile

EXPECTED_FREE_SHA256 = "55121028168f9a5394fe79ccc3102caa60e5df85c59a03639dc6e5392e5b2ee1"
EXPECTED_FREE_SIZE = 11573
EXPECTED_FREE_ENTRIES = [
    "prompt-quarry-developer-starter-v1/LICENSE.md",
    "prompt-quarry-developer-starter-v1/OFFER.md",
    "prompt-quarry-developer-starter-v1/QUICKSTART.md",
    "prompt-quarry-developer-starter-v1/README.md",
    "prompt-quarry-developer-starter-v1/prompts/bug-diagnosis.md",
    "prompt-quarry-developer-starter-v1/prompts/code-review.md",
    "prompt-quarry-developer-starter-v1/prompts/technical-decision.md",
]

ATTRIBUTION = {
    "source": "smoke",
    "medium": "test",
    "campaign": "pq-launch-0",
    "content": "commercial-e2e-smoke",
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        return None


def fail(message: str) -> None:
    raise SystemExit(f"COMMERCIAL LAUNCH SMOKE: FAIL — {message}")


def url(base: str, path: str, query: dict[str, str] | None = None) -> str:
    target = urllib.parse.urljoin(base.rstrip("/") + "/", path.lstrip("/"))
    if query:
        target += "?" + urllib.parse.urlencode(query)
    return target


def request_bytes(target: str, *, timeout: float) -> tuple[int, dict[str, str], bytes]:
    req = urllib.request.Request(target, headers={"User-Agent": "PromptQuarryLaunchSmoke/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status, {k.lower(): v for k, v in response.headers.items()}, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, exc.read()


def request_no_redirect(target: str, *, timeout: float) -> tuple[int, dict[str, str], bytes]:
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(target, headers={"User-Agent": "PromptQuarryLaunchSmoke/1.0"})
    try:
        with opener.open(req, timeout=timeout) as response:
            return response.status, {k.lower(): v for k, v in response.headers.items()}, response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, exc.read()


def assert_page(base: str, path: str, required: tuple[str, ...], timeout: float) -> None:
    status, headers, body = request_bytes(url(base, path), timeout=timeout)
    if status != 200:
        fail(f"{path} returned HTTP {status}")
    content_type = headers.get("content-type", "")
    if "text/html" not in content_type:
        fail(f"{path} is not HTML: {content_type}")
    text = body.decode("utf-8", errors="replace").lower()
    for phrase in required:
        if phrase.lower() not in text:
            fail(f"{path} missing expected copy: {phrase}")
    print(f"PASS page {path}")


def verify_free_pack(base: str, timeout: float) -> None:
    status, headers, body = request_bytes(url(base, "/api/free-pack/v1", ATTRIBUTION), timeout=timeout)
    if status != 200:
        fail(f"Free Pack route returned HTTP {status}")
    if headers.get("content-type", "").split(";")[0] != "application/zip":
        fail("Free Pack response is not application/zip")
    if len(body) != EXPECTED_FREE_SIZE:
        fail(f"Free Pack size mismatch: {len(body)} != {EXPECTED_FREE_SIZE}")

    observed = hashlib.sha256(body).hexdigest()
    if observed != EXPECTED_FREE_SHA256:
        fail(f"Free Pack sha256 mismatch: {observed}")
    if headers.get("x-prompt-quarry-sha256") != EXPECTED_FREE_SHA256:
        fail("Free Pack integrity response header does not match canonical sha256")

    with zipfile.ZipFile(io.BytesIO(body), "r") as archive:
        names = archive.namelist()
        if names != EXPECTED_FREE_ENTRIES:
            fail(f"Free Pack entries mismatch: {names}")
        bad = archive.testzip()
        if bad:
            fail(f"Free Pack CRC failure: {bad}")

    print(f"PASS Free Pack sha256={observed}")


def verify_checkout_redirect(base: str, expected_host: str | None, timeout: float) -> None:
    target = url(base, "/api/commerce/developer-pack/checkout", ATTRIBUTION)
    status, headers, body = request_no_redirect(target, timeout=timeout)

    if status == 503:
        detail = body.decode("utf-8", errors="replace")
        fail(f"checkout is not configured on deployed environment: {detail}")
    if status not in (301, 302, 303, 307, 308):
        fail(f"checkout route did not redirect: HTTP {status}")

    location = headers.get("location")
    if not location:
        fail("checkout redirect missing Location header")
    parsed = urllib.parse.urlparse(location)
    if parsed.scheme != "https":
        fail("checkout redirect is not HTTPS")
    if expected_host and parsed.hostname != expected_host:
        fail(f"checkout host mismatch: {parsed.hostname} != {expected_host}")
    if "/checkout/buy/" not in parsed.path:
        fail("configured checkout is not a shareable /checkout/buy/ URL")

    query = urllib.parse.parse_qs(parsed.query)
    for key, value in ATTRIBUTION.items():
        provider_key = f"checkout[custom][{key}]"
        if query.get(provider_key) != [value]:
            fail(f"checkout attribution missing: {provider_key}={value}")

    print(f"PASS checkout redirect host={parsed.hostname}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt Quarry public commercial surface smoke test")
    parser.add_argument("--base-url", default=os.getenv("PQ_BASE_URL"), help="Deployed Prompt Quarry base URL")
    parser.add_argument("--expected-checkout-host", default=os.getenv("PQ_EXPECT_CHECKOUT_HOST"))
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    if not args.base_url:
        fail("--base-url or PQ_BASE_URL is required")
    parsed_base = urllib.parse.urlparse(args.base_url)
    if parsed_base.scheme not in ("http", "https") or not parsed_base.netloc:
        fail("base URL must be an absolute http(s) URL")

    assert_page(args.base_url, "/", ("stop collecting random prompts", "prompt quarry"), args.timeout)
    assert_page(args.base_url, "/free/developer-starter-pack", ("three structured prompts", "developer starter pack"), args.timeout)
    assert_page(args.base_url, "/developer-pack", ("developer pack v1", "$19"), args.timeout)
    assert_page(args.base_url, "/license", ("use it", "adapt it", "resell"), args.timeout)
    verify_free_pack(args.base_url, args.timeout)
    verify_checkout_redirect(args.base_url, args.expected_checkout_host, args.timeout)

    print("COMMERCIAL PUBLIC SURFACE: PASS")
    print("attribution=smoke/test/pq-launch-0/commercial-e2e-smoke")
    print("PAYMENT GATE: NOT SATISFIED BY THIS SCRIPT")
    print("required_next=complete a real Lemon Squeezy test checkout and observe a signed order_created webhook")
    print("PQ-LAUNCH-0=BLOCKED until real provider test order + delivery are observed")


if __name__ == "__main__":
    main()
