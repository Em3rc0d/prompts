from __future__ import annotations

import argparse
import json
from collections import deque

import httpx
from bs4 import BeautifulSoup


def safe_text(value: str | None, limit: int = 180) -> str | None:
    if not value:
        return None
    value = " ".join(value.split())
    return value if len(value) <= limit else value[:limit] + "…"


def walk_json(value, prefix: str = "", max_items: int = 120):
    queue = deque([(prefix, value)])
    emitted = 0
    while queue and emitted < max_items:
        path, current = queue.popleft()
        if isinstance(current, dict):
            for key, child in current.items():
                child_path = f"{path}.{key}" if path else str(key)
                queue.append((child_path, child))
        elif isinstance(current, list):
            for idx, child in enumerate(current[:20]):
                queue.append((f"{path}[{idx}]", child))
        elif isinstance(current, (str, int, float, bool)) or current is None:
            # Do not emit long body-like strings. This probe is for structure/metadata.
            if isinstance(current, str) and len(current) > 220:
                shown = f"<string:{len(current)} chars>"
            else:
                shown = current
            yield path, shown
            emitted += 1


def probe(url: str) -> dict:
    headers = {"User-Agent": "PromptQuarry/0.2 (+personal research; metadata probe)"}
    with httpx.Client(timeout=30, follow_redirects=True, headers=headers) as client:
        response = client.get(url)

    result = {
        "url": url,
        "final_url": str(response.url),
        "http_status": response.status_code,
        "content_type": response.headers.get("content-type"),
    }
    if response.status_code in {401, 403, 429}:
        result["blocked"] = True
        return result

    soup = BeautifulSoup(response.text, "html.parser")
    result["title"] = safe_text(soup.title.string if soup.title else None)
    result["h1"] = [safe_text(x.get_text(" ", strip=True)) for x in soup.find_all("h1")[:4]]
    result["h2"] = [safe_text(x.get_text(" ", strip=True)) for x in soup.find_all("h2")[:8]]

    meta = {}
    for node in soup.find_all("meta"):
        key = node.get("property") or node.get("name")
        value = node.get("content")
        if key in {"description", "og:title", "og:description", "twitter:title", "twitter:description"}:
            meta[key] = safe_text(value)
    result["meta"] = meta

    structured = []
    for script in soup.find_all("script"):
        raw = script.string or script.get_text()
        if not raw:
            continue
        if script.get("type") == "application/ld+json" or script.get("id") == "__NEXT_DATA__":
            try:
                obj = json.loads(raw)
            except Exception:
                continue
            structured.append({"script_id": script.get("id"), "script_type": script.get("type"), "fields": list(walk_json(obj))})
    result["structured"] = structured
    result["html_bytes"] = len(response.content)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")
    args = parser.parse_args()
    for url in args.urls:
        print(json.dumps(probe(url), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
