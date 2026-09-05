#!/usr/bin/env python3
"""Execute one clean Starter N09 observation from the user's WSL only.

Properties:
- exact case PM-STARTER-CR-NORMAL-0001
- exact 8,100-byte frozen envelope + SHA-256 gate
- one HTTP request maximum, zero retry loop
- no evaluation contract / answer key in runtime input
- evidence written only to a caller-supplied local WSL directory
- no GitHub artifact upload, no Vercel deployment, no promotion

The model itself is remote unless a future local-model surface is separately governed.
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
POLICY_PATH = ROOT / "commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json"
EXPECTED_SHA = "d8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207"
EXPECTED_BYTES = 8100
SURFACE = "WSL_LOCAL_SINGLE_REQUEST_RESPONSES_API"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize(text: str) -> str:
    return text.rstrip("\n") + "\n"


def render(surface: str, instance: str) -> bytes:
    return (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + normalize(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + normalize(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    ).encode("utf-8")


def assert_wsl() -> None:
    version = Path("/proc/version").read_text(encoding="utf-8", errors="ignore").lower()
    if "microsoft" not in version and "wsl" not in version:
        raise RuntimeError("blocked: this executor is WSL-local only")


def load_envelope() -> tuple[bytes, dict, dict, dict]:
    case = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    clean = json.loads(CLEAN_SURFACE_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    if case.get("case_id") != CASE_ID:
        raise RuntimeError("case identity mismatch")
    if case.get("evaluation_contract_is_runtime_input") is not False:
        raise RuntimeError("evaluation contract boundary drifted")
    if clean.get("automatic_retries") != 0:
        raise RuntimeError("clean-surface retry boundary drifted")
    if policy.get("policy_state") != "LOCAL_ONLY_UNTIL_EXPLICITLY_CHANGED_BY_USER":
        raise RuntimeError("local-only policy is not active")
    if policy.get("current_authorization_state") != "DISARMED_PREVIOUS_V3_AUTHORIZATION_CONSUMED":
        raise RuntimeError("repository policy must remain disarmed; runtime authorization is supplied separately")

    workflow = (ROOT / case["workflow_surface_path"]).read_text(encoding="utf-8")
    envelope = render(workflow, case["instance_data_markdown"])
    if len(envelope) != EXPECTED_BYTES:
        raise RuntimeError(f"envelope byte mismatch: {len(envelope)}")
    if sha256(envelope) != EXPECTED_SHA:
        raise RuntimeError("envelope SHA-256 mismatch")

    forbidden = [b"expected_state", b"blocking_dimensions", b"assessment_answer_key"]
    if any(marker in envelope for marker in forbidden):
        raise RuntimeError("evaluation-only material leaked into runtime input")
    return envelope, case, clean, policy


def extract_output(payload: dict) -> str:
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
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    args = parser.parse_args()

    assert_wsl()
    exact_auth = "AUTORIZO PM-STARTER-CR-NORMAL-0001: 1 ejecución, 0 reintentos."
    if args.authorization.strip() != exact_auth:
        raise SystemExit("blocked: fresh exact runtime authorization missing")

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("blocked before model use: OPENAI_API_KEY is not present in local WSL environment")

    envelope, case, clean, policy = load_envelope()
    out = args.output_dir.expanduser().resolve()
    if out.exists():
        raise SystemExit("blocked: output directory already exists")
    out.mkdir(parents=True)

    execution_id = f"PM-STARTER-CR-NORMAL-0001-WSL-{secrets.token_hex(6).upper()}"
    started_at = utc_now()
    body = {
        "model": args.model,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": envelope.decode("utf-8")}]}],
        "store": False,
        "max_output_tokens": args.max_output_tokens,
    }
    encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=encoded,
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )

    # Exactly one transport attempt. No retry loop exists below.
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            raw = response.read()
            http_status = response.status
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        failure = {
            "schema": "prompt-machine-starter-n09-wsl-local-failure-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "execution_surface": SURFACE,
            "model_requested": args.model,
            "started_at": started_at,
            "failed_at": utc_now(),
            "surface_submissions": 1,
            "provider_requests": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "http_status": exc.code,
            "runtime_envelope_bytes": EXPECTED_BYTES,
            "runtime_envelope_sha256": EXPECTED_SHA,
            "response_body_sha256": sha256(raw),
            "state": "LOCAL_WSL_PROVIDER_FAILURE_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        (out / "raw-provider-error.bin").write_bytes(raw)
        write_json(out / "receipt.json", failure)
        print(json.dumps({k: failure[k] for k in failure if k not in {"response_body"}}, indent=2, sort_keys=True))
        return 2
    except Exception as exc:
        failure = {
            "schema": "prompt-machine-starter-n09-wsl-local-failure-v1",
            "execution_id": execution_id,
            "case_id": CASE_ID,
            "execution_surface": SURFACE,
            "model_requested": args.model,
            "started_at": started_at,
            "failed_at": utc_now(),
            "surface_submissions": 1,
            "provider_requests": 1,
            "automatic_retries": 0,
            "behavioral_observations": 0,
            "runtime_envelope_bytes": EXPECTED_BYTES,
            "runtime_envelope_sha256": EXPECTED_SHA,
            "error_type": type(exc).__name__,
            "state": "LOCAL_WSL_TRANSPORT_FAILURE_NO_RETRY_HUMAN_REVIEW_REQUIRED",
        }
        write_json(out / "receipt.json", failure)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 2

    payload = json.loads(raw.decode("utf-8"))
    output = extract_output(payload)
    raw_output = output.encode("utf-8")
    (out / "raw-provider-response.json").write_bytes(raw)
    (out / "raw-output.md").write_bytes(raw_output)

    evidence = {
        "schema": "prompt-machine-starter-n09-wsl-local-observation-v1",
        "version": "1.0.0",
        "execution_id": execution_id,
        "case_id": CASE_ID,
        "workflow_id": case["workflow_id"],
        "execution_surface": SURFACE,
        "execution_location": "USER_WSL",
        "fresh_independent_surface": True,
        "evaluation_contract_is_runtime_input": False,
        "expected_result_is_runtime_input": False,
        "model_requested": args.model,
        "runtime_envelope_bytes": EXPECTED_BYTES,
        "runtime_envelope_sha256": EXPECTED_SHA,
        "started_at": started_at,
        "completed_at": utc_now(),
        "http_status": http_status,
        "request_id": headers.get("x-request-id") or headers.get("X-Request-Id"),
        "surface_submissions": 1,
        "provider_requests": 1,
        "automatic_retries": 0,
        "automatic_second_case": False,
        "raw_output_sha256": sha256(raw_output),
        "raw_output_bytes": len(raw_output),
        "raw_provider_response_sha256": sha256(raw),
        "github_artifact_uploaded": False,
        "vercel_deployment_created": False,
        "human_review_required": True,
        "automatic_promotion": False,
        "state": "CLEAN_LOCAL_WSL_RUNTIME_OBSERVED_HUMAN_REVIEW_REQUIRED",
        "clean_surface_contract_version": clean["version"],
        "local_policy_version": policy["version"],
    }
    write_json(out / "runtime-evidence.json", evidence)
    write_json(out / "review-packet.json", {
        "schema": "prompt-machine-starter-n09-wsl-local-review-packet-v1",
        "execution_id": execution_id,
        "case_id": CASE_ID,
        "review_status": "HUMAN_REVIEW_REQUIRED",
        "automatic_retry": False,
        "automatic_next_case": False,
        "promotion_claim": "NONE",
    })

    # Deliberately print metadata only; raw model output stays on local disk.
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
