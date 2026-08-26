from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from mk1_behavioral_runner import REAL_EXECUTION_MODES, load


def promote_tested(artifact: dict, receipt: dict) -> dict:
    if artifact.get("state") != "VALID":
        raise ValueError(f"Only VALID artifacts may enter F4 promotion; got {artifact.get('state')!r}")
    if receipt.get("phase") != "F4":
        raise ValueError("Receipt is not an F4 behavioral receipt")
    if receipt.get("artifact_id") != artifact.get("id"):
        raise ValueError("Receipt artifact_id does not match source artifact")
    if receipt.get("artifact_version") != artifact.get("version"):
        raise ValueError("Receipt artifact_version does not match source artifact")
    if receipt.get("execution_mode") not in REAL_EXECUTION_MODES:
        raise ValueError("Synthetic/non-real F4 receipts cannot promote an artifact")
    if receipt.get("status") != "BEHAVIORAL_PASS":
        raise ValueError(f"F4 receipt status must be BEHAVIORAL_PASS; got {receipt.get('status')!r}")
    if receipt.get("eligible_for_tested") is not True:
        raise ValueError("F4 receipt is not eligible_for_tested")
    if receipt.get("blocking_failures"):
        raise ValueError("F4 receipt contains blocking failures")
    if receipt.get("unresolved_blocking_human_checks") not in (0, None):
        raise ValueError("F4 receipt has unresolved blocking human checks")
    if not receipt.get("receipt_id"):
        raise ValueError("F4 receipt_id is required")
    if not receipt.get("fixture_set_id"):
        raise ValueError("F4 fixture_set_id is required")

    runtime = receipt.get("runtime") or {}
    missing_runtime = [key for key in ("provider", "model", "run_at") if not runtime.get(key)]
    if missing_runtime:
        raise ValueError(f"F4 receipt missing runtime identity: {missing_runtime}")

    promoted = copy.deepcopy(artifact)
    promoted["state"] = "TESTED"
    claims = list(promoted.get("claims") or [])
    for claim in ("engineered", "tested"):
        if claim not in claims:
            claims.append(claim)
    promoted["claims"] = claims

    evaluation = promoted["evaluation"]
    evaluation["fixture_set_id"] = receipt["fixture_set_id"]
    evaluation["receipt_id"] = receipt["receipt_id"]
    evaluation["blocking_failures"] = list(receipt.get("blocking_failures") or [])
    evaluation["baseline_id"] = None
    evaluation["rubric_score"] = None

    fixtures = promoted["provenance"].setdefault("fixtures", [])
    if receipt["fixture_set_id"] not in fixtures:
        fixtures.append(receipt["fixture_set_id"])

    promoted["updated_at"] = runtime["run_at"]
    return promoted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    artifact = load(Path(args.artifact))
    receipt = load(Path(args.receipt))
    promoted = promote_tested(artifact, receipt)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(promoted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(promoted, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
