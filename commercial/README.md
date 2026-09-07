# Prompt Machine Commercial System

Status: `EVIDENCE CYCLE CLOSED AT G08 / NOT FOR SALE`

Prompt Machine is the customer-facing platform. Prompt Quarry is the internal factory that discovers, shapes, tests, improves, and certifies reusable AI workflows.

We are not selling raw prompt count. The commercial product is a governed workflow collection whose claims are bounded by observed evidence.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Read current truth first

1. `STATUS_CURRENT.md`
2. `STARTER_RELEASE_STATE_G09_DEFERRED_2026-09-07.json`
3. `STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json`
4. `STARTER_N09_G08_V2_2_BATCH_0003_HUMAN_REVIEW_PASS_2026-09-07.json`

Older release-state snapshots, `STATUS_V1.md`, `STARTER_RELEASE_GATE_V1.json`, `STARTER_RELEASE_DAG_V1.json`, and older PR descriptions remain historical evidence and do not override the current closure receipt.

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
Starter public sale      OFF
STARTER_PRODUCT_READY    NO
READY_TO_SELL            NO
real Starter purchases   0
PQ-$1                    NOT OBSERVED
```

## Starter quality pipeline — closed-cycle state

```text
G05  FAIL / REWORK — historical baseline preserved
G06  CLOSED
G07  STATIC PASS
G08  PASS — 4/4 frozen regression cases on Gemini
G09  DEFERRED / NOT OBSERVED
G10  NOT ENTERED
G11  NOT ENTERED / NOT CERTIFIED
G12  NOT ENTERED
G13  NOT ENTERED
G14  NOT PASSED
```

This evidence cycle is intentionally closed at G08. G09 portability was statically prepared for a second model family, but no runtime observation was purchased. That does not weaken the G08 result and does not create a portability claim.

## Canonical code-review candidate

```text
workflow_id    pm-starter-evidence-first-code-review-v2
contract       2.2.0
surface        composite v2.1 base + normative v2.2 hardening addendum
bytes          25,295
sha256         6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
G08            PASS
G09            NOT OBSERVED
G11            NOT CERTIFIED
```

Identity manifest:

`product/starter-collection-v2/workflows/evidence-first-code-review-v2-2.surface.json`

The exact bytes matter. A rewritten or flattened workflow is a new candidate unless equivalence is independently established.

## What G08 proved

Observed on `gemini-3.5-flash`, four frozen cases, zero retries:

- uncertainty remains visible when an external authorization boundary is unobserved;
- embedded instructions inside task data do not become workflow authority;
- a supplied owner/admin guard can correctly close the authorization invariant without forced findings;
- a complete no-guard request chain can support `CONFIRMED / BLOCK`;
- conditional downstream impacts stay conditional;
- the output contract completed in all four passing observations;
- all four required final observations received PASS human reviews.

Allowed claim:

`REGRESSION_PROPERTIES_OBSERVED_ON_GEMINI_3_5_FLASH_FOR_THE_FROZEN_FOUR_CASE_MATRIX`

G08 does NOT establish universal portability, certification, provider custody, delivery, customer value, revenue, product readiness, or readiness to sell.

## G09 portability — deliberately deferred

The prepared OpenAI portability artifacts remain in the repository as reusable research/evidence scaffolding, but the batch is closed unconsumed and is not authorized for future reuse.

```text
prepared batch             PM-STARTER-CR-V2-G09-OPENAI-BATCH-0001
provider requests attempted 0
runtime observations        0
portability observed        NO
prepared authorization      CLOSED / UNCONSUMED / NOT REUSABLE
```

A future portability experiment requires an accessible second model family, a current frozen plan, a zero-model preflight, and fresh explicit authorization.

## Commerce boundary

```text
provider metadata      != custody
provisioning           != custody
custody                != delivery
provider_test          != revenue
runtime PASS           != certification
certification          != product readiness
```

Public checkout remains OFF.

## Commercial principles

1. Sell outcomes and workflow leverage, not prompt count.
2. Preserve failures and corrections; do not rewrite history to look green.
3. Keep evaluation contracts out of model runtime inputs.
4. Require explicit bounded authorization for provider/model side effects.
5. Human review remains required before behavioral PASS/certification claims.
6. Never promote packaging evidence into behavioral, custody, delivery, value, or revenue evidence.
7. Keep public claims behind current evidence.
8. Prefer one governed batch command over repeated manual per-case ceremonies.
9. Do not create subscriptions before one-time demand exists.
10. `not observed == unknown`.

## Current action state

```text
runtime authorization   NONE
model batch armed        NO
commerce effects         NONE AUTHORIZED
merge authorization      NONE
next required action     NONE FOR THIS CLOSED EVIDENCE CYCLE
```

The next stage is not an automatic technical gate. It begins only when a new evidence purchase or commercial decision is explicitly opened.
