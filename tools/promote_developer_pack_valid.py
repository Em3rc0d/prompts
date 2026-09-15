from __future__ import annotations

import json
from pathlib import Path

MANIFEST = Path("product/developer-pack-v1/MANIFEST.draft.json")
STATIC_RECEIPT = ".ci/developer-pack-v1/latest.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    changed = 0

    # Product release readiness is deliberately independent from artifact maturity.
    if manifest.get("release_status") != "DRAFT":
        raise SystemExit("Refusing static promotion: product release_status must remain DRAFT")

    for artifact in manifest.get("artifacts", []):
        if not artifact.get("distribution", {}).get("include"):
            continue
        state = artifact.get("maturity_state")
        if state == "DRAFT":
            artifact["maturity_state"] = "VALID"
            claims = artifact.setdefault("claims", [])
            if "valid" not in claims:
                claims.append("valid")
            refs = artifact.setdefault("evidence_refs", [])
            if STATIC_RECEIPT not in refs:
                refs.append(STATIC_RECEIPT)
            changed += 1
        elif state == "VALID":
            claims = artifact.setdefault("claims", [])
            if "valid" not in claims:
                claims.append("valid")
            refs = artifact.setdefault("evidence_refs", [])
            if STATIC_RECEIPT not in refs:
                refs.append(STATIC_RECEIPT)
        else:
            raise SystemExit(
                f"Refusing promotion for {artifact.get('artifact_id')}: unexpected maturity {state!r}"
            )

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PROMOTION OK changed={changed} release_status={manifest['release_status']}")
    print("BOUNDARY: VALID is static acceptance only; F4-F7 states are untouched.")


if __name__ == "__main__":
    main()
