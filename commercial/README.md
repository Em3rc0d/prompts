# Prompt Machine Commercial System

Status: `CODE REVIEW EDITION — G14 OFFLINE READY / EXTERNAL EVIDENCE PENDING / NOT FOR SALE`

Prompt Machine is the customer-facing platform. Prompt Quarry is the internal factory that discovers, shapes, tests, improves, and certifies reusable AI workflows.

We do not sell raw prompt count. The commercial product is a governed workflow whose claims are bounded by observed evidence.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Read current truth first

1. `STATUS_CURRENT.md`
2. `STARTER_CODE_REVIEW_RELEASE_STATE_G14_OFFLINE_READY_2026-09-08.json`
3. `STARTER_N09_G09_MODEL_SPECIFIC_CLASSIFICATION_2026-09-07.json`
4. `../certification/receipts/starter-code-review-v2.2-g11-certification.json`
5. `STARTER_CODE_REVIEW_G12_PACK_REBUILD_PASS_2026-09-07.json`
6. `STARTER_CODE_REVIEW_G13_PACK_QA_PASS_2026-09-07.json`

Older release-state snapshots, `STATUS_V1.md`, `STARTER_RELEASE_GATE_V1.json`, `STARTER_RELEASE_DAG_V1.json`, and older PR descriptions are historical evidence and do not override the current state.

## First paid release candidate

```text
Prompt Machine Starter — Code Review Edition
version        1.0.0-rc1
price          $9 one-time — hypothesis
workflow       Evidence-first Code Review v2.2
model scope    Gemini 3.5 Flash
classification MODEL_SPECIFIC
```

Bug Diagnosis is excluded from this RC until it earns its own behavioral certification.

RC archive:

```text
prompt-machine-starter-code-review-edition-v1.0.0-rc1.zip
14,667 bytes
SHA-256 7ec282ea1766679f425fd5aad526d6382e6a3c5af2caab9ded07e55b9a773cde
```

## Current quality pipeline

```text
G05  FAIL / REWORK — historical baseline preserved
G06  CLOSED
G07  PASS
G08  PASS — 4/4 frozen final regression cases
G09  MODEL_SPECIFIC / PASS_FOR_DEMONSTRATED_SCOPE
G10  KEEP / RECORDED
G11  PASS_FOR_EXACT_DECLARED_SCOPE
G12  PASS
G13  PASS
G14  OFFLINE PREP PASS / EXTERNAL EVIDENCE PENDING
```

G11 certification is deliberately narrow:

`PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`

It covers the exact v2.2 surface, Gemini 3.5 Flash, and the frozen four-case regression matrix. It does not certify untested model families, universal software security, customer outcomes, provider custody, delivery, or readiness to sell.

## Operator model

Operational UX rule:

`one user action <= one command`

`tools/pm_operator.py` runs release checks in a temporary detached worktree, protects the user's active working tree, builds and verifies the exact RC, runs pack/commerce/G14 offline checks, and reports only:

```text
PASS
BLOCKED
ACTION_REQUIRED
```

The operator performs zero external provider/model/commerce effects unless a separate external action is explicitly opened.

## G14 boundary

Offline G14 preparation is CI green and fail closed. The new Code Review Edition has isolated commerce mode, checkout, signed webhook and exact Lemon Squeezy custody verification logic.

Still required before G14 PASS:

```text
customer license / sale terms        PENDING
provider product/variant             NOT OBSERVED
provider custody of exact RC         NOT OBSERVED
controlled provider test order       NOT OBSERVED
live delivery canary                 NOT OBSERVED
```

Public checkout remains OFF.

## Commercial hypothesis

```text
FREE       $0
STARTER    $9 one-time
FULL       $19 one-time
SUBSCRIPTION deferred
```

Primary milestone:

`PQ-$1 = first real non-test paid purchase successfully delivered`

Current commercial truth:

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
PQ-$1               NOT OBSERVED
```

## Evidence boundaries

```text
provider metadata      != custody
provisioning           != custody
custody                != delivery
provider_test          != revenue
runtime PASS           != universal certification
certification          != product readiness
packaging              != customer value
```

## Commercial principles

1. Sell outcomes and workflow leverage, not prompt count.
2. Preserve failures and corrections; do not rewrite history to look green.
3. Keep evaluation contracts out of model runtime inputs.
4. Require bounded authorization for provider/model side effects.
5. Human review remains required for behavioral certification decisions.
6. Never promote packaging evidence into behavioral, custody, delivery, value, or revenue evidence.
7. Keep public claims behind current evidence.
8. Prefer one governed operator command over manual ceremonies.
9. Do not create subscriptions before one-time demand exists.
10. `not observed == unknown`.
