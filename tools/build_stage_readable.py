from __future__ import annotations

import argparse
import json
from pathlib import Path

RULE = "=" * 88


def write_copy(source: Path, target: Path, label: str) -> None:
    body = source.read_text(encoding="utf-8")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "\n".join(
            [
                "PROMPT QUARRY — HUMAN READING COPY",
                RULE,
                f"STAGE / DOCUMENT     : {label}",
                f"SOURCE REPOSITORY FILE: {source.as_posix()}",
                "CONTENT ORIGIN       : REPOSITORY DOCUMENTATION / ARTIFACT",
                "",
                body.rstrip(),
                "",
            ]
        ),
        encoding="utf-8",
    )


def copy_mk1_candidate_prompts(out: Path) -> tuple[int, int]:
    root = Path("mk1/candidates")
    if not root.exists():
        return 0, 0

    prompt_count = 0
    receipt_count = 0

    for prompt in sorted(root.rglob("prompt.txt")):
        rel_dir = prompt.parent.relative_to(root)
        target = out / "stages" / "mk1" / "candidates" / rel_dir.with_suffix(".txt")
        write_copy(prompt, target, "MK1 ENGINEERED CANDIDATE — HUMAN PROMPT")
        prompt_count += 1

    for index in sorted(root.rglob("INDEX.txt")):
        rel = index.relative_to(root)
        target = out / "stages" / "mk1" / "candidates" / rel
        write_copy(index, target, "MK1 CANDIDATE INDEX")

    for receipt in sorted(root.rglob("*.critic.txt")):
        rel = receipt.relative_to(root)
        target = out / "stages" / "mk1" / "candidates" / rel
        write_copy(receipt, target, "MK1 F3 STATIC CRITIC RECEIPT")
        receipt_count += 1

    return prompt_count, receipt_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="readable")
    args = parser.parse_args()

    out = Path(args.output)
    if not out.exists():
        raise SystemExit("Readable layer must be built before stage materialization.")

    stage_counts: dict[str, int] = {}
    stage_sources = {
        "MK0": Path("mk0"),
        "MK1": Path("mk1"),
        "MK2": Path("mk2"),
    }

    for stage, root in stage_sources.items():
        count = 0
        if root.exists():
            for path in sorted(root.rglob("*.md")):
                rel = path.relative_to(root).with_suffix(".txt")
                write_copy(path, out / "stages" / stage.lower() / rel, stage)
                count += 1
        stage_counts[stage] = count

    if Path("docs/ROADMAP.md").exists():
        write_copy(Path("docs/ROADMAP.md"), out / "stages" / "ROADMAP.txt", "MK0 → MK1 → MK2 ROADMAP")
    if Path("docs/ARCHITECTURE.md").exists():
        write_copy(Path("docs/ARCHITECTURE.md"), out / "stages" / "ARCHITECTURE.txt", "CROSS-STAGE ARCHITECTURE")
    if Path("README.md").exists():
        write_copy(Path("README.md"), out / "stages" / "ROOT_OVERVIEW.txt", "REPOSITORY OVERVIEW")

    candidate_prompt_copies, candidate_receipt_copies = copy_mk1_candidate_prompts(out)

    manifest_path = out / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["stage_document_txt_copies"] = sum(stage_counts.values()) + 3
    manifest["stage_document_counts"] = stage_counts
    manifest["mk1_candidate_prompt_txt_copies"] = candidate_prompt_copies
    manifest["mk1_candidate_receipt_txt_copies"] = candidate_receipt_copies
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme_path = out / "README.txt"
    readme = readme_path.read_text(encoding="utf-8").rstrip()
    readme += (
        "\n\nSTAGE ARCHITECTURE\n"
        + "-" * 88
        + "\n"
        + "10. stages/ROOT_OVERVIEW.txt        -> repository and MK0/MK1/MK2 overview\n"
        + "11. stages/ROADMAP.txt              -> roadmap and stage gates\n"
        + "12. stages/ARCHITECTURE.txt         -> full cross-stage architecture\n"
        + "13. stages/mk0/                     -> Knowledge Quarry documentation\n"
        + "14. stages/mk1/                     -> Prompt Forge contracts, rubric and fixtures\n"
        + "15. stages/mk1/candidates/          -> human copies of current MK1 prompts and critic receipts\n"
        + "16. stages/mk2/                     -> future Prompt Engine boundary\n"
    )
    readme_path.write_text(readme + "\n", encoding="utf-8")

    index_path = out / "INDEX.txt"
    index = index_path.read_text(encoding="utf-8").rstrip()
    index += (
        "\n\nSTAGES\n"
        + "-" * 88
        + "\n"
        + f"MK0 documents: {stage_counts['MK0']}\n"
        + f"MK1 documents: {stage_counts['MK1']}\n"
        + f"MK1 candidate prompt copies: {candidate_prompt_copies}\n"
        + f"MK1 critic receipt copies: {candidate_receipt_copies}\n"
        + f"MK2 documents: {stage_counts['MK2']}\n"
        + "Start with stages/ROOT_OVERVIEW.txt or stages/ROADMAP.txt.\n"
        + "Current MK1 prompt candidates and receipts are under stages/mk1/candidates/.\n"
    )
    index_path.write_text(index + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "stage_document_counts": stage_counts,
                "mk1_candidate_prompt_txt_copies": candidate_prompt_copies,
                "mk1_candidate_receipt_txt_copies": candidate_receipt_copies,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
