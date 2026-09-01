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


def apply_normalization(source_path: str, data: bytes, rules: dict[str, tuple[str, str]]) -> tuple[bytes, bool]:
    if source_path not in rules:
        return data, False
    before, after = rules[source_path]
    text = data.decode("utf-8")
    count = text.count(before)
    if count != 1:
        raise SystemExit(f"normalization count mismatch for {source_path}: expected 1, observed {count}")
    normalized = text.replace(before, after, 1).encode("utf-8")
    return normalized, True


def main() -> int:
    manifest = json.loads(INVENTORY.read_text(encoding="utf-8"))
    files = sorted(manifest["files"], key=lambda item: item["archive_path"])
    declared_rules = {
        item["source_path"]: (item["from"], item["to"])
        for item in manifest.get("release_normalization", {}).get("rules", [])
    }

    source_observed = []
    packaged = []
    used_rules: set[str] = set()

    for item in files:
        source_path = PRODUCT / item["source_path"]
        source_bytes = source_path.read_bytes()
        if len(source_bytes) != item["size"]:
            raise SystemExit(f"size mismatch: {item['source_path']}")
        observed_blob = git_blob_sha(source_bytes)
        if observed_blob != item["git_blob_sha"]:
            raise SystemExit(f"git blob mismatch: {item['source_path']}")

        source_observed.append({
            "source_path": item["source_path"],
            "archive_path": item["archive_path"],
            "size": len(source_bytes),
            "git_blob_sha": observed_blob,
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
        })

        packaged_bytes, normalized = apply_normalization(item["source_path"], source_bytes, declared_rules)
        if normalized:
            used_rules.add(item["source_path"])
        packaged.append({
            "source_path": item["source_path"],
            "archive_path": item["archive_path"],
            "data": packaged_bytes,
            "size": len(packaged_bytes),
            "sha256": hashlib.sha256(packaged_bytes).hexdigest(),
            "normalized": normalized,
        })

    unused_rules = sorted(set(declared_rules) - used_rules)
    if unused_rules:
        raise SystemExit(f"unused normalization rules: {','.join(unused_rules)}")

    canonical_source = json.dumps(
        [
            {
                "source_path": x["source_path"],
                "archive_path": x["archive_path"],
                "git_blob_sha": x["git_blob_sha"],
                "size": x["size"],
            }
            for x in source_observed
        ],
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    source_fingerprint = hashlib.sha256(canonical_source).hexdigest()
    if source_fingerprint != manifest["source_fingerprint_sha256"]:
        raise SystemExit("source fingerprint mismatch")

    DIST.mkdir(parents=True, exist_ok=True)
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_STORED, strict_timestamps=True) as zf:
        for item in packaged:
            info = zipfile.ZipInfo(f"{ZIP_ROOT}/{item['archive_path']}", FIXED_DT)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            zf.writestr(info, item["data"])

    archive_bytes = ARCHIVE.read_bytes()
    archive_sha256 = hashlib.sha256(archive_bytes).hexdigest()

    with zipfile.ZipFile(ARCHIVE, "r") as zf:
        members = zf.namelist()
        expected = [f"{ZIP_ROOT}/{item['archive_path']}" for item in packaged]
        if members != expected:
            raise SystemExit("archive member mismatch")
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"zip crc failure: {bad}")
        for member in members:
            body = zf.read(member).decode("utf-8")
            if "`DRAFT`" in body or "DRAFT EXAMPLE" in body or "DRAFT / CUSTOMER-FACING" in body:
                raise SystemExit(f"customer draft marker leaked into archive: {member}")

    receipt = {
        "product": manifest["product"],
        "version": manifest["version"],
        "state": "RELEASE_CANDIDATE",
        "sale_status": "NOT_FOR_SALE",
        "customer_visible_assets": len(packaged),
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
        "source_files": source_observed,
        "packaged_files": [
            {k: v for k, v in item.items() if k != "data"}
            for item in packaged
        ],
        "normalization": {
            "mode": manifest.get("release_normalization", {}).get("mode"),
            "rules_declared": len(declared_rules),
            "rules_applied": len(used_rules),
            "sources": sorted(used_rules),
        },
        "gates": {
            "inventory_exact": True,
            "blob_identity": True,
            "source_fingerprint": True,
            "normalization_exact": len(used_rules) == len(declared_rules),
            "archive_members_exact": True,
            "archive_crc": True,
            "customer_draft_markers_absent": True,
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
    print(json.dumps({
        "archive": str(ARCHIVE),
        "sha256": archive_sha256,
        "size": len(archive_bytes),
        "files": len(packaged),
        "source_fingerprint": source_fingerprint,
        "normalizations": len(used_rules),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
