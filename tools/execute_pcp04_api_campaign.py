#!/usr/bin/env python3
"""Execute frozen PCP-04 work orders against one real API runtime.

This tool is deliberately execution-only. It verifies frozen prompt/input bytes,
preserves provider responses and verbatim model output, and prepares review
packets. It MUST NOT create PCP04 execution receipts or promotion claims; review
and receipt finalization are separate gates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import httpx

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORK_ORDERS = ROOT / "build" / "pcp04-work-orders"
PREP_RECEIPT = ROOT / "certification" / "receipts" / "pcp-04-work-orders.v1.json"
EXPECTED_PACKET_SHA = "9a4e3c87457295aa90f1280297d97270bb1e7ba0f0d92162b3d70dbc6aacd213"
PROVIDERS = {"openai", "anthropic", "gemini"}
PROTOCOL = "same-role-two-verbatim-text-blocks-v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def extract_openai_text(payload: dict) -> str:
    chunks: list[str] = []
    for item in payload.get("output") or []:
        if item.get("type") != "message":
            continue
        for content in item.get("content") or []:
            if content.get("type") == "output_text" and content.get("text"):
                chunks.append(str(content["text"]))
    return "\n".join(chunks).strip()


def extract_anthropic_text(payload: dict) -> str:
    return "\n".join(
        str(item.get("text"))
        for item in payload.get("content") or []
        if item.get("type") == "text" and item.get("text")
    ).strip()


def extract_gemini_text(payload: dict) -> str:
    chunks: list[str] = []
    for candidate in payload.get("candidates") or []:
        for part in (candidate.get("content") or {}).get("parts") or []:
            if part.get("text"):
                chunks.append(str(part["text"]))
    return "\n".join(chunks).strip()


def call_runtime(provider: str, model: str, prompt_text: str, input_text: str, max_output_tokens: int) -> tuple[str, dict, dict, dict]:
    """Send baseline + fixture as two same-role text blocks.

    This avoids silently upgrading the baseline to system/developer authority and
    keeps adversarial-input behavior representative of a customer-pasted prompt.
    """
    provider = provider.casefold().strip()
    if provider not in PROVIDERS:
        raise ValueError(f"unsupported provider: {provider}")

    with httpx.Client(timeout=180.0, follow_redirects=True) as client:
        if provider == "openai":
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("OPENAI_API_KEY is not configured")
            body = {
                "model": model,
                "input": [{
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt_text},
                        {"type": "input_text", "text": input_text},
                    ],
                }],
                "store": False,
                "max_output_tokens": max_output_tokens,
            }
            response = client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json=body,
            )
            response.raise_for_status()
            payload = response.json()
            text = extract_openai_text(payload)
        elif provider == "anthropic":
            key = os.environ.get("ANTHROPIC_API_KEY")
            if not key:
                raise RuntimeError("ANTHROPIC_API_KEY is not configured")
            body = {
                "model": model,
                "max_tokens": max_output_tokens,
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "text", "text": input_text},
                    ],
                }],
            }
            response = client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
                json=body,
            )
            response.raise_for_status()
            payload = response.json()
            text = extract_anthropic_text(payload)
        else:
            key = os.environ.get("GEMINI_API_KEY")
            if not key:
                raise RuntimeError("GEMINI_API_KEY is not configured")
            body = {
                "contents": [{
                    "role": "user",
                    "parts": [{"text": prompt_text}, {"text": input_text}],
                }],
                "generationConfig": {"maxOutputTokens": max_output_tokens},
            }
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{quote(model, safe='')}:generateContent"
            response = client.post(
                endpoint,
                headers={"x-goog-api-key": key, "Content-Type": "application/json"},
                json=body,
            )
            response.raise_for_status()
            payload = response.json()
            text = extract_gemini_text(payload)

    if not text:
        raise RuntimeError(f"{provider} returned no observable text output")

    transport = {
        "http_status": response.status_code,
        "request_id": response.headers.get("x-request-id") or response.headers.get("request-id") or response.headers.get("x-goog-request-id"),
        "response_content_type": response.headers.get("content-type"),
    }
    request_contract = {
        "protocol": PROTOCOL,
        "provider": provider,
        "model": model,
        "max_output_tokens": max_output_tokens,
        "store": False if provider == "openai" else None,
        "prompt_role": "user",
        "fixture_role": "user",
        "prompt_block_index": 1,
        "fixture_block_index": 2,
    }
    return text, payload, transport, request_contract


def ensure_work_orders(work_orders_dir: Path) -> dict:
    manifest_path = work_orders_dir / "manifest.json"
    if not manifest_path.is_file():
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "prepare_pcp04_work_orders.py"), "--output", str(work_orders_dir)],
            check=True,
            cwd=ROOT,
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("work_orders_jsonl_sha256") != EXPECTED_PACKET_SHA:
        raise RuntimeError("PCP-04 work-order packet fingerprint does not match frozen preparation receipt")
    prep = json.loads(PREP_RECEIPT.read_text(encoding="utf-8"))
    if prep.get("packet", {}).get("work_orders_jsonl_sha256") != EXPECTED_PACKET_SHA:
        raise RuntimeError("persisted PCP-04 preparation receipt fingerprint drifted")
    if manifest.get("required_execution_count") != 84 or manifest.get("work_order_count") != 70:
        raise RuntimeError("unexpected PCP-04 work-order cardinality")
    return manifest


def expand_execution_plan(work_orders_dir: Path) -> list[dict]:
    orders = [json.loads(line) for line in (work_orders_dir / "work-orders.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    plan: list[dict] = []
    for order in orders:
        repetitions = int(order["fixture"]["required_repetitions"])
        for repetition_index in range(1, repetitions + 1):
            plan.append({"order": order, "repetition_index": repetition_index})
    if len(plan) != 84:
        raise RuntimeError(f"expected 84 expanded executions, got {len(plan)}")
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Observe real PCP-04 API executions without fabricating review or promotion evidence.")
    parser.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    parser.add_argument("--model", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--work-orders-dir", type=Path, default=DEFAULT_WORK_ORDERS)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prompt-id")
    parser.add_argument("--case-class")
    parser.add_argument("--limit", type=int, default=0, help="0 means execute every selected observation")
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    args = parser.parse_args()

    if not args.campaign_id.startswith("PQ-PCP04-CAMPAIGN-"):
        raise SystemExit("campaign id must start with PQ-PCP04-CAMPAIGN-")
    if args.limit < 0:
        raise SystemExit("--limit cannot be negative")

    manifest = ensure_work_orders(args.work_orders_dir)
    plan = expand_execution_plan(args.work_orders_dir)
    if args.prompt_id:
        plan = [row for row in plan if row["order"]["prompt_id"] == args.prompt_id]
    if args.case_class:
        plan = [row for row in plan if row["order"]["fixture"]["case_class"] == args.case_class]
    if args.limit:
        plan = plan[: args.limit]
    if not plan:
        raise SystemExit("execution selection is empty")

    out = args.output_dir
    raw_dir = out / "raw"
    evidence_dir = out / "evidence"
    review_dir = out / "review"
    for path in (raw_dir, evidence_dir, review_dir):
        path.mkdir(parents=True, exist_ok=True)

    run_nonce = secrets.token_hex(8).upper()
    started_at = utc_now()
    observations: list[dict] = []

    for sequence, item in enumerate(plan, start=1):
        order = item["order"]
        repetition_index = item["repetition_index"]
        prompt_id = order["prompt_id"]
        case_id = order["fixture"]["case_id"]
        prompt_path = args.work_orders_dir / prompt_id / "prompt.txt"
        input_path = args.work_orders_dir / prompt_id / case_id / "input.txt"
        prompt_bytes = prompt_path.read_bytes()
        input_bytes = input_path.read_bytes()

        if sha256_bytes(prompt_bytes) != order["prompt"]["sha256"]:
            raise RuntimeError(f"prompt byte drift: {prompt_id}")
        if sha256_bytes(input_bytes) != order["fixture"]["input_sha256"]:
            raise RuntimeError(f"fixture input byte drift: {prompt_id}/{case_id}")

        execution_id = f"PCP04-{run_nonce}-{sequence:03d}-{prompt_id}-{case_id}-R{repetition_index}"
        observed_at_start = utc_now()
        text, provider_payload, transport, request_contract = call_runtime(
            args.provider,
            args.model,
            prompt_bytes.decode("utf-8"),
            input_bytes.decode("utf-8"),
            args.max_output_tokens,
        )
        observed_at = utc_now()

        raw_path = raw_dir / f"{execution_id}.txt"
        raw_path.write_text(text, encoding="utf-8")
        raw_sha = sha256_bytes(raw_path.read_bytes())

        evidence = {
            "schema": "prompt-quarry-pcp04-runtime-observation-v1",
            "campaign_id": args.campaign_id,
            "execution_id": execution_id,
            "work_order_id": order["work_order_id"],
            "prompt_id": prompt_id,
            "case_id": case_id,
            "case_class": order["fixture"]["case_class"],
            "repetition_index": repetition_index,
            "provider": args.provider,
            "surface": "api",
            "model_or_configuration": f"{args.model};family={args.family};protocol={PROTOCOL};max_output_tokens={args.max_output_tokens}",
            "protocol": request_contract,
            "started_at": observed_at_start,
            "observed_at": observed_at,
            "prompt_sha256": order["prompt"]["sha256"],
            "input_sha256": order["fixture"]["input_sha256"],
            "transport": transport,
            "provider_response_sha256": sha256_json(provider_payload),
            "provider_response": provider_payload,
            "raw_output_sha256": raw_sha,
            "fresh_independent_run": True,
            "synthetic": False,
            "behavioral_claim": "NONE_UNTIL_REVIEW",
        }
        evidence["evidence_sha256"] = sha256_json(evidence)
        evidence_path = evidence_dir / f"{execution_id}.json"
        write_json(evidence_path, evidence)

        assertions = sorted(set(order["evaluation_contract"]["matrix_special_assertions"]) | set(order["evaluation_contract"]["fixture_assertions"]))
        review_packet = {
            "schema": "prompt-quarry-pcp04-review-packet-v1",
            "campaign_id": args.campaign_id,
            "execution_id": execution_id,
            "work_order_id": order["work_order_id"],
            "prompt_id": prompt_id,
            "case_id": case_id,
            "case_class": order["fixture"]["case_class"],
            "repetition_index": repetition_index,
            "instructions": "Review the verbatim output against the frozen input and every blocking dimension/assertion. Do not infer PASS from execution success. Fill every status and evidence note before receipt finalization.",
            "prompt_path": str(prompt_path.relative_to(ROOT)),
            "input_path": str(input_path.relative_to(ROOT)),
            "raw_output_path": str(raw_path),
            "runtime_evidence_path": str(evidence_path),
            "blocking_dimensions": [
                {"dimension": dimension, "status": None, "evidence": None}
                for dimension in order["evaluation_contract"]["blocking_dimensions"]
            ],
            "special_assertions": [
                {"assertion": assertion, "result": None, "evidence": None}
                for assertion in assertions
            ],
            "outcome_signature": None,
            "unresolved_blocking_human_checks": len(order["evaluation_contract"]["blocking_dimensions"]) + len(assertions),
            "blocking_failures": [],
            "case_pass": None,
            "eligible_for_prompt_tested": False,
        }
        review_path = review_dir / f"{execution_id}.review.json"
        write_json(review_path, review_packet)

        observations.append({
            "sequence": sequence,
            "execution_id": execution_id,
            "work_order_id": order["work_order_id"],
            "prompt_id": prompt_id,
            "case_id": case_id,
            "case_class": order["fixture"]["case_class"],
            "repetition_index": repetition_index,
            "raw_output_path": str(raw_path),
            "raw_output_sha256": raw_sha,
            "runtime_evidence_path": str(evidence_path),
            "runtime_evidence_sha256": evidence["evidence_sha256"],
            "review_path": str(review_path),
        })
        print(f"OBSERVED {sequence}/{len(plan)} {execution_id}", flush=True)

    campaign_manifest = {
        "schema": "prompt-quarry-pcp04-unreviewed-api-campaign-v1",
        "campaign_id": args.campaign_id,
        "state": "REAL_EXECUTIONS_OBSERVED_REVIEW_REQUIRED",
        "provider": args.provider,
        "surface": "api",
        "model": args.model,
        "family": args.family,
        "runtime_protocol": PROTOCOL,
        "runtime_identity": f"{args.provider}|api|{args.model}|{args.family}|{PROTOCOL}|max_output_tokens={args.max_output_tokens}",
        "source_work_order_manifest": manifest["manifest_id"],
        "source_work_orders_jsonl_sha256": manifest["work_orders_jsonl_sha256"],
        "started_at": started_at,
        "completed_at": utc_now(),
        "selected_execution_count": len(plan),
        "full_campaign_required_execution_count": 84,
        "review_required": True,
        "receipts_created": 0,
        "promotion_claim": "NONE",
        "observations": observations,
    }
    campaign_manifest["manifest_sha256"] = sha256_json(campaign_manifest)
    write_json(out / "campaign.unreviewed.json", campaign_manifest)

    forbidden_receipts = list(out.rglob("receipt.json")) + list(out.rglob("*.receipt.json"))
    if forbidden_receipts:
        raise RuntimeError("execution-only tool created a forbidden receipt")

    print(json.dumps({
        "status": "REAL_EXECUTIONS_OBSERVED_REVIEW_REQUIRED",
        "campaign_id": args.campaign_id,
        "observed": len(plan),
        "receipts_created": 0,
        "promotion_claim": "NONE",
        "manifest": str(out / "campaign.unreviewed.json"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
