#!/usr/bin/env python3
"""Run governed G09 OpenAI portability BATCH-0001.

This runner tests the exact canonical Evidence-first Code Review v2.2 composite
surface that earned G08 PASS, using the exact same four frozen cases and the
same predeclared out-of-band evaluation contracts on a declared non-Gemini
model family.

All integrity checks run before authorization is consumed. At most one OpenAI
Responses API request is issued per case, in frozen order, with zero retries.
Evaluation contracts and expected results are never sent to the model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "PM-STARTER-CR-V2-G09-OPENAI-BATCH-0001"
WORKFLOW_ID = "pm-starter-evidence-first-code-review-v2"
MODEL = "gpt-5.6-luna"
MODEL_FAMILY = "OPENAI_GPT_5_6"
PROVIDER = "OPENAI_RESPONSES_API"
ENDPOINT = "https://api.openai.com/v1/responses"
MAX_OUTPUT_TOKENS = 4096
REASONING_EFFORT = "low"
EXACT_AUTH = "AUTORIZO PM-STARTER-CR-V2-G09-OPENAI-BATCH-0001: hasta 4 ejecuciones, 0 reintentos por caso."

PLAN = ROOT / "commercial/STARTER_N09_G09_OPENAI_BATCH_0001_PLAN.json"
G09_DESIGN = ROOT / "commercial/STARTER_N09_G09_PORTABILITY_DESIGN_V1.json"
G08_PASS = ROOT / "commercial/STARTER_N09_G08_V2_2_BATCH_0003_HUMAN_REVIEW_PASS_2026-09-07.json"
G08_FREEZE = ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_FREEZE_RECEIPT_2026-09-07.json"
SURFACE_MANIFEST = ROOT / "product/starter-collection-v2/workflows/evidence-first-code-review-v2-2.surface.json"
BASE_SURFACE = ROOT / "product/starter-collection-v2/workflows/evidence-first-code-review.md"
ADDENDUM_SURFACE = ROOT / "product/starter-collection-v2/workflows/evidence-first-code-review-v2-2-hardening.md"
CASES_DIR = ROOT / "product/starter-collection-v2/evaluation/cases"
REVIEWS_DIR = ROOT / "product/starter-collection-v2/evaluation/reviews"

EXPECTED_BASE_BLOB = "20b837873cc766dfb139ecfe3c8127c4f301029c"
EXPECTED_ADDENDUM_BLOB = "6da13d8c4e0ad11fd791d89949453208fb5ca168"
EXPECTED_COMPOSITE_SHA256 = "6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977"
EXPECTED_COMPOSITE_BYTES = 25295
OPEN_MARKER = "<<<NORMATIVE_HARDENING_ADDENDUM_V2_2>>>"
CLOSE_MARKER = "<<<END_NORMATIVE_HARDENING_ADDENDUM_V2_2>>>"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def assert_wsl() -> bool:
    p = Path("/proc/version")
    text = p.read_text(errors="ignore").lower() if p.exists() else ""
    return "microsoft" in text or "wsl" in text


def norm(text: str) -> str:
    return text.rstrip("\n") + "\n"


def composite_surface(base_text: str, addendum_text: str) -> str:
    return (
        base_text.rstrip("\n")
        + "\n\n---\n\n"
        + OPEN_MARKER
        + "\n"
        + addendum_text.rstrip("\n")
        + "\n"
        + CLOSE_MARKER
        + "\n"
    )


def render(surface: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + norm(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + norm(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def canonical_case_path(case_id: str) -> Path:
    return CASES_DIR / f"{case_id}.json"


def canonical_evaluation_path(case_id: str) -> Path:
    return REVIEWS_DIR / f"{case_id}.evaluation.json"


def extract_output_text(payload: dict) -> str:
    chunks: list[str] = []
    for item in payload.get("output") or []:
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        for part in item.get("content") or []:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "output_text" and isinstance(part.get("text"), str):
                if part["text"]:
                    chunks.append(part["text"])
    return "\n".join(chunks).strip()


def load_and_preflight(output_root: Path) -> tuple[dict, list[dict], list[dict]]:
    checks: dict[str, bool] = {}
    prepared: list[dict] = []
    evaluations: list[dict] = []
    rendered_envelopes: dict[str, dict[str, object]] = {}

    try:
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
        design = json.loads(G09_DESIGN.read_text(encoding="utf-8"))
        g08_pass = json.loads(G08_PASS.read_text(encoding="utf-8"))
        freeze = json.loads(G08_FREEZE.read_text(encoding="utf-8"))
        manifest = json.loads(SURFACE_MANIFEST.read_text(encoding="utf-8"))
        base_bytes = BASE_SURFACE.read_bytes()
        addendum_bytes = ADDENDUM_SURFACE.read_bytes()
        base_text = base_bytes.decode("utf-8")
        addendum_text = addendum_bytes.decode("utf-8")
    except Exception as exc:
        return ({
            "schema": "prompt-machine-starter-n09-g09-openai-batch-preflight-v1",
            "batch_id": BATCH_ID,
            "recorded_at": now(),
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
    surface_sha = sha256(surface_bytes)

    cases = plan.get("cases") or []
    required_cases = design.get("required_cases") or []
    frozen_cases = freeze.get("frozen_cases") or []
    frozen = {x.get("case_id"): x for x in frozen_cases if isinstance(x, dict)}

    composition = manifest.get("composition_order") or []
    manifest_base_blob = composition[0].get("github_blob_sha") if len(composition) > 0 else None
    manifest_addendum_blob = composition[1].get("github_blob_sha") if len(composition) > 1 else None

    checks.update({
        "contracts_and_surfaces_loadable": True,
        "wsl_detected": assert_wsl(),
        "openai_api_key_present": bool(os.environ.get("OPENAI_API_KEY")),
        "batch_id_exact": plan.get("batch_id") == BATCH_ID,
        "batch_not_self_authorized_in_repo": plan.get("state") == "PREPARED_NOT_AUTHORIZED",
        "gate_exact": plan.get("gate") == "G09_PORTABILITY",
        "workflow_id_exact": plan.get("workflow_id") == WORKFLOW_ID,
        "contract_version_exact": plan.get("candidate_contract_version") == "2.2.0",
        "provider_exact": plan.get("provider") == PROVIDER,
        "model_family_exact": plan.get("model_family") == MODEL_FAMILY,
        "model_exact": plan.get("model") == MODEL,
        "endpoint_exact": plan.get("provider_endpoint") == ENDPOINT,
        "credential_name_exact": plan.get("credential_environment_variable") == "OPENAI_API_KEY",
        "generation_output_budget_exact": (plan.get("generation") or {}).get("max_output_tokens") == MAX_OUTPUT_TOKENS,
        "reasoning_effort_exact": (plan.get("generation") or {}).get("reasoning_effort") == REASONING_EFFORT,
        "store_false": (plan.get("generation") or {}).get("store") is False,
        "tools_disabled": (plan.get("generation") or {}).get("tools_enabled") is False,
        "g08_pass_exact": g08_pass.get("g08_result") == "PASS",
        "g08_four_passes": all(v == "PASS" for v in (g08_pass.get("human_review_results") or {}).values()) and len(g08_pass.get("human_review_results") or {}) == 4,
        "g09_design_not_armed": design.get("state") == "DESIGNED_NOT_ARMED",
        "g09_requires_non_gemini": (design.get("portability_baseline_requirement") or {}).get("minimum_new_non_gemini_families") == 1,
        "g09_same_surface_required": (design.get("portability_baseline_requirement") or {}).get("same_canonical_surface_required") is True,
        "manifest_contract_exact": manifest.get("contract_version") == "2.2.0",
        "manifest_g08_pass": manifest.get("g08_result") == "PASS",
        "manifest_portability_not_yet_tested": manifest.get("portability_status") == "NOT_YET_G09_TESTED",
        "base_surface_present": BASE_SURFACE.is_file(),
        "addendum_surface_present": ADDENDUM_SURFACE.is_file(),
        "base_blob_exact": base_blob == EXPECTED_BASE_BLOB == manifest_base_blob,
        "addendum_blob_exact": addendum_blob == EXPECTED_ADDENDUM_BLOB == manifest_addendum_blob,
        "composite_bytes_exact": len(surface_bytes) == EXPECTED_COMPOSITE_BYTES == manifest.get("tested_composite_surface_bytes"),
        "composite_sha_exact": surface_sha == EXPECTED_COMPOSITE_SHA256 == manifest.get("tested_composite_surface_sha256") == plan.get("canonical_surface_sha256"),
        "four_cases_exact": len(cases) == 4 and len(set(cases)) == 4,
        "same_g09_required_cases": cases == required_cases,
        "same_original_frozen_order": cases == [x.get("case_id") for x in frozen_cases],
        "max_total_requests_four": plan.get("maximum_provider_requests_total") == 4,
        "one_request_per_case": plan.get("maximum_provider_requests_per_case") == 1,
        "zero_retries": plan.get("automatic_retries_per_case") == 0,
        "human_review_after_batch": plan.get("human_review_timing") == "AFTER_BATCH",
        "human_review_required": plan.get("human_review_required") is True,
        "automatic_semantic_judgement_false": plan.get("automatic_semantic_judgement") is False,
        "automatic_certification_false": plan.get("automatic_certification") is False,
        "automatic_promotion_false": plan.get("automatic_promotion") is False,
        "evaluation_excluded": plan.get("evaluation_contract_is_runtime_input") is False,
        "expected_excluded": plan.get("expected_result_is_runtime_input") is False,
        "clean_context_required": plan.get("clean_independent_context_required") is True,
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
        checks[prefix + "case_file_sha_frozen"] = sha256(case_bytes) == frozen_case.get("case_file_sha256")
        checks[prefix + "evaluation_file_sha_frozen"] = sha256(eval_bytes) == frozen_case.get("evaluation_file_sha256")
        checks[prefix + "case_id_exact"] = case.get("case_id") == case_id
        checks[prefix + "workflow_id_exact"] = case.get("workflow_id") == WORKFLOW_ID
        checks[prefix + "runtime_not_preexecuted_fixture"] = case.get("runtime_executed") is False
        checks[prefix + "evaluation_not_runtime_fixture"] = case.get("evaluation_contract_is_runtime_input") is False
        checks[prefix + "evaluation_case_exact"] = evaluation.get("case_id") == case_id
        checks[prefix + "evaluation_predeclared"] = evaluation.get("predeclared_before_runtime") is True
        checks[prefix + "evaluation_not_runtime"] = evaluation.get("evaluation_contract_is_runtime_input") is False
        checks[prefix + "expected_not_runtime"] = evaluation.get("expected_result_is_runtime_input") is False

        envelope = render(surface, case.get("instance_data_markdown", ""))
        envelope_sha = sha256(envelope)
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
            "case_path": str(case_path.relative_to(ROOT)),
            "evaluation_path": str(eval_path.relative_to(ROOT)),
            "envelope": envelope,
            "envelope_bytes": envelope_bytes,
            "envelope_sha256": envelope_sha,
        })
        evaluations.append(evaluation)

    checks["all_four_cases_prepared"] = len(prepared) == 4 and len(evaluations) == 4
    failed = [name for name, ok in checks.items() if not ok]
    report = {
        "schema": "prompt-machine-starter-n09-g09-openai-batch-preflight-v1",
        "batch_id": BATCH_ID,
        "recorded_at": now(),
        "provider": PROVIDER,
        "model_family": MODEL_FAMILY,
        "model": MODEL,
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "runtime_executions_attempted": 0,
        "canonical_surface_bytes": len(surface_bytes),
        "canonical_surface_sha256": surface_sha,
        "rendered_envelopes": rendered_envelopes,
        "checks": checks,
        "verdict": "PASS" if not failed else "FAIL",
        "failed_checks": failed,
        "authorization_not_consumed_during_preflight": True,
        "truth_boundary": "ZERO_MODEL_G09_PREFLIGHT_ONLY_UNTIL_PASS_AND_EXACT_OPENAI_BATCH_AUTHORIZATION",
    }
    return report, prepared, evaluations


def request_case(case: dict, key: str, out: Path) -> dict:
    case_id = case["case_id"]
    body = {
        "model": MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": case["envelope"].decode("utf-8"),
                    }
                ],
            }
        ],
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "reasoning": {"effort": REASONING_EFFORT},
        "store": False,
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=encoded,
        method="POST",
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
    )
    execution_id = f"{case_id}-G09-OPENAI-BATCH-0001-{secrets.token_hex(6).upper()}"
    started_at = now()
    out.mkdir(parents=True, exist_ok=False)

    try:
        with urllib.request.urlopen(req, timeout=240) as response:
            raw = response.read()
            http_status = response.status
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        (out / "raw-provider-error.bin").write_bytes(raw)
        receipt = {
            "schema": "prompt-machine-starter-n09-g09-openai-provider-failure-v1",
            "batch_id": BATCH_ID,
            "case_id": case_id,
            "execution_id": execution_id,
            "provider": PROVIDER,
            "model_family": MODEL_FAMILY,
            "model_requested": MODEL,
            "started_at": started_at,
            "completed_at": now(),
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "http_status": exc.code,
            "behavioral_observations": 0,
            "response_body_sha256": sha256(raw),
            "evaluation_contract_sent": False,
            "expected_result_sent": False,
            "credential_value_recorded": False,
            "state": "PROVIDER_FAILURE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        write_json(out / "runtime-evidence.json", receipt)
        return receipt
    except Exception as exc:
        receipt = {
            "schema": "prompt-machine-starter-n09-g09-openai-transport-failure-v1",
            "batch_id": BATCH_ID,
            "case_id": case_id,
            "execution_id": execution_id,
            "provider": PROVIDER,
            "model_family": MODEL_FAMILY,
            "model_requested": MODEL,
            "started_at": started_at,
            "completed_at": now(),
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "error_type": type(exc).__name__,
            "evaluation_contract_sent": False,
            "expected_result_sent": False,
            "credential_value_recorded": False,
            "state": "TRANSPORT_FAILURE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        write_json(out / "runtime-evidence.json", receipt)
        return receipt

    (out / "raw-provider-response.json").write_bytes(raw)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        receipt = {
            "schema": "prompt-machine-starter-n09-g09-openai-invalid-response-v1",
            "batch_id": BATCH_ID,
            "case_id": case_id,
            "execution_id": execution_id,
            "provider": PROVIDER,
            "model_family": MODEL_FAMILY,
            "model_requested": MODEL,
            "started_at": started_at,
            "completed_at": now(),
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "http_status": http_status,
            "behavioral_observations": 0,
            "raw_provider_response_sha256": sha256(raw),
            "evaluation_contract_sent": False,
            "expected_result_sent": False,
            "credential_value_recorded": False,
            "state": "INVALID_PROVIDER_RESPONSE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        write_json(out / "runtime-evidence.json", receipt)
        return receipt

    output = extract_output_text(payload)
    output_bytes = output.encode("utf-8")
    (out / "raw-output.md").write_bytes(output_bytes)
    receipt = {
        "schema": "prompt-machine-starter-n09-g09-portability-case-observation-v1",
        "batch_id": BATCH_ID,
        "case_id": case_id,
        "execution_id": execution_id,
        "provider": PROVIDER,
        "model_family": MODEL_FAMILY,
        "model_requested": MODEL,
        "provider_model_version": payload.get("model"),
        "provider_response_id": payload.get("id"),
        "provider_response_status": payload.get("status"),
        "incomplete_details": payload.get("incomplete_details"),
        "started_at": started_at,
        "completed_at": now(),
        "http_status": http_status,
        "provider_requests_attempted": 1,
        "automatic_retries": 0,
        "behavioral_observations": 1 if output else 0,
        "runtime_envelope_bytes": case["envelope_bytes"],
        "runtime_envelope_sha256": case["envelope_sha256"],
        "request_body_sha256": sha256(encoded),
        "raw_provider_response_sha256": sha256(raw),
        "raw_output_bytes": len(output_bytes),
        "raw_output_sha256": sha256(output_bytes),
        "usage_metadata": payload.get("usage"),
        "evaluation_contract_sent": False,
        "expected_result_sent": False,
        "credential_value_recorded": False,
        "human_review_required": True,
        "automatic_semantic_judgement": False,
        "automatic_certification": False,
        "automatic_promotion": False,
        "state": "OBSERVED_HUMAN_REVIEW_REQUIRED" if output else "EMPTY_OUTPUT_HUMAN_REVIEW_REQUIRED",
    }
    write_json(out / "runtime-evidence.json", receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", required=True)
    args = parser.parse_args()

    try:
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
        output_root = Path(os.path.expandvars(os.path.expanduser(plan["output_root"]))).resolve()
    except Exception as exc:
        print(f"G09_BATCH_BLOCKED_PLAN_LOAD_FAILURE:{type(exc).__name__}")
        return 2

    preflight, cases, evaluations = load_and_preflight(output_root)
    print("=== ZERO-MODEL G09 PREFLIGHT ===")
    print(json.dumps(preflight, ensure_ascii=False, indent=2, sort_keys=True))
    if preflight["verdict"] != "PASS":
        print("G09_BATCH_BLOCKED_AUTHORIZATION_NOT_CONSUMED")
        return 2

    if args.authorization.strip() != EXACT_AUTH:
        print("G09_BATCH_BLOCKED_EXACT_AUTHORIZATION_MISSING")
        return 2

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("G09_BATCH_BLOCKED_OPENAI_API_KEY_MISSING_AUTHORIZATION_NOT_CONSUMED")
        return 2

    output_root.mkdir(parents=True, exist_ok=False)
    write_json(output_root / "preflight.json", preflight)
    batch_started = now()
    receipts: list[dict] = []
    review_cases: list[dict] = []

    for index, (case, evaluation) in enumerate(zip(cases, evaluations), start=1):
        case_out = output_root / f"{index:02d}-{case['case_id']}"
        receipt = request_case(case, key, case_out)
        receipts.append(receipt)
        raw_path = case_out / "raw-output.md"
        raw_output = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
        review_cases.append({
            "order": index,
            "case_id": case["case_id"],
            "evaluation_contract": evaluation,
            "runtime_evidence": receipt,
            "raw_output": raw_output,
        })

    summary = {
        "schema": "prompt-machine-starter-n09-g09-portability-batch-runtime-summary-v1",
        "gate": "G09_PORTABILITY",
        "batch_id": BATCH_ID,
        "provider": PROVIDER,
        "model_family": MODEL_FAMILY,
        "model": MODEL,
        "started_at": batch_started,
        "completed_at": now(),
        "authorization_consumed": True,
        "provider_requests_attempted": sum(int(r.get("provider_requests_attempted", 0)) for r in receipts),
        "maximum_provider_requests_authorized": 4,
        "automatic_retries": 0,
        "cases_attempted": len(receipts),
        "behavioral_observations": sum(int(r.get("behavioral_observations", 0)) for r in receipts),
        "human_review_required": True,
        "automatic_semantic_judgement": False,
        "automatic_certification": False,
        "automatic_promotion": False,
        "g09_claim": "NONE_UNTIL_BATCH_HUMAN_REVIEW",
        "case_receipts": receipts,
    }
    write_json(output_root / "batch-summary.json", summary)

    bundle = {
        "schema": "prompt-machine-starter-n09-g09-portability-human-review-bundle-v1",
        "gate": "G09_PORTABILITY",
        "batch_id": BATCH_ID,
        "provider": PROVIDER,
        "model_family": MODEL_FAMILY,
        "model": MODEL,
        "provider_requests_attempted_by_review_bundle": 0,
        "model_inference_requests_attempted_by_review_bundle": 0,
        "review_rule": "Evaluate each case only against its predeclared frozen evaluation contract. Four clean observations plus four PASS reviews are required for baseline G09 portability PASS. Any blocking semantic failure => G09 REWORK. Provider/transport failure without output => NO_OBSERVATION, not workflow FAIL.",
        "claim_boundary_if_all_pass": "PORTABILITY_OBSERVED_ACROSS_TWO_MODEL_FAMILIES_ONLY",
        "cases": review_cases,
    }
    write_json(output_root / "human-review-bundle.json", bundle)

    print("=== G09 BATCH RUNTIME SUMMARY ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    print("=== G09 HUMAN REVIEW BUNDLE ===")
    print(json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"G09_BATCH_OUTPUT_ROOT={output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
