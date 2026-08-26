from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def hashed_string_info(value):
    if not isinstance(value, str):
        return None, None
    match = re.fullmatch(r"<string:(\d+) chars sha256:([0-9a-f]+)>", value)
    if not match:
        return None, None
    return int(match.group(1)), f"sha256:{match.group(2)}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/normalized/alpacka-ai-blog-articles.jsonl")
    parser.add_argument("--manifest", default="quarry/normalized/alpacka-ai-blog-articles-manifest.json")
    args = parser.parse_args()

    probe = json.loads(Path(args.input).read_text(encoding="utf-8"))
    records = []

    for result in probe.get("results", []):
        article = None
        endpoint = None
        for entry in result.get("network", []):
            if "/rest/v1/blog_posts" not in (entry.get("url") or ""):
                continue
            shape = entry.get("json_shape")
            if isinstance(shape, list) and shape and isinstance(shape[0], dict):
                article = shape[0]
                endpoint = entry.get("url")
                break
        if not article:
            continue

        content_length, content_hash = hashed_string_info(article.get("content"))
        excerpt_length, excerpt_hash = hashed_string_info(article.get("excerpt"))
        records.append({
            "id": f"alpacka_blog_{article.get('id')}",
            "artifact_type": "reference",
            "source_id": "src_alpacka_web",
            "source_url": result.get("requested_url"),
            "official_url": result.get("final_url"),
            "title": article.get("title"),
            "slug": article.get("slug"),
            "category": article.get("category"),
            "published": article.get("published"),
            "created_at": article.get("created_at"),
            "updated_at": article.get("updated_at"),
            "content_length": content_length,
            "content_sha256_prefix": content_hash,
            "excerpt_length": excerpt_length,
            "excerpt_sha256_prefix": excerpt_hash,
            "headings": result.get("headings") or {},
            "visible_text_length": result.get("visible_text_length"),
            "visible_text_sha256_prefix": result.get("visible_text_sha256"),
            "verification": "source-api-observed",
            "capture_mode": "public-supabase-blog-metadata",
            "metadata": {
                "endpoint_observed": endpoint,
                "body_storage_policy": "article body not stored; sanitized network probe retains length/hash only",
            },
        })

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "records": len(records),
        "categories": sorted({r.get("category") for r in records if r.get("category")}),
        "slugs": [r.get("slug") for r in records],
        "source_probe": str(args.input),
        "body_storage_policy": "No blog article body is duplicated into normalized data. Records retain source metadata, headings, lengths and hash prefixes.",
    }
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
