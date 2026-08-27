from __future__ import annotations

import json
from pathlib import Path

from mk1_f5_benchmark import find_fixture_set, load
from mk1_f7_portable import build_portability_receipt, promote_portable, validate_portability_receipt_integrity, validate_portability_inventory
from mk1_materialize_f7_portable import index_certified, supplemental_receipts
from mk1_prompt_linter import lint_artifact


SOURCE = Path("mk1/candidates/f6")
EVIDENCE = Path("mk1/receipts/f7")
OUTPUT = Path("mk1/candidates/f7")
FIXTURES = Path("mk1/fixtures/f4/fixture-sets.json")


def index_portable(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    if not root.exists():
        return index
    for artifact_path in sorted(root.glob("*/artifact.json")):
        artifact = load(artifact_path)
        artifact_id = artifact["id"]
        if artifact_id in index:
            raise AssertionError(f"Duplicate F7 artifact id: {artifact_id}")
        index[artifact_id] = artifact_path.parent
    return index


def main() -> None:
    certified_index = index_certified(SOURCE)
    supplements = supplemental_receipts(EVIDENCE)
    fixture_document = load(FIXTURES)
    persisted = index_portable(OUTPUT)

    unknown = sorted({row.get("artifact_id") for row in supplements if row.get("artifact_id") not in certified_index})
    if unknown:
        raise AssertionError(f"F7 evidence has no F6 certified source: {unknown}")

    expected: dict[str, tuple[dict, dict, list[dict]]] = {}
    pending: dict[str, dict] = {}
    for artifact_id, source_bundle in sorted(certified_index.items()):
        certified = load(source_bundle / "artifact.json")
        certification_receipt = load(source_bundle / "certification_receipt.json")
        source_candidate = load(source_bundle / "source_candidate_artifact.json")
        source_tested = load(source_bundle / "source_tested_artifact.json")
        baseline = load(source_bundle / "baseline.json")
        f6_evidence = load(source_bundle / "certification_f5_receipts.json").get("receipts") or []
        fixture_set = find_fixture_set(fixture_document, artifact_id)
        evidence = f6_evidence + [row for row in supplements if row.get("artifact_id") == artifact_id]
        inventory = validate_portability_inventory(evidence)
        if inventory["runtime_provider_count"] < 3 or inventory["runtime_family_count"] < 3:
            pending[artifact_id] = inventory
            continue
        receipt = build_portability_receipt(certified, certification_receipt, source_candidate, source_tested, baseline, fixture_set, evidence)
        expected[artifact_id] = (promote_portable(certified, receipt), receipt, evidence)

    if set(persisted) != set(expected):
        raise AssertionError(f"F7 persisted inventory mismatch: persisted={sorted(persisted)} expected={sorted(expected)}")

    manifest_path = OUTPUT / "manifest.json"
    if not manifest_path.exists():
        raise AssertionError("Missing F7 manifest")
    manifest = load(manifest_path)
    expected_status = "PORTABLE_ARTIFACTS_MATERIALIZED" if expected else ("PENDING_PORTABILITY_EVIDENCE" if certified_index else "NO_F6_CERTIFIED_ARTIFACTS")
    if manifest.get("status") != expected_status:
        raise AssertionError(f"F7 manifest status mismatch: expected {expected_status}, got {manifest.get('status')}")
    if manifest.get("portable_count") != len(expected) or manifest.get("pending_count") != len(pending):
        raise AssertionError("F7 manifest counts mismatch")
    if manifest.get("minimum_runtime_providers") != 3 or manifest.get("minimum_runtime_families") != 3:
        raise AssertionError("F7 portability diversity policy drifted")

    for artifact_id, (reconstructed, receipt, evidence) in expected.items():
        bundle = persisted[artifact_id]
        observed = load(bundle / "artifact.json")
        if observed != reconstructed:
            raise AssertionError(f"F7 PORTABLE artifact cannot be deterministically reconstructed: {artifact_id}")
        persisted_receipt = load(bundle / "portability_receipt.json")
        validate_portability_receipt_integrity(persisted_receipt)
        if persisted_receipt != receipt:
            raise AssertionError(f"F7 portability receipt cannot be deterministically reconstructed: {artifact_id}")
        evidence_doc = load(bundle / "cross_provider_f5_receipts.json")
        if evidence_doc.get("receipts") != evidence:
            raise AssertionError(f"F7 persisted F5 evidence inventory mismatch: {artifact_id}")
        if observed.get("state") != "PORTABLE" or observed.get("claims") != ["engineered", "tested", "improved", "certified", "portable"]:
            raise AssertionError(f"F7 portable state/claims invalid: {artifact_id}")
        lint = lint_artifact(observed)
        if lint.get("status") != "PASS":
            raise AssertionError(f"F7 portable artifact fails linter: {artifact_id}: {lint}")

    print(json.dumps({
        "mk1_f7_repository": "PASS",
        "f6_certified": len(certified_index),
        "portable": len(expected),
        "pending": len(pending),
        "state": expected_status,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
