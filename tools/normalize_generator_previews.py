from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def variables(text: str) -> list[str]:
    found = []
    for match in re.finditer(r"\[\s*([^\[\]\n]{1,80}?)\s*\]", text):
        value = " ".join(match.group(1).split()).strip()
        if value and value not in found:
            found.append(value)
    return found


def signals(text: str) -> dict:
    low = text.casefold()
    return {
        "role_assignment": bool(re.search(r"\b(act[uú]a como|eres un|eres una|adopta el rol)\b", low)),
        "variable_template": bool(variables(text)),
        "numbered_contract_items": len(re.findall(r"\(\d+\)", text)),
        "output_contract": any(token in low for token in ("genera", "crea", "deriva", "para cada")),
        "audience_or_user_context": any(token in low for token in ("audiencia", "producto", "objetivo", "oferta", "muestras")),
    }


def purpose_for(index: int) -> str:
    return {
        1: "growth-strategy-planning",
        2: "lead-magnet-ideation",
        3: "writing-style-specification",
    }.get(index, "generator-preview")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/normalized/alpacka-ai-generator-previews.jsonl")
    parser.add_argument("--manifest", default="quarry/normalized/alpacka-ai-generator-previews-manifest.json")
    args = parser.parse_args()

    source_rows = [
        row for row in read_jsonl(Path(args.input))
        if row.get("raw", {}).get("element") == "pre" and row.get("body")
    ]

    records = []
    for index, row in enumerate(source_rows, 1):
        body = row["body"]
        records.append({
            "id": f"alpacka_generator_preview_{index}",
            "artifact_type": "prompt-reference",
            "source_id": row.get("source_id"),
            "source_url": row.get("source_url"),
            "purpose": purpose_for(index),
            "access": "public-preview",
            "body_length": len(body),
            "body_sha256": row.get("fingerprint"),
            "variables": variables(body),
            "structural_signals": signals(body),
            "verification": row.get("verification"),
            "capture_mode": "rendered-generator-preview-metadata",
            "captured_at": row.get("captured_at"),
            "metadata": {
                "body_storage_policy": "source body not duplicated into normalized or library layers",
                "raw_source_key": row.get("source_key"),
                "source_raw_file": str(args.input),
            },
        })

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "records": len(records),
        "purposes": [r["purpose"] for r in records],
        "source": str(args.input),
        "policy": "Public preview bodies remain only in the raw capture layer. Normalized records retain provenance, hashes, variables and structural signals only.",
    }
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
