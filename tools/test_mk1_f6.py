from __future__ import annotations

import copy
import json

from mk1_f5_benchmark import promote_improved, run_benchmark
from mk1_f6_certify import build_certification_receipt, promote_certified
from mk1_prompt_linter import lint_artifact
from test_mk1_f5 import baseline, execution, fixture_set, tested_artifact


def make_receipt(family: str, index: int, randomization_ref: str | None = None) -> dict:
    value = execution()
    value["execution_id"] = f"f6-real-{index}"
    value["runtime"] = {
        "provider": f"provider-{index}",
        "model": f"model-{index}",
        "family": family,
        "run_at": f"2026-08-27T0{index}:00:00Z",
    }
    value["review"] = {
        "reviewer_type": "human",
        "reviewer_ref": f"reviewer-{index:02d}",
        "reviewed_at": f"2026-08-27T0{index}:10:00Z",
        "blinded": True,
        "randomization_ref": randomization_ref or f"blind-f6-{index:03d}",
    }
    return run_benchmark(tested_artifact(), baseline(), fixture_set(), value)


def source_bundle() -> tuple[dict, dict, dict, dict, list[dict]]:
    source = tested_artifact()
    b = baseline()
    fs = fixture_set()
    receipts = [
        make_receipt("family-alpha", 1),
        make_receipt("family-beta", 2),
        make_receipt("family-gamma", 3),
    ]
    candidate = promote_improved(source, receipts[0])
    return source, candidate, b, fs, receipts


def test_certification_pass() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    receipt = build_certification_receipt(candidate, source, b, fs, receipts)
    assert receipt["status"] == "CERTIFICATION_PASS"
    assert receipt["eligible_for_certified"] is True
    assert receipt["runtime_family_count"] == 3
    assert receipt["source_candidate_f5_receipt_id"] == candidate["evaluation"]["receipt_id"]
    certified = promote_certified(candidate, receipt)
    assert certified["state"] == "CERTIFIED"
    assert certified["claims"] == ["engineered", "tested", "improved", "certified"]
    assert certified["evaluation"]["receipt_id"] == receipt["receipt_id"]
    assert certified["evaluation"]["rubric_score"] == 100.0
    lint = lint_artifact(certified)
    assert lint["status"] == "PASS", lint
    return {"status": receipt["status"], "families": receipt["runtime_families"], "state": certified["state"]}


def test_less_than_three_families_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    try:
        build_certification_receipt(candidate, source, b, fs, receipts[:2])
    except ValueError as exc:
        assert "at least 3" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must reject underpowered cross-runtime evidence")


def test_duplicate_family_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    receipts[2] = make_receipt("family-beta", 4)
    try:
        build_certification_receipt(candidate, source, b, fs, receipts)
    except ValueError as exc:
        assert "distinct runtime families" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must not count the same runtime family twice")


def test_candidate_origin_receipt_required() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    evidence = [receipts[1], receipts[2], make_receipt("family-delta", 4)]
    try:
        build_certification_receipt(candidate, source, b, fs, evidence)
    except ValueError as exc:
        assert "exact F5 receipt" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 evidence must include the receipt that created the CANDIDATE")


def test_prompt_drift_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    drifted = copy.deepcopy(candidate)
    drifted["prompt_body"] += "\nDRIFT\n"
    try:
        build_certification_receipt(drifted, source, b, fs, receipts)
    except ValueError as exc:
        assert "identity drift" in str(exc) or "fingerprint" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must reject candidate prompt drift")


def test_tampered_f5_receipt_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    receipts[2]["runtime"]["model"] = "tampered-model"
    try:
        build_certification_receipt(candidate, source, b, fs, receipts)
    except ValueError as exc:
        assert "integrity check failed" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must reject tampered F5 evidence")


def test_distinct_randomization_required() -> dict:
    source = tested_artifact()
    b = baseline()
    fs = fixture_set()
    receipts = [
        make_receipt("family-alpha", 1, "same-blind-seed"),
        make_receipt("family-beta", 2, "same-blind-seed"),
        make_receipt("family-gamma", 3, "other-blind-seed"),
    ]
    candidate = promote_improved(source, receipts[0])
    try:
        build_certification_receipt(candidate, source, b, fs, receipts)
    except ValueError as exc:
        assert "distinct blind randomization_ref" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must not reuse the same blind randomization across runtime evidence")


def test_tampered_f6_receipt_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    receipt = build_certification_receipt(candidate, source, b, fs, receipts)
    receipt["runtime_family_count"] = 4
    try:
        promote_certified(candidate, receipt)
    except ValueError as exc:
        assert "integrity check failed" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 promotion must reject a tampered certification receipt")


def main() -> None:
    print(json.dumps({
        "mk1_f6": "PASS",
        "certification_pass": test_certification_pass(),
        "minimum_runtime_families": test_less_than_three_families_rejected(),
        "distinct_runtime_families": test_duplicate_family_rejected(),
        "candidate_origin_receipt": test_candidate_origin_receipt_required(),
        "prompt_identity_freeze": test_prompt_drift_rejected(),
        "f5_receipt_integrity": test_tampered_f5_receipt_rejected(),
        "independent_blind_randomization": test_distinct_randomization_required(),
        "f6_receipt_integrity": test_tampered_f6_receipt_rejected(),
        "policy": "CERTIFIED requires the exact CANDIDATE to preserve F5 superiority with 100% blocking pass, zero regressions/baseline wins and blinded human review across at least three distinct declared runtime families."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
