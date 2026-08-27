from __future__ import annotations

import json
from pathlib import Path

from mk1_build_f3_critic_reports import bind_critic_receipt, load
from mk1_prompt_critic import critique_artifact


SOURCE = Path("mk1/candidates/f2")
OUTPUT = Path("mk1/candidates/f3")


def index_source() -> dict[str, Path]:
    rows: dict[str, Path] = {}
    for artifact_path in sorted(SOURCE.glob("*/artifact.json")):
        artifact = load(artifact_path)
        artifact_id = artifact["id"]
        if artifact_id in rows:
            raise AssertionError(f"Duplicate F2 artifact id: {artifact_id}")
        rows[artifact_id] = artifact_path.parent
    return rows


def main() -> None:
    manifest_path = OUTPUT / "manifest.json"
    if not manifest_path.exists():
        raise AssertionError("Missing F3 manifest")
    manifest = load(manifest_path)
    if manifest.get("mk_stage") != "MK1" or manifest.get("phase") != "F3" or manifest.get("status") != "STATIC_CRITIC_PASS":
        raise AssertionError("Invalid F3 manifest identity/status")
    if "exact artifact version" not in str(manifest.get("identity_policy", "")):
        raise AssertionError("F3 manifest does not declare exact identity binding")

    source = index_source()
    rows = manifest.get("reports") or []
    by_id = {row.get("artifact_id"): row for row in rows}
    if len(rows) != len(by_id):
        raise AssertionError("Duplicate artifact rows in F3 manifest")
    if set(by_id) != set(source):
        raise AssertionError(f"F3 source/report inventory mismatch: source={sorted(source)} reports={sorted(by_id)}")

    for artifact_id, bundle in source.items():
        artifact = load(bundle / "artifact.json")
        lint = load(bundle / "lint.json")
        if artifact.get("state") != "VALID" or lint.get("status") != "PASS":
            raise AssertionError(f"F3 source is no longer VALID/lint PASS: {artifact_id}")

        expected_raw = critique_artifact(artifact)
        if expected_raw.get("status") != "PASS":
            raise AssertionError(f"Current F2 artifact no longer passes F3 critic: {artifact_id}")
        expected = bind_critic_receipt(artifact, expected_raw, bundle)
        identity = expected["source_identity"]

        row = by_id[artifact_id]
        checks = {
            "artifact_version": artifact["version"],
            "source_bundle": bundle.as_posix(),
            "prompt_fingerprint": identity["prompt_fingerprint"],
            "artifact_fingerprint": identity["artifact_fingerprint"],
            "artifact_state": "VALID",
            "critic_status": "PASS",
            "critic_version": expected["critic_version"],
            "blocking": 0,
            "errors": 0,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                raise AssertionError(f"F3 manifest binding mismatch for {artifact_id}.{key}: expected={value!r} got={row.get(key)!r}")

        critic_path = Path(row["critic_json"])
        human_path = Path(row["critic_txt"])
        if not critic_path.exists() or not human_path.exists():
            raise AssertionError(f"F3 receipt files missing for {artifact_id}")
        observed = load(critic_path)
        if observed != expected:
            raise AssertionError(f"F3 critic receipt is stale or cannot be reconstructed: {artifact_id}")

        human = human_path.read_text(encoding="utf-8")
        if identity["prompt_fingerprint"] not in human or identity["artifact_fingerprint"] not in human:
            raise AssertionError(f"F3 human receipt omits frozen identity: {artifact_id}")

    if manifest.get("report_count") != len(source):
        raise AssertionError("F3 report_count mismatch")

    print(json.dumps({
        "mk1_f3_repository": "PASS",
        "reports": len(source),
        "identity_binding": "artifact-version+prompt-sha256+artifact-sha256",
        "state": "STATIC_CRITIC_PASS",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
