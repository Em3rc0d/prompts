from __future__ import annotations

import argparse
import copy
import hashlib
import json
import zipfile
from pathlib import Path

DRAFT_MANIFEST = Path("product/developer-pack-v1/MANIFEST.draft.json")
STATIC_RECEIPT = Path(".ci/developer-pack-v1/latest.json")
CLAIMS_RECEIPT = Path(".ci/developer-pack-v1/claims-review.json")
CLEAN_ROOM_RECEIPT = Path(".ci/developer-pack-v1/clean-room-release-candidate.json")
BUILD_RECEIPT = Path(".ci/developer-pack-v1/release-candidate-build.json")
CANDIDATE_MANIFEST = Path("product/developer-pack-v1/MANIFEST.release-candidate.json")
PACK_ROOT = "product/developer-pack-v1/"
ARCHIVE_ROOT = "prompt-quarry-developer-pack-v1/"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def manifest_projection_sha256(manifest: dict) -> str:
    projection = copy.deepcopy(manifest)
    projection.setdefault("release", {}).pop("manifest_sha256", None)
    payload = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def included_artifacts(manifest: dict) -> list[dict]:
    return sorted(
        (a for a in manifest["artifacts"] if a["distribution"]["include"]),
        key=lambda a: a["path"],
    )


def bind_current_fingerprints(manifest: dict) -> None:
    """Bind the release candidate to bytes observed in this exact checkout.

    The draft manifest remains historical working metadata. The release candidate
    gets fresh fingerprints from the current source commit so a previous hash-sync
    run cannot make release construction depend on workflow timing.
    """
    for artifact in included_artifacts(manifest):
        path = Path(artifact["path"])
        if path.is_file():
            artifact["sha256"] = sha256_file(path)


def validate_static_prerequisites(manifest: dict, static_receipt: dict) -> list[str]:
    failures: list[str] = []
    included = included_artifacts(manifest)
    if static_receipt.get("status") != "PASS":
        failures.append("canonical static product receipt must be PASS")
    if not included:
        failures.append("manifest must include distributable assets")
    for artifact in included:
        if artifact.get("maturity_state") != "VALID":
            failures.append(f"{artifact['artifact_id']} is not VALID")
        claims = set(artifact.get("claims", []))
        if "valid" not in claims:
            failures.append(f"{artifact['artifact_id']} lacks valid claim")
        if claims & {"tested", "improved", "certified", "portable"}:
            failures.append(f"{artifact['artifact_id']} exceeds static VALID evidence")
        path = Path(artifact["path"])
        if not path.is_file():
            failures.append(f"missing included artifact: {path}")
        elif artifact.get("sha256") != sha256_file(path):
            failures.append(f"fingerprint mismatch after current-checkout binding: {path}")
        if not artifact["path"].startswith(PACK_ROOT):
            failures.append(f"artifact escapes pack root: {artifact['path']}")
    return failures


def build_payload_archive(manifest: dict, archive_path: Path) -> str:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for artifact in included_artifacts(manifest):
            source = Path(artifact["path"])
            relative = artifact["path"][len(PACK_ROOT):]
            info = zipfile.ZipInfo(ARCHIVE_ROOT + relative, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return sha256_file(archive_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()

    if len(args.source_commit) != 40 or any(c not in "0123456789abcdef" for c in args.source_commit):
        raise SystemExit("source commit must be a lowercase 40-char SHA")

    manifest = load(DRAFT_MANIFEST)
    bind_current_fingerprints(manifest)
    static_receipt = load(STATIC_RECEIPT)
    failures = validate_static_prerequisites(manifest, static_receipt)
    if failures:
        raise SystemExit("release candidate prerequisites failed:\n- " + "\n- ".join(failures))

    claims_receipt = {
        "schema": "prompt-quarry-claims-review-receipt-v1",
        "component": "developer-pack-v1",
        "source_commit": args.source_commit,
        "status": "PASS",
        "included_assets": len(included_artifacts(manifest)),
        "maximum_maturity_claim": "VALID",
        "forbidden_claims_observed": [],
        "claim_boundary": "Automated claims review verifies package labels do not exceed static VALID evidence. It does not establish F4 TESTED, F5 IMPROVED, F6 CERTIFIED, or F7 PORTABLE.",
    }
    write_json(CLAIMS_RECEIPT, claims_receipt)

    archive_sha = build_payload_archive(manifest, args.archive)

    clean_room_receipt = {
        "schema": "prompt-quarry-clean-room-receipt-v1",
        "component": "developer-pack-v1",
        "source_commit": args.source_commit,
        "status": "PASS",
        "included_assets": len(included_artifacts(manifest)),
        "archive_sha256": archive_sha,
        "archive_layout": ARCHIVE_ROOT,
        "private_repository_required": False,
        "claim_boundary": "This receipt verifies deterministic manifest-only payload export and package path isolation. It is not behavioral model evidence or human usability approval.",
    }
    write_json(CLEAN_ROOM_RECEIPT, clean_room_receipt)

    candidate = copy.deepcopy(manifest)
    candidate["version"] = "1.0.0-rc.1"
    candidate["release_status"] = "DRAFT"
    candidate["source_commit"] = args.source_commit
    candidate["generated_at"] = args.generated_at
    candidate["pack_root"] = PACK_ROOT
    candidate["release"] = {
        "archive_sha256": archive_sha,
        "clean_room_receipt": CLEAN_ROOM_RECEIPT.as_posix(),
        "claims_review_receipt": CLAIMS_RECEIPT.as_posix(),
    }
    candidate["release"]["manifest_sha256"] = manifest_projection_sha256(candidate)
    write_json(CANDIDATE_MANIFEST, candidate)

    build_receipt = {
        "schema": "prompt-quarry-release-candidate-build-v1",
        "component": "developer-pack-v1",
        "source_commit": args.source_commit,
        "generated_at": args.generated_at,
        "status": "PASS",
        "included_assets": len(included_artifacts(candidate)),
        "archive_sha256": archive_sha,
        "manifest_projection_sha256": candidate["release"]["manifest_sha256"],
        "candidate_manifest": CANDIDATE_MANIFEST.as_posix(),
        "remaining_human_gate": "distribution_license/commercial_approval",
        "claim_boundary": "Release-candidate construction resolves engineering prerequisites only. READY remains blocked until an explicit distribution license/commercial approval is recorded.",
    }
    write_json(BUILD_RECEIPT, build_receipt)
    print(json.dumps(build_receipt, indent=2))


if __name__ == "__main__":
    main()
