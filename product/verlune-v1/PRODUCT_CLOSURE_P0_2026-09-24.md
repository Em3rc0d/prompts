# Verlune v1 — Product Closure P0

Status: `IMPLEMENTED_CANDIDATE / PUBLIC_SALE_CLOSED`

Date: 2026-09-24

## Objective

Close the customer-journey ambiguity identified in the full-site review without bypassing the existing release gates.

The change separates:

```text
DISCOVER PREMIUM
      ↓
/premium
      ↓
PURCHASE (only when explicitly enabled)
      ↓
LICENSE + CHECKOUT EMAIL
      ↓
/unlock
      ↓
PRIVATE /app
```

from the previous ambiguous path where prospective buyers were sent directly to an unlock form.

## Implemented

- public `/premium` discovery/value surface;
- real launch-core counts sourced from the 17-asset Premium catalog;
- Premium purchase CTA hidden/disabled unless commerce is explicitly live and access is configured;
- dedicated `/api/commerce/verlune-premium/checkout` route;
- provider-test and live-canary token gates;
- HTTPS + Lemon Squeezy hostname validation;
- explicit `NOT_FOR_SALE` default configuration;
- Home, Free, header and footer route Premium intent to `/premium`;
- `/unlock` remains the existing-purchase entitlement surface;
- Verlune Free license now explicitly scopes all 11 launch-core Free assets;
- public License page now describes the full Free Library rather than only the legacy three-workflow package;
- build audit added for these boundaries.

## Commercial boundary

This implementation does **not** open public Premium purchasing.

Required default:

```text
VERLUNE_PREMIUM_COMMERCE_MODE=off
VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=NOT_FOR_SALE
```

The USD 9 value remains the governed launch-price hypothesis until the remaining human/commercial gates close. The page only renders the USD 9 purchase CTA when the deployment has explicitly enabled live public commerce.

## Live-sale prerequisites

Before changing the sale status to `LIVE`:

1. freeze/audit the Live-mode Lemon Squeezy Premium product + variant identity;
2. configure the live checkout URL;
3. confirm access validation uses that exact Live identity;
4. complete Human Review / value review;
5. execute one controlled live-canary purchase/unlock flow;
6. verify revocation/deactivation against the live entitlement;
7. record the release decision.

## License scope

`product/verlune-v1/free/LICENSE.md` now governs the current Free launch core:

- 8 structured prompts;
- 3 structured workflows;
- accompanying Free documentation.

It preserves the intended use/adaptation and no-resale/no-redistribution policy of the previous governed Free developer license, while applying it to the actual Verlune Free Library surface.

The repository license text remains an intended permissions/restrictions statement and retains its independent-legal-review note.

## Gate effect

```text
PREMIUM_DISCOVERY_SURFACE       IMPLEMENTED
PREMIUM_PURCHASE_BOUNDARY       FAIL_CLOSED
PREMIUM_PUBLIC_SALE             CLOSED
UNLOCK_ROLE                     EXISTING_PURCHASE
FREE_LICENSE_SCOPE              11_ASSETS
LIVE_IDENTITY                   OPEN
LIVE_CANARY                     OPEN
HUMAN_VISUAL_ACCEPTANCE         OPEN
READY_TO_SELL                   false
```
