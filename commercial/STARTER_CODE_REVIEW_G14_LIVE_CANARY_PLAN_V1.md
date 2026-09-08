# Verlune Code Review
## G14 Live Canary Plan v1

Status: `VERLUNE 1.0.0 FROZEN / BRAND ADOPTED / LEMON TEST REBRAND + FILE REVALIDATION PENDING / LIVE NOT AUTHORIZED`

Date: 2026-09-08

This plan prevents historical Test-mode success from being promoted into an unbounded Live launch.

Master invariant:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Brand architecture

```text
Verlune        customer-facing masterbrand
Prompt Machine internal product/release engine
Prompt Quarry  internal evidence/certification factory
```

Stable `pm` / `pq` machine IDs may remain for evidence continuity. Buyer-facing product copy, packaging, store name and product name use Verlune.

## Canonical customer artifact

```text
product     Verlune Code Review
version     1.0.0
archive     verlune-code-review-v1.0.0.zip
bytes       18,859
SHA-256     4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649
payload fp  46554b5aa36166e6bee7f07b572fa4bece29811270e014cb96381099c87ca430
members     8
Pack QA     77/77 PASS
```

The certified workflow inside remains byte-identical:

```text
WORKFLOW.md bytes   25,295
WORKFLOW.md SHA-256 6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
```

RC1, RC2 and the pre-Live Prompt Machine-branded final package are historical/superseded packaging evidence only. None may be copied to Live or sold as Verlune Code Review.

## Already observed

```text
G14 historical Test product published                 PASS — RC2 evidence
G14 historical Test provider metadata                 PASS — RC2 evidence
G14 Test webhook                                      PASS
G14 Test private checkout                             PASS
G14 Test order                                        PASS
G14 Test signed order_created acceptance              PASS
L0 Test provider identity reconciliation              PASS
Verlune 1.0.0 deterministic rebuild                   PASS
Verlune 1.0.0 Pack QA                                 PASS — 77/77
real purchase                                         0
real revenue                                          0
```

Historical Test success proves the integration path, not provider validation of the new Verlune package.

## Provider separation invariant

Lemon Squeezy Test and Live are separate provider data sets. Therefore:

```text
Test IDs / API key / checkout URL       MUST NOT be Live fallbacks
historical RC2 archive identity          MUST NOT be Live release identity
pre-brand Prompt Machine archive         MUST NOT be Live release identity
Verlune archive identity                 MUST match exact frozen bytes before Live
```

## L0 — Historical Test identity reconciliation — PASS

```text
store_id             462419
product_id           1347720
variant_id           2105176
provider order_id    9415856
order number         4624191
historical 1347702   API NOT_FOUND
```

Receipt:

`commercial/STARTER_CODE_REVIEW_G14_TEST_ID_RECONCILIATION_PASS_2026-09-08.json`

No Test ID may be reused as a Live fallback.

## L0.5 — Customer-facing brand — ADOPTED / PROVIDER UPDATE PENDING

Brand decision is frozen in:

`commercial/VERLUNE_BRAND_ARCHITECTURE_V1.md`

Required Lemon Test state before further release progress:

```text
Store name    Verlune
Product name  Verlune Code Review
Price         USD 9.00 one-time
```

The internal webhook hostname may remain `prompt-quarry-stage.vercel.app`; it is infrastructure, not buyer-facing branding.

Legal/supplier identity must remain truthful and distinct from display-brand decisions. Provider verification must not be bypassed.

## L0.75 — Verlune Test artifact revalidation

Replace the historical downloadable file with the exact Verlune package and run the read-only Test metadata probe.

Expected:

```text
filename  verlune-code-review-v1.0.0.zip
bytes     18,859
sha256    4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649
price     USD 9.00 one-time
store     Verlune
product   Verlune Code Review
```

Prepared probe:

`tools/pm_g14_lemonsqueezy_probe.py`

The probe anchors Test discovery to canonical store id `462419` and then requires the visible store name to be `Verlune`. It has no provider side effects.

Because Lemon disables Test-mode file downloads, this stage proves metadata, not byte custody. A second Test purchase is not automatically required merely to establish Live custody.

## L1 — Store activation

Owner/provider action only. Not authorized by historical Test success or this plan.

Required:

- complete business details truthfully;
- complete identity/business verification using legitimate information;
- comply with provider eligibility requirements;
- wait for provider approval.

Public checkout remains separately gated.

## L2 — Copy exact Verlune product to Live

Only after L0.75 and store approval:

- switch Lemon to Live mode;
- copy/recreate `Verlune Code Review` in Live;
- retain USD 9.00 one-time price;
- attach exact `verlune-code-review-v1.0.0.zip`;
- keep public storefront/checkout OFF unless separately approved.

## L3 — Freeze NEW Live provider identity

Create a NEW Live API key. Read-only discovery must freeze:

- Live store id;
- Live product id;
- Live variant id;
- Live file id;
- Live checkout identity;
- Live file metadata.

No Test ID is accepted as fallback.

## L4 — Live provider byte custody — zero-purchase first

Before any real order, retrieve a fresh signed Live `download_url` and verify:

```text
filename = verlune-code-review-v1.0.0.zip
bytes    = 18,859
sha256   = 4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649
```

Prepared tooling:

- `tools/pm_g14_lemonsqueezy_live_preflight.py`
- `tools/verify_lemonsqueezy_starter_code_review_file.py`

This proves provider-held byte custody only. It does not prove buyer delivery.

## L5 — Live webhook + private canary gate

Use separate Live values and keep:

```text
STARTER_CODE_REVIEW_COMMERCE_MODE=live_canary
NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS=NOT_FOR_SALE
```

Use a new Live webhook secret, Live Store/Product/Variant IDs and a new private live-canary token. Webhook scope remains `order_created` for the first canary.

## L6 — Buyer-delivery canary

Only after separate explicit owner authorization.

Purpose:

- at most one controlled Live order if still required;
- observe provider-signed `order_created`;
- confirm buyer access to exact Verlune `1.0.0`;
- verify buyer-facing download is exactly 18,859 bytes with the canonical SHA-256.

This stage may involve a real transaction and is not implicitly authorized.

## L7 — G14 Live decision

Only after L0-L6 evidence is reviewed:

```text
G14_LIVE_PASS       yes/no
PRODUCT_READY       yes/no
READY_TO_SELL       yes/no
PUBLIC_CHECKOUT     separate explicit decision
```

## Fail-closed boundaries

```text
historical RC2 Test PASS  != Verlune provider validation
Test metadata PASS        != Live custody
Live custody PASS         != buyer delivery
buyer delivery PASS       != customer value
real canary order         != PQ-$1 unless genuine non-test customer purchase
PRODUCT_READY             != READY_TO_SELL
READY_TO_SELL             != PUBLIC_CHECKOUT ON
```

## Current frontier

`L0.5 Lemon Test rename to Verlune + L0.75 exact Verlune Test file upload/revalidation`
