from __future__ import annotations

import copy
import json

from mk1_f5_benchmark import promote_improved, run_benchmark
from mk1_f6_certify import build_certification_receipt, promote_certified
from mk1_prompt_linter import lint_artifact
from test_mk1_f5 import baseline, execution, fixture_set, tested_artifact


TARGET_PROVIDER = "openai"
TARGET_MODEL = "gpt-target"
TARGET_FAMILY = "openai-gpt-target"


def make_receipt(
    index: int,
    *,
    provider: str = TARGET_PROVIDER,
    model: str = TARGET_MODEL,
    family: str = TARGET_FAMILY,
    randomization_ref: str | None = None,
    identity_evidence_ref: str | None = None,
) -> dict:
    value = execution()
    value["execution_id"] = f"f6-real-{index}"
    value["runtime"] = {
        "provider": provider,
        "model": model,
        "family": family,
        "run_at": f"2026-08-27T0{index}:00:00Z",
        "identity_evidence_ref": identity_evidence_ref or f"runtime-evidence-{index:03d}",
    }
    value["review"] = {
        "reviewer_type": "human",
        "reviewer_ref": "reviewer-certification",
        "reviewed_at": f"2026-08-27T0{index}:10:00Z",
        "blinded": True,
        "randomization_ref": randomization_ref or f"blind-f6-{index:03d}",
    }
    return run_benchmark(tested_artifact(), baseline(), fixture_set(), value)


def source_bundle() -> tuple[dict, dict, dict, dict, list[dict]]:
    source = tested_artifact()
    b = baseline()
    fs = fixture_set()
    receipts = [make_receipt(1), make_receipt(2), make_receipt(3)]
    candidate = promote_improved(source, receipts[0])
    return source, candidate, b, fs, receipts


def test_certification_pass() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    receipt = build_certification_receipt(candidate, source, b, fs, receipts)
    assert receipt["status"] == "CERTIFICATION_PASS"
    assert receipt["eligible_for_certified"] is True
    assert receipt["independent_f5_receipt_count"] == 3
    assert receipt["target_runtime"] == {
        "provider": TARGET_PROVIDER,
        "model": TARGET_MODEL,
        "family": TARGET_FAMILY,
    }
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
        "target_runtime": receipt["target_runtime"],
        "independent_runs": receipt["independent_f5_receipt_count"],
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


def test_less_than_three_independent_receipts_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    try:
        build_certification_receipt(candidate, source, b, fs, receipts[:2])
    except ValueError as exc:
        assert "at least 3" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must reject underpowered same-runtime evidence")


def test_provider_drift_rejected() -> dict:
    return expect_rejected(
        [make_receipt(1), make_receipt(2), make_receipt(3, provider="other-provider")],
        "same target runtime",
    )


def test_model_drift_rejected() -> dict:
    return expect_rejected(
        [make_receipt(1), make_receipt(2), make_receipt(3, model="other-model")],
        "same target runtime",
    )


def test_family_drift_rejected() -> dict:
    return expect_rejected(
        [make_receipt(1), make_receipt(2), make_receipt(3, family="other-family")],
        "same target runtime",
    )


def test_runtime_identity_evidence_required() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    bad = copy.deepcopy(receipts[2])
    bad["runtime"].pop("identity_evidence_ref")
    try:
        build_certification_receipt(candidate, source, b, fs, [receipts[0], receipts[1], bad])
    except ValueError as exc:
        assert "integrity check failed" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must reject runtime identity evidence removal")


def test_distinct_runtime_identity_evidence_required() -> dict:
    return expect_rejected(
        [
            make_receipt(1, identity_evidence_ref="same-runtime-proof"),
            make_receipt(2, identity_evidence_ref="same-runtime-proof"),
            make_receipt(3),
        ],
        "distinct runtime identity evidence",
    )


def test_candidate_origin_receipt_required() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    evidence = [receipts[1], receipts[2], make_receipt(4)]
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
        make_receipt(1, randomization_ref="same-blind-seed"),
        make_receipt(2, randomization_ref="same-blind-seed"),
        make_receipt(3),
    ]
    return expect_rejected(receipts, "distinct blind randomization_ref")


def test_distinct_execution_required() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    duplicate = copy.deepcopy(receipts[2])
    duplicate["execution_id"] = receipts[1]["execution_id"]
    # Modifying the signed receipt is itself invalid; this still locks execution identity into the receipt.
    try:
        build_certification_receipt(candidate, source, b, fs, [receipts[0], receipts[1], duplicate])
    except ValueError as exc:
        assert "integrity check failed" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F6 must reject duplicate/tampered execution identity")


def test_tampered_f6_receipt_rejected() -> dict:
    source, candidate, b, fs, receipts = source_bundle()
    receipt = build_certification_receipt(candidate, source, b, fs, receipts)
    receipt["independent_f5_receipt_count"] = 4
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
        "minimum_independent_runs": test_less_than_three_independent_receipts_rejected(),
        "provider_drift": test_provider_drift_rejected(),
        "model_drift": test_model_drift_rejected(),
        "family_drift": test_family_drift_rejected(),
        "runtime_identity_evidence": test_runtime_identity_evidence_required(),
        "distinct_runtime_identity_evidence": test_distinct_runtime_identity_evidence_required(),
        "candidate_origin_receipt": test_candidate_origin_receipt_required(),
        "prompt_identity_freeze": test_prompt_drift_rejected(),
        "f5_receipt_integrity": test_tampered_f5_receipt_rejected(),
        "independent_blind_randomization": test_distinct_randomization_required(),
        "independent_execution_identity": test_distinct_execution_required(),
        "f6_receipt_integrity": test_tampered_f6_receipt_rejected(),
        "policy": "CERTIFIED requires the exact CANDIDATE to preserve 100% blocking pass and F5 superiority in at least three independent blinded benchmark executions on the same provider/model/family. Cross-provider portability is evaluated separately in F7."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
