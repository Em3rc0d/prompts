from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from mk1_architecture_selector import select_architecture, validate_brief
from mk1_prompt_linter import lint_artifact


ASSEMBLER_VERSION = "1.0.0"

DOMAIN_ROLES_ES = {
    "software": "un especialista senior en ingeniería de software orientado a evidencia, trade-offs y verificación",
    "marketing": "un estratega de marketing orientado a experimentos, aprendizaje medible y claridad de audiencia",
    "legal": "un analista jurídico cuidadoso que distingue hechos, supuestos, jurisdicción e incertidumbre",
    "research": "un investigador analítico que separa evidencia, inferencia y recomendación",
    "education": "un diseñador instruccional que adapta profundidad y comprobación de comprensión al objetivo",
    "general": "un especialista práctico orientado al objetivo y a resultados verificables",
}

DOMAIN_ROLES_EN = {
    "software": "a senior software engineering specialist focused on evidence, trade-offs, and verification",
    "marketing": "a marketing strategist focused on measurable experiments, learning value, and audience clarity",
    "legal": "a careful legal analyst who separates facts, assumptions, jurisdiction, and uncertainty",
    "research": "an analytical researcher who separates evidence, inference, and recommendation",
    "education": "an instructional designer who adapts depth and comprehension checks to the learning goal",
    "general": "a practical specialist focused on the declared outcome and verifiable results",
}

PROCESS_ES = {
    "answer": ["Identifica la pregunta central.", "Usa sólo el contexto relevante.", "Entrega la respuesta directa antes de ampliar detalles."],
    "analyze": ["Define los criterios de análisis.", "Separa observaciones de inferencias.", "Evalúa cada criterio y sintetiza hallazgos.", "Prioriza conclusiones por impacto y evidencia."],
    "audit": ["Define criterios de revisión.", "Inspecciona cada área de forma sistemática.", "Clasifica hallazgos por severidad/evidencia.", "Propón acciones concretas y verificables."],
    "compare": ["Fija dimensiones de comparación comunes.", "Evalúa todas las opciones bajo los mismos criterios.", "Expón trade-offs y sensibilidad a supuestos.", "Concluye según los criterios declarados."],
    "decide": ["Aclara objetivo y restricciones.", "Define criterios de decisión y pesos cuando sean necesarios.", "Compara alternativas de forma consistente.", "Recomienda una opción y explica qué podría cambiar la decisión."],
    "generate": ["Aclara los criterios de diversidad y utilidad.", "Genera alternativas materialmente distintas.", "Descarta duplicados disfrazados.", "Ordena las mejores opciones según el objetivo."],
    "plan": ["Diagnostica el punto de partida.", "Define hitos y dependencias.", "Prioriza acciones por impacto/riesgo.", "Cierra con primeros pasos y criterios de progreso."],
    "research": ["Define la pregunta y los criterios de decisión.", "Recopila evidencia pertinente.", "Distingue evidencia primaria/secundaria e inferencias.", "Compara alternativas y formula una recomendación trazable."],
    "review": ["Comprende intención y contexto.", "Revisa corrección, riesgos y calidad.", "Prioriza hallazgos.", "Propón correcciones concretas y cómo verificarlas."],
    "rewrite": ["Conserva significado e intención.", "Elimina ambigüedad y ruido.", "Ajusta claridad/tono sin introducir hechos nuevos.", "Verifica fidelidad antes de devolver."],
    "summarize": ["Identifica ideas centrales y evidencia clave.", "Elimina repetición sin perder matices materiales.", "Distingue hechos, decisiones y pendientes cuando aplique.", "Entrega el nivel de detalle solicitado."],
    "teach": ["Comprueba el nivel inicial cuando sea necesario.", "Explica por bloques progresivos.", "Usa ejemplos o práctica relevante.", "Comprueba comprensión y corrige conceptos erróneos."],
    "troubleshoot": ["Define el síntoma y el estado esperado.", "Separa evidencia observada de hipótesis.", "Prioriza hipótesis por probabilidad/coste de verificación.", "Propón pruebas mínimas y criterios para confirmar o descartar cada causa."],
}

PROCESS_EN = {
    "answer": ["Identify the central question.", "Use only relevant context.", "Return the direct answer before optional detail."],
    "analyze": ["Define analysis criteria.", "Separate observations from inferences.", "Evaluate each criterion and synthesize findings.", "Prioritize conclusions by impact and evidence."],
    "audit": ["Define review criteria.", "Inspect each area systematically.", "Classify findings by severity and evidence.", "Propose concrete, verifiable actions."],
    "compare": ["Define shared comparison dimensions.", "Evaluate all options under the same criteria.", "Expose trade-offs and assumption sensitivity.", "Conclude against the declared criteria."],
    "decide": ["Clarify goal and constraints.", "Define decision criteria and weights when useful.", "Compare alternatives consistently.", "Recommend an option and state what could change the decision."],
    "generate": ["Clarify diversity and usefulness criteria.", "Generate materially distinct alternatives.", "Remove disguised duplicates.", "Rank the strongest options against the goal."],
    "plan": ["Diagnose the starting point.", "Define milestones and dependencies.", "Prioritize actions by impact and risk.", "Close with first actions and progress criteria."],
    "research": ["Define the question and decision criteria.", "Gather relevant evidence.", "Separate primary/secondary evidence from inference.", "Compare alternatives and produce a traceable recommendation."],
    "review": ["Understand intent and context.", "Review correctness, risks, and quality.", "Prioritize findings.", "Propose concrete fixes and verification steps."],
    "rewrite": ["Preserve meaning and intent.", "Remove ambiguity and noise.", "Improve clarity/tone without adding new facts.", "Verify fidelity before returning."],
    "summarize": ["Identify central ideas and key evidence.", "Remove repetition without losing material nuance.", "Separate facts, decisions, and open items when relevant.", "Return the requested level of detail."],
    "teach": ["Check the learner's starting level when necessary.", "Teach in progressive blocks.", "Use relevant examples or practice.", "Check understanding and correct misconceptions."],
    "troubleshoot": ["Define the symptom and expected state.", "Separate observed evidence from hypotheses.", "Prioritize hypotheses by likelihood and verification cost.", "Propose minimal tests and pass/fail criteria for each cause."],
}


def clean_id(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")
    return value or "candidate"


def _architecture_flags(selection: dict) -> dict:
    selected = set(selection["selected_blocks"])
    return {
        "purpose": "PURPOSE" in selected,
        "role": "ROLE" in selected,
        "context": "CONTEXT" in selected,
        "intake": "INTAKE" in selected,
        "assumptions": "ASSUMPTIONS" in selected,
        "process": "PROCESS" in selected,
        "constraints": "CONSTRAINTS" in selected,
        "output_contract": "OUTPUT_CONTRACT" in selected,
        "quality_gate": "QUALITY_GATE" in selected,
        "fallback": "FALLBACK" in selected,
    }


def _role(domain: str, language: str) -> str:
    key = domain.strip().casefold()
    if language == "en":
        return DOMAIN_ROLES_EN.get(key, f"an experienced {domain} specialist focused on evidence and useful outcomes")
    return DOMAIN_ROLES_ES.get(key, f"un especialista con experiencia en {domain} orientado a evidencia y resultados útiles")


def _sections(brief: dict, selection: dict) -> list[tuple[str, str]]:
    language = brief.get("language") or "es"
    if language == "mixed":
        language = "es"
    es = language != "en"
    selected = set(selection["selected_blocks"])
    required_inputs = brief["inputs"]["required"]
    optional_inputs = brief["inputs"]["optional"]
    output = brief["output_needs"]
    sections: list[tuple[str, str]] = []

    if "PURPOSE" in selected:
        heading = "PROPÓSITO" if es else "PURPOSE"
        body = brief["goal"]
        sections.append((heading, body))

    if "ROLE" in selected:
        heading = "ROL" if es else "ROLE"
        role = _role(brief["domain"], language)
        body = f"Actúa como {role}." if es else f"Act as {role}."
        sections.append((heading, body))

    if "CONTEXT" in selected:
        heading = "CONTEXTO" if es else "CONTEXT"
        lines = []
        if required_inputs:
            lines.append("Entradas requeridas:" if es else "Required inputs:")
            lines.extend(f"- {{{name}}}" for name in required_inputs)
        if optional_inputs:
            lines.append("Entradas opcionales:" if es else "Optional inputs:")
            lines.extend(f"- {{{name}}}" for name in optional_inputs)
        if brief.get("constraints"):
            lines.append("Restricciones del brief:" if es else "Brief constraints:")
            lines.extend(f"- {item}" for item in brief["constraints"])
        sections.append((heading, "\n".join(lines)))

    if "INTAKE" in selected:
        heading = "ENTRADA" if es else "INTAKE"
        if es:
            lines = [
                "Antes de ejecutar, comprueba si falta alguna entrada requerida que cambie materialmente el resultado.",
                "- Pregunta sólo por esas entradas faltantes.",
                "- No repitas preguntas sobre información ya proporcionada.",
                "- Si puedes avanzar de forma segura con un supuesto menor, decláralo en vez de bloquear innecesariamente.",
            ]
        else:
            lines = [
                "Before executing, check whether any missing required input would materially change the result.",
                "- Ask only for those missing inputs.",
                "- Do not repeat questions about information already supplied.",
                "- If a minor assumption is safe, label it instead of blocking unnecessarily.",
            ]
        sections.append((heading, "\n".join(lines)))

    if "ASSUMPTIONS" in selected:
        heading = "SUPUESTOS" if es else "ASSUMPTIONS"
        if es:
            body = (
                "Distingue hechos proporcionados, observaciones, inferencias y supuestos. "
                "No conviertas un supuesto en hecho. Si un supuesto puede cambiar materialmente la conclusión, señálalo antes de cerrar la respuesta."
            )
        else:
            body = (
                "Separate supplied facts, observations, inferences, and assumptions. "
                "Do not turn an assumption into a fact. If an assumption could materially change the conclusion, surface it before finalizing."
            )
        sections.append((heading, body))

    if "PROCESS" in selected:
        heading = "PROCESO" if es else "PROCESS"
        steps = (PROCESS_ES if es else PROCESS_EN)[brief["intent"]]
        sections.append((heading, "\n".join(f"{i}. {step}" for i, step in enumerate(steps, 1))))

    if "CONSTRAINTS" in selected:
        heading = "RESTRICCIONES" if es else "CONSTRAINTS"
        if es:
            rules = [
                "No inventes hechos, cifras, fuentes, resultados de herramientas ni contexto no proporcionado/observado.",
                "Separa hechos de recomendaciones e inferencias.",
            ]
            if output["evidence"]:
                rules.append("Toda afirmación material que dependa de evidencia debe quedar respaldada o marcada como no verificada.")
            if output["citations"]:
                rules.append("Incluye fuentes/citas para las afirmaciones materiales verificables cuando estén disponibles.")
            if brief["risk"] == "high-stakes":
                rules.extend(
                    [
                        "No presentes una conclusión de alto impacto como certeza cuando dependa de datos, jurisdicción o evaluación profesional faltante.",
                        "Distingue información general de consejo profesional individualizado y señala cuándo debe intervenir un profesional cualificado.",
                    ]
                )
        else:
            rules = [
                "Do not invent facts, figures, sources, tool results, or context that was not supplied or observed.",
                "Separate facts from recommendations and inferences.",
            ]
            if output["evidence"]:
                rules.append("Every material evidence-dependent claim must be supported or marked as unverified.")
            if output["citations"]:
                rules.append("Include sources/citations for material verifiable claims when available.")
            if brief["risk"] == "high-stakes":
                rules.extend(
                    [
                        "Do not present consequential conclusions as certain when required data, jurisdiction, or professional evaluation is missing.",
                        "Separate general information from individualized professional advice and indicate when qualified expertise is needed.",
                    ]
                )
        rules.extend(brief.get("constraints") or [])
        sections.append((heading, "\n".join(f"- {rule}" for rule in rules)))

    if "OUTPUT_CONTRACT" in selected:
        heading = "FORMATO DE SALIDA" if es else "OUTPUT CONTRACT"
        lines = []
        if output["alternatives"] > 1:
            lines.append(
                f"- Entrega {output['alternatives']} alternativas materialmente distintas." if es
                else f"- Return {output['alternatives']} materially distinct alternatives."
            )
        if output["structured"]:
            lines.append("- Usa una estructura consistente y escaneable." if es else "- Use a consistent, scannable structure.")
        if output["evidence"]:
            lines.append("- Separa evidencia, inferencia y recomendación." if es else "- Separate evidence, inference, and recommendation.")
        if output["citations"]:
            lines.append("- Incluye las fuentes/citas relevantes al final de cada afirmación o sección respaldada." if es else "- Attach relevant sources/citations to supported claims or sections.")
        lines.append("Criterios de éxito:" if es else "Success criteria:")
        lines.extend(f"- {criterion}" for criterion in brief["success_criteria"])
        sections.append((heading, "\n".join(lines)))

    if "QUALITY_GATE" in selected:
        heading = "VERIFICACIÓN" if es else "QUALITY GATE"
        if es:
            checks = [
                "Antes de devolver, confirma que cumpliste todos los criterios de éxito.",
                "Comprueba que no agregaste hechos no respaldados.",
                "Comprueba que las entradas requeridas fueron usadas o declaradas como faltantes.",
                "Elimina duplicación que no aporte valor.",
            ]
        else:
            checks = [
                "Before returning, confirm every success criterion is satisfied.",
                "Check that no unsupported facts were added.",
                "Check that required inputs were used or explicitly identified as missing.",
                "Remove duplication that adds no value.",
            ]
        sections.append((heading, "\n".join(f"- {check}" for check in checks)))

    if "FALLBACK" in selected:
        heading = "SI FALTA INFORMACIÓN" if es else "FALLBACK"
        if es:
            lines = [
                "- Si falta información crítica, identifica exactamente qué falta y por qué cambia el resultado.",
                "- Si la evidencia no puede verificarse, marca esa parte como no verificada en vez de inventarla.",
                "- Si existen varias interpretaciones plausibles, pide aclaración o presenta escenarios separados con sus supuestos.",
            ]
            if brief["risk"] == "high-stakes":
                lines.append("- Si la decisión requiere evaluación profesional o datos específicos no disponibles, limita la conclusión y recomienda la verificación apropiada.")
        else:
            lines = [
                "- If critical information is missing, state exactly what is missing and why it changes the result.",
                "- If evidence cannot be verified, mark it as unverified instead of inventing it.",
                "- If multiple interpretations are plausible, ask for clarification or present separate assumption-labeled scenarios.",
            ]
            if brief["risk"] == "high-stakes":
                lines.append("- If the decision requires unavailable professional evaluation or specific data, bound the conclusion and recommend appropriate verification.")
        sections.append((heading, "\n".join(lines)))

    return sections


def assemble_candidate(brief: dict) -> tuple[dict, dict, dict]:
    validate_brief(brief)
    selection = select_architecture(brief)
    sections = _sections(brief, selection)
    prompt_body = "\n\n".join(f"{heading}\n{body}" for heading, body in sections).strip() + "\n"

    patterns = []
    if {"ROLE", "INTAKE", "CONSTRAINTS", "OUTPUT_CONTRACT"}.issubset(set(selection["selected_blocks"])):
        patterns.append("library/patterns/skill-design/role-intake-rules-output.md")

    artifact = {
        "id": f"pq_mk1_{clean_id(brief['brief_id'])}",
        "version": "0.1.0",
        "state": "DRAFT",
        "artifact_type": "prompt",
        "title": brief["title"],
        "domain": brief["domain"],
        "intent": brief["intent"],
        "risk": brief["risk"],
        "language": brief.get("language") or "es",
        "model_targets": brief.get("model_targets") or ["model-agnostic"],
        "purpose": brief["goal"],
        "success_criteria": brief["success_criteria"],
        "inputs": brief["inputs"],
        "architecture": _architecture_flags(selection),
        "techniques": selection["techniques"],
        "prompt_body": prompt_body,
        "claims": ["engineered"],
        "provenance": {
            "mk0_inputs": [
                "quarry/analysis/alpacka-ai-free-technique-matrix.json",
                "quarry/fixtures/alpacka-free-golden-fixtures-manifest.json",
            ],
            "patterns": patterns,
            "fixtures": [],
            "source_families": ["src_alpacka_web"],
        },
        "evaluation": {
            "baseline_id": None,
            "fixture_set_id": None,
            "receipt_id": None,
            "rubric_score": None,
            "blocking_failures": [],
        },
        "created_at": None,
        "updated_at": None,
    }

    lint = lint_artifact(artifact)
    if lint["status"] == "PASS":
        artifact["state"] = "VALID"
        lint = lint_artifact(artifact)
    return artifact, selection, lint


def human_readable(artifact: dict, selection: dict, lint: dict) -> str:
    return (
        "PROMPT QUARRY — MK1 ENGINEERED CANDIDATE\n"
        + "=" * 88
        + f"\nTITLE             : {artifact['title']}"
        + f"\nID                : {artifact['id']}"
        + f"\nVERSION           : {artifact['version']}"
        + f"\nSTATE             : {artifact['state']}"
        + f"\nDOMAIN / INTENT   : {artifact['domain']} / {artifact['intent']}"
        + f"\nRISK              : {artifact['risk']}"
        + f"\nLINTER            : {lint['status']} ({lint['error_count']} errors, {lint['warning_count']} warnings, {lint['blocking_count']} blockers)"
        + f"\nARCHITECTURE      : {selection['architecture_signature']}"
        + "\nCLAIM             : engineered; NOT YET tested/certified/improved"
        + "\n\nWHAT THIS MEANS\n"
        + "-" * 88
        + "\nThis is an MK1 Prompt Forge candidate assembled from a task contract and MK0-derived design patterns."
        + "\nVALID means static contract/lint checks passed. It does NOT mean runtime-tested or CERTIFIED."
        + "\n\nPROMPT TO USE\n"
        + "-" * 88
        + "\n"
        + artifact["prompt_body"].rstrip()
        + "\n\nARCHITECTURE REASONS\n"
        + "-" * 88
        + "\n"
        + "\n".join(
            f"{block}: " + " | ".join(selection["reasons"].get(block, []))
            for block in selection["selected_blocks"]
        )
        + "\n\nPROVENANCE\n"
        + "-" * 88
        + "\nMK0 inputs:\n- "
        + "\n- ".join(artifact["provenance"]["mk0_inputs"])
        + ("\nPatterns:\n- " + "\n- ".join(artifact["provenance"]["patterns"]) if artifact["provenance"]["patterns"] else "\nPatterns: (none explicitly selected)")
        + "\n"
    )


def write_bundle(brief: dict, output_dir: str | Path) -> dict:
    artifact, selection, lint = assemble_candidate(brief)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "artifact.json").write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "architecture.json").write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "lint.json").write_text(json.dumps(lint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "prompt.txt").write_text(human_readable(artifact, selection, lint), encoding="utf-8")
    return {"artifact": artifact, "architecture": selection, "lint": lint, "output_dir": output.as_posix()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", help="Path to an MK1 Task Brief JSON")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))
    result = write_bundle(brief, args.output_dir)
    print(
        json.dumps(
            {
                "assembler_version": ASSEMBLER_VERSION,
                "artifact_id": result["artifact"]["id"],
                "state": result["artifact"]["state"],
                "lint_status": result["lint"]["status"],
                "architecture_signature": result["architecture"]["architecture_signature"],
                "output_dir": result["output_dir"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    raise SystemExit(0 if result["lint"]["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
