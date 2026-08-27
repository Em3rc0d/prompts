from __future__ import annotations

import argparse
import json
from pathlib import Path

POLICY_PATH = Path("mk0/harvester/POLICY.json")


def load_policy(path: Path = POLICY_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def aggregate_confidence(confidence: dict, policy: dict) -> float:
    required = policy["aggregate_confidence"]["required_dimensions"]
    values = [float(confidence[name]) for name in required]
    return min(values)


def route_candidate(record: dict, policy: dict) -> tuple[str, list[str], float]:
    confidence = record["confidence"]
    aggregate = aggregate_confidence(confidence, policy)
    flags = set(record.get("critical_flags", []))
    overrides = policy["critical_overrides"]

    reject = flags.intersection(overrides["force_reject"])
    if reject:
        return "REJECTED", [f"force_reject:{x}" for x in sorted(reject)], aggregate

    blocked = flags.intersection(overrides["block_auto_candidate"])
    forced_review = flags.intersection(overrides["force_human_review"])

    if blocked or forced_review:
        reasons = [f"block_auto:{x}" for x in sorted(blocked)]
        reasons += [f"force_review:{x}" for x in sorted(forced_review)]
        return "HUMAN_REVIEW_REQUIRED", reasons, aggregate

    routing = policy["routing"]
    if aggregate >= float(routing["auto_candidate_min_confidence"]):
        return "GOLDEN_CANDIDATE", ["confidence_at_or_above_auto_candidate_threshold"], aggregate

    if aggregate >= float(routing["human_review_min_confidence"]):
        return "HUMAN_REVIEW_REQUIRED", ["confidence_in_human_review_band"], aggregate

    return routing["below_human_review_default"], ["confidence_below_human_review_threshold"], aggregate


def apply_route(record: dict, policy: dict) -> dict:
    route, reasons, aggregate = route_candidate(record, policy)
    output = dict(record)
    output["confidence"] = dict(record["confidence"])
    output["confidence"]["aggregate"] = aggregate
    output["route"] = route
    output["route_reasons"] = reasons
    output["stage"] = route
    output["policy_version"] = policy["policy_version"]
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Route an MK0 Harvester candidate")
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--policy", type=Path, default=POLICY_PATH)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    policy = load_policy(args.policy)
    record = json.loads(args.candidate.read_text(encoding="utf-8"))
    routed = apply_route(record, policy)
    encoded = json.dumps(routed, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
