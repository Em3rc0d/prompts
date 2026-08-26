from __future__ import annotations

import json
from pathlib import Path

from mk1_behavioral_runner import run_fixture_set
from mk1_promote_tested import promote_tested


FIXTURE_PATH = Path("mk1/fixtures/f4/fixture-sets.json")


def artifact() -> dict:
    return {
        "id": "pq_mk1_test_behavior",
        "version": "0.1.0",
        "state": "VALID",
        "claims": ["engineered"],
        "provenance": {
            "mk0_inputs": [],
            "patterns": [],
            "fixtures": [],
            "source_families": [],
        },
        "evaluation": {
            "baseline_id": None,
            "fixture_set_id": None,
            "receipt_id": None,
            "rubric_score": None,
            "blocking_failures": [],
        },
        "updated_at": None,
    }


def fixture_set() -> dict:
    return {
        "fixture_set_id": "pq_mk1_fs_test_behavior_v1",
        "version": "0.1.0",
        "artifact_id": "pq_mk1_test_behavior",
        "artifact_version": "0.1.0",
        "cases": [
            {
                "fixture_id": "happy",
                "class": "happy-path",
                "severity": "blocking",
                "expected": {
                    "machine_assertions": [
                        {"type": "contains_all", "values": ["alpha", "42"]},
                        {"type": "not_contains_any", "values": ["invented"]},
                    ],
                    "human_checks": ["Meaning is preserved"],
                },
            }
        ],
    }


def passing_response() -> dict:
    return {
        "happy": {
            "output": "Alpha remains 42.",
            "human_checks": {"Meaning is preserved": {"status": "PASS", "note": "Reviewed fixture output."}},
        }
    }


def real_pass_receipt() -> dict:
    return run_fixture_set(
        artifact(),
        fixture_set(),
        {
            "execution_id": "manual-observed-pass",
            "mode": "manual-observed",
            "runtime": {"provider": "test-provider", "model": "test-model", "run_at": "2026-08-26T22:55:00Z"},
            "responses": passing_response(),
        },
    )


def test_fixture_inventory() -> dict:
    document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    sets = document["fixture_sets"]
    assert len(sets) == 3, sets
    assert sum(len(item["cases"]) for item in sets) == 15, sets

    expected_ids = {
        "pq_mk1_fs_content_clear_rewrite_v1",
        "pq_mk1_fs_software_code_review_v1",
        "pq_mk1_fs_research_technical_decision_v1",
    }
    assert {item["fixture_set_id"] for item in sets} == expected_ids

    observed_classes = {case["class"] for item in sets for case in item["cases"]}
    required_classes = {"happy-path", "minimal", "missing-critical", "ambiguous", "contradictory", "edge", "noise", "regression"}
    assert required_classes <= observed_classes, observed_classes

    for item in sets:
        assert item["artifact_id"].startswith("pq_mk1_"), item
        assert item["artifact_version"] == "0.1.0", item
        for case in item["cases"]:
            assert case["severity"] in {"normal", "blocking"}, case
            assert case["expected"]["machine_assertions"], case
            assert case["expected"]["human_checks"], case

    return {"fixture_sets": len(sets), "fixtures": 15, "classes": sorted(observed_classes)}


def test_synthetic_never_promotes() -> dict:
    receipt = run_fixture_set(
        artifact(),
        fixture_set(),
        {
            "execution_id": "synthetic-pass",
            "mode": "synthetic",
            "responses": passing_response(),
        },
    )
    assert receipt["status"] == "HARNESS_CHARACTERIZATION", receipt
    assert receipt["eligible_for_tested"] is False, receipt
    assert receipt["blocking_failures"] == [], receipt

    try:
        promote_tested(artifact(), receipt)
    except ValueError as exc:
        assert "cannot promote" in str(exc).lower(), exc
    else:
        raise AssertionError("Synthetic receipt must never promote to TESTED")

    return {"status": receipt["status"], "eligible": receipt["eligible_for_tested"], "promotion_rejected": True}


def test_real_pass_is_eligible_and_promotable() -> dict:
    receipt = real_pass_receipt()
    assert receipt["status"] == "BEHAVIORAL_PASS", receipt
    assert receipt["eligible_for_tested"] is True, receipt
    assert receipt["receipt_id"].startswith("pq_mk1_f4_receipt_"), receipt

    promoted = promote_tested(artifact(), receipt)
    assert promoted["state"] == "TESTED", promoted
    assert "tested" in promoted["claims"], promoted
    assert promoted["evaluation"]["fixture_set_id"] == receipt["fixture_set_id"], promoted
    assert promoted["evaluation"]["receipt_id"] == receipt["receipt_id"], promoted
    assert promoted["evaluation"]["baseline_id"] is None, promoted
    assert promoted["evaluation"]["rubric_score"] is None, promoted
    assert promoted["updated_at"] == receipt["runtime"]["run_at"], promoted

    return {"status": receipt["status"], "eligible": receipt["eligible_for_tested"], "promoted_state": promoted["state"]}


def test_unresolved_human_check_blocks() -> dict:
    receipt = run_fixture_set(
        artifact(),
        fixture_set(),
        {
            "execution_id": "human-unresolved",
            "mode": "manual-observed",
            "runtime": {"provider": "test-provider", "model": "test-model", "run_at": "2026-08-26T22:55:00Z"},
            "responses": {"happy": {"output": "Alpha remains 42."}},
        },
    )
    assert receipt["status"] == "BEHAVIORAL_FAIL", receipt
    assert receipt["eligible_for_tested"] is False, receipt
    assert receipt["unresolved_blocking_human_checks"] == 1, receipt
    return {"status": receipt["status"], "unresolved": receipt["unresolved_blocking_human_checks"]}


def test_machine_failure_blocks() -> dict:
    response = passing_response()
    response["happy"]["output"] = "Alpha is now invented."
    receipt = run_fixture_set(
        artifact(),
        fixture_set(),
        {
            "execution_id": "machine-fail",
            "mode": "api",
            "runtime": {"provider": "test-provider", "model": "test-model", "run_at": "2026-08-26T22:55:00Z"},
            "responses": response,
        },
    )
    assert receipt["status"] == "BEHAVIORAL_FAIL", receipt
    assert receipt["eligible_for_tested"] is False, receipt
    assert receipt["blocking_failures"] == ["happy"], receipt
    return {"status": receipt["status"], "blocking": receipt["blocking_failures"]}


def test_real_runtime_identity_required() -> dict:
    try:
        run_fixture_set(
            artifact(),
            fixture_set(),
            {"execution_id": "bad-runtime", "mode": "api", "responses": passing_response()},
        )
    except ValueError as exc:
        assert "runtime identity" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Real execution without runtime identity should fail")


def test_receipt_identity_mismatch_rejected() -> dict:
    receipt = real_pass_receipt()
    receipt["artifact_version"] = "9.9.9"
    try:
        promote_tested(artifact(), receipt)
    except ValueError as exc:
        assert "artifact_version" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Mismatched receipt version must be rejected")


def main() -> None:
    result = {
        "mk1_f4": "PASS",
        "fixture_inventory": test_fixture_inventory(),
        "synthetic_never_promotes": test_synthetic_never_promotes(),
        "real_pass_is_eligible_and_promotable": test_real_pass_is_eligible_and_promotable(),
        "unresolved_human_blocks": test_unresolved_human_check_blocks(),
        "machine_failure_blocks": test_machine_failure_blocks(),
        "runtime_identity_required": test_real_runtime_identity_required(),
        "receipt_identity_mismatch_rejected": test_receipt_identity_mismatch_rejected(),
        "policy": "F4 CI characterizes harness and state-transition guardrails only. No real prompt execution or TESTED artifact is claimed by this test suite.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
