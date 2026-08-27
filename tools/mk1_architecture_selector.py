from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


SELECTOR_VERSION = "1.1.0"

BLOCK_ORDER = [
    "PURPOSE",
    "ROLE",
    "CONTEXT",
    "INTAKE",
    "ASSUMPTIONS",
    "PROCESS",
    "CONSTRAINTS",
    "OUTPUT_CONTRACT",
    "QUALITY_GATE",
    "FALLBACK",
]

ANALYTICAL_INTENTS = {
    "analyze",
    "audit",
    "compare",
    "decide",
    "plan",
    "research",
    "review",
    "teach",
    "troubleshoot",
}

DOMAIN_EXPERTISE_INTENTS = {
    "audit",
    "research",
    "review",
    "teach",
    "troubleshoot",
}

AMBIGUITY_SENSITIVE_INTENTS = {
    "analyze",
    "audit",
    "compare",
    "decide",
    "research",
    "rewrite",
    "troubleshoot",
}


def load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_brief(brief: dict, schema_path: str | Path = "mk1/specs/TASK_BRIEF.schema.json") -> None:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(brief), key=lambda e: list(e.absolute_path))
    if errors:
        rendered = []
        for error in errors:
            where = ".".join(str(x) for x in error.absolute_path) or "<root>"
            rendered.append(f"{where}: {error.message}")
        raise ValueError("Invalid MK1 task brief:\n- " + "\n- ".join(rendered))


def _add(selected: dict[str, bool], reasons: dict[str, list[str]], block: str, reason: str) -> None:
    selected[block] = True
    reasons.setdefault(block, []).append(reason)


def select_architecture(brief: dict) -> dict:
    """Select the smallest explainable MK1 architecture for a validated task brief."""

    intent = brief["intent"]
    domain = brief["domain"].strip().casefold()
    risk = brief["risk"]
    complexity = brief["complexity"]
    interaction = brief["interaction"]
    constraints = brief.get("constraints") or []
    required_inputs = brief["inputs"]["required"]
    optional_inputs = brief["inputs"]["optional"]
    output = brief["output_needs"]

    selected = {block: False for block in BLOCK_ORDER}
    reasons: dict[str, list[str]] = {}
    warnings: list[str] = []

    _add(selected, reasons, "PURPOSE", "Every MK1 artifact needs an explicit task outcome.")
    _add(selected, reasons, "OUTPUT_CONTRACT", "Every MK1 artifact needs observable output semantics.")

    generic_domains = {"general", "creative", "personal"}
    if risk == "high-stakes" or intent in DOMAIN_EXPERTISE_INTENTS or domain not in generic_domains:
        _add(
            selected,
            reasons,
            "ROLE",
            "Domain expertise, task intent or risk benefits from a constrained expert perspective.",
        )

    if required_inputs or optional_inputs or constraints or complexity != "simple":
        _add(
            selected,
            reasons,
            "CONTEXT",
            "The task depends on supplied variables, constraints or non-trivial operating context.",
        )

    if interaction != "one-shot" and required_inputs:
        _add(
            selected,
            reasons,
            "INTAKE",
            "Interaction permits targeted questions for missing required inputs.",
        )

    if risk == "high-stakes" or complexity != "simple" or intent in AMBIGUITY_SENSITIVE_INTENTS:
        _add(
            selected,
            reasons,
            "ASSUMPTIONS",
            "The task needs explicit handling of inference, ambiguity or consequential uncertainty.",
        )

    if complexity != "simple" or intent in ANALYTICAL_INTENTS:
        _add(
            selected,
            reasons,
            "PROCESS",
            "Decomposition or method is expected to improve reliability for this task.",
        )

    if constraints or risk == "high-stakes" or output["evidence"] or output["citations"] or intent in {
        "audit",
        "research",
        "review",
        "troubleshoot",
    }:
        _add(
            selected,
            reasons,
            "CONSTRAINTS",
            "The brief contains truth, evidence, safety or task-specific invariants.",
        )

    if risk == "high-stakes" or complexity != "simple" or intent in {
        "analyze",
        "audit",
        "compare",
        "decide",
        "plan",
        "research",
        "review",
        "rewrite",
        "summarize",
        "troubleshoot",
    }:
        _add(
            selected,
            reasons,
            "QUALITY_GATE",
            "The result benefits from an explicit final contract/self-check before return.",
        )

    if interaction != "one-shot" or risk == "high-stakes" or output["evidence"] or output["citations"] or intent in {
        "decide",
        "research",
        "troubleshoot",
    }:
        _add(
            selected,
            reasons,
            "FALLBACK",
            "The task needs defined behavior when information or evidence is insufficient.",
        )

    techniques: list[str] = []

    def technique(name: str) -> None:
        if name not in techniques:
            techniques.append(name)

    if selected["ROLE"]:
        technique("role-assignment")
    if selected["CONTEXT"]:
        technique("context-injection")
    if selected["INTAKE"]:
        technique("question-first")
        technique("variable-template")
    elif required_inputs:
        technique("variable-template")
    if selected["ASSUMPTIONS"]:
        technique("assumption-audit")
    if selected["PROCESS"]:
        technique("task-decomposition")
        technique("stepwise-procedure")
    if selected["CONSTRAINTS"]:
        technique("explicit-constraints")
    if output["structured"]:
        technique("output-schema")
    else:
        technique("output-formatting")
    if output["alternatives"] > 1:
        technique("alternative-generation")
    if selected["QUALITY_GATE"]:
        technique("self-check")
    if output["evidence"]:
        technique("evidence-requirement")
    if output["citations"]:
        technique("source-requirement")
        if not output["evidence"]:
            warnings.append("citations=true while evidence=false; citations imply an evidence-bearing task.")
    if selected["FALLBACK"]:
        technique("fallback-behavior")
    if risk == "high-stakes":
        technique("confidence-labeling")
        technique("safety-boundary")

    selected_blocks = [block for block in BLOCK_ORDER if selected[block]]
    omitted_blocks = [block for block in BLOCK_ORDER if not selected[block]]

    return {
        "selector_version": SELECTOR_VERSION,
        "brief_id": brief["brief_id"],
        "intent": intent,
        "domain": brief["domain"],
        "risk": risk,
        "complexity": complexity,
        "selected_blocks": selected_blocks,
        "omitted_blocks": omitted_blocks,
        "architecture_signature": "+".join(selected_blocks),
        "techniques": techniques,
        "reasons": reasons,
        "warnings": warnings,
        "policy": "Select the smallest purposeful architecture. Section count is not a quality metric.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", help="Path to an MK1 task brief JSON file")
    parser.add_argument("--schema", default="mk1/specs/TASK_BRIEF.schema.json")
    parser.add_argument("--output")
    args = parser.parse_args()

    brief = load_json(args.brief)
    validate_brief(brief, args.schema)
    result = select_architecture(brief)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
