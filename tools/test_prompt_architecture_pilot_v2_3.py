from __future__ import annotations

import unittest

from build_prompt_architecture_pilot_v2_3 import build_records


class PromptArchitecturePilotV23Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = {row["mode"]: row for row in build_records()}

    def test_nine_distinct_blueprints(self) -> None:
        self.assertEqual(len(self.records), 9)
        self.assertEqual(len({row["prompt_sha256"] for row in self.records.values()}), 9)

    def test_common_preflight_blocks_missing_minimum_required_inputs(self) -> None:
        expected = (
            "PREFLIGHT INVARIANT — If any configured minimum required input is absent or contradictory enough "
            "that its intended meaning cannot be established, choose BLOCKED and do not execute the domain procedure."
        )
        for row in self.records.values():
            self.assertIn(expected, row["prompt_body"])

    def test_generation_no_valid_candidate_is_scoped_to_evaluated_set(self) -> None:
        body = self.records["generation"]["prompt_body"]
        self.assertIn("none of the generated/evaluated candidates", body)
        self.assertIn("scoped to the evaluated set", body)
        self.assertIn("not proof that no conceivable candidate exists", body)
        self.assertIn("state whether the configured search space was exhaustive", body)

    def test_learning_cannot_claim_objective_met_without_configured_threshold(self) -> None:
        body = self.records["learning"]["prompt_body"]
        self.assertIn("If no objective assessment threshold has been configured, OBJECTIVE_MET is forbidden", body)
        self.assertIn("remain READY or IN_PROGRESS", body)

    def test_prior_semantic_fixes_survive(self) -> None:
        general = self.records["general"]["prompt_body"]
        audit = self.records["audit"]["prompt_body"]
        simulation = self.records["simulation"]["prompt_body"]
        generation = self.records["generation"]["prompt_body"]
        checklist = self.records["checklist"]["prompt_body"]
        self.assertIn("Not executed when BLOCKED or UNSUPPORTED", general)
        self.assertIn("INSUFFICIENT_EVIDENCE — target, scope, and rubric are defined", audit)
        self.assertIn("never evidence of the user's ability or performance", simulation)
        self.assertIn("Under HOLD, return the tied viable shortlist", generation)
        self.assertIn("missing evidence never becomes PASS", checklist)

    def test_fail_closed_product_boundary_survives(self) -> None:
        for row in self.records.values():
            body = row["prompt_body"]
            self.assertIn("INSTRUCTION / DATA BOUNDARY", body)
            self.assertIn("HIGH-STAKES BINDING BOUNDARY", body)
            self.assertIn("PRODUCT EVIDENCE BOUNDARY", body)
            self.assertEqual(row["state"], "STATIC_REVIEW_REQUIRED")
            self.assertFalse(row["automatic_product_promotion"])
            self.assertFalse(row["behavioral_evidence"])
            self.assertFalse(row["ready_to_sell"])


if __name__ == "__main__":
    unittest.main()
