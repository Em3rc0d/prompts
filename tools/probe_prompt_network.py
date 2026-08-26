from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def sanitize(value, depth: int = 0):
    if depth > 8:
        return "<max-depth>"
    if isinstance(value, dict):
        return {str(k): sanitize(v, depth + 1) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v, depth + 1) for v in value[:50]] + (["<truncated-list>"] if len(value) > 50 else [])
    if isinstance(value, str):
        normalized = " ".join(value.split())
        if len(normalized) > 160:
            return f"<string:{len(normalized)} chars sha256:{short_hash(normalized)}>"
        return normalized
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return f"<{type(value).__name__}>"


def safe_url(value: str) -> str:
    # Preserve endpoint/query structure; credentials/headers are never recorded.
    parsed = urlparse(value)
    return parsed.geturl()


async def probe_one(browser, url: str) -> dict:
    page = await browser.new_page(
        viewport={"width": 1440, "height": 1000},
        user_agent="PromptQuarry/0.3 (+personal research; sanitized network probe)",
    )
    network: list[dict] = []
    pending: list[asyncio.Task] = []

    async def inspect_response(response):
        request = response.request
        if request.resource_type not in {"xhr", "fetch", "document"}:
            return
        item = {
            "url": safe_url(response.url),
            "status": response.status,
            "resource_type": request.resource_type,
            "method": request.method,
            "content_type": response.headers.get("content-type"),
        }
        content_type = (item["content_type"] or "").lower()
        if "json" in content_type:
            try:
                payload = await response.json()
                item["json_shape"] = sanitize(payload)
            except Exception as exc:
                item["json_error"] = type(exc).__name__
        network.append(item)

    def on_response(response):
        pending.append(asyncio.create_task(inspect_response(response)))

    page.on("response", on_response)
    nav = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(5000)
    try:
        await page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)

    rendered = {}
    for selector in ["h1", "h2", "h3", "button"]:
        values = []
        locator = page.locator(selector)
        count = min(await locator.count(), 30)
        for i in range(count):
            try:
                text = " ".join((await locator.nth(i).inner_text()).split())
            except Exception:
                continue
            if not text:
                continue
            values.append(sanitize(text))
        if values:
            rendered[selector] = values

    body_text = " ".join((await page.locator("body").inner_text()).split())
    markers = {}
    for token in ["Gratis", "Premium", "Cualquier modelo", "Suscríbete", "Iniciar sesión", "Copiar prompt"]:
        markers[token] = token.casefold() in body_text.casefold()

    result = {
        "requested_url": url,
        "final_url": page.url,
        "navigation_status": nav.status if nav else None,
        "rendered": rendered,
        "visible_markers": markers,
        "body_length": len(body_text),
        "body_sha256": short_hash(body_text),
        "network": network,
    }
    await page.close()
    return result


async def async_main(args) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        results = []
        for url in args.urls:
            results.append(await probe_one(browser, url))
        await browser.close()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "probe_version": 1,
        "policy": "Long strings are replaced by length + SHA-256 prefix; request/response headers and credentials are not stored.",
        "results": results,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--output", default="quarry/fixtures/alpacka-detail-network-probe.json")
    args = parser.parse_args()
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
