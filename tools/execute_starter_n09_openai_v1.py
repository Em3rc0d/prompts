#!/usr/bin/env python3
"""Execute exactly one clean Starter N09 retest against OpenAI.

This executor is intentionally narrow:
- exact case: PM-STARTER-CR-NORMAL-0001
- exact frozen runtime envelope SHA-256
- one HTTP request maximum
- zero retries
- no evaluation contract in runtime input
- no automatic review, promotion, trust update, or release decision

The caller must provide OPENAI_API_KEY and an explicit model ID.
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
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PM-STARTER-CR-NORMAL-0001"
CASE_PATH = ROOT / "product/starter-collection-v1/evaluation/cases/PM-STARTER-CR-NORMAL-0001.json"
CLEAN_SURFACE_PATH = ROOT / "commercial/STARTER_CLEAN_RUNTIME_SURFACE_REQUIREMENTS_V1.json"
EXPECTED_ENVELOPE_SHA256 = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
EXPECTED_ENVELOPE_BYTES = 8100


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize_block(text: str) -> str:
    return text.rstrip("\n") + "\n"


def render(surface: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + normalize_block(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + normalize_block(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def load_frozen_envelope() -> tuple[bytes, dict, dict]:
    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    clean = json.loads(CLEAN_SURFACE_PATH.read_text(encoding="utf-8"))

    if case.get("case_id") != CASE_ID:
        raise RuntimeError("case identity mismatch")
    if case.get("evaluation_contract_is_runtime_input") is not False:
        raise RuntimeError("evaluation contract boundary drifted")
    if clean.get("requirement") != "CLEAN_INDEPENDENT_EXECUTION_SURFACE":
        raise RuntimeError("clean-surface contract drifted")
    if clean.get("same_candidate_retest_allowed") is not True:
        raise RuntimeError("same candidate retest is not allowed")
    if clean.get("automatic_retries") != 0:
        raise RuntimeError("retry boundary drifted")
    if CASE_ID not in clean.get("applies_to", []):
        raise RuntimeError("clean-surface contract does not apply to case")

    surface_path = ROOT / case["workflow_surface_path"]
    surface_text = surface_path.read_text(encoding="utf-8")
    envelope = render(surface_text, case["instance_data_markdown"])

    if len(envelope) != EXPECTED_ENVELOPE_BYTES:
        raise RuntimeError(f"runtime envelope byte mismatch: {len(envelope)}")
    if sha256_bytes(envelope) != EXPECTED_ENVELOPE_SHA256:
        raise RuntimeError("runtime envelope SHA-256 mismatch")
    if b"expected_state" in envelope or b"blocking_dimensions" in envelope or b"assessment_answer_key" in envelope:
        raise RuntimeError("evaluation-only material leaked into runtime envelope")

    return envelope, case, clean


def extract_output_text(payload: dict) -> str:
    chunks: list[str] = []
    for item in payload.get("output") or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content") or []:
            if content.get("type") == "output_text" and content.get("text"):
                chunks.append(str(content["text"]))
    return "\n".join(chunks).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    args = parser.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY missing: blocked before model use")

    envelope, case, clean = load_frozen_envelope()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=False)

    execution_id = f"PM-STARTER-CR-NORMAL-0001-CLEAN-{secrets.token_hex(6).upper()}"
    started_at = utc_now()

    body = {
        "model": args.model,
        "input": [{
            "role": "user",
            "content": [{"type": "input_text", "text": envelope.decode("utf-8")}],
        }],
        "store": False,
        "max_output_tokens": args.max_output_tokens,
    }
    encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request_body_sha256 = sha256_bytes(encoded)

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=encoded,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )

    # IMPORTANT: exactly one transport attempt. There is intentionally no retry loop.
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            raw = response.read()
            http_status = response.status
            response_headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        error_raw = exc.read()
        failure = {
            "schema": "prompt-machine-starter-clean-runtime-transport-failure-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "surface": "GITHUB_ACTIONS_EPHEMERAL_OPENAI_RESPONSES_API",
            "model": args.model,
            "started_at": started_at,
            "failed_at": utc_now(),
            "provider_calls_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "http_status": exc.code,
            "runtime_envelope_sha256": EXPECTED_ENVELOPE_SHA256,
            "runtime_envelope_bytes": EXPECTED_ENVELOPE_BYTES,
            "request_body_sha256": request_body_sha256,
            "error_body_sha256": sha256_bytes(error_raw),
            "state": "TRANSPORT_FAILED_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "transport-failure.json", failure)
        (out / "transport-error-body.txt").write_bytes(error_raw)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2
    except Exception as exc:
        failure = {
            "schema": "prompt-machine-starter-clean-runtime-local-failure-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "surface": "GITHUB_ACTIONS_EPHEMERAL_OPENAI_RESPONSES_API",
            "model": args.model,
            "started_at": started_at,
            "failed_at": utc_now(),
            "provider_calls_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "runtime_envelope_sha256": EXPECTED_ENVELOPE_SHA256,
            "runtime_envelope_bytes": EXPECTED_ENVELOPE_BYTES,
            "request_body_sha256": request_body_sha256,
            "error_type": type(exc).__name__,
            "state": "LOCAL_OR_TRANSPORT_FAILURE_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "transport-failure.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2

    completed_at = utc_now()
    provider_payload = json.loads(raw.decode("utf-8"))
    output_text = extract_output_text(provider_payload)
    if not output_text:
        failure = {
            "schema": "prompt-machine-starter-clean-runtime-empty-output-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "surface": "GITHUB_ACTIONS_EPHEMERAL_OPENAI_RESPONSES_API",
            "model": args.model,
            "started_at": started_at,
            "completed_at": completed_at,
            "provider_calls_attempted": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "http_status": http_status,
            "runtime_envelope_sha256": EXPECTED_ENVELOPE_SHA256,
            "runtime_envelope_bytes": EXPECTED_ENVELOPE_BYTES,
            "raw_provider_response_sha256": sha256_bytes(raw),
            "state": "EMPTY_OUTPUT_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "empty-output.json", failure)
        (out / "raw-provider-response.json").write_bytes(raw)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 3

    raw_output = output_text.encode("utf-8")
    (out / "raw-provider-response.json").write_bytes(raw)
    (out / "raw-output.md").write_bytes(raw_output)

    evidence = {
        "schema": "prompt-machine-starter-clean-runtime-observation-v1",
        "version": "1.0.0",
        "execution_id": execution_id,
        "case_id": CASE_ID,
        "workflow_id": case["workflow_id"],
        "execution_surface": "GITHUB_ACTIONS_EPHEMERAL_OPENAI_RESPONSES_API",
        "fresh_independent_surface": True,
        "evaluation_expectations_present_before_runtime": False,
        "evaluation_contract_is_runtime_input": False,
        "expected_result_is_runtime_input": False,
        "model_identity": args.model,
        "runtime_envelope_sha256": EXPECTED_ENVELOPE_SHA256,
        "runtime_envelope_bytes": EXPECTED_ENVELOPE_BYTES,
        "request_body_sha256": request_body_sha256,
        "started_at": started_at,
        "completed_at": completed_at,
        "http_status": http_status,
        "request_id": response_headers.get("x-request-id") or response_headers.get("X-Request-Id"),
        "provider_calls_attempted": 1,
        "submissions_observed": 1,
        "automatic_retries_observed": 0,
        "automatic_second_case_executed": False,
        "raw_output_sha256": sha256_bytes(raw_output),
        "raw_output_size_bytes": len(raw_output),
        "raw_provider_response_sha256": sha256_bytes(raw),
        "human_review_required": True,
        "automatic_promotion": False,
        "trust_history_updated": False,
        "release_gate_updated": False,
        "state": "CLEAN_RUNTIME_OBSERVED_HUMAN_REVIEW_REQUIRED",
        "clean_surface_contract_version": clean["version"],
    }
    write_json(out / "runtime-evidence.json", evidence)

    review_packet = {
        "schema": "prompt-machine-starter-clean-runtime-review-packet-v1",
        "execution_id": execution_id,
        "case_id": CASE_ID,
        "runtime_evidence": "runtime-evidence.json",
        "raw_output": "raw-output.md",
        "review_status": "HUMAN_REVIEW_REQUIRED",
        "review_result": None,
        "automatic_next_case": False,
        "automatic_retry": False,
        "promotion_claim": "NONE",
    }
    write_json(out / "review-packet.json", review_packet)

    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
