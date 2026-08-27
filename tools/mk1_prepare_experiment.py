from __future__ import annotations

import argparse
import hashlib
import json
import secrets
from pathlib import Path
from typing import Any

from mk1_behavioral_runner import find_fixture_set, sha256_json, sha256_text
from mk1_f5_benchmark import find_baseline
from mk1_runtime_executor import execute_observation, render_prompt, utc_now


def load(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def evidence_manifest(out: Path, stage: str, execution_id: str, provider: str, model: str, family: str, observations: list[dict]) -> str:
    manifest = {
        "evidence_schema": "mk1-runtime-execution-manifest-v1",
        "stage": stage,
        "execution_id": execution_id,
        "provider": provider,
        "model": model,
        "family": family,
        "observations": observations,
    }
    manifest["manifest_sha256"] = sha256_json(manifest)
    path = out / "runtime-evidence-manifest.json"
    write(path, manifest)
    return f"{path.as_posix()}#{manifest['manifest_sha256']}"


def prepare_f4(args: argparse.Namespace) -> None:
    artifact = load(args.artifact)
    fixture_document = load(args.fixtures)
    fixture_set = find_fixture_set(fixture_document, args.fixture_set)
    if artifact.get("state") != "VALID":
        raise ValueError("F4 preparation requires a VALID artifact")
    if fixture_set.get("artifact_id") != artifact.get("id") or fixture_set.get("artifact_version") != artifact.get("version"):
        raise ValueError("Artifact/fixture identity mismatch")

    out = Path(args.output_dir)
    evidence_dir = out / "raw"
    responses: dict[str, dict] = {}
    observations: list[dict] = []
    run_at = utc_now()

    for fixture in fixture_set.get("cases", []):
        fixture_id = fixture["fixture_id"]
        variables = (fixture.get("input") or {}).get("variables") or {}
        rendered = render_prompt(artifact["prompt_body"], variables)
        observation_id = f"{args.execution_id}--{fixture_id}"
        observed = execute_observation(args.provider, args.model, args.family, rendered, evidence_dir, observation_id)
        responses[fixture_id] = {"output": observed["output"], "human_checks": {}, "observation_evidence_ref": observed["identity_evidence_ref"]}
        observations.append({"fixture_id": fixture_id, "observation_id": observation_id, "evidence_ref": observed["identity_evidence_ref"]})

    identity_ref = evidence_manifest(out, "F4", args.execution_id, args.provider, args.model, args.family, observations)
    execution = {
        "execution_id": args.execution_id,
        "mode": "api",
        "runtime": {"provider": args.provider, "model": args.model, "family": args.family, "run_at": run_at, "identity_evidence_ref": identity_ref},
        "artifact_id": artifact["id"],
        "artifact_version": artifact["version"],
        "artifact_prompt_fingerprint": sha256_text(artifact["prompt_body"]),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version", fixture_document.get("version", "1")),
        "fixture_set_fingerprint": sha256_json({**fixture_set, "version": fixture_set.get("version", fixture_document.get("version", "1"))}),
        "responses": responses,
    }
    packet = {
        "review_schema": "mk1-f4-human-review-v1",
        "stage": "F4",
        "execution_id": args.execution_id,
        "artifact_id": artifact["id"],
        "fixture_set_id": fixture_set["fixture_set_id"],
        "instructions": "A human reviewer must mark every listed check PASS or FAIL and provide a concrete non-empty note. Do not edit model outputs.",
        "reviewer_ref": None,
        "reviewed_at": None,
        "cases": [
            {
                "fixture_id": fixture["fixture_id"],
                "name": fixture.get("name"),
                "input": fixture.get("input"),
                "output": responses[fixture["fixture_id"]]["output"],
                "human_checks": [{"check": check, "status": None, "note": None} for check in fixture.get("expected", {}).get("human_checks", [])],
            }
            for fixture in fixture_set.get("cases", [])
        ],
    }
    write(out / "execution.unreviewed.json", execution)
    write(out / "review-packet.json", packet)
    print(json.dumps({"status": "F4_REVIEW_REQUIRED", "execution": str(out / 'execution.unreviewed.json'), "review_packet": str(out / 'review-packet.json')}, indent=2))


def prepare_f5(args: argparse.Namespace) -> None:
    artifact = load(args.artifact)
    if artifact.get("state") != "TESTED":
        raise ValueError("F5 preparation requires a TESTED artifact")
    baseline_document = load(args.baselines)
    baseline = find_baseline(baseline_document, artifact["id"])
    fixture_document = load(args.fixtures)
    fixture_set = find_fixture_set(fixture_document, args.fixture_set)
    if fixture_set.get("artifact_id") != artifact.get("id"):
        raise ValueError("Artifact/fixture identity mismatch")
    if args.repeats < 3:
        raise ValueError("F5 preparation requires at least 3 repeats")

    out = Path(args.output_dir)
    evidence_dir = out / "raw"
    observations: list[dict] = []
    canonical_repeats: list[dict] = []
    review_repeats: list[dict] = []
    blind_map: dict[str, dict] = {}
    run_at = utc_now()

    for repeat in range(1, args.repeats + 1):
        canonical_pairs: dict[str, dict] = {}
        review_pairs: list[dict] = []
        for fixture in fixture_set.get("cases", []):
            fixture_id = fixture["fixture_id"]
            variables = (fixture.get("input") or {}).get("variables") or {}
            rendered_engineered = render_prompt(artifact["prompt_body"], variables)
            rendered_baseline = render_prompt(baseline["prompt_body"], variables)
            observed_by_role: dict[str, dict] = {}
            roles = ["engineered", "baseline"]
            if secrets.randbelow(2):
                roles.reverse()
            for role in roles:
                prompt = rendered_engineered if role == "engineered" else rendered_baseline
                observation_id = f"{args.execution_id}--r{repeat}--{fixture_id}--{role}"
                observed = execute_observation(args.provider, args.model, args.family, prompt, evidence_dir, observation_id)
                observed_by_role[role] = observed
                observations.append({"repeat": repeat, "fixture_id": fixture_id, "role": role, "observation_id": observation_id, "evidence_ref": observed["identity_evidence_ref"]})

            swap = bool(secrets.randbelow(2))
            labels = {"A": "baseline", "B": "engineered"} if swap else {"A": "engineered", "B": "baseline"}
            map_key = f"r{repeat}:{fixture_id}"
            blind_map[map_key] = labels
            canonical_pairs[fixture_id] = {
                "engineered": {"output": observed_by_role["engineered"]["output"], "human_checks": {}, "observation_evidence_ref": observed_by_role["engineered"]["identity_evidence_ref"]},
                "baseline": {"output": observed_by_role["baseline"]["output"], "human_checks": {}, "observation_evidence_ref": observed_by_role["baseline"]["identity_evidence_ref"]},
                "preference": {},
            }
            checks = fixture.get("expected", {}).get("human_checks", [])
            review_pairs.append({
                "fixture_id": fixture_id,
                "name": fixture.get("name"),
                "input": fixture.get("input"),
                "A": {"output": observed_by_role[labels["A"]]["output"], "human_checks": [{"check": check, "status": None, "note": None} for check in checks]},
                "B": {"output": observed_by_role[labels["B"]]["output"], "human_checks": [{"check": check, "status": None, "note": None} for check in checks]},
                "preference": {"winner": None, "note": None, "allowed": ["A", "B", "tie"]},
            })
        canonical_repeats.append({"repeat": repeat, "pairs": canonical_pairs})
        review_repeats.append({"repeat": repeat, "pairs": review_pairs})

    identity_ref = evidence_manifest(out, "F5", args.execution_id, args.provider, args.model, args.family, observations)
    blind_core = {"blind_schema": "mk1-f5-deblind-map-v1", "execution_id": args.execution_id, "assignments": blind_map}
    blind_core["randomization_ref"] = sha256_json(blind_core)
    execution = {
        "execution_id": args.execution_id,
        "mode": "api",
        "runtime": {"provider": args.provider, "model": args.model, "family": args.family, "run_at": run_at, "identity_evidence_ref": identity_ref},
        "artifact_id": artifact["id"],
        "artifact_version": artifact["version"],
        "engineered_prompt_fingerprint": sha256_text(artifact["prompt_body"]),
        "baseline_id": baseline["baseline_id"],
        "baseline_prompt_fingerprint": sha256_text(baseline["prompt_body"]),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version", fixture_document.get("version", "1")),
        "fixture_set_fingerprint": sha256_json({**fixture_set, "version": fixture_set.get("version", fixture_document.get("version", "1"))}),
        "parent_f4_receipt_id": (artifact.get("evaluation") or {}).get("receipt_id"),
        "repeats": canonical_repeats,
    }
    packet = {
        "review_schema": "mk1-f5-blind-human-review-v1",
        "stage": "F5",
        "execution_id": args.execution_id,
        "instructions": "Review A and B without attempting to infer their identities. Complete every human check on both sides, then select A, B or tie with a concrete evidence note.",
        "reviewer_ref": None,
        "reviewed_at": None,
        "repeats": review_repeats,
    }
    write(out / "execution.unreviewed.json", execution)
    write(out / "review-packet.json", packet)
    write(out / "deblind-map.private.json", blind_core)
    print(json.dumps({"status": "F5_BLIND_REVIEW_REQUIRED", "execution": str(out / 'execution.unreviewed.json'), "review_packet": str(out / 'review-packet.json'), "private_deblind_map": str(out / 'deblind-map.private.json'), "randomization_ref": blind_core["randomization_ref"]}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute MK1 F4/F5 experiments and prepare human-review packets without fabricating review evidence.")
    parser.add_argument("--stage", required=True, choices=["f4", "f5"])
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--fixture-set", required=True)
    parser.add_argument("--provider", required=True, choices=["openai", "anthropic", "gemini"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--baselines", default="mk1/baselines/f5/task-equivalent-minimal.json")
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    if args.stage == "f4":
        prepare_f4(args)
    else:
        prepare_f5(args)


if __name__ == "__main__":
    main()
