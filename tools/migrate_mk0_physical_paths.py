#!/usr/bin/env python3
"""Rewrite active repository consumers to the canonical physical MK0 paths.

This migration intentionally excludes MK0 evidence payloads because historical
provenance may contain pre-migration repository paths that must remain immutable.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPES = [
    "README.md",
    "docs",
    "tools",
    ".github",
    "mk1",
    "mk2",
    "mk0/README.md",
    "mk0/MANIFEST.json",
]
EXCLUDED = {
    ".github/workflows/mk0-path-audit.yml",
    ".github/workflows/mk0-migration-preview.yml",
    "tools/migrate_mk0_physical_paths.py",
}

# Specific quarry stages must be rewritten before the generic quarry/ fallback.
REWRITES = [
    (re.compile(r"quarry/raw/"), "mk0/raw/"),
    (re.compile(r"quarry/normalized/"), "mk0/normalized/"),
    (re.compile(r"quarry/indexes/"), "mk0/indexes/"),
    (re.compile(r"quarry/analysis/"), "mk0/analysis/"),
    (re.compile(r"quarry/fixtures/"), "mk0/golden-dataset/"),
    (re.compile(r"quarry/promotions/"), "mk0/promotions/"),
    (re.compile(r"quarry/"), "mk0/"),
    (re.compile(r"(?<!mk0/)catalog/"), "mk0/catalog/"),
    (re.compile(r"(?<!mk0/)library/"), "mk0/library/"),
    (re.compile(r"(?<!mk0/)sources/"), "mk0/sources/"),
    (re.compile(r"(?<!mk0/)readable/"), "mk0/readable/"),
]


def tracked_files() -> list[Path]:
    cmd = ["git", "ls-files", "--", *SCOPES]
    result = subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)
    files: list[Path] = []
    for raw in result.stdout.splitlines():
        if not raw or raw in EXCLUDED:
            continue
        path = ROOT / raw
        if path.is_file():
            files.append(path)
    return files


def rewrite_text(text: str) -> str:
    for pattern, replacement in REWRITES:
        text = pattern.sub(replacement, text)
    return text


def main() -> int:
    changed: list[str] = []
    for path in tracked_files():
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = rewrite_text(original)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())

    print(f"changed_files={len(changed)}")
    for item in changed:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
