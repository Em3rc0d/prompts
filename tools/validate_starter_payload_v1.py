#!/usr/bin/env python3
"""Validate the Starter customer payload and packaging identity without runtime evidence."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "product" / "starter-collection-v1"
LAYOUT = BASE / "ARTIFACT_LAYOUT_V1.json"
FREEZE = BASE / "PAYLOAD_FREEZE_V1.json"
BUILD_RECEIPT = BASE / "ARCHIVE_BUILD_RECEIPT_V1.json"

SYNTHETIC_LABEL = "SYNTHETIC EXAMPLE — NOT A RUNTIME OBSERVATION — NOT CUSTOMER EVIDENCE"
CANONICAL_ARCHIVE_SHA256 = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"
CANONICAL_ARCHIVE_SIZE = 50918


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    layout = read_json(LAYOUT)
    freeze = read_json(FREEZE)
    build_receipt = read_json(BUILD_RECEIPT)

    assert layout["schema"] == "prompt-machine-starter-artifact-layout-v1"
    assert layout["version"] == "1.0.2"
    assert layout["artifact_state"] == "DETERMINISTIC_ARCHIVE_BUILD_OBSERVED"

    required = layout["customer_visible_assets"]
    assert len(required) == 9
    assert all(item["state"].startswith("PRESENT") for item in required)

    expected_paths = {item["path"] for item in required}
    assert expected_paths == set(freeze["required_customer_assets"])

    for relative in expected_paths:
        assert (BASE / relative).is_file(), f"missing required customer asset: {relative}"

    assert layout["truth"]["required_customer_assets_total"] == 9
    assert layout["truth"]["required_customer_assets_present"] == 9
    assert layout["truth"]["required_customer_assets_pending"] == 0
    assert layout["truth"]["archive_built"] is True
    assert layout["truth"]["archive_reproducible"] is True
    assert layout["truth"]["provider_custody"] is False
    assert layout["truth"]["customer_delivery_observed"] is False
    assert layout["truth"]["ready_to_sell"] is False

    archive = layout["archive_identity"]
    assert archive["filename"] == "prompt-machine-starter-collection-v1.zip"
    assert archive["size_bytes"] == CANONICAL_ARCHIVE_SIZE
    assert archive["sha256"] == CANONICAL_ARCHIVE_SHA256
    assert archive["canonical_build_source_commit"] == "167faad0758b3e746b48ac7c898f876525d30ee3"
    assert archive["build_receipt"] == "PM-STARTER-ARCHIVE-BUILD-V1-0001"
    assert archive["state"] == "REPRODUCIBLE_BUILD_OBSERVED"

    code_example = (BASE / "examples" / "code-review-worked-example.md").read_text(encoding="utf-8")
    bug_example = (BASE / "examples" / "bug-diagnosis-worked-example.md").read_text(encoding="utf-8")
    assert SYNTHETIC_LABEL in code_example
    assert SYNTHETIC_LABEL in bug_example

    evidence = (BASE / "EVIDENCE_AND_LIMITATIONS.md").read_text(encoding="utf-8")
    for statement in [
        "Starter SKU runtime observations           0",
        "Real customer task outcomes                0",
        "Real purchases                              0",
        "READY_TO_SELL                              NO",
        "architecture evidence != Starter SKU evidence",
        "MARKETING CLAIM <= OBSERVED EVIDENCE",
    ]:
        assert statement in evidence

    license_text = (BASE / "LICENSE.md").read_text(encoding="utf-8")
    for statement in [
        "Prompt Machine Starter Collection",
        "Prohibited redistribution and resale",
        "Evidence and performance boundary",
        "Synthetic worked examples are illustrative and are not runtime or customer evidence.",
        "does not automatically inherit Prompt Machine's evidence",
    ]:
        assert statement in license_text

    # PAYLOAD_FREEZE is an immutable pre-build snapshot. Its historical archive=false truth stays valid.
    assert freeze["schema"] == "prompt-machine-starter-payload-freeze-v1"
    assert freeze["receipt_id"] == "PM-STARTER-PAYLOAD-FREEZE-V1-0001"
    assert freeze["state"] == "CUSTOMER_PAYLOAD_STATIC_COMPLETE_ARCHIVE_NOT_BUILT"
    assert freeze["required_customer_asset_count"] == 9
    assert freeze["required_customer_assets_present"] == 9
    assert freeze["required_customer_assets_pending"] == 0
    assert freeze["truth"]["starter_sku_runtime_observations"] == 0
    assert freeze["truth"]["starter_skill_behavioral_observations"] == 0
    assert freeze["truth"]["real_customer_outcomes"] == 0
    assert freeze["truth"]["real_purchases"] == 0
    assert freeze["truth"]["archive_built"] is False
    assert freeze["truth"]["archive_sha256"] is None
    assert freeze["truth"]["provider_custody"] is False
    assert freeze["truth"]["public_checkout"] is False
    assert freeze["truth"]["ready_to_sell"] is False

    assert build_receipt["schema"] == "prompt-machine-starter-archive-build-receipt-v1"
    assert build_receipt["receipt_id"] == "PM-STARTER-ARCHIVE-BUILD-V1-0001"
    assert build_receipt["state"] == "DETERMINISTIC_ARCHIVE_BUILD_PASS"
    assert build_receipt["workflow_run"]["conclusion"] == "success"
    assert build_receipt["customer_archive"]["required_customer_assets"] == 9
    assert build_receipt["customer_archive"]["size_bytes"] == CANONICAL_ARCHIVE_SIZE
    assert build_receipt["customer_archive"]["sha256"] == CANONICAL_ARCHIVE_SHA256
    assert build_receipt["customer_archive"]["reproducibility_check"] == "PASS_BYTE_FOR_BYTE_TWO_BUILDS"
    assert build_receipt["validation"]["model_calls"] == 0
    assert build_receipt["validation"]["provider_calls"] == 0
    assert build_receipt["evidence_boundary"]["github_actions_artifact_is_commerce_provider_custody"] is False
    assert build_receipt["evidence_boundary"]["archive_build_is_customer_delivery_evidence"] is False
    assert build_receipt["evidence_boundary"]["archive_build_is_ready_to_sell"] is False

    conditional = layout["conditional_assets"]
    assert len(conditional) == 4
    assert all(item["state"].startswith("CONDITIONAL_") for item in conditional)
    assert layout["truth"]["skills_in_required_payload"] == 0
    assert layout["truth"]["workflow_trust_cards_in_required_payload"] == 0

    print("STARTER CUSTOMER PAYLOAD V1: PASS")
    print("required_assets=9/9")
    print("synthetic_examples_labeled=true")
    print("archive_built=true")
    print("archive_reproducible=true")
    print(f"archive_size_bytes={CANONICAL_ARCHIVE_SIZE}")
    print(f"archive_sha256={CANONICAL_ARCHIVE_SHA256}")
    print("provider_custody=false")
    print("customer_delivery_observed=false")
    print("starter_runtime_observations=0")
    print("model_calls=0")
    print("provider_calls=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
