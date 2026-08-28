# Prompt Quarry PQ-$1 Execution Plan v1

## Objective

Move from `Developer Pack v1 = READY` to the first real paying customer without reopening internal platform work.

## Current state

```text
Generator v0                  PASS
Developer Pack v1             READY / v1.0.0
Developer Pack asset maturity VALID
Developer Starter Pack v1     BUILT
Commercial funnel             DEFINED
Offer / pricing               DEFINED
Landing contract              DEFINED
Checkout architecture         DEFINED
Analytics contract            DEFINED
Launch content system         DEFINED
```

## Missing path to PQ-$1

```text
LANDING IMPLEMENTATION
    ↓
FREE DISTRIBUTION ARTIFACT
    ↓
LIVE CHECKOUT
    ↓
LIVE ANALYTICS
    ↓
END-TO-END SMOKE TEST
    ↓
LAUNCH CONTENT
    ↓
REAL TRAFFIC
    ↓
REAL PURCHASE
```

## Phase C1 — Commercial surface

### Build
A fast public landing page implementing `LANDING_V1.md`.

### Required routes

```text
/
/free/developer-starter-pack
/developer-pack
/license
```

A single-page implementation with anchored sections is acceptable for v0 if URLs/CTAs remain clear.

### Environment contract

```text
PUBLIC_FREE_PACK_URL=
PUBLIC_DEVELOPER_PACK_CHECKOUT_URL=
PUBLIC_ANALYTICS_MODE=
```

Do not hard-code provider-specific URLs throughout components.

### Definition of done
- responsive desktop/mobile;
- Free CTA works;
- paid CTA works or clearly remains disabled before checkout is configured;
- evidence boundaries visible;
- license summary visible;
- no unsupported claims;
- metadata/SEO baseline exists;
- no fake testimonials/social proof.

## Phase C2 — Free Pack distribution

### Build
Create a deterministic customer ZIP containing only:
- `README.md`;
- `QUICKSTART.md`;
- `LICENSE.md`;
- `OFFER.md`;
- 3 prompt files.

### Required evidence
Create a small release receipt containing:
- version;
- included paths;
- archive SHA-256;
- source commit;
- generated timestamp.

Do not recreate the entire paid release-governance system unless needed.

### Definition of done
A visitor can click once from the landing and receive the exact intended Free Pack.

## Phase C3 — Checkout

### Build/configure
- one-time Developer Pack v1 product;
- launch price USD $19;
- correct release payload;
- visible use/adapt license boundary;
- success/download flow.

### Provider
Primary v1 choice: Lemon Squeezy.

### Definition of done
A non-production/test transaction path is verified where provider capabilities permit, and the correct product is delivered.

## Phase C4 — Analytics

### Build
Instrument only the events defined in `ANALYTICS_V1.md`.

Minimum launch events:
- `landing_view`;
- `free_cta_clicked`;
- `free_pack_acquired`;
- `paid_cta_clicked`;
- `checkout_started`;
- `purchase_completed` where authoritative integration permits it.

### Definition of done
A local/staging smoke test can trace one synthetic funnel session without contaminating real revenue metrics.

## Phase C5 — End-to-end launch gate

Run this exact journey:

```text
LINKEDIN-LIKE URL WITH UTM
  -> LANDING
  -> FREE CTA
  -> DOWNLOAD STARTER PACK
  -> OPEN OFFER
  -> RETURN TO PAID PAGE
  -> START CHECKOUT
  -> COMPLETE TEST FLOW
  -> VERIFY DELIVERY
  -> VERIFY ANALYTICS
```

### Gate
`PQ-LAUNCH-0` is PASS only if the full customer journey works without access to the private GitHub repository.

## Phase C6 — Distribution

Use `LAUNCH_CONTENT_V1.md` through prodAgentic.

Start with three pieces, not ten drafts waiting for perfection:
1. Why Prompt Quarry exists.
2. Code-review prompt before/after structure.
3. Free Starter Pack launch/demo.

Publish, observe, then continue the sequence.

## Phase C7 — PQ-$1

`PQ-$1` requires:
- real production transaction;
- real non-zero revenue;
- customer receives Developer Pack v1;
- transaction/product version is identifiable.

After PQ-$1, record a milestone receipt/document with:
- date;
- product/version;
- price;
- acquisition source if known;
- transaction evidence reference without exposing sensitive customer/payment details;
- first customer questions/objections.

## Commit sequence

Recommended commits:

```text
C1 feat(web): build Prompt Quarry commercial landing v0
C2 release(free): build deterministic Developer Starter Pack v1 artifact
C3 feat(commerce): wire Free download and paid checkout URLs
C4 feat(analytics): instrument minimum PQ-$1 funnel events
C5 test(launch): add commercial end-to-end smoke gate
C6 content(launch): add pq-launch-0 campaign payload for prodAgentic
```

External checkout configuration may not correspond to a repository commit; document the live product id/configuration without storing secrets.

## Stop conditions

Before PQ-$1, stop and challenge any proposed work that adds:
- authentication system;
- customer dashboard;
- subscription billing;
- recommendation engine;
- MK2 implementation;
- additional prompt marketplace scraping;
- enterprise features;
- complex CMS;
- broad redesign unrelated to conversion.

Question to ask:
`Does this materially improve our ability to get, serve, or learn from the first paying customer?`

If no, defer it.

## Immediate next commit

`C1 feat(web): build Prompt Quarry commercial landing v0`

Inputs are now frozen enough to implement:
- product hierarchy;
- copy architecture;
- price hypothesis;
- evidence boundaries;
- CTAs;
- checkout abstraction;
- analytics event names.

The next work should be executable code, not another strategy document.
