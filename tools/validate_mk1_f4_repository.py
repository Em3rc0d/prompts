from __future__ import annotations

import json
from pathlib import Path

from mk1_behavioral_runner import load
from mk1_promote_tested import promote_tested


RECEIPTS_ROOT = Path("mk1/receipts/f4")
F2_ROOT = Path("mk1/candidates/f2")
F4_ROOT = Path("mk1/candidates/f4")


def index_f2() -> dict[str, dict]:
    result = {}
    for path in sorted(F2_ROOT.glob("*/artifact.json")):
        artifact = load(path)
        result[artifact["id"]] = artifact
    return result


def main() -> None:
    f2 = index_f2()
    receipts = sorted(RECEIPTS_ROOT.glob("*.receipt.json")) if RECEIPTS_ROOT.exists() else []
    receipt_by_id: dict[str, dict] = {}

    for path in receipts:
        receipt = load(path)
        rid = receipt.get("receipt_id")
        if not rid:
            raise SystemExit(f"F4 receipt missing receipt_id: {path}")
        if rid in receipt_by_id:
            raise SystemExit(f"Duplicate F4 receipt_id: {rid}")
        artifact_id = receipt.get("artifact_id")
        if artifact_id not in f2:
            raise SystemExit(f"F4 receipt references unknown F2 artifact: {path} -> {artifact_id}")

        # Reuse the promotion guard as the canonical proof that this receipt
        # is sufficient for VALID -> TESTED.
        promote_tested(f2[artifact_id], receipt)
        receipt_by_id[rid] = receipt

    persisted_tested = sorted(F4_ROOT.glob("*/artifact.json")) if F4_ROOT.exists() else []
    seen_artifacts: set[str] = set()

    for path in persisted_tested:
        artifact = load(path)
        artifact_id = artifact.get("id")
        if artifact.get("state") != "TESTED":
            raise SystemExit(f"F4 candidate artifact must be TESTED: {path}")
        if artifact_id in seen_artifacts:
            raise SystemExit(f"Duplicate persisted F4 artifact id: {artifact_id}")
        seen_artifacts.add(artifact_id)

        if artifact_id not in f2:
            raise SystemExit(f"Persisted F4 artifact has no F2 source: {path}")

        evaluation = artifact.get("evaluation") or {}
        rid = evaluation.get("receipt_id")
        if not rid or rid not in receipt_by_id:
            raise SystemExit(f"Persisted TESTED artifact lacks matching real receipt: {path} -> {rid}")

        expected = promote_tested(f2[artifact_id], receipt_by_id[rid])
        if artifact != expected:
            raise SystemExit(
                "Persisted TESTED artifact does not equal deterministic promotion output: "
                + path.as_posix()
            )

    if not receipts and persisted_tested:
        raise SystemExit("TESTED artifacts exist even though no real F4 receipts exist")

    manifest_path = F4_ROOT / "manifest.json"
    if manifest_path.exists():
        manifest = load(manifest_path)
        if manifest.get("tested_artifact_count") != len(persisted_tested):
            raise SystemExit("F4 manifest tested_artifact_count does not match persisted bundles")
        if not receipts and manifest.get("status") != "NO_REAL_RECEIPTS":
            raise SystemExit("F4 manifest must say NO_REAL_RECEIPTS when no real receipt exists")

    result = {
        "mk1_f4_repository": "PASS",
        "real_receipts": len(receipts),
        "persisted_tested_artifacts": len(persisted_tested),
        "evidence_boundary": "Every persisted TESTED artifact must deterministically reconstruct from a persisted real F4 receipt and its exact F2 source artifact.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
