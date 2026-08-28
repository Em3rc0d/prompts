from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from validate_product_manifest import validate

ROOT = Path("product/developer-pack-v1")
MANIFEST = ROOT / "MANIFEST.draft.json"
TASK_BRIEF_SCHEMA = Path("mk1/specs/TASK_BRIEF.schema.json")
REQUEST_SCHEMA = Path("mk1/specs/PROMPT_GENERATOR_REQUEST.schema.json")

REQUIRED = [
    ROOT / "README.md",
    ROOT / "QUICKSTART.md",
    ROOT / "methodology/architecture.md",
    ROOT / "methodology/evidence-states.md",
    ROOT / "methodology/evaluation.md",
    ROOT / "contracts/task-brief.example.json",
    ROOT / "contracts/prompt-request.example.json",
    ROOT / "templates/general-structured-prompt.md",
    ROOT / "templates/software-code-review.md",
    ROOT / "templates/technical-research-decision.md",
    ROOT / "examples/software-code-review/request.json",
    ROOT / "examples/software-code-review/task-brief.json",
    ROOT / "examples/software-code-review/prompt.md",
    ROOT / "examples/software-code-review/README.md",
    ROOT / "examples/technical-research-decision/request.json",
    ROOT / "examples/technical-research-decision/task-brief.json",
    ROOT / "examples/technical-research-decision/prompt.md",
    ROOT / "examples/technical-research-decision/README.md",
    ROOT / "checklists/static-quality.md",
    ROOT / "checklists/release-readiness.md",
]

FORBIDDEN_CUSTOMER_TEXT = [
    "mk0/raw/",
    "mk0/harvester/",
    "mk0/golden-dataset/",
    ".ci/",
    ".github/",
]

REQUEST_FIXTURES = [
    ROOT / "contracts/prompt-request.example.json",
    ROOT / "examples/software-code-review/request.json",
    ROOT / "examples/technical-research-decision/request.json",
]

TASK_BRIEF_FIXTURES = [
    ROOT / "contracts/task-brief.example.json",
    ROOT / "examples/software-code-review/task-brief.json",
    ROOT / "examples/technical-research-decision/task-brief.json",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_json_fixture(path: Path, schema_path: Path) -> list[str]:
    schema = json.loads(read(schema_path))
    instance = json.loads(read(path))
    validator = Draft202012Validator(schema)
    return [f"{path}: {error.message}" for error in validator.iter_errors(instance)]


def main() -> None:
    failures: list[str] = []

    for path in REQUIRED:
        if not path.is_file():
            failures.append(f"missing required pack asset: {path}")

    manifest = None
    if MANIFEST.is_file():
        failures.extend(f"manifest: {error}" for error in validate(MANIFEST, Path(".")))
        manifest = json.loads(read(MANIFEST))
        included = {a["path"] for a in manifest["artifacts"] if a["distribution"]["include"]}
        for path in REQUIRED:
            if path.as_posix() not in included:
                failures.append(f"required asset not included in manifest: {path}")
        if len(included) != len(REQUIRED):
            failures.append(f"manifest inclusion count must equal required draft surface: expected {len(REQUIRED)}, got {len(included)}")
    else:
        failures.append("manifest missing")

    if manifest:
        customer_files = [Path(a["path"]) for a in manifest["artifacts"] if a["distribution"]["include"] and a["distribution"]["customer_visible"]]
    else:
        customer_files = [p for p in REQUIRED if p.is_file()]

    for path in customer_files:
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".json"}:
            continue
        text = read(path)
        for token in FORBIDDEN_CUSTOMER_TEXT:
            if token in text:
                failures.append(f"customer asset exposes internal path {token}: {path}")

    template_contracts = {
        ROOT / "templates/general-structured-prompt.md": ["## PURPOSE", "## CONTEXT", "## PROCESS", "## RULES", "## OUTPUT CONTRACT", "## QUALITY GATE", "## FALLBACK"],
        ROOT / "templates/software-code-review.md": ["## PURPOSE", "## CONTEXT", "## REVIEW PROCESS", "## RULES", "## OUTPUT CONTRACT", "## QUALITY GATE"],
        ROOT / "templates/technical-research-decision.md": ["## PURPOSE", "## DECISION CRITERIA", "## EVIDENCE BOUNDARY", "## PROCESS", "## OUTPUT CONTRACT", "## QUALITY GATE"],
        ROOT / "examples/software-code-review/prompt.md": ["## PURPOSE", "## CONTEXT", "## INTAKE", "## REVIEW PROCESS", "## RULES", "## OUTPUT CONTRACT", "## QUALITY GATE", "## FALLBACK"],
        ROOT / "examples/technical-research-decision/prompt.md": ["## PURPOSE", "## CONTEXT", "## INTAKE", "## PROCESS", "## RULES", "## OUTPUT CONTRACT", "## QUALITY GATE", "## FALLBACK"],
    }
    for path, headings in template_contracts.items():
        if not path.is_file():
            continue
        text = read(path)
        for heading in headings:
            if heading not in text:
                failures.append(f"prompt asset missing contract section {heading}: {path}")

    for fixture in REQUEST_FIXTURES:
        if fixture.is_file():
            failures.extend(validate_json_fixture(fixture, REQUEST_SCHEMA))
    for fixture in TASK_BRIEF_FIXTURES:
        if fixture.is_file():
            failures.extend(validate_json_fixture(fixture, TASK_BRIEF_SCHEMA))

    quickstart = read(ROOT / "QUICKSTART.md") if (ROOT / "QUICKSTART.md").is_file() else ""
    for relative in [
        "templates/software-code-review.md",
        "templates/technical-research-decision.md",
        "templates/general-structured-prompt.md",
        "checklists/static-quality.md",
    ]:
        if relative not in quickstart:
            failures.append(f"quickstart missing referenced customer path: {relative}")
        if not (ROOT / relative).is_file():
            failures.append(f"quickstart references missing asset: {relative}")

    for example_root in [ROOT / "examples/software-code-review", ROOT / "examples/technical-research-decision"]:
        readme = example_root / "README.md"
        if readme.is_file():
            text = read(readme)
            for required_phrase in ["## Architecture choice", "## Static quality result", "## Maturity", "## Claim boundary"]:
                if required_phrase not in text:
                    failures.append(f"example walkthrough missing {required_phrase}: {readme}")

    if failures:
        raise AssertionError("DEVELOPER PACK V1: FAIL\n- " + "\n- ".join(failures))

    print("DEVELOPER PACK V1: PASS")
    print(f"required_assets={len(REQUIRED)}")
    print(f"validated_request_fixtures={len(REQUEST_FIXTURES)}")
    print(f"validated_task_brief_fixtures={len(TASK_BRIEF_FIXTURES)}")


if __name__ == "__main__":
    main()
