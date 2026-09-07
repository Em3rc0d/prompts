#!/usr/bin/env python3
"""Inspect the saved raw response from PM-GEMINI-MINIMAL-GEN-CTRL-001.

This tool performs ZERO provider requests and ZERO model inference. It only parses
local evidence already produced by the governed control execution.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_RESPONSE_SHA256 = "a0e09bdc4945ea43069940f0d041a6b5f5e60cf18abcb38a76c1b6abc1435bf0"
CONTROL_ID = "PM-GEMINI-MINIMAL-GEN-CTRL-001"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--response",
        type=Path,
        default=Path.home() / ".local/share/prompt-machine/n09/provider-min-gen-001/raw-provider-response.bin",
    )
    args = p.parse_args()

    path = args.response.expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"blocked: saved provider response not found: {path}")

    raw = path.read_bytes()
    actual_sha = sha(raw)
    if actual_sha != EXPECTED_RESPONSE_SHA256:
        raise SystemExit(
            "blocked: saved response hash differs from observed control receipt: " + actual_sha
        )

    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise SystemExit(f"blocked: saved response is not valid UTF-8 JSON: {type(exc).__name__}")

    candidates = payload.get("candidates") or []
    candidate_summaries = []
    visible_text_parts = 0
    thought_parts = 0
    all_text_bytes = 0

    for index, candidate in enumerate(candidates):
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        part_summaries = []
        for part_index, part in enumerate(parts):
            text = part.get("text") if isinstance(part, dict) else None
            thought = bool(part.get("thought")) if isinstance(part, dict) else False
            if thought:
                thought_parts += 1
            if isinstance(text, str) and text:
                all_text_bytes += len(text.encode("utf-8"))
                if not thought:
                    visible_text_parts += 1
            part_summaries.append(
                {
                    "index": part_index,
                    "has_text": isinstance(text, str) and bool(text),
                    "text_bytes": len(text.encode("utf-8")) if isinstance(text, str) else 0,
                    "thought": thought,
                    "has_thought_signature": isinstance(part, dict) and bool(part.get("thoughtSignature")),
                }
            )
        candidate_summaries.append(
            {
                "index": index,
                "finish_reason": candidate.get("finishReason"),
                "finish_message": candidate.get("finishMessage"),
                "role": content.get("role"),
                "parts": part_summaries,
            }
        )

    usage = payload.get("usageMetadata") or {}
    report = {
        "schema": "prompt-machine-starter-n09-gemini-minimal-generation-control-raw-inspection-v1",
        "control_id": CONTROL_ID,
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "source_response_sha256": actual_sha,
        "source_response_bytes": len(raw),
        "model_version": payload.get("modelVersion"),
        "response_id": payload.get("responseId"),
        "candidate_count": len(candidates),
        "candidate_summaries": candidate_summaries,
        "visible_text_parts": visible_text_parts,
        "thought_parts": thought_parts,
        "all_text_bytes": all_text_bytes,
        "usage_metadata": {
            "prompt_token_count": usage.get("promptTokenCount"),
            "candidates_token_count": usage.get("candidatesTokenCount"),
            "thoughts_token_count": usage.get("thoughtsTokenCount"),
            "total_token_count": usage.get("totalTokenCount"),
        },
        "prompt_feedback": payload.get("promptFeedback"),
        "truth_boundary": "LOCAL_RAW_RESPONSE_INSPECTION_ONLY_NO_NEW_PROVIDER_REQUEST_NO_G05_EVIDENCE",
    }

    out = path.parent / "raw-response-inspection.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"LOCAL_REPORT={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
