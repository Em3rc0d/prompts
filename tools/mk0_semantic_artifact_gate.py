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


def classify_artifact(title: str, body: str, source_type: str) -> dict:
    """Deterministic pre-quality semantic gate.

    This gate answers what the artifact IS, not how polished it looks.
    Reference material is preserved as explicitly non-canonical. Ambiguous
    cases remain reviewable instead of being silently promoted.
    """
    text = f"{title}\n{body}"
    low = text.casefold()

    if "<html" in low and _has(low, "github", "repository", "octicon"):
        kind, confidence, reason = "NOISY_HTML", 0.99, "raw repository webpage HTML is not semantic prompt content"
    elif re.search(r"^#\s+.*(?:faq|frequently asked questions)", body, re.I | re.M):
        kind, confidence, reason = "FAQ", 0.99, "artifact is explicitly a FAQ"
    elif _has(text, "implementation plan", "poc implementation plan"):
        kind, confidence, reason = "IMPLEMENTATION_PLAN", 0.98, "artifact is an implementation/design plan"
    elif _has(text, "activity log", "changelog") or (body.count("## 20") >= 2):
        kind, confidence, reason = "LOG_CHANGELOG", 0.97, "artifact primarily records historical activity or changes"
    elif _has(text, "architecture overview", "end-to-end chat flow") and _has(text, "mermaid", "sequenceDiagram", "graph TB"):
        kind, confidence, reason = "ARCHITECTURE_DOCUMENTATION", 0.97, "artifact primarily documents system architecture"
    elif _has(text, "codebase guide"):
        kind, confidence, reason = "CODEBASE_GUIDE", 0.98, "artifact explicitly identifies itself as a codebase guide"
    elif _has(text, "this document provides comprehensive guidance for ai assistants", "instructions for ai assistants", "ai assistants working on"):
        kind, confidence, reason = "AGENT_INSTRUCTION", 0.98, "artifact explicitly instructs AI assistants operating in a repository"
    elif source_type == "instruction-markdown" and _has(text, "agents.md") and _has(text, "don't", "must", "never", "treat every session", "before changing"):
        kind, confidence, reason = "AGENT_INSTRUCTION", 0.96, "AGENTS.md contains actionable persistent agent constraints"
    elif source_type == "prompt" and _has(text, "you are", "act as", "your task", "output"):
        kind, confidence, reason = "PROMPT", 0.94, "artifact has direct model task/instruction structure"
    elif _has(text, "quick start", "configuration", "installation") and _has(text, "build", "cli", "usage"):
        kind, confidence, reason = "MANUAL", 0.93, "artifact is primarily setup/usage documentation"
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
