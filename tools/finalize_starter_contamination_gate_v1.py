#!/usr/bin/env python3
"""Finalize release-gate fields invalidated by the contamination correction.

No model/provider execution. This removes the stale mandatory-successor route
created by the historical FAIL classification and restores the same frozen
candidate as the next eligible experiment, still disarmed.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "commercial/STARTER_RELEASE_GATE_V1.json"


def main() -> int:
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    spend = gate["next_model_spend_gate"]
    spend.update({
        "authorized_now": False,
        "reason": "The only Starter runtime observation is protocol-contaminated and supports neither PASS nor FAIL. A clean retest of the same frozen candidate requires fresh explicit authorization.",
        "preferred_first_case_when_reopened": "PM-STARTER-CR-NORMAL-0001",
        "same_frozen_candidate": True,
        "successor_required_before_retest": False,
        "clean_independent_surface_required": True,
        "fresh_explicit_authorization_required": True,
        "maximum_submissions_before_human_review": 1,
        "automatic_wave": False,
        "automatic_retries": 0,
        "automatic_second_case": False,
    })
    GATE.write_text(json.dumps(gate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("starter next model gate normalized")
    print("same_frozen_candidate=true successor_required=false clean_surface=true armed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
