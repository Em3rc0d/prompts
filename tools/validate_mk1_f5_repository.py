from __future__ import annotations

import json
import math
from pathlib import Path

from mk1_behavioral_runner import sha256_json, sha256_text
from mk1_f5_benchmark import RUNTIME_IDENTITY_FIELDS, find_baseline, find_fixture_set, load, promote_improved, validate_receipt_integrity


RECEIPTS = Path("mk1/receipts/f5")
SOURCE = Path("mk1/candidates/f4")
OUTPUT = Path("mk1/candidates/f5")
BASELINES = Path("mk1/baselines/f5/task-equivalent-minimal.json")
FIXTURES = Path("mk1/fixtures/f4/fixture-sets.json")


def index_artifacts(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in sorted(root.glob("*/artifact.json")):
        artifact = load(path)
        artifact_id = artifact["id"]
        if artifact_id in index:
            raise AssertionError(f"Duplicate artifact id under {root}: {artifact_id}")
        index[artifact_id] = path.parent
    return index


def validate_receipt(receipt: dict, source_artifact: dict, baseline: dict, fixture_set: dict) -> None:
    validate_receipt_integrity(receipt)
    if receipt.get("execution_mode") not in {"api", "manual-observed"}:
        raise AssertionError("Persisted F5 receipt must represent a real execution")
    if receipt.get("status") != "IMPROVEMENT_PASS" or receipt.get("eligible_for_improved") is not True:
        raise AssertionError("Persisted F5 receipt must be IMPROVEMENT_PASS and eligible_for_improved")
    if receipt.get("artifact_id") != source_artifact.get("id") or receipt.get("artifact_version") != source_artifact.get("version"):
        raise AssertionError("F5 receipt artifact identity mismatch")
    if source_artifact.get("state") != "TESTED" or "tested" not in set(source_artifact.get("claims") or []):
        raise AssertionError("F5 source artifact must be TESTED")
    if receipt.get("engineered_prompt_fingerprint") != sha256_text(source_artifact.get("prompt_body", "")):
        raise AssertionError("F5 engineered prompt fingerprint mismatch")
    if receipt.get("baseline_id") != baseline.get("baseline_id"):
        raise AssertionError("F5 baseline id mismatch")
    if receipt.get("baseline_prompt_fingerprint") != sha256_text(baseline.get("prompt_body", "")):
        raise AssertionError("F5 baseline fingerprint mismatch")
    if receipt.get("fixture_set_id") != fixture_set.get("fixture_set_id"):
        raise AssertionError("F5 fixture-set id mismatch")
    if receipt.get("fixture_set_version") != fixture_set.get("version"):
        raise AssertionError("F5 fixture-set version mismatch")
    if receipt.get("fixture_set_fingerprint") != sha256_json(fixture_set):
        raise AssertionError("F5 fixture-set fingerprint mismatch")
    if receipt.get("parent_f4_receipt_id") != source_artifact.get("evaluation", {}).get("receipt_id"):
        raise AssertionError("F5 receipt parent F4 lineage mismatch")

    repeat_count = int(receipt.get("repeat_count") or 0)
    pair_count = int(receipt.get("pair_count") or 0)
    fixture_count = len(fixture_set.get("cases", []))
    if repeat_count < 3:
        raise AssertionError("Persisted F5 receipt requires at least 3 repeats")
    if pair_count != repeat_count * fixture_count:
        raise AssertionError(f"F5 pair count mismatch: {pair_count} != {repeat_count}*{fixture_count}")
    if receipt.get("engineered_blocking_pass_rate") != 1.0 or receipt.get("rubric_score") != 100.0:
        raise AssertionError("F5 improved evidence requires 100% engineered blocking pass rate")
    if receipt.get("engineered_failures") or receipt.get("regressions") or receipt.get("unresolved_engineered_human_checks"):
        raise AssertionError("F5 receipt retains blocking failure/regression/unresolved evidence")

    preference = receipt.get("preference") or {}
    if preference.get("baseline", 0) != 0:
        raise AssertionError("F5 improved evidence cannot contain baseline A/B wins")
    required_wins = math.ceil(pair_count * 0.30)
    if preference.get("required_engineered_wins") != required_wins or preference.get("engineered", 0) < required_wins:
        raise AssertionError("F5 improved evidence lacks material engineered blind wins")
    if preference.get("engineered", 0) + preference.get("baseline", 0) + preference.get("tie", 0) != pair_count:
        raise AssertionError("F5 preference inventory does not equal pair count")

    review = receipt.get("review") or {}
    runtime = receipt.get("runtime") or {}
    if review.get("reviewer_type") != "human" or review.get("blinded") is not True:
        raise AssertionError("F5 persisted evidence requires blinded human review")
    for key in ("reviewer_ref", "reviewed_at", "randomization_ref"):
        if not review.get(key):
            raise AssertionError(f"F5 review missing {key}")
    for key in RUNTIME_IDENTITY_FIELDS:
        if not str(runtime.get(key, "")).strip():
            raise AssertionError(f"F5 runtime missing {key}")


def main() -> None:
    baseline_document = load(BASELINES)
    fixture_document = load(FIXTURES)
    sources = index_artifacts(SOURCE)
    persisted = index_artifacts(OUTPUT) if OUTPUT.exists() else {}
    receipt_paths = sorted(RECEIPTS.glob("*.receipt.json"))

    seen: set[str] = set()
    expected: dict[str, dict] = {}
    for receipt_path in receipt_paths:
        receipt = load(receipt_path)
        artifact_id = receipt.get("artifact_id")
        if artifact_id in seen:
            raise AssertionError(f"Multiple persisted F5 receipts for same artifact: {artifact_id}")
        seen.add(artifact_id)
        if artifact_id not in sources:
            raise AssertionError(f"F5 receipt has no TESTED F4 source: {artifact_id}")
        source_artifact = load(sources[artifact_id] / "artifact.json")
        baseline = find_baseline(baseline_document, artifact_id)
        fixture_set = find_fixture_set(fixture_document, artifact_id)
        validate_receipt(receipt, source_artifact, baseline, fixture_set)
        expected[artifact_id] = promote_improved(source_artifact, receipt)

    manifest_path = OUTPUT / "manifest.json"
    manifest = load(manifest_path) if manifest_path.exists() else None

    if not receipt_paths:
        if persisted:
            raise AssertionError("No real F5 receipts exist but CANDIDATE artifacts are persisted")
        if manifest is not None:
            if manifest.get("status") != "NO_REAL_RECEIPTS" or manifest.get("candidate_count") != 0 or manifest.get("artifacts") != []:
                raise AssertionError("F5 zero-state manifest is inconsistent")
        print(json.dumps({"mk1_f5_repository": "PASS", "real_receipts": 0, "candidates": 0, "state": "NO_REAL_RECEIPTS"}, indent=2))
        return

    if set(persisted) != set(expected):
        raise AssertionError(f"F5 materialized artifact inventory mismatch: persisted={sorted(persisted)} expected={sorted(expected)}")
    if manifest is None or manifest.get("status") != "IMPROVED_CANDIDATES_MATERIALIZED" or manifest.get("candidate_count") != len(expected):
        raise AssertionError("F5 materialized manifest missing or inconsistent")

    for artifact_id, reconstructed in expected.items():
        bundle = persisted[artifact_id]
        observed = load(bundle / "artifact.json")
        if observed != reconstructed:
            raise AssertionError(f"F5 CANDIDATE cannot be deterministically reconstructed: {artifact_id}")
        receipt = load(bundle / "benchmark_receipt.json")
        if receipt.get("receipt_id") != reconstructed.get("evaluation", {}).get("receipt_id"):
            raise AssertionError(f"F5 bundle receipt mismatch: {artifact_id}")
        if observed.get("state") != "CANDIDATE" or observed.get("claims") != ["engineered", "tested", "improved"]:
            raise AssertionError(f"F5 persisted candidate has invalid state/claims: {artifact_id}")

    print(json.dumps({"mk1_f5_repository": "PASS", "real_receipts": len(receipt_paths), "candidates": len(expected), "state": "IMPROVED_CANDIDATES_MATERIALIZED"}, indent=2))


if __name__ == "__main__":
    main()
