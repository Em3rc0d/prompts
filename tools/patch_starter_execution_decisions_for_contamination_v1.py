#!/usr/bin/env python3
"""Migrate execution-decision validation to corrected effective runtime semantics.

The original FAIL/REWORK review and failure record remain required historical
artifacts. The effective workflow classification is INCONCLUSIVE because the
runtime surface was protocol-contaminated.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_starter_execution_decisions_v1.py"


def main() -> int:
    text = PATH.read_text(encoding="utf-8")

    text = text.replace(
        'assert trust["current_evidence_state"] == "ONE_RUNTIME_OBSERVATION_REVIEWED_FAIL_REWORK_REQUIRED"',
        'assert trust["current_evidence_state"] == "ONE_RUNTIME_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED"',
    )
    text = text.replace(
        'assert trust["runtime_evidence"]["fails"] == 1',
        'assert trust["runtime_evidence"]["fails"] == 0',
    )
    text = text.replace(
        'assert trust["runtime_evidence"]["inconclusive"] == 0',
        'assert trust["runtime_evidence"]["inconclusive"] == 1',
    )

    # Historical review/failure assertions intentionally remain FAIL/REWORK and
    # successor_requires_new_version=true because those files are immutable
    # historical artifacts. Add the effective correction overlay after them.
    marker = '    assert runtime_failure["observed_workflow_version_mutated"] is False\n'
    addition = '''    correction_ref = trust["runtime_evidence"]["review_corrections"][0]\n    assert correction_ref["historical_review_id"] == human_review["review_id"]\n    assert correction_ref["historical_result"] == "FAIL"\n    assert correction_ref["effective_result"] == "INCONCLUSIVE"\n    assert correction_ref["effective_decision"] == "EXPAND_EVIDENCE"\n    assert correction_ref["reason"] == "PROTOCOL_CONTAMINATION"\n    correction_path = ROOT / correction_ref["path"]\n    correction = load(correction_path)\n    assert correction["correction_class"] == "PROTOCOL_CONTAMINATION"\n    assert correction["historical_classification"]["review_result"] == "FAIL"\n    assert correction["historical_classification"]["decision"] == "REWORK"\n    assert correction["historical_classification"]["status"] == "PRESERVED_AS_HISTORICAL_MISCLASSIFICATION"\n    assert correction["effective_classification"]["review_result"] == "INCONCLUSIVE"\n    assert correction["effective_classification"]["decision"] == "EXPAND_EVIDENCE"\n    assert correction["effective_classification"]["workflow_pass_count"] == 0\n    assert correction["effective_classification"]["workflow_fail_count"] == 0\n    assert correction["effective_classification"]["workflow_inconclusive_count"] == 1\n    assert correction["workflow_mutation"]["observed_candidate_mutated"] is False\n    assert correction["workflow_mutation"]["successor_required_by_this_observation"] is False\n    assert correction["next_evidence"]["candidate"] == "SAME_FROZEN_1.0.0_CANDIDATE"\n    assert correction["next_evidence"]["requires_clean_independent_surface"] is True\n    assert correction["next_evidence"]["requires_fresh_explicit_authorization"] is True\n    assert correction["next_evidence"]["automatic_retries"] == 0\n    historical_failure = next(row for row in trust["historical_failures"] if row["failure_id"] == runtime_failure["failure_id"])\n    assert historical_failure["historical_classification_artifact"] is True\n    assert historical_failure["effective_workflow_failure"] is False\n    assert historical_failure["superseded_by_correction"] == correction_ref["path"]\n'''
    if addition not in text:
        if marker not in text:
            raise AssertionError("execution-decision validator marker drift")
        text = text.replace(marker, marker + addition, 1)

    text = text.replace('print("starter_runtime_fails=1")', 'print("starter_runtime_fails=0")')
    summary_marker = '    print("starter_runtime_fails=0")\n'
    summary_add = '    print("starter_runtime_inconclusive=1")\n'
    if summary_add not in text:
        if summary_marker not in text:
            raise AssertionError("execution-decision summary marker drift")
        text = text.replace(summary_marker, summary_marker + summary_add, 1)
    text = text.replace('print("starter_runtime_decision=REWORK")', 'print("starter_runtime_decision=EXPAND_EVIDENCE")')

    required = [
        'ONE_RUNTIME_OBSERVATION_INCONCLUSIVE_PROTOCOL_CONTAMINATION_CLEAN_RETEST_REQUIRED',
        'assert trust["runtime_evidence"]["fails"] == 0',
        'assert trust["runtime_evidence"]["inconclusive"] == 1',
        'effective_workflow_failure"] is False',
    ]
    for value in required:
        assert value in text, value

    PATH.write_text(text, encoding="utf-8")
    print("starter execution-decision validator migrated to effective inconclusive semantics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
