from __future__ import annotations

import json
from pathlib import Path


F4_FIXTURES = Path("mk1/fixtures/f4/fixture-sets.json")
DERIVATION_MAP = Path("mk1/fixtures/f4/mk0-derivation-map.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    f4 = load(F4_FIXTURES)
    bridge = load(DERIVATION_MAP)

    golden_path = Path(bridge["mk0_golden_dataset"]["fixtures_path"])
    golden_manifest_path = Path(bridge["mk0_golden_dataset"]["manifest_path"])
    if not golden_path.exists() or not golden_manifest_path.exists():
        raise SystemExit("MK0 golden dataset paths declared by F4 derivation map do not exist")

    golden = load(golden_path)
    golden_manifest = load(golden_manifest_path)
    golden_by_id = {row["fixture_id"]: row for row in golden.get("fixtures", [])}

    expected_records = bridge["mk0_golden_dataset"].get("expected_fixture_records")
    if expected_records != len(golden_by_id):
        raise SystemExit(
            f"MK0 golden fixture count drift: bridge={expected_records}, actual={len(golden_by_id)}"
        )
    if golden_manifest.get("fixture_records") != len(golden_by_id):
        raise SystemExit("MK0 golden manifest fixture_records does not match actual fixture inventory")

    f4_by_id = {row["fixture_set_id"]: row for row in f4.get("fixture_sets", [])}
    mappings = bridge.get("mappings", [])
    map_by_set: dict[str, dict] = {}
    derivation_ids: set[str] = set()
    referenced_mk0: set[str] = set()

    for mapping in mappings:
        derivation_id = mapping.get("derivation_id")
        if not derivation_id or derivation_id in derivation_ids:
            raise SystemExit(f"Missing/duplicate derivation_id: {derivation_id!r}")
        derivation_ids.add(derivation_id)

        set_id = mapping.get("f4_fixture_set_id")
        if set_id in map_by_set:
            raise SystemExit(f"Duplicate F4 derivation mapping: {set_id}")
        if set_id not in f4_by_id:
            raise SystemExit(f"Derivation map references unknown F4 fixture set: {set_id}")
        map_by_set[set_id] = mapping

        f4_set = f4_by_id[set_id]
        if mapping.get("artifact_id") != f4_set.get("artifact_id"):
            raise SystemExit(f"Derivation artifact_id mismatch for {set_id}")
        if mapping.get("relationship") != "architecture-evidence-not-behavioral-copy":
            raise SystemExit(f"Unexpected derivation relationship for {set_id}")
        if mapping.get("mk1_behavioral_case_origin") != "authored-in-mk1":
            raise SystemExit(f"F4 behavioral origin must be explicit for {set_id}")

        refs = mapping.get("mk0_fixture_refs") or []
        if not refs:
            raise SystemExit(f"F4 fixture set lacks MK0 evidence refs: {set_id}")

        for ref in refs:
            fixture_id = ref.get("fixture_id")
            if fixture_id not in golden_by_id:
                raise SystemExit(f"F4 references unknown MK0 golden fixture: {fixture_id}")
            mk0 = golden_by_id[fixture_id]
            referenced_mk0.add(fixture_id)

            if ref.get("title") != mk0.get("title"):
                raise SystemExit(f"MK0 fixture title drift for {fixture_id}")

            declared_support = set(ref.get("supports") or [])
            actual_techniques = set(mk0.get("techniques") or [])
            unsupported = sorted(declared_support - actual_techniques)
            if unsupported:
                raise SystemExit(
                    f"F4 claims unsupported MK0 techniques for {fixture_id}: {unsupported}"
                )

    missing_mappings = sorted(set(f4_by_id) - set(map_by_set))
    extra_mappings = sorted(set(map_by_set) - set(f4_by_id))
    if missing_mappings or extra_mappings:
        raise SystemExit(
            f"F4/MK0 derivation coverage mismatch: missing={missing_mappings}, extra={extra_mappings}"
        )

    # Per-case direct lineage must remain honest. If a case declares an MK0
    # fixture id, it must exist. Empty arrays are explicitly allowed because
    # these behavioral cases are authored in MK1 rather than copied from MK0.
    direct_refs = 0
    behavioral_cases = 0
    for fixture_set in f4_by_id.values():
        for case in fixture_set.get("cases", []):
            behavioral_cases += 1
            provenance = case.get("provenance") or {}
            for fixture_id in provenance.get("mk0_fixture_ids") or []:
                direct_refs += 1
                if fixture_id not in golden_by_id:
                    raise SystemExit(
                        f"Behavioral case {case.get('fixture_id')} declares unknown direct MK0 lineage: {fixture_id}"
                    )

    result = {
        "mk1_fixture_provenance": "PASS",
        "mk0_golden_fixtures": len(golden_by_id),
        "f4_fixture_sets": len(f4_by_id),
        "f4_behavioral_cases": behavioral_cases,
        "f4_sets_with_mk0_derivation": len(map_by_set),
        "unique_mk0_golden_refs_used": len(referenced_mk0),
        "direct_case_lineage_refs": direct_refs,
        "policy": "MK0 golden fixtures provide verified structural/technique evidence. MK1 F4 behavioral cases remain explicitly authored in MK1 unless direct lineage is genuinely declared."
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
