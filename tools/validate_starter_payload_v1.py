#!/usr/bin/env python3
"""Validate the static Starter customer payload without creating runtime evidence."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "product" / "starter-collection-v1"
LAYOUT = BASE / "ARTIFACT_LAYOUT_V1.json"
FREEZE = BASE / "PAYLOAD_FREEZE_V1.json"

SYNTHETIC_LABEL = "SYNTHETIC EXAMPLE — NOT A RUNTIME OBSERVATION — NOT CUSTOMER EVIDENCE"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    layout = read_json(LAYOUT)
    freeze = read_json(FREEZE)

    assert layout["schema"] == "prompt-machine-starter-artifact-layout-v1"
    assert layout["version"] == "1.0.1"
    assert layout["artifact_state"] == "REQUIRED_CUSTOMER_PAYLOAD_PRESENT_ARCHIVE_NOT_BUILT"

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
    assert layout["truth"]["archive_built"] is False
    assert layout["archive_identity"]["filename"] is None
    assert layout["archive_identity"]["size_bytes"] is None
    assert layout["archive_identity"]["sha256"] is None
    assert layout["archive_identity"]["source_commit"] is None
    assert layout["archive_identity"]["state"] == "UNKNOWN_UNTIL_DETERMINISTIC_BUILD"

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
    assert freeze["truth"]["external_model_calls_created_by_freeze"] == 0
    assert freeze["truth"]["provider_calls_created_by_freeze"] == 0

    conditional = layout["conditional_assets"]
    assert len(conditional) == 4
    assert all(item["state"].startswith("CONDITIONAL_") for item in conditional)
    assert layout["truth"]["skills_in_required_payload"] == 0
    assert layout["truth"]["workflow_trust_cards_in_required_payload"] == 0

    print("STARTER CUSTOMER PAYLOAD V1: PASS")
    print("required_assets=9/9")
    print("synthetic_examples_labeled=true")
    print("archive_built=false")
    print("provider_custody=false")
    print("starter_runtime_observations=0")
    print("model_calls=0")
    print("provider_calls=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
