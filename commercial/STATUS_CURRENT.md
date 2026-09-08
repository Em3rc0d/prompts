# Prompt Machine — Current Status

Last reconciled: `2026-09-08`

This is the operational entrypoint for the first paid release.

## Current truth sources

1. `commercial/STARTER_CODE_REVIEW_EDITION_RELEASE_PROFILE_1_0_0_V1.json`
2. `commercial/STARTER_CODE_REVIEW_G12_PACK_REBUILD_1_0_0_PASS_2026-09-08.json`
3. `commercial/STARTER_CODE_REVIEW_G13_PACK_QA_1_0_0_PASS_2026-09-08.json`
4. `commercial/STARTER_CODE_REVIEW_G14_TEST_ID_RECONCILIATION_PASS_2026-09-08.json`
5. `commercial/STARTER_CODE_REVIEW_G14_TEST_ORDER_ACCEPTED_2026-09-08.json`
6. `commercial/STARTER_CODE_REVIEW_G14_LIVE_CANARY_PLAN_V1.md`
7. `certification/receipts/starter-code-review-v2.2-g11-certification.json`

RC1/RC2 release-candidate artifacts and their provider receipts remain historical evidence only.

## Final customer artifact

```text
product          Prompt Machine Starter — Code Review Edition
version          1.0.0
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

Canonical final archive:

```text
prompt-machine-starter-code-review-edition-v1.0.0.zip
18,955 bytes
SHA-256 9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3
payload fingerprint 9cb12bc7a950e9d36e4069a58d08fa86e5e3285ed5f74e5ffa78a931ed3c1975
8 members
customer license frozen: YES
sale terms frozen: YES
```

Final pack QA: `67/67 PASS`.

The final customer ZIP explicitly excludes transient launch state, release-candidate wording, and internal `Prompt Quarry` branding. The certified `WORKFLOW.md` bytes did not change.

## Gate state

```text
G05 Baseline Execution    FAIL / REWORK — historical defect preserved
G06 Failure Mining        CLOSED
G07 Improvement           PASS
G08 Regression            PASS — 4/4 required final cases
G09 Portability           MODEL_SPECIFIC / PASS_FOR_DEMONSTRATED_SCOPE
G10 Human Value Review    KEEP / RECORDED
G11 Certification         PASS_FOR_EXACT_DECLARED_SCOPE
G12 Pack Rebuild          PASS — final 1.0.0
G13 Pack-level QA         PASS — final 1.0.0, 67/67
G14 Provider Gates        HISTORICAL RC2 TEST INTEGRATION PASS / FINAL 1.0.0 PROVIDER VALIDATION PENDING
```

G09 does not assert cross-model portability. Behavioral evidence remains on `gemini-3.5-flash` only.

G11 certification ID: `PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`.

## Historical G14 Test integration evidence

The provider path was observed end-to-end using RC2 before the customer package was promoted to the final `1.0.0` packaging layer:

```text
Test product published                    PASS
Test webhook configured                   PASS
Vercel env + redeploy                     PASS
private provider-test checkout            PASS
paid Test order                           PASS
provider-signed order_created             PASS
webhook HTTP                              200
runtime event                             provider_test_order_accepted
historical runtime release                1.0.0-rc2 / 19,161 bytes / historical SHA MATCH
```

This demonstrates the provider integration path, not provider validation of the final archive. RC2 must not be copied to Live or sold.

## Canonical historical Test provider identity — reconciled

```text
store_id             462419
product_id           1347720
variant_id           2105176
provider order_id    9415856
order number         4624191
same-name products   1
historical 1347702   API NOT_FOUND / SUPERSEDED_NON_CANONICAL_OBSERVATION
```

These Test IDs are not Live identities and must never be reused as production fallbacks.

## Pre-Live boundaries

The current frontier is deliberately split:

```text
L0.5  customer-facing Lemon branding                PENDING
L0.75 upload/revalidate exact final 1.0.0 in Test    PENDING
L1    legitimate store activation/provider approval  PENDING
L2    copy exact final 1.0.0 to Live                 PENDING
L3    freeze NEW Live IDs + Live API key             PENDING
L4    Live provider bytes 18,955 + SHA exact          PENDING
L5    Live webhook/private canary gate                PENDING
L6    buyer delivery canary if separately authorized  PENDING
```

The Test checkout showed `By Prompt Quarry`; before buyer-facing Live checkout, customer-visible branding must be reconciled with the Prompt Machine customer-facing product strategy. Legal/supplier identity and provider verification remain truthful and separate; no bypass is allowed.

Prepared tooling is bound to final `1.0.0` and remains fail closed:

- `tools/pm_operator.py`
- `tools/pm_g14_lemonsqueezy_probe.py`
- `tools/pm_g14_lemonsqueezy_test_setup.py`
- `tools/pm_g14_lemonsqueezy_live_preflight.py`
- `tools/verify_lemonsqueezy_starter_code_review_file.py`

## Commercial state

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
real revenue        0
PQ-$1               NOT OBSERVED
```

The final artifact is frozen and locally/CI certified at G12/G13. The next legitimate external action is final Test artifact upload/revalidation plus branding reconciliation; Live activation remains a separate owner/provider boundary.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
