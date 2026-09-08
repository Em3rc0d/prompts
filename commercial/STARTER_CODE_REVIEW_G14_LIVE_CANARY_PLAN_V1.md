# Prompt Machine Starter — Code Review Edition
## G14 Live Canary Plan v1

Status: `FINAL 1.0.0 FROZEN / L0 PASS / PRE-LIVE BRAND + STORE ACTIVATION PENDING / LIVE NOT AUTHORIZED`

Date: 2026-09-08

This plan prevents Test-mode success from being promoted into an unbounded Live launch.

Master invariant:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Final customer artifact

The release candidate packaging was superseded before Live because its customer surface contained transient launch-state text. The final customer artifact is now frozen and independently QA'd:

```text
prompt-machine-starter-code-review-edition-v1.0.0.zip
18,955 bytes
SHA-256 9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3
8 members
Pack QA 67/67 PASS
```

The certified workflow inside remains byte-identical:

```text
WORKFLOW.md bytes   25,295
WORKFLOW.md SHA-256 6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
```

RC2 is historical Test-integration evidence only and must not be copied to Live or sold.

## Already observed

```text
G14 Test product published                 PASS — RC2 historical integration evidence
G14 Test provider metadata                 PASS — RC2 historical integration evidence
G14 Test webhook                           PASS
G14 Test private checkout                  PASS
G14 Test order                             PASS
G14 Test signed order_created acceptance   PASS
L0 Test provider identity reconciliation   PASS
Final 1.0.0 deterministic rebuild          PASS
Final 1.0.0 pack QA                        PASS — 67/67
real purchase                              0
real revenue                               0
```

The Test integration proves the provider path works, but the exact final `1.0.0` archive still requires provider revalidation before Live.

## Provider separation invariant

Lemon Squeezy Test mode and Live mode are separate provider data sets. Test products and IDs are not production identities.

Therefore:

```text
Test store/product/variant/file ids  MUST NOT be copied into Live config
Test API key                         MUST NOT be used for Live
Test webhook secret                  MUST NOT be used for Live
Test checkout URL                    MUST NOT be used for Live
RC2 file identity                    MUST NOT be used as Live release identity
```

## L0 — Test identity reconciliation — PASS

Canonical historical Test identity:

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
- keep storefront/product public visibility OFF unless separately approved.

A custom domain is optional. Branding consistency is required.

## L0.75 — Final Test artifact revalidation

Before using the Test product as the source for `Copy to Live Mode`, replace the historical RC2 file with the exact final `1.0.0` archive and run the read-only Test metadata probe.

Expected Test artifact:

```text
filename  prompt-machine-starter-code-review-edition-v1.0.0.zip
bytes     18,955
sha256    9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3
price     USD 9.00 one-time
```

Because Lemon disables Test-mode file downloads, this stage can prove final Test metadata but not byte custody. A second Test purchase is optional evidence and is not automatically required solely to establish Live custody.

## L1 — Store activation

Owner action only. Not authorized by Test success or this plan.

Required:

- complete Lemon Squeezy business questionnaire truthfully;
- complete provider identity verification using the legitimate account/supplier identity;
- comply with provider eligibility requirements; do not bypass them;
- wait for provider approval.

No public checkout is enabled by Prompt Machine during this stage.

## L2 — Copy final 1.0.0 to Live

After activation and final Test artifact revalidation:

- switch Lemon dashboard to Live mode;
- use `Copy to Live Mode` on the exact final Test product;
- confirm one-time price remains USD 9.00;
- confirm public storefront remains disabled unless separately approved;
- confirm the final `1.0.0` file is attached.

Canonical artifact:

```text
prompt-machine-starter-code-review-edition-v1.0.0.zip
18,955 bytes
SHA-256 9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3
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
filename = prompt-machine-starter-code-review-edition-v1.0.0.zip
bytes    = 18,955
sha256   = 9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3
```

Prepared read-only operator:

`tools/pm_g14_lemonsqueezy_live_preflight.py`

Hardened exact-byte verifier:

`tools/verify_lemonsqueezy_starter_code_review_file.py`

This proves provider-held byte custody only. It does not prove buyer delivery.

If byte identity fails: `BLOCKED`; no order is allowed.

## L5 — Live webhook + private live-canary gate

Use separate Live values:

- a new Live webhook secret;
- Live Store/Product/Variant IDs;
- a new private live-canary gate token;
- `STARTER_CODE_REVIEW_COMMERCE_MODE=live_canary`;
- `NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS=NOT_FOR_SALE`.

Webhook event scope remains bounded to `order_created` for the first canary. Public checkout stays OFF.

## L6 — Buyer-delivery canary

Only after a separate explicit owner authorization.

Purpose:

- make at most one controlled Live order if still required;
- observe provider-signed `order_created`;
- confirm buyer receives access to the exact final `1.0.0` file;
- verify the buyer-facing download produces exactly 18,955 bytes and the canonical SHA-256.

This stage may involve a real transaction. It is not authorized by Test completion or by this plan.

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
historical RC2 Test PASS  != final 1.0.0 provider validation
Test metadata PASS        != Live custody
Live custody PASS         != buyer delivery
buyer delivery PASS       != customer value
real canary order         != PQ-$1 unless it is a genuine non-test customer purchase
PRODUCT_READY             != READY_TO_SELL
READY_TO_SELL             != PUBLIC_CHECKOUT ON
```

## Current frontier

`L0.5 customer-facing brand reconciliation + L0.75 final Test artifact upload/revalidation + L1 legitimate store activation`
