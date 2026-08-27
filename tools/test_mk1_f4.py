from __future__ import annotations

import json
import tempfile
from pathlib import Path

from mk1_behavioral_runner import run_fixture_set, sha256_json, sha256_text
from mk1_materialize_f4_tested import materialize
from mk1_promote_tested import promote_tested


FIXTURE_PATH = Path("mk1/fixtures/f4/fixture-sets.json")


def artifact() -> dict:
    return {
        "id": "pq_mk1_test_behavior",
        "version": "0.1.0",
        "state": "VALID",
        "claims": ["engineered"],
        "prompt_body": "PURPOSE\nPreserve the observed fact that Alpha remains 42.\n",
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


def review_metadata() -> dict:
    return {
        "reviewer_type": "human",
        "reviewer_ref": "fixture-reviewer-01",
        "reviewed_at": "2026-08-26T22:56:00Z",
    }


def frozen_identity() -> dict:
    a = artifact()
    fs = fixture_set()
    return {
        "artifact_id": a["id"],
        "artifact_version": a["version"],
        "artifact_prompt_fingerprint": sha256_text(a["prompt_body"]),
        "fixture_set_id": fs["fixture_set_id"],
        "fixture_set_version": fs["version"],
        "fixture_set_fingerprint": sha256_json(fs),
    }


def real_execution(responses: dict | None = None) -> dict:
    return {
        "execution_id": "manual-observed-pass",
        "mode": "manual-observed",
        "runtime": {"provider": "test-provider", "model": "test-model", "run_at": "2026-08-26T22:55:00Z"},
        "review": review_metadata(),
        **frozen_identity(),
        "responses": responses if responses is not None else passing_response(),
    }


def real_pass_receipt() -> dict:
    return run_fixture_set(artifact(), fixture_set(), real_execution())


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
        {"execution_id": "synthetic-pass", "mode": "synthetic", "responses": passing_response()},
    )
    assert receipt["status"] == "HARNESS_CHARACTERIZATION", receipt
    assert receipt["eligible_for_tested"] is False, receipt
    assert receipt["blocking_failures"] == [], receipt
    assert receipt["artifact_prompt_fingerprint"].startswith("sha256:"), receipt
    assert receipt["fixture_set_fingerprint"].startswith("sha256:"), receipt

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
    assert receipt["review"]["reviewer_type"] == "human", receipt
    assert receipt["artifact_prompt_fingerprint"].startswith("sha256:"), receipt
    assert receipt["fixture_set_fingerprint"].startswith("sha256:"), receipt

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
    execution = real_execution({"happy": {"output": "Alpha remains 42."}})
    receipt = run_fixture_set(artifact(), fixture_set(), execution)
    assert receipt["status"] == "BEHAVIORAL_FAIL", receipt
    assert receipt["eligible_for_tested"] is False, receipt
    assert receipt["unresolved_blocking_human_checks"] == 1, receipt
    return {"status": receipt["status"], "unresolved": receipt["unresolved_blocking_human_checks"]}


def test_machine_failure_blocks() -> dict:
    response = passing_response()
    response["happy"]["output"] = "Alpha is now invented."
    execution = real_execution(response)
    execution["mode"] = "api"
    receipt = run_fixture_set(artifact(), fixture_set(), execution)
    assert receipt["status"] == "BEHAVIORAL_FAIL", receipt
    assert receipt["eligible_for_tested"] is False, receipt
    assert receipt["blocking_failures"] == ["happy"], receipt
    return {"status": receipt["status"], "blocking": receipt["blocking_failures"]}


def test_real_runtime_identity_required() -> dict:
    execution = real_execution()
    execution["runtime"] = {}
    try:
        run_fixture_set(artifact(), fixture_set(), execution)
    except ValueError as exc:
        assert "runtime identity" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Real execution without runtime identity should fail")


def test_human_review_metadata_required() -> dict:
    execution = real_execution()
    execution.pop("review")
    try:
        run_fixture_set(artifact(), fixture_set(), execution)
    except ValueError as exc:
        assert "reviewer_type='human'" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Real execution with human checks must identify human review")


def test_complete_observed_outputs_required() -> dict:
    execution = real_execution()
    execution["responses"] = {"happy": {"output": "", "human_checks": passing_response()["happy"]["human_checks"]}}
    try:
        run_fixture_set(artifact(), fixture_set(), execution)
    except ValueError as exc:
        assert "empty observed outputs" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Real execution cannot contain empty observed outputs")


def test_pre_execution_prompt_identity_drift_rejected() -> dict:
    execution = real_execution()
    execution["artifact_prompt_fingerprint"] = sha256_text("different prompt")
    try:
        run_fixture_set(artifact(), fixture_set(), execution)
    except ValueError as exc:
        assert "artifact_prompt_fingerprint" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Prepared execution must reject prompt identity drift")


def test_pre_execution_fixture_identity_drift_rejected() -> dict:
    execution = real_execution()
    execution["fixture_set_fingerprint"] = sha256_json({"changed": True})
    try:
        run_fixture_set(artifact(), fixture_set(), execution)
    except ValueError as exc:
        assert "fixture_set_fingerprint" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Prepared execution must reject fixture-set identity drift")


def test_receipt_identity_mismatch_rejected() -> dict:
    receipt = real_pass_receipt()
    receipt["artifact_version"] = "9.9.9"
    try:
        promote_tested(artifact(), receipt)
    except ValueError as exc:
        assert "artifact_version" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Mismatched receipt version must be rejected")


def test_prompt_fingerprint_mismatch_rejected() -> dict:
    receipt = real_pass_receipt()
    changed = artifact()
    changed["prompt_body"] += "CHANGED AFTER EXECUTION\n"
    try:
        promote_tested(changed, receipt)
    except ValueError as exc:
        assert "artifact_prompt_fingerprint" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Prompt drift after execution must invalidate F4 promotion")


def test_tampered_receipt_rejected() -> dict:
    receipt = real_pass_receipt()
    receipt["runtime"]["model"] = "tampered-model-id"
    try:
        promote_tested(artifact(), receipt)
    except ValueError as exc:
        assert "integrity check failed" in str(exc), exc
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Receipt content modified after receipt_id generation must be rejected")


def test_materializer_requires_real_receipt_and_builds_tested_bundle() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        receipts = root / "receipts"
        source = root / "f2"
        critics = root / "critics"
        output = root / "f4"
        receipts.mkdir()
        critics.mkdir()
        bundle = source / "test_behavior"
        bundle.mkdir(parents=True)

        (bundle / "artifact.json").write_text(json.dumps(artifact()), encoding="utf-8")
        (bundle / "prompt.txt").write_text("PROMPT", encoding="utf-8")
        (bundle / "architecture.json").write_text("{}", encoding="utf-8")
        (bundle / "lint.json").write_text('{"status":"PASS"}', encoding="utf-8")
        (critics / "test_behavior.critic.json").write_text('{"status":"PASS"}', encoding="utf-8")

        empty = materialize(receipts, source, critics, output)
        assert empty["status"] == "NO_REAL_RECEIPTS", empty
        assert empty["tested_artifact_count"] == 0, empty

        receipt = real_pass_receipt()
        (receipts / "observed.receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
        built = materialize(receipts, source, critics, output, require_at_least=1)
        assert built["tested_artifact_count"] == 1, built
        tested_path = output / "test_behavior" / "artifact.json"
        tested = json.loads(tested_path.read_text(encoding="utf-8"))
        assert tested["state"] == "TESTED", tested
        assert tested["evaluation"]["receipt_id"] == receipt["receipt_id"], tested
        assert (output / "test_behavior" / "behavioral_receipt.json").exists()
        assert (output / "test_behavior" / "critic.json").exists()

        return {"empty_status": empty["status"], "built_count": built["tested_artifact_count"], "state": tested["state"]}


def main() -> None:
    result = {
        "mk1_f4": "PASS",
        "fixture_inventory": test_fixture_inventory(),
        "synthetic_never_promotes": test_synthetic_never_promotes(),
        "real_pass_is_eligible_and_promotable": test_real_pass_is_eligible_and_promotable(),
        "unresolved_human_blocks": test_unresolved_human_check_blocks(),
        "machine_failure_blocks": test_machine_failure_blocks(),
        "runtime_identity_required": test_real_runtime_identity_required(),
        "human_review_metadata_required": test_human_review_metadata_required(),
        "complete_observed_outputs_required": test_complete_observed_outputs_required(),
        "pre_execution_prompt_drift_rejected": test_pre_execution_prompt_identity_drift_rejected(),
        "pre_execution_fixture_drift_rejected": test_pre_execution_fixture_identity_drift_rejected(),
        "receipt_identity_mismatch_rejected": test_receipt_identity_mismatch_rejected(),
        "prompt_fingerprint_mismatch_rejected": test_prompt_fingerprint_mismatch_rejected(),
        "tampered_receipt_rejected": test_tampered_receipt_rejected(),
        "tested_materializer": test_materializer_requires_real_receipt_and_builds_tested_bundle(),
        "policy": "F4 CI characterizes harness, frozen pre-execution identity, immutable evidence identity, human-review metadata, promotion guardrails and materialization mechanics only. No real prompt execution or TESTED artifact is claimed by this test suite.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
