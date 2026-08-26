from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL in {path}:{line_no}: {exc}") from exc
            if not isinstance(record, dict):
                raise SystemExit(f"Expected object in {path}:{line_no}")
            records.append(record)
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Append staged catalog records without duplicating IDs.")
    parser.add_argument("catalog")
    parser.add_argument("promotions")
    args = parser.parse_args()

    catalog_path = Path(args.catalog)
    promotions_path = Path(args.promotions)
    current = read_jsonl(catalog_path)
    staged = read_jsonl(promotions_path)

    current_ids = [r.get("id") for r in current]
    if len(current_ids) != len(set(current_ids)):
        raise SystemExit("Catalog already contains duplicate IDs; refusing promotion.")

    staged_ids = [r.get("id") for r in staged]
    if any(not value for value in staged_ids):
        raise SystemExit("Every staged record must have an id.")
    if len(staged_ids) != len(set(staged_ids)):
        raise SystemExit("Promotion manifest contains duplicate IDs.")

    existing = set(current_ids)
    additions = [record for record in staged if record["id"] not in existing]
    skipped = [record["id"] for record in staged if record["id"] in existing]

    if additions:
        with catalog_path.open("a", encoding="utf-8") as handle:
            if catalog_path.stat().st_size and not catalog_path.read_bytes().endswith(b"\n"):
                handle.write("\n")
            for record in additions:
                handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")

    print(json.dumps({
        "catalog_records_before": len(current),
        "staged_records": len(staged),
        "added": [r["id"] for r in additions],
        "skipped_existing": skipped,
        "catalog_records_after": len(current) + len(additions),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
