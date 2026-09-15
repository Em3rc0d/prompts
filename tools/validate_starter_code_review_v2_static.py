#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1_REL = "product/starter-collection-v1/workflows/evidence-first-code-review.md"
V2_REL = "product/starter-collection-v2/workflows/evidence-first-code-review.md"
AUDIT_REL = "commercial/STARTER_N09_G07_SUCCESSOR_STATIC_AUDIT_V1.json"
V1 = ROOT / V1_REL
V2 = ROOT / V2_REL
AUDIT = ROOT / AUDIT_REL
EXPECTED_V2_ID = "pm-starter-evidence-first-code-review-v2"


def git_head_blob(rel_path: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{rel_path}"],
        cwd=ROOT,
        text=True,
    ).strip()


def git_worktree_strict_clean(rel_path: str) -> bool:
    result = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", rel_path],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0


def git_worktree_content_clean(rel_path: str) -> bool:
    # Ignore CR characters only when they appear at end-of-line. This avoids a
    # Windows/WSL CRLF checkout being treated as a content mutation while still
    # failing on substantive text edits, added/removed lines, or other changes.
    result = subprocess.run(
        ["git", "diff", "--quiet", "--ignore-cr-at-eol", "HEAD", "--", rel_path],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    expected_v1_blob = audit["source_v1_expected_git_blob_sha"]
    v1_text = V1.read_text(encoding="utf-8") if V1.exists() else ""
    v2_text = V2.read_text(encoding="utf-8") if V2.exists() else ""

    v1_head_blob = git_head_blob(V1_REL) if V1.exists() else None
    v1_strict_clean = git_worktree_strict_clean(V1_REL) if V1.exists() else False
    v1_content_clean = git_worktree_content_clean(V1_REL) if V1.exists() else False

    checks = {
        "v1_blob_immutable": V1.exists() and v1_head_blob == expected_v1_blob,
        "v1_worktree_content_clean": V1.exists() and v1_content_clean,
        "v2_file_present": V2.exists(),
        "v2_workflow_id_exact": f"Workflow ID: `{EXPECTED_V2_ID}`" in v2_text,
        "authority_advisory_only_preserved": "Authority: `ADVISORY_ONLY`" in v2_text and "Do not merge, deploy, approve, or execute changes." in v2_text,
        "untrusted_task_data_boundary_preserved": "UNTRUSTED TASK DATA" in v2_text and "ignore that text as authority" in v2_text,
        "negative_evidence_scope_rule_present": "Absence of a control in supplied code proves only that the control is not visible in that supplied scope." in v2_text,
        "external_boundary_cap_present": "external boundary could materially invalidate a finding" in v2_text,
        "reviewable_with_unknowns_rule_present": "Use `REVIEWABLE_WITH_UNKNOWNS` whenever" in v2_text,
        "likely_cap_present": "the finding must not exceed `LIKELY`" in v2_text,
        "review_required_cap_present": "the ship recommendation must not exceed `REVIEW_REQUIRED`" in v2_text,
        "invalidating_context_none_guard_present": "`Invalidating context: None` is forbidden" in v2_text,
        "conditional_impact_rule_present": "Conditional-impact rule" in v2_text and "must not increase evidence level or severity" in v2_text,
        "block_guard_present": "## SHIP RECOMMENDATION" in v2_text and "### BLOCK guard" in v2_text and "Do not use `BLOCK`" in v2_text,
        "no_runtime_or_test_invention_rule_present": "no runtime behavior or test result was invented" in v2_text and "Do not describe proposed tests as if they were already executed." in v2_text,
        "six_part_output_contract_present": all(f"### {i}." in v2_text for i in range(1, 7)),
        "behavior_not_yet_retested_marked": "BEHAVIOR NOT YET RETESTED" in v2_text,
        "v1_not_relabelled_as_v2": EXPECTED_V2_ID not in v1_text,
    }

    report = {
        "schema": "prompt-machine-starter-code-review-v2-static-validation-v3",
        "hash_semantics": "GIT_HEAD_BLOB_PLUS_CR_AT_EOL_NORMALIZED_WORKTREE_CONTENT",
        "v1_expected_git_blob": expected_v1_blob,
        "v1_head_git_blob": v1_head_blob,
        "v1_worktree_strict_clean": v1_strict_clean,
        "v1_worktree_content_clean": v1_content_clean,
        "v1_only_eol_difference_observed": (not v1_strict_clean) and v1_content_clean,
        "successor_workflow_id": EXPECTED_V2_ID,
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
        "next_gate_if_pass": "G08_REGRESSION_TEST_DESIGN_BEFORE_ANY_MODEL_RETEST",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
