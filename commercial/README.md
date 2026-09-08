# Prompt Machine Commercial System

Status: `CODE REVIEW EDITION RC2 — G14 PROVIDER HANDOFF / PUBLIC SALE OFF`

Prompt Machine is the customer-facing platform. Prompt Quarry is the internal factory that discovers, shapes, tests, improves, and certifies reusable AI workflows.

We do not sell raw prompt count. The commercial product is a governed workflow whose claims are bounded by observed evidence.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Read current truth first

1. `STATUS_CURRENT.md`
2. `STARTER_CODE_REVIEW_RELEASE_STATE_G14_PROVIDER_HANDOFF_2026-09-08.json`
3. `STARTER_CODE_REVIEW_EDITION_RELEASE_PROFILE_RC2_V1.json`
4. `STARTER_CODE_REVIEW_G12_PACK_REBUILD_RC2_PASS_2026-09-08.json`
5. `STARTER_CODE_REVIEW_G13_PACK_QA_RC2_PASS_2026-09-08.json`
6. `STARTER_CODE_REVIEW_G14_LEMONSQUEEZY_HANDOFF_V1.md`
7. `../certification/receipts/starter-code-review-v2.2-g11-certification.json`

Older snapshots, RC1 receipts, `STATUS_V1.md`, old gate/DAG files, and older PR descriptions are historical evidence and do not override the current state.

## First paid release candidate

```text
Prompt Machine Starter — Code Review Edition
version         1.0.0-rc2
price           $9 one-time — hypothesis
workflow        Evidence-first Code Review v2.2
model scope     Gemini 3.5 Flash
classification MODEL_SPECIFIC
```

Bug Diagnosis is excluded until it earns its own behavioral certification.

RC archive:

```text
prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
19,161 bytes
SHA-256 1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
8 members
license + sale terms frozen
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
G12  PASS — RC2
G13  PASS — RC2, 65/65
G14  OFFLINE PASS / EXTERNAL PROVIDER HANDOFF IN PROGRESS
```

G11 certification is deliberately narrow:

`PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`

It covers the exact v2.2 surface, Gemini 3.5 Flash, and the frozen four-case regression matrix. It does not certify untested model families, universal software security, customer outcomes, provider custody, delivery, or readiness to sell.

## Operator model

Operational UX rule:

`one user action <= one command`

`tools/pm_operator.py` runs offline release checks in a temporary detached worktree. `tools/pm_g14_lemonsqueezy_probe.py` performs read-only provider discovery/custody observation without persisting the API key.

The provider probe discovers IDs automatically and reports one of:

```text
PASS
BLOCKED
ACTION_REQUIRED
```

It only establishes exact custody when the provider-held file is actually retrieved and matches RC2 size + SHA-256.

## G14 Lemon Squeezy boundary

The integration code is isolated, fail closed and bound to RC2. The current external handoff uses the Lemon Squeezy store `Prompt Quarry` in Test mode.

Human dashboard action still required:

```text
create exact product                  PENDING
create $9 one-time test variant       PENDING
attach exact RC2                      PENDING
publish provider file                 PENDING
```

Evidence still required afterward:

```text
provider product/variant              NOT OBSERVED
provider custody of exact RC2         NOT OBSERVED
controlled test checkout/order        NOT OBSERVED
signed webhook observation            NOT OBSERVED
delivery-canary boundary              NOT OBSERVED
```

The customer license and sale terms are frozen inside RC2 and are no longer G14 blockers.

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
8. Prefer one governed operator action over manual ceremonies.
9. Do not create subscriptions before one-time demand exists.
10. `not observed == unknown`.
