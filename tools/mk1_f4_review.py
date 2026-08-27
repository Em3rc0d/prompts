from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from mk1_behavioral_runner import HUMAN_STATUSES, find_fixture_set, load, sha256_json, sha256_text


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def review_packet_id(immutable: dict) -> str:
    digest = hashlib.sha256(canonical_json(immutable).encode("utf-8")).hexdigest()[:16]
    return f"pq_mk1_f4_review_{digest}"


def _assert_collected_envelope(envelope: dict, fixture_set: dict) -> None:
    if envelope.get("mode") not in {"api", "manual-observed"}:
        raise ValueError("F4 review accepts only real observed execution envelopes")
    if envelope.get("collection_status") != "OBSERVED_OUTPUTS_PENDING_HUMAN_REVIEW":
        raise ValueError("F4 review requires OBSERVED_OUTPUTS_PENDING_HUMAN_REVIEW envelope")
    if envelope.get("artifact_id") != fixture_set.get("artifact_id"):
        raise ValueError("F4 review artifact/fixture-set mismatch")
    if envelope.get("artifact_version") != fixture_set.get("artifact_version"):
        raise ValueError("F4 review artifact version mismatch")
    if envelope.get("fixture_set_id") != fixture_set.get("fixture_set_id"):
        raise ValueError("F4 review fixture_set_id mismatch")
    if envelope.get("fixture_set_version") != fixture_set.get("version"):
        raise ValueError("F4 review fixture-set version mismatch")
    if envelope.get("fixture_set_fingerprint") != sha256_json(fixture_set):
        raise ValueError("F4 review fixture-set fingerprint mismatch")

    runtime = envelope.get("runtime") or {}
    missing_runtime = [key for key in ("provider", "model", "family", "run_at") if not runtime.get(key)]
    if missing_runtime:
        raise ValueError(f"F4 review envelope missing runtime identity: {missing_runtime}")

    responses = envelope.get("responses") or {}
    expected = {case["fixture_id"] for case in fixture_set.get("cases", [])}
    if set(responses) != expected:
        raise ValueError("F4 review response inventory does not match frozen fixture set")
    for fixture_id in sorted(expected):
        output = str((responses[fixture_id] or {}).get("output", ""))
        if not output.strip():
            raise ValueError(f"F4 review cannot review empty observed output: {fixture_id}")


def prepare_review_packet(envelope: dict, fixture_set: dict) -> dict:
    _assert_collected_envelope(envelope, fixture_set)
    cases = []
    for fixture in fixture_set.get("cases", []):
        fixture_id = fixture["fixture_id"]
        response = envelope["responses"][fixture_id]
        output = str(response["output"])
        cases.append({
            "fixture_id": fixture_id,
            "class": fixture.get("class"),
            "severity": fixture.get("severity", "normal"),
            "name": fixture.get("name"),
            "fixture_input": fixture.get("input", {}),
            "observed_output": output,
            "observed_output_fingerprint": sha256_text(output),
            "human_check_labels": list(fixture.get("expected", {}).get("human_checks", [])),
        })

    immutable = {
        "mk_stage": "MK1",
        "phase": "F4_REVIEW",
        "execution_id": envelope["execution_id"],
        "runtime": copy.deepcopy(envelope["runtime"]),
        "artifact_id": envelope["artifact_id"],
        "artifact_version": envelope["artifact_version"],
        "artifact_prompt_fingerprint": envelope["artifact_prompt_fingerprint"],
        "fixture_set_id": envelope["fixture_set_id"],
        "fixture_set_version": envelope["fixture_set_version"],
        "fixture_set_fingerprint": envelope["fixture_set_fingerprint"],
        "cases": cases,
    }
    review = {
        "reviewer_type": "human",
        "reviewer_ref": "",
        "reviewed_at": "",
        "judgments": {
            case["fixture_id"]: {
                label: {"status": "UNRESOLVED", "note": ""}
                for label in case["human_check_labels"]
            }
            for case in cases
        },
    }
    return {
        "review_packet_id": review_packet_id(immutable),
        "immutable": immutable,
        "review": review,
        "instructions": [
            "Review only the exact observed outputs in immutable.cases; do not edit immutable fields.",
            "For every human check, record PASS or FAIL with a concrete evidence note grounded in the observed output.",
            "Fill reviewer_ref and reviewed_at only after a human completes the review.",
            "UNRESOLVED is allowed while reviewing but cannot produce a passing F4 receipt.",
            "This packet does not itself promote TESTED state.",
        ],
    }


def _validate_packet_against_envelope(envelope: dict, fixture_set: dict, packet: dict) -> None:
    _assert_collected_envelope(envelope, fixture_set)
    immutable = packet.get("immutable") or {}
    supplied_id = packet.get("review_packet_id")
    expected_id = review_packet_id(immutable)
    if supplied_id != expected_id:
        raise ValueError(f"F4 review packet integrity check failed: expected {expected_id}, got {supplied_id}")

    expected_packet = prepare_review_packet(envelope, fixture_set)
    if immutable != expected_packet["immutable"]:
        raise ValueError("F4 review immutable payload does not match the collected execution envelope")


def apply_review(envelope: dict, fixture_set: dict, packet: dict) -> dict:
    _validate_packet_against_envelope(envelope, fixture_set, packet)
    review = packet.get("review") or {}
    if review.get("reviewer_type") != "human":
        raise ValueError("F4 review requires reviewer_type='human'")
    missing_review = [key for key in ("reviewer_ref", "reviewed_at") if not str(review.get(key, "")).strip()]
    if missing_review:
        raise ValueError(f"F4 review missing reviewer metadata: {missing_review}")

    judgments = review.get("judgments") or {}
    reviewed = copy.deepcopy(envelope)
    for fixture in fixture_set.get("cases", []):
        fixture_id = fixture["fixture_id"]
        expected_labels = list(fixture.get("expected", {}).get("human_checks", []))
        case_judgments = judgments.get(fixture_id) or {}
        if set(case_judgments) != set(expected_labels):
            raise ValueError(f"F4 review judgment inventory mismatch for {fixture_id}")
        reviewed_checks = {}
        for label in expected_labels:
            value = case_judgments[label]
            status = value.get("status") if isinstance(value, dict) else None
            note = value.get("note") if isinstance(value, dict) else None
            if status not in HUMAN_STATUSES or not str(note or "").strip():
                raise ValueError(f"F4 review incomplete for {fixture_id}::{label}; PASS/FAIL plus evidence note required")
            reviewed_checks[label] = {"status": status, "note": str(note)}
        reviewed["responses"][fixture_id]["human_checks"] = reviewed_checks

    reviewed["review"] = {
        "reviewer_type": "human",
        "reviewer_ref": str(review["reviewer_ref"]),
        "reviewed_at": str(review["reviewed_at"]),
    }
    reviewed["collection_status"] = "HUMAN_REVIEW_COMPLETE"
    reviewed["review_packet_id"] = packet["review_packet_id"]
    reviewed["instructions"] = [
        "This execution envelope contains immutable observed outputs plus completed human judgments.",
        "Run mk1_behavioral_runner.py against the exact artifact and fixture set to produce the F4 receipt.",
        "Do not edit prompt/output/runtime/frozen identity after review; prepare a new execution if anything changes.",
    ]
    return reviewed


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare")
    prepare.add_argument("--execution", required=True)
    prepare.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    prepare.add_argument("--output", required=True)

    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("--execution", required=True)
    apply_cmd.add_argument("--review-packet", required=True)
    apply_cmd.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    apply_cmd.add_argument("--output", required=True)

    args = parser.parse_args()
    execution = load(Path(args.execution))
    fixture_document = load(Path(args.fixtures))
    fixture_set = find_fixture_set(fixture_document, execution["fixture_set_id"])

    if args.command == "prepare":
        result = prepare_review_packet(execution, fixture_set)
    else:
        packet = load(Path(args.review_packet))
        result = apply_review(execution, fixture_set, packet)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "mk1_f4_review": args.command.upper(),
        "output": output.as_posix(),
        "review_packet_id": result.get("review_packet_id"),
        "status": result.get("collection_status", "PENDING_HUMAN_REVIEW"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
