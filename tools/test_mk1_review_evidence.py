from __future__ import annotations

import json

from mk1_behavioral_runner import run_fixture_set
from mk1_f5_benchmark import run_benchmark
from test_mk1_f4 import artifact as f4_artifact, fixture_set as f4_fixture_set, real_execution as f4_real_execution
from test_mk1_f5 import baseline as f5_baseline, execution as f5_execution, fixture_set as f5_fixture_set, tested_artifact as f5_tested_artifact


def test_f4_bare_human_judgment_rejected() -> dict:
    execution = f4_real_execution()
    execution["responses"]["happy"]["human_checks"]["Meaning is preserved"]["note"] = ""
    try:
        run_fixture_set(f4_artifact(), f4_fixture_set(), execution)
    except ValueError as exc:
        assert "evidence note" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F4 must reject PASS/FAIL labels without evidence notes")


def test_f4_unresolved_remains_failure_not_exception() -> dict:
    execution = f4_real_execution({"happy": {"output": "Alpha remains 42."}})
    receipt = run_fixture_set(f4_artifact(), f4_fixture_set(), execution)
    assert receipt["status"] == "BEHAVIORAL_FAIL"
    assert receipt["unresolved_blocking_human_checks"] == 1
    return {"status": receipt["status"], "unresolved": 1}


def test_f5_baseline_human_evidence_required() -> dict:
    execution = f5_execution()
    baseline_response = execution["repeats"][0]["pairs"]["f5_happy"]["baseline"]
    baseline_response["human_checks"]["Meaning is preserved"] = {"status": "UNRESOLVED", "note": ""}
    try:
        run_benchmark(f5_tested_artifact(), f5_baseline(), f5_fixture_set(), execution)
    except ValueError as exc:
        assert "baseline human evidence incomplete" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 must not let unresolved baseline review manufacture superiority")


def test_f5_engineered_evidence_note_required() -> dict:
    execution = f5_execution()
    engineered_response = execution["repeats"][0]["pairs"]["f5_happy"]["engineered"]
    engineered_response["human_checks"]["Meaning is preserved"] = {"status": "PASS", "note": ""}
    try:
        run_benchmark(f5_tested_artifact(), f5_baseline(), f5_fixture_set(), execution)
    except ValueError as exc:
        assert "engineered human evidence incomplete" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 engineered human judgment requires evidence note")


def test_f5_preference_note_required() -> dict:
    execution = f5_execution()
    execution["repeats"][0]["pairs"]["f5_happy"]["preference"]["note"] = ""
    try:
        run_benchmark(f5_tested_artifact(), f5_baseline(), f5_fixture_set(), execution)
    except ValueError as exc:
        assert "preference requires evidence note" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F5 blind preference requires an evidence note")


def main() -> None:
    print(json.dumps({
        "mk1_review_evidence": "PASS",
        "f4_bare_judgment": test_f4_bare_human_judgment_rejected(),
        "f4_unresolved_semantics": test_f4_unresolved_remains_failure_not_exception(),
        "f5_baseline_symmetry": test_f5_baseline_human_evidence_required(),
        "f5_engineered_note": test_f5_engineered_evidence_note_required(),
        "f5_preference_note": test_f5_preference_note_required(),
        "policy": "Observed outputs may remain pending review, but any PASS/FAIL or A/B preference used as evidence must be symmetric, explicit and supported by a non-empty human note."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
