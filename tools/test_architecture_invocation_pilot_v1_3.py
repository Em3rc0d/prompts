from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from build_architecture_invocation_pilot_v1_3 import (
    LEARNING_ANSWER_KEY,
    build_pilot,
    write_pilot,
)


class ArchitectureInvocationPilotV13Tests(unittest.TestCase):
    def test_closes_v12_learning_key_finding(self) -> None:
        _, _, manifest = build_pilot()
        self.assertEqual(manifest["closed_findings"], ["BIND-V12-LEARN-001"])
        self.assertEqual(manifest["learning_answer_key_runtime_exposure"], 0)

    def test_learning_runtime_examples_have_no_ground_truth(self) -> None:
        bindings, invocations, _ = build_pilot()
        learning = next(row for row in bindings if row["mode"] == "learning")
        examples = learning["instance"]["assessment_examples"]
        self.assertEqual(len(examples), 5)
        self.assertTrue(all(set(row) == {"id", "text"} for row in examples))
        self.assertEqual({row["id"] for row in examples}, set(LEARNING_ANSWER_KEY))
        self.assertIn("Do not reveal or invent an answer key", learning["configuration"]["assessment_delivery_policy"])

        for row in invocations:
            if row["mode"] != "learning":
                continue
            for payload in row["_bytes"]:
                self.assertNotIn(b'"ground_truth"', payload)
                self.assertNotIn(b'"assessment_answer_key"', payload)

    def test_learning_answer_key_is_evaluation_only(self) -> None:
        _, invocations, _ = build_pilot()
        for row in invocations:
            if row["mode"] != "learning":
                continue
            evaluation = row["evaluation_contract"]
            self.assertEqual(evaluation["assessment_answer_key"], LEARNING_ANSWER_KEY)
            self.assertFalse(evaluation["assessment_key_is_runtime_input"])
            self.assertFalse(evaluation["evaluation_metadata_is_runtime_input"])
            self.assertEqual(evaluation["expected_state_set"], ["IN_PROGRESS"])
            self.assertIn("OBJECTIVE_MET is not claimed on the initial turn", evaluation["mode_specific_assertions"])

    def test_truth_boundary_remains_zero_behavior(self) -> None:
        bindings, invocations, manifest = build_pilot()
        self.assertEqual(len(bindings), 9)
        self.assertEqual(len(invocations), 18)
        self.assertEqual(manifest["external_model_calls"], 0)
        self.assertEqual(manifest["behavioral_observations"], 0)
        self.assertEqual(manifest["behavioral_claims_created"], 0)
        self.assertEqual(manifest["high_stakes_bindings"], 0)
        self.assertEqual(manifest["authority_escalations"], 0)
        self.assertFalse(manifest["bulk_regeneration_allowed"])
        self.assertTrue(all(row["runtime_executed"] is False for row in invocations))
        self.assertTrue(all(row["behavioral_claim"] == "NONE" for row in invocations))
        self.assertTrue(all(row["ready_to_sell"] is False for row in invocations))

    def test_renderer_does_not_leak_evaluation_contract_into_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pilot"
            write_pilot(out)
            rows = [json.loads(line) for line in (out / "invocations.jsonl").read_text(encoding="utf-8").splitlines() if line]
            learning_rows = [row for row in rows if row["mode"] == "learning"]
            self.assertEqual(len(learning_rows), 2)
            for row in learning_rows:
                self.assertIn("assessment_answer_key", row["evaluation_contract"])
                for rel in row["block_paths"]:
                    payload = (out / rel).read_bytes()
                    self.assertNotIn(b'"ground_truth"', payload)
                    self.assertNotIn(b'"assessment_answer_key"', payload)
                    self.assertNotIn(b"expected_state_set", payload)
                    self.assertNotIn(b"cross_cutting_assertions", payload)

    def test_renderer_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            write_pilot(first)
            write_pilot(second)
            for filename in ("bindings.jsonl", "invocations.jsonl", "manifest.json"):
                self.assertEqual((first / filename).read_bytes(), (second / filename).read_bytes())
            first_files = sorted(path.relative_to(first) for path in (first / "packets").rglob("*.*"))
            second_files = sorted(path.relative_to(second) for path in (second / "packets").rglob("*.*"))
            self.assertEqual(first_files, second_files)
            for rel in first_files:
                self.assertEqual((first / rel).read_bytes(), (second / rel).read_bytes())


if __name__ == "__main__":
    unittest.main()
