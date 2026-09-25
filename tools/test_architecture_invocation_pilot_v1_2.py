from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from build_architecture_invocation_pilot_v1_2 import (
    EXPECTED_STATE_SETS,
    PROTOCOL,
    build_pilot,
    write_pilot,
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ArchitectureInvocationPilotV12Tests(unittest.TestCase):
    def test_successor_closes_all_recorded_findings(self) -> None:
        _, _, manifest = build_pilot()
        self.assertEqual(set(manifest["closed_findings"]), {
            "BIND-V1-PROTO-001",
            "BIND-V1-LEARN-001",
            "BIND-V1-OPT-001",
            "BIND-V1-EVAL-001",
        })

    def test_counts_and_truth_boundary(self) -> None:
        bindings, invocations, manifest = build_pilot()
        self.assertEqual(len(bindings), 9)
        self.assertEqual(len(invocations), 18)
        self.assertEqual(manifest["architecture_count"], 9)
        self.assertEqual(manifest["binding_count"], 9)
        self.assertEqual(manifest["invocation_count"], 18)
        self.assertEqual(manifest["external_model_calls"], 0)
        self.assertEqual(manifest["behavioral_observations"], 0)
        self.assertEqual(manifest["behavioral_claims_created"], 0)
        self.assertEqual(manifest["high_stakes_bindings"], 0)
        self.assertEqual(manifest["authority_escalations"], 0)
        self.assertFalse(manifest["bulk_regeneration_allowed"])
        self.assertTrue(all(row["authority"] == "ADVISORY_ONLY" for row in bindings))
        self.assertTrue(all(row["risk_class"] == "LOW" for row in bindings))
        self.assertTrue(all(row["high_stakes"] is False for row in bindings))

    def test_configuration_block_defines_resolution_semantics(self) -> None:
        _, invocations, _ = build_pilot()
        for row in invocations:
            config = row["_bytes"][1].decode("utf-8")
            self.assertTrue(config.startswith("AUTHORIZED_WORKFLOW_CONFIGURATION_V1\n"))
            payload = json.loads(config.split("\n", 1)[1])
            semantics = payload["binding_semantics"]
            self.assertEqual(semantics["configuration_surface"], "THIS_BLOCK_ONLY")
            self.assertIn("configuration", semantics["source_roots"])
            self.assertIn("instance", semantics["source_roots"])
            self.assertIn("BLOCKED", semantics["unresolved_rule"])
            self.assertIn("UNTRUSTED_TASK_DATA", semantics["data_rule"])

    def test_learning_has_exactly_five_supplied_assessment_examples(self) -> None:
        bindings, _, _ = build_pilot()
        learning = next(row for row in bindings if row["mode"] == "learning")
        examples = learning["instance"]["assessment_examples"]
        self.assertEqual(len(examples), 5)
        self.assertEqual({row["ground_truth"] for row in examples}, {"DETERMINISTIC", "BEHAVIORAL"})
        self.assertEqual(len({row["id"] for row in examples}), 5)
        self.assertIn("4 of 5", learning["configuration"]["objective_assessment_threshold"])

    def test_optimization_supplies_concrete_baseline_artifact(self) -> None:
        bindings, _, _ = build_pilot()
        optimization = next(row for row in bindings if row["mode"] == "optimization")
        baseline = optimization["instance"]["current_baseline"]
        self.assertGreater(len(baseline.split()), 25)
        for required_fact in ["478", "9 architecture mothers", "Behavioral testing", "Bulk regeneration"]:
            self.assertIn(required_fact, baseline)
        self.assertIn("five facts", optimization["instance"]["optimization_objective"])
        self.assertIn("five-fact retention", optimization["instance"]["metrics"])

    def test_expected_state_contract_is_out_of_band_only(self) -> None:
        _, invocations, _ = build_pilot()
        self.assertEqual({row["mode"] for row in invocations}, set(EXPECTED_STATE_SETS))
        for row in invocations:
            evaluation = row["evaluation_contract"]
            self.assertEqual(evaluation["expected_state_set"], EXPECTED_STATE_SETS[row["mode"]])
            self.assertFalse(evaluation["evaluation_metadata_is_runtime_input"])
            self.assertGreater(len(evaluation["cross_cutting_assertions"]), 4)
            for payload in row["_bytes"]:
                self.assertNotIn(b"expected_state_set", payload)
                self.assertNotIn(b"cross_cutting_assertions", payload)

    def test_override_changes_only_instance_block(self) -> None:
        _, invocations, _ = build_pilot()
        by_mode: dict[str, dict[str, dict]] = {}
        for row in invocations:
            by_mode.setdefault(row["mode"], {})[row["variant"]] = row
        for mode, variants in by_mode.items():
            normal = variants["NORMAL"]
            override = variants["EMBEDDED_OVERRIDE"]
            self.assertEqual(normal["blocks"][0]["sha256"], override["blocks"][0]["sha256"], mode)
            self.assertEqual(normal["blocks"][1]["sha256"], override["blocks"][1]["sha256"], mode)
            self.assertNotEqual(normal["blocks"][2]["sha256"], override["blocks"][2]["sha256"], mode)
            self.assertNotIn(b"OVERRIDE_ACCEPTED", override["_bytes"][0])
            self.assertNotIn(b"OVERRIDE_ACCEPTED", override["_bytes"][1])
            self.assertIn(b"OVERRIDE_ACCEPTED", override["_bytes"][2])

    def test_protocol_remains_exact_three_block_same_role(self) -> None:
        _, invocations, _ = build_pilot()
        for row in invocations:
            self.assertEqual(row["protocol"], PROTOCOL)
            self.assertEqual(row["role"], "user")
            self.assertEqual([block["kind"] for block in row["blocks"]], [
                "FROZEN_ARCHITECTURE",
                "AUTHORIZED_CONFIGURATION",
                "UNTRUSTED_INSTANCE_DATA",
            ])
            self.assertEqual([block["index"] for block in row["blocks"]], [1, 2, 3])

    def test_renderer_persists_exact_blocks_and_no_evaluation_metadata_in_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pilot"
            manifest = write_pilot(out)
            rows = [json.loads(line) for line in (out / "invocations.jsonl").read_text(encoding="utf-8").splitlines() if line]
            self.assertEqual(manifest["renderer_version"], "1.2.0")
            self.assertEqual(len(rows), 18)
            for row in rows:
                self.assertEqual(len(row["block_paths"]), 3)
                for index, rel in enumerate(row["block_paths"]):
                    path = out / rel
                    self.assertTrue(path.is_file())
                    self.assertEqual(sha256_file(path), row["blocks"][index]["sha256"])
                    payload = path.read_bytes()
                    self.assertNotIn(b"expected_state_set", payload)
                    self.assertNotIn(b"cross_cutting_assertions", payload)

    def test_renderer_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            write_pilot(first)
            write_pilot(second)
            self.assertEqual((first / "bindings.jsonl").read_bytes(), (second / "bindings.jsonl").read_bytes())
            self.assertEqual((first / "invocations.jsonl").read_bytes(), (second / "invocations.jsonl").read_bytes())
            self.assertEqual((first / "manifest.json").read_bytes(), (second / "manifest.json").read_bytes())
            first_files = sorted(path.relative_to(first) for path in (first / "packets").rglob("*.*"))
            second_files = sorted(path.relative_to(second) for path in (second / "packets").rglob("*.*"))
            self.assertEqual(first_files, second_files)
            for rel in first_files:
                self.assertEqual((first / rel).read_bytes(), (second / rel).read_bytes())


if __name__ == "__main__":
    unittest.main()
