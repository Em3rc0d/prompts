# Prompt Machine — Current Status

Last reconciled: `2026-09-08`

This is the operational entrypoint for the first paid release candidate.

## Current truth sources

1. `commercial/STARTER_CODE_REVIEW_G14_TEST_ORDER_ACCEPTED_2026-09-08.json`
2. `commercial/STARTER_CODE_REVIEW_G14_TEST_CHECKOUT_READY_2026-09-08.json`
3. `commercial/STARTER_CODE_REVIEW_G14_TEST_WEBHOOK_CREATED_2026-09-08.json`
4. `commercial/STARTER_CODE_REVIEW_G14_TEST_PRODUCT_PUBLISHED_2026-09-08.json`
5. `commercial/STARTER_CODE_REVIEW_RELEASE_STATE_G14_PROVIDER_HANDOFF_2026-09-08.json`
6. `commercial/STARTER_CODE_REVIEW_EDITION_RELEASE_PROFILE_RC2_V1.json`
7. `commercial/STARTER_CODE_REVIEW_G12_PACK_REBUILD_RC2_PASS_2026-09-08.json`
8. `commercial/STARTER_CODE_REVIEW_G13_PACK_QA_RC2_PASS_2026-09-08.json`
9. `certification/receipts/starter-code-review-v2.2-g11-certification.json`

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
G14 Provider Gates        TEST INTEGRATION PASS / LIVE CUSTODY + DELIVERY PENDING
```

G09 does not assert cross-model portability. Behavioral evidence remains on `gemini-3.5-flash` only.

G11 certification ID: `PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`.

## G14 Test-mode evidence

Observed across Lemon Squeezy Test mode and Vercel staging:

```text
Test product published                    OBSERVED / PASS
provider file metadata                    OBSERVED / PASS
Test webhook configured                   OBSERVED / PASS
Vercel Test env import                     OBSERVED / PASS
Vercel production-target redeploy         OBSERVED / PASS
private provider-test checkout redirect    OBSERVED / PASS
provider test order                       OBSERVED / PAID TEST ORDER
signed order_created accepted             OBSERVED / PASS
webhook HTTP status                       200
runtime event                             provider_test_order_accepted
order number                              4624191
currency / total                          USD / 900 cents
test_mode                                 true
runtime release                           1.0.0-rc2 / 19,161 bytes / SHA-256 MATCH
```

The accepted event is emitted only after the webhook adapter passes signature verification, expected event shape, store/product/variant identity, paid status, Test-mode boundary and frozen release custom-data checks.

The Test-mode file download returned HTTP 403. Lemon Squeezy disables Test-mode file downloads, so exact provider-held byte custody remains reserved for a later controlled Live canary.

## Provider identity discrepancy

Historical dashboard text earlier exposed product URL id `1347702`. The provider-signed accepted order carried:

```text
store_id    462419
product_id  1347720
variant_id  2105176
```

This conflict is preserved as `UNRESOLVED_SOURCE_DISCREPANCY`; it does not invalidate the accepted Test order because the fail-closed deployed adapter matched the configured provider identity. It **must be reconciled before Live** and the Live store/product/variant IDs must then be frozen.

## Remaining G14 evidence

```text
Test-mode byte download                   UNAVAILABLE BY PROVIDER DESIGN
provider identity discrepancy             MUST RECONCILE BEFORE LIVE
Live provider byte custody                 NOT YET OBSERVED
Live delivery canary                       NOT YET OBSERVED
real purchase                              0
real revenue                               0
```

## Commercial state

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
PQ-$1               NOT OBSERVED
```

G14 Test integration is now closed for the demonstrated Test-mode path. Store activation, Live byte-custody verification, Live delivery canary, and any public-sale decision remain separate later gates.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
