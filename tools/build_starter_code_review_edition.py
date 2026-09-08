#!/usr/bin/env python3
"""Deterministically build Prompt Machine Starter — Code Review Edition v1.

The customer WORKFLOW.md is materialized from the exact v2.1 base + normative
v2.2 addendum composition that earned the scoped G11 certification. The build
fails closed if source blob identities or composite bytes drift.

The final 1.0.0 package keeps operational launch state outside the customer ZIP:
customer files may describe release scope, but must not embed transient internal
flags such as public-checkout or G14 gate state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "product/starter-code-review-edition-v1/MANIFEST.source.json"
ARCHIVE_NAME = "prompt-machine-starter-code-review-edition-v1.0.0.zip"
RECEIPT_NAME = "build-receipt.json"
BUILDER_VERSION = "1.2.0"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def canonical_text_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def compose_workflow(base: str, addendum: str, open_marker: str, close_marker: str) -> bytes:
    text = (
        base.rstrip("\n")
        + "\n\n---\n\n"
        + open_marker
        + "\n"
        + addendum.rstrip("\n")
        + "\n"
        + close_marker
        + "\n"
    )
    return text.encode("utf-8")


def payload_fingerprint(members: dict[str, bytes]) -> str:
    h = hashlib.sha256()
    for name in sorted(members):
        h.update(name.encode("utf-8"))
        h.update(b"\0")
        h.update(members[name])
        h.update(b"\0")
    return h.hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def zip_member(name: str, data: bytes) -> tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(filename=name, date_time=FIXED_ZIP_TIME)
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info, data


def build(out_dir: Path) -> dict:
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    wf = source["workflow"]

    if source.get("version") != "1.0.0":
        raise SystemExit("FAIL: source manifest is not the frozen 1.0.0 artifact")
    if source.get("status") != "FINAL_ARTIFACT_PRE_LIVE_VALIDATION":
        raise SystemExit("FAIL: source manifest operational state is unexpected")
    if source.get("customer_manifest_status") != "CUSTOMER_RELEASE":
        raise SystemExit("FAIL: customer manifest status is unexpected")
    if source.get("customer_license_frozen") is not True:
        raise SystemExit("FAIL: 1.0.0 requires a frozen customer license")

    base_path = ROOT / wf["base_path"]
    addendum_path = ROOT / wf["addendum_path"]
    base_raw = base_path.read_bytes()
    addendum_raw = addendum_path.read_bytes()

    if git_blob_sha(base_raw) != wf["base_github_blob_sha"]:
        raise SystemExit("FAIL: base workflow Git blob identity drift")
    if git_blob_sha(addendum_raw) != wf["addendum_github_blob_sha"]:
        raise SystemExit("FAIL: hardening addendum Git blob identity drift")

    base = base_raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    addendum = addendum_raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    workflow = compose_workflow(base, addendum, wf["open_marker"], wf["close_marker"])

    if len(workflow) != wf["expected_composite_bytes"]:
        raise SystemExit("FAIL: composite workflow byte length drift")
    if sha256(workflow) != wf["expected_composite_sha256"]:
        raise SystemExit("FAIL: composite workflow SHA-256 drift")

    source_to_member = {
        "product/starter-code-review-edition-v1/README.md": "README.md",
        "product/starter-code-review-edition-v1/QUICKSTART.md": "QUICKSTART.md",
        "product/starter-code-review-edition-v1/EVIDENCE.md": "EVIDENCE.md",
        "product/starter-code-review-edition-v1/CUSTOMER-LICENSE.md": "CUSTOMER-LICENSE.md",
        "product/starter-code-review-edition-v1/SALE-TERMS.md": "SALE-TERMS.md",
        "product/starter-code-review-edition-v1/RELEASE-NOTICE.md": "RELEASE-NOTICE.md",
    }

    payload: dict[str, bytes] = {}
    for src in source["customer_source_files"]:
        if src not in source_to_member:
            raise SystemExit(f"FAIL: undeclared customer source mapping: {src}")
        payload[source_to_member[src]] = canonical_text_bytes(ROOT / src)
    payload["WORKFLOW.md"] = workflow

    payload_manifest = {
        "schema": "prompt-machine-starter-code-review-edition-manifest-v1",
        "product": source["commercial_name"],
        "version": source["version"],
        "status": source["customer_manifest_status"],
        "authority": source["authority"],
        "customer_license_frozen": source["customer_license_frozen"],
        "customer_license_version": source["customer_license_version"],
        "sale_terms_version": source["sale_terms_version"],
        "workflow": {
            "workflow_id": wf["workflow_id"],
            "contract_version": wf["contract_version"],
            "bytes": len(workflow),
            "sha256": sha256(workflow),
        },
        "portability_classification": source["portability_classification"],
        "validated_model": source["validated_model"],
        "certification_id": source["certification_id"],
        "payload_fingerprint_sha256": payload_fingerprint(payload),
        "members": {
            name: {"bytes": len(data), "sha256": sha256(data)}
            for name, data in sorted(payload.items())
        },
        "claim_boundary": "MODEL_SPECIFIC_GEMINI_3_5_FLASH_FROZEN_MATRIX_ONLY",
    }
    manifest_bytes = json_bytes(payload_manifest)

    all_members = dict(payload)
    all_members["MANIFEST.json"] = manifest_bytes
    expected_members = source["archive_members"]
    if set(all_members) != set(expected_members) or len(all_members) != len(expected_members):
        raise SystemExit("FAIL: archive membership differs from frozen source manifest")

    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / ARCHIVE_NAME
    with zipfile.ZipFile(
        archive,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as zf:
        for name in expected_members:
            info, data = zip_member(name, all_members[name])
            zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    archive_bytes = archive.read_bytes()
    receipt = {
        "schema": "prompt-machine-starter-code-review-edition-build-receipt-v1",
        "builder_version": BUILDER_VERSION,
        "product": source["commercial_name"],
        "version": source["version"],
        "archive_name": ARCHIVE_NAME,
        "archive_bytes": len(archive_bytes),
        "archive_sha256": sha256(archive_bytes),
        "archive_members": expected_members,
        "archive_member_count": len(expected_members),
        "workflow_bytes": len(workflow),
        "workflow_sha256": sha256(workflow),
        "payload_fingerprint_sha256": payload_manifest["payload_fingerprint_sha256"],
        "source_operational_status": source["status"],
        "public_sale": source["public_sale"],
        "customer_manifest_status": source["customer_manifest_status"],
        "customer_license_frozen": source["customer_license_frozen"],
        "customer_license_version": source["customer_license_version"],
        "sale_terms_version": source["sale_terms_version"],
        "portability_classification": source["portability_classification"],
        "validated_model": source["validated_model"],
        "certification_id": source["certification_id"],
        "deterministic_inputs_only": True,
    }
    (out_dir / RECEIPT_NAME).write_bytes(json_bytes(receipt))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    receipt = build(Path(args.out_dir).resolve())
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
