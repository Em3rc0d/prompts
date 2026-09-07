# Prompt Machine — Current Status

Last reconciled: `2026-09-07`

This is the current operational status entrypoint for the Prompt Machine Starter evidence path.

Historical snapshots such as `commercial/STATUS_V1.md`, `commercial/STARTER_RELEASE_GATE_V1.json`, `commercial/STARTER_RELEASE_DAG_V1.json`, and the PR #4 body are preserved as history. They MUST NOT be interpreted as current runtime truth when they conflict with the superseding receipts listed below.

## Current truth sources

1. `commercial/STARTER_RELEASE_STATE_G08_PASS_2026-09-07.json`
2. `commercial/STARTER_N09_LOCAL_EXECUTION_POLICY_V1.json`
3. `commercial/STARTER_N09_G08_V2_2_BATCH_0003_HUMAN_REVIEW_PASS_2026-09-07.json`
4. `product/starter-collection-v2/workflows/evidence-first-code-review-v2-2.surface.json`
5. `commercial/STARTER_N09_G09_PORTABILITY_DESIGN_V1.json`

When a historical aggregate conflicts with one of these current receipts, the current receipt governs the present claim while the historical file remains append-only evidence of the earlier state.

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
G09 Portability           DESIGNED / RUNTIME NOT YET AUTHORIZED
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
batch                         PM-STARTER-CR-V2-G08-BATCH-0003
provider                      GOOGLE_GEMINI_API
model                         gemini-3.5-flash
provider requests             4
runtime observations          4
HTTP 200                      4/4
finish STOP                   4/4
retries                       0
human review PASS             4/4
evaluation contract at runtime NO
expected result at runtime     NO
result                        PASS
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

G09 asks a different question from G08:

> Does the exact same canonical workflow preserve those required behaviors on at least one declared non-Gemini model family in a clean independent context?

Baseline pass requires all four frozen cases to receive clean observations and PASS human reviews on one non-Gemini family. A G09 pass would support only:

`PORTABILITY_OBSERVED_ACROSS_TWO_MODEL_FAMILIES_ONLY`

It would NOT support “works on every model”, universal model agnosticism, certification, product readiness, readiness to sell, delivery, or revenue.

G09 provider/model runtime must be declared and frozen before execution. Fresh explicit authorization is required for its bounded batch.

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
