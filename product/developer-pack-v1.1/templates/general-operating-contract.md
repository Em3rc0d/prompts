# General Operating Contract Template

Maturity: `DRAFT` — reusable architecture; no behavioral claim.

Use this template when you need to turn a recurring AI-assisted task into an explicit operating contract rather than a one-off prompt.

The customer should configure the marked fields. Remove sections that do not affect execution.

---

## 0. WORKFLOW IDENTITY

Workflow name:

`[WORKFLOW_NAME]`

Workflow owner / consumer:

`[TEAM / ROLE / APPLICATION / INDIVIDUAL]`

Primary outcome:

`[WHAT MUST BE TRUE WHEN THIS WORKFLOW SUCCEEDS]`

Decision horizon / usage frequency:

`[ONE-OFF / PER PR / DAILY / PER INCIDENT / PER DECISION / OTHER]`

## 1. INPUT CONTRACT

### Required inputs

The workflow must not claim completion without these inputs:

- `[REQUIRED_INPUT_1]`
- `[REQUIRED_INPUT_2]`

### Optional inputs

Use when supplied, but do not block execution if absent:

- `[OPTIONAL_INPUT_1]`
- `[OPTIONAL_INPUT_2]`

### Input validation

Before executing:

1. identify missing required inputs;
2. identify contradictory inputs;
3. identify inputs whose meaning is ambiguous enough to change the result;
4. ignore filler that cannot materially affect the answer.

Input state must be one of:

- `READY`
- `READY_WITH_UNKNOWNS`
- `BLOCKED`

If `BLOCKED`, return only the minimum information needed to unblock the task.

## 2. CONTEXT BOUNDARY

Allowed context:

`[FILES / USER-PROVIDED TEXT / DOCUMENTS / DATA / SYSTEM CONTEXT / TOOL RESULTS]`

Disallowed assumptions:

- `[ASSUMPTION_OR_SOURCE_CLASS_1]`
- `[ASSUMPTION_OR_SOURCE_CLASS_2]`

Context rule:

> Information not present in the allowed context is `UNKNOWN` unless the workflow explicitly permits external research or tool use.

If external research is permitted, define:

- allowed source classes: `[OFFICIAL DOCS / PRIMARY SOURCES / OTHER]`;
- freshness requirement: `[NONE / DATE / MAX AGE]`;
- citation requirement: `[YES / NO / WHEN]`.

## 3. EVIDENCE POLICY

Choose or adapt evidence labels for this workflow.

Default:

- `OBSERVED` — directly present in supplied or retrieved evidence;
- `SOURCE_CLAIM` — stated by an identified source but not independently verified;
- `INFERRED` — reasoned from evidence;
- `ASSUMPTION` — required to proceed but not established;
- `UNKNOWN` — not established.

Rules:

- never promote `INFERRED`, `ASSUMPTION`, or `UNKNOWN` to `OBSERVED`;
- never turn absence of evidence into evidence of absence unless the workflow justifies that inference;
- identify the evidence source for claims that can materially change the outcome;
- if the evidence state does not support the requested certainty, downgrade the decision state rather than inventing confidence.

### Evidence threshold

Configure the minimum evidence required for the workflow's strongest conclusion:

`[EXAMPLE: 1 DIRECT OBSERVATION + NO CONTRADICTING EVIDENCE]`

## 4. OPERATING CONSTRAINTS

### Must

- `[REQUIRED_BEHAVIOR]`
- `[REQUIRED_BEHAVIOR]`

### Must not

- `[FORBIDDEN_BEHAVIOR]`
- `[FORBIDDEN_BEHAVIOR]`

### Preserve

- `[API / BEHAVIOR / DATA / TONE / COMPATIBILITY / POLICY BOUNDARY]`

### Optimization priority

Order priorities explicitly when trade-offs exist:

1. `[PRIORITY_1]`
2. `[PRIORITY_2]`
3. `[PRIORITY_3]`

## 5. EXECUTION PROCESS

Configure the task-specific procedure.

Default scaffold:

1. **Normalize the request**
   - restate the real task;
   - separate requested outcome from suggested implementation.

2. **Validate inputs**
   - apply the input contract;
   - surface blockers and material unknowns.

3. **Build an evidence ledger**
   - identify evidence that can change the result;
   - label its state.

4. **Execute the domain task**
   - `[TASK-SPECIFIC PROCEDURE]`.

5. **Challenge the result**
   - look for contradictions;
   - identify fragile assumptions;
   - identify missing evidence that could reverse the conclusion.

6. **Choose a decision state**
   - use the configured decision policy below.

7. **Verify against the output contract**
   - do not finalize until required sections and boundaries are satisfied.

## 6. DECISION / ESCALATION POLICY

Define stable workflow states.

Default:

- `COMPLETE` — contract satisfied with sufficient evidence;
- `COMPLETE_WITH_UNKNOWNS` — useful result produced, but named uncertainty remains;
- `NEEDS_REVIEW` — a human/domain decision is required;
- `BLOCKED` — required information is absent;
- `UNSUPPORTED` — requested conclusion cannot be justified from allowed evidence.

Configure transition rules:

```text
[CONDITION] -> [STATE]
[CONDITION] -> [STATE]
```

Do not choose a stronger state merely to make the answer feel decisive.

## 7. OUTPUT CONTRACT

Return exactly the sections required by the consuming workflow.

Suggested contract:

### A. Status
`[CONFIGURED DECISION STATE]`

### B. Result
`[PRIMARY DELIVERABLE]`

### C. Evidence ledger
| Claim / input | Evidence | State | Consequence |
|---|---|---|---|
| ... | ... | ... | ... |

### D. Material unknowns
Only unknowns that can change the result.

### E. Recommended next action
`[ACTION / OWNER / CONDITION]`

### F. Verification
How the consumer can check the result.

Remove sections that your real integration does not consume.

## 8. VERIFICATION CONTRACT

Before finalizing, verify:

- required inputs were handled according to policy;
- no forbidden source or assumption was silently introduced;
- material claims have an evidence state;
- the strongest conclusion meets the configured evidence threshold;
- requested constraints are preserved;
- the output contract is complete;
- unresolved uncertainty is visible;
- the next action is consistent with the decision state.

Verification result:

- `CONTRACT_PASS`
- `CONTRACT_PASS_WITH_UNKNOWNS`
- `CONTRACT_FAIL`

A `CONTRACT_PASS` is local workflow validation only. It is not Prompt Quarry F4/F5/F6/F7 evidence.

## 9. FALLBACK CONTRACT

If the workflow cannot responsibly complete:

1. return `BLOCKED`, `NEEDS_REVIEW`, or `UNSUPPORTED`;
2. preserve any safe partial result;
3. list the smallest additional evidence set that could change the state;
4. do not pad the answer with generic advice.

## 10. ADAPTATION MAP

When adapting this template, decide these points explicitly:

| Configuration point | Current value | Why it matters |
|---|---|---|
| Required inputs | `[VALUE]` | Determines when execution is allowed |
| Allowed context | `[VALUE]` | Defines provenance boundary |
| Evidence labels | `[VALUE]` | Defines certainty semantics |
| Evidence threshold | `[VALUE]` | Controls strongest allowed conclusion |
| Must / must-not rules | `[VALUE]` | Encodes workflow invariants |
| Decision states | `[VALUE]` | Makes escalation repeatable |
| Output contract | `[VALUE]` | Connects prompt to consumer |
| Verification | `[VALUE]` | Makes results inspectable |

## 11. INTEGRATION NOTES

This operating contract can be mapped into:

- a reusable prompt;
- a form with required/optional fields;
- a JSON/YAML task contract;
- a ticket/issue template;
- an ADR workflow;
- a PR-review workflow;
- an agent/tool invocation;
- Prompt Quarry Generator inputs.

Preserve the semantics when changing representation. A JSON field is not useful if its meaning becomes weaker than the prose contract.
