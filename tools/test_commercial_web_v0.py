#!/usr/bin/env python3
"""Commercial web acceptance for the current Verlune customer surface.

Legacy Prompt Machine/Starter artifacts remain historical evidence and have their own
validators. This check protects the active buyer-facing brand, evidence boundaries,
commercial ladder, and fail-closed checkout state without forcing obsolete copy back
onto the website.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
COMMERCIAL = ROOT / "commercial"

LAYOUT = WEB / "app/layout.tsx"
HOME = WEB / "app/page.tsx"
COLLECTIONS = WEB / "app/collections/page.tsx"
LEARN = WEB / "app/learn/page.tsx"
FREE = WEB / "app/free/developer-starter-pack/page.tsx"
PRODUCT = WEB / "app/starter-collection/page.tsx"
FUTURE = WEB / "app/developer-pack/page.tsx"
LICENSE = WEB / "app/license/page.tsx"
ENGINE = WEB / "components/quarry-engine.tsx"
COMMERCE_LINK = WEB / "components/commerce-link.tsx"
RELEASE = WEB / "lib/starter-code-review-release.ts"
ENV = WEB / ".env.example"
BRAND = COMMERCIAL / "VERLUNE_BRAND_ARCHITECTURE_V1.md"
STATUS = COMMERCIAL / "STATUS_CURRENT.md"
REVENUE = COMMERCIAL / "REVENUE_EXPERIMENT_V1.md"
LEGACY_PUBLIC_STARTER_CHECKOUT = WEB / "app/api/commerce/starter-collection/checkout/route.ts"
GOVERNED_CODE_REVIEW_CHECKOUT = WEB / "app/api/commerce/starter-code-review/checkout/route.ts"

VERLUNE_ARCHIVE = "verlune-code-review-v1.0.0.zip"
VERLUNE_ARCHIVE_BYTES = "18859"
VERLUNE_ARCHIVE_SHA = "4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649"

FORBIDDEN_MARKETING = (
    "battle-tested",
    "proven superior",
    "best-performing",
    "guaranteed to improve",
    "works with every model",
    "universally portable",
    "guaranteed revenue",
    "guaranteed to sell",
)


def fail(message: str) -> None:
    raise SystemExit(f"COMMERCIAL WEB V0: FAIL — {message}")


def text(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require(label: str, source: str, *tokens: str) -> None:
    for token in tokens:
        if token not in source:
            fail(f"{label} missing: {token}")


def main() -> None:
    layout = text(LAYOUT)
    home = text(HOME)
    collections = text(COLLECTIONS)
    learn = text(LEARN)
    free = text(FREE)
    product = text(PRODUCT)
    future = text(FUTURE)
    license_page = text(LICENSE)
    engine = text(ENGINE)
    commerce_link = text(COMMERCE_LINK)
    release = text(RELEASE)
    env = text(ENV)
    brand = text(BRAND)
    status = text(STATUS)
    revenue = text(REVENUE)

    public_surface = "\n".join((layout, home, collections, learn, free, product, future, license_page, engine))
    lower = public_surface.lower()

    for phrase in FORBIDDEN_MARKETING:
        if phrase in lower:
            fail(f"unsupported marketing claim observed: {phrase}")

    require(
        "layout",
        layout,
        'title: "Verlune — Reusable AI Workflows You Can Inspect"',
        'applicationName: "Verlune"',
        'aria-label="Verlune home"',
        '<b>VERLUNE</b>',
    )
    if "Prompt <b>Machine</b>" in layout:
        fail("legacy Prompt Machine wordmark leaked into global customer shell")

    require(
        "home",
        home,
        "VERLUNE / REUSABLE AI WORKFLOWS",
        "Stop starting from a blank chat.",
        "What are you trying to get done?",
        "FREE LIBRARY",
        "Verlune Code Review",
        "$9",
        "77/77",
        "marketing claim",
        "observed evidence",
        "checkout remains off",
    )

    require(
        "Verlune Code Review page",
        product,
        "Verlune Code Review",
        "One focused workflow. Exact evidence. No borrowed certainty.",
        "$9 PRICE HYPOTHESIS",
        "gemini-3.5-flash",
        "4/4",
        "77/77",
        "18,859",
        VERLUNE_ARCHIVE,
        "PROVIDER VALIDATION PENDING",
        "public checkout",
    )
    for stale in ("0 PASS, 0 FAIL, 1 INCONCLUSIVE", "9-file customer payload", "two governed workflows"):
        if stale in product:
            fail(f"superseded Starter claim leaked into Verlune product page: {stale}")

    require(
        "collections",
        collections,
        "VERLUNE / WORKFLOWS",
        "Verlune Code Review",
        "$9",
        "77/77",
        "not for sale",
        "Verlune Developer Collection",
        "$19",
        "NOT A RELEASE",
    )
    require("future collection", future, "Verlune", "$19", "price hypothesis", "NOT FOR SALE")

    require("free library", free, "Verlune", "Three workflows", "Code Review", "Bug Diagnosis", "Technical Decision")
    require("learn", learn, "VERLUNE / LEARN", "Useful ideas before a purchase.", "Evidence is part of the product.")

    require(
        "license",
        license_page,
        "VERLUNE / COMMERCIAL LICENSE",
        "Verlune Code Review is not publicly for sale yet.",
        "CUSTOMER-LICENSE.md",
        "Gemini 3.5 Flash",
        "model-specific claim",
    )

    require("workflow visualization", engine, 'aria-label="Verlune workflow visualization"', "VERLUNE WORKFLOW", "evidence visible by design")

    require(
        "Code Review release identity",
        release,
        'productId: "prompt-machine-starter-code-review-edition"',
        'version: "1.0.0"',
        f'archiveName: "{VERLUNE_ARCHIVE}"',
        f"archiveSize: {VERLUNE_ARCHIVE_BYTES}",
        VERLUNE_ARCHIVE_SHA,
        "Buyer-facing brand/product name is Verlune Code Review.",
    )
    if not GOVERNED_CODE_REVIEW_CHECKOUT.is_file():
        fail("governed Code Review checkout route is missing")
    if LEGACY_PUBLIC_STARTER_CHECKOUT.exists():
        fail("superseded public Starter checkout route still exists")

    require(
        "commerce defaults",
        env,
        "NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS=NOT_FOR_SALE",
        "STARTER_CODE_REVIEW_COMMERCE_MODE=off",
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_TEST_CHECKOUT_URL=",
        "LEMONSQUEEZY_STARTER_CODE_REVIEW_LIVE_CHECKOUT_URL=",
    )
    require("commerce link", commerce_link, 'kind: "free" | "starter" | "paid"', '"/starter-collection"', "event.preventDefault()")

    require("brand architecture", brand, "Verlune", "customer-facing", "Prompt Machine", "Prompt Quarry")
    require(
        "current commercial status",
        status,
        "CUSTOMER-FACING  Verlune",
        "PRODUCT          Verlune Code Review",
        VERLUNE_ARCHIVE,
        VERLUNE_ARCHIVE_SHA,
        "PUBLIC_CHECKOUT     OFF",
        "real purchases      0",
        "real revenue        0",
    )

    require(
        "revenue experiment",
        revenue,
        "PQ-$1 = first real non-test paid purchase successfully delivered",
        "USD 9",
        "USD 19",
        "PRICE HYPOTHESIS",
        "free download          != revenue",
        "accepted real purchase == purchase evidence",
    )

    print("COMMERCIAL WEB V0: PASS")
    print("customer_brand=Verlune")
    print("first_paid_product=Verlune Code Review")
    print("price_hypothesis_usd=9")
    print("future_collection_hypothesis_usd=19")
    print(f"archive={VERLUNE_ARCHIVE}")
    print(f"archive_bytes={VERLUNE_ARCHIVE_BYTES}")
    print(f"archive_sha256={VERLUNE_ARCHIVE_SHA}")
    print("public_checkout=OFF")
    print("ready_to_sell=false")


if __name__ == "__main__":
    main()
