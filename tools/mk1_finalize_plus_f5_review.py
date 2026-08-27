from __future__ import annotations

import argparse
import json
from pathlib import Path

from mk1_f5_benchmark import find_baseline, find_fixture_set, load
from mk1_f5_finalize_review import finalize_review


def main() -> None:
    parser = argparse.ArgumentParser(description="Finalize a ChatGPT Plus manual-observed F5 blind review with independent reviewer enforcement.")
    parser.add_argument("--observation", required=True)
    parser.add_argument("--blind-key", required=True)
    parser.add_argument("--review-packet", required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--baselines", default="mk1/baselines/f5/task-equivalent-minimal.json")
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    observation = load(args.observation)
    if observation.get("mode") != "manual-observed":
        raise ValueError("Plus F5 finalizer accepts manual-observed collections only")
    runtime = observation.get("runtime") or {}
    if runtime.get("provider") != "openai-chatgpt" or runtime.get("family") != "chatgpt-plus":
        raise ValueError("Plus F5 finalizer requires declared ChatGPT Plus runtime identity")

    packet = load(args.review_packet)
    reviewer_ref = str((packet.get("review") or {}).get("reviewer_ref") or "").strip()
    operator_refs = {str(value).strip() for value in observation.get("manual_operator_refs") or [] if str(value).strip()}
    if not operator_refs:
        raise ValueError("Manual F5 observation lacks operator provenance")
    if reviewer_ref and reviewer_ref in operator_refs:
        raise ValueError("Manual F5 blind review must be performed by a reviewer independent from the operator(s) who executed A/B prompts")

    blind_key = load(args.blind_key)
    artifact = load(args.artifact)
    baseline = find_baseline(load(args.baselines), artifact["id"])
    fixture_set = find_fixture_set(load(args.fixtures), artifact["id"])
    execution = finalize_review(observation, blind_key, packet, artifact, baseline, fixture_set)
    execution["mode"] = "manual-observed"
    execution["manual_operator_refs"] = sorted(operator_refs)
    execution["review"]["independent_from_operator"] = True

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(execution, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PLUS_F5_BLIND_REVIEW_FINALIZED",
        "execution_id": execution["execution_id"],
        "reviewer_ref": execution["review"]["reviewer_ref"],
        "operator_refs": sorted(operator_refs),
        "mode": execution["mode"],
        "output": output.as_posix(),
        "policy": "The blind reviewer is independent from the manual operator and semantic A/B mapping was revealed only by finalization.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
