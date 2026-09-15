# Prompt Machine Web

Status: `CUSTOMER EXPERIENCE IMPLEMENTED / STAGING OBSERVED / PUBLIC SALE OFF`

`web/` is the customer-facing Next.js application for **Prompt Machine**.

The internal engineering and certification factory remains **Prompt Quarry**. The frontend exposes customer value, collection discovery, workflow guidance, and compact evidence states without requiring users to understand MK0/MK1/PCP internals.

Canonical product direction: `docs/PRODUCT_VISION_V3.md`.
Commercial experiment: `commercial/REVENUE_EXPERIMENT_V1.md`.

## Brand boundary

```text
Prompt Machine   customer-facing platform
Prompt Quarry    internal workflow engineering + evidence factory
```

The public experience is organized by **what the customer wants to get done**.

The technical repository, API route names, environment variables, and historical product IDs may retain `pq-*` / `developer-pack` identifiers for compatibility until a separately governed migration is approved. A naming refactor must not silently break delivery or payment bindings.

## Stack

- Next.js 16.3.3 Active LTS
- React 19.2
- TypeScript strict mode
- App Router
- Server Components by default
- native CSS design system
- client components only where telemetry or commerce behavior requires them

## Customer routes

- `/` — outcome-first Prompt Machine landing with `$0 → $9 → $19` ladder
- `/collections` — Starter + Full collection discovery
- `/free/developer-starter-pack` — current free developer workflow entry
- `/starter-collection` — $9 Starter Collection scope/status
- `/developer-pack` — $19 Full Developer Workflow Collection status; legacy route retained for compatibility
- `/learn` — learning/acquisition/trust hub
- `/license` — commercial license summary

## Technical delivery routes

- `/api/free-pack/v1` — build-materialized governed free artifact delivery
- `/api/free-pack/v1.1.0` — canonical free artifact release
- `/api/analytics/intent` — allowlisted server-observed client intent sink
- `/api/commerce/developer-pack/checkout` — fail-closed legacy/full provider redirect
- `/api/commerce/lemonsqueezy/webhook` — signed provider evidence endpoint

The route names do not define the customer-facing product architecture.

## Current commercial ladder

```text
FREE LIBRARY                 USD 0
STARTER COLLECTION           USD 9 one-time   ← primary first paid hypothesis
FULL DEVELOPER COLLECTION    USD 19 one-time  ← broader premium / upsell
SUBSCRIPTION                 DEFERRED
```

Both paid tiers are `PRICE_HYPOTHESIS` and `NOT_FOR_SALE`.

### Free Library

Current concrete free entry:

```text
product_id       pq-developer-starter
version          1.1.0
customer files   7
archive_size     23498
archive_sha256   55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
```

It contains three developer workflows: Code Review, Bug Diagnosis, and Technical Decision.

The free layer is intended to be useful by itself. Delivery integrity does not imply behavioral certification.

### Starter Collection — $9 hypothesis

```text
product_id        pq-developer-starter-collection
candidate         1.2.0-candidate
workflow families 2
skill candidates  2
scope              FROZEN
launch price       USD 9 one-time / PRICE_HYPOTHESIS
public checkout    disabled
sale state         NOT_FOR_SALE
```

Frozen scope:

- Evidence-first Code Review;
- Evidence-first Bug Diagnosis;
- `review-code-with-evidence`;
- `diagnose-bugs-with-evidence`;
- `START_HERE` + task chooser;
- worked examples;
- verification guidance;
- adaptation cheatsheet.

Scope freeze is not runtime/certification evidence.

The Starter CTA currently routes to `/starter-collection` and emits intent only. There is deliberately no public Starter checkout path yet.

### Full Developer Workflow Collection — $19 hypothesis

```text
product_id        pq-developer-pack
candidate         1.2.0-candidate
workflow families 4
skill candidates  4
launch price       USD 19 one-time / PRICE_HYPOTHESIS
public checkout    disabled
```

Historical commerce bindings still use `pq-developer-pack` and the existing `developer-pack` route/API vocabulary. Do not migrate those identifiers casually.

The Full collection is not for sale until the required behavioral, product, archive, provider, and live-delivery gates close. It must earn the upgrade through additional coverage rather than artificial limitations in Starter.

## Commerce state machine

The existing provider state machine applies to the governed legacy/full commerce path while the Starter provider path remains intentionally unimplemented.

| Commerce mode | Public sale | Checkout gate | Accepted webhook event |
|---|---|---|---|
| `off` | any | disabled | none |
| `test` | `NOT_FOR_SALE` | private provider-test token | `provider_test_order_accepted` |
| `test` | `LIVE` | invalid configuration | none |
| `live` | `NOT_FOR_SALE` | private live-canary token | `live_delivery_canary_order_accepted` |
| `live` | `LIVE` | public live checkout | `purchase_completed` |

Only the final state can emit `purchase_completed`.

The public Full paid CTA is enabled only when:

```text
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=LIVE
```

Configuring test or canary provider data cannot expose checkout through the normal public paid CTA.

## Funnel model

```text
content / search / social
        ↓
home
        ↓
free workflow / outcome discovery
        ↓
activation on a real task
        ↓
collections
        ↓
Starter view / intent
        ↓
$9 purchase when eventually enabled
        ↓
Full view / intent
        ↓
$19 upgrade when broader value is needed
```

Client intent telemetry distinguishes:

- `landing_view`
- `free_product_viewed`
- `free_cta_clicked`
- `collections_viewed`
- `starter_product_viewed`
- `starter_cta_clicked`
- `paid_product_viewed`
- `paid_cta_clicked`

These events are **UNTRUSTED_CLIENT_INTENT**, not revenue evidence.

The same-origin server sink is:

`POST /api/analytics/intent`

Runtime logs use:

```text
PM_INTENT_EVENT
schema         prompt-machine-intent-v1
evidence_class UNTRUSTED_CLIENT_INTENT
```

A synthetic staging `landing_view` has been observed end-to-end with HTTP 202 and runtime log evidence. That proves the observability path works; it does not prove customer demand.

The browser-local anonymous `pq:session-id` remains browser-session-only and is not sent to the intent sink.

## Configuration

```text
NEXT_PUBLIC_FREE_PACK_URL=
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE
NEXT_PUBLIC_ANALYTICS_MODE=off

DEVELOPER_PACK_COMMERCE_MODE=off

LEMONSQUEEZY_DEVELOPER_PACK_TEST_CHECKOUT_URL=
LEMONSQUEEZY_DEVELOPER_PACK_LIVE_CHECKOUT_URL=
LEMONSQUEEZY_PROVIDER_TEST_TOKEN=
LEMONSQUEEZY_LIVE_CANARY_TOKEN=
LEMONSQUEEZY_WEBHOOK_SECRET=
LEMONSQUEEZY_STORE_ID=
LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID=
LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID=
```

Provider-test/live-canary tokens, webhook secrets, and provider IDs are server-side. Do not expose them through `NEXT_PUBLIC_*` variables.

## Provider protocol

Canonical protocol:

`commercial/LEMONSQUEEZY_PROVIDER_GATE_V1.md`

```text
provider test checkout + signed test webhook
        !=
customer delivery
        !=
public purchase
```

Provider Test Mode validates integration, not customer file delivery. Actual customer delivery remains a separate controlled live-canary gate before public sale.

## Web validation

Canonical build validation:

`.github/workflows/validate-prompt-machine-web.yml`

Isolated staging deployment:

`.github/workflows/deploy-prompt-machine-staging.yml`

The staging workflow is hard-bound to the Vercel `prompt-quarry-stage` project. It verifies the project identity before deployment, typechecks the app, deploys, verifies the Prompt Machine title/hero on the canonical alias, then emits a synthetic intent event and requires HTTP 202.

It never targets the separate public `prompt-quarry` production project.

The production build includes governed Free Pack materialization and Golden Path route assertion, including `/starter-collection`.

A successful build proves that the customer surface compiles and its build-time contracts pass. A successful staging smoke proves the deployed staging route/intent path was observed. Neither proves behavioral workflow quality, purchase demand, or revenue.

## Local development

```bash
cd web
npm install
npm run dev
```

Production acceptance:

```bash
npm run typecheck
npm run build
```

## Evidence boundary

Customer-facing copy follows:

```text
MARKETING CLAIM <= OBSERVED EVIDENCE
```

The frontend may describe versioned artifacts, verified archive integrity, structural validation, frozen scope, candidates, and explicit release status when those facts are evidenced.

It must not claim runtime workflow testing, improvement, certification, portability, purchase completion, or revenue without the corresponding receipts.

```text
SCOPE FROZEN != BEHAVIOR PROVEN
IMPLEMENTED != DEPLOYED
INTENT != PURCHASE
NOT OBSERVED == UNKNOWN
```
