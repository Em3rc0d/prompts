from __future__ import annotations

import argparse
import copy
import json
import shutil
from pathlib import Path

from mk1_behavioral_runner import sha256_json, sha256_text
from mk1_prompt_critic import critique_artifact


SOURCE_ROOT = Path("mk1/candidates/f2")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def bind_critic_receipt(artifact: dict, critic: dict, source_bundle: Path) -> dict:
    """Bind a static critic result to the exact F2 artifact it reviewed.

    F3 is static evidence, but it must still be immutable evidence.  A critic
    generated for an older prompt must never remain valid after prompt or
    artifact drift.
    """
    bound = copy.deepcopy(critic)
    bound["source_identity"] = {
        "artifact_id": artifact["id"],
        "artifact_version": artifact["version"],
        "prompt_fingerprint": sha256_text(artifact["prompt_body"]),
        "artifact_fingerprint": sha256_json(artifact),
        "source_bundle": source_bundle.as_posix(),
    }
    return bound


def human_report(artifact: dict, critic: dict, source_bundle: Path) -> str:
    identity = critic["source_identity"]
    lines = [
        "PROMPT QUARRY — MK1 F3 STATIC CRITIC RECEIPT",
        "=" * 88,
        f"TITLE             : {artifact['title']}",
        f"ARTIFACT ID       : {artifact['id']}",
        f"ARTIFACT VERSION  : {artifact['version']}",
        f"ARTIFACT STATE    : {artifact['state']}",
        f"PROMPT SHA-256    : {identity['prompt_fingerprint']}",
        f"ARTIFACT SHA-256  : {identity['artifact_fingerprint']}",
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
        "The receipt is cryptographically bound to the exact F2 prompt and artifact reviewed.",
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
            "F6 must provide cross-runtime evidence before CERTIFIED.",
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
        critic = bind_critic_receipt(artifact, critic, bundle)
        identity = critic["source_identity"]

        stem = bundle.name
        json_path = reports_dir / f"{stem}.critic.json"
        txt_path = reports_dir / f"{stem}.critic.txt"
        json_path.write_text(json.dumps(critic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        txt_path.write_text(human_report(artifact, critic, bundle), encoding="utf-8")

        records.append(
            {
                "artifact_id": artifact["id"],
                "artifact_version": artifact["version"],
                "title": artifact["title"],
                "source_bundle": bundle.as_posix(),
                "prompt_fingerprint": identity["prompt_fingerprint"],
                "artifact_fingerprint": identity["artifact_fingerprint"],
                "artifact_state": artifact["state"],
                "critic_status": critic["status"],
                "critic_version": critic["critic_version"],
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
        "identity_policy": "Every F3 critic receipt is bound to the exact artifact version, prompt SHA-256 and canonical artifact SHA-256 reviewed. Any drift invalidates the receipt.",
        "state_policy": "F3 critic PASS does not advance artifact state beyond VALID. Behavioral TESTED begins only in F4.",
        "claim_policy": "No CERTIFIED or IMPROVED claim is produced by F3.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "PROMPT QUARRY — MK1 F3 STATIC CRITIC INDEX",
        "=" * 88,
        "",
        "F3 adds semantic/static quality receipts to the existing F2 VALID candidates.",
        "Each receipt is frozen to the exact prompt/artifact identity shown below.",
        "These are NOT behavioral test receipts and do not change candidate state to TESTED.",
        "",
    ]
    for row in records:
        lines.extend(
            [
                f"TITLE        : {row['title']}",
                f"ARTIFACT ID  : {row['artifact_id']}",
                f"VERSION      : {row['artifact_version']}",
                f"STATE        : {row['artifact_state']}",
                f"PROMPT SHA   : {row['prompt_fingerprint']}",
                f"ARTIFACT SHA : {row['artifact_fingerprint']}",
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
