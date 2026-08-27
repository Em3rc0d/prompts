from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from mk1_behavioral_runner import HUMAN_STATUSES, sha256_json, sha256_text
from mk1_f5_benchmark import find_baseline, find_fixture_set, load
from mk1_f5_runtime_collect import SIDES, blind_key_id, packet_id


BLIND_WINNERS = {"A", "B", "tie"}


def _blind_key_core(blind_key: dict) -> dict:
    core = copy.deepcopy(blind_key)
    core.pop("blind_key_id", None)
    core.pop("warning", None)
    return core


def _validate_blind_key(blind_key: dict) -> None:
    core = _blind_key_core(blind_key)
    supplied = blind_key.get("blind_key_id")
    expected = blind_key_id(core)
    if supplied != expected:
        raise ValueError(f"F5 blind-key integrity check failed: expected {expected}, got {supplied}")
    mapping = blind_key.get("mapping") or {}
    if blind_key.get("randomization_ref") != sha256_json(mapping):
        raise ValueError("F5 blind-key randomization_ref does not match blind mapping")
    for pair_key, assignment in mapping.items():
        if set(assignment) != set(SIDES) or set(assignment.values()) != {"engineered", "baseline"}:
            raise ValueError(f"F5 blind-key has invalid A/B assignment: {pair_key}")


def _validate_source_identity(observation: dict, tested_artifact: dict, baseline: dict, fixture_set: dict) -> None:
    frozen = {
        "artifact_id": tested_artifact["id"],
        "artifact_version": tested_artifact["version"],
        "engineered_prompt_fingerprint": sha256_text(tested_artifact["prompt_body"]),
        "baseline_id": baseline["baseline_id"],
        "baseline_prompt_fingerprint": sha256_text(baseline["prompt_body"]),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version", "1"),
        "fixture_set_fingerprint": sha256_json(fixture_set),
        "parent_f4_receipt_id": tested_artifact["evaluation"]["receipt_id"],
    }
    for key, expected in frozen.items():
        if observation.get(key) != expected:
            raise ValueError(f"F5 observation source identity drift for {key}: expected {expected!r}, got {observation.get(key)!r}")
    if observation.get("collection_status") != "OBSERVED_PAIRED_OUTPUTS_PENDING_BLIND_HUMAN_REVIEW":
        raise ValueError("F5 finalizer requires pending blinded observation")


def _observation_index(observation: dict) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for repeat in observation.get("semantic_repeats") or []:
        repeat_id = repeat.get("repeat")
        for fixture_id, pair in (repeat.get("pairs") or {}).items():
            key = f"r{repeat_id}:{fixture_id}"
            if key in index:
                raise ValueError(f"Duplicate F5 observation pair: {key}")
            index[key] = pair
    if len(index) != int(observation.get("pair_count") or 0):
        raise ValueError("F5 observation pair_count mismatch")
    return index


def _validate_review_packet(observation: dict, blind_key: dict, packet: dict, fixture_set: dict) -> dict[str, dict]:
    immutable = packet.get("immutable") or {}
    supplied_packet_id = packet.get("review_packet_id")
    expected_packet_id = packet_id(immutable)
    if supplied_packet_id != expected_packet_id:
        raise ValueError(f"F5 review-packet integrity check failed: expected {expected_packet_id}, got {supplied_packet_id}")
    if immutable.get("execution_id") != observation.get("execution_id"):
        raise ValueError("F5 review packet execution_id mismatch")
    if immutable.get("runtime") != observation.get("runtime"):
        raise ValueError("F5 review packet runtime mismatch")
    for key in (
        "artifact_id", "artifact_version", "engineered_prompt_fingerprint", "baseline_id",
        "baseline_prompt_fingerprint", "fixture_set_id", "fixture_set_version",
        "fixture_set_fingerprint", "parent_f4_receipt_id", "repeat_count", "pair_count"
    ):
        if immutable.get(key) != observation.get(key):
            raise ValueError(f"F5 review packet frozen identity mismatch for {key}")
    if immutable.get("randomization_ref") != blind_key.get("randomization_ref"):
        raise ValueError("F5 review packet randomization_ref mismatch")

    observation_pairs = _observation_index(observation)
    mapping = blind_key.get("mapping") or {}
    packet_pairs = immutable.get("pairs") or []
    if len(packet_pairs) != len(observation_pairs) or set(mapping) != set(observation_pairs):
        raise ValueError("F5 review packet/blind-key/observation inventory mismatch")

    fixtures = {row["fixture_id"]: row for row in fixture_set.get("cases", [])}
    by_key: dict[str, dict] = {}
    for pair in packet_pairs:
        pair_key = pair.get("pair_key")
        if pair_key in by_key:
            raise ValueError(f"Duplicate F5 review pair: {pair_key}")
        if pair_key not in observation_pairs or pair_key not in mapping:
            raise ValueError(f"Unknown F5 review pair: {pair_key}")
        fixture_id = pair.get("fixture_id")
        fixture = fixtures.get(fixture_id)
        if not fixture:
            raise ValueError(f"F5 review pair references unknown fixture: {fixture_id}")
        if pair.get("fixture_input") != fixture.get("input", {}):
            raise ValueError(f"F5 review fixture input drift: {pair_key}")

        semantic = observation_pairs[pair_key]
        assignment = mapping[pair_key]
        sides = pair.get("sides") or {}
        if set(sides) != set(SIDES):
            raise ValueError(f"F5 review pair lacks exact A/B sides: {pair_key}")
        for side in SIDES:
            participant = assignment[side]
            observed = semantic[participant]
            packet_side = sides[side]
            if packet_side.get("observed_output") != observed.get("output"):
                raise ValueError(f"F5 review output drift detected for {pair_key}:{side}")
            if packet_side.get("observed_output_fingerprint") != observed.get("output_fingerprint"):
                raise ValueError(f"F5 review output fingerprint drift for {pair_key}:{side}")
            if observed.get("output_fingerprint") != sha256_text(str(observed.get("output", ""))):
                raise ValueError(f"F5 observation output fingerprint invalid for {pair_key}:{participant}")
            expected_labels = list(fixture.get("expected", {}).get("human_checks", []))
            if packet_side.get("human_check_labels") != expected_labels:
                raise ValueError(f"F5 review human-check labels drift for {pair_key}:{side}")
        by_key[pair_key] = pair
    return by_key


def finalize_review(observation: dict, blind_key: dict, packet: dict, tested_artifact: dict, baseline: dict, fixture_set: dict) -> dict:
    _validate_blind_key(blind_key)
    _validate_source_identity(observation, tested_artifact, baseline, fixture_set)
    packet_pairs = _validate_review_packet(observation, blind_key, packet, fixture_set)
    if blind_key.get("execution_id") != observation.get("execution_id"):
        raise ValueError("F5 blind-key execution_id mismatch")
    for key in (
        "artifact_id", "artifact_version", "engineered_prompt_fingerprint", "baseline_id",
        "baseline_prompt_fingerprint", "fixture_set_id", "fixture_set_version",
        "fixture_set_fingerprint", "parent_f4_receipt_id"
    ):
        if blind_key.get(key) != observation.get(key):
            raise ValueError(f"F5 blind-key frozen identity mismatch for {key}")

    review = packet.get("review") or {}
    if review.get("reviewer_type") != "human" or review.get("blinded") is not True:
        raise ValueError("F5 finalizer requires blinded human review")
    missing_review = [key for key in ("reviewer_ref", "reviewed_at") if not str(review.get(key, "")).strip()]
    if missing_review:
        raise ValueError(f"F5 finalizer missing reviewer metadata: {missing_review}")

    fixtures = {row["fixture_id"]: row for row in fixture_set.get("cases", [])}
    observation_pairs = _observation_index(observation)
    mapping = blind_key["mapping"]
    judgments = review.get("pair_judgments") or {}
    if set(judgments) != set(packet_pairs):
        raise ValueError("F5 review judgment inventory mismatch")

    repeat_rows: dict[int, dict] = {}
    for pair_key, pair in packet_pairs.items():
        repeat_id = int(pair["repeat"])
        fixture_id = pair["fixture_id"]
        fixture = fixtures[fixture_id]
        judgment = judgments[pair_key]
        if set(key for key in judgment if key in SIDES) != set(SIDES):
            raise ValueError(f"F5 review missing A/B judgments for {pair_key}")

        semantic_responses: dict[str, dict] = {}
        for side in SIDES:
            participant = mapping[pair_key][side]
            side_judgments = judgment.get(side) or {}
            expected_labels = list(fixture.get("expected", {}).get("human_checks", []))
            if set(side_judgments) != set(expected_labels):
                raise ValueError(f"F5 {side} human-check inventory mismatch for {pair_key}")
            human_checks = {}
            for label in expected_labels:
                value = side_judgments[label]
                status = value.get("status") if isinstance(value, dict) else None
                note = value.get("note") if isinstance(value, dict) else None
                if status not in HUMAN_STATUSES or not str(note or "").strip():
                    raise ValueError(f"F5 blind review incomplete for {pair_key}:{side}:{label}")
                human_checks[label] = {"status": status, "note": str(note)}
            observed = observation_pairs[pair_key][participant]
            semantic_responses[participant] = {
                "output": observed["output"],
                "human_checks": human_checks,
                "provider_metadata": observed.get("provider_metadata"),
            }

        preference = judgment.get("preference") or {}
        blind_winner = preference.get("winner")
        pref_note = preference.get("note")
        if blind_winner not in BLIND_WINNERS or not str(pref_note or "").strip():
            raise ValueError(f"F5 blind preference incomplete for {pair_key}; A/B/tie plus evidence note required")
        if blind_winner == "tie":
            semantic_winner = "tie"
        else:
            semantic_winner = mapping[pair_key][blind_winner]

        repeat_rows.setdefault(repeat_id, {"repeat": repeat_id, "pairs": {}})["pairs"][fixture_id] = {
            "engineered": semantic_responses["engineered"],
            "baseline": semantic_responses["baseline"],
            "preference": {"winner": semantic_winner, "note": str(pref_note)},
        }

    repeats = [repeat_rows[key] for key in sorted(repeat_rows)]
    if len(repeats) != int(observation.get("repeat_count") or 0):
        raise ValueError("F5 finalized repeat inventory mismatch")

    return {
        "execution_id": observation["execution_id"],
        "mode": "api",
        "runtime": copy.deepcopy(observation["runtime"]),
        "review": {
            "reviewer_type": "human",
            "reviewer_ref": str(review["reviewer_ref"]),
            "reviewed_at": str(review["reviewed_at"]),
            "blinded": True,
            "randomization_ref": blind_key["randomization_ref"],
        },
        "artifact_id": observation["artifact_id"],
        "artifact_version": observation["artifact_version"],
        "engineered_prompt_fingerprint": observation["engineered_prompt_fingerprint"],
        "baseline_id": observation["baseline_id"],
        "baseline_prompt_fingerprint": observation["baseline_prompt_fingerprint"],
        "fixture_set_id": observation["fixture_set_id"],
        "fixture_set_version": observation["fixture_set_version"],
        "fixture_set_fingerprint": observation["fixture_set_fingerprint"],
        "parent_f4_receipt_id": observation["parent_f4_receipt_id"],
        "repeats": repeats,
        "blind_review_provenance": {
            "review_packet_id": packet["review_packet_id"],
            "blind_key_id": blind_key["blind_key_id"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observation", required=True)
    parser.add_argument("--blind-key", required=True)
    parser.add_argument("--review-packet", required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--baselines", default="mk1/baselines/f5/task-equivalent-minimal.json")
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    observation = load(args.observation)
    blind_key = load(args.blind_key)
    packet = load(args.review_packet)
    artifact = load(args.artifact)
    baseline_doc = load(args.baselines)
    fixture_doc = load(args.fixtures)
    baseline = find_baseline(baseline_doc, artifact["id"])
    fixture_set = find_fixture_set(fixture_doc, artifact["id"])
    execution = finalize_review(observation, blind_key, packet, artifact, baseline, fixture_set)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(execution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "mk1_f5_blind_review": "FINALIZED",
        "execution_id": execution["execution_id"],
        "family": execution["runtime"]["family"],
        "repeats": len(execution["repeats"]),
        "randomization_ref": execution["review"]["randomization_ref"],
        "output": output.as_posix(),
        "policy": "Finalization reveals A/B mapping only after completed human review and does not itself claim improvement."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
