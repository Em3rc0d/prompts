#!/usr/bin/env python3
"""Validate the Prompt Machine Starter release evidence DAG.

Deterministic dependency/truth check only. No model, provider, checkout,
purchase, delivery, or customer-value execution occurs.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMERCIAL = ROOT / "commercial"
BASE = ROOT / "product" / "starter-collection-v1"

DAG_PATH = COMMERCIAL / "STARTER_RELEASE_DAG_V1.json"
GATE_PATH = COMMERCIAL / "STARTER_RELEASE_GATE_V1.json"
CANARY_PATH = BASE / "evaluation" / "STARTER_CANARY_FREEZE_V1.json"
PREFLIGHT_PATH = COMMERCIAL / "STARTER_PROVIDER_PREFLIGHT_FREEZE_V1.json"
SKILL_SCOPE_PATH = COMMERCIAL / "STARTER_SKILL_LAUNCH_SCOPE_V1.json"
COPY_RECEIPT_PATH = COMMERCIAL / "STARTER_PUBLIC_COPY_AUDIT_RECEIPT_V1.json"
EXECUTION_FREEZE_PATH = COMMERCIAL / "STARTER_EXECUTION_DECISION_FREEZE_V1.json"
STARTER_CHECKOUT = ROOT / "web" / "app" / "api" / "commerce" / "starter-collection" / "checkout" / "route.ts"

CURRENT_COPY_RUN = 33834092608
CURRENT_COPY_COMMIT = "bd086c2e7fd76bc3852eea7d2e048341dce25ed4"

CLOSED = {"STATIC_CLOSED", "OBSERVED_CLOSED", "DEFERRED_NON_BLOCKING"}
OPEN_FRONTIER = {
    "OPEN_REQUIRES_MODEL_AUTH",
    "OPEN_REQUIRES_PROVIDER_AUTH",
    "OPEN_REQUIRES_COPY_REAUDIT",
}
BLOCKED = {"BLOCKED_BY_UPSTREAM_EVIDENCE", "BLOCKED_BY_HUMAN_RELEASE_DECISION", "NOT_STARTED"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    dag = load(DAG_PATH)
    gate = load(GATE_PATH)
    canary = load(CANARY_PATH)
    preflight = load(PREFLIGHT_PATH)
    skill_scope = load(SKILL_SCOPE_PATH)
    copy_receipt = load(COPY_RECEIPT_PATH)
    execution_freeze = load(EXECUTION_FREEZE_PATH)

    assert dag["schema"] == "prompt-machine-starter-release-dag-v1"
    assert dag["version"] == "1.3.0"
    assert dag["product_id"] == "prompt-machine-starter-collection"
    assert dag["master_rule"] == "A DOWNSTREAM NODE MAY CLOSE ONLY FROM THE EVIDENCE REQUIRED BY ITS INCOMING DEPENDENCIES"

    nodes = {row["id"]: row for row in dag["nodes"]}
    assert len(nodes) == 20
    assert len(nodes) == len(dag["nodes"]), "duplicate node ids"

    valid_status = set(dag["status_vocabulary"])
    assert CLOSED | OPEN_FRONTIER | BLOCKED <= valid_status

    for node in nodes.values():
        assert node["status"] in valid_status
        for dep in node["depends_on"]:
            assert dep in nodes, f"unknown dependency {dep}"

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visited:
            return
        assert node_id not in visiting, f"cycle detected at {node_id}"
        visiting.add(node_id)
        for dep in nodes[node_id]["depends_on"]:
            visit(dep)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in nodes:
        visit(node_id)
    assert len(visited) == 20

    for node in nodes.values():
        if node["status"] in CLOSED:
            assert node["evidence"], f"closed node lacks evidence: {node['id']}"
            for relative in node["evidence"]:
                assert (ROOT / relative).is_file(), f"missing evidence path for {node['id']}: {relative}"

    for node in nodes.values():
        if node["status"] in CLOSED:
            for dep in node["depends_on"]:
                assert nodes[dep]["status"] in CLOSED, f"{node['id']} closed above unresolved {dep}"

    frontier_ids = {node_id for node_id, row in nodes.items() if row["status"] in OPEN_FRONTIER}
    assert frontier_ids == {"N09_STARTER_RUNTIME_EVIDENCE", "N14_PROVIDER_PROVISIONING_AND_CUSTODY"}
    configured_frontier = {row["node"] for row in dag["current_frontier"]["next_evidence_purchase_options"]}
    assert configured_frontier == frontier_ids
    assert dag["current_frontier"]["automatic_choice_between_frontier_nodes"] is False
    assert len(dag["current_frontier"]["closed_or_intentionally_deferred_nodes"]) == 12

    n07 = nodes["N07_PUBLIC_COPY_BOUNDARY"]
    assert n07["status"] == "OBSERVED_CLOSED"
    assert n07["depends_on"] == ["N05_DETERMINISTIC_ARCHIVE", "N06_SKILL_SCOPE"]
    assert n07["current_retest_run_id"] == CURRENT_COPY_RUN
    assert n07["current_audited_commit"] == CURRENT_COPY_COMMIT
    assert gate["public_copy_audit"]["state"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert gate["public_copy_audit"]["current_retest_run_id"] == CURRENT_COPY_RUN
    assert copy_receipt["version"] == "1.2.0"
    assert copy_receipt["final_state"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert copy_receipt["current_retest"]["run_id"] == CURRENT_COPY_RUN
    assert copy_receipt["current_retest"]["audited_commit"] == CURRENT_COPY_COMMIT

    n09 = nodes["N09_STARTER_RUNTIME_EVIDENCE"]
    assert n09["status"] == "OPEN_REQUIRES_MODEL_AUTH"
    assert n09["observed_result"] == "INCONCLUSIVE_PROTOCOL_CONTAMINATION"
    assert n09["decision"] == "EXPAND_EVIDENCE"
    assert len(n09["evidence"]) == 6
    assert all((ROOT / relative).is_file() for relative in n09["evidence"])
    assert n09["next_experiment"] == "RETEST_PM-STARTER-CR-NORMAL-0001_CLEAN_INDEPENDENT_SURFACE"
    assert n09["maximum_calls_before_review"] == 1
    assert n09["automatic_retries"] == 0
    assert n09["candidate_mutation_required"] is False
    assert n09["fresh_authorization_required"] is True
    assert n09["clean_independent_surface_required"] is True

    frozen_case = next(row for row in canary["cases"] if row["case_id"] == "PM-STARTER-CR-NORMAL-0001")
    assert frozen_case["armed"] is False
    assert frozen_case["runtime_executed"] is False
    assert frozen_case["runtime_envelope_sha256"] == "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
    assert canary["next_permitted_runtime_sequence"]["authorized_now"] is False

    n14 = nodes["N14_PROVIDER_PROVISIONING_AND_CUSTODY"]
    assert n14["status"] == "OPEN_REQUIRES_PROVIDER_AUTH"
    assert n14["maximum_custody_attempts_before_review"] == 1
    assert n14["automatic_retries"] == 0
    assert preflight["execution_limits"]["custody_packet_armed"] is False
    assert preflight["current_truth"]["provider_side_effects_executed"] is False

    assert nodes["N15_PROVIDER_INTEGRATION_PASS"]["status"] == "BLOCKED_BY_UPSTREAM_EVIDENCE"
    assert nodes["N16_LIVE_DELIVERY_CANARY"]["status"] == "BLOCKED_BY_UPSTREAM_EVIDENCE"
    assert nodes["N17_STARTER_PRODUCT_READY_REVIEW"]["status"] == "BLOCKED_BY_UPSTREAM_EVIDENCE"
    assert nodes["N18_PUBLIC_CHECKOUT_DECISION"]["status"] == "BLOCKED_BY_HUMAN_RELEASE_DECISION"
    assert nodes["N19_PQ_DOLLAR_ONE"]["status"] == "NOT_STARTED"
    assert nodes["N20_REAL_ACTIVATION_AND_RETENTION"]["status"] == "NOT_STARTED"

    assert skill_scope["state"] == "SKILLS_DEFERRED_FROM_V1_LAUNCH_PAYLOAD_EVIDENCE_OPEN"
    assert skill_scope["current_truth"]["starter_supported_skills"] == 0
    assert execution_freeze["state"] == "STATIC_EXECUTION_DECISION_GOVERNANCE_PASS_REAL_EXECUTION_UNAUTHORIZED"

    truth = dag["truth"]
    assert truth["starter_runtime_observations"] == gate["truth"]["starter_sku_workflow_runtime_observations"] == 1
    assert truth["starter_runtime_passes"] == gate["truth"]["starter_sku_workflow_runtime_passes"] == 0
    assert truth["starter_runtime_fails"] == gate["truth"]["starter_sku_workflow_runtime_fails"] == 0
    assert truth["starter_runtime_inconclusive"] == gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 1
    assert truth["provider_custody_observations"] == gate["truth"]["provider_custody_observations"] == 0
    assert truth["provider_integration_pass"] is False
    assert gate["launch_requirements"]["PROVIDER_INTEGRATION"] is False
    assert truth["live_delivery_canary_pass"] is False
    assert gate["launch_requirements"]["LIVE_DELIVERY_CANARY"] is False
    assert truth["starter_product_ready"] is False
    assert gate["launch_requirements"]["STARTER_PRODUCT_READY"] is False
    assert truth["public_checkout"] is False
    assert gate["truth"]["public_checkout_enabled"] is False
    assert truth["real_purchases"] == gate["truth"]["real_purchases"] == 0
    assert truth["pq_dollar_one"] is False
    assert gate["gates"]["pq_dollar_one"] == "NOT_OBSERVED"
    assert gate["gates"]["public_copy_evidence_audit"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert not STARTER_CHECKOUT.exists()

    print("STARTER RELEASE DAG V1: PASS")
    print("nodes=20")
    print("cycles=0")
    print("closed_or_deferred_nodes=12")
    print("frontier_nodes=2")
    print("frontier=N09_STARTER_RUNTIME_EVIDENCE,N14_PROVIDER_PROVISIONING_AND_CUSTODY")
    print(f"public_copy_boundary=OBSERVED_CLOSED:{CURRENT_COPY_RUN}")
    print("starter_runtime_observations=1")
    print("starter_runtime_fails=0")
    print("starter_runtime_inconclusive=1")
    print("starter_runtime_decision=EXPAND_EVIDENCE")
    print("runtime_authorized_now=false")
    print("provider_authorized_now=false")
    print("public_checkout=false")
    print("pq_dollar_one=false")
    print("provider_calls=0")
    print("additional_model_calls_after_canary=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
