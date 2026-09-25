#!/usr/bin/env python3
"""Build the Prompt Machine Starter Collection v1 customer archive deterministically.

The archive contains only the nine required customer-visible assets frozen by
ARTIFACT_LAYOUT_V1.json. ZIP_STORED + fixed metadata is used so the byte output
does not depend on compression-library behavior.

Building the archive creates packaging evidence only. It does not create runtime,
customer-value, provider-custody, delivery, certification, or revenue evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "product" / "starter-collection-v1"
LAYOUT_PATH = BASE / "ARTIFACT_LAYOUT_V1.json"

ARCHIVE_NAME = "prompt-machine-starter-collection-v1.zip"
ARCHIVE_ROOT = "prompt-machine-starter-collection-v1"
FIXED_TIMESTAMP = (2026, 9, 3, 0, 0, 0)
FILE_MODE = 0o100644 << 16

ALLOWED_LAYOUT_STATES = {
    "REQUIRED_CUSTOMER_PAYLOAD_PRESENT_ARCHIVE_NOT_BUILT",
    "DETERMINISTIC_ARCHIVE_BUILD_OBSERVED",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_layout() -> dict:
    return json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))


def build(output_dir: Path) -> tuple[Path, dict]:
    layout = load_layout()
    assert layout["schema"] == "prompt-machine-starter-artifact-layout-v1"
    assert layout["artifact_state"] in ALLOWED_LAYOUT_STATES

    assets = sorted(item["path"] for item in layout["customer_visible_assets"])
    assert len(assets) == 9

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / ARCHIVE_NAME

    entries: list[dict] = []
    with ZipFile(archive_path, "w", compression=ZIP_STORED) as zf:
        for relative in assets:
            source = BASE / relative
            if not source.is_file():
                raise FileNotFoundError(f"required customer asset missing: {relative}")

            data = source.read_bytes()
            archive_member = f"{ARCHIVE_ROOT}/{relative}"
            info = ZipInfo(filename=archive_member, date_time=FIXED_TIMESTAMP)
            info.compress_type = ZIP_STORED
            info.create_system = 3
            info.external_attr = FILE_MODE
            info.flag_bits = 0
            zf.writestr(info, data)

            entries.append({
                "path": relative,
                "archive_member": archive_member,
                "size_bytes": len(data),
                "sha256": sha256_bytes(data),
            })

    archive_bytes = archive_path.read_bytes()
    archive_hash = sha256_bytes(archive_bytes)
    archive_size = len(archive_bytes)

    canonical = layout["archive_identity"]
    if canonical.get("state") == "REPRODUCIBLE_BUILD_OBSERVED":
        assert canonical["filename"] == ARCHIVE_NAME
        assert canonical["sha256"] == archive_hash, (
            f"archive drift: expected {canonical['sha256']} observed {archive_hash}"
        )
        assert canonical["size_bytes"] == archive_size

    manifest = {
        "schema": "prompt-machine-starter-archive-build-v1",
        "version": "1.0.1",
        "product_id": "prompt-machine-starter-collection",
        "archive_name": ARCHIVE_NAME,
        "archive_format": "ZIP_STORED_FIXED_METADATA",
        "archive_root": ARCHIVE_ROOT,
        "required_customer_assets": len(entries),
        "entries": entries,
        "archive_size_bytes": archive_size,
        "archive_sha256": archive_hash,
        "source_commit": os.environ.get("GITHUB_SHA", "UNKNOWN_LOCAL_BUILD"),
        "canonical_archive_match": (
            canonical.get("state") == "REPRODUCIBLE_BUILD_OBSERVED"
            and canonical.get("sha256") == archive_hash
            and canonical.get("size_bytes") == archive_size
        ),
        "evidence_boundary": {
            "archive_build_is_runtime_evidence": False,
            "archive_build_is_provider_custody": False,
            "archive_build_is_delivery_evidence": False,
            "archive_build_is_product_ready": False,
            "archive_build_is_ready_to_sell": False,
        },
    }

    manifest_path = output_dir / "starter-collection-v1.build-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return archive_path, manifest


def verify_reproducible(output_dir: Path) -> dict:
    first_dir = output_dir / "first"
    second_dir = output_dir / "second"
    first_path, first = build(first_dir)
    second_path, second = build(second_dir)

    assert first["archive_sha256"] == second["archive_sha256"]
    assert first["archive_size_bytes"] == second["archive_size_bytes"]
    assert first_path.read_bytes() == second_path.read_bytes()

    final_archive = output_dir / ARCHIVE_NAME
    final_manifest = output_dir / "starter-collection-v1.build-manifest.json"
    final_archive.write_bytes(first_path.read_bytes())
    final_manifest.write_text(json.dumps(first, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return first


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="dist/starter-collection-v1")
    parser.add_argument("--verify-reproducible", action="store_true")
    args = parser.parse_args()

    output_dir = ROOT / args.output_dir
    if args.verify_reproducible:
        manifest = verify_reproducible(output_dir)
    else:
        _, manifest = build(output_dir)

    print("STARTER COLLECTION ARCHIVE BUILD: PASS")
    print(f"archive={manifest['archive_name']}")
    print(f"required_customer_assets={manifest['required_customer_assets']}")
    print(f"archive_size_bytes={manifest['archive_size_bytes']}")
    print(f"archive_sha256={manifest['archive_sha256']}")
    print(f"source_commit={manifest['source_commit']}")
    print(f"canonical_archive_match={str(manifest['canonical_archive_match']).lower()}")
    print("reproducible_check=" + ("PASS" if args.verify_reproducible else "NOT_REQUESTED"))
    print("model_calls=0")
    print("provider_calls=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
