# Prompt Quarry Commercial Status v1

Canonical execution snapshot for the path to `PQ-$1`.

Last reconciled: `2026-08-30T22:49:38-05:00`

## Truth rules

```text
IMPLEMENTED != DEPLOYED
ARTIFACT_READY != PUBLICLY_AVAILABLE
PACKAGING_READY != PROVIDER_READY
CHECKOUT_REDIRECT != PURCHASE
TEST ORDER != REAL REVENUE
SIGNED PAID PROVIDER ORDER = authoritative purchase evidence
not observed == unknown
```

## Current state

| Phase | State | What is true now | Remaining gate |
|---|---|---|---|
| C1 Premium Next.js web | `DEPLOYED / OBSERVED` | Production surface is live at `https://prompt-quarry.vercel.app` | Continue regression observation |
| C1.4 Vercel production | `PASS` | Production deployment is `READY`; canonical domain assigned | None for public serving |
| C2 Free Starter Pack | `PUBLICLY_DELIVERED / INTEGRITY_VERIFIED` | v1.1.0 ZIP is delivered with canonical size/hash | Observe acquisition separately |
| C3 Developer Pack artifact | `PACKAGING_READY` | 13-asset RC1 built twice from exact blobs; archives are byte-identical; exact SHA/size recorded | Provider test + delivered-artifact verification |
| C3.1 Paid commerce | `PROVIDER_TEST_PENDING / NOT_FOR_SALE` | Checkout/webhook routes exist and remain fail-closed | Configure Lemon Squeezy, execute controlled signed test order |
| C4 Analytics | `CODE_DEPLOYED / PURCHASE_EVIDENCE_NOT_OBSERVED` | Funnel event model exists | Observe real provider-backed purchase event later |
| C5 Golden Path | `PUBLIC_SURFACE_PASS / PAID_PROVIDER_PENDING` | Public/free path and bounded resilience gates pass | Provider checkout + signed webhook + exact paid delivery |
| C6 Distribution | `DRAFTS_READY / HOLD` | Launch material prepared, intentionally unpublished | Provider gate PASS + public-sale decision |
| PQ-LAUNCH-0 | `NOT_ACHIEVED` | Packaging is ready; paid provider proof is not | Signed controlled order + exact delivery + launch approval |
| PQ-$1 | `NOT_ACHIEVED` | No real non-test paid transaction claimed | Real non-zero revenue + identifiable delivered v1.1.0 artifact |

## C1 — Public surface

Observed production contract remains:

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

Checkout `503` is still intentional while the provider is not configured and public sale remains disabled.

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
provider_test              PENDING
public_sale                NO
sale_status                NOT_FOR_SALE
```

`PACKAGING_READY` means the distributable artifact is physically reproducible and fingerprinted. It does not establish behavioral quality or payment readiness.

## C3.1 — Provider contract

Provider design remains Lemon Squeezy.

The controlled next gate is:

```text
exact approved ZIP
  -> Lemon Squeezy product/variant
  -> hosted test checkout
  -> order_created
  -> HMAC-SHA256 signature verification
  -> expected store/product/variant
  -> paid/test-mode state according to controlled protocol
  -> purchase evidence receipt
  -> exact artifact delivery
  -> delivered bytes/hash verification
```

Artifact identity that the provider flow must deliver:

```text
version   1.1.0
bytes     86763
sha256    546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
```

Configuration surface remains:

```text
NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL
LEMONSQUEEZY_WEBHOOK_SECRET
LEMONSQUEEZY_STORE_ID
LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID
LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID
LEMONSQUEEZY_ALLOW_TEST_MODE
```

For the controlled provider gate, test mode may be enabled deliberately. Public sale remains off until the test receipt is durable and separately promoted.

## C4 — Funnel truth

```text
landing_view                 client/session
free_cta_clicked             client/session
free_pack_acquired           server after integrity verification
paid_product_viewed          client/session
paid_cta_clicked             client/session
checkout_started             server redirect when configured
purchase_completed           signed provider evidence only
```

A CTA click, redirect, page view, or webhook route presence cannot prove a purchase.

## C5 — Golden Path

Existing production evidence remains:

```text
PUBLIC SURFACE           PASS
FREE DELIVERY            PASS
FREE INTEGRITY           PASS
ROUTE PRESENCE           PASS
PRODUCTION RESILIENCE    PASS within tested envelope through C200
PAID ARTIFACT READY      PASS
PROVIDER CHECKOUT        PENDING
SIGNED TEST ORDER        NOT_OBSERVED
PAID DELIVERY            NOT_OBSERVED
```

Infrastructure evidence remains distinct from F4–F7 model-behavior evidence.

## C6 — Release sequence

The critical path has advanced to:

```text
PACKAGING_READY
        ↓
provider configuration
        ↓
controlled provider test checkout
        ↓
signed order_created webhook
        ↓
exact approved artifact delivery
        ↓
delivery fingerprint verification
        ↓
PROVIDER_GATE_PASS
        ↓
PQ-LAUNCH-0 decision
        ↓
launch distribution
        ↓
real non-test purchase
        ↓
PQ-$1
```

Do not reopen MK2, redesign the landing, or alter the product archive while this provider gate is active. Any change to one of the 13 frozen customer blobs invalidates the current archive fingerprint and requires a new release candidate build.

## Evidence boundary

```text
static_maturity   VALID_CANDIDATE
packaging         READY_FOR_PROVIDER_TEST
F4_TESTED         NO
F5_IMPROVED       NO
F6_CERTIFIED      NO
F7_PORTABLE       NO
provider_test     NOT_OBSERVED
real_revenue      NOT_OBSERVED
```

`not observed == unknown`

## Next executable gate

Configure Lemon Squeezy for the exact approved artifact, then execute one controlled test order and verify both the signed provider event and delivered ZIP fingerprint.
