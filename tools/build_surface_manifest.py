from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse, urlunparse


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def canonical_url(value: str) -> str:
    parsed = urlparse(value)
    host = parsed.netloc.lower()
    if host == "www.alpackaai.xyz":
        host = "alpackaai.xyz"
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunparse((parsed.scheme.lower() or "https", host, path, "", parsed.query, ""))


def classify_route(url: str, label: str | None) -> str:
    parsed = urlparse(url)
    path = parsed.path.lower()
    text = f"{path} {(label or '').lower()}"

    if parsed.netloc.lower().removeprefix("www.") != "alpackaai.xyz":
        return "external"
    if any(token in path for token in ("/terms", "/privacy", "/login", "/signin", "/auth")):
        return "policy-or-auth"
    if any(token in path for token in ("/pricing", "/checkout", "/subscribe")):
        return "commercial"
    if any(token in text for token in ("prompt", "prompts")):
        return "prompt-candidate"
    if any(token in text for token in ("skill", "skills", "habilidad")):
        return "skill-candidate"
    if any(token in text for token in ("categoria", "category", "tag", "coleccion", "collection")):
        return "index-or-category"
    if path in ("", "/"):
        return "root"
    return "internal-other"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--manifest", default="quarry/normalized/alpacka-ai-surface-manifest.json")
    parser.add_argument("--candidates", default="quarry/normalized/alpacka-ai-public-link-candidates.jsonl")
    args = parser.parse_args()

    input_path = Path(args.input)
    unique: dict[str, dict] = {}

    for row in read_jsonl(input_path):
        url = canonical_url(row["url"])
        record = {
            "url": url,
            "label": row.get("label"),
            "source_url": row.get("source_url"),
            "captured_at": row.get("captured_at"),
        }
        record["route_type"] = classify_route(url, record["label"])
        unique.setdefault(url, record)

    rows = sorted(unique.values(), key=lambda r: (r["route_type"], r["url"]))
    counts = Counter(row["route_type"] for row in rows)

    manifest = {
        "source": str(input_path),
        "unique_links": len(rows),
        "route_type_counts": dict(sorted(counts.items())),
        "candidate_links": sum(
            counts[key]
            for key in ("prompt-candidate", "skill-candidate", "index-or-category")
        ),
        "notes": [
            "Classification is route/label based and must be verified by fetching each candidate.",
            "www.alpackaai.xyz and alpackaai.xyz are canonicalized to the same host.",
        ],
    }

    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    candidates = [
        row
        for row in rows
        if row["route_type"] in {"prompt-candidate", "skill-candidate", "index-or-category", "internal-other"}
    ]
    candidate_path = Path(args.candidates)
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    with candidate_path.open("w", encoding="utf-8") as handle:
        for row in candidates:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(json.dumps({"status": "ok", **manifest}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
