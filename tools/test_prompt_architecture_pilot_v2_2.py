from __future__ import annotations

import unittest

from build_prompt_architecture_pilot_v2_2 import build_records


class PromptArchitecturePilotV22Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = {row["mode"]: row for row in build_records()}

    def test_nine_distinct_blueprints(self) -> None:
        self.assertEqual(len(self.records), 9)
        self.assertEqual(len({row["prompt_sha256"] for row in self.records.values()}), 9)

    def test_state_selection_no_longer_assumes_linear_strength(self) -> None:
        for row in self.records.values():
            body = row["prompt_body"]
            self.assertNotIn("Choose the weakest state", body)
            self.assertNotIn("mode-specific weakest state", body)
            self.assertIn("whose declared semantic condition is actually satisfied", body)
            self.assertIn("does not overstate execution, evidence, or completion", body)

    def test_generation_hold_keeps_tied_shortlist_but_no_winner(self) -> None:
        body = self.records["generation"]["prompt_body"]
        self.assertIn("Under HOLD, return the tied viable shortlist", body)
        self.assertIn("recommended winner to NONE", body)
        self.assertIn("Under NO_VALID_CANDIDATE, shortlist = NONE", body)

    def test_generated_simulation_transcript_is_not_user_performance_evidence(self) -> None:
        body = self.records["simulation"]["prompt_body"]
        self.assertIn("never evidence of the user's ability or performance", body)
        self.assertIn("unless actual user turns are supplied", body)

    def test_v21_high_findings_remain_closed(self) -> None:
        general = self.records["general"]["prompt_body"]
        audit = self.records["audit"]["prompt_body"]
        simulation = self.records["simulation"]["prompt_body"]
        self.assertIn("Not executed when BLOCKED or UNSUPPORTED", general)
        self.assertIn("BLOCKED — the minimum audit definition is absent", audit)
        self.assertIn("Simulation state: READY | IN_PROGRESS | COMPLETE | BLOCKED", simulation)

    def test_quality_boundaries_remain_fail_closed(self) -> None:
        for row in self.records.values():
            body = row["prompt_body"]
            self.assertIn("INSTRUCTION / DATA BOUNDARY", body)
            self.assertIn("HIGH-STAKES BINDING BOUNDARY", body)
            self.assertIn("PRODUCT EVIDENCE BOUNDARY", body)
            self.assertFalse(row["automatic_product_promotion"])
            self.assertFalse(row["behavioral_evidence"])
            self.assertFalse(row["ready_to_sell"])


if __name__ == "__main__":
    unittest.main()
