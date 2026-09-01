from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

PACK_ROOT = Path("product/developer-pack-v1")
MANIFEST_PATH = PACK_ROOT / "MANIFEST.draft.json"
TASK_BRIEF_SCHEMA = Path("mk1/specs/TASK_BRIEF.schema.json")
REQUEST_SCHEMA = Path("mk1/specs/PROMPT_GENERATOR_REQUEST.schema.json")


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    manifest = load_json(MANIFEST_PATH)
    included = [a for a in manifest["artifacts"] if a["distribution"]["include"]]
    failures: list[str] = []

    with tempfile.TemporaryDirectory(prefix="prompt-quarry-clean-room-") as temp:
        export_root = Path(temp) / "prompt-quarry-developer-pack-v1"
        export_root.mkdir(parents=True)

        for artifact in included:
            source = Path(artifact["path"])
            try:
                relative = source.relative_to(PACK_ROOT)
            except ValueError:
                failures.append(f"included artifact escapes package root: {source}")
                continue
            target = export_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if sha256(target) != artifact["sha256"]:
                failures.append(f"exported hash mismatch: {relative}")

        forbidden = ["mk0/", "mk1/", "tools/", ".ci/", ".github/"]
        for path in export_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".json"}:
                continue
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                if token in text:
                    failures.append(f"clean-room customer asset depends on internal path {token}: {path.relative_to(export_root)}")

        quickstart = export_root / "QUICKSTART.md"
        if not quickstart.is_file():
            failures.append("QUICKSTART.md missing from clean-room export")
        else:
            text = quickstart.read_text(encoding="utf-8")
            for relative in [
                "templates/software-code-review.md",
                "templates/technical-research-decision.md",
                "templates/general-structured-prompt.md",
                "checklists/static-quality.md",
            ]:
                if relative not in text:
                    failures.append(f"quickstart does not mention required path: {relative}")
                if not (export_root / relative).is_file():
                    failures.append(f"quickstart target absent from clean-room export: {relative}")

        request_schema = load_json(REQUEST_SCHEMA)
        brief_schema = load_json(TASK_BRIEF_SCHEMA)
        for path in export_root.rglob("*.json"):
            if path.name == "MANIFEST.draft.json":
                continue
            instance = load_json(path)
            if "request_id" in instance:
                errors = list(Draft202012Validator(request_schema).iter_errors(instance))
            elif "brief_id" in instance:
                errors = list(Draft202012Validator(brief_schema).iter_errors(instance))
            else:
                errors = []
            for error in errors:
                failures.append(f"clean-room contract invalid {path.relative_to(export_root)}: {error.message}")

        exported_files = sorted(p.relative_to(export_root).as_posix() for p in export_root.rglob("*") if p.is_file())
        expected_files = sorted(Path(a["path"]).relative_to(PACK_ROOT).as_posix() for a in included)
        if exported_files != expected_files:
            failures.append(f"clean-room inventory mismatch: expected={expected_files} observed={exported_files}")

    if failures:
        raise AssertionError("DEVELOPER PACK CLEAN ROOM: FAIL\n- " + "\n- ".join(failures))

    print("DEVELOPER PACK CLEAN ROOM: PASS")
    print(f"exported_artifacts={len(included)}")
    print("boundary=manifest-only export; no private repository paths required")


if __name__ == "__main__":
    main()
