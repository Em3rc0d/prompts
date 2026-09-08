# Prompt Machine — Current Status

Last reconciled: `2026-09-08`

This is the operational entrypoint for the first paid release candidate.

## Current truth sources

1. `commercial/STARTER_CODE_REVIEW_G14_TEST_CHECKOUT_READY_2026-09-08.json`
2. `commercial/STARTER_CODE_REVIEW_G14_TEST_WEBHOOK_CREATED_2026-09-08.json`
3. `commercial/STARTER_CODE_REVIEW_G14_TEST_PRODUCT_PUBLISHED_2026-09-08.json`
4. `commercial/STARTER_CODE_REVIEW_RELEASE_STATE_G14_PROVIDER_HANDOFF_2026-09-08.json`
5. `commercial/STARTER_CODE_REVIEW_EDITION_RELEASE_PROFILE_RC2_V1.json`
6. `commercial/STARTER_CODE_REVIEW_G12_PACK_REBUILD_RC2_PASS_2026-09-08.json`
7. `commercial/STARTER_CODE_REVIEW_G13_PACK_QA_RC2_PASS_2026-09-08.json`
8. `commercial/STARTER_CODE_REVIEW_G14_LEMONSQUEEZY_HANDOFF_V1.md`
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
G14 Provider Gates        TEST CHECKOUT READY / TEST ORDER + SIGNED WEBHOOK PENDING
```

G09 does not assert cross-model portability. Behavioral evidence remains on `gemini-3.5-flash` only.

G11 certification ID: `PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`.

## G14 observed state

Observed in Lemon Squeezy Test mode and Vercel staging:

```text
product name          Prompt Machine Starter — Code Review Edition
product id            1347702
price                 $9.00 one-time
product status        Published
test mode             TRUE
RC2 filename          MATCH
RC2 provider size     19,161 bytes
file status           published
provider metadata     PASS
webhook id            132724
webhook event         order_created
webhook target        https://prompt-quarry-stage.vercel.app/api/commerce/lemonsqueezy/starter-code-review-webhook
Vercel deployment     dpl_8aoy1xPf5w9o6zPnBQLN6GT3YMXT
Vercel state          READY
Vercel target         production
checkout gate         provider_test
checkout redirect     OBSERVED / HTTP 302
runtime event         provider_test_checkout_started
runtime release       1.0.0-rc2 / 19,161 bytes / SHA-256 MATCH
```

The Test-mode file download returned HTTP 403. Lemon Squeezy disables Test-mode file downloads, so this is not treated as corrupted custody evidence. Exact provider-held byte custody remains reserved for a later controlled Live canary.

## Current G14 operator path

Prepared and CI-tested:

- `tools/pm_g14_lemonsqueezy_probe.py` — read-only Test metadata.
- `tools/pm_g14_lemonsqueezy_test_setup.py` — Test webhook setup; API key not persisted.
- `tools/pm_g14_vercel_test_apply.py` — owner-only Vercel handoff, env upsert, redeploy and private Test checkout verification.
- `tools/verify_lemonsqueezy_starter_code_review_file.py` — later controlled Live byte-custody verification.

The generated signing and gate secrets remain outside the repository in an owner-only local handoff. Public sale remains `NOT_FOR_SALE`.

## Remaining external G14 evidence

```text
Test product published                    OBSERVED / PASS
provider file metadata                    OBSERVED / PASS
Test webhook configured                   OBSERVED / PASS
Test-mode byte download                   UNAVAILABLE BY PROVIDER DESIGN
Vercel Test env import                     OBSERVED / PASS
Vercel Test redeploy                       OBSERVED / PASS
private provider-test checkout redirect    OBSERVED / PASS
provider test checkout/order               NOT YET OBSERVED
signed order_created accepted              NOT YET OBSERVED
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

The next legitimate boundary is one zero-real-money Lemon Test order followed by provider-signed `order_created` acceptance in Vercel. Store activation and Live canary remain separate later decisions.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
