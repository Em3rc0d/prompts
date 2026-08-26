from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright


def sanitize(value, depth: int = 0):
    if depth > 8:
        return "<max-depth>"
    if isinstance(value, dict):
        return {str(k): sanitize(v, depth + 1) for k, v in list(value.items())[:100]}
    if isinstance(value, list):
        return [sanitize(v, depth + 1) for v in value[:50]]
    if isinstance(value, str):
        if len(value) <= 180:
            return value
        digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
        return f"<string:{len(value)} chars sha256:{digest}>"
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return str(type(value).__name__)


def text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


async def probe_page(browser, url: str) -> dict:
    page = await browser.new_page(user_agent="PromptQuarry/0.5 (+personal research; sanitized dynamic metadata probe)")
    network = []
    source_host = urlparse(url).netloc.casefold()

    async def inspect_response(response):
        request = response.request
        parsed = urlparse(response.url)
        relevant_host = parsed.netloc.casefold() == source_host or "supabase.co" in parsed.netloc.casefold()
        content_type = (response.headers.get("content-type") or "").lower()
        if not relevant_host:
            return
        if request.resource_type not in {"fetch", "xhr", "document"}:
            return
        entry = {
            "url": response.url,
            "status": response.status,
            "resource_type": request.resource_type,
            "method": request.method,
            "content_type": content_type,
        }
        if "json" in content_type:
            try:
                entry["json_shape"] = sanitize(await response.json())
            except Exception:
                entry["json_shape"] = "<unreadable-json>"
        network.append(entry)

    def on_response(response):
        asyncio.create_task(inspect_response(response))

    page.on("response", on_response)
    navigation = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    try:
        await page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        await page.wait_for_timeout(2500)
    await page.wait_for_timeout(750)

    headings = {}
    for selector in ("h1", "h2", "h3"):
        values = []
        for text in await page.locator(selector).all_text_contents():
            text = " ".join(text.split()).strip()
            if text and text not in values:
                values.append(text[:300])
        headings[selector] = values[:50]

    buttons = []
    for text in await page.locator("button").all_text_contents():
        text = " ".join(text.split()).strip()
        if text and text not in buttons:
            buttons.append(text[:120])

    visible = await page.locator("body").inner_text()
    canonical = await page.locator('link[rel="canonical"]').get_attribute("href") if await page.locator('link[rel="canonical"]').count() else None

    result = {
        "requested_url": url,
        "final_url": page.url,
        "navigation_status": navigation.status if navigation else None,
        "title": await page.title(),
        "canonical": canonical,
        "headings": headings,
        "buttons": buttons[:40],
        "visible_text_length": len(visible),
        "visible_text_sha256": text_hash(visible),
        "network": network[:100],
        "body_stored": False,
    }
    await page.close()
    return result


async def main_async(args) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        results = []
        for url in args.urls:
            results.append(await probe_page(browser, url))
        await browser.close()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "probe_version": 1,
        "policy": "No page body or long JSON strings are stored. Long strings are replaced by length and SHA-256 prefix; headers and credentials are not stored.",
        "results": results,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--output", required=True)
    asyncio.run(main_async(parser.parse_args()))
