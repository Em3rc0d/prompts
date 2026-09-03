#!/usr/bin/env python3
"""Audit Prompt Machine Starter public copy against the current evidence ceiling.

This is a deterministic static copy audit. It creates no model, provider,
customer-value, delivery, certification, or revenue evidence.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

FILES = {
    "home": WEB / "app" / "page.tsx",
    "collections": WEB / "app" / "collections" / "page.tsx",
    "starter": WEB / "app" / "starter-collection" / "page.tsx",
    "full": WEB / "app" / "developer-pack" / "page.tsx",
    "free": WEB / "app" / "free" / "developer-starter-pack" / "page.tsx",
    "license": WEB / "app" / "license" / "page.tsx",
    "layout": WEB / "app" / "layout.tsx",
    "commerce_link": WEB / "components" / "commerce-link.tsx",
}

STARTER_CHECKOUT = WEB / "app" / "api" / "commerce" / "starter-collection" / "checkout" / "route.ts"


def text(name: str) -> str:
    path = FILES[name]
    assert path.is_file(), f"missing audited surface: {path}"
    return path.read_text(encoding="utf-8")


def reject(haystack: str, needles: list[str], scope: str) -> None:
    lower = haystack.lower()
    for needle in needles:
        assert needle.lower() not in lower, f"prohibited/stale phrase in {scope}: {needle!r}"


def main() -> int:
    home = text("home")
    collections = text("collections")
    starter = text("starter")
    full = text("full")
    free = text("free")
    license_page = text("license")
    layout = text("layout")
    commerce = text("commerce_link")

    # Product identity + public sale state.
    assert "Prompt Machine" in layout
    assert "STARTER / USD 9 PRICE HYPOTHESIS · CHECKOUT OFF" in layout
    assert "FULL / USD 19 PRICE HYPOTHESIS · CHECKOUT OFF" in layout

    assert "NOT FOR SALE · $9 PRICE HYPOTHESIS · RUNTIME EVIDENCE OPEN" in starter
    assert "PRICE HYPOTHESIS, not an active checkout" in starter
    assert "0</strong><span>Starter runtime observations" in starter
    assert "Four product-specific canaries are prepared. None has been executed." in starter
    assert "skill candidate — conditional on skill evidence" in starter
    assert "packaging evidence != behavioral evidence" in starter

    # Packaging may be claimed precisely, but not promoted into behavioral/customer proof.
    assert "9/9" in starter
    assert "50,918" in starter
    assert "4eceb1ee…" in starter
    assert "byte-for-byte deterministic" in starter
    assert "does not imply provider custody or customer delivery" in starter

    # Other key surfaces preserve hypothesis/checkout language.
    assert "$9" in home and "Starter hypothesis" in home
    assert "Both checkouts stay off until release evidence closes." in home
    assert "PRIMARY PAID HYPOTHESIS · CHECKOUT OFF" in collections
    assert "$9" in collections and "price hypothesis" in collections
    assert "NOT FOR SALE" in full and "PRICE HYPOTHESIS" in full
    assert "delivery integrity—not behavioral certification" in free

    # License page must describe Prompt Machine and current non-sale state.
    assert 'title: "License | Prompt Machine"' in license_page
    assert "No paid collection is currently for sale." in license_page
    assert "Current Starter runtime observations remain zero." in license_page
    reject(
        license_page,
        [
            "License | Prompt Quarry",
            "Prompt Quarry Developer Pack proprietary commercial license summary",
            "LICENSE.md delivered with the purchased Pack is authoritative",
        ],
        "license",
    )

    # Starter CTA is always informational while the release gate is blocked.
    assert 'kind === "starter"' in commerce
    assert '? "/starter-collection"' in commerce
    assert not STARTER_CHECKOUT.exists(), "public Starter checkout route exists while audit expects checkout OFF"

    # Fail obvious unsupported Starter claims on the directly audited Starter surface.
    reject(
        starter,
        [
            "Starter is tested",
            "Starter is proven",
            "Starter is certified",
            "Starter is production-ready",
            "Starter is ready to sell",
            "Starter is portable across models",
            "customers love Starter",
            "customers trust Starter",
            "available now",
            "buy now",
        ],
        "starter",
    )

    # Prompt Quarry may appear publicly only as the named internal factory, not the customer product identity.
    assert "FACTORY / PROMPT QUARRY · EVIDENCE BEFORE CLAIMS" in layout
    assert "Prompt Quarry handles the engineering and evidence underneath" in home

    print("STARTER PUBLIC COPY EVIDENCE AUDIT V1: PASS_CURRENT_EVIDENCE_BOUNDARY")
    print("audited_surfaces=8")
    print("starter_checkout_route_present=false")
    print("starter_runtime_observations_claimed=0")
    print("price_hypothesis_visible=true")
    print("license_identity=Prompt Machine")
    print("historical_stale_license_copy_present=false")
    print("model_calls=0")
    print("provider_calls=0")
    print("customer_outcomes_created=0")
    print("revenue_evidence_created=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
