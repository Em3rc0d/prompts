from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator


LINTER_VERSION = "1.0.0"

SECTION_ALIASES = {
    "purpose": ["PURPOSE", "PROPÓSITO", "PROPOSITO", "OBJETIVO"],
    "role": ["ROLE", "ROL"],
    "context": ["CONTEXT", "CONTEXTO"],
    "intake": ["INTAKE", "ENTRADA", "PREGUNTAS", "INFORMACIÓN NECESARIA", "INFORMACION NECESARIA"],
    "assumptions": ["ASSUMPTIONS", "SUPUESTOS", "ASUNCIONES"],
    "process": ["PROCESS", "PROCESO", "MÉTODO", "METODO"],
    "constraints": ["CONSTRAINTS", "REGLAS", "RESTRICCIONES"],
    "output_contract": ["OUTPUT CONTRACT", "FORMATO DE SALIDA", "SALIDA", "ENTREGABLE"],
    "quality_gate": ["QUALITY GATE", "VERIFICACIÓN", "VERIFICACION", "AUTO-VERIFICACIÓN", "AUTO-VERIFICACION", "CHECKLIST"],
    "fallback": ["FALLBACK", "INCERTIDUMBRE", "SI FALTA INFORMACIÓN", "SI FALTA INFORMACION"],
}

STATE_ORDER_REQUIRING_FIXTURES = {"TESTED", "CANDIDATE", "CERTIFIED"}
STATE_ORDER_REQUIRING_RECEIPT = {"CANDIDATE", "CERTIFIED"}


def load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _schema_errors(artifact: dict, schema_path: str | Path) -> list[dict]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    findings: list[dict] = []
    for error in sorted(validator.iter_errors(artifact), key=lambda e: list(e.absolute_path)):
        where = ".".join(str(x) for x in error.absolute_path) or "<root>"
        findings.append(
            {
                "severity": "error",
                "code": "schema",
                "message": f"{where}: {error.message}",
            }
        )
    return findings


def _has_heading(body: str, aliases: list[str]) -> bool:
    lines = [line.strip().upper().rstrip(":") for line in body.splitlines()]
    normalized_aliases = {alias.upper().rstrip(":") for alias in aliases}
    return any(line in normalized_aliases for line in lines)


def lint_artifact(
    artifact: dict,
    schema_path: str | Path = "mk1/specs/PROMPT_ARTIFACT.schema.json",
) -> dict:
    findings = _schema_errors(artifact, schema_path)
    if findings:
        return {
            "linter_version": LINTER_VERSION,
            "artifact_id": artifact.get("id"),
            "status": "FAIL",
            "findings": findings,
            "error_count": len(findings),
            "warning_count": 0,
            "blocking_count": 0,
        }

    body = artifact["prompt_body"]
    architecture = artifact["architecture"]
    techniques = set(artifact.get("techniques") or [])
    state = artifact["state"]
    risk = artifact["risk"]
    evaluation = artifact["evaluation"]
    claims = set(artifact.get("claims") or [])

    def add(severity: str, code: str, message: str) -> None:
        findings.append({"severity": severity, "code": code, "message": message})

    if not architecture["purpose"]:
        add("error", "purpose-disabled", "MK1 architecture must include PURPOSE.")
    if not architecture["output_contract"]:
        add("error", "output-contract-disabled", "MK1 architecture must include OUTPUT_CONTRACT.")

    for block, enabled in architecture.items():
        aliases = SECTION_ALIASES[block]
        present = _has_heading(body, aliases)
        if enabled and not present:
            add("error", "missing-section", f"Architecture declares {block}=true but no matching heading is present.")
        elif not enabled and present:
            add("warning", "undeclared-section", f"Prompt contains a {block} section but architecture declares it false.")

    declared_inputs = set(artifact["inputs"]["required"]) | set(artifact["inputs"]["optional"])
    placeholders = {match.strip() for match in re.findall(r"\{([^{}]+)\}", body)}
    undefined = sorted(placeholders - declared_inputs)
    for name in undefined:
        add("error", "undefined-variable", f"Prompt references {{{name}}} but it is not declared in inputs.")

    unused_required = sorted(set(artifact["inputs"]["required"]) - placeholders)
    for name in unused_required:
        add("warning", "unused-required-input", f"Required input '{name}' is not referenced as a prompt placeholder.")

    lowered = body.casefold()
    if architecture["intake"] and re.search(r"\b(no|nunca)\s+(hagas|realices|formules|uses)\s+preguntas\b", lowered):
        add("error", "contradictory-intake", "INTAKE is enabled but the body also forbids asking questions.")

    if risk == "high-stakes":
        required_blocks = ["assumptions", "constraints", "fallback", "quality_gate"]
        for block in required_blocks:
            if not architecture[block]:
                add("blocking", "high-stakes-missing-block", f"High-stakes prompt requires {block} architecture.")
        for technique_name in ["safety-boundary", "confidence-labeling"]:
            if technique_name not in techniques:
                add("blocking", "high-stakes-missing-technique", f"High-stakes prompt requires technique '{technique_name}'.")

    if "improved" in claims:
        if not evaluation.get("baseline_id"):
            add("blocking", "improved-without-baseline", "Claim 'improved' requires baseline_id.")
        if not evaluation.get("fixture_set_id"):
            add("blocking", "improved-without-fixtures", "Claim 'improved' requires fixture_set_id.")
        if not evaluation.get("receipt_id"):
            add("blocking", "improved-without-receipt", "Claim 'improved' requires receipt_id.")
        if evaluation.get("rubric_score") is None:
            add("blocking", "improved-without-score", "Claim 'improved' requires rubric_score.")

    if state in STATE_ORDER_REQUIRING_FIXTURES and not evaluation.get("fixture_set_id"):
        add("error", "state-without-fixtures", f"State {state} requires fixture_set_id.")

    if state in STATE_ORDER_REQUIRING_RECEIPT and not evaluation.get("receipt_id"):
        add("error", "state-without-receipt", f"State {state} requires receipt_id.")

    if state == "CERTIFIED":
        score = evaluation.get("rubric_score")
        if score is None or score < 85:
            add("blocking", "certified-score", "CERTIFIED requires rubric_score >= 85.")
        if evaluation.get("blocking_failures"):
            add("blocking", "certified-with-blockers", "CERTIFIED artifact cannot retain blocking_failures.")
        if "certified" not in claims:
            add("warning", "certified-claim-missing", "State is CERTIFIED but claims does not include 'certified'.")

    if "tested" in claims and state not in {"TESTED", "CANDIDATE", "CERTIFIED", "DEPRECATED"}:
        add("warning", "tested-claim-state-mismatch", "Claim 'tested' is present but state does not represent a tested artifact.")

    provenance = artifact["provenance"]
    if not any(provenance.get(key) for key in ("mk0_inputs", "patterns", "fixtures", "source_families")):
        add("warning", "empty-provenance", "MK1 artifact has no declared MK0/pattern/fixture/source-family provenance.")

    error_count = sum(1 for f in findings if f["severity"] == "error")
    warning_count = sum(1 for f in findings if f["severity"] == "warning")
    blocking_count = sum(1 for f in findings if f["severity"] == "blocking")
    status = "PASS" if error_count == 0 and blocking_count == 0 else "FAIL"

    return {
        "linter_version": LINTER_VERSION,
        "artifact_id": artifact["id"],
        "status": status,
        "findings": findings,
        "error_count": error_count,
        "warning_count": warning_count,
        "blocking_count": blocking_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", help="Path to an MK1 prompt artifact JSON")
    parser.add_argument("--schema", default="mk1/specs/PROMPT_ARTIFACT.schema.json")
    parser.add_argument("--output")
    args = parser.parse_args()

    artifact = load_json(args.artifact)
    result = lint_artifact(artifact, args.schema)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
