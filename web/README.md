# Prompt Quarry Web v0

Status: `PRODUCTION SURFACE DEPLOYED / COMMERCE HARDENING IMPLEMENTED / PROVIDER EVIDENCE PENDING`

Next.js App Router commercial surface for the path to `PQ-LAUNCH-0` and `PQ-$1`.

## Stack

- Next.js 16.3.3 Active LTS
- React 19.2
- TypeScript strict mode
- App Router
- Server Components by default
- CSS native design system
- client component only for commerce CTA telemetry/fail-closed behavior

## Routes

- `/` — commercial landing
- `/free/developer-starter-pack` — Free Pack acquisition page
- `/developer-pack` — paid Developer Pack v1 page
- `/license` — commercial license summary
- `/api/commerce/developer-pack/checkout` — fail-closed provider redirect
- `/api/commerce/lemonsqueezy/webhook` — signed provider evidence endpoint

## Frozen paid release

```text
product_id       pq-developer-pack
version          1.1.0
archive_size     86763
archive_sha256   546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
```

Checkout custom data and accepted webhook evidence must bind to this exact identity.

## Commerce state machine

The web surface separates provider testing, live delivery canary, and public commerce.

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

Configuring a test or canary checkout cannot expose it through the normal public paid CTA.

## Configuration

Copy `.env.example` to `.env.local` for local provider work.

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

Provider-test and live-canary tokens, webhook secret, and provider IDs are server-side configuration. Do not expose secrets through `NEXT_PUBLIC_*` variables.

## Provider protocol

Canonical protocol:

`commercial/LEMONSQUEEZY_PROVIDER_GATE_V1.md`

The important evidence boundary is:

```text
provider test checkout + signed test webhook
        !=
customer delivery
        !=
public purchase
```

Lemon Squeezy Test Mode can validate checkout/webhook integration, but file downloads are disabled for test purchases. Therefore actual customer delivery must be proved by a separate controlled live canary before public sale.

## Local development

```bash
cd web
npm install
npm run dev
```

Production acceptance remains:

```bash
npm run typecheck
npm run build
```

The latest commerce hardening has passed an isolated TypeScript module-graph typecheck and adversarial webhook-contract execution. A full repository `npm run typecheck` + `npm run build` for the current branch remains a required gate before deploying these commerce changes.

## Deployment

`web/` is deployed as the Prompt Quarry public application on Vercel. The currently observed production deployment predates the latest commerce hardening changes; do not treat branch implementation as deployed evidence.

No custom customer account system is required for the current launch path. Lemon Squeezy remains the selected provider for checkout, signed order evidence, and file delivery.

## Boundaries

The surface may state that Developer Pack v1.1 is `PACKAGING_READY` and included assets are statically `VALID_CANDIDATE`. It must not claim F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE` without corresponding behavioral evidence.

`IMPLEMENTED != DEPLOYED` and `not observed == unknown`.
