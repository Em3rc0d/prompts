from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from mk1_candidate_assembler import write_bundle


BRIEFS = [
    Path("mk1/briefs/content/clear-rewrite.json"),
    Path("mk1/briefs/software/code-review.json"),
    Path("mk1/briefs/research/technical-decision.json"),
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="mk1/candidates/f2")
    args = parser.parse_args()

    output = Path(args.output)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    records = []
    for brief_path in BRIEFS:
        brief = load(brief_path)
        bundle_dir = output / brief["brief_id"]
        result = write_bundle(brief, bundle_dir)
        artifact = result["artifact"]
        selection = result["architecture"]
        lint = result["lint"]

        if artifact["state"] != "VALID" or lint["status"] != "PASS":
            raise SystemExit(f"F2 builder refuses non-VALID bundle: {artifact['id']} / {lint['status']}")
        if artifact["claims"] != ["engineered"]:
            raise SystemExit(f"F2 builder refuses unsupported claims: {artifact['id']} {artifact['claims']}")
        if artifact["evaluation"]["receipt_id"] is not None:
            raise SystemExit(f"F2 builder refuses pre-populated receipt: {artifact['id']}")

        records.append(
            {
                "brief_path": brief_path.as_posix(),
                "brief_id": brief["brief_id"],
                "artifact_id": artifact["id"],
                "title": artifact["title"],
                "domain": artifact["domain"],
                "intent": artifact["intent"],
                "state": artifact["state"],
                "claims": artifact["claims"],
                "architecture_signature": selection["architecture_signature"],
                "techniques": selection["techniques"],
                "lint_status": lint["status"],
                "lint_warnings": lint["warning_count"],
                "prompt_length": len(artifact["prompt_body"]),
                "bundle_path": bundle_dir.as_posix(),
            }
        )

    manifest = {
        "mk_stage": "MK1",
        "phase": "F2",
        "status": "VALID_CANDIDATES_ONLY",
        "candidate_count": len(records),
        "candidates": records,
        "claim_policy": "F2 artifacts are engineered and statically VALID only. They are not TESTED, CERTIFIED or IMPROVED until later fixture/baseline/rubric receipts exist.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "PROMPT QUARRY — MK1 F2 CANDIDATE INDEX",
        "=" * 88,
        "",
        "These are engineered Prompt Forge artifacts that passed the static contract/linter gate.",
        "They are NOT yet behavior-tested, CERTIFIED or proven improved against a baseline.",
        "",
    ]
    for row in records:
        lines.extend(
            [
                f"TITLE        : {row['title']}",
                f"ARTIFACT ID  : {row['artifact_id']}",
                f"STATE        : {row['state']}",
                f"DOMAIN/INTENT: {row['domain']} / {row['intent']}",
                f"ARCHITECTURE : {row['architecture_signature']}",
                f"LINT         : {row['lint_status']} ({row['lint_warnings']} warnings)",
                f"BUNDLE       : {row['bundle_path']}",
                "-" * 88,
            ]
        )
    (output / "INDEX.txt").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
