from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "uncategorized"


def pct(part: int, total: int) -> float:
    return round((part / total) * 100, 2) if total else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--analysis", default="quarry/analysis/alpacka-ai-free-structure-report.json")
    parser.add_argument("--index-dir", default="quarry/indexes/alpacka-ai/categories")
    parser.add_argument("--readme", default="library/prompts/alpacka/README.md")
    args = parser.parse_args()

    records = list(read_jsonl(Path(args.input)))
    free = [r for r in records if r.get("access") == "free"]
    premium = [r for r in records if r.get("access") == "premium"]

    category_all: Counter[str] = Counter()
    category_free: Counter[str] = Counter()
    variable_counts: Counter[str] = Counter()
    signal_counts: Counter[str] = Counter()
    numeric_totals: Counter[str] = Counter()
    by_category: dict[str, list[dict]] = defaultdict(list)

    for row in records:
        category = row.get("category") or "Uncategorized"
        category_all[category] += 1
        by_category[category].append(row)

        if row.get("access") != "free":
            continue
        category_free[category] += 1
        for variable in row.get("variables") or []:
            variable_counts[str(variable).strip()] += 1
        signals = row.get("structural_signals") or {}
        for key in ("role_assignment", "stepwise_procedure", "output_contract", "question_first", "explicit_constraints"):
            if signals.get(key):
                signal_counts[key] += 1
        for key in ("numbered_steps", "bullet_lines", "line_count", "paragraph_count"):
            value = signals.get(key)
            if isinstance(value, int):
                numeric_totals[key] += value

    report = {
        "records": len(records),
        "free_records": len(free),
        "premium_records": len(premium),
        "categories": dict(category_all.most_common()),
        "free_categories": dict(category_free.most_common()),
        "free_structure_signals": {
            key: {"count": count, "percent": pct(count, len(free))}
            for key, count in signal_counts.most_common()
        },
        "free_average_structure": {
            key: round(total / len(free), 2) if free else 0.0
            for key, total in numeric_totals.items()
        },
        "top_variables": [
            {"variable": name, "count": count}
            for name, count in variable_counts.most_common(100)
        ],
        "policy": "Analysis uses harvested metadata/fingerprints only. Prompt bodies are not read from disk because they are never persisted.",
    }

    analysis_path = Path(args.analysis)
    analysis_path.parent.mkdir(parents=True, exist_ok=True)
    analysis_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    index_dir = Path(args.index_dir)
    index_dir.mkdir(parents=True, exist_ok=True)
    for old in index_dir.glob("*.jsonl"):
        old.unlink()

    category_rows = []
    for category, rows in sorted(by_category.items(), key=lambda item: (-len(item[1]), item[0].casefold())):
        slug = slugify(category)
        path = index_dir / f"{slug}.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for row in sorted(rows, key=lambda r: ((r.get("title") or "").casefold(), r.get("uuid") or "")):
                compact = {
                    "id": row.get("id"),
                    "uuid": row.get("uuid"),
                    "title": row.get("title"),
                    "category": category,
                    "access": row.get("access"),
                    "ai_tool": row.get("ai_tool"),
                    "created_at": row.get("created_at"),
                    "official_url": row.get("official_url"),
                    "content_available": row.get("content_available"),
                    "content_length": row.get("content_length"),
                    "content_sha256": row.get("content_sha256"),
                    "variables": row.get("variables") or [],
                    "structural_signals": row.get("structural_signals"),
                }
                handle.write(json.dumps(compact, ensure_ascii=False) + "\n")
        category_rows.append((category, len(rows), category_free.get(category, 0), slug))

    lines = [
        "# Alpacka public prompt reference index",
        "",
        "This directory is a provenance-first navigation layer over public Alpacka prompt metadata.",
        "",
        "It does **not** mirror premium prompt bodies. Premium entries remain metadata-only. Free prompt bodies are not stored either; they are processed in memory for fingerprints and structural features, then discarded.",
        "",
        f"- Total prompt references: **{len(records)}**",
        f"- Free: **{len(free)}**",
        f"- Premium metadata-only: **{len(premium)}**",
        f"- Categories: **{len(category_rows)}**",
        "",
        "## Categories",
        "",
        "| Category | Total | Free | Index |",
        "| --- | ---: | ---: | --- |",
    ]
    for category, total, free_count, slug in category_rows:
        lines.append(f"| {category} | {total} | {free_count} | `quarry/indexes/alpacka-ai/categories/{slug}.jsonl` |")

    lines.extend([
        "",
        "## Structural mining",
        "",
        "Aggregate free-prompt structure is stored in `quarry/analysis/alpacka-ai-free-structure-report.json`.",
        "This includes common variable markers, role assignment, stepwise procedures, output contracts, clarification-first behavior and explicit constraints.",
        "",
        "## Provenance boundary",
        "",
        "Every record retains its official Alpacka URL. The quarry distinguishes source-observed metadata from repository-authored patterns/templates. Derived library artifacts must cite their source IDs and must not claim to reproduce premium prompt content.",
    ])

    readme = Path(args.readme)
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
