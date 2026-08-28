from __future__ import annotations

import re

GOLDEN_ARTIFACTS = {"PROMPT", "AGENT_INSTRUCTION"}
REFERENCE_ARTIFACTS = {
    "ARCHITECTURE_DOCUMENTATION", "CODEBASE_GUIDE", "DESIGN_SPEC",
    "IMPLEMENTATION_PLAN", "DOCUMENTATION", "MANUAL", "FAQ", "LOG_CHANGELOG",
}


def _has(text: str, *terms: str) -> bool:
    t = text.casefold()
    return any(term.casefold() in t for term in terms)


def _epistemic(disposition: str) -> tuple[bool, str]:
    if disposition == "GOLDEN_EVALUATION":
        return True, "CANONICAL_CANDIDATE_ONLY"
    if disposition == "REFERENCE_CORPUS":
        return False, "NON_CANONICAL_REFERENCE"
    if disposition == "REJECT":
        return False, "NON_USABLE"
    return False, "UNRESOLVED"


def _is_operational_skill(body: str, source_type: str) -> bool:
    """Recognize a persistent AI skill contract without trusting the filename alone.

    A SKILL.md-like source is promoted semantically only when it contains both
    skill metadata/identity and normative operating instructions. This avoids
    treating ordinary documentation that happens to be named SKILL.md as Golden
    material.
    """
    if source_type != "skill":
        return False

    frontmatter = bool(re.search(r"\A---\s*\n(?:(?!\n---\s*$).)*?\nname:\s*.+?\n(?:(?!\n---\s*$).)*?description:\s*.+?\n(?:(?!\n---\s*$).)*?\n---\s*", body, re.I | re.M | re.S))
    identity = _has(body, "use this skill", "this skill", "installed skill", "skill provides")
    operating_sections = sum(
        1 for term in (
            "operating contract",
            "required workflow",
            "safety gate",
            "safety gates",
            "workflow",
            "policy",
            "protocol",
        ) if term in body.casefold()
    )
    normative = sum(
        1 for term in (" must ", " never ", " do not ", " follow ", " use ", " ask ", " block ")
        if term in f" {body.casefold()} "
    )
    return frontmatter and identity and operating_sections >= 2 and normative >= 3


def classify_artifact(title: str, body: str, source_type: str) -> dict:
    """Deterministic pre-quality semantic gate.

    This gate answers what the artifact IS, not how polished it looks.
    Reference material is preserved as explicitly non-canonical. Ambiguous
    cases remain reviewable instead of being silently promoted.

    Precedence is semantic: explicit agent-operating instructions outrank
    incidental documentation words; explicit document identity outranks
    prompt-like phrases embedded inside manuals or reference material.
    """
    text = f"{title}\n{body}"
    low = text.casefold()

    if "<html" in low and _has(low, "github", "repository", "octicon"):
        kind, confidence, reason = "NOISY_HTML", 0.99, "raw repository webpage HTML is not semantic prompt content"
    elif re.search(r"^#\s+.*(?:faq|frequently asked questions)", body, re.I | re.M):
        kind, confidence, reason = "FAQ", 0.99, "artifact is explicitly a FAQ"
    elif _has(text, "implementation plan", "poc implementation plan"):
        kind, confidence, reason = "IMPLEMENTATION_PLAN", 0.98, "artifact is an implementation/design plan"
    elif re.search(r"^#\s+(?:log|changelog|activity log)\b", body, re.I | re.M):
        kind, confidence, reason = "LOG_CHANGELOG", 0.99, "artifact explicitly identifies itself as a log or changelog"
    elif _has(text, "architecture overview", "end-to-end chat flow") and _has(text, "mermaid", "sequenceDiagram", "graph TB"):
        kind, confidence, reason = "ARCHITECTURE_DOCUMENTATION", 0.97, "artifact primarily documents system architecture"
    elif _has(text, "this document provides comprehensive guidance for ai assistants", "instructions for ai assistants", "ai assistants working on", "guidance to ai agents when working with code"):
        kind, confidence, reason = "AGENT_INSTRUCTION", 0.99, "artifact explicitly instructs AI assistants or agents operating in a repository"
    elif source_type == "instruction-markdown" and _has(text, "agents.md") and _has(text, "don't", "must", "never", "treat every session", "before changing"):
        kind, confidence, reason = "AGENT_INSTRUCTION", 0.97, "AGENTS.md contains actionable persistent agent constraints"
    elif _is_operational_skill(body, source_type):
        kind, confidence, reason = "AGENT_INSTRUCTION", 0.97, "SKILL artifact contains persistent normative operating instructions for an AI agent"
    elif _has(text, "codebase guide"):
        kind, confidence, reason = "CODEBASE_GUIDE", 0.98, "artifact explicitly identifies itself as a codebase guide"
    elif _has(text, "quick start", "configuration", "installation") and _has(text, "build", "cli", "usage"):
        kind, confidence, reason = "MANUAL", 0.95, "artifact is primarily setup/usage documentation"
    elif source_type == "prompt" and _has(text, "you are", "act as", "your task", "output"):
        kind, confidence, reason = "PROMPT", 0.94, "artifact has direct model task/instruction structure"
    elif source_type in {"prompt", "instruction-markdown", "skill", "agent", "capability", "workflow"}:
        kind, confidence, reason = "AMBIGUOUS", 0.75, "source label suggests prompt-like content but semantic evidence is insufficient"
    else:
        kind, confidence, reason = "DOCUMENTATION", 0.85, "artifact is not semantically prompt-like"

    if kind in GOLDEN_ARTIFACTS:
        disposition = "GOLDEN_EVALUATION"
    elif kind in REFERENCE_ARTIFACTS:
        disposition = "REFERENCE_CORPUS"
    elif kind == "NOISY_HTML":
        disposition = "REJECT"
    else:
        disposition = "HUMAN_REVIEW"

    canonical, authority = _epistemic(disposition)
    return {
        "artifact_class": kind,
        "confidence": confidence,
        "disposition": disposition,
        "canonical": canonical,
        "authority": authority,
        "reason": reason,
    }
