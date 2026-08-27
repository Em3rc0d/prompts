from __future__ import annotations

import argparse
import copy
import json
import shutil
from pathlib import Path
from typing import Any

from mk1_behavioral_runner import sha256_json, sha256_text
from mk1_f5_benchmark import find_fixture_set, load
from mk1_f5_runtime_collect import SIDES, blind_key_id, packet_id


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def required(value: Any, field: str, context: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{context}: required field {field!r} is empty")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect completed ChatGPT Plus F5 A/B operator outputs into frozen semantic observation + reviewer-only packet.")
    parser.add_argument("--wave-dir", required=True)
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    wave_dir = Path(args.wave_dir)
    wave = load(wave_dir / "manifest.json")
    source_blind = load(wave_dir / "blind-key.private.json")
    fixture_doc = load(args.fixtures)
    fixture_set = find_fixture_set(fixture_doc, wave["artifact_id"])
    fixtures = {row["fixture_id"]: row for row in fixture_set.get("cases", [])}
    if source_blind.get("randomization_ref") != sha256_json(source_blind.get("mapping") or {}):
        raise ValueError("Source F5 wave blind mapping integrity failed")
    if source_blind.get("randomization_ref") != wave.get("randomization_ref"):
        raise ValueError("Wave/blind-key randomization mismatch")

    out = Path(args.output_dir)
    if out.exists():
        raise ValueError(f"Output directory already exists; F5 manual evidence is append-only: {out}")
    out.mkdir(parents=True, exist_ok=False)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=False)

    labels: set[str] = set()
    operator_refs: set[str] = set()
    observed_times: list[str] = []
    semantic: dict[int, dict[str, dict[str, dict]]] = {}
    review_pairs: list[dict] = []
    evidence_rows: list[dict] = []
    mapping = source_blind["mapping"]

    try:
        for case in wave.get("cases", []):
            pair_key = case["pair_key"]
            repeat = int(case["repeat"])
            fixture_id = case["fixture_id"]
            fixture = fixtures[fixture_id]
            assignment = mapping.get(pair_key) or {}
            if set(assignment) != {"A", "B"} or set(assignment.values()) != {"engineered", "baseline"}:
                raise ValueError(f"Invalid A/B mapping for {pair_key}")
            semantic.setdefault(repeat, {})[fixture_id] = {}
            reviewer_sides: dict[str, dict] = {}

            for side in SIDES:
                side_manifest = case["sides"][side]
                response_path = wave_dir / side_manifest["response_file"]
                response = load(response_path)
                context = f"{pair_key}:{side}"
                for key, expected in (("pair_key", pair_key), ("repeat", repeat), ("fixture_id", fixture_id), ("side", side)):
                    if response.get(key) != expected:
                        raise ValueError(f"{context}: response identity mismatch for {key}")
                prompt_sha = side_manifest["rendered_prompt_sha256"]
                if response.get("rendered_prompt_sha256") != prompt_sha:
                    raise ValueError(f"{context}: rendered prompt SHA drift")
                visible_label = required(response.get("visible_chatgpt_label"), "visible_chatgpt_label", context)
                observed_at = required(response.get("observed_at"), "observed_at", context)
                source_ref = required(response.get("source_reference"), "source_reference", context)
                operator_ref = required(response.get("operator_ref"), "operator_ref", context)
                model_output = required(response.get("output"), "output", context)
                labels.add(visible_label)
                operator_refs.add(operator_ref)
                observed_times.append(observed_at)

                evidence_core = {
                    "evidence_schema": "mk1-chatgpt-plus-manual-f5-observation-v1",
                    "execution_id": args.execution_id,
                    "observation_id": f"{args.execution_id}--{pair_key.replace(':', '-')}--{side}",
                    "pair_key": pair_key,
                    "repeat": repeat,
                    "fixture_id": fixture_id,
                    "side": side,
                    "provider": "openai-chatgpt",
                    "model": visible_label,
                    "family": "chatgpt-plus",
                    "observed_at": observed_at,
                    "source_reference": source_ref,
                    "operator_ref": operator_ref,
                    "rendered_prompt_sha256": prompt_sha,
                    "observed_output": model_output,
                    "observed_output_sha256": sha256_text(model_output),
                    "collection_mode": "manual-observed",
                }
                evidence_hash = sha256_json(evidence_core)
                raw = {**evidence_core, "evidence_sha256": evidence_hash}
                raw_path = raw_dir / f"r{repeat}-{fixture_id}-{side}.json"
                write(raw_path, raw)
                evidence_rows.append({
                    "pair_key": pair_key,
                    "side": side,
                    "observation_id": evidence_core["observation_id"],
                    "evidence_ref": f"{raw_path.as_posix()}#{evidence_hash}",
                })

                participant = assignment[side]
                semantic[repeat][fixture_id][participant] = {
                    "output": model_output,
                    "output_fingerprint": sha256_text(model_output),
                    "rendered_prompt_fingerprint": prompt_sha,
                    "provider_metadata": {
                        "collection_mode": "manual-observed",
                        "source_reference": source_ref,
                        "operator_ref": operator_ref,
                    },
                }
                reviewer_sides[side] = {
                    "observed_output": model_output,
                    "observed_output_fingerprint": sha256_text(model_output),
                    "human_check_labels": list(fixture.get("expected", {}).get("human_checks", [])),
                }

            review_pairs.append({
                "pair_key": pair_key,
                "repeat": repeat,
                "fixture_id": fixture_id,
                "class": fixture.get("class"),
                "severity": fixture.get("severity", "normal"),
                "fixture_input": fixture.get("input", {}),
                "sides": reviewer_sides,
            })

        if len(labels) != 1:
            raise ValueError(f"One F5 benchmark must use one visible ChatGPT configuration label; observed={sorted(labels)}")
        visible_label = next(iter(labels))

        evidence_manifest_core = {
            "evidence_schema": "mk1-runtime-execution-manifest-v1",
            "stage": "F5",
            "execution_id": args.execution_id,
            "provider": "openai-chatgpt",
            "model": visible_label,
            "family": "chatgpt-plus",
            "collection_mode": "manual-observed",
            "observations": evidence_rows,
        }
        manifest_hash = sha256_json(evidence_manifest_core)
        evidence_manifest = {**evidence_manifest_core, "manifest_sha256": manifest_hash}
        evidence_manifest_path = out / "runtime-evidence-manifest.json"
        write(evidence_manifest_path, evidence_manifest)
        identity_ref = f"{evidence_manifest_path.as_posix()}#{manifest_hash}"

        frozen_keys = (
            "artifact_id", "artifact_version", "engineered_prompt_fingerprint", "baseline_id",
            "baseline_prompt_fingerprint", "fixture_set_id", "fixture_set_version",
            "fixture_set_fingerprint", "parent_f4_receipt_id"
        )
        frozen = {key: wave[key] for key in frozen_keys}
        runtime = {
            "provider": "openai-chatgpt",
            "model": visible_label,
            "family": "chatgpt-plus",
            "run_at": max(observed_times),
            "identity_evidence_ref": identity_ref,
        }
        semantic_repeats = [
            {"repeat": repeat, "pairs": semantic[repeat]}
            for repeat in sorted(semantic)
        ]
        observation = {
            "mk_stage": "MK1",
            "phase": "F5_COLLECTION",
            "collection_status": "OBSERVED_PAIRED_OUTPUTS_PENDING_BLIND_HUMAN_REVIEW",
            "mode": "manual-observed",
            "execution_id": args.execution_id,
            "runtime": runtime,
            **frozen,
            "repeat_count": wave["repeat_count"],
            "pair_count": wave["pair_count"],
            "semantic_repeats": semantic_repeats,
            "manual_operator_refs": sorted(operator_refs),
        }
        write(out / "observation.json", observation)

        blind_core = {
            "mk_stage": "MK1",
            "phase": "F5_BLIND_KEY",
            "execution_id": args.execution_id,
            **frozen,
            "randomization_ref": wave["randomization_ref"],
            "mapping": mapping,
        }
        blind_key = copy.deepcopy(blind_core)
        blind_key["blind_key_id"] = blind_key_id(blind_core)
        blind_key["warning"] = "PRIVATE: do not expose before blind review completion."
        write(out / "blind-key.private.json", blind_key)

        immutable = {
            "mk_stage": "MK1",
            "phase": "F5_BLIND_REVIEW",
            "execution_id": args.execution_id,
            "runtime": runtime,
            **frozen,
            "repeat_count": wave["repeat_count"],
            "pair_count": wave["pair_count"],
            "randomization_ref": wave["randomization_ref"],
            "pairs": review_pairs,
        }
        review = {
            "reviewer_type": "human",
            "reviewer_ref": "",
            "reviewed_at": "",
            "blinded": True,
            "pair_judgments": {
                pair["pair_key"]: {
                    "A": {label: {"status": "UNRESOLVED", "note": ""} for label in pair["sides"]["A"]["human_check_labels"]},
                    "B": {label: {"status": "UNRESOLVED", "note": ""} for label in pair["sides"]["B"]["human_check_labels"]},
                    "preference": {"winner": "UNRESOLVED", "note": ""},
                }
                for pair in review_pairs
            },
        }
        review_packet = {
            "review_packet_id": packet_id(immutable),
            "immutable": immutable,
            "review": review,
            "instructions": [
                "Reviewer: inspect only this packet; do not inspect operator prompts or blind-key.private.json.",
                "Judge A and B independently against each human check; every PASS/FAIL needs an evidence note.",
                "Then select A, B or tie with an evidence note.",
                "Fill reviewer_ref/reviewed_at only after all judgments are complete.",
                "Do not attempt to infer or record engineered/baseline identity before deblinding.",
            ],
        }
        write(out / "review-packet.json", review_packet)
        write(out / "collection-summary.json", {
            "status": "PLUS_F5_OBSERVED_PENDING_BLIND_REVIEW",
            "execution_id": args.execution_id,
            "visible_chatgpt_label": visible_label,
            "operator_refs": sorted(operator_refs),
            "repeat_count": wave["repeat_count"],
            "pair_count": wave["pair_count"],
            "observation_count": len(evidence_rows),
            "identity_evidence_ref": identity_ref,
            "review_packet": "review-packet.json",
            "private_blind_key": "blind-key.private.json",
        })
        print(json.dumps({
            "status": "PLUS_F5_OBSERVED_PENDING_BLIND_REVIEW",
            "execution_id": args.execution_id,
            "pairs": wave["pair_count"],
            "observations": len(evidence_rows),
            "visible_chatgpt_label": visible_label,
            "output": out.as_posix(),
        }, ensure_ascii=False, indent=2))
    except Exception:
        if out.exists():
            shutil.rmtree(out)
        raise


if __name__ == "__main__":
    main()
