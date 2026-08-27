from __future__ import annotations

import json
import tempfile
from pathlib import Path

from mk1_prompt_generator_v0 import classify_request, generate, retrieve_mk0, write_bundle


def test_software_review_generation() -> None:
    request = {
        "request_id": "test_software_review",
        "request": "Create a rigorous prompt to review software code, identify confirmed bugs and security risks, separate evidence from hypotheses, suggest fixes, and explain how each finding should be verified.",
        "model_targets": ["model-agnostic"],
    }
    result = generate(request)

    assert result["classification"]["intent"] == "review"
    assert result["classification"]["domain"] == "software"
    assert result["brief"]["language"] == "en"
    assert result["artifact"]["state"] == "VALID"
    assert result["lint"]["status"] == "PASS"
    assert result["critic"]["status"] in {"PASS", "WARN"}
    assert result["generator_status"] in {"VALID_STATIC", "WARN_STATIC"}
    assert "tested" not in result["artifact"]["claims"]
    assert "certified" not in result["artifact"]["claims"]
    assert "mk0/analysis/alpacka-ai-free-technique-matrix.json" in result["artifact"]["provenance"]["mk0_inputs"]
    assert "mk0/golden-dataset/alpacka-free-golden-fixtures-manifest.json" in result["artifact"]["provenance"]["mk0_inputs"]
    assert result["artifact"]["provenance"]["knowledge_fingerprints"]
    assert result["evaluation_plan"]["f5_proof_contract"]["baseline_a"]["required"] is True
    assert result["evaluation_plan"]["f5_proof_contract"]["baseline_b"]["required"] is False


def test_mk0_teaches_but_does_not_force_frequency() -> None:
    request = {
        "request_id": "test_simple_rewrite",
        "request": "Reescribe un texto para hacerlo más claro sin cambiar los hechos ni la intención.",
        "risk": "low",
    }
    result = generate(request)
    selected = {row["technique"] for row in result["technique_selection"]["techniques"]}
    retrieved_top = {row["technique"] for row in result["retrieval"]["technique_matrix"]["top_observed_techniques"]}

    assert result["classification"]["intent"] == "rewrite"
    assert result["classification"]["language"] == "es"
    assert "variable-template" in retrieved_top
    # High frequency in MK0 is not sufficient reason to enable every observed technique.
    assert selected != retrieved_top
    assert "role-assignment" not in selected
    assert "task-decomposition" not in selected


def test_high_stakes_boundary() -> None:
    request = {
        "request_id": "test_health_research",
        "request": "Research medical treatment options and compare the available evidence for a patient-facing decision support summary.",
    }
    result = generate(request)

    assert result["classification"]["domain"] == "health"
    assert result["classification"]["risk"] == "high-stakes"
    assert result["artifact"]["architecture"]["fallback"] is True
    assert "safety-boundary" in result["artifact"]["techniques"]
    assert "confidence-labeling" in result["artifact"]["techniques"]
    assert result["lint"]["status"] == "PASS"


def test_explicit_overrides_win() -> None:
    request = {
        "request_id": "test_override",
        "request": "Look at these two options and tell me what you think.",
        "intent": "compare",
        "domain": "software",
        "risk": "normal",
        "complexity": "moderate",
        "interaction": "one-shot",
        "language": "en",
        "inputs": {"required": ["options"], "optional": ["criteria"]},
        "output_needs": {"structured": True, "alternatives": 2, "evidence": False, "citations": False},
    }
    brief, classification = classify_request(request)

    assert classification["intent"] == "compare"
    assert classification["domain"] == "software"
    assert brief["interaction"] == "one-shot"
    assert brief["inputs"]["required"] == ["options"]
    assert "intent" in classification["overrides"]
    assert "inputs" in classification["overrides"]


def test_retrieval_has_no_source_bodies() -> None:
    request = {
        "request_id": "test_retrieval",
        "request": "Research and compare database options for a transactional software product.",
    }
    _, classification = classify_request(request)
    retrieval = retrieve_mk0(classification)
    rendered = json.dumps(retrieval, ensure_ascii=False).casefold()

    assert "prompt_body" not in rendered
    assert "source body" not in rendered
    assert retrieval["technique_matrix"]["observed_records"] == 52
    assert retrieval["golden_dataset"]["fixture_records"] == 23


def test_bundle_is_traceable() -> None:
    request = {
        "request_id": "test_bundle",
        "request": "Review Python API code for correctness and security, and provide verifiable fixes.",
    }
    with tempfile.TemporaryDirectory() as tmp:
        result = write_bundle(request, tmp)
        output = Path(tmp)
        expected = {
            "request.json",
            "task-brief.json",
            "classification.json",
            "mk0-retrieval.json",
            "technique-selection.json",
            "architecture.json",
            "artifact.json",
            "lint.json",
            "critic.json",
            "evaluation-plan.json",
            "prompt.txt",
            "generation.json",
        }
        assert expected == {path.name for path in output.iterdir()}
        generation = json.loads((output / "generation.json").read_text(encoding="utf-8"))
        assert generation["artifact_id"] == result["artifact"]["id"]
        assert generation["claim_boundary"].startswith("Generated/VALID_STATIC")


def main() -> None:
    tests = [
        test_software_review_generation,
        test_mk0_teaches_but_does_not_force_frequency,
        test_high_stakes_boundary,
        test_explicit_overrides_win,
        test_retrieval_has_no_source_bodies,
        test_bundle_is_traceable,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)} MK1 Prompt Generator v0 tests")


if __name__ == "__main__":
    main()
