#!/usr/bin/env python3
"""Validate the Prompt Machine Starter release evidence DAG.

This is a deterministic dependency/truth check. It does not execute models,
providers, checkout, purchases, or delivery.
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

CLOSED = {"STATIC_CLOSED", "OBSERVED_CLOSED", "DEFERRED_NON_BLOCKING"}
OPEN_FRONTIER = {
    "OPEN_REQUIRES_MODEL_AUTH",
    "OPEN_REQUIRES_PROVIDER_AUTH",
    "OPEN_REQUIRES_SUCCESSOR_REWORK",
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
    assert dag["product_id"] == "prompt-machine-starter-collection"
    assert dag["master_rule"] == "A DOWNSTREAM NODE MAY CLOSE ONLY FROM THE EVIDENCE REQUIRED BY ITS INCOMING DEPENDENCIES"

    nodes = {row["id"]: row for row in dag["nodes"]}
    assert len(nodes) == 20
    assert len(nodes) == len(dag["nodes"]), "duplicate node ids"

    valid_status = set(dag["status_vocabulary"])
    assert CLOSED | OPEN_FRONTIER | BLOCKED <= valid_status

    # Dependency references and graph acyclicity.
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

    # Every closed/deferred node must cite evidence that actually exists.
    for node in nodes.values():
        if node["status"] in CLOSED:
            assert node["evidence"], f"closed node lacks evidence: {node['id']}"
            for relative in node["evidence"]:
                assert (ROOT / relative).is_file(), f"missing evidence path for {node['id']}: {relative}"

    # A closed node cannot depend on an unresolved node.
    for node in nodes.values():
        if node["status"] in CLOSED:
            for dep in node["depends_on"]:
                assert nodes[dep]["status"] in CLOSED, f"{node['id']} closed above unresolved {dep}"

    # Current frontier preserves the reviewed runtime failure, required successor rework,
    # stale public-copy audit, and independently disarmed provider lane.
    frontier_ids = {node_id for node_id, row in nodes.items() if row["status"] in OPEN_FRONTIER}
    assert frontier_ids == {"N07_PUBLIC_COPY_BOUNDARY", "N09_STARTER_RUNTIME_EVIDENCE", "N14_PROVIDER_PROVISIONING_AND_CUSTODY"}
    configured_frontier = {row["node"] for row in dag["current_frontier"]["next_evidence_purchase_options"]}
    assert configured_frontier == frontier_ids
    assert dag["current_frontier"]["automatic_choice_between_frontier_nodes"] is False

    n09 = nodes["N09_STARTER_RUNTIME_EVIDENCE"]
    assert n09["status"] == "OPEN_REQUIRES_SUCCESSOR_REWORK"
    assert n09["observed_result"] == "FAIL"
    assert n09["decision"] == "REWORK"
    assert len(n09["evidence"]) == 4
    assert all((ROOT / relative).is_file() for relative in n09["evidence"])
    assert n09["next_experiment"] == "NEW_SUCCESSOR_VERSION_THEN_PM-STARTER-CR-NORMAL-0001_RETEST"
    assert n09["maximum_calls_before_review"] == 1
    assert n09["automatic_retries"] == 0

    frozen_case = next(row for row in canary["cases"] if row["case_id"] == n09["next_experiment"])
    assert frozen_case["armed"] is False
    assert frozen_case["runtime_executed"] is False
    assert frozen_case["runtime_envelope_sha256"] == "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
    assert canary["next_permitted_runtime_sequence"]["authorized_now"] is False

    n07 = nodes["N07_PUBLIC_COPY_BOUNDARY"]
    assert n07["status"] == "OPEN_REQUIRES_COPY_REAUDIT"
    assert gate["public_copy_audit"]["state"] == "STALE_AFTER_STARTER_RUNTIME_EVIDENCE_CHANGE"

    n14 = nodes["N14_PROVIDER_PROVISIONING_AND_CUSTODY"]
    assert n14["status"] == "OPEN_REQUIRES_PROVIDER_AUTH"
    assert n14["maximum_custody_attempts_before_review"] == 1
    assert n14["automatic_retries"] == 0
    assert preflight["execution_limits"]["custody_packet_armed"] is False
    assert preflight["current_truth"]["provider_side_effects_executed"] is False

    # Downstream evidence claims remain blocked in the correct order.
    assert nodes["N15_PROVIDER_INTEGRATION_PASS"]["status"] == "BLOCKED_BY_UPSTREAM_EVIDENCE"
    assert nodes["N16_LIVE_DELIVERY_CANARY"]["status"] == "BLOCKED_BY_UPSTREAM_EVIDENCE"
    assert nodes["N17_STARTER_PRODUCT_READY_REVIEW"]["status"] == "BLOCKED_BY_UPSTREAM_EVIDENCE"
    assert nodes["N18_PUBLIC_CHECKOUT_DECISION"]["status"] == "BLOCKED_BY_HUMAN_RELEASE_DECISION"
    assert nodes["N19_PQ_DOLLAR_ONE"]["status"] == "NOT_STARTED"
    assert nodes["N20_REAL_ACTIVATION_AND_RETENTION"]["status"] == "NOT_STARTED"

    # Cross-check independent current-truth sources.
    assert skill_scope["state"] == "SKILLS_DEFERRED_FROM_V1_LAUNCH_PAYLOAD_EVIDENCE_OPEN"
    assert skill_scope["current_truth"]["starter_supported_skills"] == 0
    assert copy_receipt["final_state"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert execution_freeze["state"] == "STATIC_EXECUTION_DECISION_GOVERNANCE_PASS_REAL_EXECUTION_UNAUTHORIZED"

    truth = dag["truth"]
    assert truth["starter_runtime_observations"] == gate["truth"]["starter_sku_workflow_runtime_observations"] == 1
    assert truth["starter_runtime_passes"] == gate["truth"]["starter_sku_workflow_runtime_passes"] == 0
    assert truth["starter_runtime_fails"] == gate["truth"]["starter_sku_workflow_runtime_fails"] == 1
    assert truth["starter_runtime_inconclusive"] == gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 0
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
    assert not STARTER_CHECKOUT.exists()

    print("STARTER RELEASE DAG V1: PASS")
    print("nodes=20")
    print("cycles=0")
    print("closed_or_deferred_nodes=11")
    print("frontier_nodes=3")
    print("frontier=N07_PUBLIC_COPY_BOUNDARY,N09_STARTER_RUNTIME_EVIDENCE,N14_PROVIDER_PROVISIONING_AND_CUSTODY")
    print("starter_runtime_observations=1")
    print("starter_runtime_fails=1")
    print("starter_runtime_decision=REWORK")
    print("runtime_authorized_now=false")
    print("provider_authorized_now=false")
    print("public_checkout=false")
    print("pq_dollar_one=false")
    print("provider_calls=0")
    print("additional_model_calls_after_canary=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
