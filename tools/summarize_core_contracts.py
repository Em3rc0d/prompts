from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


def summarize_shape(shape):
    if isinstance(shape, list):
        first = shape[0] if shape else None
        result = {
            "shape_type": "array",
            "captured_sample_items": len(shape),
        }
        if isinstance(first, dict):
            result["item_keys"] = sorted(first.keys())
            result["sample_item"] = {
                key: value
                for key, value in first.items()
                if key in {"id", "title", "name", "category", "is_premium", "created_at", "ai_tool", "slug", "published"}
                and not (isinstance(value, str) and len(value) > 180)
            }
        return result
    if isinstance(shape, dict):
        return {
            "shape_type": "object",
            "keys": sorted(shape.keys()),
        }
    return {
        "shape_type": type(shape).__name__,
    }


def endpoint_name(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path
    if "/rpc/" in path:
        return path.rsplit("/rpc/", 1)[-1]
    if "/rest/v1/" in path:
        return path.rsplit("/rest/v1/", 1)[-1]
    return path or url


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/normalized/alpacka-ai-core-data-contracts.json")
    args = parser.parse_args()

    probe = json.loads(Path(args.input).read_text(encoding="utf-8"))
    surfaces = []
    endpoint_counts = Counter()

    for result in probe.get("results", []):
        endpoints = []
        for entry in result.get("network", []):
            url = entry.get("url") or ""
            if "supabase.co" not in urlparse(url).netloc.casefold():
                continue
            name = endpoint_name(url)
            endpoint_counts[name] += 1
            endpoints.append({
                "name": name,
                "url": url,
                "method": entry.get("method"),
                "status": entry.get("status"),
                "resource_type": entry.get("resource_type"),
                "content_type": entry.get("content_type"),
                "response_shape": summarize_shape(entry.get("json_shape")) if "json_shape" in entry else None,
            })

        buttons = result.get("buttons") or []
        counters = []
        for button in buttons:
            if any(token in button for token in ("Todos (", "Gratis (", "Premium (", "Nuevos (")):
                counters.append(button)

        surfaces.append({
            "surface_url": result.get("requested_url"),
            "final_url": result.get("final_url"),
            "title": result.get("title"),
            "navigation_status": result.get("navigation_status"),
            "h1": (result.get("headings") or {}).get("h1") or [],
            "rendered_counters": counters,
            "visible_text_length": result.get("visible_text_length"),
            "visible_text_sha256_prefix": result.get("visible_text_sha256"),
            "public_data_endpoints": endpoints,
        })

    output = {
        "source_probe": str(args.input),
        "surface_count": len(surfaces),
        "unique_endpoint_names": sorted(endpoint_counts.keys()),
        "endpoint_observation_counts": dict(endpoint_counts),
        "surfaces": surfaces,
        "policy": "Compact contract summary derived from sanitized browser/network evidence. Credentials, headers and long source bodies are not stored.",
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
