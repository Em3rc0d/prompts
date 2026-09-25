# Developer Pack v1.1 — Commercial Value Gate

Status: `BLOCKING`

Purpose: prevent a technically valid paid pack from shipping when the customer-visible value is not materially stronger than the Free Developer Starter Pack v1.1.

This gate is about product value, not F4–F7 behavioral evidence.

## Gate question

> After using the Free Starter Pack, would a developer immediately understand why paying for Developer Pack v1.1 saves meaningful design, adaptation, review, and governance work?

If the answer is unclear, the candidate fails.

## Comparison baseline

Free Developer Starter Pack v1.1 provides three finished field-ready workflows:

- Code Review;
- Bug Diagnosis;
- Technical Decision.

A Paid asset must not justify itself merely by being longer, having more headings, or repeating those workflows with different wording.

## Blocking dimensions

Score each dimension `0`, `1`, or `2`.

- `0` — no meaningful advantage over Free;
- `1` — partial advantage, but customer value is still ambiguous;
- `2` — clear, usable advantage that reduces real setup/review work.

### 1. Reuse breadth

Can the asset be reused across multiple concrete workflows without rebuilding its operating logic from scratch?

### 2. Parameterization

Does the asset expose the decisions a customer actually needs to configure, instead of hiding them inside prose?

Examples:
- evidence threshold;
- severity policy;
- review lenses;
- fallback behavior;
- required inputs;
- output shape;
- decision threshold.

### 3. Governance

Does the asset help the customer preserve boundaries across repeated use?

Examples:
- fact vs inference rules;
- forbidden claims;
- escalation states;
- missing-context handling;
- stable decision statuses.

### 4. Verification

Does the asset define how a user can inspect whether the result satisfied the workflow contract?

### 5. Adaptation speed

Does the asset include enough guidance that a developer can adapt it to a team/product workflow without reverse-engineering why each section exists?

### 6. Integration value

Can the asset map cleanly into real engineering surfaces such as:
- PR review;
- ADR;
- incident workflow;
- issue/ticket;
- architecture review;
- API/tooling integration;
- generator configuration.

### 7. Inspectability

Can another engineer review the configured workflow and understand:
- what inputs it expects;
- what evidence it may use;
- what decisions it may make;
- what uncertainty remains;
- what output it promises?

## Pass criteria

For each **core template**:

```text
minimum total score      12 / 14
no dimension             0
parameterization         2
verification             2
governance               2
```

For the **Pack as a whole**:

```text
Free prompt clone test           PASS
worked transformation test       PASS
team adaptation test             PASS
machine/repeatable boundary      PASS
customer value statement         PASS
```

## Free prompt clone test

Ask:

> Could a customer get substantially the same capability by copying one Free prompt and replacing domain nouns?

If `YES`, the Paid asset fails.

## Worked transformation test

At least one example must show:

```text
vague request
  ↓
requirements extraction
  ↓
configured template
  ↓
final operating prompt/workflow
  ↓
inspection against contract
```

A simple before/after wording rewrite does not pass.

## Team adaptation test

At least one customer-facing guide must demonstrate how to convert a generic template into a team-specific workflow by changing explicit configuration points rather than rewriting the whole prompt.

## Machine/repeatable boundary test

The Pack must expose stable fields or contracts that can be represented in code, configuration, forms, or generator inputs where appropriate.

The customer should not be forced to parse prose to discover the operational interface.

## Customer value statement test

The following statement must be true on inspection:

> The Free Pack gives me three strong prompts. Developer Pack gives me the construction and governance system I can reuse to build many of my own workflows.

If the product cannot demonstrate that statement through its files, do not ship it.

## Non-evidence rule

Passing this gate does **not** establish:

- F4 `TESTED`;
- F5 `IMPROVED`;
- F6 `CERTIFIED`;
- F7 `PORTABLE`;
- behavioral superiority over another prompt.

It establishes only that the paid product has a defensible static customer-value distinction from the Free Pack.

## Release rule

`COMMERCIAL_VALUE_GATE = PASS` is mandatory before v1.1 can enter release-candidate packaging.

Until then:

```text
sale_status = NOT_FOR_SALE
checkout    = DISABLED
```
