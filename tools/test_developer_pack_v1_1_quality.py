#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "product" / "developer-pack-v1.1"

REQUIRED = [
    PACK / "README.md",
    PACK / "SPEC.md",
    PACK / "LICENSE.md",
    PACK / "quality" / "COMMERCIAL_VALUE_GATE.md",
    PACK / "templates" / "general-operating-contract.md",
    PACK / "templates" / "software-code-review-system.md",
    PACK / "templates" / "technical-research-decision-system.md",
    PACK / "examples" / "code-review-policy-transformation.md",
]

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


def main() -> None:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    readme = (PACK / "README.md").read_text(encoding="utf-8")
    spec = (PACK / "SPEC.md").read_text(encoding="utf-8")
    gate = (PACK / "quality" / "COMMERCIAL_VALUE_GATE.md").read_text(encoding="utf-8")
    corpus = "\n".join(p.read_text(encoding="utf-8") for p in REQUIRED)
    lower = corpus.lower()

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

    for claim in FORBIDDEN_CLAIMS:
        if claim in lower:
            fail(f"unsupported marketing claim observed: {claim}")

    templates = PACK / "templates"
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

    example = (PACK / "examples" / "code-review-policy-transformation.md").read_text(encoding="utf-8")
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
    for token in ("Prohibited redistribution and resale", "Adapted work inside your own product", "Evidence and performance boundary"):
        if token not in license_text:
            fail(f"license boundary missing: {token}")

    print("DEVELOPER PACK V1.1 QUALITY: PASS")
    print(f"required_files={len(REQUIRED)}")
    print("sale_status=NOT_FOR_SALE")
    print("core_templates=3")
    print("worked_transformations=1")
    print("gate=static product-value architecture only")
    print("boundary=no F4/F5/F6/F7 behavioral claim")


if __name__ == "__main__":
    main()
