from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from mk1_behavioral_runner import find_fixture_set, run_fixture_set, sha256_json
from mk1_f5_benchmark import find_baseline, run_benchmark


def load(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require_review_header(review: dict) -> tuple[str, str]:
    reviewer_ref = str(review.get("reviewer_ref") or "").strip()
    reviewed_at = str(review.get("reviewed_at") or "").strip()
    if not reviewer_ref or not reviewed_at:
        raise ValueError("Completed human review requires reviewer_ref and reviewed_at")
    return reviewer_ref, reviewed_at


def checks_to_map(checks: list[dict], context: str) -> dict:
    result: dict[str, dict] = {}
    for item in checks:
        check = str(item.get("check") or "").strip()
        status = item.get("status")
        note = str(item.get("note") or "").strip()
        if not check or status not in {"PASS", "FAIL"} or not note:
            raise ValueError(f"Incomplete human check in {context}: {item}")
        if check in result:
            raise ValueError(f"Duplicate human check in {context}: {check}")
        result[check] = {"status": status, "note": note}
    return result


def _ref_filename(value: str) -> str:
    path_part = str(value or "").split("#", 1)[0]
    name = Path(path_part).name
    if not name:
        raise ValueError(f"Invalid evidence ref: {value!r}")
    return name


def persist_runtime_evidence(execution: dict, source_execution_path: Path, evidence_root: Path) -> None:
    """Move a reviewed execution from ephemeral staging references to durable repository evidence.

    Raw observation JSON is copied byte-for-byte. The execution manifest is rebuilt because its
    observation paths change. The canonical receipt is generated only after these durable refs exist.
    """
    execution_id = str(execution.get("execution_id") or "").strip()
    if not execution_id:
        raise ValueError("Cannot persist runtime evidence without execution_id")
    source_dir = source_execution_path.parent
    source_raw = source_dir / "raw"
    source_manifest = source_dir / "runtime-evidence-manifest.json"
    if not source_raw.is_dir() or not source_manifest.is_file():
        raise ValueError("Observed execution is missing its raw evidence directory or manifest")

    destination = evidence_root / execution_id
    destination_raw = destination / "raw"
    if destination.exists():
        shutil.rmtree(destination)
    destination_raw.mkdir(parents=True, exist_ok=True)

    manifest = load(source_manifest)
    observations = manifest.get("observations") or []
    canonical_refs: dict[str, str] = {}
    for row in observations:
        old_ref = str(row.get("evidence_ref") or "")
        filename = _ref_filename(old_ref)
        source_file = source_raw / filename
        if not source_file.is_file():
            raise ValueError(f"Missing raw observation evidence: {source_file}")
        raw = load(source_file)
        declared_hash = str(raw.get("evidence_sha256") or "")
        core = dict(raw)
        core.pop("evidence_sha256", None)
        expected_hash = sha256_json(core)
        if declared_hash != expected_hash:
            raise ValueError(f"Runtime observation evidence integrity mismatch: {source_file}")
        target = destination_raw / filename
        shutil.copyfile(source_file, target)
        canonical_ref = f"{target.as_posix()}#{declared_hash}"
        canonical_refs[old_ref] = canonical_ref
        row["evidence_ref"] = canonical_ref

    manifest.pop("manifest_sha256", None)
    manifest["manifest_sha256"] = sha256_json(manifest)
    canonical_manifest = destination / "runtime-evidence-manifest.json"
    write(canonical_manifest, manifest)
    execution["runtime"]["identity_evidence_ref"] = f"{canonical_manifest.as_posix()}#{manifest['manifest_sha256']}"

    if execution.get("mode") == "api" and "responses" in execution:
        for response in (execution.get("responses") or {}).values():
            old = response.get("observation_evidence_ref")
            if old:
                response["observation_evidence_ref"] = canonical_refs.get(old) or f"{(destination_raw / _ref_filename(old)).as_posix()}#{str(old).split('#', 1)[-1]}"
    for repeat in execution.get("repeats") or []:
        for pair in (repeat.get("pairs") or {}).values():
            for role in ("engineered", "baseline"):
                response = pair.get(role) or {}
                old = response.get("observation_evidence_ref")
                if old:
                    response["observation_evidence_ref"] = canonical_refs.get(old) or f"{(destination_raw / _ref_filename(old)).as_posix()}#{str(old).split('#', 1)[-1]}"


def finalize_f4(args: argparse.Namespace) -> None:
    artifact = load(args.artifact)
    fixture_document = load(args.fixtures)
    fixture_set = find_fixture_set(fixture_document, args.fixture_set)
    execution_path = Path(args.execution)
    execution = load(execution_path)
    review = load(args.review)
    reviewer_ref, reviewed_at = require_review_header(review)
    if review.get("execution_id") != execution.get("execution_id"):
        raise ValueError("F4 review/execution identity mismatch")

    reviewed_cases = {row["fixture_id"]: row for row in review.get("cases") or []}
    expected_ids = {row["fixture_id"] for row in fixture_set.get("cases", [])}
    if set(reviewed_cases) != expected_ids:
        raise ValueError("F4 review fixture inventory mismatch")
    for fixture_id in expected_ids:
        execution["responses"][fixture_id]["human_checks"] = checks_to_map(reviewed_cases[fixture_id].get("human_checks") or [], fixture_id)
    execution["review"] = {"reviewer_type": "human", "reviewer_ref": reviewer_ref, "reviewed_at": reviewed_at}
    persist_runtime_evidence(execution, execution_path, Path(args.evidence_root))

    receipt = run_fixture_set(artifact, fixture_set, execution)
    write(Path(args.output_execution), execution)
    write(Path(args.output_receipt), receipt)
    print(json.dumps({"status": receipt["status"], "eligible_for_tested": receipt["eligible_for_tested"], "receipt_id": receipt["receipt_id"], "runtime_evidence": execution["runtime"]["identity_evidence_ref"]}, indent=2))


def finalize_f5(args: argparse.Namespace) -> None:
    artifact = load(args.artifact)
    fixture_document = load(args.fixtures)
    fixture_set = find_fixture_set(fixture_document, args.fixture_set)
    baseline = find_baseline(load(args.baselines), artifact["id"])
    execution_path = Path(args.execution)
    execution = load(execution_path)
    review = load(args.review)
    deblind = load(args.deblind_map)
    reviewer_ref, reviewed_at = require_review_header(review)
    if review.get("execution_id") != execution.get("execution_id") or deblind.get("execution_id") != execution.get("execution_id"):
        raise ValueError("F5 review/deblind/execution identity mismatch")
    randomization_ref = str(deblind.get("randomization_ref") or "").strip()
    if not randomization_ref:
        raise ValueError("F5 deblind map lacks randomization_ref")

    canonical_repeats = {int(row["repeat"]): row for row in execution.get("repeats") or []}
    review_repeats = {int(row["repeat"]): row for row in review.get("repeats") or []}
    if set(canonical_repeats) != set(review_repeats):
        raise ValueError("F5 review repeat inventory mismatch")

    assignments = deblind.get("assignments") or {}
    for repeat_id, canonical_repeat in canonical_repeats.items():
        reviewed_pairs = {row["fixture_id"]: row for row in review_repeats[repeat_id].get("pairs") or []}
        canonical_pairs = canonical_repeat.get("pairs") or {}
        if set(reviewed_pairs) != set(canonical_pairs):
            raise ValueError(f"F5 review pair inventory mismatch in repeat {repeat_id}")
        for fixture_id, canonical_pair in canonical_pairs.items():
            reviewed = reviewed_pairs[fixture_id]
            assignment = assignments.get(f"r{repeat_id}:{fixture_id}") or {}
            if set(assignment) != {"A", "B"} or set(assignment.values()) != {"engineered", "baseline"}:
                raise ValueError(f"Invalid F5 blind assignment for r{repeat_id}:{fixture_id}")
            for blind_label in ("A", "B"):
                role = assignment[blind_label]
                canonical_pair[role]["human_checks"] = checks_to_map((reviewed.get(blind_label) or {}).get("human_checks") or [], f"r{repeat_id}:{fixture_id}:{blind_label}")
            preference = reviewed.get("preference") or {}
            blind_winner = preference.get("winner")
            note = str(preference.get("note") or "").strip()
            if blind_winner not in {"A", "B", "tie"} or not note:
                raise ValueError(f"Incomplete F5 preference review for r{repeat_id}:{fixture_id}")
            winner = "tie" if blind_winner == "tie" else assignment[blind_winner]
            canonical_pair["preference"] = {"winner": winner, "note": note}

    execution["review"] = {
        "reviewer_type": "human",
        "reviewer_ref": reviewer_ref,
        "reviewed_at": reviewed_at,
        "blinded": True,
        "randomization_ref": randomization_ref,
    }
    persist_runtime_evidence(execution, execution_path, Path(args.evidence_root))
    receipt = run_benchmark(artifact, baseline, fixture_set, execution)
    write(Path(args.output_execution), execution)
    write(Path(args.output_receipt), receipt)
    print(json.dumps({"status": receipt["status"], "eligible_for_improved": receipt["eligible_for_improved"], "receipt_id": receipt["receipt_id"], "preference": receipt["preference"], "runtime_evidence": execution["runtime"]["identity_evidence_ref"]}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Finalize observed MK1 experiments only after complete human review and durable evidence persistence.")
    parser.add_argument("--stage", required=True, choices=["f4", "f5"])
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--fixture-set", required=True)
    parser.add_argument("--execution", required=True)
    parser.add_argument("--review", required=True)
    parser.add_argument("--output-execution", required=True)
    parser.add_argument("--output-receipt", required=True)
    parser.add_argument("--evidence-root", default="mk1/evidence/runtime")
    parser.add_argument("--baselines", default="mk1/baselines/f5/task-equivalent-minimal.json")
    parser.add_argument("--deblind-map")
    args = parser.parse_args()
    if args.stage == "f4":
        finalize_f4(args)
    else:
        if not args.deblind_map:
            raise ValueError("F5 finalization requires --deblind-map")
        finalize_f5(args)


if __name__ == "__main__":
    main()
