from __future__ import annotations

import argparse
import json
from pathlib import Path

CANDIDATE = Path("product/developer-pack-v1/MANIFEST.release-candidate.json")
READY_RECEIPT = Path(".ci/developer-pack-v1/release-readiness.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-only-license-blocker", action="store_true")
    args = parser.parse_args()

    manifest = load(CANDIDATE)
    blockers: list[str] = []
    included = [a for a in manifest.get("artifacts", []) if a["distribution"]["include"]]

    if not manifest.get("source_commit") or len(manifest["source_commit"]) != 40:
        blockers.append("source_commit must bind READY to an exact 40-char commit")
    if not manifest.get("generated_at"):
        blockers.append("generated_at is required for READY")
    if not manifest.get("pack_root"):
        blockers.append("pack_root is required for READY")

    release = manifest.get("release", {})
    for field in ("archive_sha256", "manifest_sha256", "claims_review_receipt", "clean_room_receipt"):
        if not release.get(field):
            blockers.append(f"release.{field} is required before READY")
    if not release.get("distribution_license"):
        blockers.append("release.distribution_license requires explicit human/commercial approval")

    if not included:
        blockers.append("at least one included artifact is required")
    if any(a.get("maturity_state") != "VALID" for a in included):
        blockers.append("every included artifact must be VALID before READY")

    for field in ("claims_review_receipt", "clean_room_receipt"):
        ref = release.get(field)
        if ref:
            path = Path(ref)
            if not path.is_file():
                blockers.append(f"release.{field} path does not exist")
            else:
                receipt = load(path)
                if receipt.get("status") != "PASS":
                    blockers.append(f"release.{field} must reference PASS evidence")
                if receipt.get("source_commit") != manifest.get("source_commit"):
                    blockers.append(f"release.{field} source_commit mismatch")

    status = "READY" if not blockers else "BLOCKED"
    receipt = {
        "schema": "prompt-quarry-release-readiness-receipt-v1",
        "component": "developer-pack-v1",
        "source_commit": manifest.get("source_commit"),
        "status": status,
        "included_assets": len(included),
        "blockers": blockers,
        "claim_boundary": "READY is packaging/commercial readiness only. It does not establish F4 TESTED, F5 IMPROVED, F6 CERTIFIED, or F7 PORTABLE.",
    }
    write_json(READY_RECEIPT, receipt)
    print(json.dumps(receipt, indent=2))

    if args.expect_only_license_blocker:
        expected = ["release.distribution_license requires explicit human/commercial approval"]
        if blockers != expected:
            raise SystemExit("READY engineering gate did not converge to the single human blocker")
    elif blockers:
        raise SystemExit("READY gate blocked")


if __name__ == "__main__":
    main()
