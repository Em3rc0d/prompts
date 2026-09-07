# Prompt Machine Commercial System

Status: `ACTIVE EVIDENCE DEVELOPMENT / NOT FOR SALE`

Prompt Machine is the customer-facing platform. Prompt Quarry is the internal factory that discovers, shapes, tests, improves, and certifies reusable AI workflows.

We are not selling raw prompt count. The commercial product is a governed workflow collection whose claims are bounded by observed evidence.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Read current truth first

For current execution truth, read:

1. `STATUS_CURRENT.md`
2. `STARTER_RELEASE_STATE_G09_PREPARED_2026-09-07.json`
3. `STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json`
4. `STARTER_N09_G09_OPENAI_BATCH_0001_STATIC_READINESS_2026-09-07.json`

`STATUS_V1.md`, `STARTER_RELEASE_GATE_V1.json`, `STARTER_RELEASE_DAG_V1.json`, `STARTER_RELEASE_STATE_G08_PASS_2026-09-07.json`, and older PR descriptions are historical snapshots. They remain useful evidence of earlier states, but they do not override newer superseding receipts.

## Commercial hypothesis

```text
FREE       $0
STARTER    $9 one-time
FULL       $19 one-time
SUBSCRIPTION deferred
```

Primary milestone:

`PQ-$1 = first real non-test paid purchase successfully delivered`

Current truth:

```text
Starter public sale      OFF
STARTER_PRODUCT_READY    NO
READY_TO_SELL            NO
real Starter purchases   0
PQ-$1                    NOT OBSERVED
```

## Starter quality pipeline

Canonical gate order:

```text
G01 Inventory
G02 Specification
G03 Static Audit
G04 Test Design
G05 Baseline Execution
G06 Failure Mining
G07 Improvement
G08 Regression
G09 Portability
G10 Human Value Review
G11 Certification
G12 Pack Rebuild
G13 Pack-level QA
G14 Provider Gates
```

Current frontier:

```text
G05  FAIL / REWORK — historical baseline preserved
G06  CLOSED
G07  STATIC PASS
G08  PASS — 4/4 frozen regression cases on Gemini
G09  STATIC READY / OPENAI BATCH PREPARED / NOT AUTHORIZED
G10  NOT STARTED
G11  NOT STARTED
G12  NOT STARTED
G13  NOT STARTED
G14  NOT PASSED
```

## Canonical code-review candidate

```text
workflow_id    pm-starter-evidence-first-code-review-v2
contract       2.2.0
surface        composite v2.1 base + normative v2.2 hardening addendum
bytes          25,295
sha256         6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
G08            PASS
G09            NOT YET PASSED
G11            NOT CERTIFIED
```

Identity manifest:

`product/starter-collection-v2/workflows/evidence-first-code-review-v2-2.surface.json`

The exact bytes matter. A rewritten or flattened workflow is a new candidate unless equivalence is independently established.

## What G08 proved — and did not prove

Observed on `gemini-3.5-flash`, four frozen cases, zero retries:

- uncertainty remains visible when an external authorization boundary is unobserved;
- embedded instructions inside task data do not become workflow authority;
- a supplied owner/admin guard can correctly close the authorization invariant without forced findings;
- a complete no-guard request chain can support `CONFIRMED / BLOCK`;
- conditional downstream impacts stay conditional;
- the output contract completed in all four passing observations.

G08 does NOT establish universal portability, certification, provider custody, delivery, customer value, revenue, product readiness, or readiness to sell.

## Current next experiment — G09 portability

G09 keeps the same four cases, the same out-of-band evaluation contracts, and the exact same canonical v2.2 surface, but runs them on a declared **non-Gemini model family** in a clean independent context.

First prepared portability batch:

```text
batch                PM-STARTER-CR-V2-G09-OPENAI-BATCH-0001
provider             OPENAI_RESPONSES_API
model family         OPENAI_GPT_5_6
model                gpt-5.6-luna
cases                same frozen 4
envelopes            exact G08 byte/hash parity required
max requests         4 total / 1 per case
retries              0
max output tokens    8192
reasoning            low
store                false
tools                none
human review         required
authorization        NOT GRANTED
```

Hardened entrypoint:

`tools/pm_g09_openai_batch_0001_v2.py`

Its preflight must pass before authorization can be consumed. It verifies WSL, local `OPENAI_API_KEY` presence without recording the value, the exact canonical surface, exact original case/evaluation hashes, evaluation exclusion, and exact parity with all four G08-passing runtime envelopes.

Baseline G09 PASS requires 4/4 clean observations and 4/4 human-review PASS on the OpenAI family.

The strongest claim after baseline PASS is only:

`PORTABILITY_OBSERVED_ACROSS_TWO_MODEL_FAMILIES_ONLY`

Forbidden even after that pass:

- “works on every model”;
- unqualified “model agnostic”;
- “provider independent across all providers”;
- “certified” before G11;
- “product ready” or “ready to sell”.

## Commerce boundary

Provider preparation and behavior certification are separate lanes.

```text
provider metadata      != custody
provisioning           != custody
custody                != delivery
provider_test          != revenue
runtime PASS           != certification
certification          != product readiness
```

Public checkout remains blocked until the applicable behavioral, delivery, current-copy, and explicit human release gates are satisfied.

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

## Key documents

- `STATUS_CURRENT.md` — current operational state.
- `STARTER_RELEASE_STATE_G09_PREPARED_2026-09-07.json` — current release/evidence frontier.
- `PROMPT_MACHINE_14_GATE_PIPELINE_V1.json` — quality pipeline.
- `PROMPT_MACHINE_BOUNDED_BATCH_EXECUTION_POLICY_V1.json` — batch governance.
- `STARTER_N09_G08_V2_2_BATCH_0003_HUMAN_REVIEW_PASS_2026-09-07.json` — G08 PASS receipt.
- `STARTER_N09_G09_PORTABILITY_DESIGN_V1.json` — portability contract.
- `STARTER_N09_G09_OPENAI_BATCH_0001_PLAN.json` — first non-Gemini batch plan.
- `STARTER_N09_G09_OPENAI_BATCH_0001_ENVELOPE_FREEZE.json` — exact G08/G09 envelope parity.
- `STARTER_N09_G09_OPENAI_BATCH_0001_STATIC_READINESS_2026-09-07.json` — static readiness receipt.

First prove reliable behavior. Then prove portability. Then certify. Then prove delivery. Then earn the first real purchase.
