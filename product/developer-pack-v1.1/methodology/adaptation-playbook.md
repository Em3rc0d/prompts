# Adaptation Playbook — From Template to Team Workflow

Maturity: `DRAFT` — static methodology; no behavioral claim.

Purpose: turn a reusable Prompt Quarry template into a workflow that fits a real engineering team without destroying the evidence, decision, and verification semantics that make the template inspectable.

This playbook is not about making prompts longer. It is about deciding which operating choices should be explicit and stable.

---

## 1. Start from the consuming workflow, not the prompt

Before editing a template, identify where the result will be used.

Examples:

- pull-request review;
- architecture decision record;
- incident diagnosis;
- issue/ticket refinement;
- design review;
- release gate;
- internal tool or agent;
- customer-facing application feature.

Ask:

```text
Who supplies inputs?
Who consumes the result?
What decision can the result influence?
What mistake would be expensive?
What uncertainty must stay visible?
```

If those answers are unknown, prompt wording is premature.

## 2. Extract the minimum operating contract

Define five things first:

```text
OUTCOME
REQUIRED INPUTS
EVIDENCE BOUNDARY
DECISION / ESCALATION STATES
OUTPUT CONSUMER
```

Everything else should support one of those interfaces.

### Example

Vague request:

> Review our PRs carefully.

Operating contract:

```text
OUTCOME
Evidence-grounded findings + human ship recommendation.

REQUIRED INPUTS
Diff, intent, runtime context.

EVIDENCE BOUNDARY
No invented runtime/test/repository facts.

DECISION STATES
BLOCK / REVIEW_REQUIRED / SHIP_WITH_FIXES / NO_MATERIAL_ISSUE_FOUND.

OUTPUT CONSUMER
Human PR reviewer.
```

Now the template has something concrete to encode.

## 3. Classify configuration points

For each template field, classify it as one of:

- `INVARIANT` — should stay stable across most runs;
- `POLICY` — team choice that changes how the workflow behaves;
- `INSTANCE_INPUT` — supplied for each task/run;
- `OPTIONAL_CONTEXT` — used only when relevant;
- `DERIVED` — calculated or inferred from other inputs.

### Example: code review

| Field | Class | Example |
|---|---|---|
| evidence labels | INVARIANT | CONFIRMED / LIKELY / QUESTION |
| minimum reported severity | POLICY | MEDIUM |
| ship authority | POLICY | HUMAN_DECIDES |
| PR diff | INSTANCE_INPUT | current diff |
| test output | OPTIONAL_CONTEXT | CI output |
| overall risk | DERIVED | review result |

Why this matters:

If an `INSTANCE_INPUT` is baked permanently into prose, the workflow becomes hard to reuse.

If a `POLICY` is left implicit, repeated runs can silently change behavior.

## 4. Choose the evidence policy

Decide what the workflow is allowed to treat as evidence.

Configure:

- allowed source classes;
- whether external research is allowed;
- freshness expectations;
- citation expectations;
- local evidence labels;
- strongest conclusion threshold.

### Rule

A stronger conclusion must require stronger evidence, not stronger wording.

Examples:

```text
Code review:
BLOCK requires confirmed high/critical evidence.

Technical decision:
DECIDE cannot depend only on weak/old evidence for a critical criterion.

Incident diagnosis:
FIX_SUPPORTED requires evidence connecting the proposed cause to observed failure.
```

## 5. Define decision states before writing recommendations

Stable states make workflows repeatable.

Bad:

> Tell me if this is good to ship.

Better:

```text
BLOCK
REVIEW_REQUIRED
SHIP_WITH_FIXES
NO_MATERIAL_ISSUE_FOUND
```

Then define transitions:

```text
confirmed HIGH+ defect -> BLOCK
material uncertainty on critical path -> REVIEW_REQUIRED
bounded issues -> SHIP_WITH_FIXES
no material supported issue -> NO_MATERIAL_ISSUE_FOUND
```

This does not remove human judgment. It makes the operating semantics inspectable.

## 6. Bind the output to a consumer

Do not return sections just because they look professional.

For each output field ask:

> Who uses this next?

Examples:

### PR reviewer

Needs:
- finding;
- location;
- evidence;
- failure mechanism;
- fix;
- verification;
- ship recommendation.

### ADR

Needs:
- decision status;
- constraints;
- considered options;
- evidence/assumptions;
- recommendation;
- reversal triggers.

### Incident workflow

Needs:
- observations;
- ranked hypotheses;
- discriminating checks;
- mitigation/fix state;
- verification.

Delete output sections that no consumer uses.

## 7. Separate policy from instance data

Where practical, store reusable policy outside the one-off prompt invocation.

Example representation:

```text
POLICY
review lenses = correctness, security, data integrity
report threshold = MEDIUM+
ship authority = human

INSTANCE
PR diff = ...
change intent = ...
test evidence = ...
```

This separation enables:

- forms;
- configs;
- generators;
- agents;
- repeatable team workflows;
- versioned policy changes.

## 8. Map the contract into a representation

Choose the representation that fits the consuming system.

### Markdown prompt

Best when humans copy/use/adapt manually.

### JSON/YAML contract

Best when tooling, forms, or generators need stable fields.

### Application config

Best when prompt policy is embedded in a product/workflow.

### Ticket/ADR template

Best when the workflow lives inside an engineering process.

Rule:

> Change representation without weakening semantics.

A field called `confidence: 0.82` is not a replacement for explicit evidence states unless the meaning of 0.82 is defined.

## 9. Run the static contract review

Before trying the workflow on a model, inspect it structurally.

Ask:

- Can I identify the required inputs?
- Can I tell what counts as evidence?
- Can I tell which assumptions are forbidden?
- Can I identify decision/escalation states?
- Can I identify the output consumer?
- Can I verify whether the output obeyed the contract?
- Can I see what happens when evidence is insufficient?
- Can another engineer modify a policy choice without rewriting the workflow?

If not, fix the contract before evaluating runtime behavior.

## 10. Then evaluate runtime behavior separately

Static quality is not behavioral evidence.

A configured workflow may be coherent and still perform poorly with a particular model/task/context.

Keep the layers separate:

```text
STATIC CONTRACT
Does the workflow have coherent interfaces and boundaries?

RUNTIME OBSERVATION
What did a model actually do on controlled cases?

COMPARATIVE EVIDENCE
Did one version perform better under a defined protocol?
```

Prompt Quarry F4–F7 labels require their own governed evidence.

## 11. Change-control rule

When a team changes a reusable workflow, record which class changed:

```text
INPUT SHAPE
POLICY
EVIDENCE SEMANTICS
DECISION TRANSITION
OUTPUT CONTRACT
WORDING ONLY
```

Changes to evidence semantics, decision transitions, or output contracts deserve stronger review than wording-only changes because they can change workflow behavior and downstream interpretation.

## 12. Adaptation anti-patterns

### Persona inflation

Adding “You are an elite world-class engineer” without changing task semantics.

### Section inflation

Adding headings that no consumer uses.

### Hidden policy

Writing “be strict” instead of defining a reporting threshold.

### Fake precision

Using numerical scores/confidence without defined semantics.

### Evidence collapse

Removing distinctions between observed facts and inference to make output shorter.

### Decision forcing

Requiring a winner when the evidence supports `HOLD` or `REVIEW_REQUIRED`.

### Template cloning

Copying an entire finished prompt and changing nouns instead of identifying reusable policy.

## 13. Completion test

An adaptation is ready for runtime evaluation when another engineer can answer, from the workflow alone:

```text
What does it need?
What may it believe?
What must it not invent?
What policy choices are configured?
What states can it return?
What does it promise to output?
How do I inspect compliance?
What happens when it cannot know?
```

If those answers are explicit, the workflow is ready to be tested.

It is not automatically `TESTED`, `IMPROVED`, `CERTIFIED`, or `PORTABLE`.
