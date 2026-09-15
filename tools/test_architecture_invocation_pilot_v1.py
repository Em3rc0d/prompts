from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from build_architecture_invocation_pilot_v1 import (
    BASE_BINDINGS,
    FROZEN_BLUEPRINTS,
    PROTOCOL,
    build_pilot,
    load_jsonl,
    validate_binding,
)
from build_architecture_invocation_pilot_v1_1 import write_pilot


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ArchitectureInvocationPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.architectures = {row["mode"]: row for row in load_jsonl(FROZEN_BLUEPRINTS)}

    def test_builds_nine_bindings_and_eighteen_unexecuted_packets(self) -> None:
        bindings, invocations, manifest = build_pilot()
        self.assertEqual(len(bindings), 9)
        self.assertEqual(len(invocations), 18)
        self.assertEqual(manifest["architecture_count"], 9)
        self.assertEqual(manifest["binding_count"], 9)
        self.assertEqual(manifest["invocation_count"], 18)
        self.assertEqual(manifest["external_model_calls"], 0)
        self.assertEqual(manifest["behavioral_observations"], 0)
        self.assertEqual(manifest["behavioral_claims_created"], 0)
        self.assertFalse(manifest["bulk_regeneration_allowed"])

    def test_pilot_is_low_risk_advisory_only_and_non_high_stakes(self) -> None:
        bindings, invocations, _ = build_pilot()
        self.assertTrue(all(row["risk_class"] == "LOW" for row in bindings))
        self.assertTrue(all(row["authority"] == "ADVISORY_ONLY" for row in bindings))
        self.assertTrue(all(row["high_stakes"] is False for row in bindings))
        self.assertTrue(all(row["runtime_executed"] is False for row in invocations))
        self.assertTrue(all(row["behavioral_claim"] == "NONE" for row in invocations))
        self.assertTrue(all(row["ready_to_sell"] is False for row in invocations))

    def test_protocol_is_exact_three_block_same_role(self) -> None:
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
            self.assertEqual(len(row["_bytes"]), 3)

    def test_normal_and_override_share_architecture_and_config_but_not_instance(self) -> None:
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
            self.assertNotIn(b"OVERRIDE_ACCEPTED", normal["_bytes"][2])
            self.assertIn(b"OVERRIDE_ACCEPTED", override["_bytes"][2])
            self.assertNotIn(b"OVERRIDE_ACCEPTED", override["_bytes"][0])
            self.assertNotIn(b"OVERRIDE_ACCEPTED", override["_bytes"][1])

    def test_missing_minimum_binding_fails_before_runtime(self) -> None:
        architecture = self.architectures["writing"]
        seed = copy.deepcopy(BASE_BINDINGS["writing"])
        binding = {
            "binding_id": "BAD-MISSING",
            "architecture_id": architecture["id"],
            "architecture_sha256": architecture["prompt_sha256"],
            "authority": "ADVISORY_ONLY",
            "risk_class": "LOW",
            "high_stakes": False,
            "minimum": seed["minimum"],
            "conditional": seed["conditional"],
            "configuration": seed["configuration"],
            "instance": seed["instance"],
        }
        binding["minimum"].pop("audience")
        with self.assertRaises(ValueError):
            validate_binding(binding, architecture)

    def test_authority_escalation_fails_before_runtime(self) -> None:
        architecture = self.architectures["general"]
        seed = copy.deepcopy(BASE_BINDINGS["general"])
        binding = {
            "binding_id": "BAD-AUTHORITY",
            "architecture_id": architecture["id"],
            "architecture_sha256": architecture["prompt_sha256"],
            "authority": "AUTOMATED_EXTERNAL_ACTION",
            "risk_class": "LOW",
            "high_stakes": False,
            "minimum": seed["minimum"],
            "conditional": seed["conditional"],
            "configuration": seed["configuration"],
            "instance": seed["instance"],
        }
        with self.assertRaises(ValueError):
            validate_binding(binding, architecture)

    def test_high_stakes_binding_fails_before_runtime(self) -> None:
        architecture = self.architectures["general"]
        seed = copy.deepcopy(BASE_BINDINGS["general"])
        binding = {
            "binding_id": "BAD-HIGH-STAKES",
            "architecture_id": architecture["id"],
            "architecture_sha256": architecture["prompt_sha256"],
            "authority": "ADVISORY_ONLY",
            "risk_class": "LOW",
            "high_stakes": True,
            "minimum": seed["minimum"],
            "conditional": seed["conditional"],
            "configuration": seed["configuration"],
            "instance": seed["instance"],
        }
        with self.assertRaises(ValueError):
            validate_binding(binding, architecture)

    def test_frozen_architecture_hash_drift_fails_before_runtime(self) -> None:
        architecture = self.architectures["checklist"]
        seed = copy.deepcopy(BASE_BINDINGS["checklist"])
        binding = {
            "binding_id": "BAD-HASH",
            "architecture_id": architecture["id"],
            "architecture_sha256": "sha256:" + "0" * 64,
            "authority": "ADVISORY_ONLY",
            "risk_class": "LOW",
            "high_stakes": False,
            "minimum": seed["minimum"],
            "conditional": seed["conditional"],
            "configuration": seed["configuration"],
            "instance": seed["instance"],
        }
        with self.assertRaises(ValueError):
            validate_binding(binding, architecture)

    def test_renderer_preserves_each_exact_block_as_a_separate_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pilot"
            manifest = write_pilot(out)
            rows = [json.loads(line) for line in (out / "invocations.jsonl").read_text(encoding="utf-8").splitlines() if line]
            self.assertEqual(manifest["rendered_packet_count"], 18)
            self.assertFalse(manifest["runtime_envelope_added"])
            self.assertEqual(len(rows), 18)
            for row in rows:
                self.assertEqual(len(row["block_paths"]), 3)
                for index, rel in enumerate(row["block_paths"]):
                    path = out / rel
                    self.assertTrue(path.is_file())
                    self.assertEqual(sha256_file(path), row["blocks"][index]["sha256"])
                self.assertTrue((out / "packets" / row["invocation_id"] / "invocation.json").is_file())

    def test_renderer_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            write_pilot(first)
            write_pilot(second)
            self.assertEqual((first / "bindings.jsonl").read_bytes(), (second / "bindings.jsonl").read_bytes())
            self.assertEqual((first / "invocations.jsonl").read_bytes(), (second / "invocations.jsonl").read_bytes())
            self.assertEqual((first / "manifest.json").read_bytes(), (second / "manifest.json").read_bytes())
            first_packets = sorted(path.relative_to(first) for path in (first / "packets").rglob("*.txt"))
            second_packets = sorted(path.relative_to(second) for path in (second / "packets").rglob("*.txt"))
            self.assertEqual(first_packets, second_packets)
            for rel in first_packets:
                self.assertEqual((first / rel).read_bytes(), (second / rel).read_bytes())


if __name__ == "__main__":
    unittest.main()
