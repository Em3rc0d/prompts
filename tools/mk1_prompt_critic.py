from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from mk1_prompt_linter import lint_artifact


CRITIC_VERSION = "1.1.0"

HEADING_NAMES = {
    "purpose", "propósito", "proposito", "objetivo",
    "role", "rol", "context", "contexto", "intake", "entrada",
    "assumptions", "supuestos", "process", "proceso", "método", "metodo",
    "constraints", "restricciones", "reglas", "output contract", "formato de salida",
    "salida", "entregable", "quality gate", "verificación", "verificacion",
    "fallback", "si falta información", "si falta informacion", "incertidumbre",
}

CONTRADICTION_RULES = [
    (
        "questions-required-vs-forbidden",
        [r"\b(pregunta|pregunte|ask)\b", r"\b(solicita|solicite|request)\b"],
        [
            r"\bno\s+(?:hagas|formules|realices|uses)\s+preguntas\b",
            r"\bnunca\s+(?:hagas|formules|realices)?\s*preguntas\b",
            r"\b(?:never|do not|don't)\s+ask\s+(?:any\s+)?questions?\b",
        ],
        "The prompt both enables/requests clarification and forbids questions.",
    ),
    (
        "explanation-required-vs-output-only",
        [r"\b(explica|explain|razona|reasoning|justifica|justify)\b"],
        [r"\b(solo|sólo|only)\b.{0,30}\b(resultado|respuesta|texto|answer|output|revised text)\b"],
        "The prompt asks for explanation/reasoning while also requiring only the final output.",
    ),
    (
        "certainty-vs-uncertainty",
        [r"\b(debes asegurar|garantiza|guarantee|be certain|certainty)\b"],
        [r"\b(no verificada|unverified|incertidumbre|uncertainty|supuesto|assumption)\b"],
        "The prompt mixes absolute-certainty instructions with explicit uncertainty handling.",
    ),
]

VAGUE_OUTPUT_TERMS = {
    "buena respuesta", "best answer", "respuesta útil", "useful answer", "resultado completo",
    "complete result", "de forma profesional", "professionally", "lo mejor posible", "as best as possible",
}

PROVENANCE_LAUNDERING_PATTERNS = [
    r"\b(original premium prompt|prompt premium original)\b",
    r"\b(verbatim source|fuente textual exacta|texto exacto de la fuente)\b",
    r"\b(reproduce exactly the source|reproduce exactamente la fuente)\b",
]

UNSUPPORTED_ASSUMPTION_PATTERNS = [
    r"\bassume that\b",
    r"\bassume the user\b",
    r"\bpresume that\b",
    r"\basume que\b",
    r"\bpresume que\b",
    r"\bda por hecho\b",
]


def _fold(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.casefold()
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _meaningful_lines(body: str) -> list[tuple[int, str, str]]:
    rows = []
    folded_headings = {_fold(x) for x in HEADING_NAMES}
    for idx, raw in enumerate(body.splitlines(), 1):
        text = raw.strip()
        if not text:
            continue
        folded = _fold(text.rstrip(":"))
        if folded in folded_headings:
            continue
        if len(folded) < 18:
            continue
        rows.append((idx, text, folded))
    return rows


def _section(body: str, aliases: set[str]) -> str:
    lines = body.splitlines()
    normalized_aliases = {_fold(a) for a in aliases}
    folded_headings = {_fold(x) for x in HEADING_NAMES}
    start = None
    collected = []
    for line in lines:
        stripped = line.strip().rstrip(":")
        folded = _fold(stripped)
        if folded in folded_headings:
            if start is not None:
                break
            if folded in normalized_aliases:
                start = True
            continue
        if start is not None:
            collected.append(line)
    return "\n".join(collected).strip()


def _add(findings: list[dict], severity: str, code: str, message: str, remediation: str, evidence=None) -> None:
    record = {"severity": severity, "code": code, "message": message, "remediation": remediation}
    if evidence is not None:
        record["evidence"] = evidence
    findings.append(record)


def critique_artifact(artifact: dict) -> dict:
    lint = lint_artifact(artifact)
    findings: list[dict] = []
    body = artifact.get("prompt_body") or ""
    folded_body = _fold(body)
    architecture = artifact.get("architecture") or {}
    intent = artifact.get("intent")
    risk = artifact.get("risk")

    if lint["status"] != "PASS":
        _add(findings, "error", "linter-not-pass", "The artifact has not passed the MK1 structural linter.", "Resolve linter errors/blockers before interpreting critic results as a quality pass.", {"errors": lint["error_count"], "blockers": lint["blocking_count"]})

    meaningful = _meaningful_lines(body)
    counter = Counter(row[2] for row in meaningful)
    duplicates = {text for text, count in counter.items() if count > 1}
    for duplicate in sorted(duplicates):
        matches = [{"line": line, "text": text} for line, text, folded in meaningful if folded == duplicate]
        _add(findings, "warning", "duplicate-instruction", "The same non-trivial instruction appears multiple times.", "Keep the instruction in the block that owns the responsibility and remove repeated copies elsewhere.", matches)

    normalized_rows = []
    for line, text, folded in meaningful:
        semantic = re.sub(r"^(?:[-*]|\d+[.)])\s*", "", folded).strip()
        semantic = re.sub(r"\b(brief|contexto|context)\b\s*:?", "", semantic).strip()
        normalized_rows.append((line, text, semantic))
    semantic_counter = Counter(row[2] for row in normalized_rows if len(row[2]) >= 24)
    for duplicate, count in semantic_counter.items():
        if count > 1 and duplicate not in duplicates:
            matches = [{"line": line, "text": text} for line, text, semantic in normalized_rows if semantic == duplicate]
            _add(findings, "warning", "near-duplicate-instruction", "Semantically equivalent instruction lines appear more than once.", "Consolidate repeated constraints/context into one authoritative section.", matches)

    for code, positive_patterns, negative_patterns, message in CONTRADICTION_RULES:
        positive = any(re.search(pattern, folded_body, re.IGNORECASE) for pattern in positive_patterns)
        negative = any(re.search(pattern, folded_body, re.IGNORECASE) for pattern in negative_patterns)
        if positive and negative:
            _add(findings, "error", code, message, "Choose one contract or explicitly scope when each behavior applies.")

    output_text = _section(body, {"OUTPUT CONTRACT", "FORMATO DE SALIDA", "SALIDA", "ENTREGABLE"})
    if architecture.get("output_contract"):
        if len(output_text) < 40:
            _add(findings, "error", "vague-output-contract", "OUTPUT_CONTRACT is present but too weak to make success observable.", "Specify required fields/sections, number of alternatives, ordering, decision criteria, or other verifiable deliverables.", output_text)
        elif any(term in _fold(output_text) for term in {_fold(t) for t in VAGUE_OUTPUT_TERMS}) and not re.search(r"(^|\n)\s*[-*\d]", output_text):
            _add(findings, "warning", "generic-output-language", "The output contract relies on generic quality adjectives without enough verifiable structure.", "Replace generic adjectives with observable deliverables or evaluation criteria.", output_text)

    intent_requirements = {
        "review": ["hallazgo", "finding", "severidad", "severity", "fix", "correcci", "verific"],
        "audit": ["hallazgo", "finding", "severidad", "severity", "riesgo", "risk", "accion", "action"],
        "compare": ["criterio", "criteria", "trade-off", "compar", "recommend"],
        "research": ["evidencia", "evidence", "fuente", "source", "recomend", "recommend", "trade-off"],
        "troubleshoot": ["hipotes", "hypothes", "prueba", "test", "evidence", "evidencia"],
    }
    if intent in intent_requirements and output_text:
        hits = sum(1 for token in intent_requirements[intent] if token in _fold(output_text))
        if hits < 2:
            _add(findings, "warning", "intent-output-under-specified", f"The {intent} output contract does not expose enough intent-specific fields/criteria.", "Make the deliverable encode the core decision/review fields instead of relying only on general success criteria.", {"matched_signals": hits, "required_signal_family": intent_requirements[intent]})

    assumption_text = _section(body, {"ASSUMPTIONS", "SUPUESTOS"})
    unsupported_matches = []
    for pattern in UNSUPPORTED_ASSUMPTION_PATTERNS:
        unsupported_matches.extend(match.group(0) for match in re.finditer(pattern, body, re.IGNORECASE))
    if unsupported_matches and not architecture.get("assumptions"):
        _add(findings, "error", "assumption-without-contract", "The prompt instructs assumptions but has no ASSUMPTIONS architecture block.", "Add explicit assumption handling or remove the assumption instruction.", unsupported_matches)
    if architecture.get("assumptions") and len(assumption_text) < 40:
        _add(findings, "warning", "weak-assumption-contract", "ASSUMPTIONS exists but does not clearly define how inference should be labeled/handled.", "State what may be inferred, what must be labeled, and when missing information must stop or branch execution.", assumption_text)

    for pattern in PROVENANCE_LAUNDERING_PATTERNS:
        if re.search(pattern, body, re.IGNORECASE):
            _add(findings, "blocking", "provenance-laundering-language", "Prompt wording implies access to exact/original source content without an evidence contract proving that wording is available.", "Remove the source-reproduction claim or attach explicit source-body provenance that justifies it.", pattern)

    if risk == "high-stakes":
        fallback_text = _section(body, {"FALLBACK", "SI FALTA INFORMACIÓN", "SI FALTA INFORMACION", "INCERTIDUMBRE"})
        constraints_text = _section(body, {"CONSTRAINTS", "RESTRICCIONES", "REGLAS"})
        high_stakes_signals = ["profesional", "professional", "jurisdic", "uncertainty", "incertid", "no verificada", "unverified"]
        combined = _fold(fallback_text + "\n" + constraints_text)
        if sum(1 for token in high_stakes_signals if token in combined) < 2:
            _add(findings, "blocking", "high-stakes-boundary-too-generic", "High-stakes blocks exist, but their wording is too generic to establish a consequential uncertainty/professional boundary.", "Add domain-relevant uncertainty, missing-evidence, jurisdiction/data and escalation behavior.")

    # Overfit is about unjustified ceremony, not raw section count. A simple rewrite may
    # legitimately need intake/assumptions/fallback when its brief explicitly permits intake
    # and contains semantic-fidelity / untrusted-input constraints. ROLE + PROCESS are the
    # strongest ceremony signals for a low-risk simple transformation; near-full vocabulary
    # remains suspicious regardless of exact ordering.
    enabled_count = sum(1 for value in architecture.values() if value)
    simple_transform = intent in {"rewrite", "summarize", "answer"} and risk == "low"
    ceremony_blocks = [name for name in ("role", "process") if architecture.get(name)]
    near_full_vocabulary = enabled_count >= 9
    if simple_transform and enabled_count >= 8 and (near_full_vocabulary or len(ceremony_blocks) == 2):
        _add(
            findings,
            "warning",
            "architecture-overfit",
            "A low-risk simple intent uses near-full architecture or adds both ROLE and PROCESS ceremony.",
            "Remove blocks that do not materially improve task reliability; keep reliability blocks only when the brief or failure modes justify them.",
            {"enabled_blocks": enabled_count, "ceremony_blocks": ceremony_blocks},
        )

    severity_counts = Counter(f["severity"] for f in findings)
    status = "FAIL" if severity_counts["blocking"] or severity_counts["error"] else ("WARN" if severity_counts["warning"] else "PASS")

    return {
        "critic_version": CRITIC_VERSION,
        "artifact_id": artifact.get("id"),
        "status": status,
        "findings": findings,
        "counts": {"blocking": severity_counts["blocking"], "error": severity_counts["error"], "warning": severity_counts["warning"]},
        "linter_status": lint["status"],
        "policy": "F3 critic is a static quality characterization layer. PASS does not imply behavioral testing or certification.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("--output")
    args = parser.parse_args()
    artifact = json.loads(Path(args.artifact).read_text(encoding="utf-8"))
    result = critique_artifact(artifact)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    raise SystemExit(0 if result["status"] != "FAIL" else 1)


if __name__ == "__main__":
    main()
