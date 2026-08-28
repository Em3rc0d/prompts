from __future__ import annotations

import argparse
import json
from pathlib import Path

POLICY_PATH = Path("mk0/harvester/POLICY.json")


def load_policy(path: Path = POLICY_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def aggregate_confidence(confidence: dict, policy: dict) -> float:
    required = policy["aggregate_confidence"]["required_dimensions"]
    return min(float(confidence[name]) for name in required)


def evaluate_eligibility(record: dict, policy: dict) -> dict:
    flags = set(record.get("critical_flags", []))
    overrides = policy["critical_overrides"]
    force_reject = flags.intersection(overrides["force_reject"])
    research_blockers = flags.intersection(overrides["block_research_auto_candidate"])
    distribution_blockers = flags.intersection(overrides["block_distribution"])
    semantic = record.get("semantic_gate", {})
    disposition = semantic.get("disposition")
    semantic_research_block = disposition in {"REFERENCE_CORPUS", "REJECT"}
    semantic_distribution_block = disposition != "GOLDEN_EVALUATION"

    research_eligible = not force_reject and not research_blockers and not semantic_research_block
    distribution_eligible = not force_reject and not distribution_blockers and not semantic_distribution_block

    research_reasons = ([f"force_reject:{x}" for x in sorted(force_reject)] +
                        [f"research_block:{x}" for x in sorted(research_blockers)])
    distribution_reasons = ([f"force_reject:{x}" for x in sorted(force_reject)] +
                            [f"distribution_block:{x}" for x in sorted(distribution_blockers)])
    if semantic_research_block:
        research_reasons.append(f"semantic_gate:{disposition.casefold()}")
    if semantic_distribution_block:
        distribution_reasons.append(f"semantic_gate:{(disposition or 'unknown').casefold()}")
    return {
        "golden_research_eligibility": {"eligible": research_eligible, "reasons": research_reasons or ["research_gate_pass"]},
        "distribution_eligibility": {"eligible": distribution_eligible, "reasons": distribution_reasons or ["distribution_gate_pass"]},
    }


def route_candidate(record: dict, policy: dict) -> tuple[str, list[str], float]:
    aggregate = aggregate_confidence(record["confidence"], policy)
    semantic = record.get("semantic_gate", {})
    disposition = semantic.get("disposition")
    artifact_class = semantic.get("artifact_class", "UNKNOWN")

    # Semantic identity precedes quality/confidence. Polished documentation is still documentation.
    if disposition == "REJECT":
        return "REJECTED", [f"semantic_reject:{artifact_class}"], aggregate
    if disposition == "REFERENCE_CORPUS":
        return "HOLD", [f"reference_corpus:{artifact_class}"], aggregate
    if disposition == "HUMAN_REVIEW":
        return "HUMAN_REVIEW_REQUIRED", [f"semantic_ambiguous:{artifact_class}"], aggregate

    flags = set(record.get("critical_flags", []))
    overrides = policy["critical_overrides"]
    reject = flags.intersection(overrides["force_reject"])
    if reject:
        return "REJECTED", [f"force_reject:{x}" for x in sorted(reject)], aggregate
    research_blocked = flags.intersection(overrides["block_research_auto_candidate"])
    forced_review = flags.intersection(overrides["force_human_review"])
    if research_blocked or forced_review:
        reasons = [f"research_block:{x}" for x in sorted(research_blocked)]
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
    output["eligibility"] = evaluate_eligibility(record, policy)
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
