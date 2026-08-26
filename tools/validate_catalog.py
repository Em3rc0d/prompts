from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from common import read_jsonl

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "catalog" / "schema.json"
CATALOG_PATH = ROOT / "catalog" / "catalog.jsonl"
SOURCES_PATH = ROOT / "catalog" / "sources.jsonl"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    sources = {record["id"]: record for record in read_jsonl(SOURCES_PATH)}
    records = list(read_jsonl(CATALOG_PATH))

    errors: list[str] = []
    ids: set[str] = set()

    for index, record in enumerate(records, 1):
        record_id = record.get("id", f"line-{index}")
        if record_id in ids:
            fail(f"duplicate id: {record_id}", errors)
        ids.add(record_id)

        if record.get("source_id") not in sources:
            fail(f"{record_id}: unknown source_id {record.get('source_id')!r}", errors)

        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "<root>"
            fail(f"{record_id}: schema {location}: {error.message}", errors)

        provenance = record.get("provenance") or []
        if not provenance:
            fail(f"{record_id}: missing provenance", errors)

        source_url = record.get("source_url")
        if source_url and not any(item.get("url") == source_url for item in provenance):
            fail(f"{record_id}: source_url is not represented in provenance", errors)

        if record.get("verification") == "source-body-observed" and not record.get("body"):
            fail(f"{record_id}: source-body-observed requires body", errors)

        if record.get("fingerprint") and not record.get("body"):
            fail(f"{record_id}: fingerprint exists but body is null", errors)

        if record.get("official_post_url") and "threads.com" in record["official_post_url"]:
            if record.get("source_id") != "src_alpacka_threads":
                fail(f"{record_id}: Threads official_post_url does not use Threads source_id", errors)

    if errors:
        print("Catalog validation FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Catalog validation OK: {len(records)} records, {len(sources)} sources")


if __name__ == "__main__":
    main()
