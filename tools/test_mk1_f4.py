from __future__ import annotations

import json
from pathlib import Path

from mk1_behavioral_runner import run_fixture_set


FIXTURE_PATH = Path("mk1/fixtures/f4/fixture-sets.json")


def artifact() -> dict:
    return {
        "id": "pq_mk1_test_behavior",
        "version": "0.1.0",
        "state": "VALID",
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
    return {"status": receipt["status"], "eligible": receipt["eligible_for_tested"]}


def test_real_pass_is_eligible() -> dict:
    receipt = run_fixture_set(
        artifact(),
        fixture_set(),
        {
            "execution_id": "manual-observed-pass",
            "mode": "manual-observed",
            "runtime": {"provider": "test-provider", "model": "test-model", "run_at": "2026-08-26T22:55:00Z"},
            "responses": passing_response(),
        },
    )
    assert receipt["status"] == "BEHAVIORAL_PASS", receipt
    assert receipt["eligible_for_tested"] is True, receipt
    assert receipt["receipt_id"].startswith("pq_mk1_f4_receipt_"), receipt
    return {"status": receipt["status"], "eligible": receipt["eligible_for_tested"]}


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


def main() -> None:
    result = {
        "mk1_f4": "PASS",
        "fixture_inventory": test_fixture_inventory(),
        "synthetic_never_promotes": test_synthetic_never_promotes(),
        "real_pass_is_eligible": test_real_pass_is_eligible(),
        "unresolved_human_blocks": test_unresolved_human_check_blocks(),
        "machine_failure_blocks": test_machine_failure_blocks(),
        "runtime_identity_required": test_real_runtime_identity_required(),
        "policy": "F4 CI characterizes the behavioral harness only. No real prompt execution or TESTED state is claimed by this test suite.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
