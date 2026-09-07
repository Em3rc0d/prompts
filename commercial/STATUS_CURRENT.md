# Prompt Machine — Current Status

Last reconciled: `2026-09-07`

This is the current operational status entrypoint for the Prompt Machine Starter evidence path.

Historical snapshots such as `commercial/STATUS_V1.md`, `commercial/STARTER_RELEASE_GATE_V1.json`, `commercial/STARTER_RELEASE_DAG_V1.json`, and the PR #4 body are preserved as history. They MUST NOT be interpreted as current runtime truth when they conflict with newer superseding receipts.

## Current truth sources

1. `commercial/STARTER_RELEASE_STATE_G08_PASS_2026-09-07.json`
2. `commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json`
3. `commercial/STARTER_N09_G08_V2_2_BATCH_0003_HUMAN_REVIEW_PASS_2026-09-07.json`
4. `product/starter-collection-v2/workflows/evidence-first-code-review-v2-2.surface.json`
5. `commercial/STARTER_N09_G09_PORTABILITY_DESIGN_V1.json`
6. `commercial/STARTER_N09_G09_OPENAI_BATCH_0001_PLAN.json`
7. `commercial/STARTER_N09_G09_OPENAI_BATCH_0001_ENVELOPE_FREEZE.json`
8. `commercial/STARTER_N09_G09_OPENAI_BATCH_0001_STATIC_READINESS_2026-09-07.json`

When a historical aggregate conflicts with one of these current receipts, the current receipt governs the present claim while the historical file remains evidence of the earlier state.

## 14-gate state

```text
G01 Inventory             CLOSED / historical
G02 Specification         CLOSED / historical
G03 Static Audit          CLOSED / historical
G04 Test Design           CLOSED / historical
G05 Baseline Execution    FAIL / REWORK — preserved historical result
G06 Failure Mining        CLOSED
G07 Improvement           STATIC PASS
G08 Regression            PASS — 4/4 required cases on canonical v2.2 composite
G09 Portability           STATIC READY / BATCH PREPARED / NOT AUTHORIZED
G10 Human Value Review    NOT STARTED
G11 Certification         NOT STARTED
G12 Pack Rebuild          NOT STARTED
G13 Pack-level QA         NOT STARTED
G14 Provider Gates        NOT PASSED
```

## Canonical Evidence-first Code Review candidate

```text
workflow_id     pm-starter-evidence-first-code-review-v2
contract        2.2.0
surface mode    composite v2.1 base + normative v2.2 hardening addendum
bytes           25,295
sha256          6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
G08             PASS
G09             NOT YET PASSED
G11             NOT CERTIFIED
```

Canonical identity:

`product/starter-collection-v2/workflows/evidence-first-code-review-v2-2.surface.json`

Do not flatten, rewrite, or silently mutate this surface and continue to cite the G08 result. Any byte-changing candidate requires a new identity and the applicable revalidation.

## G08 evidence

```text
batch                          PM-STARTER-CR-V2-G08-BATCH-0003
provider                       GOOGLE_GEMINI_API
model                          gemini-3.5-flash
provider requests              4
runtime observations           4
HTTP 200                       4/4
finish STOP                    4/4
retries                        0
human review PASS              4/4
evaluation contract at runtime NO
expected result at runtime     NO
result                         PASS
```

Observed regression properties:

- unknown external authorization boundary -> `LIKELY / REVIEW_REQUIRED`;
- embedded instructions remain untrusted task data;
- supplied owner/admin guard -> no forced finding / `NO_MATERIAL_ISSUE_FOUND`;
- complete supplied no-guard chain -> `CONFIRMED / BLOCK`;
- conditional downstream impact remains conditional;
- output contract completed.

This supports only the frozen four-case regression claim on the exact canonical surface.

## Current next gate — G09 portability

G09 asks:

> Does the exact same canonical workflow preserve the required behaviors on at least one declared non-Gemini model family in a clean independent context?

The first portability batch is now statically prepared:

```text
batch                 PM-STARTER-CR-V2-G09-OPENAI-BATCH-0001
provider              OPENAI_RESPONSES_API
model family          OPENAI_GPT_5_6
model                 gpt-5.6-luna
cases                 same frozen 4
surface               exact G08-passing v2.2 bytes
per-case envelopes    exact G08 byte/hash parity required
max requests total    4
max requests/case     1
retries               0
max output tokens     8192
reasoning             low
store                 false
tools                 none
evaluation at runtime NO
expected at runtime   NO
human review          REQUIRED
authorization         NOT GRANTED
```

Operational entrypoint:

`tools/pm_g09_openai_batch_0001_v2.py`

The hardened entrypoint performs zero-model integrity checks first. It requires the exact four G08 envelope byte counts and SHA-256 values before an authorization can be consumed. It also checks local WSL and `OPENAI_API_KEY` presence without recording the credential value.

Baseline G09 PASS requires all four cases to produce clean observations and all four frozen evaluation contracts to receive PASS human reviews on this non-Gemini family.

A G09 baseline PASS would support only:

`PORTABILITY_OBSERVED_ACROSS_TWO_MODEL_FAMILIES_ONLY`

It would NOT support “works on every model”, universal model agnosticism, certification, product readiness, readiness to sell, delivery, or revenue.

## Authorization state

```text
G08 BATCH-0003 authorization      CONSUMED / CLOSED
G09 OPENAI BATCH-0001             DISARMED
fresh explicit G09 authorization  REQUIRED
provider requests in G09          0
model observations in G09         0
```

No G09 runtime should execute until the user explicitly authorizes its bounded batch.

## Commerce and product state

```text
provider custody       NOT OBSERVED
provider integration   NOT PASSED
live delivery          NOT OBSERVED
public checkout        OFF
real purchases         0
PQ-$1                  NOT OBSERVED
STARTER_PRODUCT_READY  NO
READY_TO_SELL          NO
```

## Hard boundaries

```text
G08 PASS != portability
G09 static readiness != G09 PASS
G09 PASS != certification
certification != provider custody
provider custody != delivery
provider_test != revenue
packaging != product readiness
model response != human certification
historical snapshot != current truth
```

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
