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
    WEB / "app/api/free-pack/v1/route.ts",
    WEB / "app/api/free-pack/v1.1.0/route.ts",
    WEB / "app/api/commerce/developer-pack/checkout/route.ts",
    WEB / "app/api/commerce/lemonsqueezy/webhook/route.ts",
    WEB / "components/commerce-link.tsx",
    WEB / "components/funnel-tracker.tsx",
    WEB / "components/quarry-engine.tsx",
    WEB / "generated/free-developer-starter-v1.ts",
    WEB / "generated/free-pack-archive.d.ts",
    WEB / "scripts/fetch-free-pack.mjs",
    WEB / "scripts/assert-golden-path-build.mjs",
    WEB / "lib/commerce-mode.ts",
    WEB / "lib/developer-pack-release.ts",
    WEB / "lib/lemonsqueezy.ts",
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

EXPECTED_FREE_SHA256 = "55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32"
EXPECTED_FREE_SIZE = "23498"
EXPECTED_PAID_SHA256 = "546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009"
EXPECTED_PAID_SIZE = "86763"


def fail(message: str) -> None:
    raise SystemExit(f"COMMERCIAL WEB V0: FAIL — {message}")


def require_tokens(label: str, source: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in source:
            fail(f"{label} missing: {token}")


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
        "quarry engine",
        "not observed = unknown",
    ]
    for phrase in required_copy:
        if phrase not in lower:
            fail(f"required commercial boundary/copy missing: {phrase}")

    for phrase in FORBIDDEN_MARKETING:
        if phrase in lower:
            fail(f"unsupported marketing claim observed: {phrase}")

    commerce_link = (WEB / "components/commerce-link.tsx").read_text(encoding="utf-8")
    require_tokens(
        "public commerce fail-closed contract",
        commerce_link,
        (
            "NEXT_PUBLIC_FREE_PACK_URL",
            "NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS",
            '=== "LIVE"',
            '"/api/free-pack/v1.1.0"',
            '"/api/commerce/developer-pack/checkout"',
            '"/developer-pack"',
            "event.preventDefault()",
        ),
    )
    if "NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL" in commerce_link:
        fail("customer-facing CTA bypasses the governed server checkout gate")

    env = (WEB / ".env.example").read_text(encoding="utf-8")
    for key in (
        "NEXT_PUBLIC_FREE_PACK_URL=",
        "NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE",
        "NEXT_PUBLIC_ANALYTICS_MODE=off",
        "DEVELOPER_PACK_COMMERCE_MODE=off",
        "LEMONSQUEEZY_DEVELOPER_PACK_TEST_CHECKOUT_URL=",
        "LEMONSQUEEZY_DEVELOPER_PACK_LIVE_CHECKOUT_URL=",
        "LEMONSQUEEZY_PROVIDER_TEST_TOKEN=",
        "LEMONSQUEEZY_LIVE_CANARY_TOKEN=",
        "LEMONSQUEEZY_WEBHOOK_SECRET=",
        "LEMONSQUEEZY_STORE_ID=",
        "LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID=",
        "LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID=",
    ):
        if key not in env:
            fail(f"commerce environment contract missing: {key}")
    for legacy in ("NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL", "LEMONSQUEEZY_ALLOW_TEST_MODE"):
        if legacy in env:
            fail(f"legacy commerce environment key still present: {legacy}")

    free_route = (WEB / "app/api/free-pack/v1/route.ts").read_text(encoding="utf-8")
    free_materializer = (WEB / "scripts/fetch-free-pack.mjs").read_text(encoding="utf-8")
    free_declaration = (WEB / "generated/free-pack-archive.d.ts").read_text(encoding="utf-8")
    require_tokens(
        "free pack runtime integrity contract",
        free_route,
        (
            "FREE_PACK_BASE64",
            EXPECTED_FREE_SHA256,
            f"EXPECTED_SIZE = {EXPECTED_FREE_SIZE}",
            "free_pack_integrity_failure",
            "X-Prompt-Quarry-SHA256",
            "X-Prompt-Quarry-Version",
        ),
    )
    require_tokens(
        "free pack build materialization contract",
        free_materializer,
        (
            EXPECTED_FREE_SHA256,
            f"EXPECTED_SIZE = {EXPECTED_FREE_SIZE}",
            'path.join(dir, "free-pack-archive.ts")',
            "FREE PACK MATERIALIZE: PASS",
        ),
    )
    if "FREE_PACK_BASE64: string" not in free_declaration:
        fail("clean-checkout type declaration for build-materialized Free Pack is missing")

    generated = (WEB / "generated/free-developer-starter-v1.ts").read_text(encoding="utf-8")
    if EXPECTED_FREE_SHA256 not in generated:
        fail("free pack generated snapshot is not bound to v1.1 release fingerprint")
    if 'FREE_PACK_VERSION = "1.1.0"' not in generated or f"FREE_PACK_ARCHIVE_SIZE = {EXPECTED_FREE_SIZE}" not in generated:
        fail("free pack generated snapshot does not identify v1.1 size/version")

    release = (WEB / "lib/developer-pack-release.ts").read_text(encoding="utf-8")
    require_tokens(
        "paid release identity contract",
        release,
        (
            'productId: "pq-developer-pack"',
            'version: "1.1.0"',
            f"archiveSize: {EXPECTED_PAID_SIZE}",
            EXPECTED_PAID_SHA256,
            'export type CommerceGate = "provider_test" | "live_canary" | "live"',
            "pq_product_id",
            "pq_product_version",
            "pq_archive_sha256",
            "pq_archive_size",
            "pq_gate",
        ),
    )

    checkout = (WEB / "app/api/commerce/developer-pack/checkout/route.ts").read_text(encoding="utf-8")
    require_tokens(
        "paid checkout gate contract",
        checkout,
        (
            "commerce_disabled",
            "commerce_configuration_conflict",
            "provider_test_not_authorized",
            "live_canary_not_authorized",
            'request.headers.get("x-pq-provider-test-token")',
            'request.headers.get("x-pq-live-canary-token")',
            "releaseCheckoutCustomData(gate)",
            '"provider_test_checkout_started"',
            '"live_delivery_canary_checkout_started"',
            '"checkout_started"',
            "checkout_url_must_use_https",
        ),
    )

    webhook_lib = (WEB / "lib/lemonsqueezy.ts").read_text(encoding="utf-8")
    require_tokens(
        "signed provider evidence contract",
        webhook_lib,
        (
            'createHmac("sha256"',
            "timingSafeEqual",
            "release_identity_mismatch",
            "commerce_gate_configuration_mismatch",
            '"provider_test_order_accepted"',
            '"live_delivery_canary_order_accepted"',
            '"purchase_completed"',
            'evidence: "provider_signed_order_created"',
        ),
    )

    tracker = (WEB / "components/funnel-tracker.tsx").read_text(encoding="utf-8")
    for token in ("NEXT_PUBLIC_ANALYTICS_MODE", "landing_view", "paid_product_viewed", "utm_source", "sessionStorage"):
        if token not in tracker:
            fail(f"analytics contract missing: {token}")
    for forbidden_event in (
        'event: "provider_test_order_accepted"',
        'event: "live_delivery_canary_order_accepted"',
        'event: "purchase_completed"',
    ):
        if forbidden_event in tracker:
            fail(f"client analytics manufactures provider/revenue evidence: {forbidden_event}")

    if "lemonsqueezy.com" in lower or "gumroad.com" in lower:
        fail("checkout provider URL is hard-coded in customer-facing source")

    css = (WEB / "app/globals.css").read_text(encoding="utf-8")
    for breakpoint in ("@media(max-width:900px)", "@media(max-width:620px)"):
        if breakpoint not in css:
            fail(f"responsive gate missing: {breakpoint}")

    for visual_contract in (".heroPremium", ".engineShell", ".pipeline", ".productFrame", ".evidenceLadder", ".premiumCta"):
        if visual_contract not in css:
            fail(f"premium visual system contract missing: {visual_contract}")

    if "prefers-reduced-motion:reduce" not in css:
        fail("reduced-motion accessibility gate missing")

    layout = (WEB / "app/layout.tsx").read_text(encoding="utf-8")
    require_tokens(
        "brand shell/accessibility contract",
        layout,
        (
            'title: "Prompt Quarry — Structured Prompts for Developers"',
            'applicationName: "Prompt Quarry"',
            '<html lang="en">',
            'aria-label="Prompt Quarry home"',
            'aria-label="Primary"',
            "brandGlyph",
            "brandWord",
            "brandVersion",
            "FunnelTracker",
        ),
    )

    package = (WEB / "package.json").read_text(encoding="utf-8")
    if '"next": "16.3.3"' not in package:
        fail("Next.js Active LTS security release 16.3.3 is not pinned")

    print("COMMERCIAL WEB V0: PASS")
    print(f"required_files={len(REQUIRED)}")
    print("framework=Next.js 16.3.3 App Router")
    print("visual_system=premium technical/editorial + Quarry Engine")
    print("brand_shell=metadata + semantic navigation + accessible brand controls")
    print("free_delivery=v1.1 build-materialized ZIP + runtime SHA-256 fail-closed verification")
    print("paid_release=Developer Pack v1.1.0 exact 86763-byte release identity")
    print("commerce=provider_test/live_canary/live gates; public CTA defaults NOT_FOR_SALE")
    print("purchase_evidence=signed public-live provider order only")
    print("analytics=minimal UTM/session bridge; no client purchase/revenue inference")
    print("boundary=READY/VALID only; F4-F7 superiority/certification claims remain unasserted")


if __name__ == "__main__":
    main()
