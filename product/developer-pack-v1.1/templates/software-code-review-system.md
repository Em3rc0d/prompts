# Software Code Review System Template

Maturity: `DRAFT` — reusable operating template; no behavioral claim.

Use this when you need a repeatable code-review workflow across repositories, PRs, patches, languages, and risk profiles.

Unlike a finished Code Review prompt, this template exposes the review policy itself as configuration.

---

## 0. REVIEW POLICY

Workflow name:

`[REVIEW_POLICY_NAME]`

Review target:

`[PR / DIFF / FILES / MODULE / CHANGESET]`

Change intent:

`[WHAT THE CHANGE IS SUPPOSED TO DO]`

Consumer:

`[AUTHOR / REVIEWER / TEAM / CI BOT / RELEASE GATE]`

Ship authority:

`[ADVISORY_ONLY / HUMAN_DECIDES / BLOCKING_GATE]`

## 1. INPUT CONTRACT

### Required

- code, diff, or exact changed files;
- change intent or acceptance criteria;
- runtime/language context sufficient to interpret the change.

### Conditionally required

Add when relevant:

- schema/API contract;
- database migration;
- authorization model;
- concurrency model;
- deployment/runtime constraints;
- compatibility requirements;
- observed test results;
- incident/reproduction evidence.

Input state:

- `REVIEWABLE`
- `REVIEWABLE_WITH_UNKNOWNS`
- `INSUFFICIENT_CONTEXT`

Do not manufacture defects to compensate for missing context.

## 2. REVIEW LENSES

Enable only lenses relevant to the change.

```text
[ ] correctness
[ ] regression risk
[ ] security / trust boundary
[ ] data integrity
[ ] reliability / error handling
[ ] concurrency / ordering
[ ] performance / resource use
[ ] API / schema compatibility
[ ] observability / operability
[ ] maintainability
[ ] tests / verification
[ ] custom: __________
```

A disabled lens should not generate filler commentary.

## 3. EVIDENCE POLICY

Finding evidence levels:

- `CONFIRMED` — failure mechanism is directly supported by supplied code/context;
- `LIKELY` — strong inference, but one material fact remains unobserved;
- `QUESTION` — context is needed before treating the concern as a defect;
- `DISMISSED` — candidate finding failed challenge/review and should not be reported.

Rules:

- cite the smallest useful code location or snippet;
- connect evidence → failure mechanism → impact;
- never claim runtime behavior or test success unless supplied evidence establishes it;
- never convert a risky pattern into a vulnerability without a reachable threat/missing control;
- preserve uncertainty explicitly.

### Reporting threshold

Configure:

```text
minimum evidence level to report: [CONFIRMED / LIKELY / QUESTION]
minimum severity to report:       [CRITICAL / HIGH / MEDIUM / LOW]
max findings:                     [N / UNLIMITED]
```

Default recommended policy for human PR review:

```text
report CONFIRMED + LIKELY
include QUESTION only when it can change ship decision
exclude pure style preferences
```

## 4. SEVERITY POLICY

Default rubric:

- `CRITICAL` — plausible catastrophic impact such as major compromise, irreversible data loss, or broad outage;
- `HIGH` — likely incorrect behavior, serious exposure, corruption, or major reliability failure;
- `MEDIUM` — meaningful bounded defect or operational/maintenance risk;
- `LOW` — minor issue worth fixing but unlikely to materially affect correctness or operations.

Teams may override definitions, but must document the override here:

`[TEAM_SEVERITY_POLICY]`

## 5. REVIEW PROCESS

### Phase A — reconstruct intent

1. State what the change appears intended to do.
2. Identify affected interfaces/state transitions.
3. Surface missing context that can materially change the review.

### Phase B — trace changed behavior

Inspect relevant paths for:

- invalid control flow;
- broken state transitions;
- incorrect assumptions about input shape;
- incomplete error handling;
- trust-boundary mistakes;
- data consistency problems;
- concurrency/order hazards;
- retry/idempotency issues;
- resource leaks/unbounded work;
- compatibility/regression risks.

### Phase C — generate candidate findings

For each candidate:

1. identify exact evidence;
2. state failure mechanism;
3. state impact;
4. assign evidence level;
5. assign severity;
6. identify context that could invalidate it.

### Phase D — challenge candidate findings

Reject a candidate if:

- it is style preference only;
- the failure mechanism cannot be explained;
- supplied context disproves it;
- it depends on an unstated assumption that cannot be defended;
- it duplicates a stronger finding;
- it has no material consequence under the configured policy.

### Phase E — prioritize

Order by:

1. severity;
2. evidence strength;
3. reachability/likelihood;
4. blast radius;
5. remediation urgency.

Do not bury a blocking defect under low-value notes.

## 6. SHIP DECISION POLICY

Configure permitted states:

- `BLOCK`
- `REVIEW_REQUIRED`
- `SHIP_WITH_FIXES`
- `SHIP`
- `NO_MATERIAL_ISSUE_FOUND`

Suggested transition rules:

```text
CONFIRMED CRITICAL/HIGH finding       -> BLOCK
LIKELY HIGH with material unknown      -> REVIEW_REQUIRED
bounded MEDIUM/LOW findings            -> SHIP_WITH_FIXES
no material supported finding          -> NO_MATERIAL_ISSUE_FOUND
insufficient context for key path       -> REVIEW_REQUIRED
```

The model may recommend a state. Human/CI authority is defined by `Ship authority` above.

## 7. OUTPUT CONTRACT

### 1. Review state

`REVIEWABLE | REVIEWABLE_WITH_UNKNOWNS | INSUFFICIENT_CONTEXT`

### 2. Executive assessment

- intended change;
- overall risk;
- highest-priority concern;
- ship recommendation.

### 3. Findings

For each accepted finding:

**[SEVERITY] — [TITLE]**

- Evidence level: `CONFIRMED | LIKELY | QUESTION`
- Location: `[FILE / SYMBOL / LINE / SNIPPET]`
- Evidence: `[WHAT SUPPORTS THE FINDING]`
- Failure mechanism: `[HOW IT BREAKS]`
- Impact: `[WHY IT MATTERS]`
- Recommended fix: `[SMALLEST USEFUL FIX]`
- Verification: `[HOW TO PROVE THE FIX]`
- Invalidating context: `[WHAT COULD CHANGE THIS FINDING]`
- Confidence: `high | medium | low`

### 4. Missing context

Only information that can materially change a finding or ship decision.

### 5. Verification plan

Include applicable checks:

- happy path;
- edge/boundary case;
- failure/retry path;
- security/authorization path;
- regression case;
- monitoring/observability confirmation.

### 6. Ship recommendation

One configured ship state plus rationale.

## 8. VERIFICATION CONTRACT

Before finalizing, verify:

- every finding maps to supplied evidence or a labeled inference;
- every finding explains a failure mechanism;
- severity matches configured rubric;
- no test result was invented;
- no disabled review lens produced filler;
- duplicate findings were merged;
- missing context is material, not generic;
- ship recommendation follows configured transition rules.

Local result:

- `REVIEW_CONTRACT_PASS`
- `REVIEW_CONTRACT_PASS_WITH_UNKNOWNS`
- `REVIEW_CONTRACT_FAIL`

This is local workflow validation, not Prompt Quarry F4–F7 evidence.

## 9. TEAM ADAPTATION MAP

Configure explicitly:

| Configuration | Example |
|---|---|
| Review lenses | correctness + security + data integrity |
| Severity policy | organization incident rubric |
| Reporting threshold | CONFIRMED/LIKELY MEDIUM+ |
| Ship authority | human reviewer |
| Max findings | 8 |
| Required verification | unit + integration + auth regression |
| Compatibility policy | no breaking API/schema change |

## 10. INTEGRATION SHAPES

This template can be bound to:

- pull-request review instructions;
- repository contribution guide;
- CI review gate;
- code-review agent;
- issue-generation workflow;
- security review precheck;
- Prompt Quarry Generator configuration.

When integrating, preserve the evidence and ship-decision semantics. Do not reduce them to an untyped `score` without explicit meaning.
