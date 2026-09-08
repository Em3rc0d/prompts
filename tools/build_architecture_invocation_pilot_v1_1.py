from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from build_architecture_invocation_pilot_v1 import ROOT, build_pilot, canonical_json, sha256_bytes

RENDERER_VERSION = "1.1.0"


def write_pilot(output_dir: Path) -> dict:
    bindings, invocations, manifest = build_pilot()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    packets_dir = output_dir / "packets"
    packets_dir.mkdir()

    (output_dir / "bindings.jsonl").write_text(
        "".join(canonical_json(row) + "\n" for row in bindings), encoding="utf-8"
    )

    clean_rows: list[dict] = []
    for source_row in invocations:
        row = {key: value for key, value in source_row.items() if key != "_bytes"}
        blocks = source_row["_bytes"]
        packet_dir = packets_dir / row["invocation_id"]
        packet_dir.mkdir()

        block_paths = []
        for index, payload in enumerate(blocks, start=1):
            path = packet_dir / f"block-{index}.txt"
            path.write_bytes(payload)
            observed = sha256_bytes(payload)
            expected = row["blocks"][index - 1]["sha256"]
            if observed != expected:
                raise ValueError(f"rendered block hash mismatch for {row['invocation_id']} block {index}")
            block_paths.append(str(path.relative_to(output_dir)))

        row["renderer_version"] = RENDERER_VERSION
        row["block_paths"] = block_paths
        (packet_dir / "invocation.json").write_text(
            json.dumps(row, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        clean_rows.append(row)

    (output_dir / "invocations.jsonl").write_text(
        "".join(canonical_json(row) + "\n" for row in clean_rows), encoding="utf-8"
    )

    manifest = dict(manifest)
    manifest["renderer_version"] = RENDERER_VERSION
    manifest["packet_layout"] = "one directory per invocation with three exact UTF-8 block files plus invocation.json"
    manifest["runtime_envelope_added"] = False
    manifest["rendered_packet_count"] = len(clean_rows)
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "quarry" / "etl" / "prompt-library-v1" / "invocation-pilot-v1",
    )
    args = parser.parse_args()
    print(json.dumps(write_pilot(args.output_dir), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
