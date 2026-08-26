from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


def sha256(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def clean(value: str | None, limit: int = 500) -> str | None:
    if value is None:
        return None
    value = " ".join(value.split()).strip()
    return value[:limit] if value else None


def meta(soup: BeautifulSoup, *, name: str | None = None, prop: str | None = None) -> str | None:
    tag = soup.find("meta", attrs={"name": name}) if name else soup.find("meta", attrs={"property": prop})
    return clean(tag.get("content")) if tag else None


def jsonld_metadata(soup: BeautifulSoup) -> dict:
    values = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text() or ""
        try:
            data = json.loads(raw)
        except Exception:
            continue
        values.append(data)

    found: dict[str, str | list[str] | None] = {}

    def walk(node):
        if isinstance(node, dict):
            type_value = node.get("@type")
            types = type_value if isinstance(type_value, list) else [type_value] if type_value else []
            if any(t in {"Article", "BlogPosting", "NewsArticle"} for t in types):
                for key in ("headline", "datePublished", "dateModified"):
                    if key in node and key not in found:
                        found[key] = clean(str(node[key]), 300)
                author = node.get("author")
                if author and "author" not in found:
                    if isinstance(author, dict):
                        found["author"] = clean(str(author.get("name")), 200)
                    elif isinstance(author, list):
                        names = []
                        for item in author:
                            if isinstance(item, dict) and item.get("name"):
                                names.append(clean(str(item["name"]), 100))
                        found["author"] = [name for name in names if name]
                    else:
                        found["author"] = clean(str(author), 200)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    for value in values:
        walk(value)
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--output", default="quarry/normalized/public-page-metadata.jsonl")
    parser.add_argument("--manifest", default="quarry/normalized/public-page-metadata-manifest.json")
    args = parser.parse_args()

    records = []
    statuses: Counter[str] = Counter()
    client = httpx.Client(timeout=30.0, follow_redirects=True, headers={"user-agent": "PromptQuarry/0.5 (+personal research; metadata-only)"})
    try:
        for url in args.urls:
            response = client.get(url)
            response.raise_for_status()
            statuses[str(response.status_code)] += 1
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            final_url = str(response.url)
            base_host = urlparse(final_url).netloc.casefold()

            headings = {}
            for level in ("h1", "h2", "h3"):
                values = []
                for tag in soup.find_all(level):
                    value = clean(tag.get_text(" ", strip=True), 250)
                    if value and value not in values:
                        values.append(value)
                headings[level] = values[:50]

            canonical_tag = soup.find("link", rel=lambda value: value and "canonical" in value)
            canonical = urljoin(final_url, canonical_tag.get("href")) if canonical_tag and canonical_tag.get("href") else final_url

            internal_links = []
            external_links = []
            for anchor in soup.find_all("a", href=True):
                href = urljoin(final_url, anchor.get("href"))
                parsed = urlparse(href)
                if parsed.scheme not in {"http", "https"}:
                    continue
                target = href.split("#", 1)[0]
                bucket = internal_links if parsed.netloc.casefold() == base_host else external_links
                if target not in bucket:
                    bucket.append(target)

            text = soup.get_text(" ", strip=True)
            record = {
                "source_url": url,
                "final_url": final_url,
                "canonical_url": canonical,
                "http_status": response.status_code,
                "title": clean(soup.title.get_text(" ", strip=True), 300) if soup.title else None,
                "meta_description": meta(soup, name="description"),
                "og_title": meta(soup, prop="og:title"),
                "og_description": meta(soup, prop="og:description"),
                "headings": headings,
                "structured_article_metadata": jsonld_metadata(soup),
                "html_bytes": len(html),
                "html_sha256": sha256(html),
                "visible_text_length": len(text),
                "internal_links": internal_links[:200],
                "external_links": external_links[:100],
                "capture_mode": "metadata-only-page-harvest",
                "body_stored": False,
            }
            records.append(record)
    finally:
        client.close()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "records": len(records),
        "http_statuses": dict(statuses),
        "source_urls": args.urls,
        "body_storage_policy": "No article body is stored. The harvest retains page metadata, headings, links, sizes and fingerprints only.",
    }
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
