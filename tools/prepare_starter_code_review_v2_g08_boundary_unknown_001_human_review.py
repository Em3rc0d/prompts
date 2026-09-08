#!/usr/bin/env python3
"""Prepare an integrity-checked, zero-provider human review input for G08 v2 case #1."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001"
EXECUTION_ID = "PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001-GEMINI-WSL-54994A901604"
REPO_RECEIPT_PATH = ROOT / "commercial/STARTER_N09_G08_V2_BOUNDARY_UNKNOWN_001_RUNTIME_RECEIPT_2026-09-07.json"
PACKET_PATH = ROOT / "commercial/STARTER_N09_G08_V2_BOUNDARY_UNKNOWN_001_HUMAN_REVIEW_PACKET.json"
EVAL_PATH = ROOT / "product/starter-collection-v2/evaluation/reviews/PM-STARTER-CR-V2-BOUNDARY-UNKNOWN-0001.evaluation.json"
OUT_DIR = Path(os.path.expandvars(os.path.expanduser("$HOME/.local/share/prompt-machine/n09/g08-v2-boundary-unknown-001"))).resolve()
RAW_OUTPUT_PATH = OUT_DIR / "raw-output.md"
RUNTIME_EVIDENCE_PATH = OUT_DIR / "runtime-evidence.json"
LOCAL_REVIEW_PACKET_PATH = OUT_DIR / "review-packet.json"
LOCAL_REPORT_PATH = OUT_DIR / "human-review-input.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    repo_receipt = json.loads(REPO_RECEIPT_PATH.read_text(encoding="utf-8"))
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    evaluation = json.loads(EVAL_PATH.read_text(encoding="utf-8"))

    for path in (RAW_OUTPUT_PATH, RUNTIME_EVIDENCE_PATH, LOCAL_REVIEW_PACKET_PATH):
        if not path.exists():
            raise SystemExit(f"blocked: missing local runtime artifact: {path}")

    raw = RAW_OUTPUT_PATH.read_bytes()
    runtime = json.loads(RUNTIME_EVIDENCE_PATH.read_text(encoding="utf-8"))
    local_packet = json.loads(LOCAL_REVIEW_PACKET_PATH.read_text(encoding="utf-8"))
    actual_bytes = len(raw)
    actual_sha = sha256(raw)

    checks = {
        "repo_receipt_case_exact": repo_receipt.get("case_id") == CASE_ID,
        "repo_receipt_execution_exact": repo_receipt.get("execution_id") == EXECUTION_ID,
        "repo_receipt_behavioral_observation_one": repo_receipt.get("behavioral_observations") == 1,
        "repo_receipt_human_review_required": repo_receipt.get("human_review_required") is True,
        "repo_receipt_authorization_consumed": repo_receipt.get("authorization_consumed") is True,
        "runtime_case_exact": runtime.get("case_id") == CASE_ID,
        "runtime_execution_exact": runtime.get("execution_id") == EXECUTION_ID,
        "runtime_behavioral_observation_one": runtime.get("behavioral_observations") == 1,
        "runtime_human_review_required": runtime.get("human_review_required") is True,
        "runtime_no_automatic_next_case": runtime.get("automatic_next_case") is False,
        "runtime_evaluation_not_sent": runtime.get("evaluation_contract_sent") is False,
        "runtime_expected_result_not_sent": runtime.get("expected_result_sent") is False,
        "runtime_finish_reason_matches": runtime.get("finish_reasons") == packet.get("observed_finish_reasons"),
        "raw_output_bytes_match": actual_bytes == repo_receipt.get("raw_output_bytes") == packet.get("expected_raw_output_bytes") == local_packet.get("raw_output_bytes"),
        "raw_output_sha_match": actual_sha == repo_receipt.get("raw_output_sha256") == packet.get("expected_raw_output_sha256") == local_packet.get("raw_output_sha256"),
        "runtime_envelope_bytes_match": runtime.get("runtime_envelope_bytes") == packet.get("expected_runtime_envelope_bytes"),
        "runtime_envelope_sha_match": runtime.get("runtime_envelope_sha256") == packet.get("expected_runtime_envelope_sha256"),
        "evaluation_case_exact": evaluation.get("case_id") == CASE_ID,
        "evaluation_not_runtime_input": evaluation.get("evaluation_contract_is_runtime_input") is False,
        "expected_result_not_runtime_input": evaluation.get("expected_result_is_runtime_input") is False,
        "evaluation_predeclared": evaluation.get("predeclared_before_runtime") is True,
        "human_review_required_by_contract": evaluation.get("human_review_required_after_runtime") is True,
    }

    verdict = "PASS" if all(checks.values()) else "FAIL"
    report = {
        "schema": "prompt-machine-starter-n09-g08-v2-boundary-unknown-human-review-input-v1",
        "case_id": CASE_ID,
        "execution_id": EXECUTION_ID,
        "provider_requests_attempted": 0,
        "model_inference_requests_attempted": 0,
        "runtime_executions_attempted": 0,
        "automatic_semantic_judgement": False,
        "integrity_checks": checks,
        "integrity_verdict": verdict,
        "raw_output_bytes": actual_bytes,
        "raw_output_sha256": actual_sha,
        "finish_reasons": runtime.get("finish_reasons"),
        "max_tokens_interpretation": packet.get("max_tokens_interpretation"),
        "evaluation_expected": evaluation.get("expected"),
        "blocking_dimensions": evaluation.get("blocking_dimensions"),
        "review_rule": evaluation.get("review_rule"),
        "raw_output": raw.decode("utf-8"),
        "case_2_authorized": False,
        "truth_boundary": "LOCAL_INTEGRITY_VERIFICATION_AND_HUMAN_REVIEW_INPUT_ONLY; ZERO_PROVIDER_REQUEST; ZERO_MODEL_CALL; NO_AUTOMATIC_NEXT_CASE"
    }

    LOCAL_REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"LOCAL_REPORT={LOCAL_REPORT_PATH}")
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
