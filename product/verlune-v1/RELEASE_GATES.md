# Verlune v1 — Catalog and Release Gates

Status: `CANDIDATE GOVERNANCE`

Date: 2026-09-22

## Purpose

Prevent the new Verlune positioning from becoming a larger but weak prompt pack.

A catalog entry is a candidate until it earns its customer-facing state.

```text
SOURCE / IDEA
   ↓
CANDIDATE
   ↓
STRUCTURE CHECKED
   ↓
RUNTIME TESTED
   ↓
HUMAN REVIEWED
   ↓
RELEASE ELIGIBLE
   ↓
FREE or PREMIUM CATALOG
```

`CERTIFIED` remains a stronger optional state with its own governed evidence.

## Gate 0 — Commercial usefulness

Before prompt engineering, answer:

- What recognizable problem does this asset solve?
- Who encounters the problem?
- Why would they reuse the asset?
- What does the user have at the end?
- Can a normal user understand when to use it?
- Is it materially distinct from another catalog entry?

Reject candidates that exist primarily to increase item count.

## Gate 1 — Classification

Every candidate must declare:

- category;
- artifact type: prompt or workflow;
- tier candidate: Free or Premium;
- customer outcome;
- required inputs;
- intended output;
- authority boundary;
- target runtime/model scope if any.

Free/Premium is not decided by length.

## Gate 2 — Static structure

### Prompt minimum

- explicit outcome;
- required inputs;
- material optional context;
- constraints;
- executable instructions;
- output contract;
- missing-information behavior;
- verification guidance.

### Workflow minimum

All prompt requirements plus:

- trigger;
- stages;
- state transitions or decision states where material;
- fallback / blocked semantics;
- output consumer;
- verification at workflow level.

Critical static ambiguity is a blocker.

## Gate 3 — Free runtime minimum

Before a Free asset is publicly promoted, require at least:

1. one normal-case execution;
2. one missing/ambiguous-input execution;
3. human review of both;
4. no known critical instruction-following or fabrication failure;
5. explicit known limitations;
6. exact version identity.

This minimum does not imply portability or certification.

## Gate 4 — Premium Prompt runtime minimum

A Premium Prompt requires a stronger test set:

1. normal case;
2. minimal or missing-input case;
3. ambiguous/noisy case;
4. adversarial or instruction-conflict case;
5. human review;
6. versioned result;
7. known limitations;
8. no unresolved critical failure.

If a Premium Prompt has a Free sibling, Premium must demonstrate a material capability difference rather than cosmetic wording.

## Gate 5 — Premium Workflow runtime minimum

A Premium Workflow requires:

- normal case;
- missing critical input;
- ambiguity/noise;
- contradictory input;
- adversarial embedded instruction where relevant;
- repeatability check;
- state/fallback behavior review;
- output-contract review;
- verification-behavior review;
- exact version identity;
- known limitations.

Certification may impose stricter requirements.

## Gate 6 — Builder productization

Prompt Builder and Workflow Builder are product-critical. They cannot launch based only on static methodology.

Minimum Builder test matrix must span multiple categories, for example:

- Development & Tech;
- Study & Learning;
- Research & Analysis;
- Business & Operations;
- Writing & Communication;
- Content & Marketing;
- Planning & Productivity;
- Career & Job Search.

For each Builder, verify that:

- a non-expert can start from a plain-language need;
- questions are limited to material missing information;
- internal terminology is hidden or explained;
- the generated artifact preserves the requested goal;
- required inputs are explicit;
- unsupported assumptions remain visible;
- output/fallback/verification behavior is usable;
- the Builder does not silently claim certification;
- the final artifact can be copied and reused;
- at least one generated artifact is subsequently executed and reviewed.

Runtime/model compatibility claims require separate observed evidence.

## Gate 7 — Catalog balance

Before launch, inspect the catalog as a customer.

Requirements:

- no category exists only as a decorative empty shell;
- Free demonstrates breadth;
- Premium demonstrates meaningful additional depth;
- Development does not dominate the entire brand;
- near-duplicates are rejected or consolidated;
- titles describe customer outcomes rather than prompt-engineering techniques;
- high-stakes professional domains are not introduced without dedicated safety review.

## Gate 8 — Premium value review

Ask a cold question:

> If the buyer ignores our internal engineering work, does the delivered product still feel worth testing for USD 9?

PASS requires the answer to be supported by the actual customer surface:

- useful Premium prompts;
- useful Premium workflows;
- Prompt Builder;
- Workflow Builder;
- adaptation support;
- evaluation support;
- clear examples;
- easy access.

Hashes, certification receipts and internal complexity may support trust but cannot substitute for customer value.

## Gate 9 — Access and execution

Before public Premium sale:

- purchase path succeeds;
- entitlement/license is created as intended;
- Verlune can validate entitlement server-side;
- invalid/revoked entitlement fails closed;
- successful customer unlock creates the intended session;
- Premium content is not accidentally public;
- Builder copy/open flow works;
- customer can execute the Builder in each assistant for which compatibility is claimed;
- no provider secret is exposed client-side.

## Gate 10 — Website claim audit

Every public claim must map to current evidence.

Prohibited without evidence:

- works with every AI;
- guaranteed better answers;
- never hallucinates;
- all prompts are certified;
- customer-generated workflows are certified;
- lifetime future content;
- unlimited hosted AI;
- measurable productivity gains;
- professional medical/legal/financial substitution.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Launch gate

```text
PRODUCT_MODEL_FROZEN
CATALOG_V1_FROZEN
FREE_RELEASE_ASSETS_PASS
PREMIUM_RELEASE_ASSETS_PASS
PROMPT_BUILDER_PASS
WORKFLOW_BUILDER_PASS
PREMIUM_VALUE_REVIEW_PASS
ENTITLEMENT_E2E_PASS
PUBLIC_SITE_CLAIM_AUDIT_PASS
COMMERCE_E2E_PASS
        ↓
READY_TO_LAUNCH
```

If any required gate is open, public distribution remains intentionally limited.
