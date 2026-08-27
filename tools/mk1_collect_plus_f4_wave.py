from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mk1_behavioral_runner import sha256_json, sha256_text


def load(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def require_text(value: Any, field: str, fixture_id: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{fixture_id}: required manual observation field {field!r} is empty")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert completed ChatGPT Plus F4 response templates into a frozen manual-observed execution envelope plus raw evidence manifest.")
    parser.add_argument("--wave-dir", required=True, help="Artifact packet directory, e.g. mk1/manual/f4/chatgpt-plus/content_clear_rewrite")
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    wave_dir = Path(args.wave_dir)
    manifest = load(wave_dir / "manifest.json")
    output = Path(args.output_dir)
    if output.exists():
        raise ValueError(f"Output directory already exists; manual evidence is append-only: {output}")
    output.mkdir(parents=True, exist_ok=False)
    raw_dir = output / "raw"
    raw_dir.mkdir(parents=True, exist_ok=False)

    labels: set[str] = set()
    observations: list[dict] = []
    responses: dict[str, dict] = {}
    observed_times: list[str] = []

    try:
        for case in manifest.get("cases", []):
            fixture_id = case["fixture_id"]
            response_path = wave_dir / case["response_file"]
            response = load(response_path)
            if response.get("fixture_id") != fixture_id:
                raise ValueError(f"{fixture_id}: response fixture identity mismatch")
            expected_prompt_sha = case["rendered_prompt_sha256"]
            if response.get("rendered_prompt_sha256") != expected_prompt_sha:
                raise ValueError(f"{fixture_id}: rendered prompt SHA changed after packet generation")

            visible_label = require_text(response.get("visible_chatgpt_label"), "visible_chatgpt_label", fixture_id)
            observed_at = require_text(response.get("observed_at"), "observed_at", fixture_id)
            source_reference = require_text(response.get("source_reference"), "source_reference", fixture_id)
            model_output = require_text(response.get("output"), "output", fixture_id)
            labels.add(visible_label)
            observed_times.append(observed_at)

            evidence_core = {
                "evidence_schema": "mk1-chatgpt-plus-manual-observation-v1",
                "execution_id": args.execution_id,
                "observation_id": f"{args.execution_id}--{fixture_id}",
                "fixture_id": fixture_id,
                "provider": "openai-chatgpt",
                "model": visible_label,
                "family": "chatgpt-plus",
                "observed_at": observed_at,
                "source_reference": source_reference,
                "rendered_prompt_sha256": expected_prompt_sha,
                "observed_output": model_output,
                "observed_output_sha256": sha256_text(model_output),
                "collection_mode": "manual-observed",
            }
            evidence_hash = sha256_json(evidence_core)
            evidence = {**evidence_core, "evidence_sha256": evidence_hash}
            raw_path = raw_dir / f"{fixture_id}.json"
            write(raw_path, evidence)
            evidence_ref = f"{raw_path.as_posix()}#{evidence_hash}"
            observations.append({
                "fixture_id": fixture_id,
                "observation_id": evidence_core["observation_id"],
                "evidence_ref": evidence_ref,
            })
            responses[fixture_id] = {
                "output": model_output,
                "human_checks": {},
                "manual_source_reference": source_reference,
            }

        if len(labels) != 1:
            raise ValueError(f"One F4 certification execution must use exactly one visible ChatGPT configuration label; observed={sorted(labels)}")
        visible_label = next(iter(labels))

        evidence_manifest_core = {
            "evidence_schema": "mk1-runtime-execution-manifest-v1",
            "stage": "F4",
            "execution_id": args.execution_id,
            "provider": "openai-chatgpt",
            "model": visible_label,
            "family": "chatgpt-plus",
            "collection_mode": "manual-observed",
            "observations": observations,
        }
        manifest_hash = sha256_json(evidence_manifest_core)
        evidence_manifest = {**evidence_manifest_core, "manifest_sha256": manifest_hash}
        evidence_manifest_path = output / "runtime-evidence-manifest.json"
        write(evidence_manifest_path, evidence_manifest)
        identity_ref = f"{evidence_manifest_path.as_posix()}#{manifest_hash}"

        execution = {
            "execution_id": args.execution_id,
            "mode": "manual-observed",
            "collection_status": "OBSERVED_OUTPUTS_PENDING_HUMAN_REVIEW",
            "runtime": {
                "provider": "openai-chatgpt",
                "model": visible_label,
                "family": "chatgpt-plus",
                "run_at": max(observed_times),
                "identity_evidence_ref": identity_ref,
            },
            "review": {
                "reviewer_type": "human",
                "reviewer_ref": "",
                "reviewed_at": "",
            },
            "artifact_id": manifest["artifact_id"],
            "artifact_version": manifest["artifact_version"],
            "artifact_prompt_fingerprint": manifest["artifact_prompt_fingerprint"],
            "fixture_set_id": manifest["fixture_set_id"],
            "fixture_set_version": manifest["fixture_set_version"],
            "fixture_set_fingerprint": manifest["fixture_set_fingerprint"],
            "responses": responses,
            "instructions": [
                "This execution was collected manually from fresh ChatGPT Plus conversations.",
                "Do not edit observed outputs or frozen identity fields after collection.",
                "Complete human review separately before generating an F4 receipt.",
                "The runtime model field records the exact visible ChatGPT configuration label, not an inferred hidden backend model id.",
            ],
        }
        write(output / "execution.unreviewed.json", execution)
        write(output / "collection-summary.json", {
            "status": "PLUS_F4_OBSERVED_PENDING_REVIEW",
            "execution_id": args.execution_id,
            "artifact_id": manifest["artifact_id"],
            "fixture_set_id": manifest["fixture_set_id"],
            "visible_chatgpt_label": visible_label,
            "observation_count": len(observations),
            "identity_evidence_ref": identity_ref,
        })
        print(json.dumps({
            "status": "PLUS_F4_OBSERVED_PENDING_REVIEW",
            "execution_id": args.execution_id,
            "artifact_id": manifest["artifact_id"],
            "observations": len(observations),
            "visible_chatgpt_label": visible_label,
            "output": output.as_posix(),
        }, ensure_ascii=False, indent=2))
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise


if __name__ == "__main__":
    main()
