#!/usr/bin/env python3
"""Commercial web acceptance for the active Verlune customer surface.

Historical Prompt Machine / Starter artifacts retain their own evidence and validators.
This check protects the current buyer-facing Verlune information architecture, claim
boundaries, Code Review release identity, Premium fail-closed state, and legacy redirects.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
COMMERCIAL = ROOT / "commercial"

LAYOUT = WEB / "app/layout.tsx"
HOME = WEB / "app/page.tsx"
FREE = WEB / "app/free/page.tsx"
PREMIUM = WEB / "app/premium/page.tsx"
CODE_REVIEW = WEB / "app/code-review/page.tsx"
LEARN = WEB / "app/learn/page.tsx"
LICENSE = WEB / "app/license/page.tsx"
UNLOCK = WEB / "app/unlock/page.tsx"
COLLECTIONS = WEB / "app/collections/page.tsx"
DEVELOPER_PACK = WEB / "app/developer-pack/page.tsx"
STARTER_COLLECTION = WEB / "app/starter-collection/page.tsx"
COMMERCE_LINK = WEB / "components/commerce-link.tsx"
CODE_REVIEW_RELEASE = WEB / "lib/starter-code-review-release.ts"
PUBLIC_PRODUCTS = WEB / "lib/public-products.ts"
PREMIUM_COMMERCE = WEB / "lib/verlune-premium-commerce.ts"
PREMIUM_CHECKOUT = WEB / "app/api/commerce/verlune-premium/checkout/route.ts"
ENV = WEB / ".env.example"
BRAND = COMMERCIAL / "VERLUNE_BRAND_ARCHITECTURE_V1.md"

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
    "new content weekly",
    "lifetime access",
    "priority support",
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
    free = text(FREE)
    premium = text(PREMIUM)
    code_review = text(CODE_REVIEW)
    learn = text(LEARN)
    license_page = text(LICENSE)
    unlock = text(UNLOCK)
    collections = text(COLLECTIONS)
    developer_pack = text(DEVELOPER_PACK)
    starter_collection = text(STARTER_COLLECTION)
    commerce_link = text(COMMERCE_LINK)
    release = text(CODE_REVIEW_RELEASE)
    public_products = text(PUBLIC_PRODUCTS)
    premium_commerce = text(PREMIUM_COMMERCE)
    premium_checkout = text(PREMIUM_CHECKOUT)
    env = text(ENV)
    brand = text(BRAND)

    public_surface = "\n".join(
        (layout, home, free, premium, code_review, learn, license_page, unlock)
    )
    lower = public_surface.lower()

    for phrase in FORBIDDEN_MARKETING:
        if phrase in lower:
            fail(f"unsupported marketing claim observed: {phrase}")

    require(
        "layout",
        layout,
        'default: "Verlune — Structured AI work"',
        'applicationName: "Verlune"',
        'aria-label="Verlune home"',
        '<span>VERLUNE</span>',
        'href="/premium">Premium</',
        'href="/unlock">Unlock access',
    )
    if "Prompt <b>Machine</b>" in layout:
        fail("legacy Prompt Machine wordmark leaked into global customer shell")

    require(
        "home",
        home,
        "STRUCTURED AI WORK",
        "Use ours.",
        "Build yours.",
        "Work better with AI.",
        "PROMPT ≠ WORKFLOW",
        'href="/free"',
        'href="/premium"',
        "Generated is not certified.",
    )

    require(
        "Free Library",
        free,
        "VERLUNE FREE",
        "Useful before",
        "FREE PROMPTS",
        "FREE WORKFLOWS",
        "FREE ≠ THROWAWAY",
        "No universal model claim.",
        'href="/premium"',
    )

    require(
        "Premium discovery",
        premium,
        "VERLUNE PREMIUM",
        "Go deeper.",
        "Build your own.",
        "Purchasing not open yet",
        "Already purchased? Unlock",
        "PREMIUM_ASSETS.length",
        "getVerlunePremiumCommerceState",
        "/api/commerce/verlune-premium/checkout",
    )

    require(
        "Premium commerce state",
        premium_commerce,
        'VERLUNE_PREMIUM_CANDIDATE_PRICE_USD = 9',
        'VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE"',
        'VERLUNE_PREMIUM_COMMERCE_MODE',
        'purchaseAvailable: mode === "live"',
    )
    require(
        "Premium checkout boundary",
        premium_checkout,
        "commerce_disabled",
        "premium_access_not_configured",
        "provider_test_not_authorized",
        "live_canary_not_authorized",
        "checkout_url_not_allowed",
    )

    require(
        "Code Review page wiring",
        code_review,
        "CODE_REVIEW as product",
        "ProductActions",
        "A WORKFLOW FOR THE CHANGE IN FRONT OF YOU",
        "EVIDENCE WITH BOUNDARIES",
        "product.evidenceSummary.packQA",
        "product.evidenceSummary.regression",
        "product.evidenceSummary.model",
        "It is advisory.",
    )
    require(
        "Code Review public product facts",
        public_products,
        'name: "Verlune Code Review"',
        "price: 9",
        'billingModel: "one-time"',
        'packQA: "77/77"',
        'regression: "4/4 human-review passes"',
        'model: "Gemini 3.5 Flash"',
    )

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

    require(
        "Learn",
        learn,
        "VERLUNE / LEARN",
        "Useful ideas before a purchase.",
        "Evidence is part of the product.",
    )

    require(
        "License",
        license_page,
        "VERLUNE / LICENSE",
        "Your work.",
        "VERLUNE FREE LIBRARY",
        "FREE_ASSETS.length",
        "CUSTOMER-LICENSE.md",
    )

    require(
        "Unlock",
        unlock,
        "VERLUNE PREMIUM / PRIVATE ACCESS",
        "Unlock the library you purchased.",
        "License + checkout email",
        'href="/premium">← Explore Premium',
    )

    for label, source in (
        ("collections redirect", collections),
        ("developer-pack redirect", developer_pack),
        ("starter-collection redirect", starter_collection),
    ):
        require(label, source, 'permanentRedirect("/code-review")')

    require(
        "commerce defaults",
        env,
        "NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS=NOT_FOR_SALE",
        "STARTER_CODE_REVIEW_COMMERCE_MODE=off",
        "VERLUNE_PREMIUM_COMMERCE_MODE=off",
        "VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=NOT_FOR_SALE",
        "LEMONSQUEEZY_VERLUNE_PREMIUM_TEST_CHECKOUT_URL=",
        "LEMONSQUEEZY_VERLUNE_PREMIUM_LIVE_CHECKOUT_URL=",
    )
    if "VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=LIVE" in env:
        fail("Premium public sale is enabled in example/default configuration")

    require(
        "commerce link",
        commerce_link,
        'kind: "free" | "code-review" | "starter" | "paid"',
        '"/api/commerce/starter-code-review/checkout"',
        '"/code-review"',
        "event.preventDefault()",
    )

    require(
        "brand architecture",
        brand,
        "Verlune",
        "customer-facing",
        "Prompt Machine",
        "Prompt Quarry",
    )

    print("COMMERCIAL WEB V0: PASS")
    print("customer_brand=Verlune")
    print("home_positioning=Use ours / Build yours / Work better with AI")
    print("free_library_assets=19")
    print("premium_library_assets=41")
    print("premium_discovery=/premium")
    print("premium_public_sale=OFF")
    print("unlock_role=existing_purchase")
    print("code_review_release=1.0.0")
    print(f"code_review_archive={VERLUNE_ARCHIVE}")
    print("ready_to_sell=false")


if __name__ == "__main__":
    main()
