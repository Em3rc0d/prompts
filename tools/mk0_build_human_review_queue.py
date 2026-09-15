from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

DEFAULT_CANDIDATES = Path("mk0/golden-dataset/candidate-queue/batch-001.jsonl")
QUEUE_ROOT = Path("mk0/golden-dataset/human-review-queue")
ANALYSIS_ROOT = Path("mk0/analysis/harvester")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def safe_policy_tag(version: str) -> str:
    return "v" + version.replace(".", "-")


def priority(candidate: dict) -> tuple[int, str, list[str]]:
    semantic = candidate["semantic_gate"]
    c = candidate["confidence"]["aggregate"]
    flags = set(candidate.get("critical_flags", []))

    # Highest calibration value: unresolved semantic identity that already met
    # the policy threshold or a critical override. Human decisions here improve
    # the semantic gate rather than merely accepting a score.
    if semantic["disposition"] == "HUMAN_REVIEW":
        reasons = ["semantic_identity_unresolved"]
        if 0.90 <= c < 0.95:
            reasons.append("owner_validation_band")
        reasons.extend(sorted(flags.intersection({"conflicting_classifiers", "high_novelty_ambiguous_mapping"})))
        return 1, "P1_SEMANTIC_CALIBRATION", reasons

    # Prompt/agent artifacts already passed semantic identity but still require
    # owner review due to confidence or critical routing rules.
    if semantic["disposition"] == "GOLDEN_EVALUATION":
        reasons = ["golden_evaluation_requires_review"]
        if 0.90 <= c < 0.95:
            reasons.append("owner_validation_band")
        reasons.extend(sorted(flags.intersection({"conflicting_classifiers", "high_novelty_ambiguous_mapping"})))
        return 2, "P2_GOLDEN_EVALUATION", reasons

    return 3, "P3_OTHER_ESCALATION", sorted(flags) or ["other_human_review_reason"]


def compact(candidate: dict, template_ref: str) -> dict:
    rank, bucket, reasons = priority(candidate)
    return {
        "queue_id": f"hrq-{candidate['candidate_id'][5:]}",
        "priority": rank,
        "priority_bucket": bucket,
        "candidate_id": candidate["candidate_id"],
        "source_id": candidate["source_id"],
        "artifact_type": candidate["artifact_type"],
        "semantic_gate": candidate["semantic_gate"],
        "family": candidate["classification"]["family"],
        "domain": candidate["classification"]["domain"],
        "intent": candidate["classification"]["intent"],
        "aggregate_confidence": candidate["confidence"]["aggregate"],
        "confidence": candidate["confidence"],
        "quality": candidate["quality"],
        "techniques": candidate["techniques"],
        "architecture": candidate["architecture"],
        "critical_flags": candidate.get("critical_flags", []),
        "machine_route_reasons": candidate.get("route_reasons", []),
        "review_reasons": reasons,
        "golden_research_eligible": candidate["eligibility"]["golden_research_eligibility"]["eligible"],
        "distribution_eligible": candidate["eligibility"]["distribution_eligibility"]["eligible"],
        "candidate_fingerprint": candidate["candidate_fingerprint"],
        "machine_route": candidate["route"],
        "policy_version": candidate["policy_version"],
        "review_template_ref": template_ref,
    }


def template(candidate: dict) -> dict:
    return {
        "schema": "prompt-quarry-human-review-v1",
        "review_id": "review-" + candidate["candidate_id"][5:],
        "candidate_id": candidate["candidate_id"],
        "candidate_fingerprint": candidate["candidate_fingerprint"],
        "policy_version": candidate["policy_version"],
        "reviewer_role": "human-owner",
        "decision": "HOLD",
        "decision_reason_codes": ["PENDING_HUMAN_DECISION"],
        "rationale": "Pending human review; replace this placeholder with the review rationale.",
        "reviewed_at": "1970-01-01T00:00:00Z",
        "machine_confidence_at_review": candidate["confidence"]["aggregate"],
        "machine_route_at_review": candidate["route"],
        "semantic_gate_at_review": candidate["semantic_gate"],
        "corrections": [],
        "source_commit": None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a policy-versioned MK0 human review queue")
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    args = parser.parse_args()

    all_candidates = load_jsonl(args.candidates)
    versions = {c["policy_version"] for c in all_candidates}
    if len(versions) != 1:
        raise ValueError(f"candidate batch must contain exactly one policy version, got {sorted(versions)}")
    policy_version = versions.pop()
    tag = safe_policy_tag(policy_version)

    out = QUEUE_ROOT / f"batch-001-{tag}.jsonl"
    templates = QUEUE_ROOT / f"templates-{tag}"
    summary = ANALYSIS_ROOT / f"human-review-queue-batch-001-{tag}.json"

    candidates = [c for c in all_candidates if c["route"] == "HUMAN_REVIEW_REQUIRED"]
    queue = []
    for c in candidates:
        template_ref = f"{templates.as_posix()}/{c['candidate_id']}.json"
        queue.append(compact(c, template_ref))
    queue.sort(key=lambda r: (r["priority"], -r["aggregate_confidence"], -r["quality"]["golden_value"], r["candidate_id"]))

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in queue), encoding="utf-8")
    templates.mkdir(parents=True, exist_ok=True)
    for c in candidates:
        (templates / f"{c['candidate_id']}.json").write_text(json.dumps(template(c), indent=2) + "\n", encoding="utf-8")

    buckets = Counter(x["priority_bucket"] for x in queue)
    semantics = Counter(x["semantic_gate"]["artifact_class"] for x in queue)
    domains = Counter(x["domain"] for x in queue)
    payload = {
        "schema": "prompt-quarry-human-review-queue-summary-v1",
        "batch_id": f"mk0-human-review-001-{tag}",
        "policy_version": policy_version,
        "status": "PASS",
        "records": len(queue),
        "priority_buckets": dict(buckets),
        "semantic_artifact_classes": dict(semantics),
        "domains": dict(domains),
        "first_review_set": [x["candidate_id"] for x in queue[:10]],
        "queue_ref": out.as_posix(),
        "templates_ref": templates.as_posix(),
        "claim_boundary": "Queue prioritization only. Human review may approve governed dataset candidacy but does not establish redistribution rights, truth, or behavioral certification. Historical review batches are not overwritten."
    }
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
