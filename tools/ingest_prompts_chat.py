from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


EXPECTED_FIELDS = {"act", "prompt", "for_devs", "type", "contributor"}


def fnvpair_utf16(text: str) -> str:
    """Reproduce Prompt Quarry's lightweight fnvpair-v1 working fingerprint."""
    raw = text.encode("utf-16-le", errors="surrogatepass")
    h1 = 0x811C9DC5
    h2 = 0x9E3779B9
    unit_index = 0
    for offset in range(0, len(raw), 2):
        code_unit = raw[offset] | (raw[offset + 1] << 8)
        h1 = ((h1 ^ code_unit) * 0x01000193) & 0xFFFFFFFF
        h2 = ((h2 ^ (code_unit + (unit_index & 255))) * 0x85EBCA6B) & 0xFFFFFFFF
        unit_index += 1
    return f"fnvpair:{h1:08x}{h2:08x}"


def normalize_row(row: dict[str, str], index: int) -> dict:
    content = row["prompt"]
    title = row["act"]
    return {
        "id": f"pc-{index:06d}",
        "artifact_type": "prompt-source",
        "source_id": "src_prompts_chat",
        "source_row": index + 1,
        "title": title,
        "title_normalized": " ".join(title.split()),
        "type": row["type"].strip(),
        "for_devs": row["for_devs"].strip().upper() == "TRUE",
        "content": content,
        "content_fingerprint": fnvpair_utf16(content),
        "content_length": len(content),
        "content_origin": "source-observed-cc0",
        "verification": "source-repository-observed",
        "certification_state": "UNREVIEWED",
    }


def write_chunks(records: list[dict], output_dir: Path, chunk_chars: int) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    parts: list[list[str]] = []
    current: list[str] = []
    chars = 0

    for record in records:
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        if current and chars + len(line) + 1 > chunk_chars:
            parts.append(current)
            current = []
            chars = 0
        current.append(line)
        chars += len(line) + 1

    if current:
        parts.append(current)

    names: list[str] = []
    for part_number, lines in enumerate(parts, 1):
        name = f"prompts-{part_number:04d}.jsonl"
        (output_dir / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
        names.append(name)
    return names


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest a pinned prompts.chat prompts.csv into Prompt Quarry."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source-blob-sha", required=True)
    parser.add_argument("--captured-on", required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("quarry/normalized/prompts-chat"),
    )
    parser.add_argument("--chunk-chars", type=int, default=1_400_000)
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != EXPECTED_FIELDS:
            raise SystemExit(f"Unexpected prompts.chat CSV schema: {reader.fieldnames}")
        rows = list(reader)

    records = [normalize_row(row, index) for index, row in enumerate(rows, 1)]
    parts = write_chunks(records, args.output_dir, args.chunk_chars)

    print(
        json.dumps(
            {
                "source_commit": args.source_commit,
                "source_blob_sha": args.source_blob_sha,
                "captured_on": args.captured_on,
                "records": len(records),
                "parts": parts,
                "contributors_copied": False,
                "certification_state": "UNREVIEWED",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
