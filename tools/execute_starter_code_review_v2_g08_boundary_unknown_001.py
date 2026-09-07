#!/usr/bin/env python3
"""Execute exactly one governed G08 v2 BOUNDARY-UNKNOWN regression observation."""
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
CASE_ID = "PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001"
WORKFLOW_ID = "pm-starter-evidence-first-code-review-v2"
EXPECTED_MODEL = "gemini-3.5-flash"
EXPECTED_BYTES = 12008
EXPECTED_SHA = "72cfc51bca3b09d88f6230f51a706735ecb985b4c541093833c2ea64a10b6b92"
EXPECTED_MAX_OUTPUT_TOKENS = 4096
EXACT_AUTH = "AUTORIZO PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001: 1 ejecución, 0 reintentos."
PROVIDER = "GOOGLE_GEMINI_API"
SURFACE = "WSL_LOCAL_GEMINI_GENERATE_CONTENT_API"
CASE_PATH = ROOT / "product/starter-collection-v2/evaluation/cases/PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001.json"
EVAL_PATH = ROOT / "product/starter-collection-v2/evaluation/reviews/PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001.evaluation.json"
DESIGN_PATH = ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_DESIGN_V1.json"
FREEZE_PATH = ROOT / "commercial/STARTER_N09_G08_V2_REGRESSION_FREEZE_RECEIPT_2026-09-07.json"
PLAN_PATH = ROOT / "commercial/STARTER_N09_G08_V2_BOUNDARY_UNKNOWN_001_PLAN.json"
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
MODEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def assert_wsl() -> None:
    p = Path("/proc/version")
    text = p.read_text(errors="ignore").lower() if p.exists() else ""
    if "microsoft" not in text and "wsl" not in text:
        raise SystemExit("blocked: WSL could not be verified")


def frozen_case(freeze: dict) -> dict:
    matches = [x for x in freeze.get("frozen_cases", []) if x.get("case_id") == CASE_ID]
    if len(matches) != 1:
        raise SystemExit("blocked: frozen case missing or duplicated")
    return matches[0]


def load_contracts() -> tuple[bytes, dict, dict, dict, dict, dict]:
    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    evaluation = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    design = json.loads(DESIGN_PATH.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    frozen = frozen_case(freeze)
    order = design.get("execution_order") or []
    checks = {
        "case_id": case.get("case_id") == CASE_ID,
        "workflow_id": case.get("workflow_id") == WORKFLOW_ID,
        "eval_excluded": case.get("evaluation_contract_is_runtime_input") is False,
        "evaluation_case": evaluation.get("case_id") == CASE_ID,
        "evaluation_not_runtime": evaluation.get("evaluation_contract_is_runtime_input") is False,
        "expected_not_runtime": evaluation.get("expected_result_is_runtime_input") is False,
        "freeze_pass": freeze.get("verdict") == "PASS",
        "frozen_bytes": frozen.get("runtime_envelope_bytes") == EXPECTED_BYTES,
        "frozen_sha": frozen.get("runtime_envelope_sha256") == EXPECTED_SHA,
        "first_case_only": len(order) >= 1 and order[0] == CASE_ID,
        "design_single_request": design.get("runtime_governance", {}).get("maximum_provider_requests_per_authorization") == 1,
        "design_zero_retries": design.get("runtime_governance", {}).get("automatic_retries") == 0,
        "design_no_next": design.get("runtime_governance", {}).get("automatic_next_case") is False,
        "plan_state": plan.get("state") == "PREPARED_ZERO_MODEL_PREFLIGHT_REQUIRED",
        "plan_model": plan.get("model") == EXPECTED_MODEL,
        "plan_single_request": plan.get("maximum_provider_requests") == 1,
        "plan_zero_retries": plan.get("automatic_retries") == 0,
        "plan_no_next": plan.get("automatic_next_case") is False,
        "plan_eval_excluded": plan.get("evaluation_contract_is_runtime_input") is False,
        "local_only": policy.get("policy_state") == "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER",
        "provider": policy.get("inference_provider") == PROVIDER,
    }
    bad = [k for k, v in checks.items() if not v]
    if bad:
        raise SystemExit("blocked: contract drift: " + ", ".join(bad))
    workflow = (ROOT / case["workflow_surface_path"]).read_text(encoding="utf-8")
    envelope = render(workflow, case["instance_data_markdown"])
    if len(envelope) != EXPECTED_BYTES or sha(envelope) != EXPECTED_SHA:
        raise SystemExit("blocked: frozen v2 runtime envelope drifted")
    eval_bytes = EVAL_PATH.read_bytes()
    if eval_bytes in envelope:
        raise SystemExit("blocked: evaluation contract leaked into runtime input")
    if any(x in envelope for x in (b'"expected"', b'"blocking_dimensions"', b'expected_result_is_runtime_input')):
        raise SystemExit("blocked: evaluation markers leaked into runtime input")
    return envelope, case, evaluation, design, freeze, plan


def extract_text(payload: dict) -> str:
    chunks: list[str] = []
    for candidate in payload.get("candidates") or []:
        for part in (candidate.get("content") or {}).get("parts") or []:
            if isinstance(part.get("text"), str) and part["text"]:
                chunks.append(part["text"])
    return "\n".join(chunks).strip()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--authorization", required=True)
    args = p.parse_args()

    assert_wsl()
    if args.authorization.strip() != EXACT_AUTH:
        raise SystemExit("blocked: fresh exact case authorization missing")
    if args.model != EXPECTED_MODEL or not MODEL_RE.fullmatch(args.model):
        raise SystemExit("blocked: model differs from frozen case plan")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("blocked before provider use: GEMINI_API_KEY missing")

    envelope, case, evaluation, design, freeze, plan = load_contracts()
    out = args.output_dir.expanduser().resolve()
    planned = Path(os.path.expandvars(os.path.expanduser(plan["output_directory"]))).resolve()
    if out != planned:
        raise SystemExit("blocked: output directory differs from frozen case plan")
    if out.exists():
        raise SystemExit("blocked: output directory already exists")
    out.mkdir(parents=True)

    execution_id = f"{CASE_ID}-GEMINI-WSL-{secrets.token_hex(6).upper()}"
    started_at = now()
    body = {
        "contents": [{"role": "user", "parts": [{"text": envelope.decode("utf-8")}]}],
        "generationConfig": {"maxOutputTokens": EXPECTED_MAX_OUTPUT_TOKENS},
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + urllib.parse.quote(args.model, safe="") + ":generateContent"
    req = urllib.request.Request(endpoint, data=encoded, method="POST", headers={"x-goog-api-key": key, "Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=240) as response:
            raw = response.read()
            status = response.status
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        receipt = {
            "schema": "prompt-machine-starter-n09-g08-v2-boundary-unknown-001-failure-v1",
            "case_id": CASE_ID,
            "execution_id": execution_id,
            "provider": PROVIDER,
            "model_requested": args.model,
            "started_at": started_at,
            "failed_at": now(),
            "http_status": exc.code,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "automatic_next_case": False,
            "behavioral_observations": 0,
            "runtime_envelope_bytes": EXPECTED_BYTES,
            "runtime_envelope_sha256": EXPECTED_SHA,
            "request_body_sha256": sha(encoded),
            "response_body_sha256": sha(raw),
            "state": "PROVIDER_FAILURE_NO_RETRY_STOP_G08_SEQUENCE_HUMAN_REVIEW_REQUIRED",
        }
        (out / "raw-provider-error.bin").write_bytes(raw)
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 2
    except Exception as exc:
        receipt = {
            "schema": "prompt-machine-starter-n09-g08-v2-boundary-unknown-001-transport-failure-v1",
            "case_id": CASE_ID,
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "automatic_next_case": False,
            "behavioral_observations": 0,
            "error_type": type(exc).__name__,
            "state": "TRANSPORT_FAILURE_NO_RETRY_STOP_G08_SEQUENCE_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 2

    (out / "raw-provider-response.json").write_bytes(raw)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        receipt = {
            "schema": "prompt-machine-starter-n09-g08-v2-boundary-unknown-001-invalid-response-v1",
            "case_id": CASE_ID,
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "automatic_next_case": False,
            "behavioral_observations": 0,
            "http_status": status,
            "raw_provider_response_sha256": sha(raw),
            "state": "INVALID_PROVIDER_RESPONSE_STOP_G08_SEQUENCE_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 3

    output = extract_text(payload)
    if not output:
        receipt = {
            "schema": "prompt-machine-starter-n09-g08-v2-boundary-unknown-001-empty-output-v1",
            "case_id": CASE_ID,
            "execution_id": execution_id,
            "provider_requests_attempted": 1,
            "automatic_retries": 0,
            "automatic_next_case": False,
            "behavioral_observations": 0,
            "http_status": status,
            "finish_reasons": [c.get("finishReason") for c in payload.get("candidates") or []],
            "raw_provider_response_sha256": sha(raw),
            "state": "EMPTY_OUTPUT_STOP_G08_SEQUENCE_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "receipt.json", receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 3

    raw_output = output.encode("utf-8")
    (out / "raw-output.md").write_bytes(raw_output)
    evidence = {
        "schema": "prompt-machine-starter-n09-g08-v2-regression-observation-v1",
        "version": "1.0.0",
        "case_id": CASE_ID,
        "workflow_id": WORKFLOW_ID,
        "execution_id": execution_id,
        "regression_order_position": 1,
        "provider": PROVIDER,
        "execution_surface": SURFACE,
        "execution_location": "USER_WSL",
        "model_requested": args.model,
        "provider_model_version": payload.get("modelVersion"),
        "provider_response_id": payload.get("responseId"),
        "runtime_envelope_bytes": EXPECTED_BYTES,
        "runtime_envelope_sha256": EXPECTED_SHA,
        "started_at": started_at,
        "completed_at": now(),
        "http_status": status,
        "request_id": headers.get("x-request-id") or headers.get("X-Request-Id"),
        "provider_requests_attempted": 1,
        "automatic_retries": 0,
        "automatic_next_case": False,
        "behavioral_observations": 1,
        "finish_reasons": [c.get("finishReason") for c in payload.get("candidates") or []],
        "raw_output_sha256": sha(raw_output),
        "raw_output_bytes": len(raw_output),
        "raw_provider_response_sha256": sha(raw),
        "request_body_sha256": sha(encoded),
        "usage_metadata": payload.get("usageMetadata"),
        "credential_value_recorded": False,
        "evaluation_contract_sent": False,
        "expected_result_sent": False,
        "human_review_required": True,
        "automatic_semantic_judgement": False,
        "automatic_certification": False,
        "automatic_promotion": False,
        "next_case_authorized": False,
        "state": "CLEAN_G08_V2_BOUNDARY_UNKNOWN_OBSERVED_HUMAN_REVIEW_REQUIRED",
    }
    write_json(out / "runtime-evidence.json", evidence)
    write_json(out / "review-packet.json", {
        "schema": "prompt-machine-starter-n09-g08-v2-human-review-packet-v1",
        "case_id": CASE_ID,
        "execution_id": execution_id,
        "evaluation_contract": str(EVAL_PATH.relative_to(ROOT)),
        "raw_output_sha256": evidence["raw_output_sha256"],
        "raw_output_bytes": evidence["raw_output_bytes"],
        "review_status": "HUMAN_REVIEW_REQUIRED",
        "automatic_next_case": False,
        "g08_claim": "NONE_UNTIL_HUMAN_REVIEW",
    })
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
