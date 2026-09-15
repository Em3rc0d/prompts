# Prompt Machine — Customer Trust Surface v1

Status: `DESIGNED / NOT PUBLIC / PUBLICATION GATE CLOSED`

Date: `2026-09-03`

## 1. Purpose

Prompt Machine should make evidence understandable to customers without converting nuanced history into a decorative green badge.

The customer-facing trust surface is a projection of the governed Trust Card, which is itself derived from internal evidence.

```text
RAW / REVIEWED EVIDENCE
        ↓
INTERNAL LEDGER
        ↓
TRUST CONTEXT
        ↓
DETERMINISTIC TRUST CARD
        ↓
HUMAN REVIEW
        ↓
CUSTOMER TRUST SURFACE
```

The UI may simplify presentation. It may not simplify away material failures, limitations, unknowns, or scope.

## 2. Core UX principle

The customer question is:

> **Why should I trust this workflow for this job?**

The answer should be inspectable in under one minute, with deeper evidence available on demand.

Do not make the user decode internal PCP/MK/F-state terminology to understand the answer.

## 3. Required visible sections

A public workflow Trust Surface should contain, when evidence exists:

```text
WORKFLOW / VERSION / INTENDED JOB
        ↓
CURRENT EVIDENCE SNAPSHOT
        ↓
WHAT WE TESTED
        ↓
WHAT FAILED / WHAT WE FOUND
        ↓
WHAT CHANGED
        ↓
CURRENT LIMITATIONS
        ↓
LAST EVIDENCE UPDATE
        ↓
VIEW EVIDENCE DETAILS
```

If a section has no applicable evidence, say so precisely rather than hiding the section in a way that implies success.

## 4. Header

Display:

- workflow name;
- workflow version;
- intended job/outcome;
- evidence scope;
- last evidence update;
- evidence status label.

Allowed status labels should describe evidence state, not prestige.

Examples:

```text
STATICALLY REVIEWED
OBSERVED IN BOUNDED CASES
HUMAN-REVIEWED CASES
REGRESSION OBSERVED
REAL-TASK USE OBSERVED
RETURN USE OBSERVED
PURCHASE + DELIVERY OBSERVED
```

Avoid labels such as:

```text
PERFECT
TRUSTED 100%
AI VERIFIED
GUARANTEED
UNBREAKABLE
BEST
```

## 5. Evidence snapshot

Prefer scoped facts over opaque scores.

Good:

```text
7 bounded observations
7 expected-state matches
3 adversarial instruction/data cases
0 blocking review failures observed
11 prepared cases not yet run
```

Bad:

```text
Quality score: 98/100
Reliability: 100%
Security: A+
```

A future score is permitted only if Prompt Machine develops and validates a separate scoring methodology with documented semantics.

## 6. What we tested

Use plain-language conditions.

Examples:

- normal checklist execution;
- task data containing embedded override text;
- learning workflow without learner evidence;
- release-summary generation with unknown deployment state;
- advisory release planning without executing a release.

Each condition should map to one or more evidence references internally.

Do not say `tested against prompt injection` if only one narrow embedded-override fixture was evaluated. Say exactly what class of adversarial condition was observed.

## 7. Failure presentation

Failures are not hidden in an accordion titled `technical details` merely to protect conversion.

A material historical failure should be summarized as:

```text
FOUND
What went wrong.

IMPACT
Why it mattered.

CHANGED
What changed in the successor.

RETESTED
What regression evidence now exists.

STILL UNKNOWN
What remains unsupported.
```

A historical failure that has been corrected should remain visible as historical evidence, not be presented as a current defect.

## 8. Zero observed failures wording

If a bounded campaign has no observed material failures, do not write:

> No failures.

Use:

> No material failures were observed in the currently listed bounded cases.

Then show the untested or unknown scope.

Absence of observed failure is not proof that failure is impossible.

## 9. Pre-runtime issues

Static design mistakes and runtime failures are different evidence classes.

Example:

```text
PRE-RUNTIME ISSUE
Learning v1.2 exposed an answer key inside runtime-visible input.

CHANGE
v1.3 moved the answer key outside runtime input.

FOLLOW-UP
Two bounded Learning observations preserved the corrected boundary.
```

Do not relabel this as `the model failed` if no runtime failure was observed.

## 10. Limitations

Material limitations are first-class UX, not legal footer text.

Examples:

```text
Not certified
Portability across providers not established
Real customer task outcomes not yet observed
No repeat-use evidence yet
Remaining prepared cases not yet executed
```

A limitation can become resolved only when new evidence supports that transition.

## 11. Unknowns

Unknowns should be visible and phrased concretely.

Good:

> Behavior on other model/provider surfaces has not yet been observed.

Bad:

> Results may vary.

Generic disclaimers are not a substitute for identifying what Prompt Machine actually does not know.

## 12. Customer-facing narrative pattern

A short narrative may be rendered from the Trust Card:

> This workflow is not marked reliable because it looks well written. We record the cases we run, compare observed behavior with predeclared expectations, preserve failures and limitations, and strengthen claims only when new evidence supports them.

For a workflow with a corrected historical failure:

> An earlier version exposed a failure in **X**. We changed **Y**, reran the motivating case plus relevant regressions, and the current version passed those specified checks. **Z** remains unproven.

These are templates, not permission to invent facts. Every variable must be supported by the Trust Card.

## 13. Progressive disclosure

Recommended surface hierarchy:

```text
LEVEL 1 — glance
workflow + version + evidence state + last update

LEVEL 2 — understand
what tested + key results + limitations

LEVEL 3 — inspect
history timeline + failures + changes + regressions

LEVEL 4 — audit
machine-readable evidence references / hashes / receipts where appropriate
```

A casual buyer should not need Level 4. A skeptical technical buyer should be able to reach it.

## 14. Visual semantics

Color may support meaning but cannot carry meaning alone.

Recommended semantic treatment:

- `PASS`: positive but scoped;
- `FAIL`: visible and neutral/diagnostic, not shame-oriented;
- `INCONCLUSIVE`: distinct from pass/fail;
- `UNKNOWN`: explicit;
- `HISTORICAL`: clearly separated from current state;
- `LIMITATION`: persistent until resolved by evidence.

Always pair color with text/iconography suitable for accessible interpretation.

Do not use celebratory animation for a PASS in a way that visually implies certification.

## 15. Mobile behavior

The first mobile viewport of a Trust Surface should communicate:

1. which workflow/version this evidence refers to;
2. current evidence scope;
3. one sentence on what was observed;
4. the most material limitation.

Detailed history may expand below.

Do not require a horizontal table to understand the evidence.

## 16. Accessibility

Minimum requirements:

- status is never color-only;
- semantic headings;
- keyboard-accessible details disclosure;
- readable dates and versions;
- no tooltip-only critical evidence;
- screen-reader text for status icons;
- failure/history timeline usable without animation.

## 17. Privacy boundary

The Trust Surface must not expose customer task contents, identities, confidential artifacts, or private repository material merely to make the evidence feel more convincing.

Public evidence can use:

- bounded metadata;
- anonymized/authorized case descriptions;
- hashes or receipt identifiers when useful;
- synthetic fixtures clearly labeled as synthetic.

Synthetic evidence must never be presented as a real customer case.

## 18. Publication gate

A Trust Card may exist internally before it is public.

Required path:

```text
EVIDENCE SOURCES
→ deterministic Trust Card generation
→ validator PASS
→ HUMAN REVIEW
→ privacy/redaction review when relevant
→ claim review
→ PUBLICATION_ELIGIBLE
→ customer surface
```

Automatic publication remains blocked.

A workflow update that changes evidence materially should make the public projection stale until regenerated/reviewed.

## 19. Current first campaign

Current card:

`PM-TRUST-CARD-MANUAL-CANARY-V1-0001`

Scope:

`BOUNDED_CAMPAIGN`

Current state:

```text
behavioral observations             7
expected-state matches              7 / 7
blocking review failures            0
embedded-override observations      3
remaining prepared cases           11
public Trust Card                   NO
READY_TO_SELL                       NO
```

This campaign-level card must not be displayed as certification of one individual workflow.

## 20. Product principle

> **The Trust Surface is not where Prompt Machine invents credibility. It is where accumulated evidence becomes understandable.**

The commercial advantage is not a prettier badge. It is the ability to show how the workflow changed because evidence existed.
