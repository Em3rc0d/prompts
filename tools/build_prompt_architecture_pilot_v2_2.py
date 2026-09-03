from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_prompt_architecture_pilot_v2_1 import build_records as build_v21_records

PILOT_VERSION = "2.2.0"
LINEAGE = "successor-to-architecture-pilot-v2.1-after-static-audit-v2.1"


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def transform_body(mode: str, body: str) -> str:
    body = body.replace(
        "# Prompt Machine Architecture Blueprint v2.1 —",
        "# Prompt Machine Architecture Blueprint v2.2 —",
        1,
    )
    body = body.replace(
        "Choose the weakest state that accurately reflects the input/evidence condition. Never strengthen a state merely to make the answer appear decisive.",
        "Choose the state whose declared semantic condition is actually satisfied. When more than one condition appears applicable, choose the state that does not overstate execution, evidence, or completion.",
    )
    body = body.replace(
        "If responsible execution is impossible, use the mode-specific weakest state, do not execute or imply completion of the blocked/unsupported portion, preserve only safe partial evidence that does not imply task completion, and request the smallest additional information set capable of changing the state.",
        "If responsible execution is impossible, choose the mode-specific state whose declared condition actually applies, do not execute or imply completion of the blocked/unsupported portion, preserve only safe partial evidence that does not imply task completion, and request the smallest additional information set capable of changing the state.",
    )

    if mode == "generation":
        body = body.replace(
            "Shortlist and trade-offs when one exists; NONE when HOLD or NO_VALID_CANDIDATE makes a shortlist/winner unjustified.",
            "Viable shortlist and trade-offs. Under HOLD, return the tied viable shortlist but set recommended winner to NONE. Under NO_VALID_CANDIDATE, shortlist = NONE and explain the established hard-constraint conflicts.",
        )

    if mode == "simulation":
        anchor = (
            "5. For BATCH_DEBRIEF mode, evaluate a supplied transcript or explicitly generated practice transcript according to the configured task; mark generated turns as simulated."
        )
        replacement = anchor + (
            "\n6. Generated turns may be evaluated as simulated scenario/dialogue output, but they are never evidence of the user's ability or performance unless actual user turns are supplied."
            "\n7. Do not reveal a hidden ideal answer during interactive practice unless coaching mode explicitly permits it."
            "\n8. Debrief only against the declared rubric and observable simulation turns, then give targeted next-practice actions."
        )
        old_tail = (
            anchor
            + "\n6. Do not reveal a hidden ideal answer during interactive practice unless coaching mode explicitly permits it."
            + "\n7. Debrief only against the declared rubric and observable simulation turns, then give targeted next-practice actions."
        )
        if old_tail not in body:
            raise ValueError("Simulation process anchor changed; refusing silent transform")
        body = body.replace(old_tail, replacement)

    return body


def build_records() -> list[dict]:
    records = []
    for source in build_v21_records():
        mode = source["mode"]
        body = transform_body(mode, source["prompt_body"])
        records.append(
            {
                "schema": "prompt-machine-architecture-blueprint-v2.2",
                "pilot_version": PILOT_VERSION,
                "lineage": LINEAGE,
                "id": f"pm_architecture_{mode}_v2_2",
                "mode": mode,
                "state": "STATIC_REVIEW_REQUIRED",
                "content_origin": "repository-authored-quality-rework",
                "source_relation": "successor-to-v2.1-after-static-semantic-audit",
                "prompt_body": body,
                "prompt_sha256": sha256_text(body),
                "automatic_product_promotion": False,
                "behavioral_evidence": False,
                "ready_to_sell": False,
            }
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="quarry/etl/prompt-library-v1/architecture-pilot-v2.2")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    records = build_records()
    if len(records) != 9 or len({row["prompt_sha256"] for row in records}) != 9:
        raise SystemExit("Expected nine distinct v2.2 architecture blueprints")

    with (output_dir / "blueprints.jsonl").open("w", encoding="utf-8") as handle:
        for row in records:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    manifest = {
        "schema": "prompt-machine-architecture-pilot-manifest-v2.2",
        "pilot_version": PILOT_VERSION,
        "lineage": LINEAGE,
        "status": "STATIC_REVIEW_REQUIRED",
        "architecture_count": 9,
        "modes": [row["mode"] for row in records],
        "closed_static_audit_v2_1_findings": [
            "ARCH-V21-COMMON-001",
            "ARCH-V21-SIM-001",
            "ARCH-V21-GEN-001"
        ],
        "automatic_product_promotions": 0,
        "external_model_calls": 0,
        "behavioral_claims_created": 0,
        "ready_to_sell_claims_created": 0,
        "bulk_regeneration_allowed": False,
        "next_gate": "Final static semantic freeze audit before designing deterministic category binding and invocation rendering."
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
