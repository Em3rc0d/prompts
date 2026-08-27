from __future__ import annotations

import json

from mk1_finalize_experiment import checks_to_map, require_review_header
from mk1_runtime_executor import _anthropic_text, _gemini_text, _openai_text, render_prompt


def test_renderer() -> dict:
    body = "Text={text}\nTone={tone}\nObject={config}"
    rendered = render_prompt(body, {"text": "Alpha 42", "tone": "   ", "config": {"b": 2, "a": 1}})
    assert "Text=Alpha 42" in rendered
    assert "Tone=[NOT PROVIDED: tone]" in rendered
    assert 'Object={"a": 1, "b": 2}' in rendered
    assert render_prompt("{missing}", {}) == "[NOT PROVIDED: missing]"
    return {"present_values": "PASS", "missing_values_explicit": "PASS", "structured_values_deterministic": "PASS"}


def test_provider_extractors() -> dict:
    openai = {"output": [{"type": "message", "content": [{"type": "output_text", "text": "OpenAI observed"}]}]}
    anthropic = {"content": [{"type": "text", "text": "Anthropic observed"}]}
    gemini = {"candidates": [{"content": {"parts": [{"text": "Gemini observed"}]}}]}
    assert _openai_text(openai) == "OpenAI observed"
    assert _anthropic_text(anthropic) == "Anthropic observed"
    assert _gemini_text(gemini) == "Gemini observed"
    return {"openai": "PASS", "anthropic": "PASS", "gemini": "PASS"}


def test_human_evidence_boundary() -> dict:
    valid = checks_to_map([{"check": "Meaning preserved", "status": "PASS", "note": "Compared source and output."}], "fixture")
    assert valid["Meaning preserved"]["status"] == "PASS"
    rejected = []
    for bad in (
        [{"check": "Meaning preserved", "status": None, "note": "Reviewed."}],
        [{"check": "Meaning preserved", "status": "PASS", "note": ""}],
        [{"check": "Meaning preserved", "status": "UNKNOWN", "note": "Reviewed."}],
    ):
        try:
            checks_to_map(bad, "fixture")
        except ValueError:
            rejected.append(True)
        else:
            raise AssertionError(f"Incomplete/non-binary human evidence was accepted: {bad}")
    try:
        require_review_header({"reviewer_ref": "human-01", "reviewed_at": None})
    except ValueError:
        rejected.append(True)
    else:
        raise AssertionError("Review without reviewed_at was accepted")
    assert len(rejected) == 4
    return {"complete_review": "PASS", "invalid_reviews_rejected": len(rejected)}


def main() -> None:
    print(json.dumps({
        "mk1_observed_experiment_pipeline": "PASS",
        "renderer": test_renderer(),
        "provider_response_extractors": test_provider_extractors(),
        "human_evidence_boundary": test_human_evidence_boundary(),
        "policy": "Preparation captures observed provider outputs and leaves review unresolved. Finalization requires explicit human PASS/FAIL evidence; F5 identities remain blind until review is complete."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
