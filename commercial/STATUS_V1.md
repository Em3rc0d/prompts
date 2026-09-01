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
| C1 Premium Next.js web | `DEPLOYED / OBSERVED` | Existing production surface is live at `https://prompt-quarry.vercel.app` | Current commerce hardening not yet deployed |
| C1.4 Vercel production | `PASS / PRE-HARDENING DEPLOYMENT` | Observed deployment is `READY`; canonical domain assigned | Full current-branch build then controlled deployment |
| C2 Free Starter Pack | `PUBLICLY_DELIVERED / INTEGRITY_VERIFIED` | v1.1.0 ZIP is delivered with canonical size/hash | Observe acquisition separately |
| C3 Developer Pack artifact | `PACKAGING_READY` | 13-asset RC1 built twice from exact blobs; archives byte-identical; exact SHA/size recorded | Provider custody + integration + live delivery canary |
| C3.1 Paid commerce | `HARDENED CONTRACT / PROVIDER_PENDING / NOT_FOR_SALE` | Test, live-canary, and public-live evidence are semantically separated; release identity is bound into checkout/webhook | Full branch build, Lemon Squeezy configuration, controlled provider gates |
| C4 Analytics | `CODE DEPLOYED FOR EXISTING FUNNEL / NEW COMMERCE EVENTS NOT DEPLOYED` | Funnel model exists; provider-test/canary semantics now exist on branch | Deploy after full build; observe provider evidence later |
| C5 Golden Path | `PUBLIC_SURFACE_PASS / PAID_PROVIDER_PENDING` | Public/free path and bounded resilience gates pass | Provider custody + signed test + exact live-canary delivery |
| C6 Distribution | `DRAFTS_READY / HOLD` | Launch material prepared, intentionally unpublished | Provider gate PASS + explicit public-sale decision |
| PQ-LAUNCH-0 | `NOT_ACHIEVED` | Packaging is ready; paid provider proof is not | G1/G2/G3 PASS + public-commerce promotion |
| PQ-$1 | `NOT_ACHIEVED` | No real public non-test purchase claimed | Real public `pq_gate=live` purchase + exact customer delivery evidence |

## C1 — Public surface

Existing observed production contract remains:

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

The observed production deployment predates the latest commerce hardening commits. Branch implementation must not be promoted into deployment evidence.

## C2 — Developer Starter Pack v1.1.0

```text
version            1.1.0
customer_files     7
archive_size       23498 bytes
archive_sha256     55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
delivery_state     PUBLICLY_DELIVERED
integrity_state    VERIFIED
```

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

All 13 customer source files were reconstructed from exact Git blob bytes and verified against their frozen blob SHA and size before execution. Both builds used the canonical builder in isolated clean roots.

Durable evidence:

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

The earlier GitHub Actions run `33295722641` remains an infrastructure incident only: the `build-candidate` job had zero executed steps and produced zero artifacts. It was not used as product evidence.

### Current packaging state

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

`PACKAGING_READY` means the distributable artifact is physically reproducible and fingerprinted. It does not establish behavioral quality, provider custody, customer delivery, or payment readiness.

## C3.1 — Commerce hardening

Canonical provider protocol:

`commercial/LEMONSQUEEZY_PROVIDER_GATE_V1.md`

Current branch implements three mutually distinct commerce gates:

```text
provider_test  -> provider_test_order_accepted
live_canary    -> live_delivery_canary_order_accepted
live           -> purchase_completed
```

Only `live` can emit `purchase_completed`.

Checkout release binding is exact:

```text
pq_product_id       pq-developer-pack
pq_product_version  1.1.0
pq_archive_sha256   546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
pq_archive_size     86763
pq_gate             provider_test | live_canary | live
```

Webhook acceptance requires HMAC signature, `order_created`, paid order state, exact store/product/variant, expected test/live mode, exact release custom data, and the exact expected gate.

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

Legacy single-checkout and allow-test flags are no longer the contract.

### Executed hardening checks

Observed in an isolated local validation harness against the current commerce module graph:

```text
TypeScript isolated typecheck                 PASS
provider file verifier py_compile             PASS
provider file verifier --help                 PASS
provider verifier missing API key fail-closed PASS
webhook adversarial cases                     16 / 16 PASS
```

Adversarial cases included invalid signature, unsupported event, unpaid order, store/product/variant mismatch, test/live mismatch, tampered release hash, missing release metadata, wrong signed gate, invalid mode/gate configuration, malformed JSON, and missing order shape.

This is **not** yet a full repository `npm run typecheck` / `npm run build` receipt. Full current-branch web build remains required before deployment.

## C3.2 — Provider gate

The provider path is intentionally split because Lemon Squeezy Test Mode supports checkout/webhook integration testing but disables file downloads for test purchases.

```text
G0 PACKAGING_READY                PASS
G1 PROVIDER_CUSTODY_PASS          NOT_OBSERVED
G2 PROVIDER_INTEGRATION_PASS      NOT_OBSERVED
G3 LIVE_DELIVERY_CANARY_PASS      NOT_OBSERVED
G4 PUBLIC_COMMERCE_READY          NO
```

### G1 — Provider custody

Use `tools/verify_lemonsqueezy_provider_file.py` to verify product/variant/file metadata and optionally provider-held file bytes against the exact RC1.

Provider API download evidence proves provider custody only; it does not prove customer delivery.

### G2 — Provider integration test

Run test checkout while public sale remains disabled:

```text
DEVELOPER_PACK_COMMERCE_MODE=test
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE
```

Expected signed evidence:

```text
provider_test_order_accepted
```

No customer delivery claim is permitted at this stage.

### G3 — Live delivery canary

Run one controlled live order while public sale remains disabled:

```text
DEVELOPER_PACK_COMMERCE_MODE=live
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE
```

The private canary checkout emits signed gate `live_canary` and accepted evidence:

```text
live_delivery_canary_order_accepted
```

Then verify the actual customer-delivered artifact:

```text
version   1.1.0
bytes     86763
sha256    546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
```

This canary is not `PQ-$1`.

### G4 — Public commerce

Only after G1/G2/G3 are durable PASS may an explicit decision set:

```text
DEVELOPER_PACK_COMMERCE_MODE=live
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=LIVE
```

Only a non-test order bound to `pq_gate=live` may emit `purchase_completed`.

## C4 — Funnel truth

```text
landing_view                         client/session
free_cta_clicked                     client/session
free_pack_acquired                   server after integrity verification
paid_product_viewed                  client/session
paid_cta_clicked                     client/session
provider_test_checkout_started       private controlled redirect
live_delivery_canary_checkout_started private controlled redirect
checkout_started                     public live redirect only
provider_test_order_accepted         signed provider test evidence
live_delivery_canary_order_accepted  signed live-canary evidence
purchase_completed                   signed public-live provider evidence only
```

A CTA click, redirect, page view, test order, canary order, or webhook route presence cannot prove `PQ-$1`.

## C5 — Golden Path

Existing production evidence remains:

```text
PUBLIC SURFACE           PASS
FREE DELIVERY            PASS
FREE INTEGRITY           PASS
ROUTE PRESENCE           PASS
PRODUCTION RESILIENCE    PASS within tested envelope through C200
PAID ARTIFACT READY      PASS
COMMERCE HARDENING       IMPLEMENTED ON BRANCH
FULL CURRENT WEB BUILD   NOT_OBSERVED
PROVIDER CUSTODY         NOT_OBSERVED
SIGNED TEST ORDER        NOT_OBSERVED
LIVE CANARY DELIVERY     NOT_OBSERVED
PUBLIC PAID PURCHASE     NOT_OBSERVED
```

Infrastructure evidence remains distinct from F4–F7 model-behavior evidence.

## C6 — Release sequence

The critical path is now:

```text
PACKAGING_READY
        ↓
full current-branch typecheck/build
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

Do not reopen MK2, redesign the landing, merge PR #2, enable public sale, or alter the product archive while this provider gate is active. Any change to one of the 13 frozen customer blobs invalidates the current archive fingerprint and requires a new release candidate build.

## Evidence boundary

```text
static_maturity       VALID_CANDIDATE
packaging             READY_FOR_PROVIDER_TEST
commerce_contract     HARDENED_ON_BRANCH
full_web_build        NOT_OBSERVED_AFTER_HARDENING
provider_custody      NOT_OBSERVED
provider_test         NOT_OBSERVED
live_delivery_canary  NOT_OBSERVED
F4_TESTED             NO
F5_IMPROVED           NO
F6_CERTIFIED          NO
F7_PORTABLE           NO
real_public_revenue   NOT_OBSERVED
```

`not observed == unknown`

## Next executable gate

Obtain a full current-branch web typecheck/build receipt without deploying public commerce. Once that passes, configure Lemon Squeezy for the exact approved artifact and execute G1 provider custody verification followed by the controlled G2 provider integration test.
