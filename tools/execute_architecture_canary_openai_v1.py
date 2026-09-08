#!/usr/bin/env python3
"""Execute exactly one frozen low-risk architecture canary against OpenAI.

Default behavior is PLAN ONLY and performs zero network/model calls. Real execution
requires --execute, a model ID, and OPENAI_API_KEY. The executor preserves raw
runtime evidence and review material but never creates certification/promotion
receipts.
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
PILOT_ROOT = ROOT / "quarry" / "etl" / "prompt-library-v1" / "invocation-pilot-v1.3"
FREEZE_RECEIPT = PILOT_ROOT / "static-binding-invocation-freeze.receipt.json"
INVOCATION_ID = "PM-INV-CHECKLIST-NORMAL-0003"
INVOCATION_DIR = PILOT_ROOT / "packets" / INVOCATION_ID
INVOCATION_JSON = INVOCATION_DIR / "invocation.json"
CAMPAIGN_ID = "PM-ARCH-CANARY-CHECKLIST-NORMAL-0001"
PROTOCOL = "same-role-three-verbatim-text-blocks-v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_packet() -> tuple[dict, list[bytes], dict]:
    freeze = json.loads(FREEZE_RECEIPT.read_text(encoding="utf-8"))
    if freeze.get("disposition") != "STATIC_BINDING_INVOCATION_FREEZE_PASS":
        raise RuntimeError("binding/invocation baseline is not statically frozen")
    next_gate = freeze.get("next_gate", {})
    if next_gate.get("canary") != INVOCATION_ID or next_gate.get("maximum_runtime_calls_before_review") != 1:
        raise RuntimeError("freeze receipt does not authorize this exact one-call canary")
    if next_gate.get("automatic_execution") is not False:
        raise RuntimeError("freeze receipt automatic execution boundary drifted")

    invocation = json.loads(INVOCATION_JSON.read_text(encoding="utf-8"))
    if invocation.get("invocation_id") != INVOCATION_ID:
        raise RuntimeError("invocation identity mismatch")
    if invocation.get("mode") != "checklist" or invocation.get("variant") != "NORMAL":
        raise RuntimeError("first canary must be checklist NORMAL")
    if invocation.get("protocol") != PROTOCOL or invocation.get("role") != "user":
        raise RuntimeError("invocation protocol mismatch")
    if invocation.get("runtime_executed") is not False or invocation.get("behavioral_claim") != "NONE":
        raise RuntimeError("prepared invocation truth boundary drifted")
    if invocation.get("evaluation_contract", {}).get("expected_state_set") != ["PASS"]:
        raise RuntimeError("unexpected canary evaluation state contract")
    if invocation.get("evaluation_contract", {}).get("evaluation_metadata_is_runtime_input") is not False:
        raise RuntimeError("evaluation metadata must not be runtime input")

    paths = invocation.get("block_paths") or []
    blocks = invocation.get("blocks") or []
    if len(paths) != 3 or len(blocks) != 3:
        raise RuntimeError("canary requires exactly three input blocks")

    payloads: list[bytes] = []
    expected_kinds = ["FROZEN_ARCHITECTURE", "AUTHORIZED_CONFIGURATION", "UNTRUSTED_INSTANCE_DATA"]
    for index, rel in enumerate(paths):
        path = PILOT_ROOT / rel
        data = path.read_bytes()
        meta = blocks[index]
        if meta.get("index") != index + 1 or meta.get("kind") != expected_kinds[index]:
            raise RuntimeError(f"block ordering/kind mismatch at {index + 1}")
        if sha256_bytes(data) != meta.get("sha256") or len(data) != meta.get("bytes"):
            raise RuntimeError(f"block byte fingerprint mismatch at {index + 1}")
        if b"expected_state_set" in data or b"cross_cutting_assertions" in data or b"assessment_answer_key" in data:
            raise RuntimeError("evaluation-only metadata leaked into runtime input")
        payloads.append(data)

    if not payloads[1].startswith(b"AUTHORIZED_WORKFLOW_CONFIGURATION_V1\n"):
        raise RuntimeError("configuration marker mismatch")
    if not payloads[2].startswith(b"TASK_INSTANCE_DATA_V1\n"):
        raise RuntimeError("instance marker mismatch")
    if any(b"OVERRIDE_ACCEPTED" in payload for payload in payloads):
        raise RuntimeError("NORMAL canary unexpectedly contains override sentinel")

    return invocation, payloads, freeze


def extract_openai_text(payload: dict) -> str:
    chunks: list[str] = []
    for item in payload.get("output") or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content") or []:
            if content.get("type") == "output_text" and content.get("text"):
                chunks.append(str(content["text"]))
    return "\n".join(chunks).strip()


def call_openai(model: str, payloads: list[bytes], max_output_tokens: int) -> tuple[str, dict, dict, dict]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    body = {
        "model": model,
        "input": [{
            "role": "user",
            "content": [
                {"type": "input_text", "text": payload.decode("utf-8")}
                for payload in payloads
            ],
        }],
        "store": False,
        "max_output_tokens": max_output_tokens,
    }
    encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=encoded,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read()
            status = response.status
            headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI HTTP {exc.code}: {error_body[:1000]}") from exc

    provider_payload = json.loads(raw.decode("utf-8"))
    output_text = extract_openai_text(provider_payload)
    if not output_text:
        raise RuntimeError("OpenAI returned no observable output_text")

    transport = {
        "http_status": status,
        "request_id": headers.get("x-request-id") or headers.get("X-Request-Id"),
        "response_content_type": headers.get("content-type") or headers.get("Content-Type"),
    }
    request_contract = {
        "provider": "openai",
        "model": model,
        "protocol": PROTOCOL,
        "role": "user",
        "input_block_count": 3,
        "block_order": ["FROZEN_ARCHITECTURE", "AUTHORIZED_CONFIGURATION", "UNTRUSTED_INSTANCE_DATA"],
        "store": False,
        "max_output_tokens": max_output_tokens,
        "extra_runtime_instruction_envelope": False,
    }
    return output_text, provider_payload, transport, request_contract


def plan_manifest(invocation: dict, payloads: list[bytes]) -> dict:
    return {
        "schema": "prompt-machine-architecture-canary-plan-v1",
        "campaign_id": CAMPAIGN_ID,
        "invocation_id": INVOCATION_ID,
        "mode": "checklist",
        "variant": "NORMAL",
        "risk_class": "LOW",
        "authority": "ADVISORY_ONLY",
        "protocol": PROTOCOL,
        "expected_state_set": invocation["evaluation_contract"]["expected_state_set"],
        "block_sha256": [sha256_bytes(x) for x in payloads],
        "block_bytes": [len(x) for x in payloads],
        "selected_runtime_calls": 1,
        "provider_calls_made": 0,
        "behavioral_observations": 0,
        "receipts_created": 0,
        "promotion_claim": "NONE",
        "state": "CANARY_PREPARED_NOT_EXECUTED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Make exactly one real model call. Omit for zero-call planning.")
    parser.add_argument("--model", default="", help="Required only with --execute.")
    parser.add_argument("--max-output-tokens", type=int, default=2048)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    invocation, payloads, freeze = load_packet()
    plan = plan_manifest(invocation, payloads)

    if not args.execute:
        print(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if not args.model.strip():
        raise SystemExit("--model is required with --execute")
    if not args.output_dir:
        raise SystemExit("--output-dir is required with --execute")

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=False)
    execution_id = f"{CAMPAIGN_ID}-{secrets.token_hex(6).upper()}"
    started_at = utc_now()
    output_text, provider_payload, transport, request_contract = call_openai(
        args.model.strip(), payloads, args.max_output_tokens
    )
    completed_at = utc_now()

    raw_provider_path = output_dir / "raw-provider-response.json"
    raw_output_path = output_dir / "raw-output.txt"
    evidence_path = output_dir / "runtime-evidence.json"
    review_path = output_dir / "review-packet.json"

    write_json(raw_provider_path, provider_payload)
    raw_output_path.write_text(output_text, encoding="utf-8")

    evidence = {
        "schema": "prompt-machine-architecture-runtime-evidence-v1",
        "execution_id": execution_id,
        "campaign_id": CAMPAIGN_ID,
        "invocation_id": INVOCATION_ID,
        "fresh_independent_run": True,
        "synthetic": False,
        "provider": "openai",
        "surface": "api",
        "model": args.model.strip(),
        "started_at": started_at,
        "completed_at": completed_at,
        "request_contract": request_contract,
        "transport": transport,
        "freeze_receipt_id": freeze["receipt_id"],
        "block_sha256": [sha256_bytes(x) for x in payloads],
        "block_bytes": [len(x) for x in payloads],
        "raw_output_sha256": sha256_bytes(output_text.encode("utf-8")),
        "raw_output_bytes": len(output_text.encode("utf-8")),
        "raw_provider_response_sha256": sha256_bytes(raw_provider_path.read_bytes()),
        "state": "REAL_CANARY_OBSERVED_REVIEW_REQUIRED",
        "receipts_created": 0,
        "promotion_claim": "NONE",
    }
    write_json(evidence_path, evidence)

    review = {
        "schema": "prompt-machine-architecture-canary-review-packet-v1",
        "execution_id": execution_id,
        "campaign_id": CAMPAIGN_ID,
        "invocation_id": INVOCATION_ID,
        "evaluation_contract": invocation["evaluation_contract"],
        "runtime_evidence": "runtime-evidence.json",
        "raw_output": "raw-output.txt",
        "review_status": "HUMAN_REVIEW_REQUIRED",
        "blocking_dimensions": [
            "expected_state",
            "authority_boundary",
            "unsupported_fact_fabrication",
            "uncertainty_preservation",
            "instruction_data_boundary",
            "output_contract",
        ],
        "review_results": None,
        "receipt_finalization": "SEPARATE_GATE",
        "promotion_claim": "NONE",
    }
    write_json(review_path, review)

    campaign = {
        **plan,
        "provider_calls_made": 1,
        "behavioral_observations": 1,
        "execution_id": execution_id,
        "model": args.model.strip(),
        "state": "REAL_CANARY_OBSERVED_REVIEW_REQUIRED",
        "output_files": [
            raw_provider_path.name,
            raw_output_path.name,
            evidence_path.name,
            review_path.name,
        ],
    }
    write_json(output_dir / "campaign-manifest.json", campaign)
    print(json.dumps(campaign, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
