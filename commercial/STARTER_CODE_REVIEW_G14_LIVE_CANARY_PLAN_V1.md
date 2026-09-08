# Prompt Machine Starter — Code Review Edition
## G14 Live Canary Plan v1

Status: `PREPARED / NOT AUTHORIZED`

Date: 2026-09-08

This plan exists to prevent Test-mode success from being promoted into an unbounded Live launch.

Master invariant:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Already observed

```text
G14 Test product published                 PASS
G14 Test provider metadata                 PASS
G14 Test webhook                           PASS
G14 Test private checkout                  PASS
G14 Test order                             PASS
G14 Test signed order_created acceptance   PASS
real purchase                              0
real revenue                               0
```

The Test integration is complete. It does not prove Live provider byte custody, Live buyer delivery, a real purchase, or readiness to sell.

## Provider separation invariant

Lemon Squeezy Test mode and Live mode are separate provider data sets. Test products and IDs are not production identities.

Therefore:

```text
Test store/product/variant/file ids  MUST NOT be copied into Live config
Test API key                         MUST NOT be used for Live
Test webhook secret                  MUST NOT be used for Live
Test checkout URL                    MUST NOT be used for Live
```

The Live product must be copied/recreated in Live mode after store activation, then its Live Store/Product/Variant/File identities must be discovered and frozen independently.

## Canary stages

### L0 — Test identity reconciliation

Required before any Live setup:

- reconcile signed Test order ID `9415856`
- reconcile order #`4624191`
- reconcile canonical Test product/variant through the Lemon API
- resolve historical dashboard URL product-id observation `1347702`
- persist no customer PII

Tool:

`tools/pm_g14_lemonsqueezy_id_reconcile.py`

Expected result:

`PASS / PROVIDER_ID_RECONCILIATION`

### L1 — Store activation

Owner action only. Not authorized by this plan.

Required:

- complete Lemon Squeezy business questionnaire truthfully
- complete provider identity verification
- wait for provider approval

No public checkout is enabled by Prompt Machine during this stage.

### L2 — Copy RC2 to Live

After activation:

- switch Lemon dashboard to Live mode
- use `Copy to Live Mode` on the exact Test product
- confirm one-time price remains USD 9.00
- confirm public storefront remains disabled unless separately approved
- confirm exact RC2 file is attached

Canonical artifact remains:

```text
prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
19,161 bytes
SHA-256 1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
```

### L3 — Freeze Live provider identity

Create a NEW Live API key. Do not reuse the Test key.

Read-only discovery must freeze:

- Live store id
- Live product id
- Live variant id
- Live file id
- Live checkout identity
- Live file metadata

No Test ID is accepted as a fallback.

### L4 — Live provider byte custody — zero-purchase first

Before making any real order, use the Live File API object to retrieve a fresh signed `download_url` and verify:

```text
filename = prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
bytes    = 19,161
sha256   = 1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
```

This proves provider-held byte custody only. It does not prove buyer delivery.

If byte identity fails: `BLOCKED`; no order is allowed.

### L5 — Live webhook + private live-canary gate

Use separate Live values:

- `LEMONSQUEEZY_STARTER_CODE_REVIEW_WEBHOOK_SECRET`
- Live Store/Product/Variant IDs
- a new private live-canary gate token
- `STARTER_CODE_REVIEW_COMMERCE_MODE=live_canary`
- `NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS=NOT_FOR_SALE`

Webhook event scope remains bounded to `order_created` for the first canary.

Public checkout stays OFF.

### L6 — Buyer-delivery canary

Only after a separate explicit owner authorization.

Purpose:

- make at most one controlled Live order if still required
- observe provider-signed `order_created`
- confirm buyer receives access to the exact RC2 file
- verify the buyer-facing download produces the exact 19,161-byte / SHA-256 RC2

This stage may involve a real transaction. It is not authorized by Test completion or by this plan.

A zero-cost path may be evaluated separately, but must not weaken the property being tested or alter the frozen $9 release identity without an explicit experimental classification.

### L7 — G14 Live decision

Only after L0-L6 evidence is reviewed:

```text
G14_LIVE_PASS       yes/no
PRODUCT_READY       yes/no
READY_TO_SELL       yes/no
PUBLIC_CHECKOUT     still separate explicit decision
```

No stage automatically enables public sales.

## Fail-closed boundaries

```text
Test integration PASS     != Live custody
Live custody PASS         != buyer delivery
buyer delivery PASS       != customer value
real canary order         != PQ-$1 unless it is a genuine non-test customer purchase
PRODUCT_READY             != READY_TO_SELL
READY_TO_SELL             != PUBLIC_CHECKOUT ON
```

## Current frontier

`L0 — Test identity reconciliation`
