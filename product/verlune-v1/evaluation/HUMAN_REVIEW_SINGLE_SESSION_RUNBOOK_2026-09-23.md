# Verlune v1 — Single-Session Human Review Runbook

Status: `READY_TO_EXECUTE_AFTER_CURRENT_STAGING_REDEPLOY`

Date: 2026-09-23

## Goal

Execute H1-H11 in one reviewer session without exposing repository internals or making the reviewer repeat engineering tests.

The reviewer should not be coached on what answer is desired. Record objections verbatim.

## Reviewer

Use one person who:
- did not build Prompt Machine / Verlune;
- has used an AI assistant before;
- has not been taught the internal Prompt / Workflow taxonomy in advance.

The builder/operator may observe and take notes, but should not explain the product unless the runbook explicitly asks for a question.

## Candidate surface

Use the current staging alias:

`https://prompt-quarry-stage.vercel.app`

The candidate must include the latest customer-preview cleanup before review.

## One-session sequence

### A. Cold product comprehension — H1

Open the product without explaining it.

Ask the reviewer:

1. What is Verlune?
2. What is a Prompt here?
3. What is a Workflow here?
4. What do you get for free?
5. What does Premium add?
6. What do the Builders do?
7. Where does the AI actually run?

Record the answer before correcting anything.

### B. Free usefulness — H2

Have the reviewer choose and use Free assets from at least three different categories on real tasks.

For each, record:
- task attempted;
- whether inputs were understandable;
- whether missing information behavior made sense;
- whether the result was useful;
- whether verification guidance was actionable.

Do not select only developer assets.

### C. Premium depth + taxonomy — H3 / H4

Unlock Premium using the Test entitlement.

Show one Premium Prompt and one Premium Workflow from different categories without explaining the distinction.

Ask:
- What feels materially stronger than Free?
- What is the difference between this Prompt and this Workflow?

PASS requires a capability/process distinction, not merely “one is longer.”

### D. Prompt Builder — H5

Open Prompt Builder.

Reviewer starts from one natural-language recurring need of their own.

They should:
- copy the Builder;
- run it in their normal compatible AI assistant;
- answer its intake;
- obtain a reusable prompt;
- identify what changes per run;
- run the quick test.

Record any point where operator explanation was needed.

### E. Workflow Builder — H6

Use one real recurring process from the reviewer.

Reviewer should:
- run Workflow Builder;
- obtain a workflow;
- apply it to one instance;
- identify whether it could be reused on a second instance.

Record invented states/decisions, missing fallback, or unclear output consumer as blockers.

### F. Cross-category credibility — H7

Browse every public launch category.

The reviewer must identify any category that feels like filler, decorative expansion, or notably weaker than the rest.

Record exact rejected assets/categories.

### G. Purchase logic + USD 9 threshold — H8 / H9

Show Free first, then Premium.

Ask exactly:

> Ignoring our internal effort, what do you actually get by paying?

Then ask exactly:

> Does this product make you reasonably think: “this may solve enough recurring AI work that I’d pay USD 9 to try it”?

Do not argue with the answer.

Record:
- concrete expected uses;
- objections;
- anything they expected but could not find.

### H. Trust boundary — H10

Ask the reviewer to explain:
- what has actually been tested;
- what “generated” means;
- whether anything appears universally certified;
- whether Verlune appears to replace professional judgment;
- whether correctness is guaranteed.

PASS requires no materially false interpretation caused by the product.

### I. End-to-end friction — H11

Without repository help, reviewer performs:

```text
FREE:
find asset → understand inputs → use in AI → get result → verify

PREMIUM:
unlock → find Premium asset → use → open Builder → create → reuse
```

Record every point where they:
- get lost;
- need an internal path;
- cannot tell what to click/copy;
- cannot tell what input is expected;
- cannot recover from an error.

## Result

Score each H1-H11 only:

- `PASS`
- `FAIL`

Do not average failures away.

Final disposition:
- `PASS_FOR_LANDING_REDESIGN`
- `PASS_WITH_NONBLOCKING_NOTES`
- `REWORK_REQUIRED`

Any H1-H11 FAIL forces `REWORK_REQUIRED`.

## Minimal record to return

The operator only needs to return:

```text
Reviewer:
Date:
Candidate URL/commit:

H1 PASS/FAIL — note
H2 PASS/FAIL — note
H3 PASS/FAIL — note
H4 PASS/FAIL — note
H5 PASS/FAIL — note
H6 PASS/FAIL — note
H7 PASS/FAIL — note
H8 PASS/FAIL — note
H9 PASS/FAIL — objection verbatim
H10 PASS/FAIL — note
H11 PASS/FAIL — note

Rejected assets/categories:
Other objections:
Final disposition:
```

No additional engineering stress test is required during this human review.
