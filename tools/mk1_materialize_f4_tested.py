from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from mk1_behavioral_runner import load
from mk1_promote_tested import promote_tested


def index_f2_candidates(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for artifact_path in sorted(root.glob("*/artifact.json")):
        artifact = load(artifact_path)
        artifact_id = artifact["id"]
        if artifact_id in index:
            raise ValueError(f"Duplicate F2 artifact id: {artifact_id}")
        index[artifact_id] = artifact_path.parent
    return index


def copy_if_exists(source: Path, target: Path) -> None:
    if source.exists():
        shutil.copy2(source, target)


def materialize(
    receipts_root: Path,
    source_root: Path,
    critic_root: Path,
    output_root: Path,
    require_at_least: int = 0,
) -> dict:
    f2 = index_f2_candidates(source_root)
    receipt_paths = sorted(receipts_root.glob("*.receipt.json"))

    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    rows = []
    for receipt_path in receipt_paths:
        receipt = load(receipt_path)
        artifact_id = receipt.get("artifact_id")
        if artifact_id not in f2:
            raise ValueError(f"No F2 source artifact found for receipt {receipt_path}: {artifact_id}")

        source_bundle = f2[artifact_id]
        source_artifact = load(source_bundle / "artifact.json")
        tested_artifact = promote_tested(source_artifact, receipt)

        slug = source_bundle.name
        bundle = output_root / slug
        bundle.mkdir(parents=True, exist_ok=True)

        (bundle / "artifact.json").write_text(
            json.dumps(tested_artifact, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (bundle / "behavioral_receipt.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (bundle / "source.json").write_text(
            json.dumps(
                {
                    "source_f2_bundle": source_bundle.as_posix(),
                    "source_f3_critic": (critic_root / f"{slug}.critic.json").as_posix(),
                    "source_f4_receipt": receipt_path.as_posix(),
                    "state_transition": "VALID -> TESTED",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        for name in ("prompt.txt", "architecture.json", "lint.json"):
            copy_if_exists(source_bundle / name, bundle / name)
        copy_if_exists(critic_root / f"{slug}.critic.json", bundle / "critic.json")

        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_version": tested_artifact["version"],
                "state": tested_artifact["state"],
                "fixture_set_id": receipt["fixture_set_id"],
                "receipt_id": receipt["receipt_id"],
                "runtime": receipt["runtime"],
                "bundle": bundle.as_posix(),
            }
        )

    if len(rows) < require_at_least:
        raise SystemExit(f"Expected at least {require_at_least} eligible F4 receipts, got {len(rows)}")

    manifest = {
        "mk_stage": "MK1",
        "phase": "F4B",
        "status": "TESTED_ARTIFACTS_MATERIALIZED" if rows else "NO_REAL_RECEIPTS",
        "tested_artifact_count": len(rows),
        "artifacts": rows,
        "source_policy": "Only persisted real BEHAVIORAL_PASS receipts accepted by mk1_promote_tested may materialize TESTED artifacts.",
        "claim_policy": "TESTED does not imply CANDIDATE, CERTIFIED, or IMPROVED. Baseline comparison remains F5.",
    }
    (output_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipts", default="mk1/receipts/f4")
    parser.add_argument("--source", default="mk1/candidates/f2")
    parser.add_argument("--critics", default="mk1/candidates/f3/reports")
    parser.add_argument("--output", default="mk1/candidates/f4")
    parser.add_argument("--require-at-least", type=int, default=0)
    args = parser.parse_args()

    manifest = materialize(
        receipts_root=Path(args.receipts),
        source_root=Path(args.source),
        critic_root=Path(args.critics),
        output_root=Path(args.output),
        require_at_least=args.require_at_least,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
