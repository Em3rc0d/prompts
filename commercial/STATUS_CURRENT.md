# Prompt Machine — Current Status

Last reconciled: `2026-09-08`

This is the current operational status entrypoint for the first Prompt Machine paid release candidate.

## Current truth sources

Read in this order:

1. `commercial/STARTER_CODE_REVIEW_RELEASE_STATE_G14_OFFLINE_READY_2026-09-08.json`
2. `commercial/STARTER_N09_G09_MODEL_SPECIFIC_CLASSIFICATION_2026-09-07.json`
3. `certification/receipts/starter-code-review-v2.2-g11-certification.json`
4. `commercial/STARTER_CODE_REVIEW_G12_PACK_REBUILD_PASS_2026-09-07.json`
5. `commercial/STARTER_CODE_REVIEW_G13_PACK_QA_PASS_2026-09-07.json`
6. `product/starter-collection-v2/workflows/evidence-first-code-review-v2-2.surface.json`

Older release states, `STATUS_V1.md`, `STARTER_RELEASE_GATE_V1.json`, `STARTER_RELEASE_DAG_V1.json`, and pre-reconciliation PR descriptions remain historical evidence. They do not override this status.

## Release candidate

```text
product          Prompt Machine Starter — Code Review Edition
profile          PM-STARTER-CODE-REVIEW-EDITION-V1
version          1.0.0-rc1
price            $9 one-time — hypothesis
workflow count   1
```

Bug Diagnosis is not included in this RC; it is deferred until it earns its own behavioral certification.

Canonical Code Review surface:

```text
workflow_id      pm-starter-evidence-first-code-review-v2
contract         2.2.0
bytes            25,295
sha256           6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
authority        ADVISORY_ONLY
```

Canonical RC archive:

```text
prompt-machine-starter-code-review-edition-v1.0.0-rc1.zip
14,667 bytes
SHA-256 7ec282ea1766679f425fd5aad526d6382e6a3c5af2caab9ded07e55b9a773cde
6 members
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
G12 Pack Rebuild          PASS
G13 Pack-level QA         PASS
G14 Provider Gates        OFFLINE PREP PASS / EXTERNAL EVIDENCE PENDING
```

G09 does not assert cross-model portability. The correct classification is `MODEL_SPECIFIC` because the observed behavioral evidence is on `gemini-3.5-flash` only.

G11 certification ID:

`PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`

The word **certified** may only be used with the exact Gemini 3.5 Flash / frozen four-case / v2.2 scope or with a direct link to that evidence boundary.

## What is actually proven

Observed on the frozen four-case matrix using `gemini-3.5-flash`, with zero retries in the final passing batch:

- uncertainty is preserved when a material external authorization boundary is unobserved;
- embedded task-data instructions remain untrusted data;
- a supplied owner/admin guard can close the authorization invariant without forced findings;
- a complete supplied no-guard path can support `CONFIRMED / BLOCK`;
- conditional downstream impact remains conditional;
- the required six-section output contract completed;
- all 4 required final observations received PASS human reviews.

This is evidence for the exact tested surface and scope. It is not universal software-security or cross-provider evidence.

## G12/G13 packaging truth

The Code Review Edition was rebuilt deterministically and independently QA'd.

```text
deterministic rebuild      PASS
archive byte identity      PASS
pack QA                    PASS
QA checks                  37/37
workflow byte identity     PASS
Bug Diagnosis packaged     NO
```

Packaging evidence does not establish provider custody, customer delivery, purchase, value, or revenue.

## G14 offline preparation

The new Code Review Edition has its own isolated commerce identity and does not reuse the historical Starter v1 archive identity.

Prepared and CI-tested:

- `web/lib/starter-code-review-release.ts`
- `STARTER_CODE_REVIEW_COMMERCE_MODE`
- `/api/commerce/starter-code-review/checkout`
- `/api/commerce/lemonsqueezy/starter-code-review-webhook`
- `tools/verify_lemonsqueezy_starter_code_review_file.py`
- `tools/test_starter_code_review_g14_v1.py`
- `tools/pm_operator.py`

Defaults remain fail closed:

```text
commerce mode      off
public sale        NOT_FOR_SALE
public checkout    OFF
provider calls     0 in offline preparation
model calls        0 in offline preparation
commerce effects   0 in offline preparation
```

At source HEAD `9a0f73e235b6e9c01739fcd3ef0cc32d2bbbdba2`, 15/15 observed PR workflow runs completed successfully, including Code Review Edition, Commerce v0 and Prompt Machine Operator v1.

## Operator UX

Operator rule:

`one user action <= one command`

`tools/pm_operator.py` performs release checks in a temporary detached worktree. It does not stash, reset, pull into, or otherwise modify the user's active working tree. It returns only `PASS`, `BLOCKED`, or `ACTION_REQUIRED` at the human boundary.

## Remaining external G14 evidence

Not yet observed for this exact RC:

```text
standalone customer license / sale terms   PENDING
provider product + variant identity         NOT OBSERVED
exact provider-held archive custody         NOT OBSERVED
provider test checkout/order                NOT OBSERVED
live delivery canary                        NOT OBSERVED
real purchase                               0
real revenue                                0
```

Provider candidate remains Lemon Squeezy. Static integration and offline simulation are not provider evidence.

## Commercial state

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
PQ-$1               NOT OBSERVED
```

The next legitimate boundary is G14 external evidence. Public sale, merge, or stronger claims are not automatic consequences of offline readiness.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
