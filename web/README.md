# Prompt Machine Web

Status: `CUSTOMER EXPERIENCE REFACTOR / BUILD PASS / PUBLIC SALE OFF`

`web/` is the customer-facing Next.js application for **Prompt Machine**.

The internal engineering and certification factory remains **Prompt Quarry**. The frontend should expose customer value, collection discovery, workflow guidance, and compact evidence states without requiring users to understand MK0/MK1/PCP internals.

Canonical product direction: `docs/PRODUCT_VISION_V3.md`.

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

- `/` — outcome-first Prompt Machine landing
- `/collections` — workflow collection discovery
- `/free/developer-starter-pack` — current free developer workflow entry
- `/developer-pack` — current Developer Workflow Collection status; legacy route retained for compatibility
- `/license` — commercial license summary

## Technical delivery routes

- `/api/free-pack/v1` — build-materialized governed free artifact delivery
- `/api/free-pack/v1.1.0` — canonical free artifact release
- `/api/commerce/developer-pack/checkout` — fail-closed provider redirect
- `/api/commerce/lemonsqueezy/webhook` — signed provider evidence endpoint

The route names do not define the customer-facing product architecture.

## Current commercial experiments

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

### Developer Workflow Collection

Customer-facing name:

`Developer Workflow Collection`

Current commercial hypothesis:

```text
collection       developer
candidate        1.2.0-candidate
launch price     USD 19 one-time
public checkout  disabled
```

Historical commerce bindings still use `pq-developer-pack` and the existing `developer-pack` route/API vocabulary. Do not migrate those identifiers casually.

The collection is not for sale until the required behavioral, product, archive, provider, and live-delivery gates close.

## Commerce state machine

| Commerce mode | Public sale | Checkout gate | Accepted webhook event |
|---|---|---|---|
| `off` | any | disabled | none |
| `test` | `NOT_FOR_SALE` | private provider-test token | `provider_test_order_accepted` |
| `test` | `LIVE` | invalid configuration | none |
| `live` | `NOT_FOR_SALE` | private live-canary token | `live_delivery_canary_order_accepted` |
| `live` | `LIVE` | public live checkout | `purchase_completed` |

Only the final state can emit `purchase_completed`.

The public paid CTA is enabled only when:

```text
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=LIVE
```

Configuring test or canary provider data cannot expose checkout through the normal public paid CTA.

## Funnel model

The customer funnel is now:

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
paid intent
        ↓
checkout when enabled
        ↓
repeat usage / expansion
```

Current client telemetry preserves UTM attribution and session identity and distinguishes at least:

- `landing_view`
- `free_product_viewed`
- `free_cta_clicked`
- `collections_viewed`
- `paid_product_viewed`
- `paid_cta_clicked`

These events are instrumentation surfaces, not revenue evidence.

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

Canonical workflow:

`.github/workflows/validate-prompt-machine-web.yml`

It runs:

```text
npm install
npm run typecheck
npm run build
```

The build includes the governed Free Pack materialization and the existing Golden Path postbuild assertion.

A successful build proves that the customer surface compiles and its build-time contracts pass. It does not prove deployment, behavior, purchase demand, or revenue.

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

The frontend may describe versioned artifacts, verified archive integrity, structural validation, candidates, and explicit release status when those facts are evidenced.

It must not claim runtime testing, improvement, certification, portability, purchase completion, or revenue without the corresponding receipts.

`IMPLEMENTED != DEPLOYED` and `not observed == unknown`.
