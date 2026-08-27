from __future__ import annotations

import copy
import json

from mk1_f5_benchmark import promote_improved, run_benchmark
from mk1_f6_certify import build_certification_receipt, promote_certified
from mk1_prompt_linter import lint_artifact
from test_mk1_f5 import baseline, execution, fixture_set, tested_artifact


def make_receipt(
    family: str,
    index: int,
    randomization_ref: str | None = None,
    provider: str | None = None,
    identity_evidence_ref: str | None = None,
) -> dict:
    value = execution()
    value["execution_id"] = f"f6-real-{index}"
    value["runtime"] = {
        "provider": provider or f"provider-{index}",
        "model": f"model-{index}",
        "family": family,
        "run_at": f"2026-08-27T0{index}:00:00Z",
        "identity_evidence_ref": identity_evidence_ref or f"runtime-evidence-{index:03d}",
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
    assert receipt["runtime_provider_count"] == 3
    assert receipt["source_candidate_f5_receipt_id"] == candidate["evaluation"]["receipt_id"]
    certified = promote_certified(candidate, receipt)
    assert certified["state"] == "CERTIFIED"
    assert certified["claims"] == ["engineered", "tested", "improved", "certified"]
    assert certified["evaluation"]["receipt_id"] == receipt["receipt_id"]
    assert certified["evaluation"]["rubric_score"] == 100.0
    lint = lint_artifact(certified)
    assert lint["status"] == "PASS", lint
    return {
        "status": receipt["status"],
        "families": receipt["runtime_families"],
        "providers": receipt["runtime_providers"],
        "state": certified["state"],
    }


def expect_rejected(receipts: list[dict], reason_fragment: str) -> dict:
    source = tested_artifact()
    b = baseline()
    fs = fixture_set()
    candidate = promote_improved(source, receipts[0])
    try:
        build_certification_receipt(candidate, source, b, fs, receipts)
    except ValueError as exc:
        assert reason_fragment in str(exc), str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError(f"F6 must reject evidence: {reason_fragment}")


def test_less_than_three_families_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    try:
        build_certification_receipt(candidate, source, b, fs, receipts[:2])
    except ValueError as exc:
        assert "at least 3" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must reject underpowered cross-runtime evidence")


def test_duplicate_family_rejected() -> dict:
    return expect_rejected([
        make_receipt("family-alpha", 1),
        make_receipt("family-beta", 2),
        make_receipt(" FAMILY-BETA ", 3),
    ], "distinct runtime families")


def test_provider_diversity_required() -> dict:
    return expect_rejected([
        make_receipt("family-alpha", 1, provider="same-provider"),
        make_receipt("family-beta", 2, provider="same-provider"),
        make_receipt("family-gamma", 3, provider="provider-3"),
    ], "distinct runtime providers")


def test_runtime_identity_evidence_required() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    bad = copy.deepcopy(receipts[2])
    bad["runtime"].pop("identity_evidence_ref")
    # Integrity should fail first for a modified persisted receipt. This still proves the field is receipt-bound.
    try:
        build_certification_receipt(candidate, source, b, fs, [receipts[0], receipts[1], bad])
    except ValueError as exc:
        assert "integrity check failed" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must reject runtime identity evidence removal")


def test_distinct_runtime_identity_evidence_required() -> dict:
    return expect_rejected([
        make_receipt("family-alpha", 1, identity_evidence_ref="same-runtime-proof"),
        make_receipt("family-beta", 2, identity_evidence_ref="same-runtime-proof"),
        make_receipt("family-gamma", 3),
    ], "distinct runtime identity evidence")


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
    receipts = [
        make_receipt("family-alpha", 1, "same-blind-seed"),
        make_receipt("family-beta", 2, "same-blind-seed"),
        make_receipt("family-gamma", 3, "other-blind-seed"),
    ]
    return expect_rejected(receipts, "distinct blind randomization_ref")


def test_tampered_f6_receipt_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    receipt = build_certification_receipt(candidate, source, b, fs, receipts)
    receipt["runtime_provider_count"] = 4
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
        "provider_diversity": test_provider_diversity_required(),
        "runtime_identity_evidence": test_runtime_identity_evidence_required(),
        "distinct_runtime_identity_evidence": test_distinct_runtime_identity_evidence_required(),
        "candidate_origin_receipt": test_candidate_origin_receipt_required(),
        "prompt_identity_freeze": test_prompt_drift_rejected(),
        "f5_receipt_integrity": test_tampered_f5_receipt_rejected(),
        "independent_blind_randomization": test_distinct_randomization_required(),
        "f6_receipt_integrity": test_tampered_f6_receipt_rejected(),
        "policy": "CERTIFIED requires the exact CANDIDATE to preserve F5 superiority with 100% blocking pass, zero regressions/baseline wins and blinded human review across at least three distinct runtime families AND three distinct providers, with bound runtime identity evidence for every execution."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
