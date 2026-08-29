# Prompt Quarry Commercial Status v1

Canonical execution snapshot for the path to `PQ-$1`.

## Truth rules

```text
IMPLEMENTED != DEPLOYED
ARTIFACT_READY != PUBLICLY_AVAILABLE
CHECKOUT_CODE_READY != CHECKOUT_LIVE
CLICK != PURCHASE
SIGNED PAID PROVIDER ORDER = authoritative purchase evidence
not observed == unknown
```

## Current state

| Phase | State | What is true now | Remaining gate |
|---|---|---|---|
| C1 Premium Next.js web | `IMPLEMENTED / VISUALLY_REVIEWED` | Next.js App Router commercial surface, premium visual system, responsive desktop/mobile, evidence-safe copy | Real deployment/build observation |
| C1.4 Vercel preview | `BLOCKED_EXTERNAL` | Vercel account is connected, but Prompt Quarry project is not provisioned and current connector cannot safely import the private repo with `web/` as root | Create/import Vercel project and deploy `web/` |
| C2 Free Starter Pack | `ARTIFACT_READY / NOT_DEPLOYED` | Governed 7-file payload, deterministic ZIP contract, runtime integrity-checked download route | Deploy web so `/api/free-pack/v1` is public |
| C3 Paid commerce | `CODE_READY / PROVIDER_NOT_PROVISIONED` | Lemon Squeezy hosted-checkout abstraction, signed `order_created` webhook verification, paid/store/product/variant checks, no client-side purchase inference | Provision store product/variant, checkout URL, webhook secret/endpoint |
| C4 Analytics | `CODE_READY / NOT_LIVE` | Minimum funnel semantics implemented across client/server, campaign attribution bridge, provider-signed purchase evidence | Observe events on deployed preview/live checkout |
| C5 Launch E2E | `BLOCKED_EXTERNAL` | Smoke path is defined | Requires deployed web + provisioned checkout |
| C6 Distribution | `CONTENT_SPEC_READY / NOT_PUBLISHED` | `pq-launch-0` content system exists | Publish only after C5 passes |
| PQ-LAUNCH-0 | `NOT_ACHIEVED` | — | C5 end-to-end gate |
| PQ-$1 | `NOT_ACHIEVED` | — | Real non-zero provider revenue + delivery |

## C1 — Public surface

Framework:
- Next.js `16.3.3` App Router;
- React `19.2.0`;
- TypeScript strict;
- Server Components by default;
- Geist + Geist Mono;
- premium technical/editorial visual system;
- custom Quarry Engine visual;
- reduced-motion support.

Current routes:

```text
/
/free/developer-starter-pack
/developer-pack
/license
/api/free-pack/v1
/api/commerce/developer-pack/checkout
/api/commerce/lemonsqueezy/webhook
```

GitHub Actions jobs for the new web/release/commerce gates have repeatedly been created with no runner and zero executed steps. This is not treated as a build failure or a pass. Build evidence remains unobserved until a runner or Vercel deployment actually executes it.

## C2 — Developer Starter Pack v1

Customer payload: exactly 7 files.

```text
LICENSE.md
OFFER.md
QUICKSTART.md
README.md
prompts/bug-diagnosis.md
prompts/code-review.md
prompts/technical-decision.md
```

Release identity:

```text
product_id        pq-developer-starter
version           1.0.0
artifact_state    READY
delivery_state    NOT_DEPLOYED
archive_file      prompt-quarry-developer-starter-v1.zip
archive_size      11573 bytes
archive_sha256    sha256:55121028168f9a5394fe79ccc3102caa60e5df85c59a03639dc6e5392e5b2ee1
```

The Python release builder and Node/Next.js ZIP algorithm use the same deterministic archive contract. The download route rebuilds the governed payload and refuses delivery if size or SHA-256 differs from the release manifest.

`ARTIFACT_READY` does not mean the URL is publicly reachable. Public Free Pack acquisition requires deployment of the Next.js app.

## C3 — Developer Pack v1 commerce

Product truth remains:

```text
product            Prompt Quarry Developer Pack v1
version            1.0.0
commercial state   READY
asset maturity     VALID
launch price        USD $19
license             use/adapt/integrate YES; resale/redistribution/sublicense NO
```

Provider choice: Lemon Squeezy.

Code contract:

```text
paid CTA
  -> /api/commerce/developer-pack/checkout
  -> checkout_started server event
  -> hosted checkout URL
  -> Lemon Squeezy order_created
  -> HMAC-SHA256 signature verification
  -> status == paid
  -> store/product/variant match
  -> purchase_completed evidence
```

The webhook evidence path excludes provider customer name/email. A browser click cannot create `purchase_completed`.

Required external configuration before checkout is live:

```text
NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL
LEMONSQUEEZY_WEBHOOK_SECRET
LEMONSQUEEZY_STORE_ID
LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID
LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID
```

`LEMONSQUEEZY_ALLOW_TEST_MODE` remains `false` by default and can be explicitly enabled only for a controlled test environment.

## C4 — Minimum funnel telemetry

Implemented event chain:

```text
landing_view                 client/session
free_cta_clicked             client/session
free_pack_acquired           server, after ZIP integrity verification
paid_product_viewed          client/session
paid_cta_clicked             client/session
checkout_started             server redirect
purchase_completed           signed provider webhook only
```

Campaign attribution:

```text
source
medium
campaign
content
```

These four fields are carried through Lemon Squeezy custom checkout data and reconciled from webhook `meta.custom_data` on a successful signed order.

An anonymous random `session_id` exists only in browser `sessionStorage` for local/session-level diagnostics. It is not transferred to Lemon Squeezy.

Revenue truth remains provider-first:

```text
CHECKOUT PROVIDER TRANSACTION
    > signed server/webhook evidence
    > client telemetry
    > button click
```

## External blockers

There are currently only two blockers that cannot be completed from the repository alone:

### 1. Vercel project provisioning

Create/import Prompt Quarry from `Em3rc0d/prompts` with:

```text
Framework       Next.js
Root Directory  web/
Node            >= 20.9.0
```

Then configure environment variables and obtain a preview URL.

### 2. Lemon Squeezy product provisioning

Create the one-time product/variant for Developer Pack v1 at `USD $19`, obtain its shareable `/checkout/buy/...` URL, configure the webhook endpoint, and populate the store/product/variant/secret values.

No additional product, authentication, dashboard, subscription, CMS, or billing architecture is required before those two gates.

## Next executable gate

Once Vercel and Lemon Squeezy are provisioned, run C5 exactly:

```text
UTM URL
 -> premium landing
 -> Free CTA
 -> verified Starter Pack ZIP
 -> paid product page
 -> Buy CTA
 -> checkout_started
 -> Lemon Squeezy test checkout
 -> signed order_created webhook
 -> purchase_completed(test_mode=true)
 -> verify correct delivery
```

Only after this journey passes should Prompt Quarry be marked `PQ-LAUNCH-0` and `pq-launch-0` distribution begin.

## North star

`PQ-$1` remains intentionally simple:

> At least one real, non-test transaction with non-zero revenue for Developer Pack v1, with the delivered product/version identifiable from provider/release evidence.
