from __future__ import annotations

import json
from pathlib import Path

from mk1_f5_benchmark import find_fixture_set, load
from mk1_f6_certify import build_certification_receipt, promote_certified, validate_certification_receipt_integrity, validate_cross_runtime_f5_receipt
from mk1_materialize_f6_certified import index_candidates, supplemental_receipts, validate_evidence_inventory
from mk1_prompt_linter import lint_artifact


SOURCE = Path("mk1/candidates/f5")
EVIDENCE = Path("mk1/receipts/f6")
OUTPUT = Path("mk1/candidates/f6")
FIXTURES = Path("mk1/fixtures/f4/fixture-sets.json")


def index_certified(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    if not root.exists():
        return index
    for artifact_path in sorted(root.glob("*/artifact.json")):
        artifact = load(artifact_path)
        artifact_id = artifact["id"]
        if artifact_id in index:
            raise AssertionError(f"Duplicate F6 artifact id: {artifact_id}")
        index[artifact_id] = artifact_path.parent
    return index


def main() -> None:
    candidates = index_candidates(SOURCE) if SOURCE.exists() else {}
    supplements = supplemental_receipts(EVIDENCE)
    fixture_document = load(FIXTURES)
    persisted = index_certified(OUTPUT)

    unknown = sorted({row.get("artifact_id") for row in supplements if row.get("artifact_id") not in candidates})
    if unknown:
        raise AssertionError(f"F6 evidence has no F5 candidate source: {unknown}")

    expected: dict[str, tuple[dict, dict, list[dict]]] = {}
    pending: dict[str, list[str]] = {}
    for artifact_id, source_bundle in sorted(candidates.items()):
        candidate = load(source_bundle / "artifact.json")
        source_tested = load(source_bundle / "source_tested_artifact.json")
        baseline = load(source_bundle / "baseline.json")
        primary = load(source_bundle / "benchmark_receipt.json")
        fixture_set = find_fixture_set(fixture_document, artifact_id)
        evidence = [primary] + [row for row in supplements if row.get("artifact_id") == artifact_id]
        for receipt in evidence:
            validate_cross_runtime_f5_receipt(receipt, candidate, source_tested, baseline, fixture_set)
        families = validate_evidence_inventory(evidence)
        if primary.get("receipt_id") != (candidate.get("evaluation") or {}).get("receipt_id"):
            raise AssertionError(f"F6 primary F5 receipt mismatch: {artifact_id}")
        if len(families) < 3:
            pending[artifact_id] = families
            continue
        certification = build_certification_receipt(candidate, source_tested, baseline, fixture_set, evidence)
        expected[artifact_id] = (promote_certified(candidate, certification), certification, evidence)

    if set(persisted) != set(expected):
        raise AssertionError(f"F6 persisted inventory mismatch: persisted={sorted(persisted)} expected={sorted(expected)}")

    manifest_path = OUTPUT / "manifest.json"
    if not manifest_path.exists():
        raise AssertionError("Missing F6 manifest")
    manifest = load(manifest_path)
    expected_status = "CERTIFIED_ARTIFACTS_MATERIALIZED" if expected else ("PENDING_RUNTIME_EVIDENCE" if candidates else "NO_F5_CANDIDATES")
    if manifest.get("status") != expected_status:
        raise AssertionError(f"F6 manifest status mismatch: expected {expected_status}, got {manifest.get('status')}")
    if manifest.get("certified_count") != len(expected) or manifest.get("pending_count") != len(pending):
        raise AssertionError("F6 manifest counts mismatch")
    if manifest.get("minimum_runtime_families") != 3:
        raise AssertionError("F6 manifest minimum runtime-family policy drifted")

    for artifact_id, (reconstructed, certification, evidence) in expected.items():
        bundle = persisted[artifact_id]
        observed = load(bundle / "artifact.json")
        if observed != reconstructed:
            raise AssertionError(f"F6 CERTIFIED artifact cannot be deterministically reconstructed: {artifact_id}")
        persisted_receipt = load(bundle / "certification_receipt.json")
        validate_certification_receipt_integrity(persisted_receipt)
        if persisted_receipt != certification:
            raise AssertionError(f"F6 certification receipt cannot be deterministically reconstructed: {artifact_id}")
        evidence_doc = load(bundle / "cross_runtime_f5_receipts.json")
        if evidence_doc.get("receipts") != evidence:
            raise AssertionError(f"F6 persisted F5 evidence inventory mismatch: {artifact_id}")
        if observed.get("state") != "CERTIFIED" or observed.get("claims") != ["engineered", "tested", "improved", "certified"]:
            raise AssertionError(f"F6 certified state/claims invalid: {artifact_id}")
        lint = lint_artifact(observed)
        if lint.get("status") != "PASS":
            raise AssertionError(f"F6 certified artifact fails linter: {artifact_id}: {lint}")

    print(json.dumps({
        "mk1_f6_repository": "PASS",
        "f5_candidates": len(candidates),
        "certified": len(expected),
        "pending": len(pending),
        "state": expected_status,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
