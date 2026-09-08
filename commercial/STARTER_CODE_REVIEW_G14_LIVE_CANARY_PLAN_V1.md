# Prompt Machine Starter — Code Review Edition
## G14 Live Canary Plan v1

Status: `L0 PASS / PRE-LIVE BRAND + STORE ACTIVATION PENDING / LIVE NOT AUTHORIZED`

Date: 2026-09-08

This plan prevents Test-mode success from being promoted into an unbounded Live launch.

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
L0 Test provider identity reconciliation   PASS
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

## L0 — Test identity reconciliation — PASS

Observed canonical Test identity:

```text
store_id             462419
product_id           1347720
variant_id           2105176
provider order_id    9415856
order number         4624191
same-name products   1
historical 1347702   API NOT_FOUND
```

Resolution:

`API Product + Variant + paid Test order agree on the signed provider identity.`

Receipt:

`commercial/STARTER_CODE_REVIEW_G14_TEST_ID_RECONCILIATION_PASS_2026-09-08.json`

Tool:

`tools/pm_g14_lemonsqueezy_id_reconcile.py`

No Test ID may be reused as a Live fallback.

## L0.5 — Customer-facing brand boundary

Required before Live activation/copy is treated as release progress.

The observed Test checkout/order showed `By Prompt Quarry` while the product architecture defines:

```text
Prompt Machine = customer-facing platform/product
Prompt Quarry  = internal workflow mining/certification factory
```

Before buyer-facing Live checkout:

- reconcile the Lemon customer-visible store name/branding with Prompt Machine;
- keep supplier/legal identity truthful and distinct from display-brand decisions;
- do not bypass provider identity/business verification;
- do not expose internal Prompt Quarry terminology to buyers unless explicitly chosen as part of the commercial brand;
- keep storefront/product public visibility OFF unless separately approved.

A custom domain is optional and is not required for the first canary. Branding consistency is required.

## L1 — Store activation

Owner action only. Not authorized by Test success or this plan.

Required:

- complete Lemon Squeezy business questionnaire truthfully;
- complete provider identity verification using the legitimate account/supplier identity;
- comply with any provider eligibility requirements; do not bypass them;
- wait for provider approval.

No public checkout is enabled by Prompt Machine during this stage.

## L2 — Copy RC2 to Live

After activation:

- switch Lemon dashboard to Live mode;
- use `Copy to Live Mode` on the exact Test product;
- confirm one-time price remains USD 9.00;
- confirm public storefront remains disabled unless separately approved;
- confirm exact RC2 file is attached.

Canonical artifact remains:

```text
prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
19,161 bytes
SHA-256 1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
```

## L3 — Freeze Live provider identity

Create a NEW Live API key. Do not reuse the Test key.

Read-only discovery must freeze:

- Live store id;
- Live product id;
- Live variant id;
- Live file id;
- Live checkout identity;
- Live file metadata.

No Test ID is accepted as a fallback.

## L4 — Live provider byte custody — zero-purchase first

Before making any real order, use the Live File API object to retrieve a fresh signed `download_url` and verify:

```text
filename = prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
bytes    = 19,161
sha256   = 1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
```

Prepared read-only operator:

`tools/pm_g14_lemonsqueezy_live_preflight.py`

Hardened exact-byte verifier:

`tools/verify_lemonsqueezy_starter_code_review_file.py`

This proves provider-held byte custody only. It does not prove buyer delivery.

If byte identity fails: `BLOCKED`; no order is allowed.

## L5 — Live webhook + private live-canary gate

Use separate Live values:

- `LEMONSQUEEZY_STARTER_CODE_REVIEW_WEBHOOK_SECRET`;
- Live Store/Product/Variant IDs;
- a new private live-canary gate token;
- `STARTER_CODE_REVIEW_COMMERCE_MODE=live_canary`;
- `NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS=NOT_FOR_SALE`.

Webhook event scope remains bounded to `order_created` for the first canary.

Public checkout stays OFF.

## L6 — Buyer-delivery canary

Only after a separate explicit owner authorization.

Purpose:

- make at most one controlled Live order if still required;
- observe provider-signed `order_created`;
- confirm buyer receives access to the exact RC2 file;
- verify the buyer-facing download produces the exact 19,161-byte / SHA-256 RC2.

This stage may involve a real transaction. It is not authorized by Test completion or by this plan.

A zero-cost path may be evaluated separately, but must not weaken the property being tested or alter the frozen $9 release identity without an explicit experimental classification.

## L7 — G14 Live decision

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

`L0.5 customer-facing brand reconciliation + L1 legitimate store activation`
