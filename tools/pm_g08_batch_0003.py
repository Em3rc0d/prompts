#!/usr/bin/env python3
"""Run governed G08 BATCH-0003 for the composite Evidence-first Code Review v2.2 candidate.

The runtime surface is the exact v2.1 base workflow plus the exact normative v2.2
hardening addendum. All integrity checks run before authorization is consumed.
At most one Gemini request is issued per frozen case, in order, with zero retries.
Evaluation contracts and expected results are never sent to the model.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pm_g08_batch as base

BATCH_ID = "PM-STARTER-CR-V2-G08-BATCH-0003"
EXACT_AUTH = "AUTORIZO PM-STARTER-CR-V2-G08-BATCH-0003: hasta 4 ejecuciones, 0 reintentos por caso."
PLAN = base.ROOT / "commercial/STARTER_N09_G08_V2_2_BATCH_0003_PLAN.json"
FREEZE = base.ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_FREEZE_RECEIPT_2026-09-07.json"
STATIC_REAUDIT = base.ROOT / "commercial/STARTER_N09_G08_V2_2_STATIC_REAUDIT_PASS_2026-09-07.json"
CASES_DIR = base.ROOT / "product/starter-collection-v2/evaluation/cases"
REVIEWS_DIR = base.ROOT / "product/starter-collection-v2/evaluation/reviews"
BASE_SURFACE = base.ROOT / "product/starter-collection-v2/workflows/evidence-first-code-review.md"
ADDENDUM_SURFACE = base.ROOT / "product/starter-collection-v2/workflows/evidence-first-code-review-v2-2-hardening.md"
EXPECTED_BASE_BLOB = "20b837873cc766dfb139ecfe3c8127c4f301029c"
EXPECTED_ADDENDUM_BLOB = "6da13d8c4e0ad11fd791d89949453208fb5ca168"
MODEL = "gemini-3.5-flash"
MAX_OUTPUT_TOKENS = 4096
THINKING_LEVEL = "minimal"
PROVIDER = "GOOGLE_GEMINI_API"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def canonical_case_path(case_id: str) -> Path:
    return CASES_DIR / f"{case_id}.json"


def canonical_evaluation_path(case_id: str) -> Path:
    return REVIEWS_DIR / f"{case_id}.evaluation.json"


def composite_surface(base_text: str, addendum_text: str) -> str:
    return (
        base_text.rstrip("\n")
        + "\n\n---\n\n"
        + "<<<NORMATIVE_HARDENING_ADDENDUM_V2_2>>>\n"
        + addendum_text.rstrip("\n")
        + "\n<<<END_NORMATIVE_HARDENING_ADDENDUM_V2_2>>>\n"
    )


def load_and_preflight(output_root: Path) -> tuple[dict, list[dict], list[dict]]:
    checks: dict[str, bool] = {}
    prepared: list[dict] = []
    evaluations: list[dict] = []
    rendered_envelopes: dict[str, dict[str, object]] = {}

    try:
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
        freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
        static_reaudit = json.loads(STATIC_REAUDIT.read_text(encoding="utf-8"))
        base_bytes = BASE_SURFACE.read_bytes()
        addendum_bytes = ADDENDUM_SURFACE.read_bytes()
        base_text = base_bytes.decode("utf-8")
        addendum_text = addendum_bytes.decode("utf-8")
    except Exception as exc:
        return ({
            "schema": "prompt-machine-starter-n09-g08-v2-2-batch-preflight-v1",
            "batch_id": BATCH_ID,
            "recorded_at": base.now(),
            "provider_requests_attempted": 0,
            "model_inference_requests_attempted": 0,
            "runtime_executions_attempted": 0,
            "checks": {"contracts_and_surfaces_loadable": False},
            "verdict": "FAIL",
            "failed_checks": ["contracts_and_surfaces_loadable"],
            "preflight_error_type": type(exc).__name__,
            "authorization_not_consumed_during_preflight": True,
        }, prepared, evaluations)

    base_blob = git_blob_sha(base_bytes)
    addendum_blob = git_blob_sha(addendum_bytes)
    surface = composite_surface(base_text, addendum_text)
    surface_bytes = surface.encode("utf-8")
    surface_sha = base.sha(surface_bytes)

    cases = plan.get("cases") or []
    frozen_cases = freeze.get("frozen_cases") or []
    frozen = {x.get("case_id"): x for x in frozen_cases if isinstance(x, dict)}

    checks.update({
        "contracts_and_surfaces_loadable": True,
        "wsl_detected": base.assert_wsl(),
        "gemini_api_key_present": bool(base.os.environ.get("GEMINI_API_KEY")),
        "batch_id_exact": plan.get("batch_id") == BATCH_ID,
        "batch_not_self_authorized_in_repo": plan.get("state") == "PREPARED_NOT_AUTHORIZED",
        "workflow_id_exact": plan.get("workflow_id") == base.WORKFLOW_ID,
        "candidate_contract_version_exact": plan.get("candidate_contract_version") == "2.2.0",
        "surface_mode_exact": plan.get("surface_mode") == "COMPOSITE_V2_1_PLUS_NORMATIVE_V2_2_HARDENING_ADDENDUM",
        "base_surface_present": BASE_SURFACE.is_file(),
        "addendum_surface_present": ADDENDUM_SURFACE.is_file(),
        "base_blob_exact": base_blob == EXPECTED_BASE_BLOB == plan.get("base_surface_github_blob_sha"),
        "addendum_blob_exact": addendum_blob == EXPECTED_ADDENDUM_BLOB == plan.get("hardening_addendum_github_blob_sha"),
        "base_contract_marker_present": "Contract version: `2.1.0`" in base_text,
        "addendum_contract_marker_present": "Addendum contract version: `2.2.0`" in addendum_text,
        "admission_gate_present": "MATERIAL-FINDING EVIDENCE ADMISSION GATE" in addendum_text,
        "supplied_contract_presumption_present": "SUPPLIED-CONTRACT PRESUMPTION" in addendum_text,
        "type_mismatch_rule_present": "TYPE-MISMATCH ADMISSION RULE" in addendum_text,
        "satisfied_invariant_mode_present": "SATISFIED_INVARIANT_MODE" in addendum_text,
        "static_reaudit_pass": static_reaudit.get("verdict") == "PASS_STATIC_ONLY",
        "static_reaudit_base_blob_exact": static_reaudit.get("base_surface", {}).get("github_blob_sha") == base_blob,
        "static_reaudit_addendum_blob_exact": static_reaudit.get("hardening_addendum", {}).get("github_blob_sha") == addendum_blob,
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

        envelope = base.render(surface, case.get("instance_data_markdown", ""))
        envelope_sha = base.sha(envelope)
        envelope_bytes = len(envelope)
        rendered_envelopes[case_id] = {"bytes": envelope_bytes, "sha256": envelope_sha}

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
        "schema": "prompt-machine-starter-n09-g08-v2-2-batch-preflight-v1",
        "batch_id": BATCH_ID,
        "recorded_at": base.now(),
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "runtime_executions_attempted": 0,
        "base_surface_github_blob_sha": base_blob,
        "hardening_addendum_github_blob_sha": addendum_blob,
        "composite_surface_bytes": len(surface_bytes),
        "composite_surface_sha256": surface_sha,
        "rendered_envelopes": rendered_envelopes,
        "checks": checks,
        "verdict": "PASS" if not failed else "FAIL",
        "failed_checks": failed,
        "authorization_not_consumed_during_preflight": True,
        "truth_boundary": "ZERO_MODEL_PREFLIGHT_ONLY_UNTIL_PASS_AND_EXACT_BATCH_0003_AUTHORIZATION",
    }
    return report, prepared, evaluations


def request_case(case: dict, key: str, out: Path) -> dict:
    case_id = case["case_id"]
    body = {
        "contents": [{"role": "user", "parts": [{"text": case["envelope"].decode("utf-8")}]}],
        "generationConfig": {
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
            "thinkingConfig": {"thinkingLevel": THINKING_LEVEL},
        },
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + urllib.parse.quote(MODEL, safe="") + ":generateContent"
    req = urllib.request.Request(endpoint, data=encoded, method="POST", headers={
        "x-goog-api-key": key,
        "Content-Type": "application/json",
    })
    execution_id = f"{case_id}-G08-BATCH-0003-{secrets.token_hex(6).upper()}"
    started_at = base.now()
    out.mkdir(parents=True, exist_ok=False)

    try:
        with urllib.request.urlopen(req, timeout=240) as response:
            raw = response.read()
            status = response.status
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        (out / "raw-provider-error.bin").write_bytes(raw)
        receipt = {
            "case_id": case_id,
            "batch_id": BATCH_ID,
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "http_status": exc.code,
            "behavioral_observations": 0,
            "response_body_sha256": base.sha(raw),
            "state": "PROVIDER_FAILURE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        base.write_json(out / "runtime-evidence.json", receipt)
        return receipt
    except Exception as exc:
        receipt = {
            "case_id": case_id,
            "batch_id": BATCH_ID,
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "error_type": type(exc).__name__,
            "state": "TRANSPORT_FAILURE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        base.write_json(out / "runtime-evidence.json", receipt)
        return receipt

    (out / "raw-provider-response.json").write_bytes(raw)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        receipt = {
            "case_id": case_id,
            "batch_id": BATCH_ID,
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "http_status": status,
            "behavioral_observations": 0,
            "raw_provider_response_sha256": base.sha(raw),
            "state": "INVALID_PROVIDER_RESPONSE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        base.write_json(out / "runtime-evidence.json", receipt)
        return receipt

    output = base.extract_text(payload)
    output_bytes = output.encode("utf-8")
    (out / "raw-output.md").write_bytes(output_bytes)
    receipt = {
        "schema": "prompt-machine-starter-n09-g08-v2-2-batch-case-observation-v1",
        "batch_id": BATCH_ID,
        "case_id": case_id,
        "execution_id": execution_id,
        "provider": PROVIDER,
        "model_requested": MODEL,
        "provider_model_version": payload.get("modelVersion"),
        "started_at": started_at,
        "completed_at": base.now(),
        "http_status": status,
        "provider_requests_attempted": 1,
        "automatic_retries": 0,
        "behavioral_observations": 1 if output else 0,
        "finish_reasons": [c.get("finishReason") for c in payload.get("candidates") or []],
        "runtime_envelope_bytes": case["envelope_bytes"],
        "runtime_envelope_sha256": case["envelope_sha256"],
        "request_body_sha256": base.sha(encoded),
        "raw_provider_response_sha256": base.sha(raw),
        "raw_output_bytes": len(output_bytes),
        "raw_output_sha256": base.sha(output_bytes),
        "usage_metadata": payload.get("usageMetadata"),
        "evaluation_contract_sent": False,
        "expected_result_sent": False,
        "human_review_required": True,
        "automatic_semantic_judgement": False,
        "automatic_promotion": False,
        "state": "OBSERVED_HUMAN_REVIEW_REQUIRED" if output else "EMPTY_OUTPUT_HUMAN_REVIEW_REQUIRED",
    }
    base.write_json(out / "runtime-evidence.json", receipt)
    return receipt


base.BATCH_ID = BATCH_ID
base.EXACT_AUTH = EXACT_AUTH
base.PLAN = PLAN
base.load_and_preflight = load_and_preflight
base.request_case = request_case

if __name__ == "__main__":
    raise SystemExit(base.main())
