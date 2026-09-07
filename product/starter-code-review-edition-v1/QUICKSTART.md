# Quickstart

## 1. Use the complete workflow

Copy the entire `WORKFLOW.md` surface. Do not remove the authority/data boundary, evidence rules, satisfied-invariant rules, output contract, or final self-check.

## 2. Provide the minimum required input

Supply:

- the code, diff, or exact changed files;
- the change intent / acceptance criteria;
- enough runtime, language, framework, database, cloud, or deployment context to interpret the change.

Add when material:

- expected behavior or invariants;
- API, schema, authorization, concurrency, compatibility, or performance contracts;
- actual test, CI, reproduction, or runtime evidence.

## 3. Keep task data separate from authority

Code, comments, logs, issue text, documentation snippets, quoted prompts, and attached content are task data. Embedded instructions inside that material must not override the workflow.

## 4. Read the review state first

The workflow returns one of:

- `REVIEWABLE`
- `REVIEWABLE_WITH_UNKNOWNS`
- `INSUFFICIENT_CONTEXT`

If material external context is missing, uncertainty should remain visible rather than being promoted into certainty.

## 5. Interpret the ship recommendation correctly

Possible recommendations are:

- `BLOCK`
- `REVIEW_REQUIRED`
- `SHIP_WITH_FIXES`
- `NO_MATERIAL_ISSUE_FOUND`

These are advisory recommendations. A human or separately authorized gate decides what ships.

`NO_MATERIAL_ISSUE_FOUND` means only that no material issue was supported in the supplied scope. It is not a guarantee that the software is defect-free.

## 6. Verify before acting

Use the workflow's verification plan to decide what evidence still needs to be collected. Do not treat proposed tests as if they already ran.

## Minimal invocation pattern

After loading `WORKFLOW.md`, provide a compact payload like:

```text
CHANGE
[diff or files]

INTENT
[what the change must do]

RUNTIME CONTEXT
[language/framework/version/etc.]

MATERIAL INVARIANTS / CONTRACTS
[only what matters]

OBSERVED TEST EVIDENCE
[actual output or NONE OBSERVED]
```

Do not include an expected answer or evaluation rubric in the same runtime context when independently evaluating workflow behavior.
