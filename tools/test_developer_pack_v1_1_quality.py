#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "product" / "developer-pack-v1.1"

REQUIRED = [
    PACK / "README.md",
    PACK / "SPEC.md",
    PACK / "QUICKSTART.md",
    PACK / "LICENSE.md",
    PACK / "quality" / "COMMERCIAL_VALUE_GATE.md",
    PACK / "templates" / "general-operating-contract.md",
    PACK / "templates" / "software-code-review-system.md",
    PACK / "templates" / "technical-research-decision-system.md",
    PACK / "contracts" / "workflow-contract.schema.json",
    PACK / "contracts" / "code-review-policy.example.json",
    PACK / "methodology" / "adaptation-playbook.md",
    PACK / "checklists" / "workflow-static-review.md",
    PACK / "examples" / "code-review-policy-transformation.md",
]

# These phrases are forbidden as customer-facing performance/marketing claims.
# Governance documents are allowed to mention the phrases when explicitly
# documenting that they must NOT be claimed. Therefore this guard is scoped to
# customer-facing sales/usage surfaces instead of blindly scanning policy text.
FORBIDDEN_CLAIMS = [
    "battle-tested",
    "proven superior",
    "best-performing",
    "guaranteed to improve",
    "universally portable",
    "works with every model",
]

CORE_TEMPLATE_REQUIREMENTS = {
    "general-operating-contract.md": [
        "INPUT CONTRACT",
        "CONTEXT BOUNDARY",
        "EVIDENCE POLICY",
        "DECISION / ESCALATION POLICY",
        "OUTPUT CONTRACT",
        "VERIFICATION CONTRACT",
        "ADAPTATION MAP",
        "INTEGRATION NOTES",
    ],
    "software-code-review-system.md": [
        "REVIEW POLICY",
        "REVIEW LENSES",
        "EVIDENCE POLICY",
        "SEVERITY POLICY",
        "SHIP DECISION POLICY",
        "VERIFICATION CONTRACT",
        "TEAM ADAPTATION MAP",
        "INTEGRATION SHAPES",
    ],
    "technical-research-decision-system.md": [
        "DECISION POLICY",
        "DECISION CRITERIA",
        "EVIDENCE SOURCE POLICY",
        "EVIDENCE QUALITY POLICY",
        "OPTION VIABILITY FILTER",
        "DECISION STATE POLICY",
        "DISCRIMINATING EXPERIMENT CONTRACT",
        "VERIFICATION CONTRACT",
        "ADAPTATION MAP",
    ],
}

MIN_CORE_TEMPLATE_BYTES = 6000


def fail(message: str) -> None:
    raise SystemExit(f"DEVELOPER PACK V1.1 QUALITY: FAIL — {message}")


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def main() -> None:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    readme = (PACK / "README.md").read_text(encoding="utf-8")
    spec = (PACK / "SPEC.md").read_text(encoding="utf-8")
    quickstart = (PACK / "QUICKSTART.md").read_text(encoding="utf-8")
    gate = (PACK / "quality" / "COMMERCIAL_VALUE_GATE.md").read_text(encoding="utf-8")

    for token in ("DRAFT", "NOT FOR SALE", "not observed == unknown"):
        if token not in readme:
            fail(f"README evidence/sale boundary missing: {token}")

    for token in (
        "Free vs Paid boundary",
        "Commercial value requirements",
        "Packaging rule",
        "Release exit criteria",
    ):
        if token not in spec:
            fail(f"SPEC product contract missing: {token}")

    for token in (
        "Free prompt clone test",
        "Worked transformation test",
        "Team adaptation test",
        "Machine/repeatable boundary test",
        "sale_status = NOT_FOR_SALE",
    ):
        if token not in gate:
            fail(f"commercial value gate missing: {token}")

    for token in (
        "Configure policy before instance data",
        "machine-readable contract",
        "Run the static review",
        "STATIC_READY_FOR_RUNTIME_TEST",
    ):
        if token not in quickstart:
            fail(f"Quickstart operating guidance missing: {token}")

    templates = PACK / "templates"
    example_path = PACK / "examples" / "code-review-policy-transformation.md"
    methodology_path = PACK / "methodology" / "adaptation-playbook.md"
    checklist_path = PACK / "checklists" / "workflow-static-review.md"

    customer_claim_surfaces = [
        readme,
        quickstart,
        example_path.read_text(encoding="utf-8"),
        methodology_path.read_text(encoding="utf-8"),
        checklist_path.read_text(encoding="utf-8"),
    ]
    customer_claim_surfaces.extend(
        path.read_text(encoding="utf-8") for path in sorted(templates.glob("*.md"))
    )
    customer_claim_text = "\n".join(customer_claim_surfaces).lower()

    for claim in FORBIDDEN_CLAIMS:
        if claim in customer_claim_text:
            fail(f"unsupported customer-facing marketing claim observed: {claim}")

    for filename, required_tokens in CORE_TEMPLATE_REQUIREMENTS.items():
        path = templates / filename
        size = path.stat().st_size
        if size < MIN_CORE_TEMPLATE_BYTES:
            fail(f"{filename} is below core template floor: {size} < {MIN_CORE_TEMPLATE_BYTES}")
        text = path.read_text(encoding="utf-8")
        for token in required_tokens:
            if token not in text:
                fail(f"{filename} missing operating interface: {token}")
        if "no behavioral claim" not in text.lower():
            fail(f"{filename} missing behavioral evidence boundary")

    schema = load_json(PACK / "contracts" / "workflow-contract.schema.json")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("workflow contract is not bound to JSON Schema draft 2020-12")
    required_fields = set(schema.get("required", []))
    for field in (
        "inputs",
        "context_policy",
        "evidence_policy",
        "decision_policy",
        "output_contract",
        "verification",
    ):
        if field not in required_fields:
            fail(f"workflow contract required interface missing: {field}")

    policy = load_json(PACK / "contracts" / "code-review-policy.example.json")
    if policy.get("contract_version") != "1.1":
        fail("code-review policy contract_version must be 1.1")
    if policy.get("decision_policy", {}).get("authority") != "human_decides":
        fail("code-review example must preserve explicit human ship authority")
    states = set(policy.get("decision_policy", {}).get("states", []))
    for state in ("BLOCK", "REVIEW_REQUIRED", "SHIP_WITH_FIXES", "NO_MATERIAL_ISSUE_FOUND"):
        if state not in states:
            fail(f"code-review policy decision state missing: {state}")
    if "F4 TESTED" not in policy.get("evidence_boundary", ""):
        fail("machine-readable contract missing Prompt Quarry evidence boundary")

    adaptation = methodology_path.read_text(encoding="utf-8")
    for token in (
        "INVARIANT",
        "POLICY",
        "INSTANCE_INPUT",
        "OPTIONAL_CONTEXT",
        "Change-control rule",
        "Adaptation anti-patterns",
    ):
        if token not in adaptation:
            fail(f"adaptation playbook missing: {token}")

    checklist = checklist_path.read_text(encoding="utf-8")
    for token in (
        "Outcome",
        "Evidence semantics",
        "Decision / escalation",
        "Verification",
        "Free-vs-Paid value check",
        "STATIC_REWORK_REQUIRED",
    ):
        if token not in checklist:
            fail(f"static workflow checklist missing: {token}")

    example = example_path.read_text(encoding="utf-8")
    for token in (
        "Starting request",
        "Extract the workflow requirements",
        "Configure the reusable template",
        "Resulting team operating prompt",
        "What the Paid system added",
        "Inspection checklist",
    ):
        if token not in example:
            fail(f"worked transformation incomplete: {token}")

    license_text = (PACK / "LICENSE.md").read_text(encoding="utf-8")
    for token in (
        "Prohibited redistribution and resale",
        "Adapted work inside your own product",
        "Evidence and performance boundary",
    ):
        if token not in license_text:
            fail(f"license boundary missing: {token}")

    print("DEVELOPER PACK V1.1 QUALITY: PASS")
    print(f"required_files={len(REQUIRED)}")
    print("sale_status=NOT_FOR_SALE")
    print("core_templates=3")
    print("machine_contracts=2")
    print("worked_transformations=1")
    print("gate=static product-value architecture only")
    print("boundary=no F4/F5/F6/F7 behavioral claim")


if __name__ == "__main__":
    main()
