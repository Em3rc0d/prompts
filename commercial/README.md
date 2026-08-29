# Prompt Quarry Commercial System v1

Status: `ACTIVE EXECUTION / EXTERNAL PROVISIONING PENDING`

This directory converts Prompt Quarry from a product repository into a sellable system.

For the current execution truth, read `STATUS_V1.md` first. Strategy documents describe the intended system; `STATUS_V1.md` records which gates are actually implemented, deployed, provisioned, or still unknown.

## North-star milestone

`PQ-$1 = verified revenue > 0 from a Prompt Quarry product.`

The commercial system exists to move one qualified person through this path:

```text
CONTENT
  -> ATTENTION
  -> FREE DEVELOPER STARTER PACK
  -> USE
  -> TRUST
  -> DEVELOPER PACK V1
  -> CHECKOUT
  -> DELIVERY
  -> CUSTOMER
  -> PQ-$1
```

## Products

### Free acquisition product

`product/free-developer-starter-v1/`

Purpose:
- deliver immediate useful value;
- demonstrate Prompt Quarry's structured-prompt philosophy;
- reduce buyer uncertainty before asking for payment;
- create a natural upgrade path.

The free product is intentionally incomplete. It contains finished prompts, but not the full methodology, reusable contracts, evidence system, end-to-end examples, or checklists of the paid pack.

Current artifact identity is recorded in `product/free-developer-starter-v1/MANIFEST.release.json`. The deterministic download endpoint is `/api/free-pack/v1`; public availability still requires deployment of the Next.js app.

### Paid product

`product/developer-pack-v1/`

Commercial state: `READY`
Evidence maturity of included assets: `VALID`
Launch price: `USD $19`

The paid product is not sold as a pile of prompts. It is sold as a compact developer prompt system: reusable templates, methodology, examples, contracts, checklists, and explicit evidence boundaries.

Paid commerce code is prepared for Lemon Squeezy hosted checkout and signed `order_created` webhook evidence. Checkout is not `LIVE` until the real provider product/variant, checkout URL, webhook secret, and deployment are provisioned.

## Current execution boundary

```text
C1  Premium Next.js web         IMPLEMENTED / VISUALLY_REVIEWED
C1.4 Vercel preview             BLOCKED_EXTERNAL
C2  Free Pack                   ARTIFACT_READY / NOT_DEPLOYED
C3  Paid commerce               CODE_READY / PROVIDER_NOT_PROVISIONED
C4  Minimum analytics           CODE_READY / NOT_LIVE
C5  End-to-end launch gate      BLOCKED_EXTERNAL
C6  Launch content              CONTENT_SPEC_READY / NOT_PUBLISHED
PQ-LAUNCH-0                     NOT_ACHIEVED
PQ-$1                           NOT_ACHIEVED
```

See `STATUS_V1.md` for hashes, endpoints, evidence semantics, and exact remaining gates.

## Commercial principles

1. Sell outcomes and workflow leverage, not prompt count.
2. Never advertise `TESTED`, `IMPROVED`, `CERTIFIED`, or `PORTABLE` without their corresponding F4-F7 evidence.
3. The Free Pack must create value before asking for payment.
4. Paid value must remain clearly larger than free value.
5. Do not create subscriptions before one-time paid demand exists.
6. Do not add commercial infrastructure that delays the first sale without materially reducing risk.
7. Every funnel step must have one primary action.
8. Measure behavior before redesigning from opinion.
9. `IMPLEMENTED != DEPLOYED` and `CLICK != PURCHASE`.
10. Real provider transaction evidence remains canonical for revenue.

## Canonical commercial documents

- `STATUS_V1.md` — current execution truth and remaining blockers.
- `FUNNEL_V1.md` — funnel stages, transitions, failure modes, and conversion logic.
- `OFFER_AND_PRICING_V1.md` — product positioning, launch offer, price hypothesis, and upgrade logic.
- `LANDING_V1.md` — landing-page information architecture and customer-facing copy contract.
- `CHECKOUT_AND_DELIVERY_V1.md` — checkout, fulfillment, file delivery, and post-purchase experience.
- `ANALYTICS_V1.md` — minimum event model and KPI definitions.
- `LAUNCH_CONTENT_V1.md` — LinkedIn/prodAgentic distribution system and launch sequence.
- `EXECUTION_PLAN_V1.md` — ordered path from product readiness to `PQ-$1`.

## Commercial state machine

```text
INTERNAL
  -> OFFER_DEFINED
  -> LANDING_READY
  -> FREE_DELIVERY_READY
  -> CHECKOUT_READY
  -> LAUNCH_READY
  -> LIVE
  -> PQ-$1
```

`READY` in the product manifest is not the same state as `LAUNCH_READY` here. Product READY means the package is commercially releasable. LAUNCH_READY means a buyer can discover, understand, purchase, receive, and use it end to end.

## What is deliberately deferred

Until `PQ-$1`, do not prioritize:
- Prompt Quarry Pro subscription;
- team plans;
- affiliate program;
- API monetization;
- complex account system;
- custom billing infrastructure;
- advanced CRM;
- multi-step onboarding automation;
- large paid-ad campaigns.

First prove that a person will voluntarily exchange money for the current value proposition.
