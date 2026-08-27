from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import secrets
from pathlib import Path
from typing import Any, Callable

import httpx

from mk1_behavioral_runner import sha256_json, sha256_text
from mk1_f5_benchmark import find_baseline, find_fixture_set, load
from mk1_runtime_collect import PROVIDERS, PROVIDER_CALLS, render_prompt, utc_now


MIN_REPEATS = 3
SIDES = ("A", "B")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def packet_id(immutable: dict) -> str:
    digest = hashlib.sha256(canonical_json(immutable).encode("utf-8")).hexdigest()[:16]
    return f"pq_mk1_f5_blind_review_{digest}"


def blind_key_id(core: dict) -> str:
    digest = hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()[:16]
    return f"pq_mk1_f5_blind_key_{digest}"


def _require_sources(tested_artifact: dict, baseline: dict, fixture_set: dict) -> None:
    if tested_artifact.get("state") != "TESTED" or "tested" not in set(tested_artifact.get("claims") or []):
        raise ValueError("F5 runtime collection requires a TESTED source artifact")
    if baseline.get("task_artifact_id") != tested_artifact.get("id") or baseline.get("artifact_version") != tested_artifact.get("version"):
        raise ValueError("F5 runtime collector baseline identity/version mismatch")
    if fixture_set.get("artifact_id") != tested_artifact.get("id") or fixture_set.get("artifact_version") != tested_artifact.get("version"):
        raise ValueError("F5 runtime collector fixture identity/version mismatch")
    if not str(baseline.get("prompt_body", "")).strip():
        raise ValueError("F5 runtime collector baseline prompt is empty")
    if not (tested_artifact.get("evaluation") or {}).get("receipt_id"):
        raise ValueError("F5 runtime collector requires parent F4 receipt lineage")


def _frozen_identity(tested_artifact: dict, baseline: dict, fixture_set: dict) -> dict:
    return {
        "artifact_id": tested_artifact["id"],
        "artifact_version": tested_artifact["version"],
        "engineered_prompt_fingerprint": sha256_text(tested_artifact["prompt_body"]),
        "baseline_id": baseline["baseline_id"],
        "baseline_prompt_fingerprint": sha256_text(baseline["prompt_body"]),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version", "1"),
        "fixture_set_fingerprint": sha256_json(fixture_set),
        "parent_f4_receipt_id": tested_artifact["evaluation"]["receipt_id"],
    }


def _side_assignment(randomizer: secrets.SystemRandom) -> dict[str, str]:
    if randomizer.choice((True, False)):
        return {"A": "engineered", "B": "baseline"}
    return {"A": "baseline", "B": "engineered"}


def collect_blinded_benchmark(
    tested_artifact: dict,
    baseline: dict,
    fixture_set: dict,
    provider: str,
    model: str,
    execution_id: str,
    repeat_count: int,
    caller: Callable[[str], tuple[str, dict]],
    run_at: str | None = None,
    randomizer: secrets.SystemRandom | None = None,
) -> tuple[dict, dict, dict]:
    _require_sources(tested_artifact, baseline, fixture_set)
    if provider not in PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")
    if repeat_count < MIN_REPEATS:
        raise ValueError(f"F5 runtime collection requires at least {MIN_REPEATS} repeats")
    if not str(model).strip() or not str(execution_id).strip():
        raise ValueError("F5 runtime collection requires explicit model and execution_id")

    randomizer = randomizer or secrets.SystemRandom()
    runtime = {
        "provider": provider,
        "model": model,
        "family": PROVIDERS[provider]["family"],
        "run_at": run_at or utc_now(),
    }
    frozen = _frozen_identity(tested_artifact, baseline, fixture_set)
    semantic_repeats: list[dict] = []
    blind_map: dict[str, dict[str, str]] = {}
    blind_pairs: list[dict] = []

    for repeat in range(1, repeat_count + 1):
        semantic_pairs: dict[str, dict] = {}
        for fixture in fixture_set.get("cases", []):
            fixture_id = fixture["fixture_id"]
            engineered_prompt = render_prompt(tested_artifact["prompt_body"], fixture)
            baseline_prompt = render_prompt(baseline["prompt_body"], fixture)
            engineered_output, engineered_meta = caller(engineered_prompt)
            baseline_output, baseline_meta = caller(baseline_prompt)
            if not str(engineered_output).strip() or not str(baseline_output).strip():
                raise RuntimeError(f"F5 provider returned empty output for repeat={repeat} fixture={fixture_id}")

            semantic = {
                "engineered": {
                    "output": str(engineered_output),
                    "output_fingerprint": sha256_text(str(engineered_output)),
                    "rendered_prompt_fingerprint": sha256_text(engineered_prompt),
                    "provider_metadata": engineered_meta,
                },
                "baseline": {
                    "output": str(baseline_output),
                    "output_fingerprint": sha256_text(str(baseline_output)),
                    "rendered_prompt_fingerprint": sha256_text(baseline_prompt),
                    "provider_metadata": baseline_meta,
                },
            }
            semantic_pairs[fixture_id] = semantic

            pair_key = f"r{repeat}:{fixture_id}"
            assignment = _side_assignment(randomizer)
            blind_map[pair_key] = assignment
            sides = {}
            for side in SIDES:
                participant = assignment[side]
                observed = semantic[participant]
                sides[side] = {
                    "observed_output": observed["output"],
                    "observed_output_fingerprint": observed["output_fingerprint"],
                    "human_check_labels": list(fixture.get("expected", {}).get("human_checks", [])),
                }
            blind_pairs.append({
                "pair_key": pair_key,
                "repeat": repeat,
                "fixture_id": fixture_id,
                "class": fixture.get("class"),
                "severity": fixture.get("severity", "normal"),
                "fixture_input": fixture.get("input", {}),
                "sides": sides,
            })
        semantic_repeats.append({"repeat": repeat, "pairs": semantic_pairs})

    randomization_ref = sha256_json(blind_map)
    observation = {
        "mk_stage": "MK1",
        "phase": "F5_COLLECTION",
        "collection_status": "OBSERVED_PAIRED_OUTPUTS_PENDING_BLIND_HUMAN_REVIEW",
        "execution_id": execution_id,
        "runtime": runtime,
        **frozen,
        "repeat_count": repeat_count,
        "pair_count": len(blind_pairs),
        "semantic_repeats": semantic_repeats,
    }

    key_core = {
        "mk_stage": "MK1",
        "phase": "F5_BLIND_KEY",
        "execution_id": execution_id,
        **frozen,
        "randomization_ref": randomization_ref,
        "mapping": blind_map,
    }
    blind_key = copy.deepcopy(key_core)
    blind_key["blind_key_id"] = blind_key_id(key_core)
    blind_key["warning"] = "Do not expose this file to the blind reviewer before review completion."

    immutable = {
        "mk_stage": "MK1",
        "phase": "F5_BLIND_REVIEW",
        "execution_id": execution_id,
        "runtime": runtime,
        **frozen,
        "repeat_count": repeat_count,
        "pair_count": len(blind_pairs),
        "randomization_ref": randomization_ref,
        "pairs": blind_pairs,
    }
    review = {
        "reviewer_type": "human",
        "reviewer_ref": "",
        "reviewed_at": "",
        "blinded": True,
        "pair_judgments": {
            pair["pair_key"]: {
                "A": {
                    label: {"status": "UNRESOLVED", "note": ""}
                    for label in pair["sides"]["A"]["human_check_labels"]
                },
                "B": {
                    label: {"status": "UNRESOLVED", "note": ""}
                    for label in pair["sides"]["B"]["human_check_labels"]
                },
                "preference": {"winner": "UNRESOLVED", "note": ""},
            }
            for pair in blind_pairs
        },
    }
    review_packet = {
        "review_packet_id": packet_id(immutable),
        "immutable": immutable,
        "review": review,
        "instructions": [
            "Open this review packet without the blind-key file.",
            "Judge side A and side B independently against the declared human checks; every PASS/FAIL needs a concrete evidence note.",
            "Then choose A, B or tie for preference with an evidence note.",
            "Do not infer or record which side is the engineered prompt; semantic labels are deliberately absent from this packet.",
            "Fill reviewer_ref and reviewed_at only after the blind review is complete.",
        ],
    }
    return observation, blind_key, review_packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--baselines", default="mk1/baselines/f5/task-equivalent-minimal.json")
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    args = parser.parse_args()

    provider_cfg = PROVIDERS[args.provider]
    api_key = os.environ.get(provider_cfg["key_env"], "")
    if not api_key:
        raise SystemExit(f"Missing required environment variable {provider_cfg['key_env']}; do not pass API keys on the command line")
    if args.repeats < MIN_REPEATS:
        raise SystemExit(f"--repeats must be >= {MIN_REPEATS}")

    tested_artifact = load(args.artifact)
    baseline_doc = load(args.baselines)
    fixture_doc = load(args.fixtures)
    baseline = find_baseline(baseline_doc, tested_artifact["id"])
    fixture_set = find_fixture_set(fixture_doc, tested_artifact["id"])

    with httpx.Client(timeout=httpx.Timeout(args.timeout_seconds)) as client:
        provider_call = PROVIDER_CALLS[args.provider]

        def caller(prompt: str) -> tuple[str, dict]:
            return provider_call(client, api_key, args.model, prompt, args.max_output_tokens)

        observation, blind_key, review_packet = collect_blinded_benchmark(
            tested_artifact,
            baseline,
            fixture_set,
            args.provider,
            args.model,
            args.execution_id,
            args.repeats,
            caller,
        )

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "observation.json").write_text(json.dumps(observation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "blind-key.json").write_text(json.dumps(blind_key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "review-packet.json").write_text(json.dumps(review_packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "mk1_f5_runtime_collection": observation["collection_status"],
        "artifact_id": observation["artifact_id"],
        "provider": observation["runtime"]["provider"],
        "model": observation["runtime"]["model"],
        "family": observation["runtime"]["family"],
        "repeats": observation["repeat_count"],
        "pairs": observation["pair_count"],
        "output_dir": output.as_posix(),
        "blind_policy": "review-packet.json contains A/B outputs only; blind-key.json must remain hidden until review completion.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
