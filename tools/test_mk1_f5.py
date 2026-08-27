from __future__ import annotations

import json

from mk1_f5_benchmark import benchmark_receipt_id, promote_improved, run_benchmark, sha256_json, sha256_text
from mk1_prompt_linter import lint_artifact
from validate_mk1_f5_repository import validate_receipt as validate_persisted_receipt


def tested_artifact() -> dict:
    return {
        "id": "pq_mk1_f5_test", "version": "0.1.0", "state": "TESTED", "artifact_type": "prompt",
        "title": "F5 Test Artifact", "domain": "general", "intent": "rewrite", "risk": "low", "language": "en",
        "model_targets": ["model-agnostic"], "purpose": "Preserve Alpha 42 while producing a useful response.",
        "success_criteria": ["Alpha 42 is preserved"], "inputs": {"required": ["text"], "optional": []},
        "architecture": {"purpose": True, "role": False, "context": True, "intake": False, "assumptions": True, "process": False, "constraints": False, "output_contract": True, "quality_gate": True, "fallback": False},
        "techniques": ["context-injection", "variable-template", "assumption-audit", "output-formatting", "self-check"],
        "prompt_body": "PURPOSE\nPreserve Alpha 42.\n\nCONTEXT\n{text}\n\nASSUMPTIONS\nDo not invent facts.\n\nOUTPUT CONTRACT\nReturn a clear answer.\n\nQUALITY GATE\nVerify Alpha remains 42.\n",
        "claims": ["engineered", "tested"],
        "provenance": {"mk0_inputs": ["fixture"], "patterns": [], "fixtures": ["f5"], "source_families": []},
        "evaluation": {"baseline_id": None, "fixture_set_id": "pq_mk1_fs_f5_test_v1", "receipt_id": "pq_mk1_f4_receipt_parent", "rubric_score": None, "blocking_failures": []},
        "created_at": None, "updated_at": "2026-08-26T23:00:00Z"
    }


def baseline() -> dict:
    return {"baseline_id": "pq_f5_baseline_test_v1", "task_artifact_id": "pq_mk1_f5_test", "artifact_version": "0.1.0", "prompt_body": "Rewrite {text} clearly.", "required_inputs": ["text"], "source": "test"}


def fixture_set() -> dict:
    return {"fixture_set_id": "pq_mk1_fs_f5_test_v1", "version": "0.2.0", "artifact_id": "pq_mk1_f5_test", "artifact_version": "0.1.0", "cases": [{"fixture_id": "f5_happy", "class": "happy-path", "severity": "blocking", "input": {"variables": {"text": "Alpha remains 42."}}, "expected": {"machine_assertions": [{"type": "contains_all", "values": ["Alpha", "42"]}], "human_checks": ["Meaning is preserved"]}}]}


def response(text: str, human: str = "PASS") -> dict:
    return {"output": text, "human_checks": {"Meaning is preserved": {"status": human, "note": "Blind review."}}}


def frozen_identity() -> dict:
    a, b, fs = tested_artifact(), baseline(), fixture_set()
    return {
        "artifact_id": a["id"], "artifact_version": a["version"],
        "engineered_prompt_fingerprint": sha256_text(a["prompt_body"]),
        "baseline_id": b["baseline_id"], "baseline_prompt_fingerprint": sha256_text(b["prompt_body"]),
        "fixture_set_id": fs["fixture_set_id"], "fixture_set_version": fs["version"], "fixture_set_fingerprint": sha256_json(fs),
        "parent_f4_receipt_id": a["evaluation"]["receipt_id"]
    }


def execution(winners: list[str] | None = None, engineered_outputs: list[str] | None = None, baseline_outputs: list[str] | None = None) -> dict:
    winners = winners or ["engineered", "engineered", "engineered"]
    engineered_outputs = engineered_outputs or ["Alpha remains 42."] * 3
    baseline_outputs = baseline_outputs or ["Alpha remains 42."] * 3
    repeats = []
    for index in range(3):
        repeats.append({"repeat": index + 1, "pairs": {"f5_happy": {
            "engineered": response(engineered_outputs[index]), "baseline": response(baseline_outputs[index]),
            "preference": {"winner": winners[index], "note": "Blind pairwise judgment."}
        }}})
    return {
        "execution_id": "f5-real-test", "mode": "manual-observed",
        "runtime": {
            "provider": "test-provider", "model": "test-model", "family": "test-family-a",
            "run_at": "2026-08-26T23:30:00Z", "identity_evidence_ref": "runtime-proof-test-001"
        },
        "review": {"reviewer_type": "human", "reviewer_ref": "reviewer-01", "reviewed_at": "2026-08-26T23:35:00Z", "blinded": True, "randomization_ref": "blind-seed-001"},
        **frozen_identity(), "repeats": repeats
    }


def test_real_superiority_pass() -> dict:
    receipt = run_benchmark(tested_artifact(), baseline(), fixture_set(), execution())
    assert receipt["status"] == "IMPROVEMENT_PASS" and receipt["eligible_for_improved"] is True
    assert receipt["engineered_blocking_pass_rate"] == 1.0 and receipt["preference"]["baseline"] == 0
    assert receipt["runtime"]["family"] == "test-family-a"
    assert receipt["runtime"]["identity_evidence_ref"] == "runtime-proof-test-001"
    promoted = promote_improved(tested_artifact(), receipt)
    assert promoted["state"] == "CANDIDATE" and promoted["claims"] == ["engineered", "tested", "improved"]
    assert promoted["evaluation"]["rubric_score"] == 100.0
    lint = lint_artifact(promoted)
    assert lint["status"] == "PASS", lint
    return {"status": receipt["status"], "state": promoted["state"], "score": 100.0, "family": receipt["runtime"]["family"]}


def test_ties_are_not_improvement() -> dict:
    receipt = run_benchmark(tested_artifact(), baseline(), fixture_set(), execution(["tie", "tie", "tie"]))
    assert receipt["status"] == "NO_EVIDENCE_OF_IMPROVEMENT" and receipt["eligible_for_improved"] is False
    return {"status": receipt["status"], "eligible": False}


def test_one_baseline_win_blocks() -> dict:
    receipt = run_benchmark(tested_artifact(), baseline(), fixture_set(), execution(["engineered", "engineered", "baseline"]))
    assert receipt["status"] == "IMPROVEMENT_FAIL" and receipt["preference"]["baseline"] == 1
    return {"status": receipt["status"], "baseline_wins": 1}


def test_behavioral_regression_blocks() -> dict:
    receipt = run_benchmark(tested_artifact(), baseline(), fixture_set(), execution(engineered_outputs=["Alpha remains 42.", "Alpha remains 42.", "Alpha changed."]))
    assert receipt["status"] == "IMPROVEMENT_FAIL" and receipt["engineered_failures"] and receipt["regressions"]
    return {"status": receipt["status"], "regressions": receipt["regressions"]}


def test_less_than_three_repeats_rejected() -> dict:
    value = execution(); value["repeats"] = value["repeats"][:2]
    try: run_benchmark(tested_artifact(), baseline(), fixture_set(), value)
    except ValueError as exc:
        assert "at least 3 repeats" in str(exc); return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 must reject underpowered real benchmark")


def test_unblinded_review_rejected() -> dict:
    value = execution(); value["review"]["blinded"] = False
    try: run_benchmark(tested_artifact(), baseline(), fixture_set(), value)
    except ValueError as exc:
        assert "blinded=true" in str(exc); return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 must reject unblinded improvement benchmark")


def test_runtime_family_required() -> dict:
    value = execution(); value["runtime"].pop("family")
    try: run_benchmark(tested_artifact(), baseline(), fixture_set(), value)
    except ValueError as exc:
        assert "runtime identity" in str(exc) and "family" in str(exc); return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 must identify an explicit runtime family")


def test_runtime_identity_evidence_required() -> dict:
    value = execution(); value["runtime"].pop("identity_evidence_ref")
    try: run_benchmark(tested_artifact(), baseline(), fixture_set(), value)
    except ValueError as exc:
        assert "runtime identity" in str(exc) and "identity_evidence_ref" in str(exc); return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 must bind runtime identity evidence")


def test_persisted_runtime_family_required() -> dict:
    receipt = run_benchmark(tested_artifact(), baseline(), fixture_set(), execution())
    receipt["runtime"].pop("family")
    core = dict(receipt)
    core.pop("receipt_id", None)
    receipt["receipt_id"] = benchmark_receipt_id(core)
    try:
        validate_persisted_receipt(receipt, tested_artifact(), baseline(), fixture_set())
    except AssertionError as exc:
        assert "runtime missing family" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 persisted evidence must identify an explicit runtime family")


def test_frozen_identity_drift_rejected() -> dict:
    value = execution(); value["baseline_prompt_fingerprint"] = sha256_text("changed baseline")
    try: run_benchmark(tested_artifact(), baseline(), fixture_set(), value)
    except ValueError as exc:
        assert "baseline_prompt_fingerprint" in str(exc); return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 must reject baseline drift")


def test_tampered_receipt_rejected() -> dict:
    receipt = run_benchmark(tested_artifact(), baseline(), fixture_set(), execution()); receipt["runtime"]["model"] = "tampered"
    try: promote_improved(tested_artifact(), receipt)
    except ValueError as exc:
        assert "integrity check failed" in str(exc); return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 promotion must reject tampered receipt")


def test_synthetic_never_promotes() -> dict:
    value = execution(); value["mode"] = "synthetic"; value["repeats"] = value["repeats"][:1]
    receipt = run_benchmark(tested_artifact(), baseline(), fixture_set(), value)
    assert receipt["status"] == "BENCHMARK_CHARACTERIZATION" and receipt["eligible_for_improved"] is False
    try: promote_improved(tested_artifact(), receipt)
    except ValueError: return {"status": receipt["status"], "promotion_rejected": True}
    raise AssertionError("Synthetic F5 benchmark must never promote")


def main() -> None:
    print(json.dumps({
        "mk1_f5": "PASS",
        "real_superiority_pass": test_real_superiority_pass(),
        "ties_not_improvement": test_ties_are_not_improvement(),
        "baseline_win_blocks": test_one_baseline_win_blocks(),
        "behavioral_regression_blocks": test_behavioral_regression_blocks(),
        "minimum_repeats": test_less_than_three_repeats_rejected(),
        "blind_review_required": test_unblinded_review_rejected(),
        "runtime_family_required": test_runtime_family_required(),
        "runtime_identity_evidence_required": test_runtime_identity_evidence_required(),
        "persisted_runtime_family_required": test_persisted_runtime_family_required(),
        "frozen_identity": test_frozen_identity_drift_rejected(),
        "tampered_receipt": test_tampered_receipt_rejected(),
        "synthetic_never_promotes": test_synthetic_never_promotes(),
        "policy": "F5 improvement requires 100% engineered blocking pass rate, zero regressions, zero baseline A/B wins, material blind wins, evidenced runtime identity, exact frozen identity and a real observed benchmark."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
