from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from mk1_f5_benchmark import find_fixture_set, load
from mk1_f7_portable import (
    MIN_RUNTIME_FAMILIES,
    MIN_RUNTIME_PROVIDERS,
    build_portability_receipt,
    promote_portable,
    validate_portability_inventory,
)


FIXTURES = Path("mk1/fixtures/f4/fixture-sets.json")


def index_certified(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    if not root.exists():
        return index
    for artifact_path in sorted(root.glob("*/artifact.json")):
        artifact = load(artifact_path)
        if artifact.get("state") != "CERTIFIED":
            raise ValueError(f"F7 source must be CERTIFIED: {artifact_path}")
        artifact_id = artifact["id"]
        if artifact_id in index:
            raise ValueError(f"Duplicate F6 certified id: {artifact_id}")
        index[artifact_id] = artifact_path.parent
    return index


def supplemental_receipts(root: Path) -> list[dict]:
    if not root.exists():
        return []
    return [load(path) for path in sorted(root.rglob("*.receipt.json"))]


def copy_if_exists(source: Path, target: Path) -> None:
    if source.exists():
        shutil.copy2(source, target)


def materialize(source_root: Path, evidence_root: Path, output_root: Path, fixtures_path: Path = FIXTURES, require_at_least: int = 0) -> dict:
    certified_index = index_certified(source_root)
    supplements = supplemental_receipts(evidence_root)
    fixture_document = load(fixtures_path)

    unknown = sorted({row.get("artifact_id") for row in supplements if row.get("artifact_id") not in certified_index})
    if unknown:
        raise ValueError(f"F7 supplemental receipt has no F6 CERTIFIED source: {unknown}")

    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    portable_rows: list[dict] = []
    pending_rows: list[dict] = []

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

        if inventory["runtime_provider_count"] < MIN_RUNTIME_PROVIDERS or inventory["runtime_family_count"] < MIN_RUNTIME_FAMILIES:
            pending_rows.append({
                "artifact_id": artifact_id,
                "artifact_version": certified["version"],
                "state": certified["state"],
                "runtime_provider_count": inventory["runtime_provider_count"],
                "runtime_family_count": inventory["runtime_family_count"],
                "required_runtime_providers": MIN_RUNTIME_PROVIDERS,
                "required_runtime_families": MIN_RUNTIME_FAMILIES,
                "runtime_providers": inventory["runtime_providers"],
                "runtime_families": inventory["runtime_families"],
                "source_bundle": source_bundle.as_posix(),
            })
            continue

        portability_receipt = build_portability_receipt(
            certified, certification_receipt, source_candidate, source_tested, baseline, fixture_set, evidence
        )
        portable = promote_portable(certified, portability_receipt)
        slug = source_bundle.name
        bundle = output_root / slug
        bundle.mkdir(parents=True, exist_ok=True)
        (bundle / "artifact.json").write_text(json.dumps(portable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "portability_receipt.json").write_text(json.dumps(portability_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "cross_provider_f5_receipts.json").write_text(json.dumps({"receipts": evidence}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source_certified_artifact.json").write_text(json.dumps(certified, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source_f6_certification_receipt.json").write_text(json.dumps(certification_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source_candidate_artifact.json").write_text(json.dumps(source_candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source_tested_artifact.json").write_text(json.dumps(source_tested, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source.json").write_text(json.dumps({
            "source_f6_bundle": source_bundle.as_posix(),
            "supplemental_cross_provider_evidence_root": evidence_root.as_posix(),
            "state_transition": "CERTIFIED -> PORTABLE",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for name in ("prompt.txt", "architecture.json", "lint.json", "critic.json", "behavioral_receipt.json", "benchmark_receipt.json"):
            copy_if_exists(source_bundle / name, bundle / name)

        portable_rows.append({
            "artifact_id": artifact_id,
            "artifact_version": portable["version"],
            "state": portable["state"],
            "receipt_id": portability_receipt["receipt_id"],
            "runtime_provider_count": portability_receipt["runtime_provider_count"],
            "runtime_family_count": portability_receipt["runtime_family_count"],
            "runtime_providers": portability_receipt["runtime_providers"],
            "runtime_families": portability_receipt["runtime_families"],
            "portable_at": portability_receipt["portable_at"],
            "bundle": bundle.as_posix(),
        })

    if len(portable_rows) < require_at_least:
        raise SystemExit(f"Expected at least {require_at_least} F7 portable artifacts, got {len(portable_rows)}")

    status = "PORTABLE_ARTIFACTS_MATERIALIZED" if portable_rows else ("PENDING_PORTABILITY_EVIDENCE" if certified_index else "NO_F6_CERTIFIED_ARTIFACTS")
    manifest = {
        "mk_stage": "MK1",
        "phase": "F7",
        "status": status,
        "portable_count": len(portable_rows),
        "pending_count": len(pending_rows),
        "artifacts": portable_rows,
        "pending": pending_rows,
        "minimum_runtime_providers": MIN_RUNTIME_PROVIDERS,
        "minimum_runtime_families": MIN_RUNTIME_FAMILIES,
        "state_policy": "PORTABLE is optional and may only descend from exact F6 CERTIFIED artifacts with valid cross-provider F5 evidence.",
        "claim_policy": "PORTABLE is cross-provider evidence, not a prerequisite for CERTIFIED and not a universal compatibility claim.",
    }
    (output_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="mk1/candidates/f6")
    parser.add_argument("--evidence", default="mk1/receipts/f7")
    parser.add_argument("--fixtures", default=FIXTURES.as_posix())
    parser.add_argument("--output", default="mk1/candidates/f7")
    parser.add_argument("--require-at-least", type=int, default=0)
    args = parser.parse_args()
    result = materialize(Path(args.source), Path(args.evidence), Path(args.output), Path(args.fixtures), args.require_at_least)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
