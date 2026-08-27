from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from mk1_behavioral_runner import evaluate_case, sha256_json, sha256_text


REAL_MODES = {"api", "manual-observed"}
ALL_MODES = REAL_MODES | {"synthetic"}
WINNERS = {"engineered", "baseline", "tie"}
MIN_REPEATS = 3
MIN_ENGINEERED_WIN_FRACTION = 0.30


def load(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def benchmark_receipt_id(core: dict) -> str:
    digest = hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()[:16]
    return f"pq_mk1_f5_receipt_{digest}"


def find_baseline(document: dict, task_artifact_id: str) -> dict:
    matches = [row for row in document.get("baselines", []) if row.get("task_artifact_id") == task_artifact_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one F5 primary baseline for {task_artifact_id}; got {len(matches)}")
    baseline = dict(matches[0])
    baseline["baseline_document_version"] = document.get("version", "1")
    return baseline


def find_fixture_set(document: dict, artifact_id: str) -> dict:
    matches = [row for row in document.get("fixture_sets", []) if row.get("artifact_id") == artifact_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one F5 fixture set for {artifact_id}; got {len(matches)}")
    fixture_set = dict(matches[0])
    fixture_set["version"] = document.get("version", "1")
    return fixture_set


def _require_source(tested_artifact: dict, baseline: dict, fixture_set: dict) -> None:
    if tested_artifact.get("state") != "TESTED":
        raise ValueError(f"F5 requires TESTED source artifact; got {tested_artifact.get('state')!r}")
    if "tested" not in set(tested_artifact.get("claims") or []):
        raise ValueError("F5 source artifact must carry tested claim")
    if not tested_artifact.get("evaluation", {}).get("receipt_id"):
        raise ValueError("F5 source artifact must preserve a real parent F4 receipt_id")
    if baseline.get("task_artifact_id") != tested_artifact.get("id"):
        raise ValueError("F5 baseline task_artifact_id mismatch")
    if baseline.get("artifact_version") != tested_artifact.get("version"):
        raise ValueError("F5 baseline artifact_version mismatch")
    if fixture_set.get("artifact_id") != tested_artifact.get("id"):
        raise ValueError("F5 fixture-set artifact_id mismatch")
    if fixture_set.get("artifact_version") != tested_artifact.get("version"):
        raise ValueError("F5 fixture-set artifact_version mismatch")
    if not str(baseline.get("prompt_body", "")).strip():
        raise ValueError("F5 baseline requires non-empty prompt_body")


def _require_real_execution(execution: dict, fixture_set: dict) -> None:
    runtime = execution.get("runtime") or {}
    missing_runtime = [key for key in ("provider", "model", "run_at") if not runtime.get(key)]
    if missing_runtime:
        raise ValueError(f"Real F5 benchmark missing runtime identity: {missing_runtime}")
    if not execution.get("execution_id"):
        raise ValueError("Real F5 benchmark requires execution_id")

    review = execution.get("review") or {}
    if review.get("reviewer_type") != "human":
        raise ValueError("Real F5 benchmark requires reviewer_type='human'")
    missing_review = [key for key in ("reviewer_ref", "reviewed_at", "randomization_ref") if not review.get(key)]
    if missing_review:
        raise ValueError(f"Real F5 benchmark missing blind-review metadata: {missing_review}")
    if review.get("blinded") is not True:
        raise ValueError("Real F5 benchmark requires blinded=true")

    repeats = execution.get("repeats") or []
    if len(repeats) < MIN_REPEATS:
        raise ValueError(f"Real F5 benchmark requires at least {MIN_REPEATS} repeats; got {len(repeats)}")

    expected_ids = {row["fixture_id"] for row in fixture_set.get("cases", [])}
    repeat_ids = set()
    for repeat in repeats:
        repeat_id = repeat.get("repeat")
        if repeat_id in repeat_ids:
            raise ValueError(f"Duplicate F5 repeat identifier: {repeat_id!r}")
        repeat_ids.add(repeat_id)
        pairs = repeat.get("pairs") or {}
        if set(pairs) != expected_ids:
            missing = sorted(expected_ids - set(pairs))
            extra = sorted(set(pairs) - expected_ids)
            raise ValueError(f"F5 repeat {repeat_id!r} pair inventory mismatch; missing={missing} extra={extra}")
        for fixture_id, pair in pairs.items():
            for participant in ("engineered", "baseline"):
                output = str((pair.get(participant) or {}).get("output", "")).strip()
                if not output:
                    raise ValueError(f"F5 repeat {repeat_id!r} fixture {fixture_id} missing {participant} output")
            preference = pair.get("preference") or {}
            if preference.get("winner") not in WINNERS:
                raise ValueError(f"F5 repeat {repeat_id!r} fixture {fixture_id} missing valid blind preference")
            if not str(preference.get("note", "")).strip():
                raise ValueError(f"F5 repeat {repeat_id!r} fixture {fixture_id} preference requires evidence note")


def run_benchmark(tested_artifact: dict, baseline: dict, fixture_set: dict, execution: dict) -> dict:
    _require_source(tested_artifact, baseline, fixture_set)
    mode = execution.get("mode")
    if mode not in ALL_MODES:
        raise ValueError(f"Unsupported F5 execution mode: {mode!r}")

    engineered_prompt = tested_artifact["prompt_body"]
    baseline_prompt = baseline["prompt_body"]
    frozen = {
        "artifact_id": tested_artifact["id"],
        "artifact_version": tested_artifact["version"],
        "engineered_prompt_fingerprint": sha256_text(engineered_prompt),
        "baseline_id": baseline["baseline_id"],
        "baseline_prompt_fingerprint": sha256_text(baseline_prompt),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version", "1"),
        "fixture_set_fingerprint": sha256_json(fixture_set),
        "parent_f4_receipt_id": tested_artifact["evaluation"]["receipt_id"],
    }

    if mode in REAL_MODES:
        _require_real_execution(execution, fixture_set)
        for key, expected in frozen.items():
            if execution.get(key) != expected:
                raise ValueError(f"F5 frozen identity mismatch for {key}: expected {expected!r}, got {execution.get(key)!r}")

    fixtures = {row["fixture_id"]: row for row in fixture_set.get("cases", [])}
    rows = []
    engineered_failures = []
    regressions = []
    unresolved = 0
    wins = {"engineered": 0, "baseline": 0, "tie": 0}

    repeats = execution.get("repeats") or []
    for repeat in repeats:
        repeat_id = repeat.get("repeat")
        pairs = repeat.get("pairs") or {}
        for fixture_id, fixture in fixtures.items():
            pair = pairs.get(fixture_id, {})
            engineered = evaluate_case(fixture, pair.get("engineered") or {})
            base = evaluate_case(fixture, pair.get("baseline") or {})
            winner = (pair.get("preference") or {}).get("winner")
            if winner in WINNERS:
                wins[winner] += 1
            unresolved += len(engineered["unresolved_human_checks"])
            if fixture.get("severity", "normal") == "blocking" and not engineered["pass"]:
                engineered_failures.append(f"r{repeat_id}:{fixture_id}")
            if base["pass"] and not engineered["pass"]:
                regressions.append(f"r{repeat_id}:{fixture_id}")
            rows.append({
                "repeat": repeat_id,
                "fixture_id": fixture_id,
                "class": fixture.get("class"),
                "engineered_pass": engineered["pass"],
                "baseline_pass": base["pass"],
                "engineered": engineered,
                "baseline": base,
                "preference": pair.get("preference") or {},
            })

    total_pairs = len(rows)
    engineered_passes = sum(1 for row in rows if row["engineered_pass"])
    baseline_passes = sum(1 for row in rows if row["baseline_pass"])
    engineered_pass_rate = engineered_passes / total_pairs if total_pairs else 0.0
    baseline_pass_rate = baseline_passes / total_pairs if total_pairs else 0.0
    required_wins = math.ceil(total_pairs * MIN_ENGINEERED_WIN_FRACTION) if total_pairs else 1

    if mode == "synthetic":
        status = "BENCHMARK_CHARACTERIZATION"
        eligible = False
    elif engineered_failures or regressions or unresolved:
        status = "IMPROVEMENT_FAIL"
        eligible = False
    elif wins["baseline"] > 0:
        status = "IMPROVEMENT_FAIL"
        eligible = False
    elif wins["engineered"] < required_wins:
        status = "NO_EVIDENCE_OF_IMPROVEMENT"
        eligible = False
    else:
        status = "IMPROVEMENT_PASS"
        eligible = True

    core = {
        "mk_stage": "MK1",
        "phase": "F5",
        **frozen,
        "execution_id": execution.get("execution_id"),
        "execution_mode": mode,
        "runtime": execution.get("runtime") or {},
        "review": execution.get("review") or {},
        "repeat_count": len(repeats),
        "pair_count": total_pairs,
        "engineered_blocking_pass_rate": round(engineered_pass_rate, 6),
        "baseline_blocking_pass_rate": round(baseline_pass_rate, 6),
        "rubric_score": round(engineered_pass_rate * 100, 2),
        "engineered_failures": engineered_failures,
        "regressions": regressions,
        "unresolved_engineered_human_checks": unresolved,
        "preference": {**wins, "required_engineered_wins": required_wins},
        "status": status,
        "eligible_for_improved": eligible,
        "results": rows,
        "state_policy": "Only a real IMPROVEMENT_PASS receipt may support TESTED -> CANDIDATE and claim improved.",
        "claim_policy": "F5 improvement is scoped to this exact baseline, fixture set and runtime. It is not universal or cross-runtime certification.",
    }
    core["receipt_id"] = benchmark_receipt_id(core)
    return core


def validate_receipt_integrity(receipt: dict) -> None:
    supplied = receipt.get("receipt_id")
    core = copy.deepcopy(receipt)
    core.pop("receipt_id", None)
    expected = benchmark_receipt_id(core)
    if supplied != expected:
        raise ValueError(f"F5 receipt integrity check failed: expected {expected}, got {supplied}")


def promote_improved(tested_artifact: dict, receipt: dict) -> dict:
    validate_receipt_integrity(receipt)
    if tested_artifact.get("state") != "TESTED":
        raise ValueError("F5 promotion requires TESTED source artifact")
    if receipt.get("artifact_id") != tested_artifact.get("id") or receipt.get("artifact_version") != tested_artifact.get("version"):
        raise ValueError("F5 receipt artifact identity mismatch")
    if receipt.get("engineered_prompt_fingerprint") != sha256_text(tested_artifact.get("prompt_body", "")):
        raise ValueError("F5 engineered prompt fingerprint mismatch")
    if receipt.get("parent_f4_receipt_id") != tested_artifact.get("evaluation", {}).get("receipt_id"):
        raise ValueError("F5 receipt does not descend from the artifact's F4 receipt")
    if receipt.get("execution_mode") not in REAL_MODES:
        raise ValueError("Synthetic F5 receipt cannot promote")
    if receipt.get("status") != "IMPROVEMENT_PASS" or receipt.get("eligible_for_improved") is not True:
        raise ValueError("F5 receipt cannot promote: improvement gate did not pass")
    if receipt.get("engineered_blocking_pass_rate") != 1.0:
        raise ValueError("F5 improvement requires 100% engineered blocking pass rate")
    if receipt.get("engineered_failures") or receipt.get("regressions") or receipt.get("unresolved_engineered_human_checks"):
        raise ValueError("F5 improvement receipt retains blocking evidence")
    if (receipt.get("preference") or {}).get("baseline", 0) != 0:
        raise ValueError("F5 improvement cannot retain baseline A/B wins")

    promoted = copy.deepcopy(tested_artifact)
    promoted["state"] = "CANDIDATE"
    promoted["claims"] = ["engineered", "tested", "improved"]
    promoted["evaluation"] = {
        "baseline_id": receipt["baseline_id"],
        "fixture_set_id": receipt["fixture_set_id"],
        "receipt_id": receipt["receipt_id"],
        "rubric_score": receipt["rubric_score"],
        "blocking_failures": [],
    }
    promoted["updated_at"] = (receipt.get("runtime") or {}).get("run_at")
    return promoted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--baselines", default="mk1/baselines/f5/task-equivalent-minimal.json")
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--execution", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    artifact = load(args.artifact)
    baseline_doc = load(args.baselines)
    fixture_doc = load(args.fixtures)
    baseline = find_baseline(baseline_doc, artifact["id"])
    fixture_set = find_fixture_set(fixture_doc, artifact["id"])
    receipt = run_benchmark(artifact, baseline, fixture_set, load(args.execution))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
