from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from mk1_f5_benchmark import find_fixture_set, load
from mk1_f6_certify import (
    MIN_RUNTIME_FAMILIES,
    build_certification_receipt,
    promote_certified,
    validate_cross_runtime_f5_receipt,
)


FIXTURES = Path("mk1/fixtures/f4/fixture-sets.json")


def index_candidates(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for artifact_path in sorted(root.glob("*/artifact.json")):
        artifact = load(artifact_path)
        if artifact.get("state") != "CANDIDATE":
            raise ValueError(f"F6 source must be CANDIDATE: {artifact_path}")
        artifact_id = artifact["id"]
        if artifact_id in index:
            raise ValueError(f"Duplicate F5 candidate id: {artifact_id}")
        index[artifact_id] = artifact_path.parent
    return index


def supplemental_receipts(root: Path) -> list[dict]:
    if not root.exists():
        return []
    return [load(path) for path in sorted(root.rglob("*.receipt.json"))]


def validate_evidence_inventory(receipts: list[dict]) -> list[str]:
    receipt_ids: set[str] = set()
    execution_ids: set[str] = set()
    randomization_refs: set[str] = set()
    families: dict[str, str] = {}
    for receipt in receipts:
        receipt_id = receipt.get("receipt_id")
        execution_id = receipt.get("execution_id")
        review = receipt.get("review") or {}
        randomization_ref = review.get("randomization_ref")
        family = str((receipt.get("runtime") or {}).get("family", "")).strip()
        normalized = family.casefold()
        if receipt_id in receipt_ids:
            raise ValueError(f"Duplicate F6 evidence receipt_id: {receipt_id}")
        if execution_id in execution_ids:
            raise ValueError(f"Duplicate F6 evidence execution_id: {execution_id}")
        if randomization_ref in randomization_refs:
            raise ValueError(f"Duplicate F6 blind randomization_ref: {randomization_ref}")
        if normalized in families:
            raise ValueError(f"Duplicate F6 runtime family: {family!r} conflicts with {families[normalized]!r}")
        receipt_ids.add(receipt_id)
        execution_ids.add(execution_id)
        randomization_refs.add(randomization_ref)
        families[normalized] = family
    return sorted(families.values())


def copy_if_exists(source: Path, target: Path) -> None:
    if source.exists():
        shutil.copy2(source, target)


def materialize(
    source_root: Path,
    evidence_root: Path,
    output_root: Path,
    fixtures_path: Path = FIXTURES,
    require_at_least: int = 0,
) -> dict:
    candidates = index_candidates(source_root) if source_root.exists() else {}
    fixture_document = load(fixtures_path)
    supplements = supplemental_receipts(evidence_root)

    unknown = sorted({row.get("artifact_id") for row in supplements if row.get("artifact_id") not in candidates})
    if unknown:
        raise ValueError(f"F6 supplemental receipt has no F5 CANDIDATE source: {unknown}")

    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    certified_rows: list[dict] = []
    pending_rows: list[dict] = []

    for artifact_id, source_bundle in sorted(candidates.items()):
        candidate = load(source_bundle / "artifact.json")
        source_tested = load(source_bundle / "source_tested_artifact.json")
        baseline = load(source_bundle / "baseline.json")
        primary_receipt = load(source_bundle / "benchmark_receipt.json")
        fixture_set = find_fixture_set(fixture_document, artifact_id)

        evidence = [primary_receipt] + [row for row in supplements if row.get("artifact_id") == artifact_id]
        for receipt in evidence:
            validate_cross_runtime_f5_receipt(receipt, candidate, source_tested, baseline, fixture_set)
        families = validate_evidence_inventory(evidence)
        if primary_receipt.get("receipt_id") != (candidate.get("evaluation") or {}).get("receipt_id"):
            raise ValueError(f"F6 candidate bundle primary F5 receipt mismatch: {artifact_id}")

        if len(families) < MIN_RUNTIME_FAMILIES:
            pending_rows.append({
                "artifact_id": artifact_id,
                "artifact_version": candidate["version"],
                "state": candidate["state"],
                "runtime_family_count": len(families),
                "runtime_families": families,
                "required_runtime_families": MIN_RUNTIME_FAMILIES,
                "missing_runtime_families": MIN_RUNTIME_FAMILIES - len(families),
                "source_bundle": source_bundle.as_posix(),
            })
            continue

        certification_receipt = build_certification_receipt(candidate, source_tested, baseline, fixture_set, evidence)
        certified = promote_certified(candidate, certification_receipt)
        slug = source_bundle.name
        bundle = output_root / slug
        bundle.mkdir(parents=True, exist_ok=True)
        (bundle / "artifact.json").write_text(json.dumps(certified, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "certification_receipt.json").write_text(json.dumps(certification_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "cross_runtime_f5_receipts.json").write_text(json.dumps({"receipts": evidence}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source_candidate_artifact.json").write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source_tested_artifact.json").write_text(json.dumps(source_tested, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source.json").write_text(json.dumps({
            "source_f5_bundle": source_bundle.as_posix(),
            "primary_f5_receipt": (source_bundle / "benchmark_receipt.json").as_posix(),
            "supplemental_f5_evidence_root": evidence_root.as_posix(),
            "state_transition": "CANDIDATE -> CERTIFIED",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for name in ("prompt.txt", "architecture.json", "lint.json", "critic.json", "behavioral_receipt.json", "benchmark_receipt.json"):
            copy_if_exists(source_bundle / name, bundle / name)

        certified_rows.append({
            "artifact_id": artifact_id,
            "artifact_version": certified["version"],
            "state": certified["state"],
            "receipt_id": certification_receipt["receipt_id"],
            "runtime_family_count": certification_receipt["runtime_family_count"],
            "runtime_families": certification_receipt["runtime_families"],
            "certified_at": certification_receipt["certified_at"],
            "bundle": bundle.as_posix(),
        })

    if len(certified_rows) < require_at_least:
        raise SystemExit(f"Expected at least {require_at_least} F6 certified artifacts, got {len(certified_rows)}")

    if certified_rows:
        status = "CERTIFIED_ARTIFACTS_MATERIALIZED"
    elif candidates:
        status = "PENDING_RUNTIME_EVIDENCE"
    else:
        status = "NO_F5_CANDIDATES"

    manifest = {
        "mk_stage": "MK1",
        "phase": "F6",
        "status": status,
        "certified_count": len(certified_rows),
        "pending_count": len(pending_rows),
        "artifacts": certified_rows,
        "pending": pending_rows,
        "minimum_runtime_families": MIN_RUNTIME_FAMILIES,
        "state_policy": "Only exact F5 CANDIDATE artifacts with valid F5 IMPROVEMENT_PASS evidence across at least three distinct declared runtime families may materialize as CERTIFIED.",
        "claim_policy": "CERTIFIED is scoped evidence of cross-runtime behavioral/superiority performance under the frozen protocol; it is not universal correctness.",
    }
    (output_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="mk1/candidates/f5")
    parser.add_argument("--evidence", default="mk1/receipts/f6")
    parser.add_argument("--fixtures", default=FIXTURES.as_posix())
    parser.add_argument("--output", default="mk1/candidates/f6")
    parser.add_argument("--require-at-least", type=int, default=0)
    args = parser.parse_args()
    manifest = materialize(
        Path(args.source),
        Path(args.evidence),
        Path(args.output),
        Path(args.fixtures),
        args.require_at_least,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
