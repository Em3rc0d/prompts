#!/usr/bin/env python3
"""Validate the Developer Workflow Collection customer-experience candidate.

This gate is intentionally structural/product-level. It does not execute a model,
claim runtime behavior, or make any collection sellable.

Important state split:
- product/developer-workflow-kit-v1.2 remains the broader Full candidate.
- product/starter-collection-v1 is the independent governed Starter release line.
The validator must not erase or merge those evidence states.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "product" / "developer-workflow-kit-v1.2"
CATALOG = PRODUCT / "CATALOG.candidate.json"
SPEC = PRODUCT / "SPEC.md"
START_CANDIDATE = PRODUCT / "START_HERE.candidate.md"
START_RELEASE = PRODUCT / "START_HERE.md"
STARTER_IDENTITY = ROOT / "product" / "starter-collection-v1" / "PRODUCT_IDENTITY_V1.json"

CANONICAL_STARTER_ID = "prompt-machine-starter-collection"
LEGACY_STARTER_ID = "pq-developer-starter-collection"
STARTER_ARCHIVE_SIZE = 50918
STARTER_ARCHIVE_SHA256 = "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97"

EXPECTED_SKILLS = {
    "PQ-WF-0001": "review-code-with-evidence",
    "PQ-WF-0002": "diagnose-bugs-with-evidence",
    "PQ-WF-0003": "make-technical-decisions",
    "PQ-WF-0004": "design-ai-workflows",
}

EXPECTED_TASKS = {
    "PQ-WF-0001": "Review a software change",
    "PQ-WF-0002": "Diagnose a bug or regression",
    "PQ-WF-0003": "Make a technical decision",
    "PQ-WF-0004": "Design a reusable AI workflow",
}

EXPECTED_STARTER_WORKFLOWS = ["PQ-WF-0001", "PQ-WF-0002"]
EXPECTED_STARTER_SKILLS = ["PQ-SKILL-0001", "PQ-SKILL-0002"]
EXPECTED_STARTER_EXPERIENCE = [
    "START_HERE",
    "TASK_CHOOSER",
    "WORKED_EXAMPLES",
    "VERIFICATION_GUIDANCE",
    "ADAPTATION_CHEATSHEET",
    "EVIDENCE_AND_LIMITATIONS",
    "LICENSE",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    for path in (CATALOG, SPEC, START_CANDIDATE, STARTER_IDENTITY):
        if not path.is_file():
            fail(errors, f"required product experience file missing: {path.relative_to(ROOT)}")

    if errors:
        report = {"schema": "prompt-machine-developer-collection-experience-v1", "status": "FAIL", "errors": errors}
        print(json.dumps(report, indent=2))
        return 1

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    identity = json.loads(STARTER_IDENTITY.read_text(encoding="utf-8"))
    spec = SPEC.read_text(encoding="utf-8")
    start = START_CANDIDATE.read_text(encoding="utf-8")

    if catalog.get("sale_status") != "NOT_FOR_SALE":
        fail(errors, "candidate sale_status must remain NOT_FOR_SALE")

    brand = catalog.get("brand", {})
    if brand.get("customer_facing") != "Prompt Machine":
        fail(errors, "customer-facing brand must be Prompt Machine")
    if brand.get("internal_factory") != "Prompt Quarry":
        fail(errors, "internal factory must remain Prompt Quarry")

    ladder = catalog.get("commercial_ladder", {})
    if (ladder.get("free_usd"), ladder.get("starter_usd"), ladder.get("full_developer_usd")) != (0, 9, 19):
        fail(errors, "commercial ladder must remain $0 -> $9 -> $19")
    if ladder.get("primary_first_paid_offer") != "STARTER_COLLECTION":
        fail(errors, "$9 Starter Collection must remain the primary first paid offer")
    if ladder.get("starter_scope_state") != "FROZEN":
        fail(errors, "Starter Collection scope must remain frozen")
    if ladder.get("subscription") != "DEFERRED_UNTIL_RECURRING_VALUE_OBSERVED":
        fail(errors, "subscription must remain deferred until recurring value is observed")

    products = {row.get("product_id"): row for row in catalog.get("products", [])}
    paid = products.get("pq-developer-pack")
    if not paid:
        fail(errors, "technical paid product identity pq-developer-pack missing")
    else:
        if paid.get("display_name") != "Prompt Machine Developer Workflow Collection":
            fail(errors, "Full collection display name is not Prompt Machine aligned")
        price = paid.get("price", {})
        if price.get("launch_usd") != 19 or price.get("evidence_state") != "PRICE_HYPOTHESIS":
            fail(errors, "$19 price must remain explicitly a PRICE_HYPOTHESIS")

    planned = {row.get("product_id"): row for row in catalog.get("planned_products", [])}
    starter = planned.get(CANONICAL_STARTER_ID)
    if not starter:
        fail(errors, "canonical Starter Collection product identity missing")
    else:
        if starter.get("legacy_product_ids") != [LEGACY_STARTER_ID]:
            fail(errors, "Starter legacy identity must remain one explicit historical alias")
        if starter.get("identity_contract") != "product/starter-collection-v1/PRODUCT_IDENTITY_V1.json":
            fail(errors, "Starter catalog is not bound to its identity contract")
        if starter.get("display_name") != "Prompt Machine Starter Collection":
            fail(errors, "Starter customer display name mismatch")
        if starter.get("tier") != "PAID_STARTER" or starter.get("version") != "1.0.0-candidate":
            fail(errors, "Starter tier/version contract mismatch")
        starter_price = starter.get("price", {})
        if starter_price.get("launch_usd") != 9 or starter_price.get("evidence_state") != "PRICE_HYPOTHESIS":
            fail(errors, "$9 Starter price must remain explicitly a PRICE_HYPOTHESIS")
        if starter.get("scope_state") != "FROZEN":
            fail(errors, "Starter scope must remain FROZEN")
        if starter.get("workflows") != EXPECTED_STARTER_WORKFLOWS:
            fail(errors, "Starter must contain Code Review + Bug Diagnosis workflow families")
        if starter.get("skill_ids") != EXPECTED_STARTER_SKILLS:
            fail(errors, "Starter must contain the two corresponding skill candidates")
        if starter.get("skill_state") != "CANDIDATES_CONDITIONAL_ON_SKILL_EVIDENCE":
            fail(errors, "Starter skill candidates are being overstated as supported skills")
        if starter.get("customer_experience_contract") != EXPECTED_STARTER_EXPERIENCE:
            fail(errors, "Starter customer-experience contract mismatch")
        if starter.get("sale_status") != "NOT_FOR_SALE":
            fail(errors, "Starter must remain NOT_FOR_SALE until downstream evidence closes")

        snapshot = starter.get("current_release_snapshot", {})
        expected_snapshot = {
            "workflow_contracts_static_pass": 2,
            "executable_prompt_surfaces_static_pass": 2,
            "required_customer_assets_present": 9,
            "required_customer_assets_total": 9,
            "deterministic_archive_pass": True,
            "archive_size_bytes": STARTER_ARCHIVE_SIZE,
            "archive_sha256": STARTER_ARCHIVE_SHA256,
            "starter_runtime_observations": 0,
            "starter_skill_behavioral_observations": 0,
            "public_copy_evidence_audit": "PASS_CURRENT_EVIDENCE_BOUNDARY",
            "provider_custody": False,
            "live_delivery": False,
            "real_customer_outcomes": 0,
            "real_purchases": 0,
            "ready_to_sell": False,
        }
        if snapshot != expected_snapshot:
            fail(errors, "Starter catalog release snapshot drifted from governed Starter truth")

    identity_product = identity.get("product", {})
    identity_rules = identity.get("rules", {})
    identity_aliases = identity.get("legacy_aliases", [])
    if identity_product.get("canonical_product_id") != CANONICAL_STARTER_ID:
        fail(errors, "Starter identity contract canonical product id mismatch")
    if identity_product.get("product_version") != "1.0.0-candidate":
        fail(errors, "Starter identity contract version mismatch")
    if not any(row.get("product_id") == LEGACY_STARTER_ID for row in identity_aliases):
        fail(errors, "Starter identity contract lost legacy alias provenance")
    if identity_rules.get("historical_records_rewritten") is not False:
        fail(errors, "identity migration may not rewrite historical records")
    if identity_rules.get("legacy_alias_may_be_silently_treated_as_new_canonical_event") is not False:
        fail(errors, "legacy Starter alias may not silently become a new canonical event")

    # The broader Full candidate remains a separate, older workstream with its own
    # still-open prompt surfaces. Starter completion must not falsify this state.
    workflows = {row.get("workflow_id"): row for row in catalog.get("workflows", [])}
    if set(workflows) != set(EXPECTED_SKILLS):
        fail(errors, f"workflow set mismatch: {sorted(workflows)}")

    pending_surfaces = 0
    for workflow_id, skill_name in EXPECTED_SKILLS.items():
        row = workflows.get(workflow_id, {})
        if row.get("customer_task") != EXPECTED_TASKS[workflow_id]:
            fail(errors, f"{workflow_id}: customer task does not match frozen task chooser")
        skill = row.get("skill", {})
        if skill.get("name") != skill_name:
            fail(errors, f"{workflow_id}: expected skill {skill_name}")
        skill_path = PRODUCT / "skills" / skill_name / "SKILL.md"
        if not skill_path.is_file():
            fail(errors, f"{workflow_id}: skill entrypoint missing: {skill_path.relative_to(ROOT)}")

        prompt_surface = row.get("customer_prompt_surface")
        prompt_state = row.get("customer_prompt_state")
        if prompt_surface is None:
            pending_surfaces += 1
            if not str(prompt_state).startswith("PENDING_"):
                fail(errors, f"{workflow_id}: null customer prompt surface must carry explicit PENDING state")
        else:
            path = ROOT / str(prompt_surface)
            if not path.is_file():
                fail(errors, f"{workflow_id}: declared customer prompt surface missing: {prompt_surface}")

    experience = catalog.get("customer_experience", {})
    if experience.get("entrypoint_design") != "product/developer-workflow-kit-v1.2/START_HERE.candidate.md":
        fail(errors, "Full candidate entrypoint path is not canonical")
    if experience.get("primary_discovery_axis") != "CUSTOMER_TASK":
        fail(errors, "collection must remain task-first rather than profession/repository-first")
    if experience.get("ten_minute_activation_observed") is not False:
        fail(errors, "ten-minute activation must remain unobserved until usability evidence exists")
    if experience.get("pending_customer_prompt_surfaces") != pending_surfaces:
        fail(errors, "Full candidate pending_customer_prompt_surfaces contradict actual inventory")
    if "Starter Collection has its own governed release snapshot" not in str(experience.get("note", "")):
        fail(errors, "catalog no longer explains the Full-vs-Starter evidence-state split")

    gates = catalog.get("gates", {})
    if gates.get("customer_experience_entrypoint_design") is not True:
        fail(errors, "customer experience entrypoint design gate not recorded")
    if gates.get("starter_collection_scope_frozen") is not True:
        fail(errors, "Starter Collection scope freeze gate not recorded")
    if gates.get("customer_prompt_surfaces_complete") != (pending_surfaces == 0):
        fail(errors, "Full candidate customer_prompt_surfaces_complete contradicts actual surfaces")
    for blocked in (
        "customer_examples_complete",
        "customer_evidence_cards_complete",
        "skill_trigger_eval_pass",
        "skill_forward_test_pass",
        "prompt_skill_parity_pass",
        "pack_value_review_pass",
        "deterministic_archive_pass",
        "provider_custody_pass",
        "provider_integration_pass",
        "live_delivery_canary_pass",
        "PRODUCT_READY",
        "READY_TO_SELL",
    ):
        if gates.get(blocked) is not False:
            fail(errors, f"Full candidate pre-release gate must remain false: {blocked}")

    required_start_tokens = (
        "You do not need to read the whole collection",
        "5-minute path",
        "Choose your workflow",
        "Evidence legend",
        "What should be in the final customer archive",
        "PENDING_GOVERNED_V1_2_SURFACE",
        "START_HERE.candidate.md != RELEASE_READY",
    )
    for token in required_start_tokens:
        if token not in start:
            fail(errors, f"START_HERE candidate missing boundary: {token}")
    if start.count("PENDING_GOVERNED_V1_2_SURFACE") < pending_surfaces:
        fail(errors, "START_HERE does not expose every pending Full customer prompt surface")
    for skill_name in EXPECTED_SKILLS.values():
        if f"skills/{skill_name}/SKILL.md" not in start:
            fail(errors, f"START_HERE chooser does not link skill: {skill_name}")

    if "CANDIDATE IMPLEMENTED / STRUCTURE PASS" not in spec:
        fail(errors, "SPEC status is stale relative to implemented/validated candidate")
    for token in ("START_HERE.md", "MARKETING CLAIM <= OBSERVED EVIDENCE", "READY_TO_SELL                 NO"):
        if token not in spec:
            fail(errors, f"SPEC missing release/customer boundary: {token}")

    if pending_surfaces and START_RELEASE.exists():
        fail(errors, "Full release START_HERE.md exists while Full prompt surfaces are incomplete")

    delivery = catalog.get("delivery", {})
    if delivery.get("proposed_paid_archive_root") != "prompt-machine-developer-workflow-collection-v1.2.0":
        fail(errors, "Full proposed customer archive root is not Prompt Machine aligned")
    if delivery.get("archive_root_authoritative") is not False:
        fail(errors, "Full archive root cannot be authoritative before its deterministic receipt")

    state = "DESIGN_VALID_RELEASE_BLOCKED" if not errors and pending_surfaces else ("RELEASE_SURFACES_COMPLETE" if not errors else "FAIL")
    report = {
        "schema": "prompt-machine-developer-collection-experience-v1",
        "gate": "CUSTOMER_EXPERIENCE_DESIGN",
        "status": "PASS" if not errors else "FAIL",
        "state": state,
        "customer_brand": brand.get("customer_facing"),
        "internal_factory": brand.get("internal_factory"),
        "commercial_ladder": "$0->$9->$19",
        "starter_product_id": CANONICAL_STARTER_ID,
        "starter_legacy_alias": LEGACY_STARTER_ID,
        "starter_scope_frozen": gates.get("starter_collection_scope_frozen"),
        "starter_workflow_count": len(starter.get("workflows", [])) if starter else 0,
        "starter_static_surfaces": starter.get("current_release_snapshot", {}).get("executable_prompt_surfaces_static_pass") if starter else None,
        "starter_runtime_observations": starter.get("current_release_snapshot", {}).get("starter_runtime_observations") if starter else None,
        "workflow_count": len(workflows),
        "skill_entrypoints_verified": len(EXPECTED_SKILLS),
        "full_pending_customer_prompt_surfaces": pending_surfaces,
        "full_final_start_here_exists": START_RELEASE.exists(),
        "behavioral_claim": "NONE",
        "sale_status": catalog.get("sale_status"),
        "PRODUCT_READY": gates.get("PRODUCT_READY"),
        "READY_TO_SELL": gates.get("READY_TO_SELL"),
        "errors": errors,
        "warnings": warnings,
    }

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
