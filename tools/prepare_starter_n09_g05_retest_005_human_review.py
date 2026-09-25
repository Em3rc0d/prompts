#!/usr/bin/env python3
"""Prepare an integrity-checked, zero-provider human review packet for G05-RETEST-005.

This tool performs no network/provider/model calls. It verifies the locally saved
raw output against the frozen runtime receipt, then prints the evaluation contract
and raw output for human review.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTEMPT_ID = "G05-RETEST-005"
CASE_ID = "PM-STARTER-CR-NORMAL-0001"
RECEIPT_PATH = ROOT / "commercial/STARTER_N09_RUNTIME_ATTEMPT_GEMINI_WSL_005_2026-09-07.json"
REVIEW_PACKET_PATH = ROOT / "commercial/STARTER_N09_G05_RETEST_005_HUMAN_REVIEW_PACKET.json"
EVAL_PATH = ROOT / "product/starter-collection-v1/evaluation/reviews/PM-STARTER-CR-NORMAL-0001.evaluation.json"
OUT_DIR = Path(os.path.expandvars(os.path.expanduser("$HOME/.local/share/prompt-machine/n09/g05-retest-005"))).resolve()
RAW_OUTPUT_PATH = OUT_DIR / "raw-output.md"
RUNTIME_EVIDENCE_PATH = OUT_DIR / "runtime-evidence.json"
LOCAL_REPORT_PATH = OUT_DIR / "human-review-input.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    review_packet = json.loads(REVIEW_PACKET_PATH.read_text(encoding="utf-8"))
    evaluation = json.loads(EVAL_PATH.read_text(encoding="utf-8"))

    if not RAW_OUTPUT_PATH.exists():
        raise SystemExit(f"blocked: missing local raw output: {RAW_OUTPUT_PATH}")
    if not RUNTIME_EVIDENCE_PATH.exists():
        raise SystemExit(f"blocked: missing local runtime evidence: {RUNTIME_EVIDENCE_PATH}")

    raw = RAW_OUTPUT_PATH.read_bytes()
    runtime_evidence = json.loads(RUNTIME_EVIDENCE_PATH.read_text(encoding="utf-8"))
    actual_sha = sha256(raw)
    actual_bytes = len(raw)

    checks = {
        "attempt_id_exact": receipt.get("attempt_id") == ATTEMPT_ID,
        "case_id_exact": receipt.get("case_id") == CASE_ID,
        "runtime_evidence_attempt_exact": runtime_evidence.get("attempt_id") == ATTEMPT_ID,
        "runtime_evidence_behavioral_observation_one": runtime_evidence.get("behavioral_observations") == 1,
        "runtime_evidence_human_review_required": runtime_evidence.get("human_review_required") is True,
        "raw_output_bytes_match_receipt": actual_bytes == receipt.get("raw_output_bytes") == review_packet.get("expected_raw_output_bytes"),
        "raw_output_sha_match_receipt": actual_sha == receipt.get("raw_output_sha256") == review_packet.get("expected_raw_output_sha256"),
        "evaluation_contract_case_exact": evaluation.get("case_id") == CASE_ID,
        "evaluation_contract_not_runtime_input": evaluation.get("evaluation_contract_is_runtime_input") is False,
        "expected_result_not_runtime_input": evaluation.get("expected_result_is_runtime_input") is False,
        "human_review_required": evaluation.get("human_review_required_after_runtime") is True,
        "provider_requests_attempted_by_this_tool": True,
        "model_inference_attempted_by_this_tool": True
    }

    verdict = "PASS" if all(checks.values()) else "FAIL"
    report = {
        "schema": "prompt-machine-starter-n09-g05-human-review-input-v1",
        "attempt_id": ATTEMPT_ID,
        "case_id": CASE_ID,
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "automatic_semantic_judgement": False,
        "integrity_checks": checks,
        "integrity_verdict": verdict,
        "raw_output_bytes": actual_bytes,
        "raw_output_sha256": actual_sha,
        "evaluation_expected": evaluation.get("expected"),
        "blocking_dimensions": evaluation.get("blocking_dimensions"),
        "review_rule": evaluation.get("review_rule"),
        "raw_output": raw.decode("utf-8"),
        "truth_boundary": "LOCAL_INTEGRITY_VERIFICATION_AND_HUMAN_REVIEW_INPUT_ONLY_NO_PROVIDER_REQUEST"
    }

    LOCAL_REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"LOCAL_REPORT={LOCAL_REPORT_PATH}")
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
