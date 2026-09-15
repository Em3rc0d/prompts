#!/usr/bin/env python3
"""Hardened entrypoint for the governed G08 v2 regression batch.

This successor fixes the initial batch preflight's incorrect assumption that the
freeze receipt carried repository paths. Canonical case/evaluation paths are
derived from case_id and their bytes are verified against the frozen SHA-256
values before any provider request can occur.
"""
from __future__ import annotations

import json
from pathlib import Path

import pm_g08_batch as base

CASES_DIR = base.ROOT / "product/starter-collection-v2/evaluation/cases"
REVIEWS_DIR = base.ROOT / "product/starter-collection-v2/evaluation/reviews"


def canonical_case_path(case_id: str) -> Path:
    return CASES_DIR / f"{case_id}.json"


def canonical_evaluation_path(case_id: str) -> Path:
    return REVIEWS_DIR / f"{case_id}.evaluation.json"


def fixed_load_and_preflight(output_root: Path) -> tuple[dict, list[dict], list[dict]]:
    checks: dict[str, bool] = {}
    prepared: list[dict] = []
    evaluations: list[dict] = []

    try:
        plan = json.loads(base.PLAN.read_text(encoding="utf-8"))
        design = json.loads(base.DESIGN.read_text(encoding="utf-8"))
        freeze = json.loads(base.FREEZE.read_text(encoding="utf-8"))
    except Exception as exc:
        return ({
            "schema": "prompt-machine-starter-n09-g08-v2-batch-preflight-v2",
            "batch_id": base.BATCH_ID,
            "recorded_at": base.now(),
            "provider_requests_attempted": 0,
            "model_inference_requests_attempted": 0,
            "runtime_executions_attempted": 0,
            "checks": {"contracts_loadable": False},
            "verdict": "FAIL",
            "failed_checks": ["contracts_loadable"],
            "preflight_error_type": type(exc).__name__,
            "authorization_not_consumed_during_preflight": True,
        }, prepared, evaluations)

    cases = plan.get("cases") or []
    order = design.get("execution_order") or []
    frozen_cases = freeze.get("frozen_cases") or []
    frozen = {x.get("case_id"): x for x in frozen_cases if isinstance(x, dict)}

    checks.update({
        "contracts_loadable": True,
        "wsl_detected": base.assert_wsl(),
        "gemini_api_key_present": bool(base.os.environ.get("GEMINI_API_KEY")),
        "batch_id_exact": plan.get("batch_id") == base.BATCH_ID,
        "batch_not_self_authorized_in_repo": plan.get("state") == "PREPARED_NOT_AUTHORIZED",
        "workflow_id_exact": plan.get("workflow_id") == base.WORKFLOW_ID,
        "model_exact": plan.get("model") == base.MODEL,
        "model_syntax_valid": bool(base.MODEL_RE.fullmatch(base.MODEL)),
        "four_cases_exact": len(cases) == 4 and len(set(cases)) == 4,
        "execution_order_exact": cases == order,
        "freeze_pass": freeze.get("verdict") == "PASS",
        "freeze_four_cases_exact": len(frozen_cases) == 4,
        "max_total_requests_four": plan.get("maximum_provider_requests_total") == 4,
        "one_request_per_case": plan.get("maximum_provider_requests_per_case") == 1,
        "zero_retries": plan.get("automatic_retries_per_case") == 0,
        "human_review_after_batch": plan.get("human_review_timing") == "AFTER_BATCH",
        "evaluation_excluded": plan.get("evaluation_contract_is_runtime_input") is False,
        "expected_excluded": plan.get("expected_result_is_runtime_input") is False,
        "output_root_absent": not output_root.exists(),
    })

    for case_id in cases:
        prefix = case_id + ":"
        frozen_case = frozen.get(case_id)
        case_path = canonical_case_path(case_id)
        eval_path = canonical_evaluation_path(case_id)

        checks[prefix + "frozen_entry_present"] = isinstance(frozen_case, dict)
        checks[prefix + "case_file_present"] = case_path.is_file()
        checks[prefix + "evaluation_file_present"] = eval_path.is_file()
        if not frozen_case or not case_path.is_file() or not eval_path.is_file():
            continue

        try:
            case_bytes = case_path.read_bytes()
            eval_bytes = eval_path.read_bytes()
            case = json.loads(case_bytes.decode("utf-8"))
            evaluation = json.loads(eval_bytes.decode("utf-8"))
        except Exception:
            checks[prefix + "files_parseable"] = False
            continue

        checks[prefix + "files_parseable"] = True
        checks[prefix + "case_file_sha_frozen"] = base.sha(case_bytes) == frozen_case.get("case_file_sha256")
        checks[prefix + "evaluation_file_sha_frozen"] = base.sha(eval_bytes) == frozen_case.get("evaluation_file_sha256")
        checks[prefix + "case_id"] = case.get("case_id") == case_id
        checks[prefix + "workflow_id"] = case.get("workflow_id") == base.WORKFLOW_ID
        checks[prefix + "runtime_not_preexecuted_fixture"] = case.get("runtime_executed") is False
        checks[prefix + "eval_excluded_fixture"] = case.get("evaluation_contract_is_runtime_input") is False
        checks[prefix + "evaluation_case"] = evaluation.get("case_id") == case_id
        checks[prefix + "evaluation_predeclared"] = evaluation.get("predeclared_before_runtime") is True
        checks[prefix + "evaluation_not_runtime"] = evaluation.get("evaluation_contract_is_runtime_input") is False
        checks[prefix + "expected_not_runtime"] = evaluation.get("expected_result_is_runtime_input") is False

        workflow_path_value = case.get("workflow_surface_path")
        workflow_path = base.ROOT / workflow_path_value if isinstance(workflow_path_value, str) else Path("/__missing__")
        checks[prefix + "workflow_surface_present"] = workflow_path.is_file()
        checks[prefix + "workflow_surface_matches_freeze"] = workflow_path_value == freeze.get("workflow_surface_path")
        if not workflow_path.is_file():
            continue

        workflow = workflow_path.read_text(encoding="utf-8")
        envelope = base.render(workflow, case.get("instance_data_markdown", ""))
        envelope_sha = base.sha(envelope)
        envelope_bytes = len(envelope)

        checks[prefix + "envelope_bytes_frozen"] = envelope_bytes == frozen_case.get("runtime_envelope_bytes")
        checks[prefix + "envelope_sha_frozen"] = envelope_sha == frozen_case.get("runtime_envelope_sha256")
        checks[prefix + "evaluation_bytes_absent_from_envelope"] = eval_bytes not in envelope
        checks[prefix + "evaluation_markers_absent"] = not any(
            marker in envelope
            for marker in (b'"expected"', b'"blocking_dimensions"', b'expected_result_is_runtime_input')
        )

        prepared.append({
            "case_id": case_id,
            "case_path": str(case_path.relative_to(base.ROOT)),
            "evaluation_path": str(eval_path.relative_to(base.ROOT)),
            "envelope": envelope,
            "envelope_bytes": envelope_bytes,
            "envelope_sha256": envelope_sha,
        })
        evaluations.append(evaluation)

    checks["all_four_cases_prepared"] = len(prepared) == 4 and len(evaluations) == 4
    failed = [name for name, ok in checks.items() if not ok]
    report = {
        "schema": "prompt-machine-starter-n09-g08-v2-batch-preflight-v2",
        "batch_id": base.BATCH_ID,
        "recorded_at": base.now(),
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "runtime_executions_attempted": 0,
        "checks": checks,
        "verdict": "PASS" if not failed else "FAIL",
        "failed_checks": failed,
        "authorization_not_consumed_during_preflight": True,
        "truth_boundary": "ZERO_MODEL_PREFLIGHT_ONLY_UNTIL_PASS_AND_EXACT_BATCH_AUTHORIZATION",
    }
    return report, prepared, evaluations


base.load_and_preflight = fixed_load_and_preflight

if __name__ == "__main__":
    raise SystemExit(base.main())
