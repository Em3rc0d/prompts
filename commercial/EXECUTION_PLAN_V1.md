# Prompt Quarry PQ-$1 Execution Plan v1

## Objective

Move from `Developer Pack v1 = READY` to the first real paying customer without reopening internal platform work.

Current execution truth lives in `STATUS_V1.md`. This document defines the ordered gates.

## Current state

```text
Generator v0                  PASS
Developer Pack v1             READY / v1.0.0
Developer Pack asset maturity VALID
Premium Next.js web           IMPLEMENTED / VISUALLY_REVIEWED
Vercel preview                BLOCKED_EXTERNAL
Developer Starter Pack v1     ARTIFACT_READY / NOT_DEPLOYED
Paid commerce integration     CODE_READY / PROVIDER_NOT_PROVISIONED
Minimum funnel analytics      CODE_READY / NOT_LIVE
Launch content system         CONTENT_SPEC_READY / NOT_PUBLISHED
PQ-LAUNCH-0                   NOT_ACHIEVED
PQ-$1                         NOT_ACHIEVED
```

## Remaining path to PQ-$1

```text
PROVISION VERCEL PROJECT
    +
PROVISION LEMON SQUEEZY PRODUCT
    ↓
C5 END-TO-END SMOKE
    ↓
PQ-LAUNCH-0
    ↓
C6 LAUNCH CONTENT
    ↓
REAL TRAFFIC
    ↓
REAL PURCHASE
    ↓
PQ-$1
```

## Phase C1 — Commercial surface

State: `IMPLEMENTED / VISUALLY_REVIEWED`

Implemented in Next.js App Router under `web/`:

```text
/
/free/developer-starter-pack
/developer-pack
/license
```

The visual system is intentionally premium technical/editorial rather than generic SaaS. It includes the Quarry Engine, manufacturing pipeline, governed-product framing, evidence ladder, responsive layout, and reduced-motion handling.

Remaining gate: execute a real Next.js deployment/build in Vercel or another controlled runtime. GitHub Actions jobs have repeatedly been created without a runner and with zero executed steps, so those runs are neither PASS nor meaningful code failures.

## Phase C2 — Free Pack distribution

State: `ARTIFACT_READY / NOT_DEPLOYED`

Governed payload: exactly 7 customer files.

```text
LICENSE.md
OFFER.md
QUICKSTART.md
README.md
prompts/bug-diagnosis.md
prompts/code-review.md
prompts/technical-decision.md
```

Deterministic archive identity:

```text
filename  prompt-quarry-developer-starter-v1.zip
size      11573 bytes
sha256    55121028168f9a5394fe79ccc3102caa60e5df85c59a03639dc6e5392e5b2ee1
```

The Next.js route `/api/free-pack/v1` rebuilds the governed payload and fails closed if archive size/hash differs. `free_pack_acquired` is emitted server-side only after integrity verification.

Remaining gate: deploy the Next.js app so the route is publicly reachable.

## Phase C3 — Checkout

State: `CODE_READY / PROVIDER_NOT_PROVISIONED`

Provider: Lemon Squeezy.

Product contract:

```text
Prompt Quarry Developer Pack v1
one-time digital purchase
USD $19 launch price
use/adapt/integrate allowed
resale/redistribution/sublicense prohibited
```

Implemented flow:

```text
paid CTA
 -> /api/commerce/developer-pack/checkout
 -> checkout_started
 -> hosted provider checkout
 -> order_created webhook
 -> HMAC-SHA256 signature verification
 -> paid + store/product/variant checks
 -> purchase_completed evidence
```

Provider customer name/email are deliberately excluded from the Prompt Quarry commerce evidence path.

Remaining external configuration:

```text
NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL
LEMONSQUEEZY_WEBHOOK_SECRET
LEMONSQUEEZY_STORE_ID
LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID
LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID
```

## Phase C4 — Analytics

State: `CODE_READY / NOT_LIVE`

Minimum launch chain implemented:

```text
landing_view
free_cta_clicked
free_pack_acquired
paid_product_viewed
paid_cta_clicked
checkout_started
purchase_completed
```

Campaign fields:

```text
source
medium
campaign
content
```

The checkout redirect passes only those fields through Lemon Squeezy custom checkout data. The signed order webhook reconciles them from provider `meta.custom_data`.

An anonymous session id is generated only in browser `sessionStorage` for local diagnostics and is not sent to the payment provider.

Evidence hierarchy remains:

```text
CHECKOUT PROVIDER TRANSACTION
    > signed server/webhook evidence
    > client telemetry
    > button click
```

## Phase C5 — End-to-end launch gate

State: `BLOCKED_EXTERNAL / HARNESS NEXT`

The test journey is:

```text
UTM URL
  -> LANDING
  -> FREE CTA
  -> VERIFIED STARTER PACK ZIP
  -> PAID PRODUCT PAGE
  -> BUY CTA
  -> checkout_started
  -> REAL PROVIDER TEST CHECKOUT
  -> SIGNED order_created WEBHOOK
  -> purchase_completed(test_mode=true)
  -> VERIFY DELIVERY
```

`PQ-LAUNCH-0` is PASS only if this full journey works without access to the private GitHub repository.

A repository smoke harness should automate all public-surface assertions that do not require human/provider UI completion. The real provider test order remains mandatory; a fabricated webhook is not a substitute for it.

## Phase C6 — Distribution

State: `CONTENT_SPEC_READY / NOT_PUBLISHED`

Use `LAUNCH_CONTENT_V1.md` through prodAgentic only after C5 passes.

Start with three pieces:
1. Why Prompt Quarry exists.
2. Code-review prompt before/after structure.
3. Free Starter Pack launch/demo.

Canonical campaign:
`pq-launch-0`

Publish, observe, then continue the sequence.

## Phase C7 — PQ-$1

`PQ-$1` requires:
- a real non-test production transaction;
- real non-zero provider revenue;
- customer receives Developer Pack v1;
- transaction/product version is identifiable.

After PQ-$1, record a milestone receipt/document with:
- date;
- product/version;
- price;
- acquisition source if known;
- transaction evidence reference without exposing sensitive customer/payment details;
- first customer questions/objections.

## Current commit sequence

```text
C1 feat(web)         DONE — premium Next.js commercial surface
C2 release(free)     DONE IN CODE — deterministic Starter Pack artifact + verified route
C3 feat(commerce)    DONE IN CODE — hosted checkout bridge + signed webhook contract
C4 feat(analytics)   DONE IN CODE — minimum funnel semantics + campaign reconciliation
C5 test(launch)      NEXT — public smoke harness; full PASS awaits external provisioning
C6 content(launch)   AFTER C5 — pq-launch-0 execution payload
```

## External provisioning gates

### Vercel

Import `Em3rc0d/prompts` with:

```text
Framework       Next.js
Root Directory  web/
Node            >=20.9.0
```

### Lemon Squeezy

Provision the `$19` one-time Developer Pack v1 product/variant, shareable checkout URL, and webhook targeting:

```text
/api/commerce/lemonsqueezy/webhook
```

Subscribe to `order_created` for the initial one-time purchase flow.

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

## Immediate next repository move

`C5 test(launch): add commercial public-surface smoke harness`

It must validate the deployed landing, Free Pack integrity, paid-page availability, license route, checkout redirect contract, and attribution propagation while preserving the rule that only a real provider test checkout can satisfy the payment portion of `PQ-LAUNCH-0`.
