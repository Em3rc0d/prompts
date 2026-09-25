#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "product" / "free-developer-starter-v1"
MANIFEST = PACK / "MANIFEST.release.json"
WEB_ROUTE = ROOT / "web" / "app" / "api" / "free-pack" / "v1" / "route.ts"
WEB_GENERATED = ROOT / "web" / "generated" / "free-developer-starter-v1.ts"
WEB_COMMERCE = ROOT / "web" / "components" / "commerce-link.tsx"

EXPECTED = [
    "LICENSE.md",
    "OFFER.md",
    "QUICKSTART.md",
    "README.md",
    "prompts/bug-diagnosis.md",
    "prompts/code-review.md",
    "prompts/technical-decision.md",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "battle-tested",
    "proven superior",
    "guaranteed to improve",
    "works with every model",
]


def fail(message: str) -> None:
    raise SystemExit(f"FREE PACK V1: FAIL — {message}")


def load_builder():
    path = ROOT / "tools" / "build_free_developer_starter_v1.py"
    spec = importlib.util.spec_from_file_location("free_pack_builder", path)
    if not spec or not spec.loader:
        fail("cannot load release builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not MANIFEST.is_file():
        fail("release manifest missing")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    paths = [asset["path"] for asset in manifest.get("assets", [])]
    if paths != EXPECTED:
        fail(f"payload mismatch: expected {EXPECTED}, got {paths}")

    for relative in EXPECTED:
        if not (PACK / relative).is_file():
            fail(f"missing customer asset: {relative}")

    source = "\n".join((PACK / p).read_text(encoding="utf-8") for p in EXPECTED).lower()
    for claim in FORBIDDEN_POSITIVE_CLAIMS:
        if claim in source:
            fail(f"unsupported positive claim observed: {claim}")

    if "does not imply" not in (PACK / "README.md").read_text(encoding="utf-8").lower():
        fail("README evidence boundary missing")
    if "no resale or redistribution" not in (PACK / "LICENSE.md").read_text(encoding="utf-8").lower():
        fail("license resale/redistribution boundary missing")

    builder = load_builder()
    builder.load_and_verify()

    for required in (WEB_ROUTE, WEB_GENERATED, WEB_COMMERCE):
        if not required.is_file():
            fail(f"web distribution component missing: {required.relative_to(ROOT)}")

    route = WEB_ROUTE.read_text(encoding="utf-8")
    generated = WEB_GENERATED.read_text(encoding="utf-8")
    commerce = WEB_COMMERCE.read_text(encoding="utf-8")
    expected_hash = manifest["archive"]["archive_sha256"].removeprefix("sha256:")

    if expected_hash not in generated:
        fail("web snapshot archive hash is not bound to release manifest")
    if "FREE_PACK_ARCHIVE_SHA256" not in route or "buildStoredZip" not in route:
        fail("download route does not verify/build deterministic artifact")
    if '"/api/free-pack/v1"' not in commerce:
        fail("Free CTA fallback is not wired to deterministic download route")

    print("FREE PACK V1: PASS")
    print("included_assets=7")
    print(f"archive_sha256={manifest['archive']['archive_sha256']}")
    print("delivery=Next.js /api/free-pack/v1 fallback")
    print("boundary=free artifact release does not establish F4-F7 evidence")


if __name__ == "__main__":
    main()
