from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_prompt_architecture_pilot_v2_2 import build_records as build_v22_records

PILOT_VERSION = "2.3.0"
LINEAGE = "successor-to-architecture-pilot-v2.2-after-final-freeze-audit"


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def transform_body(mode: str, body: str) -> str:
    body = body.replace(
        "# Prompt Machine Architecture Blueprint v2.2 —",
        "# Prompt Machine Architecture Blueprint v2.3 —",
        1,
    )

    state_anchor = (
        "STATE POLICY\n"
        "Choose the state whose declared semantic condition is actually satisfied. "
        "When more than one condition appears applicable, choose the state that does not overstate execution, evidence, or completion."
    )
    state_replacement = state_anchor + (
        "\nPREFLIGHT INVARIANT — If any configured minimum required input is absent or contradictory enough that its intended meaning cannot be established, choose BLOCKED and do not execute the domain procedure. The only exception is when this architecture explicitly defines an authorized acquisition/intake state for obtaining that input before domain execution."
    )
    if state_anchor not in body:
        raise ValueError(f"STATE POLICY anchor changed for {mode}; refusing silent transform")
    body = body.replace(state_anchor, state_replacement, 1)

    if mode == "generation":
        body = body.replace(
            "NO_VALID_CANDIDATE — candidates can be explored, but every candidate violates at least one established hard constraint.",
            "NO_VALID_CANDIDATE — none of the generated/evaluated candidates satisfies all established hard constraints. This state is scoped to the evaluated set and is not proof that no conceivable candidate exists unless the configured search space is explicitly exhaustive.",
        )
        body = body.replace(
            "Under NO_VALID_CANDIDATE, shortlist = NONE and explain the established hard-constraint conflicts.",
            "Under NO_VALID_CANDIDATE, shortlist = NONE for the evaluated set, explain the established hard-constraint conflicts, and state whether the configured search space was exhaustive.",
        )

    if mode == "learning":
        objective_rule = (
            "OBJECTIVE_MET — allowed only when observable assessment evidence tied to the declared learning objective satisfies the configured threshold. Self-declared understanding alone is insufficient unless self-report is explicitly the configured objective."
        )
        replacement = objective_rule + (
            " If no objective assessment threshold has been configured, OBJECTIVE_MET is forbidden; remain READY or IN_PROGRESS as appropriate and request/configure the threshold through the authorized workflow configuration surface."
        )
        if objective_rule not in body:
            raise ValueError("Learning OBJECTIVE_MET rule changed; refusing silent transform")
        body = body.replace(objective_rule, replacement, 1)

    return body


def build_records() -> list[dict]:
    records: list[dict] = []
    for source in build_v22_records():
        mode = source["mode"]
        body = transform_body(mode, source["prompt_body"])
        records.append(
            {
                "schema": "prompt-machine-architecture-blueprint-v2.3",
                "pilot_version": PILOT_VERSION,
                "lineage": LINEAGE,
                "id": f"pm_architecture_{mode}_v2_3",
                "mode": mode,
                "state": "STATIC_REVIEW_REQUIRED",
                "content_origin": "repository-authored-quality-rework",
                "source_relation": "successor-to-v2.2-after-final-static-freeze-audit",
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
    parser.add_argument("--output-dir", default="quarry/etl/prompt-library-v1/architecture-pilot-v2.3")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    records = build_records()
    if len(records) != 9 or len({row["prompt_sha256"] for row in records}) != 9:
        raise SystemExit("Expected nine distinct v2.3 architecture blueprints")

    with (output_dir / "blueprints.jsonl").open("w", encoding="utf-8") as handle:
        for row in records:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    manifest = {
        "schema": "prompt-machine-architecture-pilot-manifest-v2.3",
        "pilot_version": PILOT_VERSION,
        "lineage": LINEAGE,
        "status": "STATIC_REVIEW_REQUIRED",
        "architecture_count": 9,
        "modes": [row["mode"] for row in records],
        "closed_static_freeze_findings": [
            "ARCH-V22-COMMON-001",
            "ARCH-V22-GEN-001",
            "ARCH-V22-LEARN-001"
        ],
        "automatic_product_promotions": 0,
        "external_model_calls": 0,
        "behavioral_claims_created": 0,
        "ready_to_sell_claims_created": 0,
        "bulk_regeneration_allowed": False,
        "next_gate": "Final static semantic freeze audit. If PASS, freeze architecture mothers and move only to deterministic binding/invocation design."
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
