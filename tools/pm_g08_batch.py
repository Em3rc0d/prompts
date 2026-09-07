#!/usr/bin/env python3
"""Run the frozen G08 v2 regression matrix as one governed local batch.

One invocation performs zero-model integrity checks first. Only if every preflight
check passes and the exact batch authorization is supplied may the runner issue
up to one Gemini request per frozen case, in order, with zero retries.
Evaluation contracts are never sent to the model; they are attached only to the
local post-run human-review bundle.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "PM-STARTER-CR-V2-G08-BATCH-0001"
WORKFLOW_ID = "pm-starter-evidence-first-code-review-v2"
MODEL = "gemini-3.5-flash"
MAX_OUTPUT_TOKENS = 4096
THINKING_LEVEL = "minimal"
EXACT_AUTH = "AUTORIZO PM-STARTER-CR-V2-G08-BATCH-0001: hasta 4 ejecuciones, 0 reintentos por caso."
PLAN = ROOT / "commercial/STARTER_N09_G08_V2_BATCH_0001_PLAN.json"
DESIGN = ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_DESIGN_V1.json"
FREEZE = ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_FREEZE_RECEIPT_2026-09-07.json"
PROVIDER = "GOOGLE_GEMINI_API"
MODEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def norm(s: str) -> str:
    return s.rstrip("\n") + "\n"


def render(surface: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + norm(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + norm(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def assert_wsl() -> bool:
    p = Path("/proc/version")
    text = p.read_text(errors="ignore").lower() if p.exists() else ""
    return "microsoft" in text or "wsl" in text


def extract_text(payload: dict) -> str:
    chunks: list[str] = []
    for candidate in payload.get("candidates") or []:
        for part in (candidate.get("content") or {}).get("parts") or []:
            if isinstance(part.get("text"), str) and part["text"]:
                chunks.append(part["text"])
    return "\n".join(chunks).strip()


def load_and_preflight(output_root: Path) -> tuple[dict, list[dict], list[dict]]:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    cases = plan.get("cases") or []
    order = design.get("execution_order") or []
    frozen = {x.get("case_id"): x for x in freeze.get("frozen_cases") or []}

    checks = {
        "wsl_detected": assert_wsl(),
        "gemini_api_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "batch_id_exact": plan.get("batch_id") == BATCH_ID,
        "batch_not_authorized_in_repo": plan.get("state") == "PREPARED_NOT_AUTHORIZED",
        "workflow_id_exact": plan.get("workflow_id") == WORKFLOW_ID,
        "model_exact": plan.get("model") == MODEL,
        "model_syntax_valid": bool(MODEL_RE.fullmatch(MODEL)),
        "four_cases_exact": len(cases) == 4 and len(set(cases)) == 4,
        "execution_order_exact": cases == order,
        "freeze_pass": freeze.get("verdict") == "PASS",
        "max_total_requests_four": plan.get("maximum_provider_requests_total") == 4,
        "one_request_per_case": plan.get("maximum_provider_requests_per_case") == 1,
        "zero_retries": plan.get("automatic_retries_per_case") == 0,
        "human_review_after_batch": plan.get("human_review_timing") == "AFTER_BATCH",
        "evaluation_excluded": plan.get("evaluation_contract_is_runtime_input") is False,
        "expected_excluded": plan.get("expected_result_is_runtime_input") is False,
        "output_root_absent": not output_root.exists(),
    }

    prepared: list[dict] = []
    evaluations: list[dict] = []
    for case_id in cases:
        frozen_case = frozen.get(case_id)
        if not frozen_case:
            checks[f"{case_id}:frozen"] = False
            continue
        case_path = ROOT / frozen_case["case_path"]
        eval_path = ROOT / frozen_case["evaluation_path"]
        case = json.loads(case_path.read_text(encoding="utf-8"))
        evaluation = json.loads(eval_path.read_text(encoding="utf-8"))
        workflow_path = ROOT / case["workflow_surface_path"]
        workflow = workflow_path.read_text(encoding="utf-8")
        envelope = render(workflow, case["instance_data_markdown"])
        envelope_sha = sha(envelope)
        envelope_bytes = len(envelope)
        prefix = case_id + ":"
        checks[prefix + "case_id"] = case.get("case_id") == case_id
        checks[prefix + "workflow_id"] = case.get("workflow_id") == WORKFLOW_ID
        checks[prefix + "runtime_not_preexecuted_fixture"] = case.get("runtime_executed") is False
        checks[prefix + "eval_excluded_fixture"] = case.get("evaluation_contract_is_runtime_input") is False
        checks[prefix + "evaluation_case"] = evaluation.get("case_id") == case_id
        checks[prefix + "evaluation_predeclared"] = evaluation.get("predeclared_before_runtime") is True
        checks[prefix + "evaluation_not_runtime"] = evaluation.get("evaluation_contract_is_runtime_input") is False
        checks[prefix + "expected_not_runtime"] = evaluation.get("expected_result_is_runtime_input") is False
        checks[prefix + "envelope_bytes"] = envelope_bytes == frozen_case.get("runtime_envelope_bytes")
        checks[prefix + "envelope_sha"] = envelope_sha == frozen_case.get("runtime_envelope_sha256")
        eval_bytes = eval_path.read_bytes()
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

    failed = [name for name, ok in checks.items() if not ok]
    report = {
        "schema": "prompt-machine-starter-n09-g08-v2-batch-preflight-v1",
        "batch_id": BATCH_ID,
        "recorded_at": now(),
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "runtime_executions_attempted": 0,
        "checks": checks,
        "verdict": "PASS" if not failed else "FAIL",
        "failed_checks": failed,
        "authorization_not_consumed_during_preflight": True,
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
    execution_id = f"{case_id}-G08-BATCH-0001-{secrets.token_hex(6).upper()}"
    started_at = now()
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
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "http_status": exc.code,
            "behavioral_observations": 0,
            "response_body_sha256": sha(raw),
            "state": "PROVIDER_FAILURE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        write_json(out / "runtime-evidence.json", receipt)
        return receipt
    except Exception as exc:
        receipt = {
            "case_id": case_id,
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "error_type": type(exc).__name__,
            "state": "TRANSPORT_FAILURE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        write_json(out / "runtime-evidence.json", receipt)
        return receipt

    (out / "raw-provider-response.json").write_bytes(raw)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        receipt = {
            "case_id": case_id,
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "http_status": status,
            "behavioral_observations": 0,
            "raw_provider_response_sha256": sha(raw),
            "state": "INVALID_PROVIDER_RESPONSE_RECORDED_BATCH_CONTINUES_NO_RETRY",
        }
        write_json(out / "runtime-evidence.json", receipt)
        return receipt

    output = extract_text(payload)
    output_bytes = output.encode("utf-8")
    (out / "raw-output.md").write_bytes(output_bytes)
    receipt = {
        "schema": "prompt-machine-starter-n09-g08-v2-batch-case-observation-v1",
        "batch_id": BATCH_ID,
        "case_id": case_id,
        "execution_id": execution_id,
        "provider": PROVIDER,
        "model_requested": MODEL,
        "provider_model_version": payload.get("modelVersion"),
        "started_at": started_at,
        "completed_at": now(),
        "http_status": status,
        "provider_requests_attempted": 1,
        "automatic_retries": 0,
        "behavioral_observations": 1 if output else 0,
        "finish_reasons": [c.get("finishReason") for c in payload.get("candidates") or []],
        "runtime_envelope_bytes": case["envelope_bytes"],
        "runtime_envelope_sha256": case["envelope_sha256"],
        "request_body_sha256": sha(encoded),
        "raw_provider_response_sha256": sha(raw),
        "raw_output_bytes": len(output_bytes),
        "raw_output_sha256": sha(output_bytes),
        "usage_metadata": payload.get("usageMetadata"),
        "evaluation_contract_sent": False,
        "expected_result_sent": False,
        "human_review_required": True,
        "automatic_semantic_judgement": False,
        "automatic_promotion": False,
        "state": "OBSERVED_HUMAN_REVIEW_REQUIRED" if output else "EMPTY_OUTPUT_HUMAN_REVIEW_REQUIRED",
    }
    write_json(out / "runtime-evidence.json", receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", required=True)
    args = parser.parse_args()

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    output_root = Path(os.path.expandvars(os.path.expanduser(plan["output_root"]))).resolve()
    preflight, cases, evaluations = load_and_preflight(output_root)
    print("=== ZERO-MODEL PREFLIGHT ===")
    print(json.dumps(preflight, ensure_ascii=False, indent=2, sort_keys=True))
    if preflight["verdict"] != "PASS":
        print("BATCH_BLOCKED_AUTHORIZATION_NOT_CONSUMED")
        return 2

    if args.authorization.strip() != EXACT_AUTH:
        print("BATCH_BLOCKED_EXACT_AUTHORIZATION_MISSING")
        return 2

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("BATCH_BLOCKED_GEMINI_API_KEY_MISSING")
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
        "schema": "prompt-machine-starter-n09-g08-v2-batch-runtime-summary-v1",
        "batch_id": BATCH_ID,
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
        "g08_claim": "NONE_UNTIL_BATCH_HUMAN_REVIEW",
        "case_receipts": receipts,
    }
    write_json(output_root / "batch-summary.json", summary)
    bundle = {
        "schema": "prompt-machine-starter-n09-g08-v2-batch-human-review-bundle-v1",
        "batch_id": BATCH_ID,
        "provider_requests_attempted_by_review_bundle": 0,
        "model_inference_requests_attempted_by_review_bundle": 0,
        "review_rule": "Evaluate each case only against its predeclared evaluation contract. Any blocking dimension failure in any required regression case => G08 REWORK.",
        "cases": review_cases,
    }
    write_json(output_root / "human-review-bundle.json", bundle)

    print("=== BATCH RUNTIME SUMMARY ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    print("=== HUMAN REVIEW BUNDLE ===")
    print(json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"BATCH_OUTPUT_ROOT={output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
