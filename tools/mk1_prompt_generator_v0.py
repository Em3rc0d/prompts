from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from jsonschema import Draft202012Validator

from mk1_architecture_selector import select_architecture, validate_brief
from mk1_candidate_assembler import assemble_candidate, human_readable
from mk1_prompt_critic import critique_artifact


GENERATOR_VERSION = "0.1.0"
REQUEST_SCHEMA = Path("mk1/specs/PROMPT_GENERATOR_REQUEST.schema.json")
MK0_MANIFEST = Path("mk0/MANIFEST.json")
TECHNIQUE_MATRIX = Path("mk0/analysis/alpacka-ai-free-technique-matrix.json")
GOLDEN_MANIFEST = Path("mk0/golden-dataset/alpacka-free-golden-fixtures-manifest.json")
RIRO_PATTERN = Path("mk0/library/patterns/skill-design/role-intake-rules-output.md")

INTENT_PATTERNS = [
    ("rewrite", ["rewrite", "reescribe", "reescribir", "reformula", "reformular", "improve clarity", "mejorar claridad"]),
    ("summarize", ["summarize", "summary", "resume", "resumir", "resumen"]),
    ("troubleshoot", ["troubleshoot", "debug", "diagnose", "diagnostica", "diagnosticar", "why is", "por que falla", "por qué falla"]),
    ("audit", ["audit", "audita", "auditar", "compliance review"]),
    ("review", ["code review", "review code", "review this", "revisa el codigo", "revisa el código", "revisar codigo", "revisar código", "pull request"]),
    ("research", ["research", "investiga", "investigar", "technical research", "state of the art"]),
    ("compare", ["compare", "comparison", "compara", "comparar", "versus", " vs "]),
    ("decide", ["decide", "choose", "select", "decidir", "elige", "elegir", "escoger", "recommend which"]),
    ("plan", ["plan", "roadmap", "planifica", "planificar", "strategy", "estrategia"]),
    ("teach", ["teach", "explain to a", "enseña", "ensenar", "enseñar", "tutorial", "lesson"]),
    ("analyze", ["analyze", "analyse", "analiza", "analizar", "assessment", "evalua", "evalúa"]),
    ("generate", ["generate", "create ideas", "brainstorm", "genera", "generar", "crear ideas"]),
]

DOMAIN_PATTERNS = [
    ("software", ["code", "codigo", "código", "api", "database", "sql", "python", "javascript", "typescript", "java", "react", "backend", "frontend", "bug", "repository", "repo", "software"]),
    ("legal", ["legal", "law", "contract", "contrato", "jurisdiction", "jurisdiccion", "jurisdicción", "regulation", "regulacion", "regulación"]),
    ("health", ["medical", "medicine", "health", "clinical", "medico", "médico", "salud", "clinico", "clínico"]),
    ("finance", ["finance", "financial", "investment", "investing", "finanzas", "inversion", "inversión", "tax", "impuesto"]),
    ("marketing", ["marketing", "campaign", "conversion", "audience", "copywriting", "linkedin", "social media", "contenido", "content strategy"]),
    ("education", ["education", "student", "teacher", "course", "learn", "educacion", "educación", "estudiante", "curso", "aprender"]),
    ("research", ["research", "evidence", "benchmark", "paper", "study", "investigacion", "investigación", "evidencia", "estudio"]),
]

HIGH_STAKES_SIGNALS = [
    "medical", "clinical", "diagnosis", "legal advice", "compliance", "safety-critical",
    "patient", "health", "investment advice", "tax advice", "jurisdiction", "regulatory",
    "medico", "médico", "clinico", "clínico", "salud", "asesoria legal", "asesoría legal",
    "seguridad critica", "seguridad crítica", "inversion", "inversión", "impuesto", "jurisdiccion", "jurisdicción",
]

SPANISH_SIGNALS = [
    " el ", " la ", " los ", " las ", " que ", " para ", " con ", " una ", " quiero ",
    " revisar ", " crear ", " generar ", " comparar ", " investigar ", " código", "texto",
]

DOMAIN_TO_MK0_CATEGORIES = {
    "marketing": ["Marketing", "Copywriting", "IG reels", "Redes Sociales", "Negocios"],
    "education": ["Educación", "Idiomas"],
    "legal": ["Abogados"],
    "health": ["Salud"],
    "finance": ["Finanzas Personales", "Negocios"],
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_path(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _fold(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.casefold()
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return f" {normalized} "


def validate_request(payload: dict, schema_path: Path = REQUEST_SCHEMA) -> None:
    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.absolute_path))
    if errors:
        rendered = []
        for error in errors:
            where = ".".join(str(x) for x in error.absolute_path) or "<root>"
            rendered.append(f"{where}: {error.message}")
        raise ValueError("Invalid MK1 generator request:\n- " + "\n- ".join(rendered))


def _detect_language(text: str) -> str:
    folded = _fold(text)
    spanish_hits = sum(1 for token in SPANISH_SIGNALS if token in folded)
    return "es" if spanish_hits >= 2 else "en"


def _detect_intent(text: str) -> str:
    folded = _fold(text)
    for intent, patterns in INTENT_PATTERNS:
        if any(_fold(pattern).strip() in folded for pattern in patterns):
            return intent
    return "answer"


def _detect_domain(text: str) -> str:
    folded = _fold(text)
    scored = []
    for domain, patterns in DOMAIN_PATTERNS:
        score = sum(1 for pattern in patterns if _fold(pattern).strip() in folded)
        if score:
            scored.append((score, domain))
    if not scored:
        return "general"
    scored.sort(key=lambda row: (-row[0], row[1]))
    return scored[0][1]


def _detect_risk(text: str, domain: str) -> str:
    folded = _fold(text)
    if domain in {"legal", "health"}:
        return "high-stakes"
    if any(_fold(signal).strip() in folded for signal in HIGH_STAKES_SIGNALS):
        return "high-stakes"
    return "normal"


def _detect_complexity(intent: str, text: str) -> str:
    if intent in {"research", "compare", "decide", "audit", "troubleshoot"}:
        return "complex"
    if intent in {"review", "analyze", "plan", "teach", "generate"}:
        return "moderate"
    if len(text) > 450:
        return "moderate"
    return "simple"


def _default_inputs(intent: str, domain: str) -> dict:
    if intent == "rewrite":
        return {"required": ["text"], "optional": ["tone", "audience"]}
    if intent == "summarize":
        return {"required": ["source"], "optional": ["audience", "detail_level"]}
    if intent == "review":
        required = ["code", "technical_context"] if domain == "software" else ["subject", "context"]
        return {"required": required, "optional": ["review_scope"]}
    if intent == "audit":
        return {"required": ["subject", "audit_criteria"], "optional": ["context", "constraints"]}
    if intent == "troubleshoot":
        return {"required": ["symptom", "technical_context"], "optional": ["observations", "constraints"]}
    if intent in {"research", "compare", "decide"}:
        return {"required": ["problem", "decision_criteria"], "optional": ["known_options", "constraints", "current_context"]}
    if intent == "plan":
        return {"required": ["goal", "current_state"], "optional": ["constraints", "deadline"]}
    if intent == "teach":
        return {"required": ["topic"], "optional": ["learner_level", "learning_goal"]}
    if intent == "generate":
        return {"required": ["goal"], "optional": ["constraints", "audience", "tone"]}
    if intent == "analyze":
        return {"required": ["subject"], "optional": ["criteria", "context"]}
    return {"required": ["question"], "optional": ["context"]}


def _default_output_needs(intent: str) -> dict:
    if intent == "research":
        return {"structured": True, "alternatives": 3, "evidence": True, "citations": True}
    if intent in {"compare", "decide"}:
        return {"structured": True, "alternatives": 3, "evidence": True, "citations": False}
    if intent in {"review", "audit", "troubleshoot", "analyze"}:
        return {"structured": True, "alternatives": 1, "evidence": True, "citations": False}
    if intent == "generate":
        return {"structured": True, "alternatives": 3, "evidence": False, "citations": False}
    if intent in {"plan", "teach"}:
        return {"structured": True, "alternatives": 1, "evidence": False, "citations": False}
    return {"structured": False, "alternatives": 1, "evidence": False, "citations": False}


def _default_success_criteria(intent: str) -> list[str]:
    base = [
        "The result directly satisfies the declared task goal.",
        "Unsupported facts, evidence, tool results, or certainty are not invented.",
    ]
    specific = {
        "rewrite": "Material meaning, facts, numbers, negations, and ambiguity are preserved.",
        "summarize": "Material ideas and evidence are preserved without adding unsupported conclusions.",
        "review": "Findings are evidence-bound, prioritized, actionable, and distinguish confirmed defects from hypotheses.",
        "audit": "Every material finding is traceable to an audit criterion and concrete evidence.",
        "troubleshoot": "Hypotheses are separated from observations and include discriminating verification steps.",
        "research": "Alternatives are compared under common criteria with evidence, uncertainty, and trade-offs explicit.",
        "compare": "All alternatives are evaluated under the same declared criteria and trade-offs remain visible.",
        "decide": "The recommendation is traceable to criteria and states what evidence could change it.",
        "plan": "The plan exposes priorities, dependencies, risks, and observable progress criteria.",
        "teach": "The explanation matches the learner context and includes a useful comprehension check.",
        "generate": "Alternatives are materially distinct rather than cosmetic variations.",
        "analyze": "Observations, inferences, assumptions, and conclusions remain distinguishable.",
        "answer": "The direct answer is returned before optional detail.",
    }
    base.append(specific[intent])
    return base


def classify_request(payload: dict) -> tuple[dict, dict]:
    validate_request(payload)
    text = payload["request"].strip()
    intent = payload.get("intent") or _detect_intent(text)
    domain = payload.get("domain") or _detect_domain(text)
    risk = payload.get("risk") or _detect_risk(text, domain)
    complexity = payload.get("complexity") or _detect_complexity(intent, text)
    language = payload.get("language") or _detect_language(text)
    interaction = payload.get("interaction") or "intake-allowed"
    inputs = payload.get("inputs") or _default_inputs(intent, domain)
    output_needs = payload.get("output_needs") or _default_output_needs(intent)
    success_criteria = payload.get("success_criteria") or _default_success_criteria(intent)

    title = payload.get("title") or f"Generated {intent} prompt — {payload['request_id']}"
    brief = {
        "brief_id": payload["request_id"],
        "title": title,
        "intent": intent,
        "domain": domain,
        "risk": risk,
        "complexity": complexity,
        "goal": text,
        "inputs": inputs,
        "success_criteria": success_criteria,
        "interaction": interaction,
        "language": language,
        "constraints": payload.get("constraints") or [],
        "output_needs": output_needs,
        "model_targets": payload.get("model_targets") or ["model-agnostic"],
        "notes": payload.get("notes") or [],
    }
    validate_brief(brief)

    classification = {
        "generator_version": GENERATOR_VERSION,
        "request_id": payload["request_id"],
        "intent": intent,
        "domain": domain,
        "risk": risk,
        "complexity": complexity,
        "interaction": interaction,
        "language": language,
        "overrides": sorted(key for key in ("intent", "domain", "risk", "complexity", "interaction", "language", "inputs", "output_needs", "success_criteria") if key in payload),
        "policy": "Classification is deterministic/heuristic in v0. Explicit request fields override inference.",
    }
    return brief, classification


def retrieve_mk0(classification: dict) -> dict:
    manifest = _load_json(MK0_MANIFEST)
    matrix = _load_json(TECHNIQUE_MATRIX)
    golden = _load_json(GOLDEN_MANIFEST)

    top_techniques = [
        {
            "technique": name,
            "count": stats["count"],
            "percent": stats["percent"],
        }
        for name, stats in sorted(
            matrix["technique_presence"].items(),
            key=lambda item: (-item[1]["count"], item[0]),
        )[:10]
    ]

    mapped = DOMAIN_TO_MK0_CATEGORIES.get(classification["domain"], [])
    categories_available = set(matrix.get("category_counts", {}))
    relevant_categories = [
        {
            "category": category,
            "observed_records": matrix["category_counts"][category],
        }
        for category in mapped
        if category in categories_available
    ]

    return {
        "retrieval_version": "0.1.0",
        "request_id": classification["request_id"],
        "mk0_manifest": {
            "path": MK0_MANIFEST.as_posix(),
            "sha256": _sha256_path(MK0_MANIFEST),
            "characterized_snapshot": manifest["characterized_snapshot"],
        },
        "technique_matrix": {
            "path": TECHNIQUE_MATRIX.as_posix(),
            "sha256": _sha256_path(TECHNIQUE_MATRIX),
            "observed_records": matrix["records"],
            "top_observed_techniques": top_techniques,
        },
        "golden_dataset": {
            "path": GOLDEN_MANIFEST.as_posix(),
            "sha256": _sha256_path(GOLDEN_MANIFEST),
            "fixture_records": golden["fixture_records"],
            "techniques_covered": golden["techniques_covered"],
            "selection_policy": golden["selection_policy"],
        },
        "domain_evidence": {
            "requested_domain": classification["domain"],
            "relevant_observed_categories": relevant_categories,
            "domain_specific_evidence_available": bool(relevant_categories),
        },
        "truth_boundary": manifest["truth_boundary"],
        "policy": "MK0 teaches through characterized evidence. Retrieval does not copy source bodies and does not force high-frequency techniques into the prompt.",
    }


def select_techniques(brief: dict, retrieval: dict) -> tuple[dict, dict]:
    architecture = select_architecture(brief)
    matrix = _load_json(TECHNIQUE_MATRIX)
    golden = _load_json(GOLDEN_MANIFEST)
    presence = matrix["technique_presence"]
    covered = set(golden["techniques_covered"])

    support = []
    for technique in architecture["techniques"]:
        stats = presence.get(technique)
        support.append(
            {
                "technique": technique,
                "selected_by_task_contract": True,
                "mk0_observed": stats is not None,
                "observed_count": stats["count"] if stats else None,
                "observed_percent": stats["percent"] if stats else None,
                "golden_covered": technique in covered,
            }
        )

    selection = {
        "selection_version": "0.1.0",
        "request_id": brief["brief_id"],
        "techniques": support,
        "architecture_signature": architecture["architecture_signature"],
        "retrieval_refs": [
            retrieval["technique_matrix"]["path"],
            retrieval["golden_dataset"]["path"],
        ],
        "policy": "Task/risk/output requirements select techniques. MK0 frequency is supporting evidence, never an automatic inclusion rule.",
    }
    return architecture, selection


def _fix_provenance(artifact: dict, retrieval: dict) -> None:
    artifact["provenance"]["mk0_inputs"] = [
        retrieval["mk0_manifest"]["path"],
        retrieval["technique_matrix"]["path"],
        retrieval["golden_dataset"]["path"],
    ]
    artifact["provenance"]["patterns"] = [
        path.replace("library/", "mk0/library/", 1) if path.startswith("library/") else path
        for path in artifact["provenance"].get("patterns", [])
    ]
    artifact["provenance"]["knowledge_fingerprints"] = {
        "mk0_manifest": retrieval["mk0_manifest"]["sha256"],
        "technique_matrix": retrieval["technique_matrix"]["sha256"],
        "golden_dataset": retrieval["golden_dataset"]["sha256"],
    }


def _evaluation_plan(artifact_id: str) -> dict:
    return {
        "candidate": artifact_id,
        "f5_proof_contract": {
            "baseline_a": {
                "kind": "task-equivalent-minimal",
                "required": True,
                "purpose": "Prove the engineered candidate adds value over a fair minimal task-equivalent prompt.",
            },
            "baseline_b": {
                "kind": "best-comparable-mk0",
                "required": False,
                "purpose": "Optional stronger comparison against a genuinely task-equivalent MK0 prompt when exact source-body provenance and reuse rights/contract permit it.",
                "guardrail": "Do not compare against an unrelated MK0 prompt and do not reconstruct unavailable source bodies as if observed.",
            },
            "promotion_rule": "Only real F5 paired/blind evidence can establish improvement. Generator output alone remains static/VALID at best.",
        },
    }


def generate(payload: dict) -> dict:
    brief, classification = classify_request(payload)
    retrieval = retrieve_mk0(classification)
    architecture, technique_selection = select_techniques(brief, retrieval)

    artifact, assembled_architecture, lint = assemble_candidate(brief)
    if assembled_architecture["architecture_signature"] != architecture["architecture_signature"]:
        raise RuntimeError("Architecture selector drift between selection and assembler.")
    _fix_provenance(artifact, retrieval)

    # Re-run static checks after provenance enrichment.
    from mk1_prompt_linter import lint_artifact

    lint = lint_artifact(artifact)
    critic = critique_artifact(artifact)
    if lint["status"] != "PASS" or critic["status"] == "FAIL":
        generator_status = "REJECTED_STATIC"
    elif critic["status"] == "WARN":
        generator_status = "WARN_STATIC"
    else:
        generator_status = "VALID_STATIC"

    return {
        "generator_version": GENERATOR_VERSION,
        "request": payload,
        "brief": brief,
        "classification": classification,
        "retrieval": retrieval,
        "technique_selection": technique_selection,
        "architecture": architecture,
        "artifact": artifact,
        "lint": lint,
        "critic": critic,
        "generator_status": generator_status,
        "evaluation_plan": _evaluation_plan(artifact["id"]),
        "claim_boundary": "Generated/VALID_STATIC is not TESTED, IMPROVED, CERTIFIED, or PORTABLE.",
    }


def write_bundle(payload: dict, output_dir: str | Path) -> dict:
    result = generate(payload)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    files = {
        "request.json": result["request"],
        "task-brief.json": result["brief"],
        "classification.json": result["classification"],
        "mk0-retrieval.json": result["retrieval"],
        "technique-selection.json": result["technique_selection"],
        "architecture.json": result["architecture"],
        "artifact.json": result["artifact"],
        "lint.json": result["lint"],
        "critic.json": result["critic"],
        "evaluation-plan.json": result["evaluation_plan"],
    }
    for name, value in files.items():
        (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (output / "prompt.txt").write_text(
        human_readable(result["artifact"], result["architecture"], result["lint"]),
        encoding="utf-8",
    )
    generation_manifest = {
        "generator_version": GENERATOR_VERSION,
        "generator_status": result["generator_status"],
        "artifact_id": result["artifact"]["id"],
        "artifact_state": result["artifact"]["state"],
        "lint_status": result["lint"]["status"],
        "critic_status": result["critic"]["status"],
        "architecture_signature": result["architecture"]["architecture_signature"],
        "claim_boundary": result["claim_boundary"],
        "files": sorted(list(files) + ["prompt.txt", "generation.json"]),
    }
    (output / "generation.json").write_text(json.dumps(generation_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result["output_dir"] = output.as_posix()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt Quarry MK1 Prompt Generator v0")
    parser.add_argument("request", help="Path to a PROMPT_GENERATOR_REQUEST JSON file")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    payload = _load_json(Path(args.request))
    result = write_bundle(payload, args.output_dir)
    print(
        json.dumps(
            {
                "generator_version": GENERATOR_VERSION,
                "generator_status": result["generator_status"],
                "artifact_id": result["artifact"]["id"],
                "state": result["artifact"]["state"],
                "intent": result["classification"]["intent"],
                "domain": result["classification"]["domain"],
                "architecture_signature": result["architecture"]["architecture_signature"],
                "critic_status": result["critic"]["status"],
                "output_dir": result["output_dir"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    raise SystemExit(1 if result["generator_status"] == "REJECTED_STATIC" else 0)


if __name__ == "__main__":
    main()
