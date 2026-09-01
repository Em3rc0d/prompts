# Quickstart — Developer Starter Pack v1.1

This Pack is designed to be used, not read front-to-back.

## 1. Pick the workflow

Choose the prompt closest to the job:

- `prompts/code-review.md` — review code or a diff and produce evidence-ranked findings plus a ship decision.
- `prompts/bug-diagnosis.md` — diagnose a defect using observations, hypotheses, discriminating checks, and verification.
- `prompts/technical-decision.md` — compare technical options against hard constraints, evidence, trade-offs, and reversibility.

## 2. Fill only the inputs that can change the answer

Replace the bracketed placeholders with concrete information.

Good context changes the analysis. Filler only makes the prompt longer.

Useful inputs include:
- exact code/diff;
- expected behavior;
- versions and environment;
- hard constraints;
- real error/log evidence;
- decision criteria;
- known unknowns.

If a field does not apply, remove it instead of leaving an ambiguous placeholder.

## 3. Preserve evidence labels

The prompts deliberately separate facts from inference.

Do not delete those boundaries just because a shorter answer looks cleaner.

A practical rule:

`OBSERVED / SUPPLIED FACT → INFERENCE → RECOMMENDATION`

If the first step is missing, the later steps should not be presented as certainty.

## 4. Use the output contract

Do not ask the model for “thoughts”.

The output sections are part of the prompt's interface. They make the answer easier to inspect, compare, and reuse.

Examples:
- Code Review ends with a `SHIP DECISION`.
- Bug Diagnosis distinguishes `DIAGNOSE_FIRST`, `MITIGATE_NOW`, and `FIX_SUPPORTED`.
- Technical Decision distinguishes `DECIDE`, `CONDITIONAL`, and `HOLD`.

## 5. Run one real task

Do not evaluate the Pack from the template alone.

Use one prompt on a task you already understand well enough to judge.

Check:
- Did it ask for the right missing context?
- Did it separate evidence from assumption?
- Did it avoid inventing certainty?
- Was the output immediately usable?
- Which section would you remove or change for your workflow?

## 6. Adapt deliberately

You are allowed to adapt the prompts for your authorized work under `LICENSE.md`.

Good adaptations:
- replace generic criteria with your team's actual review rubric;
- add system-specific constraints;
- remove irrelevant sections;
- bind the output contract to a ticket, ADR, PR review, or incident workflow.

Bad adaptation:
- adding sections only to make the prompt look sophisticated.

## 7. Keep the evidence boundary honest

These prompts are engineered and statically structured.

Distribution of this Pack does **not** establish F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE`.

Runtime behavior must be observed separately.

## Want the reusable system behind these prompts?

Developer Pack adds reusable prompt architecture, task/request contracts, methodology, worked transformations, and quality/release gates for building your own governed prompt workflows.

The Starter Pack should prove the design philosophy on real work first.
