from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from mk1_prompt_critic import critique_artifact


SOURCE_ROOT = Path("mk1/candidates/f2")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def human_report(artifact: dict, critic: dict, source_bundle: Path) -> str:
    lines = [
        "PROMPT QUARRY — MK1 F3 STATIC CRITIC RECEIPT",
        "=" * 88,
        f"TITLE             : {artifact['title']}",
        f"ARTIFACT ID       : {artifact['id']}",
        f"ARTIFACT STATE    : {artifact['state']}",
        f"CRITIC STATUS     : {critic['status']}",
        f"CRITIC VERSION    : {critic['critic_version']}",
        f"BLOCKING FINDINGS : {critic['counts']['blocking']}",
        f"ERROR FINDINGS    : {critic['counts']['error']}",
        f"WARNING FINDINGS  : {critic['counts']['warning']}",
        f"SOURCE BUNDLE     : {source_bundle.as_posix()}",
        "CLAIM             : static critic characterization only",
        "",
        "WHAT THIS MEANS",
        "-" * 88,
        "F3 reviews semantic/static quality beyond schema/lint: contradictions, duplicated instructions,",
        "output-contract specificity, assumptions, provenance wording and high-stakes boundaries.",
        "A PASS here does NOT mean runtime behavior was tested and does NOT certify or prove improvement.",
        "",
        "FINDINGS",
        "-" * 88,
    ]
    if not critic["findings"]:
        lines.append("No F3 static critic findings for this artifact.")
    else:
        for finding in critic["findings"]:
            lines.extend(
                [
                    f"[{finding['severity'].upper()}] {finding['code']}",
                    f"  {finding['message']}",
                    f"  Remediation: {finding['remediation']}",
                ]
            )
    lines.extend(
        [
            "",
            "NEXT EVIDENCE REQUIRED",
            "-" * 88,
            "F4 must execute behavioral fixtures before this artifact may become TESTED.",
            "F5 must provide fair baseline comparison before any IMPROVED claim.",
            "F6 must apply the certification rubric/receipt before CERTIFIED.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=SOURCE_ROOT.as_posix())
    parser.add_argument("--output", default="mk1/candidates/f3")
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)
    if not source.exists():
        raise SystemExit(f"Missing F2 candidate root: {source}")
    if output.exists():
        shutil.rmtree(output)
    reports_dir = output / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for artifact_path in sorted(source.glob("*/artifact.json")):
        bundle = artifact_path.parent
        artifact = load(artifact_path)
        lint = load(bundle / "lint.json")
        if artifact.get("state") != "VALID" or lint.get("status") != "PASS":
            raise SystemExit(f"F3 refuses non-VALID/non-PASS F2 artifact: {artifact_path}")

        critic = critique_artifact(artifact)
        if critic["status"] != "PASS":
            raise SystemExit(
                f"F3 critic did not pass for {artifact['id']}: "
                + json.dumps(critic, ensure_ascii=False)
            )

        stem = bundle.name
        json_path = reports_dir / f"{stem}.critic.json"
        txt_path = reports_dir / f"{stem}.critic.txt"
        json_path.write_text(json.dumps(critic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        txt_path.write_text(human_report(artifact, critic, bundle), encoding="utf-8")

        records.append(
            {
                "artifact_id": artifact["id"],
                "title": artifact["title"],
                "source_bundle": bundle.as_posix(),
                "artifact_state": artifact["state"],
                "critic_status": critic["status"],
                "blocking": critic["counts"]["blocking"],
                "errors": critic["counts"]["error"],
                "warnings": critic["counts"]["warning"],
                "critic_json": json_path.as_posix(),
                "critic_txt": txt_path.as_posix(),
            }
        )

    manifest = {
        "mk_stage": "MK1",
        "phase": "F3",
        "status": "STATIC_CRITIC_PASS",
        "report_count": len(records),
        "reports": records,
        "state_policy": "F3 critic PASS does not advance artifact state beyond VALID. Behavioral TESTED begins only in F4.",
        "claim_policy": "No CERTIFIED or IMPROVED claim is produced by F3.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "PROMPT QUARRY — MK1 F3 STATIC CRITIC INDEX",
        "=" * 88,
        "",
        "F3 adds semantic/static quality receipts to the existing F2 VALID candidates.",
        "These are NOT behavioral test receipts and do not change candidate state to TESTED.",
        "",
    ]
    for row in records:
        lines.extend(
            [
                f"TITLE        : {row['title']}",
                f"ARTIFACT ID  : {row['artifact_id']}",
                f"STATE        : {row['artifact_state']}",
                f"CRITIC       : {row['critic_status']} ({row['warnings']} warnings)",
                f"HUMAN REPORT : {row['critic_txt']}",
                "-" * 88,
            ]
        )
    (output / "INDEX.txt").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    if len(records) != 3:
        raise SystemExit(f"Expected 3 F2 artifacts for current F3 baseline, got {len(records)}")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
