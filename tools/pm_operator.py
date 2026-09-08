#!/usr/bin/env python3
"""Prompt Machine one-command operator entrypoint.

Default behavior intentionally has no provider/model/commerce side effects.
It fetches the configured remote branch, creates a detached temporary worktree,
runs release checks there, prints a compact status, persists an audit receipt,
and removes the temporary worktree. The user's active working tree is never
stashed, reset, pulled, or modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "feat/workflow-kits-product-model-20260902"
RC_NAME = "prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip"
EXPECTED_RC_BYTES = 19161
EXPECTED_RC_SHA256 = "1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88"
EXPECTED_WORKFLOW_BYTES = 25295
EXPECTED_WORKFLOW_SHA256 = "6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977"


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
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=str(cwd),
        text=True,
        capture_output=True,
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


def operator_data_root() -> Path:
    xdg = os.environ.get("XDG_DATA_HOME", "").strip()
    base = Path(xdg).expanduser() if xdg else Path.home() / ".local" / "share"
    return base / "prompt-machine" / "operator"


def new_receipt_dir(head: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = operator_data_root() / f"{stamp}-{head[:12]}"
    suffix = 0
    candidate = target
    while candidate.exists():
        suffix += 1
        candidate = Path(f"{target}-{suffix}")
    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


def sha256_file(path: Path) -> str:
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
            "expected_workflow_bytes": EXPECTED_WORKFLOW_BYTES,
            "expected_workflow_sha256": EXPECTED_WORKFLOW_SHA256,
        }
        if not archive_observation["identity_pass"]:
            results.append(
                CheckResult(
                    name="release_archive_identity",
                    ok=False,
                    returncode=2,
                    stdout=json.dumps(archive_observation, sort_keys=True),
                    stderr="release candidate identity differs from frozen licensed RC2 G12/G13 receipt",
                )
            )

    return results, archive_observation


def write_receipt(
    details: Path,
    *,
    head: str,
    remote: str,
    branch: str,
    results: list[CheckResult],
    archive: dict[str, object],
) -> Path:
    failed = [item for item in results if not item.ok]
    receipt = {
        "schema": "prompt-machine-operator-receipt-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "head": head,
        "remote": remote,
        "branch": branch,
        "active_working_tree_modified": False,
        "external_effects": 0,
        "release_candidate": "1.0.0-rc2",
        "customer_license_frozen": True,
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
    path = details / "operator-receipt.json"
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def compact_print(
    *,
    state: str,
    stage: str,
    head: str,
    next_action: str,
    receipt: Path | None = None,
) -> None:
    print("PROMPT MACHINE OPERATOR")
    print(f"state: {state}")
    print(f"stage: {stage}")
    print(f"head: {head}")
    print("release_candidate: 1.0.0-rc2")
    print("external_effects: 0")
    if receipt is not None:
        print(f"receipt: {receipt}")
    print(f"next: {next_action}")


def isolated_release_check(root: Path, remote: str, branch: str) -> int:
    remote_ref = f"refs/remotes/{remote}/{branch}"
    refspec = f"+refs/heads/{branch}:{remote_ref}"
    fetch = run(["git", "fetch", "--quiet", remote, refspec], cwd=root)
    if fetch.returncode != 0:
        compact_print(
            state="BLOCKED",
            stage="REPOSITORY_SYNC",
            head="UNKNOWN",
            next_action=(fetch.stderr or fetch.stdout or "Repository fetch failed.").strip()[:500],
        )
        return 2

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

    details = new_receipt_dir(head)
    worktree_base = Path(tempfile.mkdtemp(prefix="prompt-machine-operator-worktree-"))
    worktree = worktree_base / "repo"

    add = run(["git", "worktree", "add", "--detach", str(worktree), head], cwd=root)
    if add.returncode != 0:
        compact_print(
            state="BLOCKED",
            stage="CLEAN_WORKTREE",
            head=head,
            receipt=details,
            next_action=(add.stderr or add.stdout or "Temporary worktree creation failed.").strip()[:500],
        )
        shutil.rmtree(worktree_base, ignore_errors=True)
        return 2

    try:
        results, archive = run_release_checks(worktree, details_dir=details)
        receipt = write_receipt(
            details,
            head=head,
            remote=remote,
            branch=branch,
            results=results,
            archive=archive,
        )
        failed = [item for item in results if not item.ok]

        if failed:
            detail = (failed[0].stderr or failed[0].stdout or "check failed").strip()[:500]
            compact_print(
                state="BLOCKED",
                stage=failed[0].name,
                head=head,
                receipt=receipt,
                next_action=detail,
            )
            return 2

        compact_print(
            state="ACTION_REQUIRED",
            stage="G14_EXTERNAL_BOUNDARY",
            head=head,
            receipt=receipt,
            next_action="Licensed RC2 offline checks pass. Provider-side G14 evidence requires the separately governed provider handoff.",
        )
        return 0
    finally:
        run(["git", "worktree", "remove", "--force", str(worktree)], cwd=root)
        shutil.rmtree(worktree_base, ignore_errors=True)


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
                next_action=(failed[0].stderr or failed[0].stdout or "check failed").strip()[:500],
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
        help="Run current release checks without provider/model/commerce side effects.",
    )
    release.add_argument("--remote", default=DEFAULT_REMOTE)
    release.add_argument("--branch", default=DEFAULT_BRANCH)
    release.add_argument(
        "--local",
        action="store_true",
        help="Run in the current checkout (intended for CI/smoke use).",
    )

    args = parser.parse_args()
    root = repo_root()

    if args.command == "release-check":
        if args.local:
            return local_release_check(root)
        return isolated_release_check(root, args.remote, args.branch)

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
