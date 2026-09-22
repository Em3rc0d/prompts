# Verlune v1 — Human Review Gate

Status: `REVIEW CONTRACT / NOT YET EXECUTED`

Date: 2026-09-22

## Purpose

This is the gate between **product construction** and **landing redesign**.

The reviewer is not being asked whether Verlune "looks promising." The reviewer is deciding whether the actual product is coherent, useful, understandable and worth exposing publicly.

No averaging away blockers.

## Review inputs

Human review must use the exact candidate release surfaces:

- Product Model;
- Launch Scope;
- final Free launch-core assets;
- final Premium launch-core assets;
- Prompt Builder;
- Workflow Builder;
- Adaptation Guide;
- Evaluation Toolkit;
- customer-facing examples;
- evidence/limitations cards;
- candidate Premium access flow.

Do not review internal repository machinery as a substitute for the customer product.

## H1 — Product comprehension

A reviewer unfamiliar with internal Prompt Machine terminology should be able to state, after seeing the product:

- what Verlune is;
- what a Prompt is;
- what a Workflow is;
- what Free provides;
- what Premium adds;
- what the Builders do;
- where AI execution happens.

PASS only if no internal explanation is required to understand the basic product.

## H2 — Free usefulness

Select assets from multiple categories and perform real tasks.

PASS requires:

- the asset solves the stated bounded task;
- inputs are understandable;
- the result shape is useful;
- missing information is handled sensibly;
- verification guidance is actionable;
- the asset does not feel intentionally degraded.

Free must create trust, not frustration.

## H3 — Premium depth

Sample Premium Prompts and Premium Workflows across categories.

PASS requires a visible capability difference from Free through at least one of:

- deeper task decomposition;
- stronger input/context policy;
- richer decision semantics;
- adaptation;
- stronger fallback;
- advanced verification;
- specialization;
- reusable process structure.

"Longer wording" does not count.

## H4 — Prompt vs Workflow distinction

Give a reviewer both artifact types without explaining the intended distinction first.

PASS when the reviewer can correctly observe that:

- a Prompt is a reusable instruction for a bounded task;
- a Workflow governs a recurring process with stages/states/decisions where material.

If the two feel interchangeable, taxonomy is not ready.

## H5 — Prompt Builder

Starting only from a natural-language need, the reviewer must successfully create a reusable prompt.

PASS requires:

- low-friction intake;
- no dependency on prompt-engineering knowledge;
- materially useful generated prompt;
- clear reusable vs per-run inputs;
- sensible fallback/verification;
- no false certification language.

## H6 — Workflow Builder

Starting only from a natural-language recurring process, the reviewer must successfully create a reusable workflow.

PASS requires:

- trigger/outcome captured correctly;
- required inputs identified;
- stages make sense;
- decisions/states are not invented unnecessarily;
- material uncertainty remains visible;
- fallback works;
- output consumer is clear;
- resulting workflow can be reused on a second instance.

## H7 — Cross-category credibility

Review at least one launch-core asset in every public category.

PASS requires that Verlune does not feel like a developer product with decorative non-technical categories.

A category with weak filler content is a blocker or must be removed from launch.

## H8 — Free vs Premium purchase logic

Show the reviewer Free first, then Premium.

Ask:

> "Ignoring our internal effort, what do you actually get by paying?"

PASS only if the answer naturally mentions meaningful capabilities such as:

- deeper library;
- premium workflows;
- Builders;
- adaptation;
- evaluation.

If the answer is mainly "more prompts", FAIL.

## H9 — USD 9 test-purchase threshold

Ask the reviewer:

> "Does this product make you reasonably think: 'this may solve enough recurring AI work that I'd pay USD 9 to try it'?"

This is not a guarantee of market demand. It is a minimum product-coherence gate.

PASS requires the reviewer to identify concrete expected uses, not merely compliment presentation.

Record objections verbatim.

## H10 — Trust boundary

PASS requires:

- tested vs untested is distinguishable;
- generated vs certified is distinguishable;
- model/host limits are visible where relevant;
- no professional-substitution claim is implied;
- no guarantee of correctness is implied;
- limitations do not overwhelm ordinary product use.

Trust information should support purchase, not become the primary product.

## H11 — Friction

A reviewer should be able to move through:

```text
FIND ASSET
→ UNDERSTAND INPUTS
→ USE IN THEIR AI
→ GET RESULT
→ VERIFY
```

and for Premium:

```text
UNLOCK
→ FIND PREMIUM ASSET
→ USE
→ OPEN BUILDER
→ CREATE
→ REUSE
```

without needing repository knowledge.

Any step requiring manual discovery of internal Markdown paths is a UX defect.

## H12 — Final disposition

Allowed outcomes:

- `PASS_FOR_LANDING_REDESIGN`
- `PASS_WITH_NONBLOCKING_NOTES`
- `REWORK_REQUIRED`

`PASS_WITH_NONBLOCKING_NOTES` is allowed only when every blocking section H1–H11 passes.

## Review record

Record:

- exact commit/release candidate;
- reviewer;
- date;
- H1–H11 result;
- observed failures;
- objections;
- assets rejected;
- assets demoted to backlog;
- final disposition.

## Landing authorization

Only these outcomes authorize the landing rebuild:

- `PASS_FOR_LANDING_REDESIGN`
- `PASS_WITH_NONBLOCKING_NOTES`

`REWORK_REQUIRED` keeps the existing landing unchanged.
