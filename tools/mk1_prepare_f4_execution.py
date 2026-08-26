from __future__ import annotations

import argparse
import json
from pathlib import Path

from mk1_behavioral_runner import find_fixture_set, load


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--fixture-set", required=True)
    parser.add_argument("--mode", choices=["api", "manual-observed", "synthetic"], required=True)
    parser.add_argument("--provider")
    parser.add_argument("--model")
    parser.add_argument("--run-at")
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    document = load(Path(args.fixtures))
    fixture_set = find_fixture_set(document, args.fixture_set)

    runtime = {}
    if args.mode != "synthetic":
        runtime = {
            "provider": args.provider,
            "model": args.model,
            "run_at": args.run_at,
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
        "artifact_id": fixture_set["artifact_id"],
        "artifact_version": fixture_set["artifact_version"],
        "fixture_set_id": fixture_set["fixture_set_id"],
        "responses": responses,
        "instructions": [
            "Replace each empty output with the actually observed model/runtime output.",
            "Resolve each human check explicitly as PASS or FAIL with a note.",
            "Do not change fixture input after execution; create a new fixture-set version instead.",
            "Synthetic envelopes characterize the harness only and can never support TESTED state.",
        ],
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(envelope, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
