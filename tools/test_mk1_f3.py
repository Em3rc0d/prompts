from __future__ import annotations

import copy
import json
import re
from pathlib import Path

from mk1_candidate_assembler import assemble_candidate
from mk1_prompt_critic import critique_artifact
from test_mk1_f1 import base_valid_artifact


F2_BRIEFS = [
    Path("mk1/briefs/content/clear-rewrite.json"),
    Path("mk1/briefs/software/code-review.json"),
    Path("mk1/briefs/research/technical-decision.json"),
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def codes(report: dict) -> set[str]:
    return {finding["code"] for finding in report["findings"]}


def assert_code(report: dict, code: str, expected_status: str | None = None) -> None:
    if code not in codes(report):
        raise AssertionError(f"Expected critic code {code!r}: {json.dumps(report, ensure_ascii=False, indent=2)}")
    if expected_status and report["status"] != expected_status:
        raise AssertionError(f"Expected status {expected_status}, got {report['status']} for {code}")


def replace_section(body: str, heading: str, replacement: str) -> str:
    pattern = rf"(?ms)^{re.escape(heading)}\n.*?(?=^[A-ZÁÉÍÓÚÜÑ /-]+\n|\Z)"
    updated, count = re.subn(pattern, heading + "\n" + replacement.strip() + "\n\n", body)
    if count != 1:
        raise AssertionError(f"Could not replace section {heading!r}, count={count}")
    return updated.rstrip() + "\n"


def test_clean_f2_candidates() -> list[dict]:
    results = []
    for path in F2_BRIEFS:
        artifact, selection, lint = assemble_candidate(load(path))
        if lint["status"] != "PASS":
            raise AssertionError(f"Precondition failed: {path} linter={lint['status']}")
        report = critique_artifact(artifact)
        if report["status"] != "PASS":
            raise AssertionError(
                f"Clean F2 candidate should pass F3 critic: {path}\n"
                + json.dumps(report, ensure_ascii=False, indent=2)
            )
        results.append(
            {
                "brief": path.as_posix(),
                "artifact_id": artifact["id"],
                "critic": report["status"],
                "signature": selection["architecture_signature"],
            }
        )
    return results


def test_regressions() -> list[dict]:
    results = []

    duplicate = base_valid_artifact()
    duplicate["id"] = "pq_mk1_f3_duplicate_instruction"
    duplicate["prompt_body"] = duplicate["prompt_body"].replace(
        "QUALITY GATE\n",
        "QUALITY GATE\nBefore returning, verify that no factual meaning was added or removed.\n",
    )
    report = critique_artifact(duplicate)
    assert_code(report, "duplicate-instruction", "WARN")
    results.append({"case": "duplicate-instruction", "status": report["status"]})

    code_review, _, _ = assemble_candidate(load(Path("mk1/briefs/software/code-review.json")))
    contradiction = copy.deepcopy(code_review)
    contradiction["id"] = "pq_mk1_f3_questions_contradiction"
    contradiction["prompt_body"] = contradiction["prompt_body"].replace(
        "- Pregunta sólo por esas entradas faltantes.",
        "- Pregunta sólo por esas entradas faltantes.\n- No hagas preguntas.",
    )
    report = critique_artifact(contradiction)
    assert_code(report, "questions-required-vs-forbidden", "FAIL")
    results.append({"case": "questions-required-vs-forbidden", "status": report["status"]})

    vague = base_valid_artifact()
    vague["id"] = "pq_mk1_f3_vague_output"
    vague["prompt_body"] = replace_section(vague["prompt_body"], "OUTPUT CONTRACT", "Hazlo bien.")
    report = critique_artifact(vague)
    assert_code(report, "vague-output-contract", "FAIL")
    results.append({"case": "vague-output-contract", "status": report["status"]})

    laundering = base_valid_artifact()
    laundering["id"] = "pq_mk1_f3_provenance_laundering"
    laundering["prompt_body"] += "\nReproduce exactamente la fuente original premium prompt.\n"
    report = critique_artifact(laundering)
    assert_code(report, "provenance-laundering-language", "FAIL")
    results.append({"case": "provenance-laundering-language", "status": report["status"]})

    high_stakes = copy.deepcopy(code_review)
    high_stakes["id"] = "pq_mk1_f3_high_stakes_generic_boundary"
    high_stakes["risk"] = "high-stakes"
    for technique in ["safety-boundary", "confidence-labeling"]:
        if technique not in high_stakes["techniques"]:
            high_stakes["techniques"].append(technique)
    high_stakes["prompt_body"] = replace_section(
        high_stakes["prompt_body"],
        "RESTRICCIONES",
        "- Sé cuidadoso.\n- No inventes hechos.",
    )
    high_stakes["prompt_body"] = replace_section(
        high_stakes["prompt_body"],
        "SI FALTA INFORMACIÓN",
        "- Indica que falta información.",
    )
    report = critique_artifact(high_stakes)
    assert_code(report, "high-stakes-boundary-too-generic", "FAIL")
    results.append({"case": "high-stakes-boundary-too-generic", "status": report["status"]})

    overfit = base_valid_artifact()
    overfit["id"] = "pq_mk1_f3_architecture_overfit"
    overfit["architecture"] = {key: True for key in overfit["architecture"]}
    overfit["techniques"] = sorted(
        set(overfit["techniques"])
        | {"role-assignment", "question-first", "assumption-audit", "task-decomposition", "explicit-constraints", "fallback-behavior"}
    )
    overfit["prompt_body"] = (
        "PURPOSE\nRewrite {text} clearly.\n\n"
        "ROLE\nAct as a careful editor.\n\n"
        "CONTEXT\nInput: {text}. Optional tone: {tone}.\n\n"
        "INTAKE\nAsk only if the required text is missing.\n\n"
        "ASSUMPTIONS\nLabel any assumption rather than presenting it as fact.\n\n"
        "PROCESS\n1. Read the text.\n2. Rewrite it.\n3. Re-check meaning.\n\n"
        "CONSTRAINTS\n- Do not add facts.\n- Preserve meaning.\n\n"
        "OUTPUT CONTRACT\nReturn the revised text with the same material meaning.\n\n"
        "QUALITY GATE\nVerify that meaning is preserved and no facts were added.\n\n"
        "FALLBACK\nIf the text is missing, ask for it instead of inventing input.\n"
    )
    report = critique_artifact(overfit)
    assert_code(report, "architecture-overfit", "WARN")
    results.append({"case": "architecture-overfit", "status": report["status"]})

    return results


def main() -> None:
    clean = test_clean_f2_candidates()
    regressions = test_regressions()
    print(
        json.dumps(
            {
                "mk1_f3": "PASS",
                "clean_f2_candidates": clean,
                "regression_cases": regressions,
                "policy": "F3 static critic detects semantic-quality defects beyond schema/lint. PASS remains static evidence only and does not imply behavioral testing/certification."
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
