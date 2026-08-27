from __future__ import annotations

import argparse
import json
import re
import secrets
import shutil
from pathlib import Path
from typing import Any

from mk1_behavioral_runner import sha256_json, sha256_text
from mk1_f5_benchmark import find_baseline, find_fixture_set, load
from mk1_f5_runtime_collect import blind_key_id
from mk1_runtime_collect import render_prompt


SIDES = ("A", "B")


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe(value: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", value.casefold()).strip("-")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a frozen ChatGPT Plus manual-observed F5 paired/blind execution wave from an exact TESTED artifact.")
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--baselines", default="mk1/baselines/f5/task-equivalent-minimal.json")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.repeats < 3:
        raise ValueError("F5 requires at least 3 repeats")
    artifact = load(args.artifact)
    if artifact.get("state") != "TESTED" or "tested" not in set(artifact.get("claims") or []):
        raise ValueError("ChatGPT Plus F5 wave requires an exact TESTED artifact")
    parent_receipt = (artifact.get("evaluation") or {}).get("receipt_id")
    if not parent_receipt:
        raise ValueError("F5 source artifact must preserve its real F4 receipt_id")

    fixture_doc = load(args.fixtures)
    baseline_doc = load(args.baselines)
    fixture_set = find_fixture_set(fixture_doc, artifact["id"])
    baseline = find_baseline(baseline_doc, artifact["id"])
    if fixture_set.get("artifact_version") != artifact.get("version") or baseline.get("artifact_version") != artifact.get("version"):
        raise ValueError("F5 source/baseline/fixture version mismatch")

    out = Path(args.output)
    if out.exists():
        shutil.rmtree(out)
    (out / "operator" / "responses").mkdir(parents=True, exist_ok=True)
    randomizer = secrets.SystemRandom()
    mapping: dict[str, dict[str, str]] = {}
    cases: list[dict] = []

    for repeat in range(1, args.repeats + 1):
        repeat_dir = out / "operator" / f"repeat-{repeat:02d}"
        repeat_dir.mkdir(parents=True, exist_ok=True)
        for fixture in fixture_set.get("cases", []):
            fixture_id = fixture["fixture_id"]
            engineered_prompt = render_prompt(artifact["prompt_body"], fixture)
            baseline_prompt = render_prompt(baseline["prompt_body"], fixture)
            assignment = {"A": "engineered", "B": "baseline"}
            if randomizer.choice((True, False)):
                assignment = {"A": "baseline", "B": "engineered"}
            pair_key = f"r{repeat}:{fixture_id}"
            mapping[pair_key] = assignment
            side_rows: dict[str, dict] = {}
            for side in SIDES:
                role = assignment[side]
                prompt = engineered_prompt if role == "engineered" else baseline_prompt
                prompt_sha = sha256_text(prompt)
                prompt_file = repeat_dir / f"{safe(fixture_id)}.{side}.txt"
                prompt_file.write_text(
                    "\n".join([
                        "PROMPT QUARRY — MK1 F5 CHATGPT PLUS OPERATOR PACKET",
                        "",
                        f"PAIR: {pair_key}",
                        f"SIDE: {side}",
                        f"PROMPT SHA-256: {prompt_sha}",
                        "",
                        "Use a NEW clean ChatGPT Plus conversation.",
                        "Use the same visible ChatGPT configuration label for the entire F5 benchmark.",
                        "Paste only the frozen prompt below and preserve the full answer exactly.",
                        "Do not inspect blind-key.private.json before human review is complete.",
                        "",
                        "BEGIN FROZEN PROMPT",
                        prompt.rstrip(),
                        "END FROZEN PROMPT",
                        "",
                    ]),
                    encoding="utf-8",
                )
                response_file = out / "operator" / "responses" / f"r{repeat}-{safe(fixture_id)}-{side}.response.json"
                write(response_file, {
                    "pair_key": pair_key,
                    "repeat": repeat,
                    "fixture_id": fixture_id,
                    "side": side,
                    "visible_chatgpt_label": None,
                    "observed_at": None,
                    "source_reference": None,
                    "operator_ref": None,
                    "rendered_prompt_sha256": prompt_sha,
                    "output": None,
                })
                side_rows[side] = {
                    "prompt_file": prompt_file.relative_to(out).as_posix(),
                    "response_file": response_file.relative_to(out).as_posix(),
                    "rendered_prompt_sha256": prompt_sha,
                }
            cases.append({
                "pair_key": pair_key,
                "repeat": repeat,
                "fixture_id": fixture_id,
                "class": fixture.get("class"),
                "severity": fixture.get("severity", "normal"),
                "sides": side_rows,
            })

    frozen = {
        "artifact_id": artifact["id"],
        "artifact_version": artifact["version"],
        "engineered_prompt_fingerprint": sha256_text(artifact["prompt_body"]),
        "baseline_id": baseline["baseline_id"],
        "baseline_prompt_fingerprint": sha256_text(baseline["prompt_body"]),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version", fixture_doc.get("version", "1")),
        "fixture_set_fingerprint": sha256_json(fixture_set),
        "parent_f4_receipt_id": parent_receipt,
    }
    randomization_ref = sha256_json(mapping)
    blind_core = {
        "mk_stage": "MK1",
        "phase": "F5_BLIND_KEY",
        "execution_mode": "manual-observed",
        **frozen,
        "randomization_ref": randomization_ref,
        "mapping": mapping,
    }
    blind_key = dict(blind_core)
    blind_key["blind_key_id"] = blind_key_id(blind_core)
    blind_key["warning"] = "PRIVATE: do not expose to the human reviewer until all A/B judgments are complete."
    write(out / "blind-key.private.json", blind_key)

    wave = {
        "schema": "mk1-plus-f5-manual-wave-v1",
        "mk_stage": "MK1",
        "phase": "F5",
        "execution_mode": "manual-observed",
        **frozen,
        "repeat_count": args.repeats,
        "fixture_count": len(fixture_set.get("cases", [])),
        "pair_count": len(cases),
        "observation_count": len(cases) * 2,
        "randomization_ref": randomization_ref,
        "cases": cases,
        "operator_policy": "The operator executes A/B prompts and records outputs but does not perform the blind A/B review from this packet.",
        "review_policy": "The reviewer receives only the generated reviewer packet after collection; blind-key.private.json remains hidden until review completion.",
    }
    write(out / "manifest.json", wave)
    (out / "INDEX.txt").write_text(
        "\n".join([
            "PROMPT QUARRY — MK1 F5 CHATGPT PLUS BLINDED BENCHMARK",
            "",
            f"Artifact: {artifact['id']} v{artifact['version']}",
            f"Repeats: {args.repeats}",
            f"Fixtures: {len(fixture_set.get('cases', []))}",
            f"A/B pairs: {len(cases)}",
            f"Manual observations: {len(cases) * 2}",
            "",
            "Operator: execute all operator/repeat-*/ files in fresh chats and fill operator/responses/*.response.json.",
            "Reviewer: do not receive operator prompts or blind-key.private.json; review only the packet generated after collection.",
            "Generation alone never grants IMPROVED/CANDIDATE.",
            "",
        ]),
        encoding="utf-8",
    )
    print(json.dumps({"status": "PLUS_F5_WAVE_READY", "pairs": len(cases), "observations": len(cases) * 2, "randomization_ref": randomization_ref, "output": out.as_posix()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
