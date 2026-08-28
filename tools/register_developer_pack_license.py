from __future__ import annotations

import json
from pathlib import Path

MANIFEST = Path("product/developer-pack-v1/MANIFEST.draft.json")
LICENSE = Path("product/developer-pack-v1/LICENSE.md")
ARTIFACT_ID = "pq-devpack-license"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifacts = manifest["artifacts"]
    matches = [a for a in artifacts if a.get("artifact_id") == ARTIFACT_ID or a.get("path") == LICENSE.as_posix()]
    record = {
        "artifact_id": ARTIFACT_ID,
        "path": LICENSE.as_posix(),
        "artifact_type": "license",
        "authority": "prompt-quarry",
        "provenance_class": "product-authored",
        "maturity_state": "VALID",
        "claims": ["engineered", "valid"],
        "evidence_refs": [".ci/developer-pack-v1/latest.json"],
        "sha256": "sha256:" + "0" * 64,
        "distribution": {
            "include": True,
            "customer_visible": True,
            "redistributable": True,
            "notes": "Prompt Quarry proprietary use-and-adapt license; redistribution/resale rights are not granted to customers."
        }
    }
    if matches:
        index = artifacts.index(matches[0])
        artifacts[index] = record
        for extra in matches[1:]:
            artifacts.remove(extra)
    else:
        artifacts.append(record)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"LICENSE ASSET REGISTERED: {ARTIFACT_ID}")


if __name__ == "__main__":
    main()
