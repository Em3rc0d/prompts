#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

REQUIRED = [
    WEB / "index.html",
    WEB / "free/developer-starter-pack/index.html",
    WEB / "developer-pack/index.html",
    WEB / "license/index.html",
    WEB / "assets/styles.css",
    WEB / "assets/app.js",
    WEB / "config.js",
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
        fail("missing required files: " + ", ".join(missing))

    html = "\n".join(path.read_text(encoding="utf-8") for path in REQUIRED if path.suffix == ".html")
    lower = html.lower()

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

    config = (WEB / "config.js").read_text(encoding="utf-8")
    for key in ("freePackUrl", "developerPackCheckoutUrl", "analyticsMode"):
        if key not in config:
            fail(f"runtime configuration key missing: {key}")

    # Provider URLs must remain configuration, not page semantics.
    if "lemonsqueezy.com" in lower or "gumroad.com" in lower:
        fail("checkout provider URL is hard-coded in customer-facing HTML")

    styles = (WEB / "assets/styles.css").read_text(encoding="utf-8")
    if "@media(max-width:560px)" not in styles or "@media(max-width:880px)" not in styles:
        fail("responsive mobile/tablet gates missing")

    print("COMMERCIAL WEB V0: PASS")
    print(f"required_files={len(REQUIRED)}")
    print("routes=/,/free/developer-starter-pack/,/developer-pack/,/license/")
    print("boundary=READY/VALID only; F4-F7 superiority/certification claims remain unasserted")


if __name__ == "__main__":
    main()
