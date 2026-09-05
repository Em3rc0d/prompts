#!/usr/bin/env python3
"""Validate the current Prompt Machine Starter launch checkpoint.

This binds skill scope, the current public-copy re-audit, protocol-contaminated
runtime truth, and provider preflight without promoting any of them into sale,
delivery, customer-value, certification, or revenue evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMERCIAL = ROOT / "commercial"
WEB = ROOT / "web"

GATE = COMMERCIAL / "STARTER_RELEASE_GATE_V1.json"
DAG = COMMERCIAL / "STARTER_RELEASE_DAG_V1.json"
SKILL_SCOPE = COMMERCIAL / "STARTER_SKILL_LAUNCH_SCOPE_V1.json"
COPY_RECEIPT = COMMERCIAL / "STARTER_PUBLIC_COPY_AUDIT_RECEIPT_V1.json"
PROVIDER_PREFLIGHT = COMMERCIAL / "STARTER_PROVIDER_PREFLIGHT_FREEZE_V1.json"
STARTER_PAGE = WEB / "app" / "starter-collection" / "page.tsx"
COLLECTIONS_PAGE = WEB / "app" / "collections" / "page.tsx"
HOME_PAGE = WEB / "app" / "page.tsx"
STARTER_CHECKOUT = WEB / "app" / "api" / "commerce" / "starter-collection" / "checkout" / "route.ts"

CANONICAL_PRODUCT_ID = "prompt-machine-starter-collection"
CANONICAL_ARCHIVE_SHA256 = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"
CANONICAL_ARCHIVE_SIZE = 50918
CURRENT_COPY_RUN = 33834092608
CURRENT_COPY_COMMIT = "bd086c2e7fd76bc3852eea7d2e048341dce25ed4"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    gate = read_json(GATE)
    dag = read_json(DAG)
    skill = read_json(SKILL_SCOPE)
    copy = read_json(COPY_RECEIPT)
    preflight = read_json(PROVIDER_PREFLIGHT)

    assert gate["product"]["product_id"] == CANONICAL_PRODUCT_ID
    assert gate["product"]["sale_state"] == "NOT_FOR_SALE"
    assert gate["version"] == "1.0.10"
    assert gate["checkpoint_revision"] == "runtime-protocol-contamination-copy-reaudit-20260904"

    assert skill["state"] == "SKILLS_DEFERRED_FROM_V1_LAUNCH_PAYLOAD_EVIDENCE_OPEN"
    assert skill["product_id"] == CANONICAL_PRODUCT_ID
    assert skill["decision"]["starter_v1_launch_value_is_workflow_led"] is True
    assert skill["decision"]["skills_are_launch_blocking"] is False
    assert skill["decision"]["skills_are_currently_supported_product_features"] is False
    assert skill["decision"]["skills_may_be_marketed_as_included_or_tested"] is False
    assert len(skill["current_candidates"]) == 2
    assert all(row["material_semantic_drift"]["observed"] is True for row in skill["current_candidates"])
    assert skill["existing_evidence"]["HOST_TESTED"] is False
    assert skill["existing_evidence"]["SKILL_TRIGGER_EVAL_PASS"] is False
    assert skill["existing_evidence"]["SKILL_FORWARD_TEST_PASS"] is False
    assert skill["existing_evidence"]["PROMPT_SKILL_PARITY_PASS"] is False
    assert skill["launch_payload_boundary"]["skills_in_current_deterministic_archive"] == 0
    assert skill["current_truth"]["starter_supported_skills"] == 0
    assert skill["current_truth"]["starter_skill_behavioral_observations"] == 0

    gate_skill = gate["skill_launch_scope"]
    assert gate_skill["state"] == skill["state"]
    assert gate_skill["supported_skills"] == 0
    assert gate_skill["structural_candidates"] == 2
    assert gate_skill["skills_in_current_archive"] == 0
    assert gate_skill["skills_are_launch_blocking"] is False
    assert gate["truth"]["starter_supported_skills"] == 0
    assert gate["truth"]["starter_structural_skill_candidates"] == 2
    assert gate["truth"]["starter_skills_in_current_archive"] == 0
    assert gate["gates"]["starter_skill_launch_scope"] == "DEFERRED_NON_BLOCKING_ZERO_SUPPORTED_SKILLS"

    # Public-copy history preserves all three cycles: identity/packaging, skill scope,
    # and the runtime-evidence staleness correction after protocol contamination.
    assert copy["version"] == "1.2.0"
    assert copy["final_state"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert len(copy["history"][0]["material_findings"]) == 3
    assert copy["history"][0]["state"] == "FAIL_EVIDENCE_SCOPE_AMBIGUOUS"
    assert len(copy["subsequent_reaudits"]) == 2

    skill_reaudit = copy["subsequent_reaudits"][0]
    assert skill_reaudit["pre_retest_review"]["state"] == "FAIL_PRODUCT_SCOPE_AMBIGUOUS"
    assert len(skill_reaudit["pre_retest_review"]["material_findings"]) == 3
    assert skill_reaudit["retest"]["run_id"] == 33805620505
    assert skill_reaudit["retest"]["conclusion"] == "success"

    runtime_reaudit = copy["subsequent_reaudits"][1]
    assert runtime_reaudit["pre_retest_review"]["state"] == "FAIL_EVIDENCE_STATE_STALE"
    assert len(runtime_reaudit["pre_retest_review"]["material_findings"]) == 3
    assert runtime_reaudit["retest"]["run_id"] == CURRENT_COPY_RUN
    assert runtime_reaudit["retest"]["audited_commit"] == CURRENT_COPY_COMMIT
    assert runtime_reaudit["retest"]["conclusion"] == "success"
    observed = runtime_reaudit["retest"]["observed_truth"]
    assert observed["starter_runtime_observations_claimed"] == 1
    assert observed["starter_runtime_passes_claimed"] == 0
    assert observed["starter_runtime_fails_claimed"] == 0
    assert observed["starter_runtime_inconclusive_claimed"] == 1
    assert observed["starter_clean_runtime_observations_claimed"] == 0

    assert copy["current_retest"]["run_id"] == CURRENT_COPY_RUN
    assert copy["current_retest"]["audited_commit"] == CURRENT_COPY_COMMIT
    assert copy["current_retest"]["conclusion"] == "success"
    assert copy["model_calls"] == 0
    assert copy["provider_calls"] == 0
    assert copy["ready_to_sell"] is False

    gate_copy = gate["public_copy_audit"]
    assert gate_copy["state"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert gate_copy["open_material_findings"] == 0
    assert gate_copy["current_retest_run_id"] == CURRENT_COPY_RUN
    assert gate_copy["current_audited_commit"] == CURRENT_COPY_COMMIT
    assert gate["gates"]["public_copy_evidence_audit"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"

    nodes = {node["id"]: node for node in dag["nodes"]}
    assert dag["version"] == "1.3.0"
    assert nodes["N07_PUBLIC_COPY_BOUNDARY"]["status"] == "OBSERVED_CLOSED"
    assert nodes["N07_PUBLIC_COPY_BOUNDARY"]["current_retest_run_id"] == CURRENT_COPY_RUN
    assert nodes["N09_STARTER_RUNTIME_EVIDENCE"]["status"] == "OPEN_REQUIRES_MODEL_AUTH"
    assert nodes["N14_PROVIDER_PROVISIONING_AND_CUSTODY"]["status"] == "OPEN_REQUIRES_PROVIDER_AUTH"
    frontier = {row["node"] for row in dag["current_frontier"]["next_evidence_purchase_options"]}
    assert frontier == {"N09_STARTER_RUNTIME_EVIDENCE", "N14_PROVIDER_PROVISIONING_AND_CUSTODY"}

    assert preflight["state"] == "STATIC_PROVIDER_EXECUTION_PRECONDITIONS_PASS_DISARMED"
    assert preflight["product_id"] == CANONICAL_PRODUCT_ID
    assert preflight["validated_by"]["run_id"] == 33804846142
    assert preflight["validated_by"]["conclusion"] == "success"
    assert preflight["execution_limits"]["custody_packet_armed"] is False
    assert preflight["execution_limits"]["delivery_canary_armed"] is False
    assert preflight["execution_limits"]["maximum_live_transactions"] == 1
    assert preflight["execution_limits"]["custody_automatic_retries"] == 0
    assert preflight["execution_limits"]["delivery_automatic_retries"] == 0
    assert preflight["canonical_artifact"]["size_bytes"] == CANONICAL_ARCHIVE_SIZE
    assert preflight["canonical_artifact"]["sha256"] == CANONICAL_ARCHIVE_SHA256
    assert preflight["current_truth"]["provider_side_effects_executed"] is False
    assert preflight["current_truth"]["provider_custody_observations"] == 0
    assert preflight["current_truth"]["live_canary_orders"] == 0
    assert preflight["current_truth"]["verified_deliveries"] == 0
    assert preflight["current_truth"]["real_customer_purchases"] == 0
    assert preflight["current_truth"]["public_checkout"] is False

    gate_preflight = gate["provider_preflight_freeze"]
    assert gate_preflight["state"] == preflight["state"]
    assert gate_preflight["validation_run_id"] == 33804846142
    assert gate_preflight["custody_packet_armed"] is False
    assert gate_preflight["delivery_canary_armed"] is False
    assert gate_preflight["maximum_live_transactions"] == 1
    assert gate["gates"]["provider_preflight"] == "PASS_STATIC_DISARMED"
    assert gate["gates"]["live_delivery_preflight"] == "PASS_STATIC_PREPARED_DISARMED"
    assert gate["gates"]["live_delivery_canary"] == "NOT_STARTED"

    starter = STARTER_PAGE.read_text(encoding="utf-8")
    collections = COLLECTIONS_PAGE.read_text(encoding="utf-8")
    home = HOME_PAGE.read_text(encoding="utf-8")
    for source in (starter, collections, home):
        assert "two installable skill candidates" not in source.lower()
    assert "0 supported skill assets" in starter
    assert "remain separate skill candidates—not supported Starter v1 assets" in starter
    assert "00</strong><span>supported skills today" in collections
    assert "not part of the current 9-file Starter archive" in home
    assert "One Starter runtime observation exists" in starter
    assert "0 PASS, 0 FAIL, 1 INCONCLUSIVE" in starter
    assert "clean independent surface" in starter
    assert not STARTER_CHECKOUT.exists()

    assert gate["truth"]["starter_sku_workflow_runtime_observations"] == 1
    assert gate["truth"]["starter_sku_workflow_runtime_passes"] == 0
    assert gate["truth"]["starter_sku_workflow_runtime_fails"] == 0
    assert gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 1
    assert gate["starter_behavioral_canary_freeze"]["armed_cases"] == 0
    assert gate["runtime_protocol_correction"]["effective_result"] == "INCONCLUSIVE_PROTOCOL_CONTAMINATION"
    assert gate["runtime_protocol_correction"]["effective_decision"] == "EXPAND_EVIDENCE"
    assert gate["runtime_protocol_correction"]["historical_fail_review_preserved"] is True
    assert gate["runtime_protocol_correction"]["successor_required_before_clean_retest"] is False
    assert gate["runtime_protocol_correction"]["same_frozen_candidate_retest_required"] is True
    assert gate["runtime_protocol_correction"]["armed"] is False
    assert gate["gates"]["starter_specific_behavioral_evidence"] == "OBSERVED_ONE_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"

    assert gate["launch_requirements"]["STARTER_PRODUCT_READY"] is False
    assert gate["launch_requirements"]["PROVIDER_CUSTODY"] is False
    assert gate["launch_requirements"]["PROVIDER_INTEGRATION"] is False
    assert gate["launch_requirements"]["LIVE_DELIVERY_CANARY"] is False
    assert gate["launch_requirements"]["PUBLIC_COPY_EVIDENCE_AUDIT"] is True
    assert gate["truth"]["real_purchases"] == 0
    assert gate["truth"]["public_checkout_enabled"] is False
    assert gate["truth"]["ready_to_sell"] is False

    print("STARTER LAUNCH CHECKPOINT V1: PASS")
    print("starter_supported_skills=0")
    print("starter_structural_skill_candidates=2")
    print("skill_launch_scope=DEFERRED_NON_BLOCKING")
    print("public_copy_historical_skill_retest=33805620505:success")
    print(f"public_copy_current_retest={CURRENT_COPY_RUN}:success")
    print("public_copy_current_state=PASS_CURRENT_EVIDENCE_BOUNDARY")
    print("release_frontier=N09,N14")
    print("provider_preflight=PASS_STATIC_DISARMED")
    print("provider_side_effects=0")
    print("starter_runtime_observations=1")
    print("starter_runtime_passes=0")
    print("starter_runtime_fails=0")
    print("starter_runtime_inconclusive=1")
    print("public_checkout=BLOCKED")
    print("ready_to_sell=false")
    print("additional_model_calls_after_canary=0")
    print("provider_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
