# Prompt Machine — Current Status

Last reconciled: `2026-09-08`

This is the operational entrypoint for the first paid release candidate.

## Current truth sources

1. `commercial/STARTER_CODE_REVIEW_G14_TEST_ID_RECONCILIATION_PASS_2026-09-08.json`
2. `commercial/STARTER_CODE_REVIEW_G14_TEST_ORDER_ACCEPTED_2026-09-08.json`
3. `commercial/STARTER_CODE_REVIEW_G14_TEST_CHECKOUT_READY_2026-09-08.json`
4. `commercial/STARTER_CODE_REVIEW_G14_TEST_WEBHOOK_CREATED_2026-09-08.json`
5. `commercial/STARTER_CODE_REVIEW_G14_TEST_PRODUCT_PUBLISHED_2026-09-08.json`
6. `commercial/STARTER_CODE_REVIEW_G14_LIVE_CANARY_PLAN_V1.md`
7. `commercial/STARTER_CODE_REVIEW_EDITION_RELEASE_PROFILE_RC2_V1.json`
8. `commercial/STARTER_CODE_REVIEW_G12_PACK_REBUILD_RC2_PASS_2026-09-08.json`
9. `commercial/STARTER_CODE_REVIEW_G13_PACK_QA_RC2_PASS_2026-09-08.json`
10. `certification/receipts/starter-code-review-v2.2-g11-certification.json`

Older release states and RC1 artifacts remain historical evidence only.

## Release candidate

```text
product          Prompt Machine Starter — Code Review Edition
version          1.0.0-rc2
price            $9 one-time — hypothesis
workflow count   1
```

Canonical workflow:

```text
workflow_id      pm-starter-evidence-first-code-review-v2
contract         2.2.0
bytes            25,295
sha256           6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
authority        ADVISORY_ONLY
```

Canonical RC2:

```text
prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
19,161 bytes
SHA-256 1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
8 members
customer license frozen: YES
sale terms frozen: YES
```

## Gate state

```text
G05 Baseline Execution    FAIL / REWORK — historical defect preserved
G06 Failure Mining        CLOSED
G07 Improvement           PASS
G08 Regression            PASS — 4/4 required final cases
G09 Portability           MODEL_SPECIFIC / PASS_FOR_DEMONSTRATED_SCOPE
G10 Human Value Review    KEEP / RECORDED
G11 Certification         PASS_FOR_EXACT_DECLARED_SCOPE
G12 Pack Rebuild          PASS — RC2
G13 Pack-level QA         PASS — RC2, 65/65
G14 Provider Gates        TEST INTEGRATION + TEST ID RECONCILIATION PASS / PRE-LIVE GATES PENDING
```

G09 does not assert cross-model portability. Behavioral evidence remains on `gemini-3.5-flash` only.

G11 certification ID: `PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`.

## G14 Test-mode evidence

Observed across Lemon Squeezy Test mode and Vercel staging:

```text
Test product published                    OBSERVED / PASS
provider file metadata                    OBSERVED / PASS
Test webhook configured                   OBSERVED / PASS
Vercel Test env import                    OBSERVED / PASS
Vercel production-target redeploy         OBSERVED / PASS
private provider-test checkout redirect   OBSERVED / PASS
provider Test order                       OBSERVED / PAID TEST ORDER
signed order_created accepted             OBSERVED / PASS
webhook HTTP status                       200
runtime event                             provider_test_order_accepted
order number                              4624191
currency / total                          USD / 900 cents
test_mode                                 true
runtime release                           1.0.0-rc2 / 19,161 bytes / SHA-256 MATCH
```

Test-mode file downloads are disabled by Lemon Squeezy, so exact provider-held byte custody remains reserved for Live.

## Canonical Test provider identity — reconciled

The read-only Lemon API reconciliation closed the earlier dashboard mismatch:

```text
store_id             462419
product_id           1347720
variant_id           2105176
provider order_id    9415856
order number         4624191
same-name products   1
historical 1347702   API NOT_FOUND / SUPERSEDED_NON_CANONICAL_OBSERVATION
```

The API Product, Variant and paid signed Test order agree on the canonical Test identity. This is now `PASS / PROVIDER_ID_RECONCILIATION`.

These Test IDs are **not** production identities and must never be reused as Live fallbacks. Lemon Test and Live data are separate.

## Pre-Live brand/merchant boundary

The buyer-facing Test checkout/order displayed `By Prompt Quarry`, while the commercial architecture defines:

```text
Prompt Machine = customer-facing product/platform
Prompt Quarry  = internal workflow mining/certification factory
```

Before any Live copy/checkout, the customer-visible Lemon store/merchant branding must be reconciled so buyers are not presented with an internal factory name as the product seller brand unless that is an explicit commercial decision.

This branding gate is separate from legal supplier identity: provider identity/business verification must be completed truthfully and must not be bypassed.

## Remaining G14 evidence

```text
Test integration                         PASS
Test provider ID reconciliation          PASS
customer-facing Lemon branding           MUST RECONCILE BEFORE LIVE
store activation / provider approval     NOT YET OBSERVED
Live product copied/recreated            NOT YET OBSERVED
Live API key                             NOT YET OBSERVED
Live store/product/variant/file IDs       NOT YET OBSERVED
Live provider byte custody               NOT YET OBSERVED
Live delivery canary                     NOT YET OBSERVED
real purchase                            0
real revenue                             0
```

Prepared tooling includes a read-only Live preflight and a hardened exact-byte custody verifier. Public sale remains fail closed.

## Commercial state

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
PQ-$1               NOT OBSERVED
```

G14 Test integration and L0 identity reconciliation are closed. The current frontier is pre-Live branding + legitimate store activation; Live identity/custody/delivery remain separate gates.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
