# Quickstart — Developer Pack v1.1

Status: `DRAFT / NOT FOR SALE`

Goal: configure one reusable engineering workflow from the Pack and make it inspectable before you spend time tuning wording.

You do not need to read every file first.

## 1. Choose the closest system template

Start with one:

- `templates/software-code-review-system.md` — PR/code review policy;
- `templates/technical-research-decision-system.md` — architecture, vendor, migration, build-vs-buy, tool/dependency decisions;
- `templates/general-operating-contract.md` — recurring technical workflow that does not fit the two specialized systems.

Do not choose by prompt length. Choose by the decision/process you need to make repeatable.

## 2. Write the consuming workflow in one sentence

Examples:

```text
Review every backend PR using our evidence and ship policy.

Create ADR-ready comparisons for infrastructure decisions.

Diagnose production defects without jumping from symptom to fix.
```

Then identify:

```text
WHO supplies inputs?
WHO consumes the result?
WHAT decision can it influence?
WHAT failure would be expensive?
```

These answers drive the configuration.

## 3. Configure policy before instance data

Separate reusable policy from per-run inputs.

### Policy

Stable across many runs:

- evidence labels;
- allowed source classes;
- severity/decision thresholds;
- review lenses;
- must/must-not rules;
- output contract;
- escalation states;
- authority.

### Instance data

Changes each run:

- current code/diff;
- current error/logs;
- current options;
- current requirements;
- current evidence.

If you bake instance data into reusable policy, you make the system harder to reuse.

If you leave policy implicit, repeated runs can silently change behavior.

## 4. Use the Adaptation Playbook

Open:

`methodology/adaptation-playbook.md`

Classify important fields as:

```text
INVARIANT
POLICY
INSTANCE_INPUT
OPTIONAL_CONTEXT
DERIVED
```

Then make the team choices explicit.

Example for PR review:

```text
review_lenses       correctness, security, data integrity
minimum_severity    MEDIUM
report_evidence     CONFIRMED + LIKELY
ship_authority      HUMAN_DECIDES
confirmed_HIGH+     BLOCK
likely_HIGH         REVIEW_REQUIRED
```

## 5. Inspect the worked transformation

Open:

`examples/code-review-policy-transformation.md`

Follow the path:

```text
vague request
  ↓
workflow requirements
  ↓
configured policy
  ↓
operating prompt
  ↓
inspection checklist
```

The important part is not the final wording. It is seeing which semantics became stable configuration.

## 6. Use the machine-readable contract when useful

Files:

- `contracts/workflow-contract.schema.json`
- `contracts/code-review-policy.example.json`

The schema represents the same operating concepts used by the Markdown templates:

```text
inputs
context_policy
evidence_policy
constraints
process
decision_policy
output_contract
verification
fallback
```

Use it when you want to map the workflow into:

- a form;
- JSON/YAML configuration;
- an internal tool;
- an agent invocation;
- Prompt Quarry Generator inputs.

Do not convert a workflow to JSON merely to make it look technical. Use machine-readable representation when another system benefits from stable fields.

## 7. Run the static review

Open:

`checklists/workflow-static-review.md`

Do not run a behavioral comparison yet if the workflow cannot answer:

```text
What does it need?
What may it treat as evidence?
What must it not invent?
What states can it return?
What output does it promise?
How do I inspect compliance?
What happens when it cannot know?
```

Choose a static state:

```text
STATIC_READY_FOR_RUNTIME_TEST
STATIC_READY_WITH_KNOWN_GAPS
STATIC_REWORK_REQUIRED
```

## 8. Run one real task you can judge

Use a task where you already understand enough of the domain to evaluate the result.

Do not judge the workflow only by whether the answer sounds polished.

Inspect:

- Did it respect the evidence policy?
- Did it handle missing inputs according to contract?
- Did it use the intended decision state?
- Did it satisfy the output contract?
- Did it make unsupported claims?
- Was the result useful to the actual downstream consumer?

Record observations separately from the template itself.

## 9. Change one policy at a time when tuning

Examples:

- minimum reporting severity;
- evidence threshold;
- source freshness requirement;
- ship/decision transition;
- enabled review lens;
- output section.

Changing many semantics at once makes it difficult to understand why behavior changed.

## 10. Keep product evidence states separate

A well-designed workflow can still behave poorly at runtime.

A good result on one task can still fail elsewhere.

Therefore:

```text
STATIC CONTRACT PASS
    !=
F4 TESTED
    !=
F5 IMPROVED
    !=
F6 CERTIFIED
    !=
F7 PORTABLE
```

Prompt Quarry's product evidence labels require their own governed protocols and receipts.

## Suggested first 15-minute exercise

1. Open `templates/software-code-review-system.md`.
2. Choose 4–6 review lenses your team actually cares about.
3. Set evidence/reporting thresholds.
4. Define who has ship authority.
5. Define `BLOCK` and `REVIEW_REQUIRED` transitions.
6. Paste one real PR/diff as instance input.
7. Run the workflow.
8. Inspect it with `checklists/workflow-static-review.md` and your own knowledge of the change.

If that exercise feels like configuring a reusable engineering policy rather than collecting another prompt, Developer Pack is doing its job.
