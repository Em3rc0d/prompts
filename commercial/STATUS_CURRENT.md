# Prompt Machine / Verlune — Current Status

Last reconciled: `2026-09-08`

This is the operational entrypoint for the first paid release.

## Brand architecture

```text
CUSTOMER-FACING  Verlune
PRODUCT          Verlune Code Review
PRODUCT ENGINE   Prompt Machine
EVIDENCE FACTORY Prompt Quarry
```

`Prompt Machine` and `Prompt Quarry` remain internal engineering identities. Stable machine IDs may retain their historical `pm` / `pq` prefixes for evidence continuity.

## Current truth sources

1. `commercial/VERLUNE_BRAND_ARCHITECTURE_V1.md`
2. `commercial/VERLUNE_CODE_REVIEW_RELEASE_PROFILE_1_0_0_V1.json`
3. `commercial/VERLUNE_CODE_REVIEW_G12_PACK_REBUILD_1_0_0_PASS_2026-09-08.json`
4. `commercial/VERLUNE_CODE_REVIEW_G13_PACK_QA_1_0_0_PASS_2026-09-08.json`
5. `commercial/VERLUNE_G14_LEMON_BRAND_AND_ACTIVATION_SUBMITTED_2026-09-08.json`
6. `commercial/STARTER_CODE_REVIEW_G14_TEST_ID_RECONCILIATION_PASS_2026-09-08.json`
7. `commercial/STARTER_CODE_REVIEW_G14_TEST_ORDER_ACCEPTED_2026-09-08.json`
8. `commercial/STARTER_CODE_REVIEW_G14_LIVE_CANARY_PLAN_V1.md`
9. `certification/receipts/starter-code-review-v2.2-g11-certification.json`

RC1, RC2 and the pre-Live Prompt Machine-branded `1.0.0` package remain historical/superseded evidence only.

## Canonical customer artifact

```text
brand            Verlune
product          Verlune Code Review
version          1.0.0
price            $9 one-time — hypothesis
workflow count   1
archive          verlune-code-review-v1.0.0.zip
bytes            18,859
sha256           4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649
payload fp       46554b5aa36166e6bee7f07b572fa4bece29811270e014cb96381099c87ca430
members          8
Pack QA          77/77 PASS
```

Canonical certified workflow remains unchanged:

```text
workflow_id      pm-starter-evidence-first-code-review-v2
contract         2.2.0
bytes            25,295
sha256           6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
authority        ADVISORY_ONLY
```

The customer ZIP contains Verlune branding and explicitly excludes customer-facing `Prompt Machine`, `Prompt Quarry`, transient launch-state text and release-candidate wording.

## Gate state

```text
G05 Baseline Execution    FAIL / REWORK — historical defect preserved
G06 Failure Mining        CLOSED
G07 Improvement           PASS
G08 Regression            PASS — 4/4 required final cases
G09 Portability           MODEL_SPECIFIC / PASS_FOR_DEMONSTRATED_SCOPE
G10 Human Value Review    KEEP / RECORDED
G11 Certification         PASS_FOR_EXACT_DECLARED_SCOPE
G12 Pack Rebuild          PASS — Verlune 1.0.0
G13 Pack-level QA         PASS — Verlune 1.0.0, 77/77
G14 Provider Gates        HISTORICAL RC2 TEST PATH PASS / VERLUNE TEST PROVIDER VALIDATION PENDING
```

Behavioral evidence remains on `gemini-3.5-flash` only. G09 does not assert cross-model portability.

## Historical G14 Test integration

The provider path was observed end-to-end with the historical RC2 packaging before the final Verlune customer package existed:

```text
Test product published                    PASS
Test webhook configured                   PASS
Vercel env + redeploy                     PASS
private provider-test checkout            PASS
paid Test order                           PASS
provider-signed order_created             PASS
webhook HTTP                              200
runtime event                             provider_test_order_accepted
historical release                        1.0.0-rc2 / 19,161 bytes / historical SHA MATCH
```

This proves the provider integration path, not provider validation of the Verlune archive.

Canonical historical Test provider identity remains:

```text
store_id             462419
product_id           1347720
variant_id           2105176
provider order_id    9415856
order number         4624191
historical 1347702   API NOT_FOUND / SUPERSEDED_NON_CANONICAL_OBSERVATION
```

These Test IDs are not Live identities.

## Current Lemon state — observed

```text
mode                         Test
store_id                     462419
customer-facing store name   Verlune
store logo                   OBSERVED
currency                     USD
activation application       SUBMITTED
identity verification        IN REVIEW
provider approval            NOT YET OBSERVED
Live readiness               NOT YET OBSERVED
```

The store branding observation does not prove that the Test product name or downloadable file has been migrated to Verlune. Store URL and contact email are intentionally not recorded in the evidence receipt.

## Pre-Live frontier

```text
L0    historical Test provider ID reconciliation      PASS
L0.5  Verlune brand architecture                      ADOPTED
      Lemon Test store name + logo                    PASS / OBSERVED
      Lemon Test product rename                       PENDING
L0.75 upload + metadata-revalidate Verlune 1.0.0      PENDING
L1    store activation application                    SUBMITTED
      identity verification                           IN_REVIEW
      provider approval                               PENDING
L2    copy exact Verlune 1.0.0 to Live                PENDING
L3    freeze NEW Live IDs + create Live API key        PENDING
L4    Live provider bytes 18,859 + exact SHA           PENDING
L5    Live webhook/private canary gate                 PENDING
L6    buyer delivery canary if separately authorized   PENDING
```

Prepared tooling is bound to Verlune `1.0.0 / 18,859 / 4d7def...` and remains fail closed.

## Commercial state

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
real revenue        0
PQ-$1               NOT OBSERVED
```

The next legitimate external action is to rename the existing Lemon Test product to `Verlune Code Review`, replace the historical downloadable file with the exact Verlune archive, and then run the read-only Test metadata probe. Provider activation review can proceed independently; no Live claim is made until approval is actually observed.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
