from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from mk1_behavioral_runner import sha256_json, sha256_text
from mk1_f6_certify import normalize_identity, validate_certification_receipt_integrity, validate_f5_evidence_receipt


MIN_RUNTIME_FAMILIES = 3
MIN_RUNTIME_PROVIDERS = 3


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def portability_receipt_id(core: dict) -> str:
    digest = hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()[:16]
    return f"pq_mk1_f7_receipt_{digest}"


def _require_certified(certified: dict, certification_receipt: dict, source_candidate: dict) -> None:
    validate_certification_receipt_integrity(certification_receipt)
    if certified.get("state") != "CERTIFIED":
        raise ValueError(f"F7 requires CERTIFIED source; got {certified.get('state')!r}")
    if set(certified.get("claims") or []) != {"engineered", "tested", "improved", "certified"}:
        raise ValueError("F7 source must carry exactly engineered/tested/improved/certified claims")
    if source_candidate.get("state") != "CANDIDATE":
        raise ValueError("F7 requires the F5 CANDIDATE ancestor from the F6 bundle")
    for key in ("id", "version", "prompt_body"):
        if certified.get(key) != source_candidate.get(key):
            raise ValueError(f"F7 certified/candidate identity drift for {key}")
    if certification_receipt.get("artifact_id") != certified.get("id"):
        raise ValueError("F7 source F6 receipt artifact mismatch")
    if certification_receipt.get("engineered_prompt_fingerprint") != sha256_text(certified.get("prompt_body", "")):
        raise ValueError("F7 source F6 receipt prompt fingerprint mismatch")


def validate_portability_inventory(receipts: list[dict]) -> dict:
    receipt_ids: set[str] = set()
    execution_ids: set[str] = set()
    randomization_refs: set[str] = set()
    identity_evidence_refs: set[str] = set()
    providers: dict[str, str] = {}
    families: dict[str, str] = {}

    for receipt in receipts:
        receipt_id = str(receipt.get("receipt_id") or "")
        execution_id = str(receipt.get("execution_id") or "")
        review = receipt.get("review") or {}
        runtime = receipt.get("runtime") or {}
        randomization_ref = str(review.get("randomization_ref") or "")
        identity_evidence_ref = str(runtime.get("identity_evidence_ref") or "")
        provider = str(runtime.get("provider") or "").strip()
        family = str(runtime.get("family") or "").strip()
        pkey = normalize_identity(provider)
        fkey = normalize_identity(family)

        if receipt_id in receipt_ids:
            raise ValueError(f"Duplicate F7 evidence receipt_id: {receipt_id}")
        if execution_id in execution_ids:
            raise ValueError(f"Duplicate F7 evidence execution_id: {execution_id}")
        if randomization_ref in randomization_refs:
            raise ValueError(f"Duplicate F7 randomization_ref: {randomization_ref}")
        if identity_evidence_ref in identity_evidence_refs:
            raise ValueError(f"Duplicate F7 runtime identity evidence: {identity_evidence_ref}")
        if not pkey or not fkey:
            raise ValueError("F7 evidence requires non-empty provider and family")

        receipt_ids.add(receipt_id)
        execution_ids.add(execution_id)
        randomization_refs.add(randomization_ref)
        identity_evidence_refs.add(identity_evidence_ref)
        providers.setdefault(pkey, provider)
        families.setdefault(fkey, family)

    return {
        "receipt_count": len(receipt_ids),
        "runtime_provider_count": len(providers),
        "runtime_family_count": len(families),
        "runtime_providers": sorted(providers.values(), key=normalize_identity),
        "runtime_families": sorted(families.values(), key=normalize_identity),
    }


def build_portability_receipt(
    certified: dict,
    certification_receipt: dict,
    source_candidate: dict,
    source_tested: dict,
    baseline: dict,
    fixture_set: dict,
    f5_receipts: list[dict],
) -> dict:
    _require_certified(certified, certification_receipt, source_candidate)
    if not f5_receipts:
        raise ValueError("F7 requires F5 evidence")

    for receipt in f5_receipts:
        validate_f5_evidence_receipt(receipt, source_candidate, source_tested, baseline, fixture_set)

    source_candidate_f5 = (source_candidate.get("evaluation") or {}).get("receipt_id")
    if source_candidate_f5 not in {row.get("receipt_id") for row in f5_receipts}:
        raise ValueError("F7 evidence must include the exact F5 receipt that created the source CANDIDATE")

    inventory = validate_portability_inventory(f5_receipts)
    if inventory["runtime_provider_count"] < MIN_RUNTIME_PROVIDERS:
        raise ValueError(f"F7 requires {MIN_RUNTIME_PROVIDERS} distinct runtime providers")
    if inventory["runtime_family_count"] < MIN_RUNTIME_FAMILIES:
        raise ValueError(f"F7 requires {MIN_RUNTIME_FAMILIES} distinct runtime families")

    evidence = []
    for receipt in f5_receipts:
        runtime = receipt.get("runtime") or {}
        review = receipt.get("review") or {}
        evidence.append({
            "receipt_id": receipt["receipt_id"],
            "execution_id": receipt.get("execution_id"),
            "execution_mode": receipt.get("execution_mode"),
            "runtime": copy.deepcopy(runtime),
            "reviewer_ref": review.get("reviewer_ref"),
            "reviewed_at": review.get("reviewed_at"),
            "randomization_ref": review.get("randomization_ref"),
            "rubric_score": receipt.get("rubric_score"),
            "engineered_wins": (receipt.get("preference") or {}).get("engineered"),
            "baseline_wins": (receipt.get("preference") or {}).get("baseline"),
            "ties": (receipt.get("preference") or {}).get("tie"),
        })
    evidence.sort(key=lambda row: (normalize_identity((row.get("runtime") or {}).get("provider")), normalize_identity((row.get("runtime") or {}).get("family")), str(row.get("receipt_id"))))
    portable_at = max(str(row.get("reviewed_at") or "") for row in evidence)

    core = {
        "mk_stage": "MK1",
        "phase": "F7",
        "artifact_id": certified["id"],
        "artifact_version": certified["version"],
        "engineered_prompt_fingerprint": sha256_text(certified["prompt_body"]),
        "baseline_id": baseline["baseline_id"],
        "baseline_prompt_fingerprint": sha256_text(baseline["prompt_body"]),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version"),
        "fixture_set_fingerprint": sha256_json(fixture_set),
        "parent_f4_receipt_id": (source_tested.get("evaluation") or {}).get("receipt_id"),
        "source_candidate_f5_receipt_id": source_candidate_f5,
        "source_f6_certification_receipt_id": certification_receipt["receipt_id"],
        "f5_evidence_count": len(evidence),
        "runtime_provider_count": inventory["runtime_provider_count"],
        "runtime_family_count": inventory["runtime_family_count"],
        "runtime_providers": inventory["runtime_providers"],
        "runtime_families": inventory["runtime_families"],
        "f5_evidence": evidence,
        "portable_at": portable_at,
        "status": "PORTABILITY_PASS",
        "eligible_for_portable": True,
        "state_policy": "Only this exact CERTIFIED artifact may advance to PORTABLE while its F6 certification and all bound cross-provider F5 evidence remain valid.",
        "claim_policy": "PORTABLE means the exact certified prompt preserved the declared F5 behavioral/superiority contract across at least three distinct providers and three distinct runtime families. It is not universal compatibility.",
    }
    core["receipt_id"] = portability_receipt_id(core)
    return core


def validate_portability_receipt_integrity(receipt: dict) -> None:
    supplied = receipt.get("receipt_id")
    core = copy.deepcopy(receipt)
    core.pop("receipt_id", None)
    expected = portability_receipt_id(core)
    if supplied != expected:
        raise ValueError(f"F7 receipt integrity check failed: expected {expected}, got {supplied}")


def promote_portable(certified: dict, receipt: dict) -> dict:
    validate_portability_receipt_integrity(receipt)
    if certified.get("state") != "CERTIFIED":
        raise ValueError("F7 promotion requires CERTIFIED source artifact")
    if receipt.get("artifact_id") != certified.get("id") or receipt.get("artifact_version") != certified.get("version"):
        raise ValueError("F7 portability receipt artifact identity mismatch")
    if receipt.get("engineered_prompt_fingerprint") != sha256_text(certified.get("prompt_body", "")):
        raise ValueError("F7 portability receipt prompt fingerprint mismatch")
    if receipt.get("source_f6_certification_receipt_id") != (certified.get("evaluation") or {}).get("receipt_id"):
        raise ValueError("F7 portability receipt does not descend from the artifact's F6 certification")
    if receipt.get("status") != "PORTABILITY_PASS" or receipt.get("eligible_for_portable") is not True:
        raise ValueError("F7 receipt is not eligible for PORTABLE promotion")
    if int(receipt.get("runtime_provider_count") or 0) < MIN_RUNTIME_PROVIDERS:
        raise ValueError("F7 receipt lacks required provider diversity")
    if int(receipt.get("runtime_family_count") or 0) < MIN_RUNTIME_FAMILIES:
        raise ValueError("F7 receipt lacks required family diversity")

    promoted = copy.deepcopy(certified)
    promoted["state"] = "PORTABLE"
    promoted["claims"] = ["engineered", "tested", "improved", "certified", "portable"]
    promoted["evaluation"] = {
        "baseline_id": receipt["baseline_id"],
        "fixture_set_id": receipt["fixture_set_id"],
        "receipt_id": receipt["receipt_id"],
        "rubric_score": 100.0,
        "blocking_failures": [],
    }
    promoted["updated_at"] = receipt["portable_at"]
    return promoted
