#!/usr/bin/env python3
"""Validate the historical Starter checkpoint without forcing stale copy into Verlune.

The old Prompt Machine Starter evidence remains immutable historical evidence. The
current customer-facing surface has moved to Verlune Code Review, so this validator
checks both layers explicitly instead of requiring the website to reproduce obsolete
Starter merchandising.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMERCIAL = ROOT / "commercial"
WEB = ROOT / "web"

GATE = COMMERCIAL / "STARTER_RELEASE_GATE_V1.json"
DAG = COMMERCIAL / "STARTER_RELEASE_DAG_V1.json"
SKILL_SCOPE = COMMERCIAL / "STARTER_SKILL_LAUNCH_SCOPE_V1.json"
COPY_RECEIPT = COMMERCIAL / "STARTER_PUBLIC_COPY_AUDIT_RECEIPT_V1.json"
PROVIDER_PREFLIGHT = COMMERCIAL / "STARTER_PROVIDER_PREFLIGHT_FREEZE_V1.json"
STATUS = COMMERCIAL / "STATUS_CURRENT.md"
BRAND = COMMERCIAL / "VERLUNE_BRAND_ARCHITECTURE_V1.md"
STARTER_PAGE = WEB / "app" / "starter-collection" / "page.tsx"
COLLECTIONS_PAGE = WEB / "app" / "collections" / "page.tsx"
HOME_PAGE = WEB / "app" / "page.tsx"
STARTER_CHECKOUT = WEB / "app" / "api" / "commerce" / "starter-collection" / "checkout" / "route.ts"

CANONICAL_PRODUCT_ID = "prompt-machine-starter-collection"
CANONICAL_ARCHIVE_SHA256 = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"
CANONICAL_ARCHIVE_SIZE = 50918
CURRENT_COPY_RUN = 33834092608
CURRENT_COPY_COMMIT = "bd086c2e7fd76bc3852eea7d2e048341dce25ed4"
VERLUNE_ARCHIVE = "verlune-code-review-v1.0.0.zip"
VERLUNE_ARCHIVE_SHA256 = "4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649"
VERLUNE_ARCHIVE_SIZE = 18859
VERLUNE_WORKFLOW_SHA256 = "6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(source: str, *tokens: str) -> None:
    for token in tokens:
        assert token in source, token


def main() -> int:
    gate = read_json(GATE)
    dag = read_json(DAG)
    skill = read_json(SKILL_SCOPE)
    copy = read_json(COPY_RECEIPT)
    preflight = read_json(PROVIDER_PREFLIGHT)

    # Historical Starter checkpoint stays preserved rather than rewritten to Verlune.
    assert gate["product"]["product_id"] == CANONICAL_PRODUCT_ID
    assert gate["product"]["sale_state"] == "NOT_FOR_SALE"
    assert gate["version"] == "1.0.10"
    assert gate["checkpoint_revision"] == "runtime-protocol-contamination-copy-reaudit-20260904"
    assert gate["truth"]["real_purchases"] == 0
    assert gate["truth"]["public_checkout_enabled"] is False
    assert gate["truth"]["ready_to_sell"] is False
    assert gate["launch_requirements"]["STARTER_PRODUCT_READY"] is False

    # Historical skill and public-copy evidence remains internally consistent.
    assert skill["state"] == "SKILLS_DEFERRED_FROM_V1_LAUNCH_PAYLOAD_EVIDENCE_OPEN"
    assert skill["product_id"] == CANONICAL_PRODUCT_ID
    assert skill["current_truth"]["starter_supported_skills"] == 0
    assert skill["current_truth"]["starter_skill_behavioral_observations"] == 0
    assert skill["launch_payload_boundary"]["skills_in_current_deterministic_archive"] == 0
    assert gate["gates"]["starter_skill_launch_scope"] == "DEFERRED_NON_BLOCKING_ZERO_SUPPORTED_SKILLS"

    assert copy["version"] == "1.2.0"
    assert copy["final_state"] == "PASS_CURRENT_EVIDENCE_BOUNDARY"
    assert copy["current_retest"]["run_id"] == CURRENT_COPY_RUN
    assert copy["current_retest"]["audited_commit"] == CURRENT_COPY_COMMIT
    assert copy["current_retest"]["conclusion"] == "success"
    assert copy["model_calls"] == 0
    assert copy["provider_calls"] == 0
    assert copy["ready_to_sell"] is False

    # The historical DAG remains historical evidence; dedicated DAG tests validate it in depth.
    nodes = {node["id"]: node for node in dag["nodes"]}
    assert dag["version"] == "1.3.0"
    assert nodes["N07_PUBLIC_COPY_BOUNDARY"]["status"] == "OBSERVED_CLOSED"
    assert nodes["N09_STARTER_RUNTIME_EVIDENCE"]["status"] == "OPEN_REQUIRES_MODEL_AUTH"
    assert nodes["N14_PROVIDER_PROVISIONING_AND_CUSTODY"]["status"] == "OPEN_REQUIRES_PROVIDER_AUTH"

    # Historical provider preflight is preserved exactly and remains disarmed.
    assert preflight["state"] == "STATIC_PROVIDER_EXECUTION_PRECONDITIONS_PASS_DISARMED"
    assert preflight["product_id"] == CANONICAL_PRODUCT_ID
    assert preflight["canonical_artifact"]["size_bytes"] == CANONICAL_ARCHIVE_SIZE
    assert preflight["canonical_artifact"]["sha256"] == CANONICAL_ARCHIVE_SHA256
    assert preflight["execution_limits"]["custody_packet_armed"] is False
    assert preflight["execution_limits"]["delivery_canary_armed"] is False
    assert preflight["current_truth"]["real_customer_purchases"] == 0
    assert preflight["current_truth"]["public_checkout"] is False

    # Current customer surface must describe the successor product, not replay stale Starter copy.
    starter = STARTER_PAGE.read_text(encoding="utf-8")
    collections = COLLECTIONS_PAGE.read_text(encoding="utf-8")
    home = HOME_PAGE.read_text(encoding="utf-8")
    status = STATUS.read_text(encoding="utf-8")
    brand = BRAND.read_text(encoding="utf-8")

    require(
        starter,
        "Verlune Code Review",
        "One focused workflow. Exact evidence. No borrowed certainty.",
        "4/4",
        "77/77",
        "18,859",
        "PROVIDER VALIDATION PENDING",
    )
    require(
        collections,
        "Verlune Code Review",
        "01</strong><span>workflow",
        "$9",
        "77/77",
        "not for sale",
    )
    require(
        home,
        "VERLUNE / REUSABLE AI WORKFLOWS",
        "What are you trying to get done?",
        "Verlune Code Review",
        "marketing claim",
        "observed evidence",
    )
    require(
        status,
        "CUSTOMER-FACING  Verlune",
        VERLUNE_ARCHIVE,
        str(VERLUNE_ARCHIVE_SIZE),
        VERLUNE_ARCHIVE_SHA256,
        VERLUNE_WORKFLOW_SHA256,
        "PUBLIC_CHECKOUT     OFF",
    )
    require(brand, "Verlune", "Prompt Machine", "Prompt Quarry")

    for source in (starter, collections, home):
        assert "two installable skill candidates" not in source.lower()
        assert "0 PASS, 0 FAIL, 1 INCONCLUSIVE" not in source
    assert not STARTER_CHECKOUT.exists()

    print("STARTER LAUNCH CHECKPOINT V1: PASS")
    print("historical_starter_checkpoint=preserved")
    print("historical_starter_ready_to_sell=false")
    print("historical_public_checkout=false")
    print("current_customer_brand=Verlune")
    print("current_product=Verlune Code Review")
    print(f"current_archive={VERLUNE_ARCHIVE}")
    print(f"current_archive_bytes={VERLUNE_ARCHIVE_SIZE}")
    print(f"current_archive_sha256={VERLUNE_ARCHIVE_SHA256}")
    print("current_public_checkout=OFF")
    print("provider_calls=0")
    print("model_calls=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
