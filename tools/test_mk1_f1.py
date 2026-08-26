from __future__ import annotations

import copy
import json
from pathlib import Path

from mk1_architecture_selector import select_architecture, validate_brief
from mk1_prompt_linter import lint_artifact


SELECTOR_CASES = Path("mk1/fixtures/f1/selector-cases.json")


def assert_equal(actual, expected, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}\nexpected={expected!r}\nactual={actual!r}")


def test_selector() -> dict:
    cases = json.loads(SELECTOR_CASES.read_text(encoding="utf-8"))
    results = []
    for case in cases:
        brief = case["brief"]
        validate_brief(brief)
        result = select_architecture(brief)
        assert_equal(result["selected_blocks"], case["expected_selected"], f"Selector mismatch: {case['name']}")
        assert_equal(result["omitted_blocks"], case["expected_omitted"], f"Omission mismatch: {case['name']}")
        if brief["risk"] == "high-stakes":
            required = {"safety-boundary", "confidence-labeling", "fallback-behavior"}
            missing = sorted(required - set(result["techniques"]))
            if missing:
                raise AssertionError(f"High-stakes selector case missing techniques {missing}: {case['name']}")
        results.append(
            {
                "name": case["name"],
                "signature": result["architecture_signature"],
                "techniques": result["techniques"],
            }
        )
    return {"cases": len(cases), "results": results}


def base_valid_artifact() -> dict:
    return {
        "id": "pq_mk1_fixture_simple_rewrite",
        "version": "1.0.0",
        "state": "DRAFT",
        "artifact_type": "prompt",
        "title": "Clear rewrite",
        "domain": "general",
        "intent": "rewrite",
        "risk": "low",
        "language": "en",
        "model_targets": ["model-agnostic"],
        "purpose": "Rewrite supplied text more clearly without changing its meaning.",
        "success_criteria": ["Meaning is preserved", "Wording is clearer"],
        "inputs": {
            "required": ["text"],
            "optional": ["tone"]
        },
        "architecture": {
            "purpose": True,
            "role": False,
            "context": True,
            "intake": False,
            "assumptions": False,
            "process": False,
            "constraints": False,
            "output_contract": True,
            "quality_gate": True,
            "fallback": False
        },
        "techniques": ["context-injection", "variable-template", "output-formatting", "self-check"],
        "prompt_body": (
            "PURPOSE\n"
            "Rewrite {text} for clarity while preserving meaning.\n\n"
            "CONTEXT\n"
            "Use {tone} when supplied; otherwise preserve the original tone.\n\n"
            "OUTPUT CONTRACT\n"
            "Return only the revised text.\n\n"
            "QUALITY GATE\n"
            "Before returning, verify that no factual meaning was added or removed.\n"
        ),
        "claims": ["engineered"],
        "provenance": {
            "mk0_inputs": ["quarry/analysis/alpacka-ai-free-technique-matrix.json"],
            "patterns": [],
            "fixtures": [],
            "source_families": ["src_alpacka_web"]
        },
        "evaluation": {
            "baseline_id": None,
            "fixture_set_id": None,
            "receipt_id": None,
            "rubric_score": None,
            "blocking_failures": []
        },
        "created_at": None,
        "updated_at": None
    }


def test_linter() -> dict:
    cases = []

    valid = base_valid_artifact()
    report = lint_artifact(valid)
    if report["status"] != "PASS":
        raise AssertionError(f"Valid artifact failed lint: {json.dumps(report, ensure_ascii=False, indent=2)}")
    cases.append({"name": "valid-simple-artifact", "status": report["status"], "findings": report["findings"]})

    undefined = copy.deepcopy(valid)
    undefined["id"] = "pq_mk1_fixture_undefined_variable"
    undefined["prompt_body"] = undefined["prompt_body"].replace("{text}", "{ghost}", 1)
    report = lint_artifact(undefined)
    if report["status"] != "FAIL" or not any(f["code"] == "undefined-variable" for f in report["findings"]):
        raise AssertionError("Undefined-variable fixture did not fail as expected")
    cases.append({"name": "undefined-variable", "status": report["status"]})

    high_stakes = copy.deepcopy(valid)
    high_stakes["id"] = "pq_mk1_fixture_high_stakes_missing_safety"
    high_stakes["risk"] = "high-stakes"
    report = lint_artifact(high_stakes)
    if report["status"] != "FAIL" or report["blocking_count"] < 1:
        raise AssertionError("High-stakes missing-safety fixture did not produce blocking findings")
    cases.append({"name": "high-stakes-missing-safety", "status": report["status"], "blocking": report["blocking_count"]})

    improved = copy.deepcopy(valid)
    improved["id"] = "pq_mk1_fixture_fake_improved_claim"
    improved["claims"] = ["engineered", "improved"]
    report = lint_artifact(improved)
    codes = {f["code"] for f in report["findings"]}
    if report["status"] != "FAIL" or "improved-without-baseline" not in codes or "improved-without-receipt" not in codes:
        raise AssertionError("Unsupported improved claim was not blocked")
    cases.append({"name": "improved-without-receipt", "status": report["status"]})

    fake_certified = copy.deepcopy(valid)
    fake_certified["id"] = "pq_mk1_fixture_fake_certification"
    fake_certified["state"] = "CERTIFIED"
    fake_certified["claims"] = ["engineered", "tested", "certified"]
    fake_certified["evaluation"].update(
        {
            "fixture_set_id": "pq_mk1_fs_fixture",
            "receipt_id": "pq_mk1_receipt_fixture",
            "rubric_score": 80
        }
    )
    report = lint_artifact(fake_certified)
    if report["status"] != "FAIL" or not any(f["code"] == "certified-score" for f in report["findings"]):
        raise AssertionError("Fake CERTIFIED artifact below threshold was not blocked")
    cases.append({"name": "certified-below-threshold", "status": report["status"]})

    invalid_state = copy.deepcopy(valid)
    invalid_state["id"] = "pq_mk1_fixture_generated_is_not_quality_state"
    invalid_state["state"] = "GENERATED"
    report = lint_artifact(invalid_state)
    if report["status"] != "FAIL" or not any(f["code"] == "schema" for f in report["findings"]):
        raise AssertionError("GENERATED quality-state regression was not rejected by schema")
    cases.append({"name": "generated-not-quality-state", "status": report["status"]})

    return {"cases": len(cases), "results": cases}


def main() -> None:
    selector = test_selector()
    linter = test_linter()
    result = {
        "mk1_f1": "PASS",
        "selector": selector,
        "linter": linter,
        "policy": "F1 tests characterize deterministic architecture selection and block unsupported quality claims before candidate generation."
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
