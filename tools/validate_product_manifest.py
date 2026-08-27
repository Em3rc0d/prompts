from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_PATH = Path("product/specs/PRODUCT_MANIFEST.schema.json")
FORBIDDEN_PREFIXES = (
    ".git/",
    ".github/",
    ".ci/",
    "quarry/raw/",
    "sources/",
)
STATE_RANK = {
    "DRAFT": 0,
    "VALID": 1,
    "TESTED": 2,
    "CANDIDATE": 3,
    "CERTIFIED": 4,
    "PORTABLE": 5,
}
CLAIM_MIN_STATE = {
    "engineered": "DRAFT",
    "valid": "VALID",
    "tested": "TESTED",
    "improved": "CANDIDATE",
    "certified": "CERTIFIED",
    "portable": "PORTABLE",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def schema_errors(manifest: dict) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(manifest), key=lambda e: list(e.absolute_path)):
        where = ".".join(str(x) for x in error.absolute_path) or "<root>"
        errors.append(f"schema:{where}: {error.message}")
    return errors


def semantic_errors(manifest: dict, repo_root: Path) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    paths: set[str] = set()
    by_id: dict[str, dict] = {}

    for index, artifact in enumerate(manifest.get("artifacts", [])):
        aid = artifact["artifact_id"]
        path = artifact["path"]

        if aid in ids:
            errors.append(f"artifact[{index}]: duplicate artifact_id {aid}")
        ids.add(aid)
        by_id[aid] = artifact

        if path in paths:
            errors.append(f"artifact[{index}]: duplicate path {path}")
        paths.add(path)

        normalized = path.replace("\\", "/")
        if normalized.startswith(FORBIDDEN_PREFIXES):
            errors.append(f"artifact[{index}]: forbidden internal path {path}")

        state = artifact["maturity_state"]
        for claim in artifact["claims"]:
            required = CLAIM_MIN_STATE[claim]
            if STATE_RANK[state] < STATE_RANK[required]:
                errors.append(
                    f"artifact[{index}]: claim {claim} requires >= {required}, got {state}"
                )

        if artifact["distribution"]["include"]:
            absolute = repo_root / path
            if not absolute.is_file():
                errors.append(f"artifact[{index}]: included path does not exist: {path}")
            else:
                observed = sha256(absolute)
                if artifact["sha256"] != observed:
                    errors.append(
                        f"artifact[{index}]: sha256 mismatch for {path}: manifest={artifact['sha256']} observed={observed}"
                    )

        if artifact["provenance_class"] in {"mk0-derived", "mk1-derived"} and not artifact.get("source_refs"):
            errors.append(
                f"artifact[{index}]: {artifact['provenance_class']} requires non-empty source_refs"
            )

    for index, artifact in enumerate(manifest.get("artifacts", [])):
        for dependency in artifact.get("dependencies", []):
            if dependency not in by_id:
                errors.append(f"artifact[{index}]: unknown dependency {dependency}")
            if dependency == artifact["artifact_id"]:
                errors.append(f"artifact[{index}]: self dependency {dependency}")

    if manifest.get("generator_v0", {}).get("bundled"):
        receipt_path = repo_root / manifest["generator_v0"]["canonical_receipt"]
        if not receipt_path.is_file():
            errors.append("generator_v0: canonical receipt missing")
        else:
            receipt = load_json(receipt_path)
            if receipt.get("status") != "PASS":
                errors.append("generator_v0: bundled while canonical receipt is not PASS")
            if receipt.get("source_commit") != manifest["generator_v0"].get("receipt_source_commit"):
                errors.append("generator_v0: receipt_source_commit does not match canonical receipt")

    if manifest.get("release_status") in {"READY", "RELEASED"}:
        included = [a for a in manifest.get("artifacts", []) if a["distribution"]["include"]]
        if not included:
            errors.append("release: READY/RELEASED requires at least one included artifact")
        if any(a["maturity_state"] == "DRAFT" for a in included):
            errors.append("release: READY/RELEASED cannot include DRAFT artifacts")
        if manifest.get("source_commit") is None:
            errors.append("release: READY/RELEASED requires source_commit")

    return errors


def validate(path: Path, repo_root: Path) -> list[str]:
    manifest = load_json(path)
    errors = schema_errors(manifest)
    if not errors:
        errors.extend(semantic_errors(manifest, repo_root))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Prompt Quarry product manifest")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()

    errors = validate(args.manifest, args.repo_root)
    if errors:
        print("PRODUCT MANIFEST: FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("PRODUCT MANIFEST: PASS")


if __name__ == "__main__":
    main()
