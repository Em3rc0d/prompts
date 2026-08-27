from __future__ import annotations

import argparse
import json
from pathlib import Path

from mk1_behavioral_runner import find_fixture_set, load, sha256_json, sha256_text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--fixture-set", required=True)
    parser.add_argument("--mode", choices=["api", "manual-observed", "synthetic"], required=True)
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--family")
    parser.add_argument("--run-at")
    parser.add_argument("--reviewer-ref")
    parser.add_argument("--reviewed-at")
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    document = load(Path(args.fixtures))
    fixture_set = find_fixture_set(document, args.fixture_set)
    artifact = load(Path(args.artifact))

    if artifact.get("id") != fixture_set.get("artifact_id"):
        raise SystemExit("Artifact id does not match selected fixture set")
    if artifact.get("version") != fixture_set.get("artifact_version"):
        raise SystemExit("Artifact version does not match selected fixture set")
    prompt_body = artifact.get("prompt_body")
    if not isinstance(prompt_body, str) or not prompt_body.strip():
        raise SystemExit("Artifact requires non-empty prompt_body")

    runtime = {}
    review = {}
    if args.mode != "synthetic":
        runtime = {
            "provider": args.provider,
            "model": args.model,
            "family": args.family,
            "run_at": args.run_at,
        }
        review = {
            "reviewer_type": "human",
            "reviewer_ref": args.reviewer_ref or "",
            "reviewed_at": args.reviewed_at or "",
        }

    responses = {}
    for fixture in fixture_set["cases"]:
        responses[fixture["fixture_id"]] = {
            "fixture_input": fixture.get("input", {}),
            "output": "",
            "human_checks": {
                check: {"status": "UNRESOLVED", "note": ""}
                for check in fixture.get("expected", {}).get("human_checks", [])
            },
        }

    envelope = {
        "execution_id": args.execution_id,
        "mode": args.mode,
        "runtime": runtime,
        "review": review,
        "artifact_id": artifact["id"],
        "artifact_version": artifact["version"],
        "artifact_prompt_fingerprint": sha256_text(prompt_body),
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set["version"],
        "fixture_set_fingerprint": sha256_json(fixture_set),
        "responses": responses,
        "instructions": [
            "This envelope is frozen to the exact artifact prompt fingerprint and fixture-set fingerprint recorded above.",
            "Replace each empty output with the actually observed model/runtime output.",
            "Resolve each declared human check explicitly as PASS or FAIL with an evidence note.",
            "For real executions, fill provider, model, family, run_at, reviewer_ref and reviewed_at; reviewer_type must remain human.",
            "Do not substitute model self-judgment for declared human review.",
            "Do not change prompt or fixture input after preparing/executing this envelope; version and prepare a new envelope instead.",
            "Synthetic envelopes characterize the harness only and can never support TESTED state."
        ],
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(envelope, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
