# Prompt Machine — Current Status

Last reconciled: `2026-09-08`

This is the current operational status entrypoint for the first Prompt Machine paid release candidate.

## Current truth sources

Read in this order:

1. `commercial/STARTER_CODE_REVIEW_G14_TEST_PRODUCT_PUBLISHED_2026-09-08.json`
2. `commercial/STARTER_CODE_REVIEW_RELEASE_STATE_G14_PROVIDER_HANDOFF_2026-09-08.json`
3. `commercial/STARTER_CODE_REVIEW_EDITION_RELEASE_PROFILE_RC2_V1.json`
4. `commercial/STARTER_CODE_REVIEW_G12_PACK_REBUILD_RC2_PASS_2026-09-08.json`
5. `commercial/STARTER_CODE_REVIEW_G13_PACK_QA_RC2_PASS_2026-09-08.json`
6. `commercial/STARTER_CODE_REVIEW_G14_LEMONSQUEEZY_HANDOFF_V1.md`
7. `certification/receipts/starter-code-review-v2.2-g11-certification.json`
8. `commercial/STARTER_N09_G09_MODEL_SPECIFIC_CLASSIFICATION_2026-09-07.json`

Older release states and RC1 artifacts remain historical evidence only.

## Release candidate

```text
product          Prompt Machine Starter — Code Review Edition
profile          PM-STARTER-CODE-REVIEW-EDITION-V1
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
G14 Provider Gates        TEST PRODUCT PUBLISHED / METADATA PASS / TEST ORDER PENDING
```

G09 does not assert cross-model portability. Observed behavioral evidence remains on `gemini-3.5-flash` only.

G11 certification ID: `PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`.

## RC2 packaging truth

```text
deterministic rebuild      PASS
archive byte identity      PASS
pack QA                    PASS
QA checks                  65/65
workflow byte identity     PASS
customer license frozen    YES
sale terms frozen          YES
stale RC1 references       NO
Bug Diagnosis packaged     NO
```

Packaging evidence does not establish provider custody, delivery, purchase, value, or revenue.

## G14 — observed Lemon Squeezy state

Observed on 2026-09-08 in Lemon Squeezy **Test mode**:

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
```

The local read-only provider probe additionally observed exact name, size, `published` file status, and `test_mode=true`. Lemon returned no file version; that field is optional and is not part of cryptographic custody identity.

A direct provider file download returned HTTP 403. This is **not** classified as a custody failure: Lemon Squeezy documents file downloads as disabled for Test-mode purchases. Therefore:

```text
provider metadata evidence      OBSERVED / PASS
provider byte custody           NOT OBSERVABLE IN TEST MODE
provider test checkout/order    NOT YET OBSERVED
signed order_created webhook    NOT YET OBSERVED
```

Byte custody remains reserved for a later controlled Live canary using `tools/verify_lemonsqueezy_starter_code_review_file.py`.

## Commerce implementation

Prepared and CI-tested:

- `web/lib/starter-code-review-release.ts` — bound to RC2
- `/api/commerce/starter-code-review/checkout`
- `/api/commerce/lemonsqueezy/starter-code-review-webhook`
- `tools/verify_lemonsqueezy_starter_code_review_file.py`
- `tools/test_starter_code_review_g14_v1.py`
- `tools/pm_operator.py`
- `tools/pm_g14_lemonsqueezy_probe.py` — read-only Test-mode metadata probe
- `tools/pm_g14_lemonsqueezy_test_setup.py` — bounded Test-mode setup operator

`prompt-quarry-stage.vercel.app` is deployed and its Code Review webhook path is routable; a GET receives `405 Method Not Allowed`, which is expected because the route only accepts POST.

Defaults remain fail closed:

```text
commerce mode      off
public sale        NOT_FOR_SALE
public checkout    OFF
```

## Operator UX

Invariant:

`one user action <= one command`

`pm_g14_lemonsqueezy_test_setup.py` discovers Store/Product/Variant/File and the provider checkout URL, generates separate webhook and provider-test secrets, and with explicit `--apply-webhook` creates only the Test-mode `order_created` webhook. It never persists or prints the Lemon API key. Generated secrets are written only to a chmod-0600 local Vercel handoff file and are excluded from receipts.

CI validates the setup operator offline with no provider effects.

## Remaining external G14 evidence

```text
Test product published                    OBSERVED / PASS
provider file metadata                    OBSERVED / PASS
Test-mode byte download                   UNAVAILABLE BY PROVIDER DESIGN
Test webhook configured                   NOT YET OBSERVED
provider test checkout/order              NOT YET OBSERVED
signed order_created accepted             NOT YET OBSERVED
Live provider byte custody                NOT YET OBSERVED
Live delivery canary                      NOT YET OBSERVED
real purchase                             0
real revenue                              0
```

## Commercial state

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
PQ-$1               NOT OBSERVED
```

The next legitimate boundary is Test-mode webhook configuration followed by a zero-real-money Test checkout/order. Store activation and Live canary remain separate later decisions.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
