from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from mk1_f5_benchmark import find_baseline, load, promote_improved


def index_tested(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for artifact_path in sorted(root.glob("*/artifact.json")):
        artifact = load(artifact_path)
        if artifact.get("state") != "TESTED":
            raise ValueError(f"F5 source must be TESTED: {artifact_path}")
        artifact_id = artifact["id"]
        if artifact_id in index:
            raise ValueError(f"Duplicate F4 artifact id: {artifact_id}")
        index[artifact_id] = artifact_path.parent
    return index


def copy_if_exists(source: Path, target: Path) -> None:
    if source.exists():
        shutil.copy2(source, target)


def materialize(receipts_root: Path, source_root: Path, baselines_path: Path, output_root: Path, require_at_least: int = 0) -> dict:
    tested = index_tested(source_root)
    baseline_document = load(baselines_path)
    receipt_paths = sorted(receipts_root.glob("*.receipt.json"))

    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    rows = []
    seen_artifacts: set[str] = set()
    for receipt_path in receipt_paths:
        receipt = load(receipt_path)
        artifact_id = receipt.get("artifact_id")
        if artifact_id in seen_artifacts:
            raise ValueError(f"Multiple F5 receipts for the same artifact are not allowed in one materialization: {artifact_id}")
        seen_artifacts.add(artifact_id)
        if artifact_id not in tested:
            raise ValueError(f"No F4 TESTED source found for F5 receipt {receipt_path}: {artifact_id}")

        source_bundle = tested[artifact_id]
        source_artifact = load(source_bundle / "artifact.json")
        candidate = promote_improved(source_artifact, receipt)
        baseline = find_baseline(baseline_document, artifact_id)
        if baseline["baseline_id"] != receipt.get("baseline_id"):
            raise ValueError(f"F5 receipt baseline mismatch for {artifact_id}")

        slug = source_bundle.name
        bundle = output_root / slug
        bundle.mkdir(parents=True, exist_ok=True)
        (bundle / "artifact.json").write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "benchmark_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "baseline.json").write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source_tested_artifact.json").write_text(json.dumps(source_artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (bundle / "source.json").write_text(json.dumps({
            "source_f4_bundle": source_bundle.as_posix(),
            "source_f4_receipt": (source_bundle / "behavioral_receipt.json").as_posix(),
            "source_f5_receipt": receipt_path.as_posix(),
            "baseline_id": baseline["baseline_id"],
            "state_transition": "TESTED -> CANDIDATE",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        for name in ("prompt.txt", "architecture.json", "lint.json", "critic.json", "behavioral_receipt.json"):
            copy_if_exists(source_bundle / name, bundle / name)

        rows.append({
            "artifact_id": artifact_id,
            "artifact_version": candidate["version"],
            "state": candidate["state"],
            "baseline_id": receipt["baseline_id"],
            "fixture_set_id": receipt["fixture_set_id"],
            "receipt_id": receipt["receipt_id"],
            "runtime": receipt["runtime"],
            "rubric_score": receipt["rubric_score"],
            "bundle": bundle.as_posix(),
        })

    if len(rows) < require_at_least:
        raise SystemExit(f"Expected at least {require_at_least} eligible F5 receipts, got {len(rows)}")

    manifest = {
        "mk_stage": "MK1",
        "phase": "F5",
        "status": "IMPROVED_CANDIDATES_MATERIALIZED" if rows else "NO_REAL_RECEIPTS",
        "candidate_count": len(rows),
        "artifacts": rows,
        "source_policy": "Only persisted real IMPROVEMENT_PASS receipts accepted by mk1_f5_benchmark.promote_improved may materialize CANDIDATE artifacts.",
        "claim_policy": "CANDIDATE/improved is scoped to the exact baseline, fixture set and runtime in its F5 receipt. Cross-runtime CERTIFIED remains F6.",
    }
    (output_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipts", default="mk1/receipts/f5")
    parser.add_argument("--source", default="mk1/candidates/f4")
    parser.add_argument("--baselines", default="mk1/baselines/f5/task-equivalent-minimal.json")
    parser.add_argument("--output", default="mk1/candidates/f5")
    parser.add_argument("--require-at-least", type=int, default=0)
    args = parser.parse_args()
    manifest = materialize(Path(args.receipts), Path(args.source), Path(args.baselines), Path(args.output), args.require_at_least)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
