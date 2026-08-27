from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any

from mk1_behavioral_runner import find_fixture_set, sha256_json, sha256_text


ARTIFACTS = {
    "content_clear_rewrite": "mk1/candidates/f2/content_clear_rewrite/artifact.json",
    "software_code_review": "mk1/candidates/f2/software_code_review/artifact.json",
    "research_technical_decision": "mk1/candidates/f2/research_technical_decision/artifact.json",
}
PLACEHOLDER = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


def load(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_prompt(prompt_body: str, variables: dict[str, Any]) -> str:
    """Render only supplied fixture variables.

    Missing variables deliberately remain literal placeholders. That is part of
    the frozen experiment: missing-input fixtures must exercise the prompt's
    own intake/fallback behavior rather than a post-hoc sentinel.
    """
    rendered = prompt_body
    for name, value in variables.items():
        if isinstance(value, (dict, list)):
            replacement = json.dumps(value, ensure_ascii=False, sort_keys=True)
        else:
            replacement = str(value)
        rendered = rendered.replace("{" + str(name) + "}", replacement)
    return rendered


def safe_name(value: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", value.casefold()).strip("-")


def build_case_text(artifact: dict, fixture_set: dict, fixture: dict, rendered: str, ordinal: int) -> str:
    machine = fixture.get("expected", {}).get("machine_assertions", [])
    human = fixture.get("expected", {}).get("human_checks", [])
    return "\n".join([
        "PROMPT QUARRY — MK1 F4 CHATGPT PLUS OBSERVATION",
        "",
        f"ARTIFACT       : {artifact['id']} v{artifact['version']}",
        f"FIXTURE        : {fixture['fixture_id']}",
        f"CLASS          : {fixture.get('class')}",
        f"SEVERITY       : {fixture.get('severity', 'normal')}",
        f"CASE           : {ordinal:02d}",
        f"PROMPT SHA-256 : {sha256_text(rendered)}",
        "",
        "EXECUTION RULES",
        "- Use a NEW, clean ChatGPT Plus conversation for this case.",
        "- Keep the same visible ChatGPT configuration/model label for the whole wave.",
        "- Paste ONLY the text inside BEGIN FROZEN PROMPT / END FROZEN PROMPT.",
        "- Copy the FULL answer exactly; do not rewrite or improve it.",
        "- Do not reveal expected checks to the evaluated chat.",
        "",
        "BEGIN FROZEN PROMPT",
        rendered.rstrip(),
        "END FROZEN PROMPT",
        "",
        "AFTER EXECUTION — EVIDENCE FIELDS",
        "visible_chatgpt_label =",
        "observed_at =",
        "source_reference =",
        "full_output = <store separately in the response file>",
        "",
        "REVIEW CONTRACT — DO NOT SHOW TO THE EVALUATED CHAT",
        "Machine assertions:",
        json.dumps(machine, ensure_ascii=False, indent=2),
        "Human checks:",
        json.dumps(human, ensure_ascii=False, indent=2),
        "",
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize frozen ChatGPT Plus F4 certification packets for all foundational MK1 prompts.")
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--output", default="mk1/manual/f4/chatgpt-plus")
    args = parser.parse_args()

    fixture_document = load(args.fixtures)
    out = Path(args.output)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    wave_artifacts: list[dict] = []
    total_cases = 0
    index_lines = [
        "PROMPT QUARRY — MK1 F4 CHATGPT PLUS CERTIFICATION WAVE",
        "",
        "This directory is a frozen manual-observed execution packet.",
        "Execute every case in a fresh ChatGPT Plus conversation.",
        "Do not use the current Prompt Quarry project conversation as evidence.",
        "",
    ]

    for slug, artifact_path in ARTIFACTS.items():
        artifact = load(artifact_path)
        fixture_set_id = f"pq_mk1_fs_{slug}_v1"
        fixture_set = find_fixture_set(fixture_document, fixture_set_id)
        if artifact.get("state") != "VALID":
            raise SystemExit(f"{slug}: F4 Plus wave requires VALID artifact")
        if fixture_set.get("artifact_id") != artifact.get("id") or fixture_set.get("artifact_version") != artifact.get("version"):
            raise SystemExit(f"{slug}: artifact/fixture identity mismatch")

        artifact_dir = out / slug
        cases_dir = artifact_dir / "cases"
        responses_dir = artifact_dir / "responses"
        cases_dir.mkdir(parents=True, exist_ok=True)
        responses_dir.mkdir(parents=True, exist_ok=True)
        case_manifest: list[dict] = []

        for ordinal, fixture in enumerate(fixture_set.get("cases", []), start=1):
            fixture_id = fixture["fixture_id"]
            variables = (fixture.get("input") or {}).get("variables") or {}
            rendered = render_prompt(artifact["prompt_body"], variables)
            prompt_sha = sha256_text(rendered)
            filename = f"{ordinal:02d}-{safe_name(fixture_id)}.txt"
            (cases_dir / filename).write_text(
                build_case_text(artifact, fixture_set, fixture, rendered, ordinal),
                encoding="utf-8",
            )
            response_template = {
                "fixture_id": fixture_id,
                "visible_chatgpt_label": None,
                "observed_at": None,
                "source_reference": None,
                "rendered_prompt_sha256": prompt_sha,
                "output": None,
            }
            write_json(responses_dir / f"{fixture_id}.response.json", response_template)
            case_manifest.append({
                "ordinal": ordinal,
                "fixture_id": fixture_id,
                "class": fixture.get("class"),
                "severity": fixture.get("severity", "normal"),
                "case_file": f"cases/{filename}",
                "response_file": f"responses/{fixture_id}.response.json",
                "rendered_prompt_sha256": prompt_sha,
            })

        artifact_manifest = {
            "schema": "mk1-plus-f4-manual-wave-v1",
            "artifact_slug": slug,
            "artifact_id": artifact["id"],
            "artifact_version": artifact["version"],
            "artifact_prompt_fingerprint": sha256_text(artifact["prompt_body"]),
            "fixture_set_id": fixture_set["fixture_set_id"],
            "fixture_set_version": fixture_set.get("version", fixture_document.get("version", "1")),
            "fixture_set_fingerprint": sha256_json(fixture_set),
            "case_count": len(case_manifest),
            "blocking_case_count": sum(1 for row in fixture_set.get("cases", []) if row.get("severity", "normal") == "blocking"),
            "cases": case_manifest,
            "execution_mode": "manual-observed",
            "runtime_policy": "Use one exact visible ChatGPT Plus configuration label for the complete execution. Do not infer a hidden backend model id.",
        }
        write_json(artifact_dir / "manifest.json", artifact_manifest)
        (artifact_dir / "INDEX.txt").write_text(
            "\n".join([
                f"MK1 F4 CHATGPT PLUS — {artifact['title']}",
                "",
                f"Artifact: {artifact['id']} v{artifact['version']}",
                f"Fixture set: {fixture_set['fixture_set_id']}",
                f"Cases: {len(case_manifest)} (all blocking: {artifact_manifest['blocking_case_count']})",
                "",
                "Run cases in numeric order. Each case must use a fresh ChatGPT conversation.",
                "Store the full answer in the matching responses/*.response.json file.",
                "Do not edit the frozen case prompt or its SHA-256.",
                "",
            ]),
            encoding="utf-8",
        )
        wave_artifacts.append({
            "slug": slug,
            "artifact_id": artifact["id"],
            "manifest": f"{slug}/manifest.json",
            "index": f"{slug}/INDEX.txt",
            "cases": len(case_manifest),
        })
        total_cases += len(case_manifest)
        index_lines.append(f"- {slug}: {len(case_manifest)} cases → {slug}/INDEX.txt")

    wave = {
        "schema": "mk1-plus-f4-wave-manifest-v1",
        "mk_stage": "MK1",
        "phase": "F4",
        "execution_mode": "manual-observed",
        "target_product": "ChatGPT Plus",
        "artifact_count": len(wave_artifacts),
        "case_count": total_cases,
        "blocking_case_count": total_cases,
        "artifacts": wave_artifacts,
        "state_policy": "Packet generation does not promote state. Only completed manual observations plus human review may produce BEHAVIORAL_PASS receipts and TESTED artifacts.",
    }
    write_json(out / "manifest.json", wave)
    index_lines += [
        "",
        f"TOTAL: {len(wave_artifacts)} artifacts / {total_cases} blocking observations.",
        "",
        "A generated packet is not evidence and does not change any artifact state.",
    ]
    (out / "INDEX.txt").write_text("\n".join(index_lines), encoding="utf-8")
    print(json.dumps({"status": "PLUS_F4_WAVE_READY", "artifacts": len(wave_artifacts), "cases": total_cases, "output": out.as_posix()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
