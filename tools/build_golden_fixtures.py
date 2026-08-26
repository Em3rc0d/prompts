from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def compact(row: dict, reason: str) -> dict:
    return {
        "fixture_id": f"fixture_{row['uuid']}",
        "prompt_id": row.get("id"),
        "uuid": row.get("uuid"),
        "title": row.get("title"),
        "category": row.get("category"),
        "official_url": row.get("official_url"),
        "content_sha256": row.get("content_sha256"),
        "content_length": row.get("content_length"),
        "techniques": row.get("techniques") or [],
        "architecture_signature": row.get("architecture_signature"),
        "features": row.get("features") or {},
        "selection_reason": reason,
        "body_stored": False,
    }


def rank(row: dict) -> tuple:
    return (
        len(row.get("techniques") or []),
        (row.get("features") or {}).get("variable_markers", 0),
        (row.get("features") or {}).get("numbered_steps", 0),
        row.get("content_length") or 0,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/fixtures/alpacka-free-golden-fixtures.json")
    parser.add_argument("--manifest", default="quarry/fixtures/alpacka-free-golden-fixtures-manifest.json")
    args = parser.parse_args()

    rows = read_jsonl(Path(args.input))
    if not rows:
        raise SystemExit("No technique vectors found.")

    selected: dict[str, dict] = {}
    reasons: dict[str, set[str]] = defaultdict(set)

    # One strongest exemplar for every observed technique.
    all_techniques = sorted({t for row in rows for t in row.get("techniques", [])})
    for technique in all_techniques:
        candidates = [row for row in rows if technique in (row.get("techniques") or [])]
        if not candidates:
            continue
        winner = max(candidates, key=rank)
        selected[winner["uuid"]] = winner
        reasons[winner["uuid"]].add(f"technique:{technique}")

    # One strongest exemplar per source category.
    categories = sorted({row.get("category") for row in rows if row.get("category")})
    for category in categories:
        candidates = [row for row in rows if row.get("category") == category]
        winner = max(candidates, key=rank)
        selected[winner["uuid"]] = winner
        reasons[winner["uuid"]].add(f"category:{category}")

    # Exemplars for the ten most frequent architecture signatures.
    signature_counts = Counter(row.get("architecture_signature") or "none" for row in rows)
    for signature, count in signature_counts.most_common(10):
        candidates = [row for row in rows if (row.get("architecture_signature") or "none") == signature]
        winner = max(candidates, key=rank)
        selected[winner["uuid"]] = winner
        reasons[winner["uuid"]].add(f"signature:{signature} (n={count})")

    fixtures = []
    for uuid, row in sorted(selected.items(), key=lambda item: ((item[1].get("category") or "").casefold(), (item[1].get("title") or "").casefold())):
        fixtures.append(compact(row, "; ".join(sorted(reasons[uuid]))))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"fixtures": fixtures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "source_records": len(rows),
        "fixture_records": len(fixtures),
        "techniques_covered": all_techniques,
        "technique_count": len(all_techniques),
        "categories_covered": categories,
        "category_count": len(categories),
        "top_signatures_covered": [signature for signature, _ in signature_counts.most_common(10)],
        "selection_policy": "Union of strongest exemplar per observed technique, strongest exemplar per category, and exemplar per top-10 architecture signature. Ranking favors technique breadth, variable markers, numbered steps and then content length.",
        "body_storage_policy": "Fixtures contain references, fingerprints and feature vectors only. Prompt bodies are not stored.",
    }
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
