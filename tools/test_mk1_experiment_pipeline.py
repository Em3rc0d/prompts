from __future__ import annotations

import json
import tempfile
from pathlib import Path

from mk1_behavioral_runner import sha256_json
from mk1_finalize_experiment import checks_to_map, persist_runtime_evidence, require_review_header
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


def build_staged_evidence(root: Path, execution_id: str = "immutable-test") -> tuple[Path, dict, Path]:
    staging = root / "staging"
    raw_dir = staging / "raw"
    raw_dir.mkdir(parents=True)
    raw_core = {
        "evidence_schema": "mk1-runtime-observation-v1",
        "observation_id": f"{execution_id}--case-1",
        "provider": "test-provider",
        "model": "test-model",
        "family": "test-family",
        "started_at": "2026-08-27T01:00:00Z",
        "completed_at": "2026-08-27T01:00:01Z",
        "rendered_prompt_sha256": "sha256:rendered",
        "transport": {"http_status": 200, "request_id": "req-test", "response_content_type": "application/json"},
        "raw_response": {"id": "provider-response-test"},
        "observed_output": "Alpha remains 42.",
    }
    raw = dict(raw_core)
    raw["evidence_sha256"] = sha256_json(raw_core)
    raw_file = raw_dir / f"{execution_id}--case-1.json"
    raw_file.write_text(json.dumps(raw), encoding="utf-8")
    staged_ref = f"{raw_file.as_posix()}#{raw['evidence_sha256']}"
    manifest_core = {
        "evidence_schema": "mk1-runtime-execution-manifest-v1",
        "stage": "F4",
        "execution_id": execution_id,
        "provider": "test-provider",
        "model": "test-model",
        "family": "test-family",
        "observations": [{"fixture_id": "case-1", "observation_id": raw_core["observation_id"], "evidence_ref": staged_ref}],
    }
    manifest = dict(manifest_core)
    manifest["manifest_sha256"] = sha256_json(manifest_core)
    (staging / "runtime-evidence-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    execution_file = staging / "execution.unreviewed.json"
    execution_file.write_text("{}", encoding="utf-8")
    execution = {
        "execution_id": execution_id,
        "mode": "api",
        "runtime": {"provider": "test-provider", "model": "test-model", "family": "test-family", "run_at": "2026-08-27T01:00:00Z", "identity_evidence_ref": f"{(staging / 'runtime-evidence-manifest.json').as_posix()}#{manifest['manifest_sha256']}"},
        "responses": {"case-1": {"output": "Alpha remains 42.", "human_checks": {}, "observation_evidence_ref": staged_ref}},
    }
    return execution_file, execution, raw_file


def test_durable_evidence_persistence() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        execution_file, execution, _ = build_staged_evidence(root)
        evidence_root = root / "evidence"
        persist_runtime_evidence(execution, execution_file, evidence_root)
        canonical = evidence_root / "immutable-test"
        canonical_manifest = json.loads((canonical / "runtime-evidence-manifest.json").read_text(encoding="utf-8"))
        manifest_core = dict(canonical_manifest)
        supplied_manifest_hash = manifest_core.pop("manifest_sha256")
        assert supplied_manifest_hash == sha256_json(manifest_core)
        assert execution["runtime"]["identity_evidence_ref"].startswith((canonical / "runtime-evidence-manifest.json").as_posix() + "#")
        response_ref = execution["responses"]["case-1"]["observation_evidence_ref"]
        assert response_ref.startswith((canonical / "raw").as_posix() + "/")
        copied_file = Path(response_ref.split("#", 1)[0])
        copied = json.loads(copied_file.read_text(encoding="utf-8"))
        copied_core = dict(copied)
        supplied_raw_hash = copied_core.pop("evidence_sha256")
        assert supplied_raw_hash == sha256_json(copied_core)
        try:
            persist_runtime_evidence(execution, execution_file, evidence_root)
        except ValueError as exc:
            assert "immutable" in str(exc)
        else:
            raise AssertionError("Finalized runtime evidence was overwritable")
        return {"canonical_manifest_integrity": "PASS", "canonical_raw_integrity": "PASS", "second_write_rejected": "PASS"}


def test_tampered_runtime_evidence_rejected() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        execution_file, execution, raw_file = build_staged_evidence(root, "tamper-test")
        raw = json.loads(raw_file.read_text(encoding="utf-8"))
        raw["observed_output"] = "Tampered after capture"
        raw_file.write_text(json.dumps(raw), encoding="utf-8")
        evidence_root = root / "evidence"
        try:
            persist_runtime_evidence(execution, execution_file, evidence_root)
        except ValueError as exc:
            assert "integrity mismatch" in str(exc)
            assert not (evidence_root / "tamper-test").exists(), "failed persistence must roll back partial durable evidence"
            return {"tamper_rejected": "PASS", "partial_write_rolled_back": "PASS"}
        raise AssertionError("Tampered raw runtime evidence was accepted")


def main() -> None:
    print(json.dumps({
        "mk1_observed_experiment_pipeline": "PASS",
        "renderer": test_renderer(),
        "provider_response_extractors": test_provider_extractors(),
        "human_evidence_boundary": test_human_evidence_boundary(),
        "durable_evidence_persistence": test_durable_evidence_persistence(),
        "tampered_evidence": test_tampered_runtime_evidence_rejected(),
        "policy": "Preparation captures observed provider outputs and leaves review unresolved. Finalization requires explicit human PASS/FAIL evidence, canonical immutable runtime evidence, and F5 identities remain blind until review is complete."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
