from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from mk0_harvester_router import apply_route, load_policy

SOURCE_RECORDS = Path("mk0/normalized/harvester/source-records.jsonl")
CANDIDATE_SCHEMA = Path("mk0/harvester/CANDIDATE_RECORD.schema.json")
QUEUE_ROOT = Path("mk0/golden-dataset/candidate-queue")
RAW_ROOT = Path("mk0/raw/harvester")

DOMAIN_RULES = {
    "software": ["code", "software", "api", "github", "debug", "test", "developer", "programming", "cli", "python", "javascript", "typescript"],
    "research": ["research", "paper", "evidence", "study", "literature", "benchmark", "empirical"],
    "content": ["content", "write", "writing", "copy", "blog", "article", "social", "marketing"],
    "data": ["data", "sql", "database", "analytics", "dataset", "spreadsheet"],
    "agentic": ["agent", "skill", "tool", "workflow", "capability", "instructions"],
}
INTENT_RULES = {
    "review": ["review", "audit", "critique", "check", "inspect"],
    "generate": ["generate", "create", "write", "draft", "build", "implement"],
    "research": ["research", "investigate", "evidence", "study", "compare", "benchmark"],
    "transform": ["rewrite", "refactor", "convert", "improve", "optimize", "edit"],
    "operate": ["run", "execute", "deploy", "publish", "workflow", "automate"],
}
TECHNIQUE_RULES = {
    "role-framing": ["you are", "act as", "role:"],
    "explicit-constraints": ["must", "must not", "never", "required", "constraints"],
    "structured-output": ["json", "yaml", "markdown", "format", "schema", "output"],
    "step-decomposition": ["steps", "step-by-step", "workflow", "procedure", "process"],
    "examples": ["example", "examples", "few-shot"],
    "verification": ["verify", "validate", "test", "check", "evidence", "citation"],
    "tool-use": ["tool", "command", "api", "browser", "search"],
    "context-boundary": ["context", "source", "provided", "do not assume", "unknown"],
}
ARCH_RULES = {
    "role-task-constraints-output": ["you are", "must", "output"],
    "procedure-driven": ["steps", "workflow", "procedure"],
    "evidence-grounded": ["evidence", "citation", "source", "verify"],
    "tool-augmented": ["tool", "api", "browser", "command"],
    "example-conditioned": ["example", "few-shot"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def read_body(record: dict) -> str:
    ref = record.get("provenance", {}).get("raw_record_ref")
    if not ref:
        return ""
    path = Path(ref)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def normalized_text(text: str) -> str:
    text = text.casefold()
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fingerprint(text: str) -> str:
    return "sha256:" + hashlib.sha256(normalized_text(text).encode()).hexdigest()


def score_rules(text: str, rules: dict[str, list[str]]) -> tuple[str, int, int]:
    folded = text.casefold()
    scores = {key: sum(1 for token in tokens if token in folded) for key, tokens in rules.items()}
    ordered = sorted(scores.items(), key=lambda row: (-row[1], row[0]))
    best, best_score = ordered[0]
    second = ordered[1][1] if len(ordered) > 1 else 0
    return best, best_score, second


def detected(text: str, rules: dict[str, list[str]]) -> list[str]:
    folded = text.casefold()
    return sorted(key for key, tokens in rules.items() if any(token in folded for token in tokens))


def confidence_from_margin(best: int, second: int, *, base: float, ceiling: float) -> float:
    if best <= 0:
        return 0.72
    margin = best - second
    return min(ceiling, base + min(best, 6) * 0.025 + max(margin, 0) * 0.015)


def characterize(record: dict, body: str, seen: dict[str, str], policy: dict) -> dict:
    title = record.get("title") or ""
    text = f"{title}\n{body}"
    domain, d_best, d_second = score_rules(text, DOMAIN_RULES)
    intent, i_best, i_second = score_rules(text, INTENT_RULES)
    techniques = detected(text, TECHNIQUE_RULES)
    architecture = detected(text, ARCH_RULES)
    fp = fingerprint(body or record["canonical_url"])
    duplicate_of = seen.get(fp)

    classification_conf = min(
        confidence_from_margin(d_best, d_second, base=0.79, ceiling=0.98),
        confidence_from_margin(i_best, i_second, base=0.79, ceiling=0.98),
    )
    technique_conf = min(0.98, 0.84 + min(len(techniques), 7) * 0.02) if techniques else 0.78
    architecture_conf = min(0.98, 0.84 + min(len(architecture), 5) * 0.025) if architecture else 0.76
    dedup_conf = 0.99 if body else 0.82

    length = len(body)
    structural = min(0.98, 0.55 + min(length, 12000) / 30000 + min(len(techniques), 6) * 0.035)
    novelty = 0.20 if duplicate_of else min(0.95, 0.58 + min(len(techniques), 6) * 0.045 + min(len(architecture), 4) * 0.03)
    coverage = min(0.95, 0.55 + (0.12 if domain != "agentic" else 0.08) + min(len(techniques), 5) * 0.04)
    golden_value = round((structural * 0.40) + (novelty * 0.30) + (coverage * 0.30), 4)

    flags: list[str] = []
    if record.get("license_status") == "UNKNOWN":
        flags.append("license_unknown_for_redistribution")
    if record.get("body_observation_status") != "OBSERVED":
        flags.append("content_observation_ambiguity")
    if d_best == d_second and d_best > 0:
        flags.append("conflicting_classifiers")
    if novelty >= 0.90 and architecture_conf < 0.90:
        flags.append("high_novelty_ambiguous_mapping")

    family = f"{domain}_{intent}"
    candidate_id = "cand-" + hashlib.sha256((record["source_id"] + fp).encode()).hexdigest()[:20]
    candidate = {
        "schema": "prompt-quarry-candidate-record-v1",
        "candidate_id": candidate_id,
        "source_id": record["source_id"],
        "candidate_fingerprint": fp,
        "artifact_type": record["source_type"] if record["source_type"] in {"prompt", "skill", "agent", "instruction-markdown", "capability", "workflow"} else "other",
        "stage": "SCORED",
        "classification": {"domain": domain, "intent": intent, "family": family, "language": record.get("language")},
        "techniques": techniques,
        "architecture": architecture,
        "confidence": {
            "classification": round(classification_conf, 4),
            "technique_extraction": round(technique_conf, 4),
            "architecture_mapping": round(architecture_conf, 4),
            "deduplication": dedup_conf,
            "aggregate": 0.0,
        },
        "quality": {
            "structural_quality": round(structural, 4),
            "novelty": round(novelty, 4),
            "coverage_value": round(coverage, 4),
            "golden_value": golden_value,
        },
        "duplicate_of": duplicate_of,
        "critical_flags": sorted(set(flags)),
        "route": "HOLD",
        "route_reasons": [],
        "policy_version": policy["policy_version"],
        "source_record_ref": "mk0/normalized/harvester/source-records.jsonl",
        "characterization_ref": "mk0/analysis/harvester/characterization-batch-001-receipt.json",
        "created_at": utc_now(),
    }
    routed = apply_route(candidate, policy)
    if not duplicate_of:
        seen[fp] = candidate_id
    return routed


def validate(records: list[dict]) -> None:
    schema = json.loads(CANDIDATE_SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for i, record in enumerate(records):
        for error in validator.iter_errors(record):
            errors.append(f"record[{i}] {error.json_path}: {error.message}")
    if errors:
        raise ValueError("candidate validation failed:\n" + "\n".join(errors))


def persist(records: list[dict], output: Path, receipt: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    routes = Counter(r["route"] for r in records)
    domains = Counter(r["classification"]["domain"] for r in records)
    families = Counter(r["classification"]["family"] for r in records)
    techniques = Counter(t for r in records for t in r["techniques"])
    aggregates = [r["confidence"]["aggregate"] for r in records]
    payload = {
        "schema": "prompt-quarry-characterization-receipt-v1",
        "batch_id": "mk0-characterization-001",
        "status": "PASS",
        "created_at": utc_now(),
        "records": len(records),
        "routes": dict(routes),
        "domains": dict(domains),
        "top_families": dict(families.most_common(12)),
        "top_techniques": dict(techniques.most_common(12)),
        "aggregate_confidence": {"min": min(aggregates), "max": max(aggregates), "mean": round(sum(aggregates)/len(aggregates), 4)},
        "duplicates": sum(1 for r in records if r.get("duplicate_of")),
        "claim_boundary": "Heuristic MK0 characterization only. Routing does not establish behavioral quality, certification, portability, or redistribution rights. UNKNOWN license remains UNKNOWN.",
    }
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=SOURCE_RECORDS)
    parser.add_argument("--output", type=Path, default=QUEUE_ROOT / "batch-001.jsonl")
    parser.add_argument("--receipt", type=Path, default=Path("mk0/analysis/harvester/characterization-batch-001-receipt.json"))
    args = parser.parse_args()
    policy = load_policy()
    sources = load_jsonl(args.input)
    seen: dict[str, str] = {}
    candidates = [characterize(source, read_body(source), seen, policy) for source in sources]
    validate(candidates)
    persist(candidates, args.output, args.receipt)
    print(json.dumps({"records": len(candidates), "output": str(args.output), "receipt": str(args.receipt)}, indent=2))


if __name__ == "__main__":
    main()
