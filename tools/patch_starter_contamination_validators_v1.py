#!/usr/bin/env python3
"""Migrate Starter validators to the effective INCONCLUSIVE contamination state.

Idempotent by design: validators may have been partially migrated by the main
correction script. This tool normalizes semantics without creating evidence.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalize(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        return text.replace(old, new)
    if new in text:
        return text
    raise AssertionError(f"validator shape drift: {label}")


def ensure_after(text: str, marker: str, addition: str, label: str) -> str:
    if addition in text:
        return text
    if marker not in text:
        raise AssertionError(f"validator marker missing: {label}")
    return text.replace(marker, marker + addition, 1)


def patch_release_gate() -> None:
    path = ROOT / "tools/validate_starter_release_gate_v1.py"
    text = path.read_text(encoding="utf-8")

    text = normalize(
        text,
        'assert gates["starter_specific_behavioral_evidence"] == "OPEN_ZERO_OBSERVATIONS"',
        'assert gates["starter_specific_behavioral_evidence"] == "OBSERVED_ONE_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"',
        "release gate behavioral evidence",
    )
    text = normalize(
        text,
        'assert gates["public_copy_evidence_audit"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"',
        'assert gates["public_copy_evidence_audit"] == "STALE_AFTER_RUNTIME_EVIDENCE_CHANGE"',
        "release gate public copy",
    )
    text = normalize(
        text,
        'print("starter_sku_runtime_observations=0")',
        'print("starter_sku_runtime_observations=1")',
        "release gate summary observations",
    )
    marker = '    print("starter_sku_runtime_observations=1")\n'
    text = ensure_after(
        text,
        marker,
        '    print("starter_sku_runtime_passes=0")\n    print("starter_sku_runtime_fails=0")\n    print("starter_sku_runtime_inconclusive=1")\n',
        "release gate runtime summary",
    )
    text = normalize(
        text,
        'print("public_copy_audit=PASS_CURRENT_EVIDENCE_BOUNDARY")',
        'print("public_copy_audit=STALE_AFTER_RUNTIME_EVIDENCE_CHANGE")',
        "release gate summary copy",
    )

    path.write_text(text, encoding="utf-8")


def patch_launch_checkpoint() -> None:
    path = ROOT / "tools/validate_starter_launch_checkpoint_v1.py"
    text = path.read_text(encoding="utf-8")

    text = normalize(
        text,
        'assert gate["checkpoint_revision"] == "first-starter-runtime-failure-20260904"',
        'assert gate["checkpoint_revision"] == "runtime-protocol-contamination-correction-20260904"',
        "checkpoint revision",
    )
    text = text.replace(
        "# Runtime failure must be recorded without promotion or automatic continuation.",
        "# Protocol-contaminated runtime is preserved but cannot count as workflow PASS or FAIL.",
    )
    text = text.replace(
        'assert gate["truth"]["starter_sku_workflow_runtime_fails"] == 1',
        'assert gate["truth"]["starter_sku_workflow_runtime_fails"] == 0',
    )
    fail_marker = '    assert gate["truth"]["starter_sku_workflow_runtime_fails"] == 0\n'
    text = ensure_after(
        text,
        fail_marker,
        '    assert gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 1\n',
        "checkpoint inconclusive count",
    )
    text = normalize(
        text,
        'assert gate["gates"]["starter_specific_behavioral_evidence"] == "OBSERVED_ONE_FAIL_REWORK_REQUIRED"',
        'assert gate["gates"]["starter_specific_behavioral_evidence"] == "OBSERVED_ONE_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"',
        "checkpoint behavioral state",
    )

    armed_marker = '    assert gate["starter_behavioral_canary_freeze"]["armed_cases"] == 0\n'
    correction_assertions = (
        '    assert gate["runtime_protocol_correction"]["effective_result"] == "INCONCLUSIVE_PROTOCOL_CONTAMINATION"\n'
        '    assert gate["runtime_protocol_correction"]["effective_decision"] == "EXPAND_EVIDENCE"\n'
        '    assert gate["runtime_protocol_correction"]["historical_fail_review_preserved"] is True\n'
        '    assert gate["runtime_protocol_correction"]["successor_required_before_clean_retest"] is False\n'
        '    assert gate["runtime_protocol_correction"]["same_frozen_candidate_retest_required"] is True\n'
        '    assert gate["runtime_protocol_correction"]["armed"] is False\n'
    )
    text = ensure_after(text, armed_marker, correction_assertions, "checkpoint correction assertions")

    text = text.replace('print("starter_runtime_fails=1")', 'print("starter_runtime_fails=0")')
    summary_marker = '    print("starter_runtime_fails=0")\n'
    text = ensure_after(
        text,
        summary_marker,
        '    print("starter_runtime_inconclusive=1")\n',
        "checkpoint summary inconclusive",
    )
    path.write_text(text, encoding="utf-8")


def patch_release_dag() -> None:
    path = ROOT / "tools/validate_starter_release_dag_v1.py"
    text = path.read_text(encoding="utf-8")

    text = text.replace(
        "# Current frontier preserves the reviewed runtime failure, required successor rework,\n    # stale public-copy audit, and independently disarmed provider lane.",
        "# Current frontier preserves the protocol-contaminated observation, clean retest requirement,\n    # stale public-copy audit, and independently disarmed provider lane.",
    )
    pairs = [
        ('assert n09["status"] == "OPEN_REQUIRES_SUCCESSOR_REWORK"', 'assert n09["status"] == "OPEN_REQUIRES_MODEL_AUTH"', "N09 status"),
        ('assert n09["observed_result"] == "FAIL"', 'assert n09["observed_result"] == "INCONCLUSIVE_PROTOCOL_CONTAMINATION"', "N09 result"),
        ('assert n09["decision"] == "REWORK"', 'assert n09["decision"] == "EXPAND_EVIDENCE"', "N09 decision"),
        ('assert len(n09["evidence"]) == 4', 'assert len(n09["evidence"]) == 6', "N09 evidence count"),
        ('assert n09["next_experiment"] == "NEW_SUCCESSOR_VERSION_THEN_PM-STARTER-CR-NORMAL-0001_RETEST"', 'assert n09["next_experiment"] == "RETEST_PM-STARTER-CR-NORMAL-0001_CLEAN_INDEPENDENT_SURFACE"', "N09 next experiment"),
        ('assert truth["starter_runtime_fails"] == gate["truth"]["starter_sku_workflow_runtime_fails"] == 1', 'assert truth["starter_runtime_fails"] == gate["truth"]["starter_sku_workflow_runtime_fails"] == 0', "DAG fails"),
        ('assert truth["starter_runtime_inconclusive"] == gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 0', 'assert truth["starter_runtime_inconclusive"] == gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 1', "DAG inconclusive"),
    ]
    for old, new, label in pairs:
        text = normalize(text, old, new, label)

    retry_marker = '    assert n09["automatic_retries"] == 0\n'
    text = ensure_after(
        text,
        retry_marker,
        '    assert n09["candidate_mutation_required"] is False\n    assert n09["fresh_authorization_required"] is True\n    assert n09["clean_independent_surface_required"] is True\n',
        "N09 clean retest invariants",
    )

    text = text.replace('print("starter_runtime_fails=1")', 'print("starter_runtime_fails=0")')
    dag_summary_marker = '    print("starter_runtime_fails=0")\n'
    text = ensure_after(
        text,
        dag_summary_marker,
        '    print("starter_runtime_inconclusive=1")\n',
        "DAG summary inconclusive",
    )
    text = text.replace('print("starter_runtime_decision=REWORK")', 'print("starter_runtime_decision=EXPAND_EVIDENCE")')
    path.write_text(text, encoding="utf-8")


def main() -> int:
    patch_release_gate()
    patch_launch_checkpoint()
    patch_release_dag()
    print("starter contamination validators normalized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
