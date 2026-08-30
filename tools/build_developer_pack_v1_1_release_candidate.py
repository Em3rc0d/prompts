#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "product" / "developer-pack-v1.1"
INVENTORY = PRODUCT / "CUSTOMER_INVENTORY.release-candidate.json"
DIST = ROOT / "dist"
ARCHIVE = DIST / "prompt-quarry-developer-pack-v1.1.0.zip"
RECEIPT = ROOT / ".ci" / "developer-pack-v1.1" / "release-candidate.json"
ZIP_ROOT = "prompt-quarry-developer-pack-v1.1.0"
FIXED_DT = (1980, 1, 1, 0, 0, 0)


def git_blob_sha(data: bytes) -> str:
    payload = b"blob " + str(len(data)).encode() + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def main() -> int:
    manifest = json.loads(INVENTORY.read_text(encoding="utf-8"))
    files = sorted(manifest["files"], key=lambda item: item["path"])

    observed = []
    for item in files:
        path = PRODUCT / item["path"]
        data = path.read_bytes()
        if len(data) != item["size"]:
            raise SystemExit(f"size mismatch: {item['path']}")
        if git_blob_sha(data) != item["git_blob_sha"]:
            raise SystemExit(f"git blob mismatch: {item['path']}")
        observed.append({
            "path": item["path"],
            "size": len(data),
            "git_blob_sha": git_blob_sha(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })

    canonical_source = json.dumps(
        [{"path": x["path"], "git_blob_sha": x["git_blob_sha"], "size": x["size"]} for x in observed],
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    source_fingerprint = hashlib.sha256(canonical_source).hexdigest()
    if source_fingerprint != manifest["source_fingerprint_sha256"]:
        raise SystemExit("source fingerprint mismatch")

    DIST.mkdir(parents=True, exist_ok=True)
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_STORED, strict_timestamps=True) as zf:
        for item in observed:
            data = (PRODUCT / item["path"]).read_bytes()
            info = zipfile.ZipInfo(f"{ZIP_ROOT}/{item['path']}", FIXED_DT)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            zf.writestr(info, data)

    archive_bytes = ARCHIVE.read_bytes()
    archive_sha256 = hashlib.sha256(archive_bytes).hexdigest()

    with zipfile.ZipFile(ARCHIVE, "r") as zf:
        members = zf.namelist()
        expected = [f"{ZIP_ROOT}/{item['path']}" for item in observed]
        if members != expected:
            raise SystemExit("archive member mismatch")
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"zip crc failure: {bad}")

    receipt = {
        "product": manifest["product"],
        "version": manifest["version"],
        "state": "RELEASE_CANDIDATE",
        "sale_status": "NOT_FOR_SALE",
        "customer_visible_assets": len(observed),
        "source_fingerprint_sha256": source_fingerprint,
        "archive": {
            "path": str(ARCHIVE.relative_to(ROOT)),
            "size": len(archive_bytes),
            "sha256": archive_sha256,
            "format": "zip-store",
            "root": ZIP_ROOT,
            "timestamp": "1980-01-01T00:00:00",
            "mode": "100644",
        },
        "files": observed,
        "gates": {
            "inventory_exact": True,
            "blob_identity": True,
            "source_fingerprint": True,
            "archive_members_exact": True,
            "archive_crc": True,
            "deterministic_rules": True,
        },
        "evidence_boundary": {
            "static_maturity": "VALID_CANDIDATE",
            "F4_TESTED": False,
            "F5_IMPROVED": False,
            "F6_CERTIFIED": False,
            "F7_PORTABLE": False,
        },
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"archive": str(ARCHIVE), "sha256": archive_sha256, "size": len(archive_bytes), "files": len(observed)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
