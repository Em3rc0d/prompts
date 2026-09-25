from __future__ import annotations

import unittest

from execute_architecture_canary_openai_v1 import (
    CAMPAIGN_ID,
    INVOCATION_ID,
    PROTOCOL,
    load_packet,
    plan_manifest,
)


class ArchitectureCanaryOpenAITests(unittest.TestCase):
    def test_plan_is_exactly_one_low_risk_unexecuted_call(self) -> None:
        invocation, payloads, freeze = load_packet()
        plan = plan_manifest(invocation, payloads)
        self.assertEqual(plan["campaign_id"], CAMPAIGN_ID)
        self.assertEqual(plan["invocation_id"], INVOCATION_ID)
        self.assertEqual(plan["mode"], "checklist")
        self.assertEqual(plan["variant"], "NORMAL")
        self.assertEqual(plan["risk_class"], "LOW")
        self.assertEqual(plan["authority"], "ADVISORY_ONLY")
        self.assertEqual(plan["protocol"], PROTOCOL)
        self.assertEqual(plan["expected_state_set"], ["PASS"])
        self.assertEqual(plan["selected_runtime_calls"], 1)
        self.assertEqual(plan["provider_calls_made"], 0)
        self.assertEqual(plan["behavioral_observations"], 0)
        self.assertEqual(plan["receipts_created"], 0)
        self.assertEqual(plan["promotion_claim"], "NONE")
        self.assertEqual(plan["state"], "CANARY_PREPARED_NOT_EXECUTED")
        self.assertEqual(freeze["next_gate"]["canary"], INVOCATION_ID)
        self.assertEqual(freeze["next_gate"]["maximum_runtime_calls_before_review"], 1)

    def test_exact_three_blocks_and_hashes_match_frozen_packet(self) -> None:
        invocation, payloads, _ = load_packet()
        self.assertEqual(len(payloads), 3)
        self.assertEqual([x["kind"] for x in invocation["blocks"]], [
            "FROZEN_ARCHITECTURE",
            "AUTHORIZED_CONFIGURATION",
            "UNTRUSTED_INSTANCE_DATA",
        ])
        self.assertEqual(invocation["protocol"], PROTOCOL)
        self.assertEqual(invocation["role"], "user")
        self.assertEqual(invocation["evaluation_contract"]["expected_state_set"], ["PASS"])
        self.assertFalse(invocation["evaluation_contract"]["evaluation_metadata_is_runtime_input"])
        self.assertTrue(all(b"expected_state_set" not in x for x in payloads))
        self.assertTrue(all(b"cross_cutting_assertions" not in x for x in payloads))
        self.assertTrue(all(b"OVERRIDE_ACCEPTED" not in x for x in payloads))

    def test_freeze_explicitly_forbids_automatic_execution(self) -> None:
        _, _, freeze = load_packet()
        gate = freeze["next_gate"]
        self.assertEqual(gate["execution"], "MANUAL_ARM_ONLY")
        self.assertFalse(gate["automatic_execution"])
        self.assertFalse(freeze["truth_boundary"]["behavioral_evidence"])
        self.assertEqual(freeze["truth_boundary"]["runtime_executions"], 0)
        self.assertEqual(freeze["truth_boundary"]["external_model_calls"], 0)


if __name__ == "__main__":
    unittest.main()
