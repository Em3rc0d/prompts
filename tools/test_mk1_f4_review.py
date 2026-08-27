from __future__ import annotations

import copy
import json

from mk1_behavioral_runner import run_fixture_set
from mk1_f4_review import apply_review, prepare_review_packet
from mk1_runtime_collect import collect_execution


def artifact() -> dict:
    return {
        "id": "pq_mk1_f4_review_test",
        "version": "0.1.0",
        "state": "VALID",
        "prompt_body": "Rewrite {text} without changing Alpha 42.",
    }


def fixture_set() -> dict:
    return {
        "fixture_set_id": "pq_mk1_fs_f4_review_test_v1",
        "version": "0.1.0",
        "artifact_id": "pq_mk1_f4_review_test",
        "artifact_version": "0.1.0",
        "cases": [{
            "fixture_id": "happy",
            "class": "happy-path",
            "severity": "blocking",
            "name": "Preserve fact",
            "input": {"variables": {"text": "Alpha remains 42."}},
            "expected": {
                "machine_assertions": [{"type": "contains_all", "values": ["Alpha", "42"]}],
                "human_checks": ["Meaning is preserved"],
            },
        }],
    }


def observed() -> dict:
    return collect_execution(
        artifact(),
        fixture_set(),
        "openai",
        "test-model",
        "f4-review-observed",
        lambda _: ("Alpha remains 42.", {"response_id": "fake-1"}),
        run_at="2026-08-27T01:20:00Z",
    )


def completed_packet() -> dict:
    packet = prepare_review_packet(observed(), fixture_set())
    packet["review"]["reviewer_ref"] = "reviewer-01"
    packet["review"]["reviewed_at"] = "2026-08-27T01:25:00Z"
    packet["review"]["judgments"]["happy"]["Meaning is preserved"] = {
        "status": "PASS",
        "note": "The reviewed output preserves both Alpha and the value 42 without adding a new claim.",
    }
    return packet


def test_successful_review_application() -> dict:
    envelope = observed()
    packet = completed_packet()
    reviewed = apply_review(envelope, fixture_set(), packet)
    assert reviewed["collection_status"] == "HUMAN_REVIEW_COMPLETE"
    assert reviewed["review"]["reviewer_ref"] == "reviewer-01"
    assert reviewed["responses"]["happy"]["output"] == envelope["responses"]["happy"]["output"]
    receipt = run_fixture_set(artifact(), fixture_set(), reviewed)
    assert receipt["status"] == "BEHAVIORAL_PASS"
    assert receipt["eligible_for_tested"] is True
    return {"review_status": reviewed["collection_status"], "receipt_status": receipt["status"]}


def test_output_tampering_rejected() -> dict:
    envelope = observed()
    packet = completed_packet()
    packet["immutable"]["cases"][0]["observed_output"] = "Tampered output"
    # Keep the old id: integrity must fail before anything is applied.
    try:
        apply_review(envelope, fixture_set(), packet)
    except ValueError as exc:
        assert "integrity check failed" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F4 review must reject tampered immutable output")


def test_packet_rehash_does_not_hide_envelope_drift() -> dict:
    envelope = observed()
    packet = completed_packet()
    packet["immutable"]["cases"][0]["observed_output"] = "Tampered but rehashed"
    from mk1_f4_review import review_packet_id
    packet["review_packet_id"] = review_packet_id(packet["immutable"])
    try:
        apply_review(envelope, fixture_set(), packet)
    except ValueError as exc:
        assert "does not match the collected execution envelope" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Rehashing a modified review packet must not bypass envelope identity")


def test_incomplete_check_rejected() -> dict:
    packet = completed_packet()
    packet["review"]["judgments"]["happy"]["Meaning is preserved"] = {"status": "PASS", "note": ""}
    try:
        apply_review(observed(), fixture_set(), packet)
    except ValueError as exc:
        assert "PASS/FAIL plus evidence note required" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F4 completed review requires evidenced judgments")


def test_reviewer_metadata_required() -> dict:
    packet = completed_packet()
    packet["review"]["reviewer_ref"] = ""
    try:
        apply_review(observed(), fixture_set(), packet)
    except ValueError as exc:
        assert "reviewer metadata" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F4 review requires human reviewer metadata")


def test_review_application_cannot_modify_runtime() -> dict:
    envelope = observed()
    packet = completed_packet()
    reviewed = apply_review(envelope, fixture_set(), packet)
    assert reviewed["runtime"] == envelope["runtime"]
    assert reviewed["artifact_prompt_fingerprint"] == envelope["artifact_prompt_fingerprint"]
    assert reviewed["fixture_set_fingerprint"] == envelope["fixture_set_fingerprint"]
    return {"runtime_frozen": True, "prompt_frozen": True, "fixtures_frozen": True}


def main() -> None:
    print(json.dumps({
        "mk1_f4_review": "PASS",
        "successful_application": test_successful_review_application(),
        "tamper_detection": test_output_tampering_rejected(),
        "rehash_attack": test_packet_rehash_does_not_hide_envelope_drift(),
        "complete_judgments": test_incomplete_check_rejected(),
        "reviewer_metadata": test_reviewer_metadata_required(),
        "identity_freeze": test_review_application_cannot_modify_runtime(),
        "policy": "F4 review may add only explicit human judgments to the exact observed execution; it cannot rewrite outputs, runtime identity, prompt identity or fixture identity."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
