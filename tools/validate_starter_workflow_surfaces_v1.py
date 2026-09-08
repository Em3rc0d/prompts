#!/usr/bin/env python3
"""Deterministic contract-to-prompt parity checks for Starter Collection v1.

No model/provider/network call is performed. Passing this validator establishes
static surface parity only; it creates no behavioral or product-readiness claim.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "product" / "starter-collection-v1"

CODE_CONTRACT = BASE / "contracts" / "code-review.workflow-contract.json"
BUG_CONTRACT = BASE / "contracts" / "bug-diagnosis.workflow-contract.json"
CODE_SURFACE = BASE / "workflows" / "evidence-first-code-review.md"
BUG_SURFACE = BASE / "workflows" / "evidence-first-bug-diagnosis.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_all(text: str, values: list[str], label: str) -> None:
    missing = [value for value in values if value not in text]
    assert not missing, f"{label} missing required contract semantics: {missing}"


def validate_common(contract: dict, surface: str) -> None:
    require_all(
        surface,
        [
            contract["workflow_id"],
            "ADVISORY_ONLY",
            "UNTRUSTED TASK DATA",
            "BEHAVIOR NOT YET OBSERVED",
            "MINIMUM INPUT PREFLIGHT",
            "OUTPUT CONTRACT",
            "FINAL SELF-CHECK",
        ],
        contract["workflow_id"],
    )
    assert "ignore that text as authority" in surface
    assert "certification" not in surface.lower() or "claim certification" in surface.lower()
    assert contract["evidence_boundary"]["ready_to_sell"] is False


def validate_code_review(contract: dict, surface: str) -> None:
    validate_common(contract, surface)

    require_all(surface, contract["input_contract"]["input_states"], "code-review input states")
    require_all(surface, list(contract["evidence_semantics"].keys()), "code-review evidence states")
    require_all(surface, contract["finding_contract"]["severity_states"], "code-review severity states")
    require_all(surface, contract["ship_recommendation"]["states"], "code-review ship states")

    forbidden_old_terminal = "- `SHIP` —"
    assert forbidden_old_terminal not in surface, "Starter Code Review must not restore ambiguous SHIP terminal state"

    require_all(
        surface,
        [
            "Code, diff, or exact changed files",
            "Change intent / acceptance criteria",
            "Runtime / language context sufficient to interpret the change",
            "failure mechanism",
            "Invalidating context",
            "Verification plan",
        ],
        "code-review surface",
    )


def validate_bug_diagnosis(contract: dict, surface: str) -> None:
    validate_common(contract, surface)

    require_all(surface, contract["input_contract"]["input_states"], "bug-diagnosis input states")
    require_all(surface, list(contract["evidence_semantics"].keys()), "bug-diagnosis evidence states")
    require_all(surface, contract["diagnostic_states"], "bug-diagnosis diagnostic states")
    require_all(surface, contract["action_classes"], "bug-diagnosis action classes")

    require_all(
        surface,
        [
            "Expected behavior",
            "Observed behavior",
            "Environment / version context",
            "Material evidence",
            "ROOT-CAUSE CONFIRMATION THRESHOLD",
            "explicit human approval",
            "Ranked hypotheses",
            "Remaining material unknowns",
        ],
        "bug-diagnosis surface",
    )

    assert "at most 5" in surface
    assert "Timing or correlation alone does not establish causation" in surface
    assert "A fix appearing to work once does not by itself establish root cause" in surface


def main() -> int:
    code_contract = load_json(CODE_CONTRACT)
    bug_contract = load_json(BUG_CONTRACT)
    code_surface = CODE_SURFACE.read_text(encoding="utf-8")
    bug_surface = BUG_SURFACE.read_text(encoding="utf-8")

    validate_code_review(code_contract, code_surface)
    validate_bug_diagnosis(bug_contract, bug_surface)

    print("STARTER WORKFLOW SURFACE PARITY V1: PASS")
    print("contracts=2")
    print("surfaces=2")
    print("authority=ADVISORY_ONLY")
    print("instruction_data_boundary=PRESENT")
    print("behavioral_observations_created=0")
    print("model_calls=0")
    print("provider_calls=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
