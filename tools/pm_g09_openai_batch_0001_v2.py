#!/usr/bin/env python3
"""Hardened entrypoint for G09 OpenAI portability BATCH-0001.

Adds an exact per-case envelope identity gate to the base OpenAI runner. The
four rendered runtime envelopes must match the byte counts and SHA-256 values
observed on the G08 BATCH-0003 PASS path before authorization can be consumed.
"""
from __future__ import annotations

import json
from pathlib import Path

import pm_g09_openai_batch_0001 as base

ENVELOPE_FREEZE = (
    base.ROOT
    / "commercial/STARTER_N09_G09_OPENAI_BATCH_0001_ENVELOPE_FREEZE.json"
)

_original_load_and_preflight = base.load_and_preflight


def load_and_preflight(output_root: Path):
    report, cases, evaluations = _original_load_and_preflight(output_root)
    checks = report.setdefault("checks", {})

    try:
        freeze = json.loads(ENVELOPE_FREEZE.read_text(encoding="utf-8"))
        expected = freeze.get("envelopes") or {}
        rendered = report.get("rendered_envelopes") or {}

        checks["g09_envelope_freeze_loadable"] = True
        checks["g09_envelope_freeze_batch_exact"] = (
            freeze.get("batch_id") == base.BATCH_ID
        )
        checks["g09_envelope_freeze_source_g08_pass"] = (
            freeze.get("source_g08_result") == "PASS_4_OF_4"
        )
        checks["g09_envelope_freeze_surface_exact"] = (
            freeze.get("canonical_surface_sha256")
            == base.EXPECTED_COMPOSITE_SHA256
        )
        checks["g09_envelope_freeze_requires_exact_match"] = (
            freeze.get("require_exact_match_before_authorization_consumption")
            is True
        )
        checks["g09_envelope_freeze_four_cases_exact"] = (
            len(expected) == 4 and set(expected) == set(rendered)
        )

        for case_id, expected_identity in expected.items():
            actual = rendered.get(case_id) or {}
            checks[f"{case_id}:g08_g09_envelope_bytes_exact"] = (
                actual.get("bytes") == expected_identity.get("bytes")
            )
            checks[f"{case_id}:g08_g09_envelope_sha256_exact"] = (
                actual.get("sha256") == expected_identity.get("sha256")
            )
    except Exception as exc:
        checks["g09_envelope_freeze_loadable"] = False
        report["envelope_freeze_error_type"] = type(exc).__name__

    failed = [name for name, ok in checks.items() if not ok]
    report["failed_checks"] = failed
    report["verdict"] = "PASS" if not failed else "FAIL"
    report["envelope_freeze"] = str(ENVELOPE_FREEZE.relative_to(base.ROOT))
    report["authorization_not_consumed_during_preflight"] = True
    report["truth_boundary"] = (
        "ZERO_MODEL_G09_PREFLIGHT_WITH_EXACT_G08_ENVELOPE_PARITY_"
        "UNTIL_PASS_AND_EXACT_OPENAI_BATCH_AUTHORIZATION"
    )
    return report, cases, evaluations


base.load_and_preflight = load_and_preflight

if __name__ == "__main__":
    raise SystemExit(base.main())
