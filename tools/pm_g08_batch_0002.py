#!/usr/bin/env python3
"""Run G08 BATCH-0002 for Evidence-first Code Review v2.1.

This runner reuses the four predeclared regression fixtures/evaluation contracts,
but binds runtime execution to the corrected v2.1 workflow surface by exact Git
blob identity. It performs all integrity checks before authorization is consumed.
At most one Gemini request is issued per case, in order, with zero retries.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pm_g08_batch as base

BATCH_ID = "PM-STARTER-CR-V2-G08-BATCH-0002"
EXACT_AUTH = "AUTORIZO PM-STARTER-CR-V2-G08-BATCH-0002: hasta 4 ejecuciones, 0 reintentos por caso."
PLAN = base.ROOT / "commercial/STARTER_N09_G08_V2_1_BATCH_0002_PLAN.json"
FREEZE = base.ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_FREEZE_RECEIPT_2026-09-07.json"
STATIC_REAUDIT = base.ROOT / "commercial/STARTER_N09_G08_V2_1_STATIC_REAUDIT_PASS_2026-09-07.json"
BOUNDED_BATCH_POLICY = base.ROOT / "commercial/PROMPT_MACHINE_BOUNDED_BATCH_EXECUTION_POLICY_V1.json"
CASES_DIR = base.ROOT / "product/starter-collection-v2/evaluation/cases"
REVIEWS_DIR = base.ROOT / "product/starter-collection-v2/evaluation/reviews"
EXPECTED_CONTRACT_MARKER = b"Contract version: `2.1.0`"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def canonical_case_path(case_id: str) -> Path:
    return CASES_DIR / f"{case_id}.json"


def canonical_evaluation_path(case_id: str) -> Path:
    return REVIEWS_DIR / f"{case_id}.evaluation.json"


def load_and_preflight(output_root: Path) -> tuple[dict, list[dict], list[dict]]:
    checks: dict[str, bool] = {}
    prepared: list[dict] = []
    evaluations: list[dict] = []
    rendered_envelopes: dict[str, dict[str, object]] = {}

    try:
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
        freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
        static_reaudit = json.loads(STATIC_REAUDIT.read_text(encoding="utf-8"))
        bounded_policy = json.loads(BOUNDED_BATCH_POLICY.read_text(encoding="utf-8"))
    except Exception as exc:
        return ({
            "schema": "prompt-machine-starter-n09-g08-v2-1-batch-preflight-v1",
            "batch_id": BATCH_ID,
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
    frozen_cases = freeze.get("frozen_cases") or []
    frozen = {x.get("case_id"): x for x in frozen_cases if isinstance(x, dict)}
    workflow_path = base.ROOT / str(plan.get("workflow_surface", ""))
    workflow_bytes = workflow_path.read_bytes() if workflow_path.is_file() else b""
    workflow_blob_sha = git_blob_sha(workflow_bytes) if workflow_bytes else ""

    checks.update({
        "contracts_loadable": True,
        "wsl_detected": base.assert_wsl(),
        "gemini_api_key_present": bool(base.os.environ.get("GEMINI_API_KEY")),
        "batch_id_exact": plan.get("batch_id") == BATCH_ID,
        "batch_not_self_authorized_in_repo": plan.get("state") == "PREPARED_NOT_AUTHORIZED",
        "workflow_id_exact": plan.get("workflow_id") == base.WORKFLOW_ID,
        "contract_version_exact": plan.get("contract_version") == "2.1.0",
        "workflow_surface_present": workflow_path.is_file(),
        "workflow_blob_sha_exact": workflow_blob_sha == plan.get("workflow_github_blob_sha"),
        "workflow_contract_marker_exact": EXPECTED_CONTRACT_MARKER in workflow_bytes,
        "static_reaudit_pass": static_reaudit.get("verdict") == "PASS_STATIC_ONLY",
        "static_reaudit_same_blob": static_reaudit.get("workflow_github_blob_sha") == workflow_blob_sha,
        "bounded_batch_policy_present": BOUNDED_BATCH_POLICY.is_file(),
        "four_cases_exact": len(cases) == 4 and len(set(cases)) == 4,
        "same_four_frozen_cases": cases == [x.get("case_id") for x in frozen_cases],
        "max_total_requests_four": plan.get("maximum_provider_requests_total") == 4,
        "one_request_per_case": plan.get("maximum_provider_requests_per_case") == 1,
        "zero_retries": plan.get("automatic_retries_per_case") == 0,
        "human_review_after_batch": plan.get("human_review_timing") == "AFTER_BATCH",
        "automatic_semantic_judgement_false": plan.get("automatic_semantic_judgement") is False,
        "automatic_certification_false": plan.get("automatic_certification") is False,
        "automatic_promotion_false": plan.get("automatic_promotion") is False,
        "evaluation_excluded": plan.get("evaluation_contract_is_runtime_input") is False,
        "expected_excluded": plan.get("expected_result_is_runtime_input") is False,
        "output_root_absent": not output_root.exists(),
    })

    workflow_text = workflow_bytes.decode("utf-8") if workflow_bytes else ""

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
        checks[prefix + "case_id_exact"] = case.get("case_id") == case_id
        checks[prefix + "workflow_id_exact"] = case.get("workflow_id") == base.WORKFLOW_ID
        checks[prefix + "runtime_not_preexecuted_fixture"] = case.get("runtime_executed") is False
        checks[prefix + "evaluation_not_runtime_fixture"] = case.get("evaluation_contract_is_runtime_input") is False
        checks[prefix + "evaluation_case_exact"] = evaluation.get("case_id") == case_id
        checks[prefix + "evaluation_predeclared"] = evaluation.get("predeclared_before_runtime") is True
        checks[prefix + "evaluation_not_runtime"] = evaluation.get("evaluation_contract_is_runtime_input") is False
        checks[prefix + "expected_not_runtime"] = evaluation.get("expected_result_is_runtime_input") is False
        checks[prefix + "workflow_surface_path_matches_plan"] = case.get("workflow_surface_path") == plan.get("workflow_surface")

        envelope = base.render(workflow_text, case.get("instance_data_markdown", ""))
        envelope_sha = base.sha(envelope)
        envelope_bytes = len(envelope)
        rendered_envelopes[case_id] = {
            "bytes": envelope_bytes,
            "sha256": envelope_sha,
        }

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
        "schema": "prompt-machine-starter-n09-g08-v2-1-batch-preflight-v1",
        "batch_id": BATCH_ID,
        "recorded_at": base.now(),
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "runtime_executions_attempted": 0,
        "workflow_github_blob_sha": workflow_blob_sha,
        "rendered_envelopes": rendered_envelopes,
        "checks": checks,
        "verdict": "PASS" if not failed else "FAIL",
        "failed_checks": failed,
        "authorization_not_consumed_during_preflight": True,
        "truth_boundary": "ZERO_MODEL_PREFLIGHT_ONLY_UNTIL_PASS_AND_EXACT_BATCH_0002_AUTHORIZATION",
    }
    return report, prepared, evaluations


base.BATCH_ID = BATCH_ID
base.EXACT_AUTH = EXACT_AUTH
base.PLAN = PLAN
base.load_and_preflight = load_and_preflight

if __name__ == "__main__":
    raise SystemExit(base.main())
