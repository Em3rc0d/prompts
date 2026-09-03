# Prompt Machine — Workflow Trust History v1

Status: `GOVERNED POLICY / CUSTOMER NARRATIVE NOT YET PUBLIC`

Date: `2026-09-03`

## 1. Purpose

Prompt Machine does not earn trust by claiming that a prompt is "premium", "optimized", or "reliable". It earns trust by preserving the inspectable history of how a workflow was designed, tested, failed, changed, retested, used, and eventually proven valuable.

A workflow's history is therefore a product asset.

```text
WORKFLOW VERSION
      ↓
TEST / REAL USE
      ↓
PASS | FAIL | INCONCLUSIVE
      ↓
EVIDENCE PRESERVED
      ↓
REVIEW
      ↓
LEARNING / DECISION
      ↓
SUCCESSOR OR RETAIN
      ↓
REGRESSION
      ↓
CURRENT TRUST STORY
```

The rule is simple:

> **Do not erase the path to trust. Preserve it, explain it, and keep every public claim at or below the evidence.**

## 2. Canonical trust-history rule

```text
PASS  → evidence
FAIL  → evidence + learning opportunity
FIX   → hypothesis embodied in a successor
RETEST → new evidence
HISTORY → inspectable basis for trust
```

A `FAIL` is not automatically a product defect forever. A historical `FAIL` followed by a documented correction and successful regression can become strong evidence that Prompt Machine detects, understands, and corrects failure modes.

A `FAIL` must never be silently deleted merely because a successor exists.

## 3. Append-only history

Once a workflow version has behavioral evidence, its evidence history is append-only.

Do not:

- overwrite the observed version;
- remove a material failure from the historical record;
- relabel a failure as a pass after the fact;
- move evidence from a predecessor to a successor;
- collapse `INCONCLUSIVE` into `PASS`;
- rewrite the original evaluation contract after seeing the result.

Corrections are represented as new records and, when behavior changes, a new workflow version.

```text
v1.0
├── observation A → PASS
├── observation B → FAIL
└── decision → REWORK

v1.1
├── successor_of → v1.0
├── change hypothesis
├── regression B → PASS
├── normal regression → PASS
└── current limitations
```

## 4. Required history events

When applicable, preserve these event classes separately:

```text
STATIC_REVIEW
INVOCATION_FREEZE
RUNTIME_OBSERVATION
HUMAN_REVIEW
PASS
FAIL
INCONCLUSIVE
DECISION_RETAIN
DECISION_REWORK
DECISION_RETIRE
DECISION_EXPAND_EVIDENCE
SUCCESSOR_CREATED
REGRESSION_PASS
REGRESSION_FAIL
USER_REPORTED_OUTCOME
RETURN_USE_EVIDENCE
PROVIDER_SIGNED_PURCHASE_EVIDENCE
DELIVERY_EVIDENCE
KNOWN_LIMITATION_ADDED
KNOWN_LIMITATION_RESOLVED
```

The event name does not create maturity by itself. It must point to the evidence that supports it.

## 5. Minimum internal trust record

Every material trust-history entry should identify, where applicable:

- workflow ID and version;
- predecessor/successor relationship;
- invocation or test ID;
- date/time;
- runtime/surface identity;
- model identity when actually known;
- expected result/state;
- observed result/state;
- PASS / FAIL / INCONCLUSIVE;
- evaluation dimensions;
- raw evidence reference or hash;
- failure taxonomy when relevant;
- human-review decision;
- change hypothesis when relevant;
- regression cases when relevant;
- known limitations;
- explicit non-claims.

If a fact is not established, store it as unknown rather than filling it in for narrative completeness.

## 6. Failure-story contract

A material failure should preserve this chain:

```text
BEFORE
  exact version / invocation that failed

OBSERVED FAILURE
  what happened, without interpretation inflation

WHY IT MATTERS
  customer, safety, correctness, trust, UX, or economic impact

HYPOTHESIS
  why we think it happened

CHANGE
  exact successor semantics changed

REGRESSION
  whether the motivating case now passes and what else was retested

CURRENT LIMITATION
  what is still unknown or unsupported
```

`HYPOTHESIS` is not fact. `CHANGE` is not proof. `REGRESSION PASS` is not customer value.

## 7. Public Trust Story

Internal evidence is forensic. Customer-facing evidence should be understandable.

A future workflow page may include a section such as:

### Why we trust this workflow

- what job the workflow is designed for;
- current version;
- number and classes of relevant observations;
- important adversarial cases tested;
- material failures discovered;
- what changed because of those failures;
- regression evidence for the current version;
- known limitations;
- last evidence update;
- link/reference to an inspectable evidence card when appropriate.

The public layer is a projection of the internal ledger, never an independently authored marketing truth.

## 8. Anti-cherry-picking rule

Prompt Machine must not create trust by selectively publishing only favorable observations.

If a public statement summarizes a bounded campaign, material failures inside that campaign must remain represented.

Bad:

> "19 tests passed."

when the actual campaign was `19 PASS / 1 material FAIL`.

Acceptable:

> "20 evaluated cases: 19 passed and 1 exposed a failure in X. We changed Y and the successor passed the motivating regression case; broader portability is still unproven."

The exact wording can change, but material evidence cannot disappear.

## 9. Public claim ladder

Public language must correspond to the strongest evidence actually available.

```text
STATIC REVIEW ONLY
→ "statically reviewed"

RUNTIME OBSERVATION
→ "observed in N identified runs/cases"

HUMAN-REVIEWED RUNTIME EVIDENCE
→ "passed these named checks in these observed cases"

SUCCESSOR + REGRESSION PASS
→ "a discovered failure was addressed and the successor passed the specified regression set"

REAL CUSTOMER OUTCOME
→ "used on a real customer task with this reported/observed outcome"

REPEAT USE
→ "return use observed"

REAL PURCHASE + DELIVERY
→ "purchased and delivered"
```

None of the above alone permits an unlimited claim such as "always works", "guaranteed", "fully reliable", or "works on every model".

## 10. Trust-card truth boundary

A customer-facing Trust Card must explicitly distinguish:

```text
OBSERVED
SUPPORTED CLAIM
KNOWN LIMITATION
UNKNOWN
HISTORICAL FAILURE
FIX / SUCCESSOR
REGRESSION EVIDENCE
CUSTOMER VALUE EVIDENCE
```

Do not collapse these into a single opaque "quality score" unless a future validated scoring system exists and its semantics are independently documented.

## 11. Privacy and disclosure

Trust history should maximize transparency without exposing unnecessary customer or internal-sensitive data.

Public projections must:

- remove unnecessary personal data;
- avoid publishing private customer artifacts without authorization;
- preserve enough metadata to understand the evidence class and conditions;
- never fabricate a sanitized example and present it as an actual observed customer case;
- label synthetic fixtures as synthetic.

## 12. Relationship to marketing

Marketing may tell the history only after the evidence exists.

```text
INTERNAL EVENT
      ↓
EVIDENCE RECORD
      ↓
REVIEWED INTERPRETATION
      ↓
ALLOWED CLAIM
      ↓
CUSTOMER NARRATIVE
```

Never reverse this pipeline by writing the story first and searching for supporting evidence later.

Master rule:

> **MARKETING CLAIM <= OBSERVED EVIDENCE**

## 13. Current Prompt Machine baseline

As of `2026-09-03`, the manual low-risk campaign has seven completed behavioral observations with seven expected-state matches and zero blocking review failures.

That evidence is promising but deliberately limited:

```text
7 observations          != certification
7 expected-state matches != portability
0 blocking failures      != proof of universal reliability
shared-plan usage data   != exact per-workflow cost accounting
```

The current campaign remains paused for the five-hour usage reserve. The next logical case is `PM-INV-PLAN-EMBEDDED_OVERRIDE-0003`, but it remains disarmed until the usage gate permits another observation.

## 14. Product principle

Prompt Machine should eventually be able to answer, for every workflow:

> **Why should I trust this workflow?**

with an inspectable history rather than a slogan.

A well-documented failure can become more valuable than an unexplained pass when it leads to a measurable correction and a successful regression. The objective is not to appear flawless. The objective is to become demonstrably better while preserving the evidence of how that happened.
