#!/usr/bin/env python3
"""Apply the append-only correction for PM-STARTER-CR-NORMAL-0001.

This migration preserves the raw output, original human review, and original
failure record. It adds a correction receipt and changes only the *effective*
workflow classification from FAIL/REWORK to INCONCLUSIVE/EXPAND_EVIDENCE
because the active runtime conversation had prior exposure to evaluation
expectations. No workflow surface is changed and no model/provider call occurs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "product" / "starter-collection-v1"
EVAL = BASE / "evaluation"
CASE_ID = "PM-STARTER-CR-NORMAL-0001"
OBS_ID = f"{CASE_ID}-OBS-0001"
ORIGINAL_REVIEW_ID = f"{CASE_ID}-HR-0001"
ORIGINAL_FAILURE_ID = f"{CASE_ID}-FAIL-0001"
CORRECTION_ID = f"{CASE_ID}-CORR-0001"
RAW_SHA = "a55477e670ce059a4356943fbfedc58e56109711985ff5dc183889a65e77e1e7"
ENVELOPE_SHA = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
RECORDED_AT = "2026-09-04T03:20:00Z"

CORRECTION_REL = f"product/starter-collection-v1/evaluation/corrections/{CASE_ID}.protocol-contamination.json"
CLEAN_SURFACE_REL = "commercial/STARTER_CLEAN_RUNTIME_SURFACE_REQUIREMENTS_V1.json"
ORIGINAL_REVIEW_REL = f"product/starter-collection-v1/evaluation/human-reviews/{CASE_ID}.human-review.json"
ORIGINAL_FAILURE_REL = f"product/starter-collection-v1/evaluation/failures/{CASE_ID}.failure.json"
OBS_REL = f"product/starter-collection-v1/evaluation/observations/{CASE_ID}.observation.json"
RAW_REL = f"product/starter-collection-v1/evaluation/observations/{CASE_ID}.raw-output.md"


def read_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, value: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def preserve_source_artifacts() -> None:
    raw = ROOT / RAW_REL
    assert raw.exists()
    assert hashlib.sha256(raw.read_bytes()).hexdigest() == RAW_SHA

    obs = read_json(OBS_REL)
    review = read_json(ORIGINAL_REVIEW_REL)
    failure = read_json(ORIGINAL_FAILURE_REL)
    assert obs["observation_id"] == OBS_ID
    assert obs["runtime_envelope_sha256"] == ENVELOPE_SHA
    assert obs["raw_output_sha256"] == RAW_SHA
    assert obs["execution_surface"] == "CHATGPT_WORK_ACTIVE_CONVERSATION"
    assert review["review_id"] == ORIGINAL_REVIEW_ID
    assert review["result"] == "FAIL"
    assert review["decision"] == "REWORK"
    assert failure["failure_id"] == ORIGINAL_FAILURE_ID


def write_correction_receipts() -> None:
    correction = {
        "schema": "prompt-machine-starter-runtime-classification-correction-v1",
        "version": "1.0.0",
        "correction_id": CORRECTION_ID,
        "case_id": CASE_ID,
        "observation_id": OBS_ID,
        "workflow_id": "pm-starter-evidence-first-code-review",
        "workflow_version": "1.0.0-candidate",
        "correction_class": "PROTOCOL_CONTAMINATION",
        "historical_artifacts": {
            "raw_output": RAW_REL,
            "observation_receipt": OBS_REL,
            "original_human_review": ORIGINAL_REVIEW_REL,
            "original_failure_record": ORIGINAL_FAILURE_REL,
            "raw_output_sha256": RAW_SHA,
            "runtime_envelope_sha256": ENVELOPE_SHA,
            "preserved_without_rewrite": True,
        },
        "protocol_basis": {
            "frozen_protocol": "commercial/STARTER_RUNTIME_TRUST_UPDATE_PROTOCOL_V1.json",
            "required_invariant": "evaluation contract and expected result remain out-of-band and unavailable to runtime input",
            "observed_surface": "CHATGPT_WORK_ACTIVE_CONVERSATION",
            "contamination_fact": "Before the runtime response, the active conversation had already contained the expected review state, ship recommendation, and LIKELY evidence ceiling.",
            "why_original_fail_is_not_effective_workflow_evidence": "The model response cannot be shown to have been produced without prior access to the evaluation expectations, so the execution cannot cleanly discriminate workflow behavior from contaminated context.",
        },
        "historical_classification": {
            "review_result": "FAIL",
            "decision": "REWORK",
            "workflow_fail_count_incremented": True,
            "status": "PRESERVED_AS_HISTORICAL_MISCLASSIFICATION",
        },
        "effective_classification": {
            "review_result": "INCONCLUSIVE",
            "decision": "EXPAND_EVIDENCE",
            "reason": "INCONCLUSIVE_PROTOCOL_CONTAMINATION",
            "workflow_pass_count": 0,
            "workflow_fail_count": 0,
            "workflow_inconclusive_count": 1,
            "runtime_observation_count": 1,
        },
        "workflow_mutation": {
            "observed_candidate_mutated": False,
            "successor_required_by_this_observation": False,
            "design_signal_preserved": "The contaminated output still provides a non-claim design signal about possible over-certainty, but it cannot justify a behavioral FAIL claim or mandatory successor.",
        },
        "next_evidence": {
            "case_id": CASE_ID,
            "candidate": "SAME_FROZEN_1.0.0_CANDIDATE",
            "requires_clean_independent_surface": True,
            "requires_fresh_explicit_authorization": True,
            "maximum_submissions_before_human_review": 1,
            "automatic_retries": 0,
            "automatic_second_case": False,
            "armed": False,
        },
        "claim_boundary": {
            "runtime_pass_claim": False,
            "runtime_fail_claim": False,
            "certification_claim": False,
            "product_ready_claim": False,
            "ready_to_sell": False,
        },
        "recorded_at": RECORDED_AT,
    }
    write_json(CORRECTION_REL, correction)

    clean = {
        "schema": "prompt-machine-starter-clean-runtime-surface-requirements-v1",
        "version": "1.0.0",
        "recorded_on": "2026-09-04",
        "state": "FROZEN_AFTER_PROTOCOL_CONTAMINATION_DISARMED",
        "applies_to": [CASE_ID],
        "purpose": "Prevent evaluation leakage from being counted as Starter workflow behavioral evidence.",
        "requirement": "CLEAN_INDEPENDENT_EXECUTION_SURFACE",
        "not_a_requirement": "CHATGPT_DOT_COM_SPECIFICALLY",
        "pre_execution_invariants": [
            "The runtime conversation/session must not have previously contained the evaluation contract, expected result, answer key, or human review.",
            "The runtime receives the exact frozen envelope and no additional task-relevant instruction that changes workflow authority or expected state.",
            "The frozen envelope SHA-256 must match d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207.",
            "Fresh explicit authorization must name the exact case, one execution, and zero retries.",
            "Maximum submissions before human review is one; automatic retries and automatic second-case execution are zero.",
        ],
        "surface_evidence_to_record": [
            "execution_surface",
            "fresh_session_or_context_identity_when_observable",
            "statement_that_evaluation_expectations_were_not_present_before_runtime",
            "runtime_envelope_sha256",
            "model_identity_when_observable",
        ],
        "fail_closed_rule": "If clean-context independence cannot be established with reasonable confidence before execution, block before model use. If contamination is discovered only afterward, preserve the output but classify the workflow result INCONCLUSIVE_PROTOCOL_CONTAMINATION.",
        "same_candidate_retest_allowed": True,
        "successor_required_before_clean_retest": False,
        "automatic_execution": False,
        "automatic_retries": 0,
        "provider_calls_created": 0,
        "model_calls_created": 0,
    }
    write_json(CLEAN_SURFACE_REL, clean)


def patch_trust_context() -> None:
    rel = "product/starter-collection-v1/trust/code-review.trust-context.json"
    trust = read_json(rel)
    trust["version"] = "1.0.2"
    trust["current_evidence_state"] = "ONE_RUNTIME_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"

    runtime = trust["runtime_evidence"]
    runtime["passes"] = 0
    runtime["fails"] = 0
    runtime["inconclusive"] = 1
    runtime["review_corrections"] = [{
        "correction_id": CORRECTION_ID,
        "path": CORRECTION_REL,
        "historical_review_id": ORIGINAL_REVIEW_ID,
        "historical_result": "FAIL",
        "effective_result": "INCONCLUSIVE",
        "effective_decision": "EXPAND_EVIDENCE",
        "reason": "PROTOCOL_CONTAMINATION",
    }]
    runtime["regressions"] = []
    runtime["retest_requirements"] = [
        "same frozen PM-STARTER-CR-NORMAL-0001 candidate",
        "clean independent execution surface",
        "fresh explicit authorization",
        "one submission before human review",
        "zero retries",
    ]

    for item in trust.get("historical_failures", []):
        if item.get("failure_id") == ORIGINAL_FAILURE_ID:
            item["historical_classification_artifact"] = True
            item["effective_workflow_failure"] = False
            item["superseded_by_correction"] = CORRECTION_REL
            item["decision"] = "HISTORICAL_REWORK_SUPERSEDED_BY_INCONCLUSIVE_PROTOCOL_CONTAMINATION"

    trust["protocol_corrections"] = [{
        "correction_id": CORRECTION_ID,
        "path": CORRECTION_REL,
        "clean_surface_requirements": CLEAN_SURFACE_REL,
        "effective_result": "INCONCLUSIVE",
    }]

    limitations = trust.get("known_limitations", [])
    if limitations:
        limitations[0] = "The only Starter-specific code-review runtime observation is protocol-contaminated and cannot support a workflow PASS or FAIL claim."
    else:
        limitations.append("The only Starter-specific code-review runtime observation is protocol-contaminated and cannot support a workflow PASS or FAIL claim.")
    if "No clean independent Starter-specific code-review runtime observation exists yet." not in limitations:
        limitations.append("No clean independent Starter-specific code-review runtime observation exists yet.")
    trust["known_limitations"] = limitations

    trust["next_evidence"] = {
        "preferred_first_case": "RETEST_SAME_FROZEN_PM-STARTER-CR-NORMAL-0001_ON_CLEAN_INDEPENDENT_SURFACE",
        "clean_surface_requirements": CLEAN_SURFACE_REL,
        "automatic_execution": False,
        "automatic_retries": 0,
        "human_review_required": True,
        "armed": False,
    }

    nonclaims = list(dict.fromkeys(trust.get("explicit_non_claims", []) + [
        "NO_RUNTIME_PASS_CLAIM",
        "NO_RUNTIME_FAIL_CLAIM",
        "NOT_CERTIFIED",
        "NOT_READY_TO_SELL",
    ]))
    trust["explicit_non_claims"] = nonclaims
    trust["truth_boundary"]["protocol_contaminated_execution_counts_as_workflow_fail"] = False
    trust["truth_boundary"]["protocol_contaminated_execution_counts_as_workflow_pass"] = False
    write_json(rel, trust)


def patch_release_gate() -> None:
    rel = "commercial/STARTER_RELEASE_GATE_V1.json"
    gate = read_json(rel)
    gate["version"] = "1.0.9"
    gate["checkpoint_revision"] = "runtime-protocol-contamination-correction-20260904"

    truth = gate["truth"]
    truth["starter_sku_workflow_runtime_observations"] = 1
    truth["starter_sku_workflow_runtime_passes"] = 0
    truth["starter_sku_workflow_runtime_fails"] = 0
    truth["starter_sku_workflow_runtime_inconclusive"] = 1

    canary = gate["starter_behavioral_canary_freeze"]
    canary["state"] = "ONE_RUNTIME_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"
    canary["runtime_observations"] = 1
    canary["runtime_passes"] = 0
    canary["runtime_fails"] = 0
    canary["runtime_inconclusive"] = 1
    canary["first_case_when_reopened"] = "RETEST_SAME_FROZEN_PM-STARTER-CR-NORMAL-0001_ON_CLEAN_INDEPENDENT_SURFACE_AFTER_FRESH_AUTHORIZATION"

    gate["runtime_protocol_correction"] = {
        "correction": CORRECTION_REL,
        "clean_surface_requirements": CLEAN_SURFACE_REL,
        "historical_fail_review_preserved": True,
        "effective_result": "INCONCLUSIVE_PROTOCOL_CONTAMINATION",
        "effective_decision": "EXPAND_EVIDENCE",
        "successor_required_before_clean_retest": False,
        "same_frozen_candidate_retest_required": True,
        "armed": False,
    }

    audit = gate["public_copy_audit"]
    audit["state"] = "STALE_AFTER_STARTER_RUNTIME_EVIDENCE_CHANGE"
    audit["stale_reason"] = "The audited public evidence boundary predates the first Starter runtime observation and its protocol-contamination correction; current effective runtime state is one INCONCLUSIVE observation, zero PASS, zero FAIL."

    trust = gate["workflow_trust_history"]
    trust["runtime_events"] = 1
    trust["reviewed_passes"] = 0
    trust["reviewed_fails"] = 0
    trust["reviewed_inconclusive"] = 1

    gates = gate["gates"]
    gates["starter_specific_behavioral_evidence"] = "OBSERVED_ONE_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"
    gates["public_copy_evidence_audit"] = "STALE_AFTER_RUNTIME_EVIDENCE_CHANGE"

    stop = gate["launch_critical_static_stop_line"]
    stop["state"] = "RUNTIME_FRONTIER_OBSERVED_INCONCLUSIVE_CLEAN_RETEST_REQUIRED"
    stop["model_frontier"] = {
        "node": "N09_STARTER_RUNTIME_EVIDENCE",
        "authorized_now": False,
        "current_result": "ONE_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION",
        "next_step": "RETEST_SAME_FROZEN_CASE_ON_CLEAN_INDEPENDENT_SURFACE_ONLY_AFTER_FRESH_AUTHORIZATION",
    }

    gate["next_zero_model_work"] = [
        "re-audit customer-facing copy against the corrected runtime evidence state before treating copy evidence as current",
        "preserve the original raw output, original FAIL/REWORK review, and original failure record as historical artifacts superseded only for effective workflow classification",
    ]
    gate["next_external_evidence_options"] = [
        "freshly authorize one clean independent retest of the same frozen PM-STARTER-CR-NORMAL-0001 candidate",
        "separately authorize one controlled provider provisioning/custody attempt",
    ]

    boundaries = gate["boundaries"]
    boundaries["protocol_contaminated_execution_implies_workflow_fail"] = False
    boundaries["protocol_contaminated_execution_implies_successor_required"] = False
    write_json(rel, gate)


def patch_release_dag() -> None:
    rel = "commercial/STARTER_RELEASE_DAG_V1.json"
    dag = read_json(rel)
    dag["version"] = "1.2.0"
    dag["recorded_on"] = "2026-09-04"

    nodes = {row["id"]: row for row in dag["nodes"]}
    n09 = nodes["N09_STARTER_RUNTIME_EVIDENCE"]
    n09["status"] = "OPEN_REQUIRES_MODEL_AUTH"
    n09["evidence"] = list(dict.fromkeys(n09.get("evidence", []) + [CORRECTION_REL, CLEAN_SURFACE_REL]))
    n09["next_experiment"] = "RETEST_PM-STARTER-CR-NORMAL-0001_CLEAN_INDEPENDENT_SURFACE"
    n09["maximum_calls_before_review"] = 1
    n09["automatic_retries"] = 0
    n09["observed_result"] = "INCONCLUSIVE_PROTOCOL_CONTAMINATION"
    n09["decision"] = "EXPAND_EVIDENCE"
    n09["candidate_mutation_required"] = False
    n09["fresh_authorization_required"] = True
    n09["clean_independent_surface_required"] = True

    n07 = nodes["N07_PUBLIC_COPY_BOUNDARY"]
    n07["status"] = "OPEN_REQUIRES_COPY_REAUDIT"
    n07["next_action"] = "Re-audit customer-facing copy against one protocol-contaminated INCONCLUSIVE runtime observation; public checkout remains blocked."

    for option in dag["current_frontier"].get("next_evidence_purchase_options", []):
        if option.get("node") == "N09_STARTER_RUNTIME_EVIDENCE":
            option["requires"] = "CLEAN_INDEPENDENT_SURFACE_THEN_FRESH_EXPLICIT_MODEL_BUDGET_AUTHORIZATION"
            option["smallest_experiment"] = "RETEST SAME FROZEN PM-STARTER-CR-NORMAL-0001 ONCE; ZERO RETRIES; HUMAN REVIEW"

    truth = dag["truth"]
    truth["starter_runtime_observations"] = 1
    truth["starter_runtime_passes"] = 0
    truth["starter_runtime_fails"] = 0
    truth["starter_runtime_inconclusive"] = 1
    write_json(rel, dag)


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement + text[b:]


def patch_release_gate_validator() -> None:
    path = ROOT / "tools" / "validate_starter_release_gate_v1.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('assert gate["version"] == "1.0.7"', 'assert gate["version"] == "1.0.9"')
    text = text.replace('assert truth["starter_sku_workflow_runtime_observations"] == 0', 'assert truth["starter_sku_workflow_runtime_observations"] == 1')

    fn = '''def validate_trust_context(path: Path, workflow_id: str) -> None:\n    trust = read_json(path)\n    assert trust["schema"] == "prompt-machine-workflow-trust-context-v1"\n    assert trust["workflow_id"] == workflow_id\n    assert trust["publication_state"] == "NOT_PUBLIC_NOT_ELIGIBLE"\n    if workflow_id == "pm-starter-evidence-first-code-review":\n        assert trust["current_evidence_state"] == "ONE_RUNTIME_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"\n        assert len(trust["runtime_evidence"]["observations"]) == 1\n        assert trust["runtime_evidence"]["passes"] == 0\n        assert trust["runtime_evidence"]["fails"] == 0\n        assert trust["runtime_evidence"]["inconclusive"] == 1\n        assert trust["runtime_evidence"]["review_corrections"][0]["effective_result"] == "INCONCLUSIVE"\n        assert trust["protocol_corrections"][0]["correction_id"] == "PM-STARTER-CR-NORMAL-0001-CORR-0001"\n        assert trust["truth_boundary"]["protocol_contaminated_execution_counts_as_workflow_fail"] is False\n    else:\n        assert trust["current_evidence_state"] == "STATIC_CONTRACT_AND_SURFACE_FROZEN_RUNTIME_UNOBSERVED"\n        assert trust["runtime_evidence"]["observations"] == []\n        assert trust["runtime_evidence"]["passes"] == 0\n        assert trust["runtime_evidence"]["fails"] == 0\n        assert trust["runtime_evidence"]["inconclusive"] == 0\n    assert trust["next_evidence"]["armed"] is False\n    assert trust["truth_boundary"]["zero_failures_with_zero_runtime_observations_means_reliable"] is False\n    assert trust["truth_boundary"]["automatic_publication"] is False\n\n\n'''
    text = replace_between(text, "def validate_trust_context", "def main()", fn)

    marker = 'assert truth["starter_sku_workflow_runtime_observations"] == 1'
    if 'starter_sku_workflow_runtime_inconclusive' not in text[text.index(marker):text.index(marker)+500]:
        text = text.replace(marker, marker + '\n    assert truth["starter_sku_workflow_runtime_passes"] == 0\n    assert truth["starter_sku_workflow_runtime_fails"] == 0\n    assert truth["starter_sku_workflow_runtime_inconclusive"] == 1')

    # Historical canary freeze remains immutable at zero runtime; the release gate carries live runtime truth.
    path.write_text(text, encoding="utf-8")


def patch_dag_validator() -> None:
    path = ROOT / "tools" / "validate_starter_release_dag_v1.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('"OPEN_REQUIRES_SUCCESSOR_REWORK"', '"OPEN_REQUIRES_MODEL_AUTH"')
    text = text.replace('"NEW_SUCCESSOR_VERSION_THEN_PM-STARTER-CR-NORMAL-0001_RETEST"', '"RETEST_PM-STARTER-CR-NORMAL-0001_CLEAN_INDEPENDENT_SURFACE"')
    text = text.replace('n09["observed_result"] == "FAIL"', 'n09["observed_result"] == "INCONCLUSIVE_PROTOCOL_CONTAMINATION"')
    text = text.replace('n09["decision"] == "REWORK"', 'n09["decision"] == "EXPAND_EVIDENCE"')
    text = text.replace('truth["starter_runtime_fails"] == 1', 'truth["starter_runtime_fails"] == 0')
    text = text.replace('truth["starter_runtime_inconclusive"] == 0', 'truth["starter_runtime_inconclusive"] == 1')
    path.write_text(text, encoding="utf-8")


def patch_launch_checkpoint_validator() -> None:
    path = ROOT / "tools" / "validate_starter_launch_checkpoint_v1.py"
    text = path.read_text(encoding="utf-8")
    replacements = {
        'ONE_RUNTIME_OBSERVATION_REVIEWED_FAIL_REWORK_REQUIRED': 'ONE_RUNTIME_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED',
        'OBSERVED_ONE_FAIL_REWORK_REQUIRED': 'OBSERVED_ONE_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED',
        'ONE_OBSERVATION_REVIEWED_FAIL': 'ONE_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION',
        'CREATE_NEW_SUCCESSOR_VERSION_AND_RETEST_ONLY_AFTER_FRESH_AUTHORIZATION': 'RETEST_SAME_FROZEN_CASE_ON_CLEAN_INDEPENDENT_SURFACE_ONLY_AFTER_FRESH_AUTHORIZATION',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace('starter_sku_workflow_runtime_fails"] == 1', 'starter_sku_workflow_runtime_fails"] == 0')
    text = text.replace('starter_sku_workflow_runtime_inconclusive"] == 0', 'starter_sku_workflow_runtime_inconclusive"] == 1')
    text = text.replace('runtime_evidence"]["fails"] == 1', 'runtime_evidence"]["fails"] == 0')
    text = text.replace('runtime_evidence"]["inconclusive"] == 0', 'runtime_evidence"]["inconclusive"] == 1')
    path.write_text(text, encoding="utf-8")


def patch_workflow_summary() -> None:
    path = ROOT / ".github" / "workflows" / "validate-starter-release-gate-v1.yml"
    text = path.read_text(encoding="utf-8")
    text = text.replace('| Starter-specific canaries | 4 PREPARED / 0 ARMED / 0 RUN |', '| Starter-specific canaries | 4 PREPARED / 0 ARMED / 1 OBSERVATION |')
    text = text.replace('| Starter SKU workflow observations | 0 |', '| Starter SKU workflow observations | 1 INCONCLUSIVE (PROTOCOL CONTAMINATION) |')
    text = text.replace('| Public copy evidence audit | PASS_CURRENT_EVIDENCE_BOUNDARY |', '| Public copy evidence audit | STALE / REAUDIT REQUIRED |')
    path.write_text(text, encoding="utf-8")


def main() -> int:
    preserve_source_artifacts()
    write_correction_receipts()
    patch_trust_context()
    patch_release_gate()
    patch_release_dag()
    patch_release_gate_validator()
    patch_dag_validator()
    patch_launch_checkpoint_validator()
    patch_workflow_summary()
    print("starter runtime contamination correction staged")
    print("effective_result=INCONCLUSIVE_PROTOCOL_CONTAMINATION")
    print("passes=0 fails=0 inconclusive=1")
    print("same_candidate_retest=true successor_required=false armed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
