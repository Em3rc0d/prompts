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
STATE_EVIDENCE_PREFIX = {
    "TESTED": "mk1/receipts/f4/",
    "CANDIDATE": "mk1/receipts/f5/",
    "CERTIFIED": "mk1/receipts/f6/",
    "PORTABLE": "mk1/receipts/f7/",
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


def _dependency_cycle(by_id: dict[str, dict]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visited:
            return None
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]

        visiting.add(node)
        stack.append(node)
        for dependency in by_id[node].get("dependencies", []):
            if dependency in by_id:
                cycle = visit(dependency)
                if cycle:
                    return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(by_id):
        cycle = visit(node)
        if cycle:
            return cycle
    return None


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

        required_prefix = STATE_EVIDENCE_PREFIX.get(state)
        if required_prefix and not any(ref.startswith(required_prefix) for ref in artifact["evidence_refs"]):
            errors.append(
                f"artifact[{index}]: {state} requires evidence under {required_prefix}"
            )

        for evidence_ref in artifact["evidence_refs"]:
            evidence_path = repo_root / evidence_ref
            if not evidence_path.is_file():
                errors.append(f"artifact[{index}]: evidence_ref does not exist: {evidence_ref}")

        source_refs = artifact.get("source_refs", [])
        if artifact["provenance_class"] in {"mk0-derived", "mk1-derived"} and not source_refs:
            errors.append(
                f"artifact[{index}]: {artifact['provenance_class']} requires non-empty source_refs"
            )
        for source_ref in source_refs:
            if source_ref.startswith(("http://", "https://")):
                continue
            if not (repo_root / source_ref).exists():
                errors.append(f"artifact[{index}]: source_ref does not exist: {source_ref}")

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

    for index, artifact in enumerate(manifest.get("artifacts", [])):
        for dependency in artifact.get("dependencies", []):
            if dependency not in by_id:
                errors.append(f"artifact[{index}]: unknown dependency {dependency}")
            if dependency == artifact["artifact_id"]:
                errors.append(f"artifact[{index}]: self dependency {dependency}")

    cycle = _dependency_cycle(by_id)
    if cycle:
        errors.append("dependencies: cycle detected: " + " -> ".join(cycle))

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
            if manifest["generator_v0"].get("receipt_status") != receipt.get("status"):
                errors.append("generator_v0: receipt_status does not match canonical receipt")

    if manifest.get("release_status") in {"READY", "RELEASED"}:
        included = [a for a in manifest.get("artifacts", []) if a["distribution"]["include"]]
        if not included:
            errors.append("release: READY/RELEASED requires at least one included artifact")
        if any(a["maturity_state"] == "DRAFT" for a in included):
            errors.append("release: READY/RELEASED cannot include DRAFT artifacts")
        if manifest.get("source_commit") is None:
            errors.append("release: READY/RELEASED requires source_commit")

        pack_root = manifest.get("pack_root")
        if pack_root:
            for artifact in included:
                if not artifact["path"].startswith(pack_root):
                    errors.append(
                        f"release: included artifact escapes pack_root {pack_root}: {artifact['path']}"
                    )

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
