from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from common import canonicalize, sha256_text, slugify, utc_now, write_jsonl

REVEAL_RE = re.compile(
    r"\b(ver|mostrar|abrir|revelar|copiar|view|show|open|copy)\b.*\b(prompt|skill|habilidad)\b",
    re.IGNORECASE,
)
PROMPT_SIGNAL_RE = re.compile(
    r"\b(prompt|act[uú]a como|tu tarea|instrucciones|objetivo|contexto|debes|genera|crea|analiza|reescribe|diseña|paso 1)\b",
    re.IGNORECASE,
)


def interesting_text(text: str) -> bool:
    text = canonicalize(text)
    if len(text) < 70 or len(text) > 30_000:
        return False
    if PROMPT_SIGNAL_RE.search(text):
        return True
    return len(text) >= 220 and any(
        token in text.lower()
        for token in ("chatgpt", "claude", "gemini", "ia", "inteligencia artificial")
    )


def parse_html_candidates(html: str, base_url: str) -> tuple[list[dict], list[dict]]:
    soup = BeautifulSoup(html, "html.parser")
    records: list[dict] = []
    links: list[dict] = []
    seen_text: set[str] = set()
    seen_link: set[str] = set()

    for anchor in soup.find_all("a", href=True):
        href = urljoin(base_url, anchor.get("href"))
        if href in seen_link:
            continue
        seen_link.add(href)
        label = canonicalize(anchor.get_text(" ", strip=True))
        links.append({"url": href, "label": label or None})

    selectors = [
        "article",
        "[role='article']",
        "[role='dialog']",
        "[class*='prompt']",
        "[class*='skill']",
        "[data-testid*='prompt']",
        "pre",
        "blockquote",
        "section",
    ]

    for selector in selectors:
        for node in soup.select(selector):
            text = canonicalize(node.get_text(" ", strip=True))
            if not interesting_text(text) or text in seen_text:
                continue
            seen_text.add(text)
            records.append(
                {
                    "text": text,
                    "selector_family": selector,
                    "element": node.name,
                    "classes": node.get("class") or [],
                }
            )

    # Modern web apps often serialize useful catalog data into script JSON.
    for script in soup.find_all("script"):
        raw = script.string or script.get_text(" ", strip=True)
        if not raw or len(raw) < 80:
            continue
        script_type = (script.get("type") or "").lower()
        if "json" not in script_type and "__next" not in raw.lower() and "prompt" not in raw.lower():
            continue
        # Keep only the script as evidence; downstream tooling can parse exact app schemas later.
        text = canonicalize(raw)
        if interesting_text(text) and text not in seen_text:
            seen_text.add(text)
            records.append(
                {
                    "text": text,
                    "selector_family": "embedded-script",
                    "element": "script",
                    "classes": [],
                }
            )

    return records, links


async def reveal_visible_prompts(page, delay_ms: int) -> list[dict]:
    captured: list[dict] = []
    buttons = page.get_by_role("button")
    count = await buttons.count()

    for index in range(min(count, 500)):
        button = buttons.nth(index)
        try:
            if not await button.is_visible():
                continue
            label = canonicalize(await button.inner_text())
            if not REVEAL_RE.search(label):
                continue

            await button.click(timeout=2_500)
            await page.wait_for_timeout(min(delay_ms, 800))

            dialogs = page.locator("[role='dialog']")
            if await dialogs.count():
                dialog = dialogs.last
                text = canonicalize(await dialog.inner_text())
                if interesting_text(text):
                    captured.append({"label": label, "text": text, "mode": "dialog"})
                await page.keyboard.press("Escape")
            else:
                body_text = canonicalize(await page.locator("body").inner_text())
                if interesting_text(body_text):
                    captured.append({"label": label, "text": body_text, "mode": "page-state"})
        except Exception:
            # A single unstable control must not kill the whole quarry run.
            continue

    return captured


async def main_async(args) -> None:
    output = Path(args.output)
    snapshot_dir = Path(args.snapshot_dir)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    captured_at = utc_now()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=not args.headful)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 1100},
            user_agent="PromptQuarry/0.1 personal-research",
        )
        page = await context.new_page()

        response = await page.goto(args.url, wait_until="domcontentloaded", timeout=60_000)
        status = response.status if response else None
        if status in {401, 403, 429}:
            print(
                json.dumps(
                    {
                        "status": "blocked",
                        "http_status": status,
                        "url": args.url,
                        "reason": "Access/rate barrier encountered; collector stopped without bypass.",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            await browser.close()
            return

        try:
            await page.wait_for_load_state("networkidle", timeout=12_000)
        except PlaywrightTimeoutError:
            pass
        await page.wait_for_timeout(args.delay_ms)

        previous_height = 0
        stagnant = 0
        for _ in range(args.max_scrolls):
            height = await page.evaluate("document.body.scrollHeight")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(args.delay_ms)
            if height == previous_height:
                stagnant += 1
                if stagnant >= 3:
                    break
            else:
                stagnant = 0
            previous_height = height

        revealed = await reveal_visible_prompts(page, args.delay_ms)
        html = await page.content()
        final_url = page.url
        title = await page.title()

        host = slugify(urlparse(final_url).netloc)
        snapshot_path = snapshot_dir / f"{host}-{captured_at[:10]}.html"
        snapshot_path.write_text(html, encoding="utf-8")

        candidates, links = parse_html_candidates(html, final_url)
        records: list[dict] = []
        seen: set[str] = set()

        for candidate in candidates:
            text = candidate["text"]
            fingerprint = sha256_text(text)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            records.append(
                {
                    "quarry_record_type": "web_candidate",
                    "source_id": "src_alpacka_web",
                    "source_key": fingerprint[7:23],
                    "source_url": final_url,
                    "official_post_url": None,
                    "raw_url": final_url,
                    "source_snapshot_path": str(snapshot_path),
                    "capture_mode": "rendered-page",
                    "verification": "source-body-observed",
                    "captured_at": captured_at,
                    "title": None,
                    "body": text,
                    "fingerprint": fingerprint,
                    "raw": {k: v for k, v in candidate.items() if k != "text"},
                }
            )

        for item in revealed:
            text = item["text"]
            fingerprint = sha256_text(text)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            records.append(
                {
                    "quarry_record_type": "web_revealed_candidate",
                    "source_id": "src_alpacka_web",
                    "source_key": fingerprint[7:23],
                    "source_url": final_url,
                    "official_post_url": None,
                    "raw_url": final_url,
                    "source_snapshot_path": str(snapshot_path),
                    "capture_mode": "rendered-page",
                    "verification": "source-body-observed",
                    "captured_at": captured_at,
                    "title": item.get("label"),
                    "body": text,
                    "fingerprint": fingerprint,
                    "raw": {"reveal_mode": item.get("mode")},
                }
            )

        count = write_jsonl(output, records)
        link_path = output.with_name(output.stem + "-links.jsonl")
        write_jsonl(
            link_path,
            (
                {
                    "source_url": final_url,
                    "captured_at": captured_at,
                    **link,
                }
                for link in links
            ),
        )

        print(
            json.dumps(
                {
                    "status": "ok",
                    "http_status": status,
                    "page_title": title,
                    "final_url": final_url,
                    "records": count,
                    "links": len(links),
                    "output": str(output),
                    "snapshot": str(snapshot_path),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        await browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect public prompt-bank evidence with a rendered browser.")
    parser.add_argument(
        "--url",
        default="https://alpackaai.xyz/bank-prompts?utm_source=threads&utm_medium=social&utm_content=link_in_bio",
    )
    parser.add_argument("--output", default="quarry/raw/alpacka-ai/web/candidates.jsonl")
    parser.add_argument("--snapshot-dir", default="quarry/raw/alpacka-ai/web/snapshots")
    parser.add_argument("--max-scrolls", type=int, default=100)
    parser.add_argument("--delay-ms", type=int, default=1_500)
    parser.add_argument("--headful", action="store_true")
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
