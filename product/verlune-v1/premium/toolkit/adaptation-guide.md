# Adapt a Verlune Prompt or Workflow

Status: `PREMIUM TOOLKIT CANDIDATE / NOT_FOR_SALE`

Use this guide to customize a Verlune asset without accidentally removing the behavior that made it useful.

## First rule

Change the **task-specific policy**, not random wording.

Before editing, identify which type of thing you are changing:

- `OUTCOME` — what success means;
- `INPUT` — information supplied each run;
- `CONTEXT` — stable background;
- `POLICY` — a reusable rule/threshold;
- `PROCESS` — how the task is performed;
- `STATE` — possible decision/result states;
- `OUTPUT` — what the consumer needs;
- `FALLBACK` — behavior when completion is not justified;
- `VERIFICATION` — how the result is checked;
- `WORDING_ONLY` — presentation without semantic change.

## Safe adaptation sequence

1. **Name the new use case.**
   What real task are you adapting the asset for?

2. **Preserve the outcome unless intentionally changing it.**
   A wording edit should not silently change the job.

3. **Separate stable policy from per-run data.**
   Do not bake today's example into the permanent artifact.

4. **Edit inputs deliberately.**
   If you add a required input, define what happens when it is absent.

5. **Edit constraints deliberately.**
   Avoid vague additions like "be strict" or "be expert." Define the behavior you mean.

6. **Check states and authority.**
   If you change when a workflow can return READY/PASS/DECIDE/etc., you changed workflow semantics.

7. **Check the output consumer.**
   Keep only fields somebody uses.

8. **Preserve fallback.**
   A shorter artifact must still know what to do when it cannot responsibly finish.

9. **Preserve verification.**
   Do not turn "sounds good" into the acceptance criterion.

10. **Retest.**
    A changed artifact does not automatically inherit previous runtime evidence.

## High-impact changes

Require stronger review:

- evidence semantics;
- hard constraints;
- authority;
- decision transitions;
- required inputs;
- fallback behavior;
- output contract.

## Lower-impact changes

Usually smaller risk, but still inspect:

- labels;
- examples;
- ordering;
- tone;
- formatting;
- wording that does not change meaning.

## Adaptation anti-patterns

Avoid:

- replacing nouns in a prompt and assuming the workflow now fits another domain;
- adding "world-class expert" instead of defining a real requirement;
- adding sections nobody uses;
- removing uncertainty labels to make output look cleaner;
- forcing a recommendation when the original allowed HOLD/BLOCKED;
- turning optional context into hidden required context;
- inventing numerical confidence scales with no meaning.

## Completion check

Before testing your adaptation, answer:

- What does it need?
- What is it allowed to assume?
- What must it not invent?
- What changed from the original?
- What states/results can it return?
- What happens when information is missing?
- What does the output consumer receive?
- How do I verify it?

If any answer is unclear, the adaptation is not ready for runtime testing.
