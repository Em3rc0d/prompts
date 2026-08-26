from __future__ import annotations

import json
from pathlib import Path

from mk1_candidate_assembler import assemble_candidate
from mk1_architecture_selector import validate_brief


BRIEFS = {
    "rewrite": Path("mk1/briefs/content/clear-rewrite.json"),
    "code_review": Path("mk1/briefs/software/code-review.json"),
    "research": Path("mk1/briefs/research/technical-decision.json"),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    results = {}
    bodies = set()

    for name, path in BRIEFS.items():
        brief = load(path)
        validate_brief(brief)
        artifact, selection, lint = assemble_candidate(brief)

        if artifact["state"] != "VALID":
            raise AssertionError(f"{name}: expected VALID, got {artifact['state']}")
        if lint["status"] != "PASS":
            raise AssertionError(f"{name}: lint failed: {json.dumps(lint, ensure_ascii=False, indent=2)}")
        if artifact["claims"] != ["engineered"]:
            raise AssertionError(f"{name}: F2 candidate must not claim tested/certified/improved: {artifact['claims']}")
        if artifact["evaluation"]["receipt_id"] is not None:
            raise AssertionError(f"{name}: F2 candidate should not have an evaluation receipt yet")
        if artifact["prompt_body"] in bodies:
            raise AssertionError(f"{name}: assembler produced duplicate prompt body across distinct briefs")
        bodies.add(artifact["prompt_body"])

        results[name] = {
            "artifact_id": artifact["id"],
            "state": artifact["state"],
            "signature": selection["architecture_signature"],
            "techniques": selection["techniques"],
            "body_length": len(artifact["prompt_body"]),
            "warnings": lint["warning_count"],
        }

    rewrite_signature = results["rewrite"]["signature"]
    expected_rewrite = "PURPOSE+CONTEXT+OUTPUT_CONTRACT+QUALITY_GATE"
    if rewrite_signature != expected_rewrite:
        raise AssertionError(f"Compact rewrite regressed: {rewrite_signature} != {expected_rewrite}")

    full_signature = "PURPOSE+ROLE+CONTEXT+INTAKE+ASSUMPTIONS+PROCESS+CONSTRAINTS+OUTPUT_CONTRACT+QUALITY_GATE+FALLBACK"
    if results["code_review"]["signature"] != full_signature:
        raise AssertionError("Code-review candidate lost full reliability architecture")
    if results["research"]["signature"] != full_signature:
        raise AssertionError("Research candidate lost full evidence architecture")

    if "source-requirement" not in results["research"]["techniques"]:
        raise AssertionError("Research candidate must request source-backed evidence")
    if "evidence-requirement" not in results["research"]["techniques"]:
        raise AssertionError("Research candidate must distinguish evidence requirements")

    print(
        json.dumps(
            {
                "mk1_f2": "PASS",
                "candidates": len(results),
                "results": results,
                "policy": "F2 proves deterministic Task Brief -> architecture -> engineered prompt -> static lint -> VALID candidate assembly. VALID is not TESTED/CERTIFIED/IMPROVED."
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
