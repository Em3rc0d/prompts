from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sync(manifest_path: Path, repo_root: Path) -> tuple[dict, list[str]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    changes: list[str] = []

    for artifact in manifest.get("artifacts", []):
        if not artifact.get("distribution", {}).get("include"):
            continue
        path = repo_root / artifact["path"]
        if not path.is_file():
            raise FileNotFoundError(f"included artifact missing: {artifact['path']}")
        observed = sha256(path)
        if artifact.get("sha256") != observed:
            artifact["sha256"] = observed
            changes.append(artifact["path"])

    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest, changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronize SHA-256 values for included Prompt Quarry product artifacts")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()

    manifest, changes = sync(args.manifest, args.repo_root)
    print(json.dumps({
        "product_id": manifest.get("product_id"),
        "version": manifest.get("version"),
        "included_artifacts": sum(1 for a in manifest.get("artifacts", []) if a.get("distribution", {}).get("include")),
        "hashes_updated": len(changes),
        "updated_paths": changes,
    }, indent=2))


if __name__ == "__main__":
    main()
