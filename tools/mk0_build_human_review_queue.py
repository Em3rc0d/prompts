from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

CANDIDATES = Path("mk0/golden-dataset/candidate-queue/batch-001.jsonl")
OUT = Path("mk0/golden-dataset/human-review-queue/batch-001.jsonl")
SUMMARY = Path("mk0/analysis/harvester/human-review-queue-batch-001.json")
TEMPLATES = Path("mk0/golden-dataset/human-review-queue/templates")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def priority(candidate: dict) -> tuple[int, str, list[str]]:
    c = candidate["confidence"]["aggregate"]
    flags = set(candidate.get("critical_flags", []))
    if 0.90 <= c < 0.95:
        return 1, "P1_CONFIDENCE_BAND", ["owner_validation_band"]
    if "conflicting_classifiers" in flags:
        return 2, "P2_CLASSIFIER_CONFLICT", ["conflicting_classifiers"]
    if "high_novelty_ambiguous_mapping" in flags:
        return 2, "P2_AMBIGUOUS_MAPPING", ["high_novelty_ambiguous_mapping"]
    return 3, "P3_OTHER_ESCALATION", sorted(flags) or ["other_human_review_reason"]


def compact(candidate: dict) -> dict:
    rank, bucket, reasons = priority(candidate)
    return {
        "queue_id": f"hrq-{candidate['candidate_id'][5:]}",
        "priority": rank,
        "priority_bucket": bucket,
        "candidate_id": candidate["candidate_id"],
        "source_id": candidate["source_id"],
        "artifact_type": candidate["artifact_type"],
        "family": candidate["classification"]["family"],
        "domain": candidate["classification"]["domain"],
        "intent": candidate["classification"]["intent"],
        "aggregate_confidence": candidate["confidence"]["aggregate"],
        "confidence": candidate["confidence"],
        "quality": candidate["quality"],
        "techniques": candidate["techniques"],
        "architecture": candidate["architecture"],
        "critical_flags": candidate.get("critical_flags", []),
        "review_reasons": reasons,
        "golden_research_eligible": candidate["eligibility"]["golden_research_eligibility"]["eligible"],
        "distribution_eligible": candidate["eligibility"]["distribution_eligibility"]["eligible"],
        "candidate_fingerprint": candidate["candidate_fingerprint"],
        "machine_route": candidate["route"],
        "policy_version": candidate["policy_version"],
        "review_template_ref": f"mk0/golden-dataset/human-review-queue/templates/{candidate['candidate_id']}.json",
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
        "corrections": [],
        "source_commit": None,
    }


def main() -> None:
    candidates = [c for c in load_jsonl(CANDIDATES) if c["route"] == "HUMAN_REVIEW_REQUIRED"]
    queue = [compact(c) for c in candidates]
    queue.sort(key=lambda r: (r["priority"], -r["aggregate_confidence"], -r["quality"]["golden_value"], r["candidate_id"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in queue), encoding="utf-8")
    TEMPLATES.mkdir(parents=True, exist_ok=True)
    for c in candidates:
        (TEMPLATES / f"{c['candidate_id']}.json").write_text(json.dumps(template(c), indent=2) + "\n", encoding="utf-8")

    buckets = Counter(x["priority_bucket"] for x in queue)
    domains = Counter(x["domain"] for x in queue)
    payload = {
        "schema": "prompt-quarry-human-review-queue-summary-v1",
        "batch_id": "mk0-human-review-001",
        "status": "PASS",
        "records": len(queue),
        "priority_buckets": dict(buckets),
        "domains": dict(domains),
        "first_review_set": [x["candidate_id"] for x in queue[:10]],
        "claim_boundary": "Queue prioritization only. Human review may approve dataset candidacy but does not establish redistribution rights or behavioral certification."
    }
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
