#!/usr/bin/env python3
"""Prepare PCP-04 baseline work orders from frozen prompt inventory and fixtures.

This script does not call a model. It binds exact prompt bytes to exact fixture
inputs and emits execution work orders that a real runtime lane may consume.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "certification" / "inventory" / "product-prompt-inventory.v1.json"
MATRIX = ROOT / "certification" / "fixtures" / "pcp-03-test-matrix.v1.json"
CASES = ROOT / "certification" / "fixtures" / "pcp-04-family-cases.v1.json"

EXPECTED_CLASSES = [
    "NORMAL", "MINIMAL", "MISSING_REQUIRED", "AMBIGUOUS", "CONTRADICTORY",
    "NOISY", "ADVERSARIAL_OVERRIDE", "EVIDENCE_DISCIPLINE",
    "OUTPUT_CONTRACT", "REPEATABILITY",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def slug(value: str) -> str:
    return value.upper().replace("PQ-PROMPT-", "P").replace("_", "-")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "pcp04-work-orders")
    args = parser.parse_args()

    inventory = read_json(INVENTORY)
    matrix = read_json(MATRIX)
    fixtures = read_json(CASES)

    if matrix.get("matrix_id") != "PQ-PCP-03-MATRIX-0001":
        raise SystemExit("unexpected PCP-03 matrix id")
    if fixtures.get("fixture_set_id") != "PQ-PCP-04-FIXTURES-0001":
        raise SystemExit("unexpected PCP-04 fixture set id")
    if fixtures.get("state") != "FROZEN_INPUTS_UNEXECUTED":
        raise SystemExit("PCP-04 fixtures must remain frozen and unexecuted")

    inventory_prompts = {row["prompt_id"]: row for row in inventory["prompts"]}
    matrix_prompts = {row["prompt_id"]: row for row in matrix["prompts"]}
    reuse = fixtures["reuse_contract"]
    family_rows = {row["family_id"]: row for row in fixtures["families"]}

    if set(inventory_prompts) != set(matrix_prompts) or set(inventory_prompts) != set(reuse):
        raise SystemExit("inventory, matrix, and fixture reuse prompt sets differ")

    if args.output.exists():
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)

    work_orders: list[dict] = []
    prompt_summaries: list[dict] = []
    required_execution_count = 0

    for prompt_id in sorted(inventory_prompts):
        inv = inventory_prompts[prompt_id]
        matrix_row = matrix_prompts[prompt_id]
        family_id = reuse[prompt_id]
        if family_id != inv["family_id"]:
            raise SystemExit(f"family mismatch for {prompt_id}: {family_id} != {inv['family_id']}")

        source_path = ROOT / inv["source"]["path"]
        source_bytes = source_path.read_bytes()
        observed_prompt_sha = sha256_bytes(source_bytes)
        expected_prompt_sha = inv["source"]["sha256"]
        if observed_prompt_sha != expected_prompt_sha:
            raise SystemExit(
                f"frozen prompt byte drift for {prompt_id}: {observed_prompt_sha} != {expected_prompt_sha}"
            )

        family_cases = family_rows[family_id]["cases"]
        by_class = {case["class"]: case for case in family_cases}
        required_classes = matrix_row["required_cases"]
        if required_classes != EXPECTED_CLASSES:
            raise SystemExit(f"unexpected class contract for {prompt_id}: {required_classes}")
        if set(by_class) != set(EXPECTED_CLASSES) or len(family_cases) != 10:
            raise SystemExit(f"family fixture coverage incomplete for {family_id}")

        prompt_dir = args.output / prompt_id
        prompt_dir.mkdir()
        (prompt_dir / "prompt.txt").write_bytes(source_bytes)
        prompt_required_executions = 0

        for case_class in EXPECTED_CLASSES:
            case = by_class[case_class]
            input_text = case["input"].rstrip() + "\n"
            input_bytes = input_text.encode("utf-8")
            case_id = case["case_id"]
            required_repetitions = 3 if case_class == "REPEATABILITY" else 1
            prompt_required_executions += required_repetitions
            required_execution_count += required_repetitions
            work_order_id = f"PQ-PCP04-WO-{slug(prompt_id)}-{case_id}"
            order = {
                "schema": "prompt-quarry-pcp04-work-order-v1",
                "work_order_id": work_order_id,
                "state": "READY_FOR_REAL_EXECUTION",
                "prompt_id": prompt_id,
                "family_id": family_id,
                "prompt": {
                    "source_path": inv["source"]["path"],
                    "sha256": observed_prompt_sha,
                    "frozen_baseline": True,
                },
                "fixture": {
                    "fixture_set_id": fixtures["fixture_set_id"],
                    "case_id": case_id,
                    "case_class": case_class,
                    "input_sha256": sha256_bytes(input_bytes),
                    "assertions": case["assertions"],
                    "required_repetitions": required_repetitions,
                },
                "runtime_contract": {
                    "real_runtime_required": True,
                    "fresh_independent_run": True,
                    "synthetic_allowed_for_promotion": False,
                    "runtime_identity_must_be_observed": True,
                    "full_raw_output_must_be_preserved": True,
                    "repeatability_runs_must_have_distinct_execution_ids": case_class == "REPEATABILITY",
                },
                "evaluation_contract": {
                    "blocking_dimensions": matrix["blocking_dimensions"],
                    "matrix_special_assertions": matrix_row["special_assertions"],
                    "fixture_assertions": case["assertions"],
                    "unresolved_blocking_human_check_is_fail": True,
                },
            }

            case_dir = prompt_dir / case_id
            case_dir.mkdir()
            (case_dir / "input.txt").write_bytes(input_bytes)
            (case_dir / "work-order.json").write_text(
                json.dumps(order, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            receipt_template = {
                "schema": "prompt-quarry-pcp04-execution-receipt-v1",
                "receipt_id": None,
                "work_order_id": work_order_id,
                "prompt_id": prompt_id,
                "prompt_sha256": observed_prompt_sha,
                "fixture_set_id": fixtures["fixture_set_id"],
                "case_id": case_id,
                "case_class": case_class,
                "repetition_index": None,
                "runtime": None,
                "execution": None,
                "raw_output": None,
                "evaluation": None,
                "promotion": {"case_pass": False, "eligible_for_prompt_tested": False},
                "template_only": True,
            }
            (case_dir / "receipt.template.json").write_text(
                json.dumps(receipt_template, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            work_orders.append(order)

        prompt_summaries.append({
            "prompt_id": prompt_id,
            "family_id": family_id,
            "prompt_sha256": observed_prompt_sha,
            "case_count": 10,
            "required_execution_count": prompt_required_executions,
        })

    if len(work_orders) != 70:
        raise SystemExit(f"expected 70 work orders, got {len(work_orders)}")
    if required_execution_count != 84:
        raise SystemExit(f"expected 84 required executions, got {required_execution_count}")

    jsonl = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in work_orders)
    (args.output / "work-orders.jsonl").write_text(jsonl, encoding="utf-8")
    manifest = {
        "schema": "prompt-quarry-pcp04-work-order-manifest-v1",
        "manifest_id": "PQ-PCP04-WORK-ORDERS-0001",
        "state": "READY_FOR_REAL_EXECUTION",
        "matrix_id": matrix["matrix_id"],
        "fixture_set_id": fixtures["fixture_set_id"],
        "inventory_id": inventory["inventory_id"],
        "prompt_count": len(prompt_summaries),
        "work_order_count": len(work_orders),
        "required_execution_count": required_execution_count,
        "repeatability_policy": {
            "case_class": "REPEATABILITY",
            "independent_runs_per_prompt": 3,
            "distinct_execution_ids_required": True
        },
        "prompt_summaries": prompt_summaries,
        "work_orders_jsonl_sha256": sha256_bytes(jsonl.encode("utf-8")),
        "behavioral_claim": "NONE",
        "F4_TESTED": False,
        "next_gate": "Execute 84 real observations across the 70 work orders, including three independent runs for every REPEATABILITY case, then persist schema-valid receipts with verbatim raw outputs.",
    }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
