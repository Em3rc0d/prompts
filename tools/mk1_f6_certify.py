from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from mk1_behavioral_runner import sha256_json, sha256_text
from mk1_f5_benchmark import validate_receipt_integrity


REAL_MODES = {"api", "manual-observed"}
MIN_INDEPENDENT_F5_RECEIPTS = 3
RUNTIME_IDENTITY_FIELDS = ("provider", "model", "family", "run_at", "identity_evidence_ref")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def certification_receipt_id(core: dict) -> str:
    digest = hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()[:16]
    return f"pq_mk1_f6_receipt_{digest}"


def normalize_identity(value: object) -> str:
    return " ".join(str(value or "").strip().casefold().split())


def normalized_runtime_target(runtime: dict) -> tuple[str, str, str]:
    return (
        normalize_identity(runtime.get("provider")),
        normalize_identity(runtime.get("model")),
        normalize_identity(runtime.get("family")),
    )


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


def validate_f5_evidence_receipt(
    receipt: dict,
    candidate: dict,
    source_tested: dict,
    baseline: dict,
    fixture_set: dict,
) -> None:
    """Validate one real F5 superiority receipt without imposing F6/F7 runtime topology."""
    validate_receipt_integrity(receipt)
    if receipt.get("execution_mode") not in REAL_MODES:
        raise ValueError("Certification evidence accepts only real F5 execution receipts")
    if receipt.get("status") != "IMPROVEMENT_PASS" or receipt.get("eligible_for_improved") is not True:
        raise ValueError("Every certification evidence receipt must independently satisfy F5 IMPROVEMENT_PASS")
    if receipt.get("artifact_id") != candidate.get("id") or receipt.get("artifact_version") != candidate.get("version"):
        raise ValueError("F5 evidence artifact identity mismatch")
    if receipt.get("engineered_prompt_fingerprint") != sha256_text(candidate.get("prompt_body", "")):
        raise ValueError("F5 evidence prompt fingerprint mismatch")
    if receipt.get("baseline_id") != baseline.get("baseline_id"):
        raise ValueError("F5 evidence baseline id mismatch")
    if receipt.get("baseline_prompt_fingerprint") != sha256_text(baseline.get("prompt_body", "")):
        raise ValueError("F5 evidence baseline fingerprint mismatch")
    if receipt.get("fixture_set_id") != fixture_set.get("fixture_set_id"):
        raise ValueError("F5 evidence fixture-set id mismatch")
    if receipt.get("fixture_set_version") != fixture_set.get("version"):
        raise ValueError("F5 evidence fixture-set version mismatch")
    if receipt.get("fixture_set_fingerprint") != sha256_json(fixture_set):
        raise ValueError("F5 evidence fixture-set fingerprint mismatch")
    if receipt.get("parent_f4_receipt_id") != (source_tested.get("evaluation") or {}).get("receipt_id"):
        raise ValueError("F5 evidence does not descend from the same F4 TESTED receipt")
    if receipt.get("engineered_blocking_pass_rate") != 1.0 or receipt.get("rubric_score") != 100.0:
        raise ValueError("Certification evidence requires 100% blocking pass and rubric score 100")
    if receipt.get("engineered_failures") or receipt.get("regressions") or receipt.get("unresolved_engineered_human_checks"):
        raise ValueError("Certification evidence retains blocking failures/regressions/unresolved human checks")

    preference = receipt.get("preference") or {}
    if preference.get("baseline", 0) != 0:
        raise ValueError("Certification evidence cannot contain a baseline A/B win")
    if preference.get("engineered", 0) < preference.get("required_engineered_wins", 1):
        raise ValueError("Certification evidence lacks material engineered blind wins")

    runtime = receipt.get("runtime") or {}
    for key in RUNTIME_IDENTITY_FIELDS:
        if not str(runtime.get(key, "")).strip():
            raise ValueError(f"Certification runtime evidence missing {key}")
    review = receipt.get("review") or {}
    if review.get("reviewer_type") != "human" or review.get("blinded") is not True:
        raise ValueError("Certification evidence requires blinded human review")
    for key in ("reviewer_ref", "reviewed_at", "randomization_ref"):
        if not str(review.get(key, "")).strip():
            raise ValueError(f"Certification review missing {key}")


def validate_target_runtime_f5_receipt(
    receipt: dict,
    candidate: dict,
    source_tested: dict,
    baseline: dict,
    fixture_set: dict,
    target_runtime: tuple[str, str, str] | None = None,
) -> tuple[str, str, str]:
    validate_f5_evidence_receipt(receipt, candidate, source_tested, baseline, fixture_set)
    runtime = receipt.get("runtime") or {}
    observed = normalized_runtime_target(runtime)
    if not all(observed):
        raise ValueError("F6 target runtime requires provider, model and family")
    if target_runtime is not None and observed != target_runtime:
        raise ValueError(
            "F6 certification requires the same target runtime for every independent F5 receipt "
            f"(expected provider/model/family={target_runtime}, got {observed})"
        )
    return observed


def build_certification_receipt(
    candidate: dict,
    source_tested: dict,
    baseline: dict,
    fixture_set: dict,
    f5_receipts: list[dict],
) -> dict:
    _require_candidate(candidate, source_tested, baseline, fixture_set)
    if len(f5_receipts) < MIN_INDEPENDENT_F5_RECEIPTS:
        raise ValueError(f"F6 requires at least {MIN_INDEPENDENT_F5_RECEIPTS} independent real F5 receipts")

    source_f5_receipt_id = (candidate.get("evaluation") or {}).get("receipt_id")
    primary = next((row for row in f5_receipts if row.get("receipt_id") == source_f5_receipt_id), None)
    if primary is None:
        raise ValueError("F6 evidence must include the exact F5 receipt that created the CANDIDATE")

    target_runtime = validate_target_runtime_f5_receipt(
        primary, candidate, source_tested, baseline, fixture_set, None
    )

    receipt_ids: set[str] = set()
    execution_ids: set[str] = set()
    randomization_refs: set[str] = set()
    identity_evidence_refs: set[str] = set()
    evidence: list[dict] = []

    for receipt in f5_receipts:
        validate_target_runtime_f5_receipt(
            receipt, candidate, source_tested, baseline, fixture_set, target_runtime
        )
        receipt_id = str(receipt.get("receipt_id") or "")
        execution_id = str(receipt.get("execution_id") or "")
        review = receipt.get("review") or {}
        runtime = receipt.get("runtime") or {}
        randomization_ref = str(review.get("randomization_ref") or "")
        identity_evidence_ref = str(runtime.get("identity_evidence_ref") or "").strip()

        if receipt_id in receipt_ids:
            raise ValueError(f"Duplicate F5 receipt in F6 evidence: {receipt_id}")
        if execution_id in execution_ids:
            raise ValueError(f"Duplicate execution_id in F6 evidence: {execution_id}")
        if randomization_ref in randomization_refs:
            raise ValueError(f"F6 requires a distinct blind randomization_ref per independent run: {randomization_ref}")
        if identity_evidence_ref in identity_evidence_refs:
            raise ValueError(f"F6 requires distinct runtime identity evidence per independent run: {identity_evidence_ref}")

        receipt_ids.add(receipt_id)
        execution_ids.add(execution_id)
        randomization_refs.add(randomization_ref)
        identity_evidence_refs.add(identity_evidence_ref)
        evidence.append({
            "receipt_id": receipt_id,
            "execution_id": execution_id,
            "execution_mode": receipt["execution_mode"],
            "runtime": copy.deepcopy(runtime),
            "reviewer_ref": review["reviewer_ref"],
            "reviewed_at": review["reviewed_at"],
            "randomization_ref": randomization_ref,
            "rubric_score": receipt["rubric_score"],
            "engineered_wins": receipt["preference"]["engineered"],
            "baseline_wins": receipt["preference"]["baseline"],
            "ties": receipt["preference"]["tie"],
        })

    if len(evidence) < MIN_INDEPENDENT_F5_RECEIPTS:
        raise ValueError(f"F6 requires {MIN_INDEPENDENT_F5_RECEIPTS} independent F5 receipts")

    evidence.sort(key=lambda row: (str(row["reviewed_at"]), row["receipt_id"]))
    certified_at = max(str(row["reviewed_at"]) for row in evidence)
    primary_runtime = primary.get("runtime") or {}
    target_runtime_doc = {
        "provider": primary_runtime["provider"],
        "model": primary_runtime["model"],
        "family": primary_runtime["family"],
    }
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
        "target_runtime": target_runtime_doc,
        "independent_f5_receipt_count": len(evidence),
        "minimum_independent_f5_receipts": MIN_INDEPENDENT_F5_RECEIPTS,
        "f5_evidence": evidence,
        "certified_at": certified_at,
        "status": "CERTIFICATION_PASS",
        "eligible_for_certified": True,
        "state_policy": "Only this exact CANDIDATE may advance to CERTIFIED, and only while all bound same-target-runtime F5 evidence remains valid.",
        "claim_policy": "CERTIFIED means the exact prompt repeatedly preserved 100% blocking pass and F5 superiority on the declared target provider/model/family across at least three independent blinded benchmark executions. Cross-provider portability is a separate F7 claim.",
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
    if int(receipt.get("independent_f5_receipt_count") or 0) < MIN_INDEPENDENT_F5_RECEIPTS:
        raise ValueError("F6 certification receipt lacks required independent same-runtime repetitions")
    target_runtime = receipt.get("target_runtime") or {}
    if not all(str(target_runtime.get(key, "")).strip() for key in ("provider", "model", "family")):
        raise ValueError("F6 certification receipt lacks target runtime identity")

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
