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
| C5 Launch E2E | `HARNESS_READY / BLOCKED_EXTERNAL` | Public-surface smoke harness validates pages, deterministic Free Pack, checkout redirect, and attribution | Deployed web + provisioned checkout + real provider test order |
| C6 Distribution | `DRAFTS_READY / NOT_PUBLISHED` | Durable `pq-launch-0` payload plus first 3 LinkedIn/prodAgentic assets are ready and held behind C5 | Publish only after C5 passes |
| PQ-LAUNCH-0 | `NOT_ACHIEVED` | — | Full C5 including provider test order + delivery |
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

GitHub Actions jobs for the new web/release/commerce/analytics gates have repeatedly been created with no runner and zero executed steps. This is not treated as a build failure or a pass. Build evidence remains unobserved until a runner or Vercel deployment actually executes it.

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

An anonymous random `session_id` exists only in browser `sessionStorage` for local/session-level diagnostics. It is not transferred to Prompt Quarry server routes or Lemon Squeezy.

Revenue truth remains provider-first:

```text
CHECKOUT PROVIDER TRANSACTION
    > signed server/webhook evidence
    > client telemetry
    > button click
```

## C5 — Public launch smoke harness

Repository harness:

```text
tools/smoke_commercial_launch_v0.py
.github/workflows/smoke-commercial-launch-v0.yml
```

Automated assertions:
- `/` returns the premium Prompt Quarry landing;
- Free Pack page is reachable;
- Developer Pack page is reachable and exposes the `$19` offer;
- license route is reachable;
- `/api/free-pack/v1` returns the exact 11,573-byte ZIP;
- Free Pack SHA-256 equals the canonical release fingerprint;
- ZIP entry list and CRCs are valid;
- paid checkout route redirects over HTTPS;
- configured checkout remains a shareable `/checkout/buy/` URL;
- `source/medium/campaign/content` reach provider custom checkout data.

The harness deliberately cannot satisfy the payment portion of C5. A real Lemon Squeezy test checkout and observed signed `order_created` webhook remain mandatory.

## C6 — Launch package

Prepared but deliberately unpublished:

```text
commercial/campaigns/pq-launch-0/CAMPAIGN.json
commercial/campaigns/pq-launch-0/README.md
commercial/campaigns/pq-launch-0/01-why-prompt-quarry-exists.md
commercial/campaigns/pq-launch-0/02-code-review-before-after.md
commercial/campaigns/pq-launch-0/03-not-observed-unknown.md
```

Each first-release draft has a stable content id, LinkedIn UTM attribution, CTA, and claims review. All are `HOLD_FOR_C5`.

Initial sequence:

```text
P01 Why Prompt Quarry exists
  -> observe
P02 Code Review before/after
  -> observe
P03 not observed == unknown
```

No item should be published until `PQ-LAUNCH-0` is achieved.

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

After Vercel and Lemon Squeezy provisioning, run:

```bash
python tools/smoke_commercial_launch_v0.py \
  --base-url https://<prompt-quarry-preview-or-domain> \
  --expected-checkout-host <checkout-host>
```

Then complete the provider portion manually/in sandbox:

```text
real Lemon Squeezy test checkout
 -> signed order_created webhook
 -> purchase_completed(test_mode=true)
 -> correct paid Pack delivery
```

Only after both automated public-surface smoke and real provider test flow pass should Prompt Quarry be marked `PQ-LAUNCH-0` and `pq-launch-0` distribution begin.

## North star

`PQ-$1` remains intentionally simple:

> At least one real, non-test transaction with non-zero revenue for Developer Pack v1, with the delivered product/version identifiable from provider/release evidence.
