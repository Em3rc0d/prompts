#!/usr/bin/env python3
"""Build exact Starter canary runtime envelopes deterministically.

Runtime input contains exactly two semantic blocks in this order:
1. FROZEN_STARTER_WORKFLOW_SURFACE
2. UNTRUSTED_INSTANCE_DATA

Evaluation contracts and expected results are intentionally excluded.
This tool performs zero model/provider calls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = ROOT / "product" / "starter-collection-v1" / "evaluation"
PLAN_PATH = EVAL_ROOT / "STARTER_CANARY_PLAN_V1.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_block(text: str) -> str:
    # Repository text is UTF-8. Preserve all content except normalize the final
    # boundary so rendering is independent of whether a source file ends in LF.
    return text.rstrip("\n") + "\n"


def render(surface: str, instance: str) -> bytes:
    envelope = (
        "<<<FROZEN_STARTER_WORKFLOW_SURFACE>>>\n"
        + normalize_block(surface)
        + "<<<END_FROZEN_STARTER_WORKFLOW_SURFACE>>>\n\n"
        + "<<<UNTRUSTED_INSTANCE_DATA>>>\n"
        + normalize_block(instance)
        + "<<<END_UNTRUSTED_INSTANCE_DATA>>>\n"
    )
    return envelope.encode("utf-8")


def build(output_dir: Path) -> dict:
    plan = read_json(PLAN_PATH)
    assert plan["schema"] == "prompt-machine-starter-canary-plan-v1"
    assert plan["state"] == "PREPARED_DISARMED_ZERO_RUNTIME_CALLS"
    assert plan["runtime_protocol"]["input_components"] == [
        "FROZEN_STARTER_WORKFLOW_SURFACE",
        "UNTRUSTED_INSTANCE_DATA",
    ]
    assert plan["runtime_protocol"]["evaluation_contract_is_runtime_input"] is False
    assert plan["runtime_protocol"]["expected_state_is_runtime_input"] is False

    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []

    for planned in sorted(plan["cases"], key=lambda item: item["priority"]):
        case_path = ROOT / planned["spec_path"]
        evaluation_path = ROOT / planned["evaluation_path"]
        case = read_json(case_path)
        evaluation = read_json(evaluation_path)

        assert case["case_id"] == planned["case_id"]
        assert evaluation["case_id"] == planned["case_id"]
        assert case["runtime_executed"] is False
        assert case["evaluation_contract_is_runtime_input"] is False
        assert evaluation["evaluation_contract_is_runtime_input"] is False
        assert evaluation["expected_result_is_runtime_input"] is False
        assert planned["armed"] is False

        surface_path = ROOT / case["workflow_surface_path"]
        surface_bytes = surface_path.read_bytes()
        surface_text = surface_bytes.decode("utf-8")
        instance_text = case["instance_data_markdown"]
        instance_bytes = instance_text.encode("utf-8")
        envelope_bytes = render(surface_text, instance_text)

        # Fail if evaluation material accidentally becomes runtime material.
        eval_bytes = evaluation_path.read_bytes()
        assert eval_bytes not in envelope_bytes
        assert b'"expected"' not in envelope_bytes
        assert b'"blocking_dimensions"' not in envelope_bytes

        envelope_name = f"{case['case_id']}.runtime-envelope.txt"
        envelope_path = output_dir / envelope_name
        envelope_path.write_bytes(envelope_bytes)

        rows.append({
            "case_id": case["case_id"],
            "workflow_id": case["workflow_id"],
            "variant": case["variant"],
            "priority": planned["priority"],
            "armed": False,
            "workflow_surface_path": case["workflow_surface_path"],
            "case_path": planned["spec_path"],
            "evaluation_path": planned["evaluation_path"],
            "envelope_file": envelope_name,
            "workflow_surface_size_bytes": len(surface_bytes),
            "workflow_surface_sha256": sha256(surface_bytes),
            "instance_data_size_bytes": len(instance_bytes),
            "instance_data_sha256": sha256(instance_bytes),
            "runtime_envelope_size_bytes": len(envelope_bytes),
            "runtime_envelope_sha256": sha256(envelope_bytes),
            "evaluation_contract_is_runtime_input": False,
            "expected_result_is_runtime_input": False,
            "runtime_executed": False,
        })

    manifest = {
        "schema": "prompt-machine-starter-canary-envelope-manifest-v1",
        "version": "1.0.0",
        "rendering_protocol": "two-labeled-blocks-fixed-order-v1",
        "encoding": "UTF-8",
        "cases": rows,
        "truth": {
            "prepared_envelopes": len(rows),
            "armed_envelopes": 0,
            "runtime_executions": 0,
            "evaluation_contracts_in_runtime_input": 0,
            "expected_results_in_runtime_input": 0,
            "model_calls": 0,
            "provider_calls": 0,
            "ready_to_sell": False,
        },
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def directory_digest(output_dir: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in output_dir.iterdir() if p.is_file()):
        h.update(path.name.encode("utf-8"))
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="dist/starter-canary-envelopes-v1")
    parser.add_argument("--verify-reproducible", action="store_true")
    args = parser.parse_args()

    output = ROOT / args.output_dir
    if args.verify_reproducible:
        first = output / "first"
        second = output / "second"
        m1 = build(first)
        m2 = build(second)
        assert m1 == m2
        assert directory_digest(first) == directory_digest(second)
        final = output / "final"
        final.mkdir(parents=True, exist_ok=True)
        for source in first.iterdir():
            if source.is_file():
                (final / source.name).write_bytes(source.read_bytes())
        manifest = m1
    else:
        manifest = build(output)

    print("STARTER CANARY ENVELOPES V1: PASS")
    for row in manifest["cases"]:
        print(
            f"{row['case_id']} bytes={row['runtime_envelope_size_bytes']} "
            f"sha256={row['runtime_envelope_sha256']} armed=false"
        )
    print(f"prepared_envelopes={manifest['truth']['prepared_envelopes']}")
    print("runtime_executions=0")
    print("model_calls=0")
    print("provider_calls=0")
    print("ready_to_sell=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
