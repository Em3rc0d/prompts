# Prompt Quarry Commercial Status v1

Canonical execution snapshot for the path to `PQ-$1`.

Last reconciled: `2026-09-01`

## Truth rules

```text
IMPLEMENTED != DEPLOYED
ARTIFACT_READY != PUBLICLY_AVAILABLE
PACKAGING_READY != PROVIDER_READY
PROVIDER_CUSTODY != CUSTOMER_DELIVERY
CHECKOUT_REDIRECT != PURCHASE
TEST ORDER != REAL REVENUE
LIVE CANARY != PUBLIC REVENUE
SIGNED PAID PROVIDER ORDER != EXACT CUSTOMER DELIVERY
not observed == unknown
```

## Current state

| Phase | State | What is true now | Remaining gate |
|---|---|---|---|
| C1 Premium Next.js web | `DEPLOYED / OBSERVED` | Existing public surface is live at `https://prompt-quarry.vercel.app` | Current commerce hardening not yet deployed |
| C1.4 Current web build | `PASS / CLEAN CI` | Typecheck, production build, Golden Path build parity, and commercial boundaries pass | Preview/runtime observation before production promotion |
| C2 Free Starter Pack | `PUBLICLY_DELIVERED / INTEGRITY_VERIFIED` | v1.1.0 ZIP delivered at canonical size/hash | Acquisition observation separate |
| C3 Developer Pack artifact | `PACKAGING_READY` | 13-asset RC1 built twice from exact blobs; byte-identical | Provider custody + integration + live delivery canary |
| C3.1 Paid commerce | `COMMERCE_BUILD_READY / PROVIDER_PENDING / NOT_FOR_SALE` | Test, canary, and public-live evidence separated; exact release bound into checkout/webhook; CI green | Lemon Squeezy provider gates |
| C4 Analytics | `EXISTING FUNNEL DEPLOYED / NEW COMMERCE EVENTS NOT DEPLOYED` | Provider-test/canary semantics implemented and built | Runtime deployment/observation later |
| C5 Golden Path | `BUILD_PASS / PUBLIC_FREE_PATH_PASS / PAID_PROVIDER_PENDING` | Current branch route parity passes; existing production/free path healthy | Provider custody + signed test + exact live-canary delivery |
| C6 Distribution | `DRAFTS_READY / HOLD` | Launch material prepared and intentionally unpublished | Provider gate PASS + explicit public-sale promotion |
| PQ-LAUNCH-0 | `NOT_ACHIEVED` | Packaging and commerce build are ready; provider proof is not | G1/G2/G3 + public-commerce promotion |
| PQ-$1 | `NOT_ACHIEVED` | No real public non-test purchase claimed | Real `pq_gate=live` purchase + exact customer delivery evidence |

## C1 — Public surface

Existing observed production contract:

```text
/                                      -> 200
/free/developer-starter-pack           -> 200
/developer-pack                         -> 200
/license                                -> 200
/api/free-pack/v1.1.0                  -> 200
/api/free-pack/v1                      -> 200
/api/commerce/developer-pack/checkout  -> 503 expected HOLD
/api/commerce/lemonsqueezy/webhook     -> 405 on GET, route present
```

Observed production deployment:

```text
deployment  dpl_5WxCPP6mTuwe9NCwxa3Wnzh77kvk
state       READY
boundary    predates current commerce hardening
```

Do not promote branch build evidence into production deployment evidence.

## C2 — Developer Starter Pack v1.1.0

```text
version            1.1.0
customer_files     7
archive_size       23498 bytes
archive_sha256     55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
delivery_state     PUBLICLY_DELIVERED
integrity_state    VERIFIED
```

The current clean CI build independently materialized that public artifact and re-verified the same size/hash before compiling the web application.

Public availability does not establish F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE`.

## C3 — Developer Pack v1.1 artifact

Frozen source identity:

```text
product                 Prompt Quarry Developer Pack
version                 1.1.0
customer_visible_assets 13
source_payload_bytes    83879
source_fingerprint      dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
inventory_blob          b287172a94246109d0e33f691f50d6ab5d1ae7aa
builder_blob            4867e3bbd5942667e01d3be62804dc3e0f10e9d1
source_commit           f0accde4aa12ecf4eae530249cb56175e5a28b66
```

Physical build evidence:

```text
build_1 exit            0
build_2 exit            0
byte_identical          YES
receipts_equal          YES
normalizations          8 / 8
archive_size            86763 bytes
archive_sha256          546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
```

Durable packaging evidence:

```text
.ci/developer-pack-v1.1/release-candidate.json
.ci/developer-pack-v1.1/build-evidence.json
.ci/developer-pack-v1.1/packaging-readiness.json
.approvals/developer-pack-v1.1/DISTRIBUTION_APPROVAL.json
```

Builder gates:

```text
inventory_exact                 PASS
blob_identity                   PASS
source_fingerprint              PASS
normalization_exact             PASS
archive_members_exact           PASS
archive_crc                     PASS
customer_draft_markers_absent   PASS
deterministic_rules             PASS
```

The historical GitHub Actions run `33295722641` remains an infrastructure incident: zero product steps executed and zero artifacts produced. It is excluded from release evidence.

### Packaging state

```text
builder_source             PASS / EXACT BLOB
inventory_freeze           PASS / EXACT BLOB
customer_payload           PASS / 13 EXACT BLOBS
commercial_value_gate      PASS (MANUAL_STATIC)
archive_execution          PASS
archive_determinism        PASS
archive_sha256             RECORDED
distribution_approval      APPROVED_FOR_CONTROLLED_PROVIDER_TEST
packaging_ready            YES
provider_custody           NOT_OBSERVED
provider_integration_test  NOT_OBSERVED
live_delivery_canary       NOT_OBSERVED
public_sale                NO
sale_status                NOT_FOR_SALE
```

## C3.1 — Commerce hardening

Canonical provider protocol:

`commercial/LEMONSQUEEZY_PROVIDER_GATE_V1.md`

Current branch implements mutually distinct evidence gates:

```text
provider_test  -> provider_test_order_accepted
live_canary    -> live_delivery_canary_order_accepted
live           -> purchase_completed
```

Only `live` can emit `purchase_completed`.

Exact checkout release binding:

```text
pq_product_id       pq-developer-pack
pq_product_version  1.1.0
pq_archive_sha256   546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
pq_archive_size     86763
pq_gate             provider_test | live_canary | live
```

Webhook acceptance requires valid HMAC signature, `order_created`, paid order status, exact store/product/variant, expected test/live mode, exact release custom data, and exact expected commerce gate.

Fail-closed matrix:

| Commerce mode | Public sale | Gate | Access |
|---|---|---|---|
| `off` | any | none | 503 |
| `test` | `NOT_FOR_SALE` | `provider_test` | private provider-test token |
| `test` | `LIVE` | invalid | fail closed |
| `live` | `NOT_FOR_SALE` | `live_canary` | private live-canary token |
| `live` | `LIVE` | `live` | public checkout |

Current configuration surface:

```text
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS
DEVELOPER_PACK_COMMERCE_MODE
LEMONSQUEEZY_DEVELOPER_PACK_TEST_CHECKOUT_URL
LEMONSQUEEZY_DEVELOPER_PACK_LIVE_CHECKOUT_URL
LEMONSQUEEZY_PROVIDER_TEST_TOKEN
LEMONSQUEEZY_LIVE_CANARY_TOKEN
LEMONSQUEEZY_WEBHOOK_SECRET
LEMONSQUEEZY_STORE_ID
LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID
LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID
```

Legacy single-checkout and allow-test flags are not part of the contract.

### Executed commerce evidence

Local adversarial harness:

```text
TypeScript isolated typecheck                 PASS
provider file verifier py_compile             PASS
provider file verifier --help                 PASS
provider verifier missing API key fail-closed PASS
webhook adversarial cases                     16 / 16 PASS
```

Clean GitHub Actions evidence for source/test head `7d910cfbba537ac62dc8e8186b43282483b37dd0`:

```text
Test Commerce v0       run 33509477412  PASS
Test Commercial Web v0 run 33509477240  PASS
npm run typecheck                         PASS
npm run build                             PASS
Free Pack materialization                 PASS
Golden Path build parity                  PASS
commercial boundaries                     PASS
```

Durable narrative evidence:

`commercial/COMMERCE_HARDENING_EVIDENCE_2026-09-01.md`

## C3.2 — Provider gate

The provider path is deliberately split because test checkout/webhook integration is not customer-delivery evidence.

```text
G0 PACKAGING_READY                PASS
G0.5 COMMERCE_BUILD_READY         PASS
G1 PROVIDER_CUSTODY_PASS          NOT_OBSERVED
G2 PROVIDER_INTEGRATION_PASS      NOT_OBSERVED
G3 LIVE_DELIVERY_CANARY_PASS      NOT_OBSERVED
G4 PUBLIC_COMMERCE_READY          NO
```

### G1 — Provider custody

Use `tools/verify_lemonsqueezy_provider_file.py` to verify product, variant, file metadata, and optionally provider-held file bytes against the exact RC1.

Provider API file verification proves custody only; it does not prove customer delivery.

### G2 — Provider integration test

```text
DEVELOPER_PACK_COMMERCE_MODE=test
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE
```

Expected accepted evidence:

```text
provider_test_order_accepted
```

No customer delivery or revenue claim is allowed at G2.

### G3 — Live delivery canary

```text
DEVELOPER_PACK_COMMERCE_MODE=live
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE
```

Controlled checkout requires the private live-canary token and signs:

```text
pq_gate=live_canary
```

Expected accepted evidence:

```text
live_delivery_canary_order_accepted
```

Then verify the actual customer-delivered artifact:

```text
version   1.1.0
bytes     86763
sha256    546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
```

The canary is not `PQ-$1`.

### G4 — Public commerce

Only after G1/G2/G3 are durable PASS may an explicit release decision set:

```text
DEVELOPER_PACK_COMMERCE_MODE=live
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=LIVE
```

Only a non-test order bound to `pq_gate=live` may emit `purchase_completed`.

## C4 — Funnel truth

```text
landing_view                           client/session
free_cta_clicked                       client/session
free_pack_acquired                     server after integrity verification
paid_product_viewed                    client/session
paid_cta_clicked                       client/session
provider_test_checkout_started         private controlled redirect
live_delivery_canary_checkout_started  private controlled redirect
checkout_started                       public live redirect only
provider_test_order_accepted           signed provider-test evidence
live_delivery_canary_order_accepted    signed live-canary evidence
purchase_completed                     signed public-live provider evidence only
```

No click, redirect, test order, canary order, route presence, or build success can prove `PQ-$1`.

## C5 — Golden Path

```text
PUBLIC SURFACE           PASS on existing production
FREE DELIVERY            PASS
FREE INTEGRITY           PASS
PRODUCTION RESILIENCE    PASS within tested envelope through C200
PAID ARTIFACT READY      PASS
COMMERCE HARDENING       PASS on branch
FULL CURRENT WEB BUILD   PASS
BUILD ROUTE PARITY       PASS
COMMERCIAL BOUNDARIES    PASS
PROVIDER CUSTODY         NOT_OBSERVED
SIGNED TEST ORDER        NOT_OBSERVED
LIVE CANARY DELIVERY     NOT_OBSERVED
PUBLIC PAID PURCHASE     NOT_OBSERVED
```

Infrastructure evidence remains distinct from F4–F7 model-behavior evidence.

## C6 — Release sequence

Critical path now:

```text
PACKAGING_READY
        ↓
COMMERCE_BUILD_READY                 PASS
        ↓
provider configuration
        ↓
PROVIDER_CUSTODY_PASS
        ↓
controlled test checkout
        ↓
signed provider_test_order_accepted
        ↓
PROVIDER_INTEGRATION_PASS
        ↓
controlled live delivery canary
        ↓
signed live_delivery_canary_order_accepted
        ↓
customer download exact hash/size
        ↓
LIVE_DELIVERY_CANARY_PASS
        ↓
explicit public-sale promotion
        ↓
PQ-LAUNCH-0
        ↓
real public non-test purchase
        ↓
exact delivered v1.1.0 artifact
        ↓
PQ-$1
```

Do not reopen MK2, redesign the landing, merge PR #2, enable public sale, or alter the 13 frozen RC1 customer blobs while this provider gate is active.

## Evidence boundary

```text
static_maturity       VALID_CANDIDATE
packaging             READY_FOR_PROVIDER_TEST
commerce_contract     PASS
full_web_build        PASS
provider_custody      NOT_OBSERVED
provider_test         NOT_OBSERVED
live_delivery_canary  NOT_OBSERVED
production_hardening  NOT_DEPLOYED
F4_TESTED             NO
F5_IMPROVED           NO
F6_CERTIFIED          NO
F7_PORTABLE           NO
real_public_revenue   NOT_OBSERVED
```

`not observed == unknown`

## Next executable gate

Audit the connected deployment configuration without changing production, then configure Lemon Squeezy for the exact approved RC1 and execute G1 provider custody verification. Only after custody is exact do we execute the controlled G2 provider integration test.
