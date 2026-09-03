from __future__ import annotations

import unittest

from build_prompt_architecture_pilot_v2_1 import MODE_BINDINGS, build_records


class PromptArchitecturePilotV21Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = {row["mode"]: row for row in build_records()}

    def test_nine_distinct_blueprints_remain(self) -> None:
        self.assertEqual(len(self.records), 9)
        self.assertEqual(set(self.records), set(MODE_BINDINGS))
        self.assertEqual(len({row["prompt_sha256"] for row in self.records.values()}), 9)

    def test_general_unsupported_does_not_execute_domain_result(self) -> None:
        body = self.records["general"]["prompt_body"]
        self.assertIn("Not executed when BLOCKED or UNSUPPORTED", body)
        self.assertIn("safe partial evidence", body.casefold())

    def test_audit_has_blocked_distinct_from_insufficient_evidence(self) -> None:
        body = self.records["audit"]["prompt_body"]
        self.assertIn("BLOCKED — the minimum audit definition is absent", body)
        self.assertIn("INSUFFICIENT_EVIDENCE — target, scope, and rubric are defined", body)
        self.assertIn("Audit status: COMPLETE | COMPLETE_WITH_UNKNOWNS | INSUFFICIENT_EVIDENCE | BLOCKED", body)
        self.assertIn("NONE when BLOCKED", body)

    def test_simulation_output_contract_includes_ready(self) -> None:
        body = self.records["simulation"]["prompt_body"]
        self.assertIn("Simulation state: READY | IN_PROGRESS | COMPLETE | BLOCKED", body)
        self.assertIn("IN_PROGRESS — valid only for INTERACTIVE", body)

    def test_all_prior_quality_invariants_survive(self) -> None:
        for row in self.records.values():
            body = row["prompt_body"]
            self.assertIn("INSTRUCTION / DATA BOUNDARY", body)
            self.assertIn("STATE POLICY", body)
            self.assertIn("HIGH-STAKES BINDING BOUNDARY", body)
            self.assertIn("PRODUCT EVIDENCE BOUNDARY", body)
            self.assertEqual(row["state"], "STATIC_REVIEW_REQUIRED")
            self.assertFalse(row["automatic_product_promotion"])
            self.assertFalse(row["behavioral_evidence"])
            self.assertFalse(row["ready_to_sell"])


if __name__ == "__main__":
    unittest.main()
