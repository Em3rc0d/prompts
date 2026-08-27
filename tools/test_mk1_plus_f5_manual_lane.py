from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)
    if expect_success and completed.returncode != 0:
        raise AssertionError(f"command failed: {args}\nstdout={completed.stdout}\nstderr={completed.stderr}")
    if not expect_success and completed.returncode == 0:
        raise AssertionError(f"command unexpectedly succeeded: {args}")
    return completed


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_tested_artifact(path: Path) -> dict:
    source = load(ROOT / "mk1/candidates/f2/content_clear_rewrite/artifact.json")
    source["state"] = "TESTED"
    source["claims"] = ["engineered", "tested"]
    source["evaluation"] = {
        "baseline_id": None,
        "fixture_set_id": "pq_mk1_fs_content_clear_rewrite_v1",
        "receipt_id": "pq_mk1_f4_receipt_test_only",
        "rubric_score": 100,
        "blocking_failures": [],
    }
    write(path, source)
    return source


def populate_operator_responses(wave: Path, label: str = "Instant", operator: str = "operator:test") -> None:
    manifest = load(wave / "manifest.json")
    counter = 0
    for case in manifest["cases"]:
        for side in ("A", "B"):
            counter += 1
            response_path = wave / case["sides"][side]["response_file"]
            response = load(response_path)
            response.update({
                "visible_chatgpt_label": label,
                "observed_at": f"2026-08-27T04:{counter // 60:02d}:{counter % 60:02d}Z",
                "source_reference": f"manual-test://{case['pair_key']}/{side}",
                "operator_ref": operator,
                "output": f"Observed blind side {side} output for {case['pair_key']} with sufficient preserved text.",
            })
            write(response_path, response)


def complete_review(packet_path: Path, reviewer_ref: str) -> None:
    packet = load(packet_path)
    packet["review"]["reviewer_ref"] = reviewer_ref
    packet["review"]["reviewed_at"] = "2026-08-27T05:00:00Z"
    for judgment in packet["review"]["pair_judgments"].values():
        for side in ("A", "B"):
            for label in list(judgment[side]):
                judgment[side][label] = {"status": "PASS", "note": "Test-only completed human evidence note."}
        judgment["preference"] = {"winner": "tie", "note": "Test-only neutral blind preference."}
    write(packet_path, packet)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="mk1-plus-f5-") as temp:
        temp_path = Path(temp)
        artifact_path = temp_path / "tested-artifact.json"
        make_tested_artifact(artifact_path)
        wave = temp_path / "wave"
        run("tools/mk1_build_plus_f5_wave.py", "--artifact", str(artifact_path), "--output", str(wave), "--repeats", "3")
        manifest = load(wave / "manifest.json")
        assert manifest["repeat_count"] == 3
        assert manifest["fixture_count"] == 10
        assert manifest["pair_count"] == 30
        assert manifest["observation_count"] == 60
        assert len(load(wave / "blind-key.private.json")["mapping"]) == 30
        populate_operator_responses(wave)

        collected = temp_path / "collected"
        run("tools/mk1_collect_plus_f5_wave.py", "--wave-dir", str(wave), "--execution-id", "test-plus-f5-001", "--output-dir", str(collected))
        observation = load(collected / "observation.json")
        assert observation["mode"] == "manual-observed"
        assert observation["runtime"]["provider"] == "openai-chatgpt"
        assert observation["runtime"]["model"] == "Instant"
        assert observation["runtime"]["family"] == "chatgpt-plus"
        assert observation["manual_operator_refs"] == ["operator:test"]
        assert observation["repeat_count"] == 3
        assert observation["pair_count"] == 30
        assert len(list((collected / "raw").glob("*.json"))) == 60
        review_packet = load(collected / "review-packet.json")
        assert len(review_packet["immutable"]["pairs"]) == 30
        assert review_packet["review"]["blinded"] is True

        # Same-person operator/reviewer is rejected for the manual blind lane.
        same_review = temp_path / "same-review.json"
        same_review.write_text((collected / "review-packet.json").read_text(encoding="utf-8"), encoding="utf-8")
        complete_review(same_review, "operator:test")
        run(
            "tools/mk1_finalize_plus_f5_review.py",
            "--observation", str(collected / "observation.json"),
            "--blind-key", str(collected / "blind-key.private.json"),
            "--review-packet", str(same_review),
            "--artifact", str(artifact_path),
            "--output", str(temp_path / "same-final.json"),
            expect_success=False,
        )

        independent_review = temp_path / "independent-review.json"
        independent_review.write_text((collected / "review-packet.json").read_text(encoding="utf-8"), encoding="utf-8")
        complete_review(independent_review, "reviewer:independent")
        run(
            "tools/mk1_finalize_plus_f5_review.py",
            "--observation", str(collected / "observation.json"),
            "--blind-key", str(collected / "blind-key.private.json"),
            "--review-packet", str(independent_review),
            "--artifact", str(artifact_path),
            "--output", str(temp_path / "finalized.json"),
        )
        finalized = load(temp_path / "finalized.json")
        assert finalized["mode"] == "manual-observed"
        assert finalized["review"]["reviewer_ref"] == "reviewer:independent"
        assert finalized["review"]["independent_from_operator"] is True
        assert finalized["manual_operator_refs"] == ["operator:test"]

        # Mixed visible ChatGPT labels invalidate one benchmark execution.
        mixed = temp_path / "mixed-wave"
        run("tools/mk1_build_plus_f5_wave.py", "--artifact", str(artifact_path), "--output", str(mixed), "--repeats", "3")
        populate_operator_responses(mixed)
        mixed_manifest = load(mixed / "manifest.json")
        first_case = mixed_manifest["cases"][0]
        first_response = mixed / first_case["sides"]["A"]["response_file"]
        row = load(first_response)
        row["visible_chatgpt_label"] = "Thinking"
        write(first_response, row)
        run("tools/mk1_collect_plus_f5_wave.py", "--wave-dir", str(mixed), "--execution-id", "test-plus-f5-mixed", "--output-dir", str(temp_path / "mixed-collected"), expect_success=False)

    print("MK1 ChatGPT Plus F5 manual lane: PASS — 3 repeats / 30 blind pairs / 60 observations; independent-review and runtime-label guards characterized")


if __name__ == "__main__":
    main()
