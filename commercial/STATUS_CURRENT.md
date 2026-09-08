# Prompt Machine — Current Status

Last reconciled: `2026-09-08`

This is the current operational status entrypoint for the first Prompt Machine paid release candidate.

## Current truth sources

Read in this order:

1. `commercial/STARTER_CODE_REVIEW_RELEASE_STATE_G14_PROVIDER_HANDOFF_2026-09-08.json`
2. `commercial/STARTER_CODE_REVIEW_EDITION_RELEASE_PROFILE_RC2_V1.json`
3. `commercial/STARTER_CODE_REVIEW_G12_PACK_REBUILD_RC2_PASS_2026-09-08.json`
4. `commercial/STARTER_CODE_REVIEW_G13_PACK_QA_RC2_PASS_2026-09-08.json`
5. `commercial/STARTER_CODE_REVIEW_G14_LEMONSQUEEZY_HANDOFF_V1.md`
6. `certification/receipts/starter-code-review-v2.2-g11-certification.json`
7. `commercial/STARTER_N09_G09_MODEL_SPECIFIC_CLASSIFICATION_2026-09-07.json`

Older release states, RC1 receipts, `STATUS_V1.md`, `STARTER_RELEASE_GATE_V1.json`, `STARTER_RELEASE_DAG_V1.json`, and older PR descriptions remain historical evidence. They do not override this status.

## Release candidate

```text
product          Prompt Machine Starter — Code Review Edition
profile          PM-STARTER-CODE-REVIEW-EDITION-V1
version          1.0.0-rc2
price            $9 one-time — hypothesis
workflow count   1
```

Bug Diagnosis is not included; it remains deferred until it earns its own behavioral certification.

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
G14 Provider Gates        OFFLINE PASS / EXTERNAL PROVIDER HANDOFF IN PROGRESS
```

G09 does not assert cross-model portability. Observed behavioral evidence is on `gemini-3.5-flash` only.

G11 certification ID:

`PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`

The word **certified** may only be used with the exact Gemini 3.5 Flash / frozen four-case / v2.2 scope or with a direct link to that evidence boundary.

## What is proven

Observed on the frozen four-case matrix using `gemini-3.5-flash`, with zero retries in the final passing batch:

- uncertainty remains visible when a material external authorization boundary is unobserved;
- embedded task-data instructions remain untrusted data;
- a supplied owner/admin guard can close the authorization invariant without forced findings;
- a complete supplied no-guard path can support `CONFIRMED / BLOCK`;
- conditional downstream impact remains conditional;
- the required six-section output contract completed;
- all 4 required final observations received PASS human reviews.

This is evidence for the exact tested surface and scope, not universal software-security or cross-model evidence.

## RC2 packaging truth

RC2 was rebuilt deterministically and independently QA'd after adding the customer license and sale terms and removing stale RC1 references.

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

Packaging evidence does not establish provider custody, customer delivery, purchase, value, or revenue.

## G14 Lemon Squeezy handoff

The Code Review Edition has its own isolated, fail-closed commerce identity. Provider candidate: Lemon Squeezy, using **Test mode** for the current handoff.

Prepared and CI-tested:

- `web/lib/starter-code-review-release.ts` — bound to RC2
- `STARTER_CODE_REVIEW_COMMERCE_MODE`
- `/api/commerce/starter-code-review/checkout`
- `/api/commerce/lemonsqueezy/starter-code-review-webhook`
- `tools/verify_lemonsqueezy_starter_code_review_file.py` — bound to RC2
- `tools/test_starter_code_review_g14_v1.py`
- `tools/pm_operator.py` — bound to RC2
- `tools/pm_g14_lemonsqueezy_probe.py` — read-only provider discovery/custody probe
- `commercial/STARTER_CODE_REVIEW_G14_LEMONSQUEEZY_HANDOFF_V1.md`

Defaults remain fail closed:

```text
commerce mode      off
public sale        NOT_FOR_SALE
public checkout    OFF
```

The read-only probe never creates provider objects and never records the API key. It discovers `store_id → product_id → variant_id → file_id`; with `--verify-bytes` it only recognizes custody when the provider-held bytes match exactly `19,161` and SHA-256 `1f141d...`.

## Operator UX

Operator rule:

`one user action <= one command`

The user's active working tree should not be used as a release state machine. `tools/pm_operator.py` uses a temporary detached worktree, while the Lemon probe can be executed from the latest remote file through `git show` without pulling or stashing the active checkout.

## Remaining external G14 evidence

Not yet observed for RC2:

```text
Lemon Squeezy test product/variant          NOT OBSERVED
provider file metadata                      NOT OBSERVED
exact provider-held archive custody         NOT OBSERVED
provider test checkout/order                NOT OBSERVED
signed webhook observation                  NOT OBSERVED
delivery-canary boundary                    NOT OBSERVED
real purchase                               0
real revenue                                0
```

The customer license and sale terms are no longer blockers; both are frozen inside RC2.

## Commercial state

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
PQ-$1               NOT OBSERVED
```

The next legitimate boundary is a Test-mode Lemon Squeezy dashboard handoff: create the exact $9 one-time product/variant, attach RC2, then run the read-only custody probe. Public sale, merge, and live activation remain separate decisions.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
