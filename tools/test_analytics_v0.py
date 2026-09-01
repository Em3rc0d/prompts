#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

TRACKER = WEB / "components" / "funnel-tracker.tsx"
LINK = WEB / "components" / "commerce-link.tsx"
FREE_ROUTE = WEB / "app" / "api" / "free-pack" / "v1" / "route.ts"
CHECKOUT_ROUTE = WEB / "app" / "api" / "commerce" / "developer-pack" / "checkout" / "route.ts"
WEBHOOK_ROUTE = WEB / "app" / "api" / "commerce" / "lemonsqueezy" / "webhook" / "route.ts"
LEMON = WEB / "lib" / "lemonsqueezy.ts"


def fail(message: str) -> None:
    raise SystemExit(f"ANALYTICS V0: FAIL — {message}")


def main() -> None:
    paths = (TRACKER, LINK, FREE_ROUTE, CHECKOUT_ROUTE, WEBHOOK_ROUTE, LEMON)
    for path in paths:
        if not path.is_file():
            fail(f"missing analytics surface: {path.relative_to(ROOT)}")

    tracker = TRACKER.read_text(encoding="utf-8")
    link = LINK.read_text(encoding="utf-8")
    free_route = FREE_ROUTE.read_text(encoding="utf-8")
    checkout_route = CHECKOUT_ROUTE.read_text(encoding="utf-8")
    webhook_route = WEBHOOK_ROUTE.read_text(encoding="utf-8")
    lemon = LEMON.read_text(encoding="utf-8")

    event_contract = {
        "landing_view": tracker,
        "free_cta_clicked": link,
        "free_pack_acquired": free_route,
        "paid_product_viewed": tracker,
        "paid_cta_clicked": link,
        "checkout_started": checkout_route,
        "purchase_completed": lemon + webhook_route,
    }
    for event, source in event_contract.items():
        if event not in source:
            fail(f"funnel event missing from authoritative surface: {event}")

    if 'event: "purchase_completed"' in tracker or 'event: "purchase_completed"' in link:
        fail("purchase_completed must not be manufactured by client telemetry")

    for token in ("provider_signed_order_created", "timingSafeEqual", 'attributes.status !== "paid"'):
        if token not in lemon:
            fail(f"authoritative purchase evidence token missing: {token}")

    for token in ("FREE_PACK_ARCHIVE_SHA256", "free_pack_integrity_failure", "PQ_FUNNEL_EVENT"):
        if token not in free_route:
            fail(f"verified Free Pack acquisition token missing: {token}")

    for field in ("source", "medium", "campaign", "content"):
        if field not in checkout_route or field not in lemon:
            fail(f"campaign attribution is not reconciled end-to-end: {field}")

    if "checkout[custom][" not in checkout_route or "custom_data" not in lemon:
        fail("provider custom-data attribution bridge missing")

    # Anonymous session exists for local/session-level diagnostics only.
    if "pq:session-id" not in tracker or "crypto.randomUUID()" not in tracker:
        fail("anonymous local session contract missing")
    external_surfaces = "\n".join((link, free_route, checkout_route, webhook_route, lemon))
    if "pq:session-id" in external_surfaces:
        fail("anonymous browser session id leaked outside local tracker")

    for pii in ("user_email", "user_name"):
        if pii in (webhook_route + lemon).lower():
            fail(f"provider PII referenced in purchase evidence path: {pii}")

    print("ANALYTICS V0: PASS")
    print("events=landing_view,free_cta_clicked,free_pack_acquired,paid_product_viewed,paid_cta_clicked,checkout_started,purchase_completed")
    print("free_acquisition=server delivery after archive integrity verification")
    print("purchase=provider-signed paid order only")
    print("attribution=source/medium/campaign/content")
    print("session_id=browser-session-only")
    print("revenue_boundary=provider transaction remains canonical")


if __name__ == "__main__":
    main()
