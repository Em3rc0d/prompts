# Prompt Quarry Web v0

Status: `PRODUCTION SURFACE DEPLOYED / COMMERCE_BUILD_READY / PROVIDER EVIDENCE PENDING`

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
- `/api/free-pack/v1` — build-materialized governed Free Pack delivery
- `/api/free-pack/v1.1.0` — canonical Free Pack release
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

Provider-test/live-canary tokens, webhook secret, and provider IDs are server-side. Do not expose them through `NEXT_PUBLIC_*` variables.

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

Lemon Squeezy Test Mode validates integration, not customer file delivery. Actual customer delivery remains a separate controlled live-canary gate before public sale.

## Clean CI acceptance

Validated source/test head:

```text
7d910cfbba537ac62dc8e8186b43282483b37dd0
```

Observed GitHub Actions receipts:

```text
Test Commerce v0        33509477412  PASS
Test Commercial Web v0  33509477240  PASS
npm run typecheck                    PASS
npm run build                        PASS
Free Pack materialization            PASS
Golden Path build parity             PASS
commercial boundary validator        PASS
```

The clean build materialized and verified the Free Pack at exactly:

```text
bytes   23498
sha256  55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
```

Detailed evidence: `commercial/COMMERCE_HARDENING_EVIDENCE_2026-09-01.md`.

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

## Deployment boundary

`web/` is the Prompt Quarry Vercel application. The currently observed production deployment predates the commerce-hardening commits. Therefore:

```text
COMMERCE_BUILD_READY  YES
HARDENING_DEPLOYED    NOT_OBSERVED
PROVIDER_CUSTODY      NOT_OBSERVED
PUBLIC_SALE           NO
```

No production promotion is implied by CI success.

## Boundaries

The surface may state that Developer Pack v1.1 is `PACKAGING_READY` and its included assets are statically `VALID_CANDIDATE`. It must not claim F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE` without corresponding behavioral evidence.

`IMPLEMENTED != DEPLOYED` and `not observed == unknown`.
