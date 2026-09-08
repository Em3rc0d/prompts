#!/usr/bin/env python3
"""Audit Prompt Machine Starter public copy against the current evidence ceiling.

This is a deterministic static copy audit. It creates no model, provider,
customer-value, delivery, certification, skill-behavior, or revenue evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
SKILL_SCOPE = ROOT / "commercial" / "STARTER_SKILL_LAUNCH_SCOPE_V1.json"
RELEASE_GATE = ROOT / "commercial" / "STARTER_RELEASE_GATE_V1.json"
RUNTIME_CORRECTION = ROOT / "product" / "starter-collection-v1" / "evaluation" / "corrections" / "PM-STARTER-CR-NORMAL-0001.protocol-contamination.json"
CLEAN_SURFACE = ROOT / "commercial" / "STARTER_CLEAN_RUNTIME_SURFACE_REQUIREMENTS_V1.json"

FILES = {
    "home": WEB / "app" / "page.tsx",
    "collections": WEB / "app" / "collections" / "page.tsx",
    "starter": WEB / "app" / "starter-collection" / "page.tsx",
    "full": WEB / "app" / "developer-pack" / "page.tsx",
    "free": WEB / "app" / "free" / "developer-starter-pack" / "page.tsx",
    "license": WEB / "app" / "license" / "page.tsx",
    "layout": WEB / "app" / "layout.tsx",
    "commerce_link": WEB / "components" / "commerce-link.tsx",
}

STARTER_CHECKOUT = WEB / "app" / "api" / "commerce" / "starter-collection" / "checkout" / "route.ts"


def text(name: str) -> str:
    path = FILES[name]
    assert path.is_file(), f"missing audited surface: {path}"
    return path.read_text(encoding="utf-8")


def reject(haystack: str, needles: list[str], scope: str) -> None:
    lower = haystack.lower()
    for needle in needles:
        assert needle.lower() not in lower, f"prohibited/stale phrase in {scope}: {needle!r}"


def load_json(path: Path) -> dict:
    assert path.is_file(), f"missing governed evidence: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    skill_scope = load_json(SKILL_SCOPE)
    gate = load_json(RELEASE_GATE)
    correction = load_json(RUNTIME_CORRECTION)
    clean_surface = load_json(CLEAN_SURFACE)

    home = text("home")
    collections = text("collections")
    starter = text("starter")
    full = text("full")
    free = text("free")
    license_page = text("license")
    layout = text("layout")
    commerce = text("commerce_link")

    # Evidence ceiling must come from governed state, not hard-coded marketing wishes.
    truth = gate["truth"]
    assert gate["version"] == "1.0.9"
    assert truth["starter_sku_workflow_runtime_observations"] == 1
    assert truth["starter_sku_workflow_runtime_passes"] == 0
    assert truth["starter_sku_workflow_runtime_fails"] == 0
    assert truth["starter_sku_workflow_runtime_inconclusive"] == 1
    assert truth["public_checkout_enabled"] is False
    assert truth["ready_to_sell"] is False

    assert correction["correction_class"] == "PROTOCOL_CONTAMINATION"
    assert correction["historical_artifacts"]["preserved_without_rewrite"] is True
    assert correction["historical_classification"]["review_result"] == "FAIL"
    assert correction["historical_classification"]["decision"] == "REWORK"
    assert correction["historical_classification"]["status"] == "PRESERVED_AS_HISTORICAL_MISCLASSIFICATION"
    effective = correction["effective_classification"]
    assert effective["review_result"] == "INCONCLUSIVE"
    assert effective["decision"] == "EXPAND_EVIDENCE"
    assert effective["reason"] == "INCONCLUSIVE_PROTOCOL_CONTAMINATION"
    assert effective["workflow_pass_count"] == 0
    assert effective["workflow_fail_count"] == 0
    assert effective["workflow_inconclusive_count"] == 1
    assert correction["workflow_mutation"]["observed_candidate_mutated"] is False
    assert correction["workflow_mutation"]["successor_required_by_this_observation"] is False

    assert clean_surface["requirement"] == "CLEAN_INDEPENDENT_EXECUTION_SURFACE"
    assert clean_surface["not_a_requirement"] == "CHATGPT_DOT_COM_SPECIFICALLY"
    assert clean_surface["same_candidate_retest_allowed"] is True
    assert clean_surface["successor_required_before_clean_retest"] is False
    assert clean_surface["automatic_execution"] is False
    assert clean_surface["automatic_retries"] == 0

    # Product identity + public sale state.
    assert "Prompt Machine" in layout
    assert "STARTER / USD 9 PRICE HYPOTHESIS · CHECKOUT OFF" in layout
    assert "FULL / USD 19 PRICE HYPOTHESIS · CHECKOUT OFF" in layout

    assert "NOT FOR SALE · $9 PRICE HYPOTHESIS · CLEAN RUNTIME EVIDENCE OPEN" in starter
    assert "PRICE HYPOTHESIS, not an active checkout" in starter
    assert "One Starter runtime observation exists" in starter
    assert "INCONCLUSIVE_PROTOCOL_CONTAMINATION" in starter
    assert "0 PASS, 0 FAIL, 1 INCONCLUSIVE" in starter
    assert "same frozen candidate must be retested on a clean independent surface" in starter
    assert "All canaries remain disarmed" in starter
    assert "1</strong><span>inconclusive observation" in starter
    assert "0 / 0</strong><span>effective PASS / FAIL" in starter
    assert "0 supported skill assets" in starter
    assert "workflow evidence != skill evidence" in starter

    reject(
        starter,
        [
            "STATIC PRODUCT SURFACES + PACKAGING PASS / RUNTIME UNOBSERVED",
            "Four product-specific canaries are prepared. None has been executed.",
            "0</strong><span>Starter runtime observations",
        ],
        "Starter stale runtime claims",
    )

    # The skill launch decision is an evidence boundary, not merely marketing wording.
    assert skill_scope["state"] == "SKILLS_DEFERRED_FROM_V1_LAUNCH_PAYLOAD_EVIDENCE_OPEN"
    assert skill_scope["decision"]["skills_are_launch_blocking"] is False
    assert skill_scope["decision"]["skills_are_required_customer_payload_assets"] is False
    assert skill_scope["decision"]["skills_are_currently_supported_product_features"] is False
    assert skill_scope["decision"]["skills_may_be_described_as_candidates"] is True
    assert skill_scope["decision"]["skills_may_be_marketed_as_included_or_tested"] is False
    assert skill_scope["launch_payload_boundary"]["skills_in_current_deterministic_archive"] == 0
    assert skill_scope["current_truth"]["starter_supported_skills"] == 0
    assert skill_scope["current_truth"]["starter_skill_behavioral_observations"] == 0
    assert skill_scope["existing_evidence"]["HOST_TESTED"] is False
    assert skill_scope["existing_evidence"]["SKILL_TRIGGER_EVAL_PASS"] is False
    assert skill_scope["existing_evidence"]["SKILL_FORWARD_TEST_PASS"] is False
    assert skill_scope["existing_evidence"]["PROMPT_SKILL_PARITY_PASS"] is False

    # Customer copy must not convert candidate surfaces into present Starter value.
    assert "not part of the current 9-file Starter archive" in home
    assert "not supported or included in the current Starter archive" in collections
    assert "00</strong><span>supported skills today" in collections
    reject(
        home + "\n" + collections + "\n" + starter,
        [
            "their two skill candidates",
            "two installable skills",
            "2 supported skills",
            "skills included in Starter",
            "Starter includes two skills",
        ],
        "Starter public skill claims",
    )

    # Packaging may be claimed precisely, but not promoted into behavioral/customer proof.
    assert "9/9" in starter
    assert "50,918" in starter
    assert "4eceb1ee…" in starter
    assert "does not imply provider custody or customer delivery" in home + starter

    # Other key surfaces preserve hypothesis/checkout language.
    assert "$9" in home and "Starter hypothesis" in home
    assert "Both checkouts stay off until release evidence closes." in home
    assert "PRIMARY PAID HYPOTHESIS · CHECKOUT OFF" in collections
    assert "$9" in collections and "price hypothesis" in collections
    assert "NOT FOR SALE" in full and "PRICE HYPOTHESIS" in full
    assert "delivery integrity—not behavioral certification" in free

    # License page must describe Prompt Machine and the corrected runtime boundary.
    assert 'title: "License | Prompt Machine"' in license_page
    assert "No paid collection is currently for sale." in license_page
    assert "one preserved runtime observation" in license_page
    assert "INCONCLUSIVE_PROTOCOL_CONTAMINATION" in license_page
    assert "0 effective PASS and 0 effective FAIL" in license_page
    assert "no clean independent Starter runtime observation exists yet" in license_page
    reject(
        license_page,
        [
            "License | Prompt Quarry",
            "Prompt Quarry Developer Pack proprietary commercial license summary",
            "LICENSE.md delivered with the purchased Pack is authoritative",
            "Current Starter runtime observations remain zero.",
        ],
        "license",
    )

    # Starter CTA is always informational while the release gate is blocked.
    assert 'kind === "starter"' in commerce
    assert '? "/starter-collection"' in commerce
    assert not STARTER_CHECKOUT.exists(), "public Starter checkout route exists while audit expects checkout OFF"

    # Runtime disclosure cannot turn the historical review artifact into a behavioral claim.
    reject(
        home + "\n" + collections + "\n" + starter + "\n" + license_page,
        [
            "Starter failed runtime validation",
            "Starter has a confirmed workflow failure",
            "Starter runtime failure",
            "Starter is tested",
            "Starter is proven",
            "Starter is certified",
            "Starter is production-ready",
            "Starter is ready to sell",
            "Starter is portable across models",
            "customers love Starter",
            "customers trust Starter",
            "available now",
            "buy now",
        ],
        "Starter evidence claims",
    )

    # Prompt Quarry may appear publicly only as the named internal factory, not the customer product identity.
    assert "FACTORY / PROMPT QUARRY · EVIDENCE BEFORE CLAIMS" in layout
    assert "Prompt Quarry handles the engineering and evidence underneath" in home

    print("STARTER PUBLIC COPY EVIDENCE AUDIT V1: PASS_CURRENT_EVIDENCE_BOUNDARY")
    print("audited_surfaces=8")
    print("starter_checkout_route_present=false")
    print("starter_runtime_observations_claimed=1")
    print("starter_runtime_passes_claimed=0")
    print("starter_runtime_fails_claimed=0")
    print("starter_runtime_inconclusive_claimed=1")
    print("clean_runtime_observations_claimed=0")
    print("historical_fail_artifact_preserved=true")
    print("historical_fail_marketed_as_effective_failure=false")
    print("starter_supported_skills_claimed=0")
    print("starter_skill_candidates_are_archive_assets=false")
    print("price_hypothesis_visible=true")
    print("license_identity=Prompt Machine")
    print("model_calls=0")
    print("provider_calls=0")
    print("customer_outcomes_created=0")
    print("revenue_evidence_created=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
