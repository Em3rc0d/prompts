from __future__ import annotations

import unittest

from build_prompt_architecture_pilot_v2 import MODE_BINDINGS, build_records


class PromptArchitecturePilotV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = build_records()
        self.by_mode = {row["mode"]: row for row in self.records}

    def test_nine_distinct_blueprints(self) -> None:
        self.assertEqual(len(self.records), 9)
        self.assertEqual(set(self.by_mode), set(MODE_BINDINGS))
        self.assertEqual(len({row["prompt_sha256"] for row in self.records}), 9)

    def test_required_quality_sections_exist(self) -> None:
        required = [
            "PURPOSE",
            "AUTHORITY",
            "INPUT CONTRACT",
            "INSTRUCTION / DATA BOUNDARY",
            "EVIDENCE AND UNCERTAINTY",
            "STATE POLICY",
            "PROCESS",
            "CONSTRAINTS",
            "OUTPUT CONTRACT",
            "VERIFICATION",
            "FALLBACK",
            "HIGH-STAKES BINDING BOUNDARY",
            "PRODUCT EVIDENCE BOUNDARY",
        ]
        for row in self.records:
            for heading in required:
                self.assertIn(heading, row["prompt_body"], f"{row['mode']} missing {heading}")

    def test_input_contract_distinguishes_required_conditional_optional(self) -> None:
        for row in self.records:
            body = row["prompt_body"]
            self.assertIn("Minimum required inputs:", body)
            self.assertIn("Conditionally required when material", body)
            self.assertIn("Optional context:", body)

    def test_every_mode_has_explicit_state_semantics(self) -> None:
        for mode, binding in MODE_BINDINGS.items():
            self.assertGreaterEqual(len(binding["states"]), 3, mode)
            body = self.by_mode[mode]["prompt_body"]
            self.assertIn("Choose the weakest state", body)
            for state_rule in binding["states"]:
                self.assertIn(state_rule, body)

    def test_generation_never_forces_winner(self) -> None:
        body = self.by_mode["generation"]["prompt_body"]
        self.assertIn("NO_VALID_CANDIDATE", body)
        self.assertIn("HOLD", body)
        self.assertIn("do not force a winner", body)
        self.assertIn("NONE when HOLD or NO_VALID_CANDIDATE", body)

    def test_writing_has_factual_blocker_and_placeholder_state(self) -> None:
        body = self.by_mode["writing"]["prompt_body"]
        self.assertIn("COMPLETE_WITH_PLACEHOLDERS", body)
        self.assertIn("placeholders may never be silently fabricated", body)
        self.assertIn("Not executed when BLOCKED", body)

    def test_simulation_has_declared_invocation_modes(self) -> None:
        body = self.by_mode["simulation"]["prompt_body"]
        self.assertIn("INTERACTIVE", body)
        self.assertIn("BATCH_DEBRIEF", body)
        self.assertIn("do not simulate the user's response", body)
        self.assertIn("IN_PROGRESS — valid only for INTERACTIVE", body)

    def test_learning_objective_met_requires_observable_assessment(self) -> None:
        body = self.by_mode["learning"]["prompt_body"]
        self.assertIn("OBJECTIVE_MET", body)
        self.assertIn("observable assessment evidence", body)
        self.assertIn("Self-declared understanding alone is insufficient", body)

    def test_optimization_diagnose_first_requires_baseline(self) -> None:
        body = self.by_mode["optimization"]["prompt_body"]
        self.assertIn("DIAGNOSE_FIRST", body)
        self.assertIn("baseline/metric evidence is insufficient", body)

    def test_checklist_pass_is_strict(self) -> None:
        body = self.by_mode["checklist"]["prompt_body"]
        self.assertIn("missing evidence never becomes PASS", body)
        self.assertIn("no blocking UNKNOWN/RISK remains", body)
        self.assertIn("PASS applies only to the inspected checklist scope", body)

    def test_high_stakes_binding_is_explicitly_separate(self) -> None:
        for row in self.records:
            body = row["prompt_body"]
            self.assertIn("A separate domain safety/authority binding", body)
            self.assertIn("legal, medical, financial", body)

    def test_no_maturity_claims(self) -> None:
        for row in self.records:
            self.assertEqual(row["state"], "STATIC_REVIEW_REQUIRED")
            self.assertFalse(row["automatic_product_promotion"])
            self.assertFalse(row["behavioral_evidence"])
            self.assertFalse(row["ready_to_sell"])


if __name__ == "__main__":
    unittest.main()
