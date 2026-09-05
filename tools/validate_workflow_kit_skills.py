#!/usr/bin/env python3
"""Validate Developer Workflow Kit v1.2 skill candidates without inflating behavior claims.

This validator covers structural gates only. It deliberately does not execute an
LLM, infer host discovery behavior, or promote any skill to HOST_TESTED or
WORKFLOW_CERTIFIED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "product" / "developer-workflow-kit-v1.2"
SKILLS = KIT / "skills"
TRIGGER_MATRIX = ROOT / "certification" / "fixtures" / "skill-trigger-matrix.v1.json"

EXPECTED = {
    "review-code-with-evidence": {
        "skill_id": "PQ-SKILL-0001",
        "workflow_id": "PQ-WF-0001",
        "lineage": ["PQ-PROMPT-0002", "PQ-PROMPT-0006"],
    },
    "diagnose-bugs-with-evidence": {
        "skill_id": "PQ-SKILL-0002",
        "workflow_id": "PQ-WF-0002",
        "lineage": ["PQ-PROMPT-0001", "PQ-PROMPT-0004"],
    },
    "make-technical-decisions": {
        "skill_id": "PQ-SKILL-0003",
        "workflow_id": "PQ-WF-0003",
        "lineage": ["PQ-PROMPT-0003", "PQ-PROMPT-0007"],
    },
    "design-ai-workflows": {
        "skill_id": "PQ-SKILL-0004",
        "workflow_id": "PQ-WF-0004",
        "lineage": ["PQ-PROMPT-0005"],
    },
}

ALLOWED_TOP_LEVEL = {"SKILL.md", "references", "scripts", "assets", "ui"}
REQUIRED_HEADINGS = {"## Required intake", "## Workflow", "## Output", "## Boundaries"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter opening delimiter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing YAML frontmatter closing delimiter")
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, body


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_relative_links(skill_dir: Path, body: str, errors: list[str]) -> None:
    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        resolved = (skill_dir / clean).resolve()
        try:
            resolved.relative_to(skill_dir.resolve())
        except ValueError:
            fail(errors, f"{skill_dir.name}: relative link escapes skill directory: {target}")
            continue
        if not resolved.exists():
            fail(errors, f"{skill_dir.name}: broken relative link: {target}")


def validate_skill(name: str, expected: dict[str, object]) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dir = SKILLS / name
    skill_md = skill_dir / "SKILL.md"

    if not skill_dir.is_dir():
        return {"name": name, "status": "FAIL", "errors": ["skill directory missing"], "warnings": []}
    if not skill_md.is_file():
        return {"name": name, "status": "FAIL", "errors": ["SKILL.md missing"], "warnings": []}

    entries = {p.name for p in skill_dir.iterdir()}
    unexpected = sorted(entries - ALLOWED_TOP_LEVEL)
    if unexpected:
        fail(errors, f"unexpected top-level files/directories: {unexpected}")

    text = skill_md.read_text(encoding="utf-8")
    try:
        frontmatter, body = parse_frontmatter(text)
    except ValueError as exc:
        return {"name": name, "status": "FAIL", "errors": [str(exc)], "warnings": []}

    fm_name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if fm_name != name:
        fail(errors, f"frontmatter name {fm_name!r} does not match directory {name!r}")
    if not NAME_RE.fullmatch(fm_name):
        fail(errors, "frontmatter name must be lowercase kebab-case")
    if len(fm_name) > 64:
        fail(errors, "frontmatter name exceeds 64 characters")
    if not description or len(description) < 40:
        fail(errors, "description is missing or too weak to discriminate discovery")
    if len(description) > 1024:
        fail(errors, "description exceeds 1024 characters")
    if "use " not in description.lower():
        fail(errors, "description must state intended use/trigger")
    if " not " not in description.lower() and "; not " not in description.lower():
        fail(errors, "description must include at least one explicit near-miss exclusion")

    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            fail(errors, f"required section missing: {heading}")

    if "STRUCTURAL_CANDIDATE / UNTESTED" not in body:
        fail(errors, "candidate must preserve explicit UNTESTED state")
    if str(expected["skill_id"]) not in body:
        fail(errors, f"skill id missing: {expected['skill_id']}")
    if str(expected["workflow_id"]) not in body:
        fail(errors, f"workflow id missing: {expected['workflow_id']}")
    for prompt_id in expected["lineage"]:
        if str(prompt_id) not in body:
            fail(errors, f"prompt lineage missing: {prompt_id}")

    lower = body.lower()
    if "fabricat" not in lower and "do not claim" not in lower:
        fail(errors, "truth/evidence boundary is not explicit")
    if "override" not in lower and "authority" not in lower:
        warnings.append("authority/adversarial boundary is not expressed with canonical wording")

    placeholder_patterns = ["[TODO]", "TODO:", "TBD", "FIXME", "<placeholder>"]
    for marker in placeholder_patterns:
        if marker.lower() in lower:
            fail(errors, f"unfinished scaffold marker present: {marker}")

    validate_relative_links(skill_dir, body, errors)

    if name == "design-ai-workflows":
        successor = KIT / "prompts" / "general-operating-contract-v1.2.md"
        if not successor.is_file():
            fail(errors, "versioned PQ-PROMPT-0005 successor is missing")
        else:
            successor_text = successor.read_text(encoding="utf-8").lower()
            required_invariants = [
                "status: blocked",
                "do not execute the domain task",
                "safe partial evidence summary is allowed",
                "partial domain conclusion is not",
            ]
            missing = [item for item in required_invariants if item not in successor_text]
            if missing:
                fail(errors, f"v1.2 successor does not preserve blocker resolution invariants: {missing}")

    return {
        "name": name,
        "skill_id": expected["skill_id"],
        "workflow_id": expected["workflow_id"],
        "status": "PASS" if not errors else "FAIL",
        "sha256": sha256(skill_md),
        "errors": errors,
        "warnings": warnings,
    }


def validate_trigger_matrix(errors: list[str]) -> dict[str, object]:
    if not TRIGGER_MATRIX.is_file():
        fail(errors, "skill trigger matrix missing")
        return {}
    data = json.loads(TRIGGER_MATRIX.read_text(encoding="utf-8"))
    if data.get("state") != "FIXTURES_DEFINED_UNEXECUTED":
        fail(errors, "trigger matrix must remain explicitly unexecuted before host evidence")
    rows = data.get("skills", [])
    by_name = {row.get("name"): row for row in rows}
    if set(by_name) != set(EXPECTED):
        fail(errors, "trigger matrix skill set does not match expected skill candidates")
    for name in EXPECTED:
        row = by_name.get(name, {})
        intended = row.get("intended", [])
        non_trigger = row.get("non_trigger", [])
        if len(intended) < 4:
            fail(errors, f"{name}: fewer than 4 intended-trigger fixtures")
        if len(non_trigger) < 4:
            fail(errors, f"{name}: fewer than 4 non-trigger fixtures")
        if len(set(intended)) != len(intended) or len(set(non_trigger)) != len(non_trigger):
            fail(errors, f"{name}: duplicate discovery fixtures")
        if set(intended) & set(non_trigger):
            fail(errors, f"{name}: fixture appears in both intended and non-trigger sets")
    return {
        "matrix_id": data.get("matrix_id"),
        "state": data.get("state"),
        "sha256": sha256(TRIGGER_MATRIX),
        "skills": len(rows),
        "fixture_count": sum(len(r.get("intended", [])) + len(r.get("non_trigger", [])) for r in rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    global_errors: list[str] = []
    observed_dirs = {p.name for p in SKILLS.iterdir() if p.is_dir()} if SKILLS.is_dir() else set()
    if observed_dirs != set(EXPECTED):
        fail(global_errors, f"skill directory set mismatch: observed={sorted(observed_dirs)} expected={sorted(EXPECTED)}")

    results = [validate_skill(name, EXPECTED[name]) for name in sorted(EXPECTED)]
    trigger = validate_trigger_matrix(global_errors)
    failed = [r for r in results if r["status"] != "PASS"]

    report = {
        "schema": "prompt-quarry-skill-structure-validation-v1",
        "gate": "SKILL_STRUCTURE",
        "status": "PASS" if not failed and not global_errors else "FAIL",
        "behavioral_claim": "NONE",
        "host_tested": False,
        "workflow_certified": False,
        "portable": False,
        "skill_count": len(results),
        "skills": results,
        "trigger_fixture_design": trigger,
        "global_errors": global_errors,
    }

    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
