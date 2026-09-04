#!/usr/bin/env python3
"""Patch validators after the append-only Starter contamination correction.

This helper exists only to migrate assertions that encoded the previous
zero-observation / FAIL-REWORK state. It creates no behavioral evidence.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise AssertionError(f"missing expected legacy assertion: {label}: {old}")
    return text.replace(old, new)


def patch_release_gate() -> None:
    path = ROOT / "tools" / "validate_starter_release_gate_v1.py"
    text = path.read_text(encoding="utf-8")

    replacements = [
        ('assert gates["starter_specific_behavioral_evidence"] == "OPEN_ZERO_OBSERVATIONS"',
         'assert gates["starter_specific_behavioral_evidence"] == "OBSERVED_ONE_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"',
         'release gate behavioral evidence'),
        ('assert gates["public_copy_evidence_audit"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"',
         'assert gates["public_copy_evidence_audit"] == "STALE_AFTER_RUNTIME_EVIDENCE_CHANGE"',
         'release gate copy state'),
        ('print("starter_sku_runtime_observations=0")',
         'print("starter_sku_runtime_observations=1")\n    print("starter_sku_runtime_passes=0")\n    print("starter_sku_runtime_fails=0")\n    print("starter_sku_runtime_inconclusive=1")',
         'release gate summary observation'),
        ('print("public_copy_audit=PASS_CURRENT_EVIDENCE_BOUNDARY")',
         'print("public_copy_audit=STALE_AFTER_RUNTIME_EVIDENCE_CHANGE")',
         'release gate summary copy'),
    ]
    for old, new, label in replacements:
        text = replace_required(text, old, new, label)

    # The customer page is intentionally still stale until the separate public-copy
    # re-audit/fix transaction. The release-gate validator must not treat stale copy
    # as evidence of the corrected runtime count.
    stale_page_assert = '    assert "0</strong><span>Starter runtime observations" in page\n'
    if stale_page_assert in text:
        text = text.replace(
            stale_page_assert,
            '    assert "0</strong><span>Starter runtime observations" in page, "public copy drift changed before governed re-audit"\n'
        )

    path.write_text(text, encoding="utf-8")


def patch_launch_checkpoint() -> None:
    path = ROOT / "tools" / "validate_starter_launch_checkpoint_v1.py"
    text = path.read_text(encoding="utf-8")
    replacements = [
        ('assert gate["checkpoint_revision"] == "first-starter-runtime-failure-20260904"',
         'assert gate["checkpoint_revision"] == "runtime-protocol-contamination-correction-20260904"',
         'checkpoint revision'),
        ('# Runtime failure must be recorded without promotion or automatic continuation.',
         '# Protocol-contaminated runtime must be preserved without being counted as workflow PASS or FAIL.',
         'runtime comment'),
        ('assert gate["truth"]["starter_sku_workflow_runtime_fails"] == 1',
         'assert gate["truth"]["starter_sku_workflow_runtime_fails"] == 0\n    assert gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 1',
         'checkpoint fail/inconclusive counts'),
        ('assert gate["gates"]["starter_specific_behavioral_evidence"] == "OBSERVED_ONE_FAIL_REWORK_REQUIRED"',
         'assert gate["gates"]["starter_specific_behavioral_evidence"] == "OBSERVED_ONE_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"',
         'checkpoint behavioral evidence'),
        ('print("starter_runtime_fails=1")',
         'print("starter_runtime_fails=0")\n    print("starter_runtime_inconclusive=1")',
         'checkpoint summary'),
    ]
    for old, new, label in replacements:
        text = replace_required(text, old, new, label)

    marker = '    assert gate["starter_behavioral_canary_freeze"]["armed_cases"] == 0\n'
    addition = (
        '    assert gate["runtime_protocol_correction"]["effective_result"] == "INCONCLUSIVE_PROTOCOL_CONTAMINATION"\n'
        '    assert gate["runtime_protocol_correction"]["effective_decision"] == "EXPAND_EVIDENCE"\n'
        '    assert gate["runtime_protocol_correction"]["historical_fail_review_preserved"] is True\n'
        '    assert gate["runtime_protocol_correction"]["successor_required_before_clean_retest"] is False\n'
        '    assert gate["runtime_protocol_correction"]["same_frozen_candidate_retest_required"] is True\n'
        '    assert gate["runtime_protocol_correction"]["armed"] is False\n'
    )
    if addition not in text:
        if marker not in text:
            raise AssertionError("missing launch checkpoint armed-case marker")
        text = text.replace(marker, marker + addition)

    path.write_text(text, encoding="utf-8")


def patch_release_dag() -> None:
    path = ROOT / "tools" / "validate_starter_release_dag_v1.py"
    text = path.read_text(encoding="utf-8")
    replacements = [
        ('# Current frontier preserves the reviewed runtime failure, required successor rework,\n    # stale public-copy audit, and independently disarmed provider lane.',
         '# Current frontier preserves the protocol-contaminated observation, clean retest requirement,\n    # stale public-copy audit, and independently disarmed provider lane.',
         'dag comment'),
        ('assert n09["status"] == "OPEN_REQUIRES_SUCCESSOR_REWORK"',
         'assert n09["status"] == "OPEN_REQUIRES_MODEL_AUTH"',
         'dag N09 status'),
        ('assert n09["observed_result"] == "FAIL"',
         'assert n09["observed_result"] == "INCONCLUSIVE_PROTOCOL_CONTAMINATION"',
         'dag observed result'),
        ('assert n09["decision"] == "REWORK"',
         'assert n09["decision"] == "EXPAND_EVIDENCE"',
         'dag decision'),
        ('assert len(n09["evidence"]) == 4',
         'assert len(n09["evidence"]) == 6',
         'dag evidence count'),
        ('assert n09["next_experiment"] == "NEW_SUCCESSOR_VERSION_THEN_PM-STARTER-CR-NORMAL-0001_RETEST"',
         'assert n09["next_experiment"] == "RETEST_PM-STARTER-CR-NORMAL-0001_CLEAN_INDEPENDENT_SURFACE"',
         'dag next experiment'),
        ('assert truth["starter_runtime_fails"] == gate["truth"]["starter_sku_workflow_runtime_fails"] == 1',
         'assert truth["starter_runtime_fails"] == gate["truth"]["starter_sku_workflow_runtime_fails"] == 0',
         'dag fail count'),
        ('assert truth["starter_runtime_inconclusive"] == gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 0',
         'assert truth["starter_runtime_inconclusive"] == gate["truth"]["starter_sku_workflow_runtime_inconclusive"] == 1',
         'dag inconclusive count'),
        ('print("starter_runtime_fails=1")',
         'print("starter_runtime_fails=0")\n    print("starter_runtime_inconclusive=1")',
         'dag summary fail'),
        ('print("starter_runtime_decision=REWORK")',
         'print("starter_runtime_decision=EXPAND_EVIDENCE")',
         'dag summary decision'),
    ]
    for old, new, label in replacements:
        # Some of these may already have been patched by the main migration.
        if old in text:
            text = text.replace(old, new)
        elif new not in text:
            raise AssertionError(f"missing both legacy and corrected DAG assertion: {label}")

    marker = '    assert n09["automatic_retries"] == 0\n'
    addition = (
        '    assert n09["candidate_mutation_required"] is False\n'
        '    assert n09["fresh_authorization_required"] is True\n'
        '    assert n09["clean_independent_surface_required"] is True\n'
    )
    if addition not in text:
        if marker not in text:
            raise AssertionError("missing DAG retry marker")
        text = text.replace(marker, marker + addition)

    path.write_text(text, encoding="utf-8")


def main() -> int:
    patch_release_gate()
    patch_launch_checkpoint()
    patch_release_dag()
    print("starter contamination validators patched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
