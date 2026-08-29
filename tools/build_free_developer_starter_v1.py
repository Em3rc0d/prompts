#!/usr/bin/env python3
from __future__ import annotations

import argparse
import binascii
import hashlib
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / "product" / "free-developer-starter-v1"
MANIFEST_PATH = PACK_ROOT / "MANIFEST.release.json"
DEFAULT_OUTPUT = ROOT / "dist" / "prompt-quarry-developer-starter-v1.zip"
DEFAULT_RECEIPT = ROOT / ".ci" / "free-developer-starter-v1" / "release.json"

ZIP_ROOT = "prompt-quarry-developer-starter-v1"
UTF8_FLAG = 0x0800
DOS_TIME = 0
DOS_DATE = 0x21
VERSION_NEEDED = 20
VERSION_MADE_BY = (3 << 8) | 20
UNIX_FILE_MODE = 0o100644


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def build_stored_zip(entries: list[tuple[str, bytes]]) -> bytes:
    local_chunks: list[bytes] = []
    central_chunks: list[bytes] = []
    offset = 0

    for relative_path, data in sorted(entries, key=lambda item: item[0]):
        archive_name = f"{ZIP_ROOT}/{relative_path}".encode("utf-8")
        crc = binascii.crc32(data) & 0xFFFFFFFF

        local_header = struct.pack(
            "<IHHHHHIIIHH",
            0x04034B50, VERSION_NEEDED, UTF8_FLAG, 0, DOS_TIME, DOS_DATE,
            crc, len(data), len(data), len(archive_name), 0,
        )
        local_record = local_header + archive_name + data
        local_chunks.append(local_record)

        external_attr = UNIX_FILE_MODE << 16
        central_header = struct.pack(
            "<IHHHHHHIIIHHHHHII",
            0x02014B50, VERSION_MADE_BY, VERSION_NEEDED, UTF8_FLAG, 0,
            DOS_TIME, DOS_DATE, crc, len(data), len(data), len(archive_name),
            0, 0, 0, 0, external_attr, offset,
        )
        central_chunks.append(central_header + archive_name)
        offset += len(local_record)

    local_blob = b"".join(local_chunks)
    central_blob = b"".join(central_chunks)
    end_record = struct.pack(
        "<IHHHHIIH",
        0x06054B50, 0, 0, len(entries), len(entries),
        len(central_blob), len(local_blob), 0,
    )
    return local_blob + central_blob + end_record


def current_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return None


def load_and_verify() -> tuple[dict, list[tuple[str, bytes]]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("schema") != "prompt-quarry-free-pack-release-v1":
        raise SystemExit("FREE PACK RELEASE: FAIL — unexpected manifest schema")

    expected_paths = [asset["path"] for asset in manifest["assets"]]
    if expected_paths != sorted(expected_paths):
        raise SystemExit("FREE PACK RELEASE: FAIL — asset paths must be lexicographically sorted")
    if len(expected_paths) != 7 or len(set(expected_paths)) != 7:
        raise SystemExit("FREE PACK RELEASE: FAIL — expected exactly 7 unique customer-visible assets")

    entries: list[tuple[str, bytes]] = []
    for asset in manifest["assets"]:
        path = asset["path"]
        source = PACK_ROOT / path
        if not source.is_file():
            raise SystemExit(f"FREE PACK RELEASE: FAIL — missing asset: {path}")
        data = source.read_bytes()
        if len(data) != asset["size_bytes"]:
            raise SystemExit(f"FREE PACK RELEASE: FAIL — size mismatch: {path}")
        if git_blob_sha1(data) != asset["git_blob_sha1"]:
            raise SystemExit(f"FREE PACK RELEASE: FAIL — git blob mismatch: {path}")
        if "sha256:" + sha256(data) != asset["sha256"]:
            raise SystemExit(f"FREE PACK RELEASE: FAIL — sha256 mismatch: {path}")
        entries.append((path, data))

    archive = build_stored_zip(entries)
    archive_meta = manifest["archive"]
    if len(archive) != archive_meta["size_bytes"]:
        raise SystemExit("FREE PACK RELEASE: FAIL — archive size mismatch")
    if "sha256:" + sha256(archive) != archive_meta["archive_sha256"]:
        raise SystemExit("FREE PACK RELEASE: FAIL — archive sha256 mismatch")
    return manifest, entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    manifest, entries = load_and_verify()
    archive = build_stored_zip(entries)

    if not args.verify_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(archive)
        receipt = {
            "schema": "prompt-quarry-free-pack-release-receipt-v1",
            "component": "free-developer-starter-v1",
            "status": "PASS",
            "version": manifest["version"],
            "payload_source_commit": manifest["payload_source_commit"],
            "payload_source_tree": manifest["payload_source_tree"],
            "build_commit": current_commit(),
            "included_assets": len(entries),
            "archive": {
                "filename": manifest["archive"]["filename"],
                "size_bytes": len(archive),
                "archive_sha256": "sha256:" + sha256(archive),
                "format": manifest["archive"]["format"],
            },
            "delivery_state": manifest["delivery_state"],
            "claims_boundary": manifest["claims_boundary"],
        }
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("FREE DEVELOPER STARTER V1: PASS")
    print(f"included_assets={len(entries)}")
    print(f"archive_size={len(archive)}")
    print(f"archive_sha256=sha256:{sha256(archive)}")
    print("boundary=artifact READY; delivery remains separate from deployment/live availability")


if __name__ == "__main__":
    main()
