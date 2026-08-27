from __future__ import annotations

import json
from pathlib import Path

BASE = Path("mk1/manual/f4/chatgpt-plus")
OUT = BASE / "batches"
BEGIN = "BEGIN FROZEN PROMPT"
END = "END FROZEN PROMPT"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def extract_frozen_prompt(text: str) -> str:
    if BEGIN not in text or END not in text:
        raise ValueError("case packet missing frozen prompt markers")
    return text.split(BEGIN, 1)[1].split(END, 1)[0].strip("\n")


def main() -> None:
    root = load(BASE / "manifest.json")
    OUT.mkdir(parents=True, exist_ok=True)

    global_offset = 0
    generated = []
    for artifact in root["artifacts"]:
        artifact_dir = BASE / artifact["slug"]
        manifest = load(BASE / artifact["manifest"])
        case_count = int(manifest["case_count"])
        start = global_offset + 1
        end = global_offset + case_count

        lines = [
            f"PROMPT QUARRY — MK1 F4 CHATGPT PLUS BATCH {start:02d}-{end:02d}",
            "",
            f"ARTIFACT: {manifest['artifact_id']} v{manifest['artifact_version']}",
            "EXECUTION MODE: manual-observed",
            "TARGET CONFIGURATION: keep the same visible ChatGPT configuration label for the whole wave (currently High).",
            "",
            "OPERATOR RULES",
            "- Each numbered case MUST run in its own NEW, clean ChatGPT conversation.",
            "- Paste only the text inside that case's BEGIN FROZEN PROMPT / END FROZEN PROMPT block.",
            "- Do not combine cases into one evaluated conversation.",
            "- Copy the full answer exactly; do not rewrite or improve it.",
            "- Do not show hidden review checks to the evaluated chat.",
            "- Return the outputs labeled with the global case number shown here.",
            "",
        ]

        for case in manifest["cases"]:
            local_ordinal = int(case["ordinal"])
            global_ordinal = global_offset + local_ordinal
            packet = (artifact_dir / case["case_file"]).read_text(encoding="utf-8")
            frozen = extract_frozen_prompt(packet)
            lines.extend([
                "=" * 80,
                f"GLOBAL CASE {global_ordinal:02d}",
                f"LOCAL CASE  {local_ordinal:02d}",
                f"FIXTURE     {case['fixture_id']}",
                f"CLASS       {case['class']}",
                f"SEVERITY    {case['severity']}",
                f"PROMPT SHA  {case['rendered_prompt_sha256']}",
                "=" * 80,
                "",
                BEGIN,
                frozen,
                END,
                "",
                f"RETURN AS: {global_ordinal:02d}: <full answer exactly as produced>",
                "",
            ])

        output = OUT / f"BATCH_{start:02d}_{end:02d}.txt"
        output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        generated.append(output.as_posix())
        global_offset = end

    index = [
        "PROMPT QUARRY — MK1 F4 CHATGPT PLUS BATCH INDEX",
        "",
        "Generated operator convenience layer only. Source case packets and their prompt SHA-256 values remain authoritative.",
        "Batching does not change the requirement that every case run in a fresh clean conversation.",
        "",
    ] + [f"- {path}" for path in generated]
    (OUT / "INDEX.txt").write_text("\n".join(index) + "\n", encoding="utf-8")

    print(json.dumps({"generated": generated, "count": len(generated)}, indent=2))


if __name__ == "__main__":
    main()
