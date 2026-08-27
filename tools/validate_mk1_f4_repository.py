from __future__ import annotations

import json
from pathlib import Path

from mk1_behavioral_runner import RUNTIME_IDENTITY_FIELDS, find_fixture_set, load, sha256_json
from mk1_promote_tested import promote_tested


RECEIPTS_ROOT = Path("mk1/receipts/f4")
F2_ROOT = Path("mk1/candidates/f2")
F4_ROOT = Path("mk1/candidates/f4")
FIXTURE_DOCUMENT = Path("mk1/fixtures/f4/fixture-sets.json")


def index_f2() -> dict[str, dict]:
    result = {}
    for path in sorted(F2_ROOT.glob("*/artifact.json")):
        artifact = load(path)
        result[artifact["id"]] = artifact
    return result


def main() -> None:
    f2 = index_f2()
    fixture_document = load(FIXTURE_DOCUMENT)
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
        if receipt.get("execution_mode") not in {"api", "manual-observed"}:
            raise SystemExit(f"F4 persisted receipt must represent a real execution: {path}")

        runtime = receipt.get("runtime") or {}
        for key in RUNTIME_IDENTITY_FIELDS:
            if not str(runtime.get(key, "")).strip():
                raise SystemExit(f"F4 receipt runtime missing {key}: {path}")

        try:
            fixture_set = find_fixture_set(fixture_document, receipt.get("fixture_set_id"))
        except KeyError as exc:
            raise SystemExit(f"F4 receipt references unknown fixture set: {path}") from exc

        if fixture_set.get("artifact_id") != artifact_id:
            raise SystemExit(f"F4 receipt fixture set belongs to another artifact: {path}")
        if receipt.get("fixture_set_version") != fixture_set.get("version"):
            raise SystemExit(f"F4 receipt fixture_set_version mismatch: {path}")
        if receipt.get("fixture_set_fingerprint") != sha256_json(fixture_set):
            raise SystemExit(f"F4 receipt fixture_set_fingerprint mismatch: {path}")

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
            raise SystemExit("Persisted TESTED artifact does not equal deterministic promotion output: " + path.as_posix())

    if not receipts and persisted_tested:
        raise SystemExit("TESTED artifacts exist even though no real F4 receipts exist")

    manifest_path = F4_ROOT / "manifest.json"
    if manifest_path.exists():
        manifest = load(manifest_path)
        if manifest.get("tested_artifact_count") != len(persisted_tested):
            raise SystemExit("F4 manifest tested_artifact_count does not match persisted bundles")
        if not receipts and manifest.get("status") != "NO_REAL_RECEIPTS":
            raise SystemExit("F4 manifest must say NO_REAL_RECEIPTS when no real receipt exists")

    print(json.dumps({
        "mk1_f4_repository": "PASS",
        "real_receipts": len(receipts),
        "persisted_tested_artifacts": len(persisted_tested),
        "fixture_fingerprints_verified": len(receipts),
        "runtime_identity_evidence_verified": len(receipts),
        "evidence_boundary": "Every persisted TESTED artifact must deterministically reconstruct from a persisted real F4 receipt, exact F2 prompt body, exact versioned fixture set and evidenced runtime identity.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
