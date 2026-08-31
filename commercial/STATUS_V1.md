# Prompt Quarry Commercial Status v1

Canonical execution snapshot for the path to `PQ-$1`.

Last reconciled: `2026-08-31T03:19Z`

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
| C1 Premium Next.js web | `DEPLOYED / OBSERVED` | Production Next.js surface is live at `https://prompt-quarry.vercel.app`; landing, Free Pack, Developer Pack and license routes return the expected public surfaces | Continue regression observation; no deployment blocker remains |
| C1.4 Vercel production | `PASS` | Vercel project `prompt-quarry` exists; production deployment `dpl_5WxCPP6mTuwe9NCwxa3Wnzh77kvk` is `READY`; canonical domain is assigned | None for public serving |
| C2 Free Starter Pack | `PUBLICLY_DELIVERED / INTEGRITY_VERIFIED` | Versioned and alias routes deliver the canonical v1.1.0 ZIP with exact size and SHA-256 | Observe real user acquisition separately from delivery correctness |
| C3 Paid commerce | `HOLD / NOT_FOR_SALE` | Checkout and webhook routes are deployed and fail closed correctly; Developer Pack v1.1 is RC1, not sellable | Execute RC1 deterministic archive twice, record artifact fingerprint, approve exact artifact, then provision/test provider checkout |
| C4 Analytics | `CODE_DEPLOYED / FUNNEL_EVIDENCE_NOT_OBSERVED` | Client/server event semantics and attribution code are present on the deployed surface | Observe and reconcile real deployed funnel events; provider purchase event requires signed order evidence |
| C5 Golden Path | `PUBLIC_SURFACE_PASS / COMMERCE_HOLD` | Required public routes satisfy the Golden Path contract; Free Pack integrity holds; production resilience receipt is healthy through bounded concurrency 200 | Paid provider test order + signed webhook + exact paid artifact delivery after RC1 READY |
| C6 Distribution | `DRAFTS_READY / HOLD` | Launch material exists but remains intentionally unpublished | Release only after paid artifact + provider flow gates pass |
| PQ-LAUNCH-0 | `NOT_ACHIEVED` | Public/free path is live; paid path is intentionally held | RC1 READY + real provider test order + verified paid delivery |
| PQ-$1 | `NOT_ACHIEVED` | No real non-test paid transaction is claimed | Real non-zero provider revenue + identifiable delivered product/version |

## C1 — Public surface

Framework currently observed in production:

```text
Next.js App Router
Node 24.x on Vercel
production deployment READY
canonical domain prompt-quarry.vercel.app
```

Observed public routes:

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

The paid surface is intentionally explicit:

```text
PAID / v1.1 · DRAFT · NOT FOR SALE
checkout_not_configured
```

A `503` on the checkout route is currently a governed commerce hold, not a deployment defect. A `404` would be a parity failure.

## C2 — Developer Starter Pack v1.1.0

Public delivery identity:

```text
product            Prompt Quarry Developer Starter Pack
version            1.1.0
delivery_state     PUBLICLY_DELIVERED
integrity_state    VERIFIED
archive_file       prompt-quarry-developer-starter-v1.1.0.zip
archive_size       23498 bytes
archive_sha256     sha256:55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
customer_files     7
```

Both the canonical versioned route and `/api/free-pack/v1` alias return the same version, size and SHA-256 headers.

The download route is immutable and exposes:

```text
x-prompt-quarry-version: 1.1.0
x-prompt-quarry-sha256: 55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
x-prompt-quarry-origin: build-materialized-release
```

Public availability does not promote any contained prompt to F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE`.

## C3 — Developer Pack v1.1

Current governed product state:

```text
product                 Prompt Quarry Developer Pack
version                 1.1.0
internal_state          RELEASE_CANDIDATE RC1
sale_status             NOT_FOR_SALE
customer_visible_assets 13
source_fingerprint      sha256:dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
static_maturity         VALID_CANDIDATE
F4_TESTED               NO
F5_IMPROVED             NO
F6_CERTIFIED            NO
F7_PORTABLE             NO
```

RC1 has a frozen customer inventory and deterministic builder contract. The four core systems have manual static Commercial Value Gate evidence at `14/14` each (`56/56` total). That is static product evidence only.

Current packaging blocker:

```text
builder_source             READY
inventory_freeze           PASS
commercial_value_gate      PASS (MANUAL_STATIC)
archive_execution          NOT_OBSERVED
archive_sha256             UNKNOWN
distribution_approval      BLOCKED
READY                      NO
sale_status                NOT_FOR_SALE
```

GitHub Actions has created relevant jobs without assigning/executing steps. A workflow conclusion with zero executed steps is not evidence that the builder failed or passed.

### Exit RC1 -> READY

RC1 may become packaging/commercial `READY` only after:

1. the deterministic builder executes successfully in a clean execution environment;
2. two independent builds produce byte-identical ZIP archives;
3. archive size and SHA-256 are recorded;
4. approval binds to the exact source fingerprint + archive fingerprint;
5. the artifact delivered by the paid path is verified against the approved fingerprint.

`READY` here means packaging/commercial readiness only. It does not grant behavioral maturity labels.

## C3.1 — Checkout/provider contract

Provider design remains Lemon Squeezy.

Current deployed route contract:

```text
paid CTA
  -> /api/commerce/developer-pack/checkout
  -> 503 while sale_status == NOT_FOR_SALE or provider is not configured

future READY state
  -> hosted checkout URL
  -> Lemon Squeezy order_created
  -> HMAC-SHA256 signature verification
  -> status == paid
  -> store/product/variant match
  -> purchase_completed evidence
  -> exact approved Developer Pack delivery
```

A browser click cannot create `purchase_completed` evidence.

Provider configuration remains withheld until the product artifact is physically closed:

```text
NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL
LEMONSQUEEZY_WEBHOOK_SECRET
LEMONSQUEEZY_STORE_ID
LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID
LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID
```

`LEMONSQUEEZY_ALLOW_TEST_MODE` remains `false` by default and is only appropriate for a controlled test flow.

## C4 — Minimum funnel telemetry

Implemented event chain:

```text
landing_view                 client/session
free_cta_clicked             client/session
free_pack_acquired           server, after ZIP integrity verification
paid_product_viewed          client/session
paid_cta_clicked             client/session
checkout_started             server redirect when commerce becomes active
purchase_completed           signed provider webhook only
```

Campaign attribution contract remains:

```text
source
medium
campaign
content
```

Deployment of analytics code is not treated as proof that live funnel events were observed. Real event evidence remains separate.

Revenue truth remains provider-first:

```text
CHECKOUT PROVIDER TRANSACTION
    > signed server/webhook evidence
    > client telemetry
    > button click
```

## C5 — Golden Path and resilience

Canonical contract:

`commercial/GOLDEN_PATH_CONTRACT_V1.json`

Production evidence:

`.ci/golden-path/wave2-production-20260829.json`

The production resilience run observed:

```text
free_pack_materialize   PASS
golden_path_build_parity PASS
required_routes         7
runtime_errors          0
first_break             null
classification          HEALTHY_THROUGH_C200_WITHIN_TESTED_ENVELOPE
```

Bounded Free Pack load phases completed successfully through concurrency `200`, including integrity verification. This establishes infrastructure delivery resilience only inside the tested envelope; it is not a behavioral, payment, or capacity guarantee.

Current Golden Path boundary:

```text
PUBLIC SURFACE           PASS
FREE DELIVERY            PASS
FREE INTEGRITY           PASS
ROUTE PRESENCE           PASS
PRODUCTION RESILIENCE    PASS within tested envelope
PAID ARTIFACT READY      NO
PROVIDER CHECKOUT        HOLD
SIGNED TEST ORDER        NOT_OBSERVED
PAID DELIVERY            NOT_OBSERVED
```

## C6 — Launch package

Prepared distribution assets remain on hold.

Do not publish the paid launch sequence while Developer Pack v1.1 is `NOT_FOR_SALE`.

The release order is now:

```text
RC1 deterministic build
  -> exact archive fingerprint
  -> distribution approval
  -> Developer Pack packaging READY
  -> provision Lemon Squeezy product/variant
  -> controlled provider test checkout
  -> signed order_created webhook
  -> verify exact paid artifact delivery
  -> PQ-LAUNCH-0
  -> publish pq-launch-0 sequence
  -> seek real non-test purchase
  -> PQ-$1
```

## Active blockers

There are two material blockers on the path to launch:

### 1. Developer Pack v1.1 physical release evidence

The frozen RC1 source exists, but deterministic archive execution and artifact fingerprint are still unobserved because the available GitHub Actions runner path has not executed job steps.

Do not substitute CI job creation, Vercel serving health, or static review for this artifact evidence.

### 2. Paid provider proof

Lemon Squeezy provisioning and a controlled provider test order remain undone. This should occur only after the exact paid artifact is packaging/commercial `READY`.

The previous Vercel project-provisioning blocker is closed.

## Next executable gate

Close the paid artifact before commerce:

```bash
python tools/build_developer_pack_v1_1_release_candidate.py
sha256sum dist/prompt-quarry-developer-pack-v1.1.0.zip

# repeat from a clean checkout/environment
python tools/build_developer_pack_v1_1_release_candidate.py
sha256sum dist/prompt-quarry-developer-pack-v1.1.0.zip
```

Acceptance:

```text
run_1 PASS
run_2 PASS
zip_bytes_1 == zip_bytes_2
archive_size recorded
archive_sha256 recorded
source_fingerprint == dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
customer_visible_assets == 13
no customer DRAFT markers
```

After that evidence is durable, provision the provider and execute the payment/delivery gate.

## North star

`PQ-$1` remains intentionally simple:

> At least one real, non-test transaction with non-zero revenue for Developer Pack v1.1, with the delivered product/version identifiable from provider and release evidence.
