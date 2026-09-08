#!/usr/bin/env python3
"""Prompt Machine one-command operator entrypoint.

Default behavior intentionally has no provider/model/commerce side effects.
It fetches the configured remote branch, creates a detached temporary worktree,
runs release checks there, prints a compact status, and removes the worktree.
The user's active working tree is never stashed, reset, pulled, or modified.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "feat/workflow-kits-product-model-20260902"
RC_NAME = "prompt-machine-starter-code-review-edition-v1.0.0-rc1.zip"
EXPECTED_RC_BYTES = 14667
EXPECTED_RC_SHA256 = "7ec282ea1766679f425fd5aad526d6382e6a3c5af2caab9ded07e55b9a773cde"


@dataclass
class CheckResult:
    name: str
    ok: bool
    returncode: int
    stdout: str
    stderr: str


def run(
    argv: list[str],
    *,
    cwd: Path,
    check: bool = False,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=str(cwd),
        text=True,
        capture_output=capture,
        check=False,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "command failed").strip()
        raise RuntimeError(f"{' '.join(argv)} failed: {detail[:1200]}")
    return result


def repo_root() -> Path:
    here = Path.cwd()
    result = run(["git", "rev-parse", "--show-toplevel"], cwd=here)
    if result.returncode != 0:
        raise RuntimeError("not inside a Git repository")
    return Path(result.stdout.strip()).resolve()


def sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def execute_check(name: str, argv: list[str], cwd: Path) -> CheckResult:
    result = run(argv, cwd=cwd)
    return CheckResult(
        name=name,
        ok=result.returncode == 0,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )


def existing_commands(root: Path, out_dir: Path) -> list[tuple[str, list[str]]]:
    commands: list[tuple[str, list[str]]] = []

    builder = root / "tools/build_starter_code_review_edition.py"
    validator = root / "tools/validate_starter_code_review_edition.py"
    if builder.is_file():
        commands.append(
            (
                "starter_code_review_build",
                [sys.executable, str(builder), "--out-dir", str(out_dir)],
            )
        )
    else:
        commands.append(("missing_builder", [sys.executable, "-c", "raise SystemExit(2)"]))

    archive = out_dir / RC_NAME
    if validator.is_file():
        commands.append(
            (
                "starter_code_review_pack_qa",
                [sys.executable, str(validator), "--archive", str(archive)],
            )
        )
    else:
        commands.append(("missing_validator", [sys.executable, "-c", "raise SystemExit(2)"]))

    offline_candidates = [
        ("commerce_contract", "tools/test_commerce_v0.py"),
        ("provider_custody_offline", "tools/test_provider_custody_verifier_v1.py"),
        ("starter_webhook_offline", "tools/test_starter_webhook_adapter_v1.py"),
        ("starter_code_review_g14_offline", "tools/test_starter_code_review_g14_v1.py"),
    ]
    for label, relative in offline_candidates:
        path = root / relative
        if path.is_file():
            commands.append((label, [sys.executable, str(path)]))

    return commands


def run_release_checks(root: Path, *, details_dir: Path) -> tuple[list[CheckResult], dict[str, object]]:
    build_dir = details_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    results: list[CheckResult] = []

    for name, argv in existing_commands(root, build_dir):
        result = execute_check(name, argv, root)
        results.append(result)
        (details_dir / f"{name}.stdout.txt").write_text(result.stdout, encoding="utf-8")
        (details_dir / f"{name}.stderr.txt").write_text(result.stderr, encoding="utf-8")
        if not result.ok:
            break

    archive = build_dir / RC_NAME
    archive_observation: dict[str, object] = {"observed": False}
    if archive.is_file():
        observed_bytes = archive.stat().st_size
        observed_sha256 = sha256_file(archive)
        archive_observation = {
            "observed": True,
            "name": archive.name,
            "bytes": observed_bytes,
            "sha256": observed_sha256,
            "identity_pass": (
                observed_bytes == EXPECTED_RC_BYTES
                and observed_sha256 == EXPECTED_RC_SHA256
            ),
        }
        if not archive_observation["identity_pass"]:
            results.append(
                CheckResult(
                    name="release_archive_identity",
                    ok=False,
                    returncode=2,
                    stdout=json.dumps(archive_observation, sort_keys=True),
                    stderr="release candidate identity differs from frozen G12/G13 receipt",
                )
            )

    return results, archive_observation


def compact_print(*, state: str, stage: str, head: str, next_action: str) -> None:
    print("PROMPT MACHINE OPERATOR")
    print(f"state: {state}")
    print(f"stage: {stage}")
    print(f"head: {head}")
    print("external_effects: 0")
    print(f"next: {next_action}")


def isolated_release_check(root: Path, remote: str, branch: str, keep: bool) -> int:
    fetch = run(["git", "fetch", "--quiet", remote, branch], cwd=root)
    if fetch.returncode != 0:
        compact_print(
            state="BLOCKED",
            stage="REPOSITORY_SYNC",
            head="UNKNOWN",
            next_action="Repository fetch failed; inspect operator receipt.",
        )
        return 2

    remote_ref = f"{remote}/{branch}"
    rev = run(["git", "rev-parse", remote_ref], cwd=root)
    if rev.returncode != 0:
        compact_print(
            state="BLOCKED",
            stage="REPOSITORY_SYNC",
            head="UNKNOWN",
            next_action=f"Remote ref {remote_ref} could not be resolved.",
        )
        return 2
    head = rev.stdout.strip()

    base = Path(tempfile.mkdtemp(prefix="prompt-machine-operator-"))
    worktree = base / "repo"
    details = base / "receipt"
    details.mkdir(parents=True, exist_ok=True)

    add = run(["git", "worktree", "add", "--detach", str(worktree), head], cwd=root)
    if add.returncode != 0:
        compact_print(
            state="BLOCKED",
            stage="CLEAN_WORKTREE",
            head=head,
            next_action="Temporary clean worktree could not be created.",
        )
        if not keep:
            shutil.rmtree(base, ignore_errors=True)
        return 2

    try:
        results, archive = run_release_checks(worktree, details_dir=details)
        failed = [item for item in results if not item.ok]
        receipt = {
            "schema": "prompt-machine-operator-receipt-v1",
            "head": head,
            "remote": remote,
            "branch": branch,
            "active_working_tree_modified": False,
            "external_effects": 0,
            "archive": archive,
            "checks": [
                {
                    "name": item.name,
                    "ok": item.ok,
                    "returncode": item.returncode,
                }
                for item in results
            ],
            "verdict": "PASS" if not failed else "BLOCKED",
        }
        (details / "operator-receipt.json").write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        if failed:
            compact_print(
                state="BLOCKED",
                stage=failed[0].name,
                head=head,
                next_action=f"Fix {failed[0].name}; detailed receipt is in {details}.",
            )
            if keep:
                print(f"details: {details}")
            return 2

        compact_print(
            state="ACTION_REQUIRED",
            stage="G14_EXTERNAL_BOUNDARY",
            head=head,
            next_action="Offline release checks pass. Provider-side G14 evidence still requires a separately authorized action.",
        )
        if keep:
            print(f"details: {details}")
        return 0
    finally:
        run(["git", "worktree", "remove", "--force", str(worktree)], cwd=root)
        if not keep:
            shutil.rmtree(base, ignore_errors=True)


def local_release_check(root: Path) -> int:
    head = run(["git", "rev-parse", "HEAD"], cwd=root, check=True).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="prompt-machine-local-check-") as tmp:
        details = Path(tmp)
        results, archive = run_release_checks(root, details_dir=details)
        failed = [item for item in results if not item.ok]
        if failed:
            compact_print(
                state="BLOCKED",
                stage=failed[0].name,
                head=head,
                next_action=f"Fix {failed[0].name}.",
            )
            return 2
        if not archive.get("identity_pass"):
            compact_print(
                state="BLOCKED",
                stage="release_archive_identity",
                head=head,
                next_action="Release archive identity mismatch.",
            )
            return 2
        compact_print(
            state="PASS",
            stage="OFFLINE_RELEASE_CHECKS",
            head=head,
            next_action="NONE",
        )
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Prompt Machine one-command operator")
    sub = parser.add_subparsers(dest="command", required=True)

    release = sub.add_parser(
        "release-check",
        help="Run the current release checks without provider/model/commerce side effects.",
    )
    release.add_argument("--remote", default=DEFAULT_REMOTE)
    release.add_argument("--branch", default=DEFAULT_BRANCH)
    release.add_argument(
        "--local",
        action="store_true",
        help="Run in the current checkout (intended for CI/smoke use).",
    )
    release.add_argument(
        "--keep-details",
        action="store_true",
        help="Keep the temporary receipt directory for debugging.",
    )

    args = parser.parse_args()
    root = repo_root()

    if args.command == "release-check":
        if args.local:
            return local_release_check(root)
        return isolated_release_check(root, args.remote, args.branch, args.keep_details)

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
