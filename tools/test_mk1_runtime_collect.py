from __future__ import annotations

import json

from mk1_runtime_collect import (
    collect_execution,
    parse_anthropic_response,
    parse_gemini_response,
    parse_openai_response,
    render_prompt,
)


def artifact() -> dict:
    return {
        "id": "pq_mk1_runtime_test",
        "version": "0.1.0",
        "state": "VALID",
        "prompt_body": "TEXT={text}\nTONE={tone}\nAUDIENCE={audience}\n",
    }


def fixture_set() -> dict:
    return {
        "fixture_set_id": "pq_mk1_fs_runtime_test_v1",
        "version": "0.1.0",
        "artifact_id": "pq_mk1_runtime_test",
        "artifact_version": "0.1.0",
        "cases": [
            {
                "fixture_id": "provided",
                "class": "happy-path",
                "severity": "blocking",
                "input": {"variables": {"text": "Alpha 42", "tone": "neutral"}},
                "expected": {"machine_assertions": [], "human_checks": ["Meaning is preserved"]},
            },
            {
                "fixture_id": "missing",
                "class": "missing-critical",
                "severity": "blocking",
                "input": {"variables": {}},
                "expected": {"machine_assertions": [], "human_checks": ["Missing input is surfaced"]},
            },
        ],
    }


def test_render_only_supplied_variables() -> dict:
    provided = render_prompt(artifact()["prompt_body"], fixture_set()["cases"][0])
    missing = render_prompt(artifact()["prompt_body"], fixture_set()["cases"][1])
    assert "TEXT=Alpha 42" in provided
    assert "TONE=neutral" in provided
    assert "AUDIENCE={audience}" in provided
    assert missing == artifact()["prompt_body"]
    return {"supplied_replaced": True, "missing_placeholders_preserved": True}


def test_openai_parser() -> dict:
    text, meta = parse_openai_response({
        "id": "resp_1",
        "model": "model-openai",
        "status": "completed",
        "output": [{"type": "message", "content": [{"type": "output_text", "text": "Observed OpenAI text"}]}],
        "usage": {"input_tokens": 10, "output_tokens": 4},
    })
    assert text == "Observed OpenAI text"
    assert meta["response_id"] == "resp_1" and meta["resolved_model"] == "model-openai"
    return {"text": text, "response_id": meta["response_id"]}


def test_anthropic_parser() -> dict:
    text, meta = parse_anthropic_response({
        "id": "msg_1",
        "model": "model-anthropic",
        "content": [{"type": "text", "text": "Observed Anthropic text"}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 11, "output_tokens": 5},
    })
    assert text == "Observed Anthropic text"
    assert meta["response_id"] == "msg_1" and meta["stop_reason"] == "end_turn"
    return {"text": text, "response_id": meta["response_id"]}


def test_gemini_parser() -> dict:
    text, meta = parse_gemini_response({
        "responseId": "gem_1",
        "modelVersion": "model-gemini",
        "candidates": [{"content": {"parts": [{"text": "Observed Gemini text"}]}, "finishReason": "STOP"}],
        "usageMetadata": {"promptTokenCount": 12, "candidatesTokenCount": 6},
    })
    assert text == "Observed Gemini text"
    assert meta["response_id"] == "gem_1" and meta["finish_reason"] == "STOP"
    return {"text": text, "response_id": meta["response_id"]}


def test_collection_never_auto_reviews() -> dict:
    calls: list[str] = []

    def caller(prompt: str) -> tuple[str, dict]:
        calls.append(prompt)
        return f"Observed output {len(calls)}", {"response_id": f"fake-{len(calls)}"}

    envelope = collect_execution(
        artifact(),
        fixture_set(),
        "openai",
        "explicit-model-id",
        "runtime-collection-test",
        caller,
        run_at="2026-08-27T01:00:00Z",
    )
    assert envelope["mode"] == "api"
    assert envelope["collection_status"] == "OBSERVED_OUTPUTS_PENDING_HUMAN_REVIEW"
    assert envelope["runtime"] == {
        "provider": "openai",
        "model": "explicit-model-id",
        "family": "openai",
        "run_at": "2026-08-27T01:00:00Z",
    }
    assert envelope["review"] == {"reviewer_type": "human", "reviewer_ref": "", "reviewed_at": ""}
    assert len(envelope["responses"]) == 2
    assert all(
        check["status"] == "UNRESOLVED" and check["note"] == ""
        for response in envelope["responses"].values()
        for check in response["human_checks"].values()
    )
    assert "{text}" in calls[1], "missing required input must remain visibly unresolved in the exact rendered prompt"
    return {"outputs": 2, "human_review": "UNRESOLVED", "family": envelope["runtime"]["family"]}


def test_empty_provider_output_rejected() -> dict:
    def caller(_: str) -> tuple[str, dict]:
        return "", {}

    try:
        collect_execution(artifact(), fixture_set(), "gemini", "model", "empty-test", caller)
    except RuntimeError as exc:
        assert "empty text" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Collector must reject empty provider output")


def test_unknown_provider_rejected() -> dict:
    try:
        collect_execution(artifact(), fixture_set(), "unknown", "model", "provider-test", lambda _: ("x", {}))
    except ValueError as exc:
        assert "Unsupported provider" in str(exc)
        return {"rejected": True, "reason": str(exc)}
    raise AssertionError("Collector must reject unknown provider")


def main() -> None:
    print(json.dumps({
        "mk1_runtime_collect": "PASS",
        "rendering": test_render_only_supplied_variables(),
        "openai_parser": test_openai_parser(),
        "anthropic_parser": test_anthropic_parser(),
        "gemini_parser": test_gemini_parser(),
        "no_auto_human_review": test_collection_never_auto_reviews(),
        "empty_output_rejected": test_empty_provider_output_rejected(),
        "unknown_provider_rejected": test_unknown_provider_rejected(),
        "policy": "Runtime collection records provider outputs verbatim against frozen prompts/fixtures but never fabricates human PASS or a TESTED receipt."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
