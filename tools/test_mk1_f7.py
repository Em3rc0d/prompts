from __future__ import annotations

import copy
import json

from mk1_f6_certify import build_certification_receipt, promote_certified
from mk1_f7_portable import build_portability_receipt, promote_portable
from mk1_prompt_linter import lint_artifact
from test_mk1_f6 import make_receipt, source_bundle


def portable_source():
    source, candidate, baseline, fixtures, f6_receipts = source_bundle()
    f6_receipt = build_certification_receipt(candidate, source, baseline, fixtures, f6_receipts)
    certified = promote_certified(candidate, f6_receipt)
    extra = [
        make_receipt(4, provider="anthropic", model="claude-target", family="anthropic-claude-target"),
        make_receipt(5, provider="gemini", model="gemini-target", family="google-gemini-target"),
    ]
    return source, candidate, certified, baseline, fixtures, f6_receipt, f6_receipts + extra


def test_portability_pass() -> dict:
    source, candidate, certified, baseline, fixtures, f6_receipt, receipts = portable_source()
    receipt = build_portability_receipt(certified, f6_receipt, candidate, source, baseline, fixtures, receipts)
    assert receipt["status"] == "PORTABILITY_PASS"
    assert receipt["eligible_for_portable"] is True
    assert receipt["runtime_provider_count"] == 3
    assert receipt["runtime_family_count"] == 3
    portable = promote_portable(certified, receipt)
    assert portable["state"] == "PORTABLE"
    assert portable["claims"] == ["engineered", "tested", "improved", "certified", "portable"]
    assert lint_artifact(portable)["status"] == "PASS"
    return {"providers": receipt["runtime_providers"], "families": receipt["runtime_families"], "state": portable["state"]}


def test_two_providers_rejected() -> dict:
    source, candidate, certified, baseline, fixtures, f6_receipt, receipts = portable_source()
    evidence = receipts[:-1]
    try:
        build_portability_receipt(certified, f6_receipt, candidate, source, baseline, fixtures, evidence)
    except ValueError as exc:
        assert "3 distinct runtime providers" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F7 must reject fewer than three providers")


def test_family_diversity_rejected() -> dict:
    source, candidate, certified, baseline, fixtures, f6_receipt, receipts = portable_source()
    replacement = make_receipt(5, provider="gemini", model="gemini-target", family="anthropic-claude-target")
    evidence = receipts[:-1] + [replacement]
    try:
        build_portability_receipt(certified, f6_receipt, candidate, source, baseline, fixtures, evidence)
    except ValueError as exc:
        assert "3 distinct runtime families" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F7 must reject fewer than three families")


def test_uncertified_source_rejected() -> dict:
    source, candidate, certified, baseline, fixtures, f6_receipt, receipts = portable_source()
    bad = copy.deepcopy(certified)
    bad["state"] = "CANDIDATE"
    try:
        build_portability_receipt(bad, f6_receipt, candidate, source, baseline, fixtures, receipts)
    except ValueError as exc:
        assert "CERTIFIED" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F7 must reject non-certified sources")


def test_prompt_drift_rejected() -> dict:
    source, candidate, certified, baseline, fixtures, f6_receipt, receipts = portable_source()
    bad = copy.deepcopy(certified)
    bad["prompt_body"] += "\nDRIFT\n"
    try:
        build_portability_receipt(bad, f6_receipt, candidate, source, baseline, fixtures, receipts)
    except ValueError as exc:
        assert "identity drift" in str(exc) or "fingerprint" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F7 must reject prompt drift")


def test_tampered_f7_receipt_rejected() -> dict:
    source, candidate, certified, baseline, fixtures, f6_receipt, receipts = portable_source()
    receipt = build_portability_receipt(certified, f6_receipt, candidate, source, baseline, fixtures, receipts)
    receipt["runtime_provider_count"] = 4
    try:
        promote_portable(certified, receipt)
    except ValueError as exc:
        assert "integrity check failed" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("F7 must reject tampered portability receipts")


def main() -> None:
    print(json.dumps({
        "mk1_f7": "PASS",
        "portability_pass": test_portability_pass(),
        "provider_diversity": test_two_providers_rejected(),
        "family_diversity": test_family_diversity_rejected(),
        "certified_source_required": test_uncertified_source_rejected(),
        "prompt_identity_freeze": test_prompt_drift_rejected(),
        "f7_receipt_integrity": test_tampered_f7_receipt_rejected(),
        "policy": "PORTABLE is an optional post-certification claim requiring the exact CERTIFIED prompt to preserve F5 superiority across at least three distinct providers and three distinct runtime families."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
