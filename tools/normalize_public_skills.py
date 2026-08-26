from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def extract_frontmatter(body: str) -> tuple[str | None, str | None]:
    match = re.search(r"---\s*name:\s*([^\n]+)\s*description:\s*([^\n]+)\s*---", body, re.I | re.S)
    if not match:
        return None, None
    return match.group(1).strip(), " ".join(match.group(2).split()).strip()


def parse_title(title: str | None) -> tuple[str | None, str | None]:
    if not title:
        return None, None
    match = re.match(r"^(.+?)\s+(GRATIS|PREMIUM)\s+", title.strip(), re.I)
    if not match:
        return None, None
    return match.group(1).strip(), match.group(2).lower()


def extract_variables(body: str) -> list[str]:
    values = []
    for pattern in (r"\{\{\s*([^{}]{1,80}?)\s*\}\}", r"\[\s*([^\[\]\n]{1,80}?)\s*\]", r"<\s*([^<>\n]{1,80}?)\s*>"):
        for match in re.finditer(pattern, body):
            value = " ".join(match.group(1).split()).strip()
            if value and value not in values:
                values.append(value)
            if len(values) >= 25:
                return values
    return values


def structure(body: str) -> dict:
    low = body.casefold()
    headings = len(re.findall(r"(?:^|\n)#{1,4}\s+", body))
    numbered = len(re.findall(r"(?:^|\n)\s*\d+[.)]\s+", body))
    bullets = len(re.findall(r"(?:^|\n)\s*[-*•]\s+", body))
    return {
        "has_role": bool(re.search(r"\b(eres un|eres una|act[uú]a como|tu rol)\b", low)),
        "has_intake_questions": any(x in low for x in ("antes de", "pregunta", "confirma", "necesitas saber")),
        "has_process": numbered >= 2 or any(x in low for x in ("proceso", "paso 1", "paso 2")),
        "has_rules": any(x in low for x in ("reglas", "reglas de oro", "obligatorio", "nunca", "siempre")),
        "has_output_contract": any(x in low for x in ("entrega siempre", "formato de entrega", "devuelve", "entrega")),
        "heading_count": headings,
        "numbered_step_count": numbered,
        "bullet_count": bullets,
        "line_count": len(body.splitlines()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/normalized/alpacka-ai-skills-metadata.jsonl")
    parser.add_argument("--manifest", default="quarry/normalized/alpacka-ai-skills-metadata-manifest.json")
    parser.add_argument("--analysis", default="quarry/analysis/alpacka-ai-skill-structure-report.json")
    parser.add_argument("--readme", default="library/skills/alpacka/README.md")
    args = parser.parse_args()

    records = []
    categories: Counter[str] = Counter()
    access_counts: Counter[str] = Counter()
    signal_counts: Counter[str] = Counter()
    variable_counts: Counter[str] = Counter()

    for row in read_jsonl(Path(args.input)):
        if row.get("quarry_record_type") != "web_revealed_candidate":
            continue
        body = row.get("body") or ""
        if not body:
            continue
        skill_name, description = extract_frontmatter(body)
        category, access = parse_title(row.get("title"))
        signals = structure(body)
        variables = extract_variables(body)
        if category:
            categories[category] += 1
        if access:
            access_counts[access] += 1
        for key, value in signals.items():
            if isinstance(value, bool) and value:
                signal_counts[key] += 1
        for variable in variables:
            variable_counts[variable] += 1

        records.append({
            "id": f"alpacka_skill_{row.get('source_key')}",
            "artifact_type": "skill-reference",
            "source_id": row.get("source_id"),
            "source_url": row.get("source_url"),
            "skill_name": skill_name,
            "description": description,
            "category": category,
            "access": access,
            "body_length": len(body),
            "body_sha256": row.get("fingerprint"),
            "variables": variables,
            "structural_signals": signals,
            "verification": row.get("verification"),
            "capture_mode": "public-skill-dialog-metadata",
            "captured_at": row.get("captured_at"),
            "metadata": {
                "body_storage_policy": "source body not duplicated into normalized/library layers",
                "raw_source_key": row.get("source_key"),
            },
        })

    records.sort(key=lambda r: ((r.get("category") or "~").casefold(), (r.get("skill_name") or "~").casefold()))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "records": len(records),
        "categories": dict(categories.most_common()),
        "access": dict(access_counts.most_common()),
        "source": str(args.input),
        "policy": "Normalized/library layers do not duplicate the observed third-party skill body. They retain provenance, concise metadata, fingerprints and structure only.",
    }
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    total = len(records)
    analysis = {
        "records": total,
        "structure_presence": {
            key: {"count": count, "percent": round(count * 100 / total, 2) if total else 0.0}
            for key, count in signal_counts.most_common()
        },
        "top_variables": [{"variable": name, "count": count} for name, count in variable_counts.most_common(50)],
        "categories": dict(categories.most_common()),
    }
    analysis_path = Path(args.analysis)
    analysis_path.parent.mkdir(parents=True, exist_ok=True)
    analysis_path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme = Path(args.readme)
    readme.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Alpacka public skill references",
        "",
        "This is a provenance-first index of publicly revealed Alpacka skills.",
        "",
        "The library layer does not mirror the source skill bodies. It stores concise metadata, source provenance, hashes, variables and structural signals so repository-authored skills can be derived without confusing source text with our own work.",
        "",
        f"- Public skill references normalized: **{total}**",
        f"- Categories observed: **{len(categories)}**",
        "",
        "| Category | Skill | Access | Source |",
        "| --- | --- | --- | --- |",
    ]
    for row in records:
        lines.append(f"| {row.get('category') or 'Uncategorized'} | `{row.get('skill_name') or row['id']}` | {row.get('access') or 'unknown'} | {row.get('source_url')} |")
    lines.extend([
        "",
        "Structural aggregate: `quarry/analysis/alpacka-ai-skill-structure-report.json`.",
        "Normalized metadata: `quarry/normalized/alpacka-ai-skills-metadata.jsonl`.",
    ])
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
