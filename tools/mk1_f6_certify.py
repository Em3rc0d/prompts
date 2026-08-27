from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from mk1_behavioral_runner import sha256_json, sha256_text
from mk1_f5_benchmark import validate_receipt_integrity


REAL_MODES = {"api", "manual-observed"}
MIN_RUNTIME_FAMILIES = 3


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def certification_receipt_id(core: dict) -> str:
    digest = hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()[:16]
    return f"pq_mk1_f6_receipt_{digest}"


def _require_candidate(candidate: dict, source_tested: dict, baseline: dict, fixture_set: dict) -> None:
    if candidate.get("state") != "CANDIDATE":
        raise ValueError(f"F6 requires CANDIDATE source; got {candidate.get('state')!r}")
    if set(candidate.get("claims") or []) != {"engineered", "tested", "improved"}:
        raise ValueError("F6 source must carry exactly engineered/tested/improved claims before certification")
    if source_tested.get("state") != "TESTED" or "tested" not in set(source_tested.get("claims") or []):
        raise ValueError("F6 requires the exact TESTED source artifact used by F5")
    for key in ("id", "version", "prompt_body"):
        if candidate.get(key) != source_tested.get(key):
            raise ValueError(f"F6 candidate/source TESTED identity drift for {key}")
    evaluation = candidate.get("evaluation") or {}
    if evaluation.get("baseline_id") != baseline.get("baseline_id"):
        raise ValueError("F6 candidate baseline id mismatch")
    if evaluation.get("fixture_set_id") != fixture_set.get("fixture_set_id"):
        raise ValueError("F6 candidate fixture-set id mismatch")
    if not evaluation.get("receipt_id"):
        raise ValueError("F6 candidate must descend from an F5 improvement receipt")


def validate_cross_runtime_f5_receipt(
    receipt: dict,
    candidate: dict,
    source_tested: dict,
    baseline: dict,
    fixture_set: dict,
) -> None:
    validate_receipt_integrity(receipt)
    if receipt.get("execution_mode") not in REAL_MODES:
        raise ValueError("F6 accepts only real F5 execution receipts")
    if receipt.get("status") != "IMPROVEMENT_PASS" or receipt.get("eligible_for_improved") is not True:
        raise ValueError("Every F6 runtime must independently satisfy F5 IMPROVEMENT_PASS")
    if receipt.get("artifact_id") != candidate.get("id") or receipt.get("artifact_version") != candidate.get("version"):
        raise ValueError("F6 F5 evidence artifact identity mismatch")
    if receipt.get("engineered_prompt_fingerprint") != sha256_text(candidate.get("prompt_body", "")):
        raise ValueError("F6 F5 evidence prompt fingerprint mismatch")
    if receipt.get("baseline_id") != baseline.get("baseline_id"):
        raise ValueError("F6 F5 evidence baseline id mismatch")
    if receipt.get("baseline_prompt_fingerprint") != sha256_text(baseline.get("prompt_body", "")):
        raise ValueError("F6 F5 evidence baseline fingerprint mismatch")
    if receipt.get("fixture_set_id") != fixture_set.get("fixture_set_id"):
        raise ValueError("F6 F5 evidence fixture-set id mismatch")
    if receipt.get("fixture_set_version") != fixture_set.get("version"):
        raise ValueError("F6 F5 evidence fixture-set version mismatch")
    if receipt.get("fixture_set_fingerprint") != sha256_json(fixture_set):
        raise ValueError("F6 F5 evidence fixture-set fingerprint mismatch")
    if receipt.get("parent_f4_receipt_id") != (source_tested.get("evaluation") or {}).get("receipt_id"):
        raise ValueError("F6 F5 evidence does not descend from the same F4 TESTED receipt")
    if receipt.get("engineered_blocking_pass_rate") != 1.0 or receipt.get("rubric_score") != 100.0:
        raise ValueError("F6 requires 100% blocking pass and rubric score 100 on every runtime")
    if receipt.get("engineered_failures") or receipt.get("regressions") or receipt.get("unresolved_engineered_human_checks"):
        raise ValueError("F6 runtime evidence retains blocking failures/regressions/unresolved human checks")

    preference = receipt.get("preference") or {}
    if preference.get("baseline", 0) != 0:
        raise ValueError("F6 runtime evidence cannot contain a baseline A/B win")
    if preference.get("engineered", 0) < preference.get("required_engineered_wins", 1):
        raise ValueError("F6 runtime evidence lacks material engineered blind wins")

    runtime = receipt.get("runtime") or {}
    for key in ("provider", "model", "family", "run_at"):
        if not str(runtime.get(key, "")).strip():
            raise ValueError(f"F6 runtime evidence missing {key}")
    review = receipt.get("review") or {}
    if review.get("reviewer_type") != "human" or review.get("blinded") is not True:
        raise ValueError("F6 requires blinded human review for every runtime")
    for key in ("reviewer_ref", "reviewed_at", "randomization_ref"):
        if not str(review.get(key, "")).strip():
            raise ValueError(f"F6 runtime review missing {key}")


def build_certification_receipt(
    candidate: dict,
    source_tested: dict,
    baseline: dict,
    fixture_set: dict,
    f5_receipts: list[dict],
) -> dict:
    _require_candidate(candidate, source_tested, baseline, fixture_set)
    if len(f5_receipts) < MIN_RUNTIME_FAMILIES:
        raise ValueError(f"F6 requires at least {MIN_RUNTIME_FAMILIES} real F5 receipts")

    receipt_ids: set[str] = set()
    execution_ids: set[str] = set()
    randomization_refs: set[str] = set()
    normalized_families: set[str] = set()
    evidence: list[dict] = []

    for receipt in f5_receipts:
        validate_cross_runtime_f5_receipt(receipt, candidate, source_tested, baseline, fixture_set)
        receipt_id = receipt["receipt_id"]
        execution_id = receipt.get("execution_id")
        randomization_ref = (receipt.get("review") or {}).get("randomization_ref")
        family = str((receipt.get("runtime") or {}).get("family", "")).strip()
        normalized_family = family.casefold()
        if receipt_id in receipt_ids:
            raise ValueError(f"Duplicate F5 receipt in F6 evidence: {receipt_id}")
        if execution_id in execution_ids:
            raise ValueError(f"Duplicate execution_id in F6 evidence: {execution_id}")
        if randomization_ref in randomization_refs:
            raise ValueError(f"F6 requires a distinct blind randomization_ref per runtime: {randomization_ref}")
        if normalized_family in normalized_families:
            raise ValueError(f"F6 requires distinct runtime families; duplicate family={family!r}")
        receipt_ids.add(receipt_id)
        execution_ids.add(execution_id)
        randomization_refs.add(randomization_ref)
        normalized_families.add(normalized_family)
        evidence.append({
            "receipt_id": receipt_id,
            "execution_id": execution_id,
            "execution_mode": receipt["execution_mode"],
            "runtime": copy.deepcopy(receipt["runtime"]),
            "reviewer_ref": receipt["review"]["reviewer_ref"],
            "reviewed_at": receipt["review"]["reviewed_at"],
            "randomization_ref": randomization_ref,
            "rubric_score": receipt["rubric_score"],
            "engineered_wins": receipt["preference"]["engineered"],
            "baseline_wins": receipt["preference"]["baseline"],
            "ties": receipt["preference"]["tie"],
        })

    source_f5_receipt_id = (candidate.get("evaluation") or {}).get("receipt_id")
    if source_f5_receipt_id not in receipt_ids:
        raise ValueError("F6 evidence must include the exact F5 receipt that created the CANDIDATE")
    if len(normalized_families) < MIN_RUNTIME_FAMILIES:
        raise ValueError(f"F6 requires {MIN_RUNTIME_FAMILIES} distinct runtime families")

    evidence.sort(key=lambda row: (row["runtime"]["family"].casefold(), row["receipt_id"]))
    certified_at = max(str(row["reviewed_at"]) for row in evidence)
    core = {
        "mk_stage": "MK1",
        "phase": "F6",
        "artifact_id": candidate["id"],
        "artifact_version": candidate["version"],
        "engineered_prompt_fingerprint": sha256_text(candidate["prompt_body"]),
        "baseline_id": baseline["baseline_id"],
        "baseline_prompt_fingerprint": sha256_text(baseline["prompt_body"]),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version"),
        "fixture_set_fingerprint": sha256_json(fixture_set),
        "parent_f4_receipt_id": (source_tested.get("evaluation") or {}).get("receipt_id"),
        "source_candidate_f5_receipt_id": source_f5_receipt_id,
        "f5_evidence_count": len(evidence),
        "runtime_family_count": len(normalized_families),
        "runtime_families": sorted(row["runtime"]["family"] for row in evidence),
        "f5_evidence": evidence,
        "certified_at": certified_at,
        "status": "CERTIFICATION_PASS",
        "eligible_for_certified": True,
        "state_policy": "Only this exact CANDIDATE may advance to CERTIFIED, and only while all bound F5 runtime evidence remains valid.",
        "claim_policy": "CERTIFIED means the exact prompt passed the declared blocking/superiority protocol across at least three distinct declared runtime families. It is not a universal correctness claim.",
    }
    core["receipt_id"] = certification_receipt_id(core)
    return core


def validate_certification_receipt_integrity(receipt: dict) -> None:
    supplied = receipt.get("receipt_id")
    core = copy.deepcopy(receipt)
    core.pop("receipt_id", None)
    expected = certification_receipt_id(core)
    if supplied != expected:
        raise ValueError(f"F6 receipt integrity check failed: expected {expected}, got {supplied}")


def promote_certified(candidate: dict, receipt: dict) -> dict:
    validate_certification_receipt_integrity(receipt)
    if candidate.get("state") != "CANDIDATE":
        raise ValueError("F6 promotion requires CANDIDATE source artifact")
    if receipt.get("artifact_id") != candidate.get("id") or receipt.get("artifact_version") != candidate.get("version"):
        raise ValueError("F6 certification receipt artifact identity mismatch")
    if receipt.get("engineered_prompt_fingerprint") != sha256_text(candidate.get("prompt_body", "")):
        raise ValueError("F6 certification receipt prompt fingerprint mismatch")
    if receipt.get("source_candidate_f5_receipt_id") != (candidate.get("evaluation") or {}).get("receipt_id"):
        raise ValueError("F6 certification receipt does not descend from the candidate's F5 receipt")
    if receipt.get("status") != "CERTIFICATION_PASS" or receipt.get("eligible_for_certified") is not True:
        raise ValueError("F6 receipt is not eligible for CERTIFIED promotion")
    if int(receipt.get("runtime_family_count") or 0) < MIN_RUNTIME_FAMILIES:
        raise ValueError("F6 certification receipt lacks required runtime-family diversity")

    promoted = copy.deepcopy(candidate)
    promoted["state"] = "CERTIFIED"
    promoted["claims"] = ["engineered", "tested", "improved", "certified"]
    promoted["evaluation"] = {
        "baseline_id": receipt["baseline_id"],
        "fixture_set_id": receipt["fixture_set_id"],
        "receipt_id": receipt["receipt_id"],
        "rubric_score": 100.0,
        "blocking_failures": [],
    }
    promoted["updated_at"] = receipt["certified_at"]
    return promoted
