#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"

TRACKER = WEB / "components" / "funnel-tracker.tsx"
LINK = WEB / "components" / "commerce-link.tsx"
INTENT_ROUTE = WEB / "app" / "api" / "analytics" / "intent" / "route.ts"
FREE_ROUTE = WEB / "app" / "api" / "free-pack" / "v1" / "route.ts"
CHECKOUT_ROUTE = WEB / "app" / "api" / "commerce" / "developer-pack" / "checkout" / "route.ts"
WEBHOOK_ROUTE = WEB / "app" / "api" / "commerce" / "lemonsqueezy" / "webhook" / "route.ts"
LEMON = WEB / "lib" / "lemonsqueezy.ts"
STARTER_IDENTITY = ROOT / "product" / "starter-collection-v1" / "PRODUCT_IDENTITY_V1.json"

CANONICAL_STARTER_PRODUCT_ID = "prompt-machine-starter-collection"
LEGACY_STARTER_PRODUCT_ID = "pq-developer-starter-collection"


def fail(message: str) -> None:
    raise SystemExit(f"ANALYTICS V0: FAIL — {message}")


def main() -> None:
    paths = (TRACKER, LINK, INTENT_ROUTE, FREE_ROUTE, CHECKOUT_ROUTE, WEBHOOK_ROUTE, LEMON, STARTER_IDENTITY)
    for path in paths:
        if not path.is_file():
            fail(f"missing analytics surface: {path.relative_to(ROOT)}")

    tracker = TRACKER.read_text(encoding="utf-8")
    link = LINK.read_text(encoding="utf-8")
    intent_route = INTENT_ROUTE.read_text(encoding="utf-8")
    free_route = FREE_ROUTE.read_text(encoding="utf-8")
    checkout_route = CHECKOUT_ROUTE.read_text(encoding="utf-8")
    webhook_route = WEBHOOK_ROUTE.read_text(encoding="utf-8")
    lemon = LEMON.read_text(encoding="utf-8")
    identity = STARTER_IDENTITY.read_text(encoding="utf-8")

    event_contract = {
        "landing_view": tracker,
        "free_cta_clicked": link,
        "free_pack_acquired": free_route,
        "starter_product_viewed": tracker,
        "starter_cta_clicked": link,
        "paid_product_viewed": tracker,
        "paid_cta_clicked": link,
        "checkout_started": checkout_route,
        "purchase_completed": lemon + webhook_route,
    }
    for event, source in event_contract.items():
        if event not in source:
            fail(f"funnel event missing from authoritative surface: {event}")

    for token in (
        'fetch("/api/analytics/intent"',
        "CLIENT_INTENT_EVENTS",
        'credentials: "same-origin"',
        "keepalive: true",
        'path.startsWith("/starter-collection")',
        f'product_id: "{CANONICAL_STARTER_PRODUCT_ID}"',
        'product_version: "1.0.0-candidate"',
    ):
        if token not in tracker:
            fail(f"client intent forwarding contract missing: {token}")

    for token in (
        'kind: "free" | "starter" | "paid"',
        'event: "starter_cta_clicked"',
        '"/starter-collection"',
        f'product_id: "{CANONICAL_STARTER_PRODUCT_ID}"',
        'product_version: "1.0.0-candidate"',
    ):
        if token not in link:
            fail(f"Starter commerce-intent contract missing: {token}")

    if LEGACY_STARTER_PRODUCT_ID in tracker or LEGACY_STARTER_PRODUCT_ID in link:
        fail("new Starter client intent still emits legacy product identity")
    if f'"product_id": "{LEGACY_STARTER_PRODUCT_ID}"' not in identity:
        fail("legacy Starter product identity is not preserved in the explicit identity contract")
    if '"new_analytics_events_use_canonical_id": true' not in identity:
        fail("Starter identity contract does not require canonical ids for new analytics")

    for token in (
        "PM_INTENT_EVENT",
        'schema: "prompt-machine-intent-v1"',
        'evidence_class: "UNTRUSTED_CLIENT_INTENT"',
        "CLIENT_INTENT_EVENTS",
        'status: 202',
        '"Cache-Control": "no-store"',
    ):
        if token not in intent_route:
            fail(f"server-observed intent contract missing: {token}")

    for client_event in (
        "landing_view",
        "collections_viewed",
        "free_product_viewed",
        "free_cta_clicked",
        "starter_product_viewed",
        "starter_cta_clicked",
        "paid_product_viewed",
        "paid_cta_clicked",
    ):
        if f'"{client_event}"' not in intent_route:
            fail(f"intent allowlist missing: {client_event}")

    for forbidden_event in ("checkout_started", "purchase_completed", "delivery_completed"):
        if f'"{forbidden_event}"' in intent_route:
            fail(f"client intent sink may not accept authoritative event: {forbidden_event}")

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
        if f'"{field}"' not in intent_route:
            fail(f"intent observation missing sanitized attribution dimension: {field}")

    if "checkout[custom][" not in checkout_route or "custom_data" not in lemon:
        fail("provider custom-data attribution bridge missing")

    # Anonymous session exists for local/session-level diagnostics only.
    if "pq:session-id" not in tracker or "crypto.randomUUID()" not in tracker:
        fail("anonymous local session contract missing")
    external_surfaces = "\n".join((link, intent_route, free_route, checkout_route, webhook_route, lemon))
    if "pq:session-id" in external_surfaces:
        fail("anonymous browser session id leaked outside local tracker")

    for sensitive_token in ("user_email", "user_name", "user-agent", "x-forwarded-for"):
        if sensitive_token in intent_route.lower():
            fail(f"client intent sink references unnecessary identity/network data: {sensitive_token}")

    for pii in ("user_email", "user_name"):
        if pii in (webhook_route + lemon).lower():
            fail(f"provider PII referenced in purchase evidence path: {pii}")

    print("ANALYTICS V0: PASS")
    print("intent_sink=/api/analytics/intent -> PM_INTENT_EVENT")
    print("intent_evidence=UNTRUSTED_CLIENT_INTENT")
    print("events=landing_view,free_cta_clicked,free_pack_acquired,starter_product_viewed,starter_cta_clicked,paid_product_viewed,paid_cta_clicked,checkout_started,purchase_completed")
    print("free_acquisition=server delivery after archive integrity verification")
    print(f"starter_identity={CANONICAL_STARTER_PRODUCT_ID}; legacy alias historical only")
    print("starter=$9 intent only; no client purchase evidence")
    print("purchase=provider-signed paid order only")
    print("attribution=source/medium/campaign/content")
    print("session_id=browser-session-only; never sent to intent sink")
    print("revenue_boundary=provider transaction remains canonical")


if __name__ == "__main__":
    main()
