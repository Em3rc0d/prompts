from __future__ import annotations

import json
from pathlib import Path

from validate_product_manifest import validate

ROOT = Path("product/developer-pack-v1")
MANIFEST = ROOT / "MANIFEST.draft.json"

REQUIRED = [
    ROOT / "README.md",
    ROOT / "QUICKSTART.md",
    ROOT / "templates/general-structured-prompt.md",
    ROOT / "templates/software-code-review.md",
    ROOT / "templates/technical-research-decision.md",
    ROOT / "checklists/static-quality.md",
    ROOT / "checklists/release-readiness.md",
]

FORBIDDEN_CUSTOMER_TEXT = [
    "mk0/raw/",
    "mk0/harvester/",
    "mk0/golden-dataset/",
    ".ci/",
    ".github/",
    "private-research-internals",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    failures: list[str] = []

    for path in REQUIRED:
        if not path.is_file():
            failures.append(f"missing required pack asset: {path}")

    if MANIFEST.is_file():
        failures.extend(f"manifest: {error}" for error in validate(MANIFEST, Path(".")))
        manifest = json.loads(read(MANIFEST))
        included = {a["path"] for a in manifest["artifacts"] if a["distribution"]["include"]}
        for path in REQUIRED:
            if path.as_posix() not in included:
                failures.append(f"required asset not included in manifest: {path}")
    else:
        failures.append("manifest missing")

    customer_files = [p for p in REQUIRED if p.is_file()]
    for path in customer_files:
        text = read(path)
        for token in FORBIDDEN_CUSTOMER_TEXT:
            if token in text and token != "private-research-internals":
                failures.append(f"customer asset exposes internal path {token}: {path}")

    template_contracts = {
        ROOT / "templates/general-structured-prompt.md": ["## PURPOSE", "## CONTEXT", "## PROCESS", "## RULES", "## OUTPUT CONTRACT", "## QUALITY GATE", "## FALLBACK"],
        ROOT / "templates/software-code-review.md": ["## PURPOSE", "## CONTEXT", "## REVIEW PROCESS", "## RULES", "## OUTPUT CONTRACT", "## QUALITY GATE"],
        ROOT / "templates/technical-research-decision.md": ["## PURPOSE", "## DECISION CRITERIA", "## EVIDENCE BOUNDARY", "## PROCESS", "## OUTPUT CONTRACT", "## QUALITY GATE"],
    }
    for path, headings in template_contracts.items():
        if not path.is_file():
            continue
        text = read(path)
        for heading in headings:
            if heading not in text:
                failures.append(f"template missing contract section {heading}: {path}")

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

    if failures:
        raise AssertionError("DEVELOPER PACK V1: FAIL\n- " + "\n- ".join(failures))

    print("DEVELOPER PACK V1: PASS")
    print(f"required_assets={len(REQUIRED)}")


if __name__ == "__main__":
    main()
