from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from validate_product_manifest import validate

CANDIDATE = Path("product/developer-pack-v1/MANIFEST.release-candidate.json")
APPROVAL_SCHEMA = Path("product/specs/DISTRIBUTION_APPROVAL.schema.json")
DEFAULT_APPROVAL = Path(".approvals/developer-pack-v1/DISTRIBUTION_APPROVAL.json")
READY_MANIFEST = Path("product/developer-pack-v1/MANIFEST.ready.json")
READY_RECEIPT = Path(".ci/developer-pack-v1/ready-promotion.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def projection_sha256(manifest: dict) -> str:
    value = copy.deepcopy(manifest)
    value.setdefault("release", {}).pop("manifest_sha256", None)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--approval", type=Path, default=DEFAULT_APPROVAL)
    parser.add_argument("--output", type=Path, default=READY_MANIFEST)
    args = parser.parse_args()

    if not CANDIDATE.is_file():
        raise SystemExit("release candidate manifest is missing")
    if not args.approval.is_file():
        raise SystemExit("explicit distribution approval is missing; READY promotion is blocked")

    approval = load(args.approval)
    schema = load(APPROVAL_SCHEMA)
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(approval), key=lambda e: list(e.absolute_path))
    if errors:
        raise SystemExit("distribution approval is invalid:\n- " + "\n- ".join(e.message for e in errors))

    candidate = load(CANDIDATE)
    if approval["candidate_source_commit"] != candidate.get("source_commit"):
        raise SystemExit("approval does not bind the current release candidate source_commit")

    ready = copy.deepcopy(candidate)
    ready["version"] = "1.0.0"
    ready["release_status"] = "READY"
    ready.setdefault("release", {})["distribution_license"] = approval["distribution_license"]
    ready["release"]["manifest_sha256"] = projection_sha256(ready)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(ready, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_errors = validate(args.output, Path("."))
    if manifest_errors:
        args.output.unlink(missing_ok=True)
        raise SystemExit("READY manifest failed product validation:\n- " + "\n- ".join(manifest_errors))

    receipt = {
        "schema": "prompt-quarry-ready-promotion-receipt-v1",
        "component": "developer-pack-v1",
        "status": "PASS",
        "release_status": "READY",
        "candidate_source_commit": ready["source_commit"],
        "distribution_license": approval["distribution_license"],
        "approval_ref": args.approval.as_posix(),
        "ready_manifest": args.output.as_posix(),
        "manifest_projection_sha256": ready["release"]["manifest_sha256"],
        "claim_boundary": "READY is a commercial packaging state only; it does not establish F4 TESTED, F5 IMPROVED, F6 CERTIFIED, or F7 PORTABLE."
    }
    READY_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    READY_RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
