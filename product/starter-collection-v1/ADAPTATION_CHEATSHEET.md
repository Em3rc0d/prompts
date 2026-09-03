# Starter Collection — Adaptation Cheatsheet

Status: `CUSTOMER SURFACE CANDIDATE / NOT FOR SALE`

The Starter workflows are reusable, but not every edit is harmless.

## Usually safe to adapt

### Code Review

- language/framework/runtime context;
- review lenses;
- severity definitions for your team;
- minimum severity/reporting threshold;
- maximum number of findings;
- organization-specific compatibility rules;
- required verification checks;
- terminology and output detail.

### Bug Diagnosis

- environment/context fields;
- maximum active hypotheses;
- team-specific confirmation evidence;
- safe/read-only diagnostic checks;
- approval-required action list;
- incident terminology;
- verification/monitoring requirements;
- output detail.

## Semantic changes — treat as a new workflow version

Changing any of these can alter behavior materially:

- required-input preflight;
- evidence labels or their meaning;
- instruction/data authority boundary;
- `ADVISORY_ONLY` authority;
- ship/diagnostic state vocabulary;
- state transition rules;
- root-cause confirmation threshold;
- rules against invented runtime/test evidence;
- safety/approval requirements;
- fallback behavior;
- verification contract.

Do not assume a modified version inherits Prompt Machine evidence.

## Adaptation record

For a material adaptation, write down:

```text
BASE WORKFLOW / VERSION
JOB / TEAM CONTEXT
WHAT CHANGED
WHY IT CHANGED
EXPECTED BENEFIT
POSSIBLE REGRESSION
HOW YOU WILL VERIFY IT
```

## Example — Code Review

Safe adaptation:

> Require PostgreSQL migration compatibility and authorization review for every database-affecting PR.

Semantic adaptation:

> Remove `QUESTION` because the team wants only definitive findings.

The second change alters uncertainty semantics and should be treated as a new workflow version requiring evaluation.

## Example — Bug Diagnosis

Safe adaptation:

> Limit active hypotheses to 3 for on-call triage and require read-only checks first.

Semantic adaptation:

> Allow `CAUSE_CONFIRMED` whenever the issue disappears after a restart.

The second change weakens the causal confirmation threshold and should not inherit the original workflow evidence.

## Rule

> **Customize the workflow to your job; do not silently customize away the evidence discipline that makes the workflow trustworthy.**
