#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

REQUIRED = [
    WEB / "package.json",
    WEB / "tsconfig.json",
    WEB / "next.config.ts",
    WEB / "app/layout.tsx",
    WEB / "app/page.tsx",
    WEB / "app/globals.css",
    WEB / "app/free/developer-starter-pack/page.tsx",
    WEB / "app/developer-pack/page.tsx",
    WEB / "app/license/page.tsx",
    WEB / "components/commerce-link.tsx",
    WEB / "components/funnel-tracker.tsx",
    WEB / ".env.example",
]

FORBIDDEN_MARKETING = [
    "battle-tested",
    "proven superior",
    "best-performing",
    "guaranteed to improve",
    "works with every model",
    "universally portable",
]


def fail(message: str) -> None:
    raise SystemExit(f"COMMERCIAL WEB V0: FAIL — {message}")


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    if missing:
        fail("missing required Next.js files: " + ", ".join(missing))

    source_files = list((WEB / "app").rglob("*.tsx")) + list((WEB / "components").rglob("*.tsx"))
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_files)
    lower = source.lower()

    required_copy = [
        "stop collecting random prompts",
        "developer starter pack",
        "developer pack v1",
        "ready",
        "valid",
        "use it. adapt it",
        "resell",
        "redistribut",
    ]
    for phrase in required_copy:
        if phrase not in lower:
            fail(f"required commercial boundary/copy missing: {phrase}")

    for phrase in FORBIDDEN_MARKETING:
        if phrase in lower:
            fail(f"unsupported marketing claim observed: {phrase}")

    commerce = (WEB / "components/commerce-link.tsx").read_text(encoding="utf-8")
    for key in ("NEXT_PUBLIC_FREE_PACK_URL", "NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL"):
        if key not in commerce:
            fail(f"public commerce environment key missing: {key}")

    tracker = (WEB / "components/funnel-tracker.tsx").read_text(encoding="utf-8")
    for token in ("NEXT_PUBLIC_ANALYTICS_MODE", "landing_view", "paid_product_viewed", "utm_source", "sessionStorage"):
        if token not in tracker:
            fail(f"analytics contract missing: {token}")

    if "lemonsqueezy.com" in lower or "gumroad.com" in lower:
        fail("checkout provider URL is hard-coded in customer-facing source")

    css = (WEB / "app/globals.css").read_text(encoding="utf-8")
    for breakpoint in ("@media(max-width:900px)", "@media(max-width:620px)"):
        if breakpoint not in css:
            fail(f"responsive gate missing: {breakpoint}")

    package = (WEB / "package.json").read_text(encoding="utf-8")
    if '"next": "16.3.3"' not in package:
        fail("Next.js Active LTS security release 16.3.3 is not pinned")

    print("COMMERCIAL WEB V0: PASS")
    print(f"required_files={len(REQUIRED)}")
    print("framework=Next.js 16.3.3 App Router")
    print("routes=/,/free/developer-starter-pack,/developer-pack,/license")
    print("analytics=minimal UTM/session bridge; no purchase/revenue inference")
    print("boundary=READY/VALID only; F4-F7 superiority/certification claims remain unasserted")


if __name__ == "__main__":
    main()
