#!/usr/bin/env python3
"""Validate and aggregate real PCP-04 execution receipts.

A receipt is accepted only when it is schema-valid, bound to a frozen work order,
points to a verbatim raw output with a matching SHA-256, and its evaluation is
internally consistent. Prompt-level TESTED eligibility is computed here; an
individual receipt cannot grant it to itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "certification" / "specs" / "PCP04_EXECUTION_RECEIPT.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_key(receipt: dict) -> tuple[str, str, str]:
    r = receipt["runtime"]
    return (r["provider"].strip(), r["surface"].strip(), r["model_or_configuration"].strip())


def expected_assertions(work_order: dict) -> set[str]:
    c = work_order["evaluation_contract"]
    return set(c["matrix_special_assertions"]) | set(c["fixture_assertions"])


def receipt_case_pass(receipt: dict, required_assertions: set[str]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    evaluation = receipt["evaluation"]
    dims = evaluation["blocking_dimensions"]
    if any(value != "PASS" for value in dims.values()):
        errors.append("one or more blocking dimensions failed")

    observed = {row["assertion"]: row for row in evaluation["special_assertions"]}
    missing = sorted(required_assertions - set(observed))
    if missing:
        errors.append(f"missing required assertions: {missing}")
    failed_assertions = sorted(
        name for name, row in observed.items() if name in required_assertions and row["result"] != "PASS"
    )
    if failed_assertions:
        errors.append(f"required assertions failed: {failed_assertions}")
    if evaluation["unresolved_blocking_human_checks"] != 0:
        errors.append("unresolved blocking human checks remain")
    if evaluation["blocking_failures"]:
        errors.append("blocking_failures is non-empty")
    return (not errors, errors)


def resolve_repo_path(value: str) -> Path:
    path = (ROOT / value).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository root: {value}") from exc
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-orders", type=Path, required=True)
    parser.add_argument("--receipts", type=Path, required=True)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    schema = load(SCHEMA_PATH)
    manifest = load(args.work_orders / "manifest.json")
    orders = {
        row["work_order_id"]: row
        for row in (
            json.loads(line)
            for line in (args.work_orders / "work-orders.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    if len(orders) != 70 or manifest["work_order_count"] != 70:
        raise SystemExit("invalid work-order packet")
    if manifest["required_execution_count"] != 84:
        raise SystemExit("work-order packet does not enforce 84 required real executions")

    receipt_paths = sorted(args.receipts.rglob("*.receipt.json")) if args.receipts.exists() else []
    if not receipt_paths:
        report = {
            "schema": "prompt-quarry-pcp04-aggregate-v1",
            "status": "EXECUTION_NOT_STARTED",
            "receipt_count": 0,
            "required_execution_count": 84,
            "prompt_results": [],
            "F4_TESTED": False,
            "errors": [],
        }
        rendered = json.dumps(report, indent=2, sort_keys=True)
        print(rendered)
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(rendered + "\n", encoding="utf-8")
        return 1 if args.require_complete else 0

    global_errors: list[str] = []
    accepted: list[dict] = []
    receipt_ids: set[str] = set()
    execution_ids: set[str] = set()
    campaign_ids: set[str] = set()
    runtime_keys: set[tuple[str, str, str]] = set()
    seen_slots: set[tuple[str, int]] = set()

    for path in receipt_paths:
        try:
            receipt = load(path)
            jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(receipt)
        except Exception as exc:
            global_errors.append(f"{path}: schema/load error: {exc}")
            continue

        receipt_id = receipt["receipt_id"]
        execution_id = receipt["execution"]["execution_id"]
        if receipt_id in receipt_ids:
            global_errors.append(f"duplicate receipt_id: {receipt_id}")
            continue
        if execution_id in execution_ids:
            global_errors.append(f"duplicate execution_id: {execution_id}")
            continue
        receipt_ids.add(receipt_id)
        execution_ids.add(execution_id)
        campaign_ids.add(receipt["campaign_id"])
        runtime_keys.add(runtime_key(receipt))

        work_order = orders.get(receipt["work_order_id"])
        if not work_order:
            global_errors.append(f"{receipt_id}: unknown work_order_id")
            continue

        binding_checks = {
            "prompt_id": (receipt["prompt_id"], work_order["prompt_id"]),
            "prompt_sha256": (receipt["prompt_sha256"], work_order["prompt"]["sha256"]),
            "fixture_set_id": (receipt["fixture_set_id"], work_order["fixture"]["fixture_set_id"]),
            "case_id": (receipt["case_id"], work_order["fixture"]["case_id"]),
            "case_class": (receipt["case_class"], work_order["fixture"]["case_class"]),
        }
        mismatches = [key for key, pair in binding_checks.items() if pair[0] != pair[1]]
        if mismatches:
            global_errors.append(f"{receipt_id}: work-order binding mismatch: {mismatches}")
            continue

        required_repetitions = work_order["fixture"]["required_repetitions"]
        repetition_index = receipt["repetition_index"]
        if repetition_index > required_repetitions:
            global_errors.append(
                f"{receipt_id}: repetition {repetition_index} exceeds required {required_repetitions}"
            )
            continue
        slot = (receipt["work_order_id"], repetition_index)
        if slot in seen_slots:
            global_errors.append(f"duplicate work-order repetition slot: {slot}")
            continue
        seen_slots.add(slot)

        try:
            raw_path = resolve_repo_path(receipt["raw_output"]["path"])
        except ValueError as exc:
            global_errors.append(f"{receipt_id}: {exc}")
            continue
        if not raw_path.is_file():
            global_errors.append(f"{receipt_id}: raw output missing: {raw_path}")
            continue
        observed_output_sha = sha256(raw_path)
        if observed_output_sha != receipt["raw_output"]["sha256"]:
            global_errors.append(f"{receipt_id}: raw output SHA mismatch")
            continue

        required = expected_assertions(work_order)
        computed_pass, case_errors = receipt_case_pass(receipt, required)
        if receipt["promotion"]["case_pass"] != computed_pass:
            global_errors.append(
                f"{receipt_id}: declared case_pass={receipt['promotion']['case_pass']} but computed={computed_pass}"
            )
            continue
        if receipt["promotion"]["eligible_for_prompt_tested"]:
            global_errors.append(
                f"{receipt_id}: individual receipts may not self-declare prompt TESTED eligibility"
            )
            continue

        accepted.append({
            "path": str(path),
            "receipt": receipt,
            "work_order": work_order,
            "computed_case_pass": computed_pass,
            "case_errors": case_errors,
        })

    if len(campaign_ids) > 1:
        global_errors.append(f"multiple campaign ids in one aggregate: {sorted(campaign_ids)}")
    if len(runtime_keys) > 1:
        global_errors.append(f"multiple runtime identities in one campaign: {sorted(runtime_keys)}")

    by_prompt: dict[str, list[dict]] = defaultdict(list)
    for row in accepted:
        by_prompt[row["receipt"]["prompt_id"]].append(row)

    prompt_results: list[dict] = []
    all_prompt_ids = sorted({order["prompt_id"] for order in orders.values()})
    for prompt_id in all_prompt_ids:
        prompt_rows = by_prompt.get(prompt_id, [])
        prompt_orders = [o for o in orders.values() if o["prompt_id"] == prompt_id]
        required_slots = {
            (order["work_order_id"], repetition)
            for order in prompt_orders
            for repetition in range(1, order["fixture"]["required_repetitions"] + 1)
        }
        observed_slots = {
            (row["receipt"]["work_order_id"], row["receipt"]["repetition_index"])
            for row in prompt_rows
        }
        missing_slots = sorted(required_slots - observed_slots)
        failed_receipts = sorted(
            row["receipt"]["receipt_id"] for row in prompt_rows if not row["computed_case_pass"]
        )

        repeatability_groups: dict[str, list[dict]] = defaultdict(list)
        for row in prompt_rows:
            if row["receipt"]["case_class"] == "REPEATABILITY":
                repeatability_groups[row["receipt"]["work_order_id"]].append(row)
        repeatability_pass = True
        repeatability_detail: list[dict] = []
        for order in prompt_orders:
            if order["fixture"]["case_class"] != "REPEATABILITY":
                continue
            group = repeatability_groups.get(order["work_order_id"], [])
            signatures = [r["receipt"]["evaluation"]["outcome_signature"] for r in group]
            distinct_execs = {r["receipt"]["execution"]["execution_id"] for r in group}
            group_pass = (
                len(group) == 3
                and len(distinct_execs) == 3
                and len(set(signatures)) == 1
                and all(r["computed_case_pass"] for r in group)
            )
            repeatability_pass = repeatability_pass and group_pass
            repeatability_detail.append({
                "work_order_id": order["work_order_id"],
                "observed_runs": len(group),
                "distinct_execution_ids": len(distinct_execs),
                "outcome_signatures": signatures,
                "pass": group_pass,
            })

        complete = not missing_slots
        prompt_pass = complete and not failed_receipts and repeatability_pass and not global_errors
        state = "BASELINE_PASS" if prompt_pass else ("INCOMPLETE" if not complete else "BASELINE_FAIL")
        prompt_results.append({
            "prompt_id": prompt_id,
            "state": state,
            "accepted_receipts": len(prompt_rows),
            "required_receipts": len(required_slots),
            "missing_slots": [f"{wo}#{rep}" for wo, rep in missing_slots],
            "failed_receipts": failed_receipts,
            "repeatability": repeatability_detail,
            "eligible_for_F4_TESTED": prompt_pass,
        })

    complete_campaign = len(accepted) == 84 and all(r["state"] != "INCOMPLETE" for r in prompt_results)
    all_prompts_pass = complete_campaign and all(r["eligible_for_F4_TESTED"] for r in prompt_results)
    status = (
        "BASELINE_PASS" if all_prompts_pass and not global_errors
        else "BASELINE_FAIL" if complete_campaign
        else "EXECUTION_INCOMPLETE"
    )
    report = {
        "schema": "prompt-quarry-pcp04-aggregate-v1",
        "status": status,
        "campaign_id": next(iter(campaign_ids)) if len(campaign_ids) == 1 else None,
        "runtime": list(next(iter(runtime_keys))) if len(runtime_keys) == 1 else None,
        "receipt_count": len(receipt_paths),
        "accepted_receipt_count": len(accepted),
        "required_execution_count": 84,
        "prompt_results": prompt_results,
        "F4_TESTED": bool(all_prompts_pass and not global_errors),
        "errors": global_errors,
    }

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")

    if global_errors:
        return 1
    if args.require_complete and not all_prompts_pass:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
