from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if expect_success and completed.returncode != 0:
        raise AssertionError(f"command failed: {args}\nstdout={completed.stdout}\nstderr={completed.stderr}")
    if not expect_success and completed.returncode == 0:
        raise AssertionError(f"command unexpectedly succeeded: {args}")
    return completed


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def populate_responses(artifact_dir: Path, label: str = "Instant") -> None:
    manifest = load(artifact_dir / "manifest.json")
    for idx, case in enumerate(manifest["cases"], start=1):
        response_path = artifact_dir / case["response_file"]
        response = load(response_path)
        response.update({
            "visible_chatgpt_label": label,
            "observed_at": f"2026-08-27T03:{idx:02d}:00Z",
            "source_reference": f"manual-test://conversation/{case['fixture_id']}",
            "output": f"Observed output for {case['fixture_id']} with enough text to characterize collection.",
        })
        write(response_path, response)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="mk1-plus-lane-") as temp:
        temp_path = Path(temp)
        wave = temp_path / "wave"
        run("tools/mk1_build_plus_f4_wave.py", "--output", str(wave))
        wave_manifest = load(wave / "manifest.json")
        assert wave_manifest["artifact_count"] == 3
        assert wave_manifest["case_count"] == 30
        assert wave_manifest["blocking_case_count"] == 30
        assert wave_manifest["execution_mode"] == "manual-observed"

        rewrite = wave / "content_clear_rewrite"
        rewrite_manifest = load(rewrite / "manifest.json")
        assert rewrite_manifest["case_count"] == 10
        assert all(row["rendered_prompt_sha256"].startswith("sha256:") for row in rewrite_manifest["cases"])
        populate_responses(rewrite)

        collected = temp_path / "collected"
        run(
            "tools/mk1_collect_plus_f4_wave.py",
            "--wave-dir", str(rewrite),
            "--execution-id", "test-plus-f4-rewrite-001",
            "--output-dir", str(collected),
        )
        execution = load(collected / "execution.unreviewed.json")
        assert execution["mode"] == "manual-observed"
        assert execution["runtime"]["provider"] == "openai-chatgpt"
        assert execution["runtime"]["model"] == "Instant"
        assert execution["runtime"]["family"] == "chatgpt-plus"
        assert execution["runtime"]["identity_evidence_ref"].startswith(str(collected / "runtime-evidence-manifest.json"))
        assert len(execution["responses"]) == 10
        assert len(list((collected / "raw").glob("*.json"))) == 10
        evidence_manifest = load(collected / "runtime-evidence-manifest.json")
        assert len(evidence_manifest["observations"]) == 10
        assert evidence_manifest["manifest_sha256"].startswith("sha256:")

        # A single execution may not silently mix visible ChatGPT configurations.
        mixed_wave = temp_path / "mixed-wave"
        run("tools/mk1_build_plus_f4_wave.py", "--output", str(mixed_wave))
        mixed_rewrite = mixed_wave / "content_clear_rewrite"
        populate_responses(mixed_rewrite)
        mixed_manifest = load(mixed_rewrite / "manifest.json")
        first_path = mixed_rewrite / mixed_manifest["cases"][0]["response_file"]
        first = load(first_path)
        first["visible_chatgpt_label"] = "Thinking"
        write(first_path, first)
        run(
            "tools/mk1_collect_plus_f4_wave.py",
            "--wave-dir", str(mixed_rewrite),
            "--execution-id", "test-plus-f4-mixed-001",
            "--output-dir", str(temp_path / "mixed-collected"),
            expect_success=False,
        )

        # Prompt identity is frozen; a changed SHA invalidates collection.
        tamper_wave = temp_path / "tamper-wave"
        run("tools/mk1_build_plus_f4_wave.py", "--output", str(tamper_wave))
        tamper_rewrite = tamper_wave / "content_clear_rewrite"
        populate_responses(tamper_rewrite)
        tamper_manifest = load(tamper_rewrite / "manifest.json")
        tamper_path = tamper_rewrite / tamper_manifest["cases"][0]["response_file"]
        tamper = load(tamper_path)
        tamper["rendered_prompt_sha256"] = "sha256:" + "0" * 64
        write(tamper_path, tamper)
        run(
            "tools/mk1_collect_plus_f4_wave.py",
            "--wave-dir", str(tamper_rewrite),
            "--execution-id", "test-plus-f4-tamper-001",
            "--output-dir", str(temp_path / "tamper-collected"),
            expect_success=False,
        )

    print("MK1 ChatGPT Plus manual lane: PASS — 3 artifacts / 30 blocking packets; collector identity/evidence regressions characterized")


if __name__ == "__main__":
    main()
