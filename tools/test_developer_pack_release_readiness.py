from __future__ import annotations

import json
from pathlib import Path

MANIFEST = Path("product/developer-pack-v1/MANIFEST.draft.json")
STATIC_RECEIPT = Path(".ci/developer-pack-v1/latest.json")
REQUIRED_RELEASE_FIELDS = {
    "archive_sha256",
    "manifest_sha256",
    "clean_room_receipt",
    "claims_review_receipt",
    "distribution_license",
}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blockers: list[str] = []

    if manifest.get("release_status") not in {"DRAFT", "READY"}:
        blockers.append("release_status must be DRAFT or READY for readiness evaluation")

    included = [a for a in manifest.get("artifacts", []) if a.get("distribution", {}).get("include")]
    non_valid = [a.get("artifact_id") for a in included if a.get("maturity_state") != "VALID"]
    if non_valid:
        blockers.append("all included assets must be statically VALID before READY: " + ", ".join(non_valid))

    if not STATIC_RECEIPT.is_file():
        blockers.append("canonical Developer Pack static receipt is missing")
    else:
        receipt = json.loads(STATIC_RECEIPT.read_text(encoding="utf-8"))
        if receipt.get("status") != "PASS":
            blockers.append("canonical Developer Pack static receipt is not PASS")
        gates = receipt.get("gates", {})
        if gates.get("clean_room_manifest_export") != "success":
            blockers.append("clean-room manifest export gate is not success")

    source_commit = manifest.get("source_commit")
    if not isinstance(source_commit, str) or len(source_commit) != 40:
        blockers.append("source_commit must bind READY to an exact 40-char commit")
    if not manifest.get("generated_at"):
        blockers.append("generated_at is required for READY")
    if not manifest.get("pack_root"):
        blockers.append("pack_root is required for READY")

    release = manifest.get("release") or {}
    for field in sorted(REQUIRED_RELEASE_FIELDS):
        if not release.get(field):
            blockers.append(f"release.{field} is required before READY")

    # Explicit epistemic boundary: release readiness must never depend on F4-F7 promotion.
    forbidden_release_claims = {"tested", "improved", "certified", "portable"}
    overclaims = []
    for artifact in included:
        bad = forbidden_release_claims.intersection(artifact.get("claims", []))
        if bad:
            overclaims.append(f"{artifact.get('artifact_id')}:{','.join(sorted(bad))}")
    if overclaims:
        blockers.append("READY gate forbids unsupported F4-F7 claims: " + "; ".join(overclaims))

    result = {
        "schema": "prompt-quarry-release-readiness-v1",
        "component": "developer-pack-v1",
        "status": "PASS" if not blockers else "BLOCKED",
        "included_assets": len(included),
        "blockers": blockers,
        "claim_boundary": "READY is a packaging and commercial release-readiness state. It does not establish TESTED/F4, IMPROVED/F5, CERTIFIED/F6, or PORTABLE/F7.",
    }
    print(json.dumps(result, indent=2))
    if blockers:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
