from __future__ import annotations

import copy
import json
from pathlib import Path

from validate_product_manifest import semantic_errors, schema_errors


MANIFEST = Path("product/developer-pack-v1/MANIFEST.draft.json")


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def assert_has(errors: list[str], fragment: str) -> None:
    assert any(fragment in error for error in errors), (fragment, errors)


def test_current_draft_schema_passes() -> None:
    manifest = load_manifest()
    assert schema_errors(manifest) == []
    assert semantic_errors(manifest, Path(".")) == []


def test_unknown_field_fails_closed() -> None:
    manifest = load_manifest()
    manifest["magic_marketing_claim"] = True
    assert_has(schema_errors(manifest), "Additional properties are not allowed")


def test_valid_cannot_claim_tested() -> None:
    manifest = load_manifest()
    manifest["artifacts"] = [
        {
            "artifact_id": "pq-bad-claim",
            "path": "product/developer-pack-v1/SPEC.md",
            "artifact_type": "methodology",
            "authority": "prompt-quarry",
            "provenance_class": "product-authored",
            "maturity_state": "VALID",
            "claims": ["engineered", "valid", "tested"],
            "evidence_refs": [],
            "sha256": None,
            "distribution": {
                "include": False,
                "customer_visible": False,
                "redistributable": False,
            },
        }
    ]
    assert schema_errors(manifest)


def test_bundled_generator_rejects_non_pass_receipt() -> None:
    manifest = load_manifest()
    manifest["generator_v0"]["bundled"] = True
    manifest["generator_v0"]["receipt_status"] = "FAIL"
    assert schema_errors(manifest)


def test_bundled_generator_rejects_receipt_commit_mismatch() -> None:
    manifest = load_manifest()
    manifest["generator_v0"]["bundled"] = True
    manifest["generator_v0"]["receipt_status"] = "PASS"
    manifest["generator_v0"]["receipt_source_commit"] = "0" * 40
    assert_has(semantic_errors(manifest, Path(".")), "receipt_source_commit does not match canonical receipt")


def test_duplicate_ids_are_rejected() -> None:
    manifest = load_manifest()
    artifact = {
        "artifact_id": "pq-duplicate",
        "path": "product/developer-pack-v1/SPEC.md",
        "artifact_type": "methodology",
        "authority": "prompt-quarry",
        "provenance_class": "product-authored",
        "maturity_state": "DRAFT",
        "claims": ["engineered"],
        "evidence_refs": [],
        "sha256": None,
        "distribution": {
            "include": False,
            "customer_visible": False,
            "redistributable": False,
        },
    }
    second = copy.deepcopy(artifact)
    second["path"] = "product/PRODUCT_MANIFEST.md"
    manifest["artifacts"] = [artifact, second]
    assert_has(semantic_errors(manifest, Path(".")), "duplicate artifact_id")


def test_included_nonexistent_path_is_rejected() -> None:
    manifest = load_manifest()
    manifest["artifacts"] = [
        {
            "artifact_id": "pq-missing-file",
            "path": "product/developer-pack-v1/DOES-NOT-EXIST.md",
            "artifact_type": "methodology",
            "authority": "prompt-quarry",
            "provenance_class": "product-authored",
            "maturity_state": "VALID",
            "claims": ["engineered", "valid"],
            "evidence_refs": [],
            "sha256": "sha256:" + "0" * 64,
            "distribution": {
                "include": True,
                "customer_visible": True,
                "redistributable": True,
            },
        }
    ]
    assert_has(semantic_errors(manifest, Path(".")), "included path does not exist")


def test_unknown_dependency_is_rejected() -> None:
    manifest = load_manifest()
    manifest["artifacts"] = [
        {
            "artifact_id": "pq-dependent",
            "path": "product/developer-pack-v1/SPEC.md",
            "artifact_type": "methodology",
            "authority": "prompt-quarry",
            "provenance_class": "product-authored",
            "maturity_state": "DRAFT",
            "claims": ["engineered"],
            "evidence_refs": [],
            "sha256": None,
            "dependencies": ["pq-does-not-exist"],
            "distribution": {
                "include": False,
                "customer_visible": False,
                "redistributable": False,
            },
        }
    ]
    assert_has(semantic_errors(manifest, Path(".")), "unknown dependency")


def main() -> None:
    tests = [
        test_current_draft_schema_passes,
        test_unknown_field_fails_closed,
        test_valid_cannot_claim_tested,
        test_bundled_generator_rejects_non_pass_receipt,
        test_bundled_generator_rejects_receipt_commit_mismatch,
        test_duplicate_ids_are_rejected,
        test_included_nonexistent_path_is_rejected,
        test_unknown_dependency_is_rejected,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)} product-manifest tests")


if __name__ == "__main__":
    main()
