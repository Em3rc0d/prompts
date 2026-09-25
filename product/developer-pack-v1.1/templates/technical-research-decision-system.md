# Technical Research / Decision System Template

Maturity: `DRAFT` — reusable operating template; no behavioral claim.

Use this when you need a repeatable architecture, build-vs-buy, vendor, dependency, migration, platform, or tooling decision workflow.

Unlike a finished Technical Decision prompt, this template exposes decision policy, evidence quality, source freshness, reversibility, and escalation as configuration.

---

## 0. DECISION POLICY

Decision name:

`[DECISION_NAME]`

Decision owner:

`[PERSON / TEAM / ROLE]`

Decision to make:

`[ONE-SENTENCE DECISION]`

Options:

- `[OPTION_A]`
- `[OPTION_B]`
- `[OPTION_C]`
- `[STATUS_QUO / BUILD / BUY / DEFER / OTHER]`

Decision horizon:

`[REVERSIBLE_IN_DAYS / REVERSIBLE_IN_MONTHS / EXPENSIVE_TO_REVERSE / EFFECTIVELY_IRREVERSIBLE]`

Decision deadline:

`[DATE / EVENT / NONE]`

## 1. CONTEXT CONTRACT

System/product context:

`[ARCHITECTURE / USERS / SCALE / TEAM / BUSINESS / REGULATORY CONTEXT]`

Hard constraints:

- `[SECURITY / COMPLIANCE]`
- `[BUDGET]`
- `[DELIVERY]`
- `[PLATFORM / LANGUAGE / REGION]`
- `[OPERABILITY / SUPPORT]`
- `[OTHER]`

An option that violates a hard constraint is `NON_VIABLE` unless the constraint itself is explicitly changed.

Do not allow a weighted score to hide a hard-constraint violation.

## 2. DECISION CRITERIA

Configure criteria explicitly.

| Criterion | Type | Importance | Measurement / evidence |
|---|---|---:|---|
| `[CRITERION]` | hard / preference | high / medium / low | `[HOW TO JUDGE IT]` |

Do not include criteria merely because they are common in architecture discussions.

Every criterion should be able to change the decision.

## 3. EVIDENCE SOURCE POLICY

Allowed evidence classes:

```text
[ ] supplied requirements/data
[ ] official documentation
[ ] primary vendor documentation
[ ] source code / repository evidence
[ ] benchmarks supplied by user/team
[ ] incident / production data
[ ] team operational experience
[ ] third-party research
[ ] external web research
```

Source freshness requirement:

`[NONE / MAX_AGE / AFTER_DATE / CURRENT_AT_DECISION_TIME]`

Citation requirement:

`[EVERY MATERIAL EXTERNAL CLAIM / ONLY DISPUTED CLAIMS / NONE]`

Evidence labels:

- `SUPPLIED_FACT` — explicitly provided by the decision owner/context;
- `OBSERVED` — directly measured or inspected;
- `SOURCE_CLAIM` — stated by an identified source;
- `INFERRED` — reasoned from evidence;
- `ASSUMPTION` — needed to proceed but not established;
- `UNKNOWN` — unresolved.

Do not convert popularity, familiarity, or vendor marketing into evidence without labeling the source.

## 4. EVIDENCE QUALITY POLICY

For each material claim, record where relevant:

- source;
- freshness;
- applicability to this system;
- whether it is measured vs claimed;
- confidence;
- what would falsify it.

Suggested evidence quality levels:

- `A` — direct system-specific measurement/observation;
- `B` — authoritative source directly applicable to current context;
- `C` — useful but indirect/general evidence;
- `D` — assumption, anecdote, or weakly applicable source.

Configure minimum quality for irreversible/high-cost decisions:

`[EXAMPLE: NO DECIDE STATUS IF CRITICAL CRITERIA DEPEND ONLY ON C/D EVIDENCE]`

## 5. OPTION VIABILITY FILTER

Before scoring or comparing:

For each option determine:

- hard-constraint conflicts;
- prerequisites;
- hidden dependencies;
- migration/adoption cost;
- lock-in/reversal cost;
- operational ownership.

State:

- `VIABLE`
- `CONDITIONALLY_VIABLE`
- `NON_VIABLE`

Only viable options enter the preference comparison.

## 6. COMPARISON PROCESS

### Phase A — normalize the decision

1. Restate what is actually being decided.
2. Separate outcome from implementation preference.
3. Remove options that are out of scope or non-viable.

### Phase B — build evidence ledger

For each option record:

- evidence supporting it;
- evidence against it;
- assumptions;
- unknowns;
- evidence quality.

### Phase C — compare under shared criteria

Use the same criteria and definitions for every viable option.

A numerical score is optional. If used:

- show how it was derived;
- do not present it as evidence;
- do not allow it to override a hard constraint;
- expose sensitivity to uncertain weights.

### Phase D — second-order consequences

Evaluate where relevant:

- migration burden;
- operating burden;
- staffing/skill requirements;
- failure modes;
- vendor/platform lock-in;
- data portability;
- security/compliance consequences;
- exit/reversal path;
- opportunity cost.

### Phase E — stress-test the leader

Ask:

- what assumption is most fragile?
- what evidence is weakest but most decision-relevant?
- what future condition makes another option better?
- what failure mode is easiest to underestimate?
- how expensive is reversal?

## 7. DECISION STATE POLICY

Configure permitted states:

- `DECIDE`
- `CONDITIONAL`
- `HOLD`
- `REJECT_ALL`

Suggested transition rules:

```text
hard constraint violated                   -> option NON_VIABLE
material criterion depends on weak evidence -> CONDITIONAL or HOLD
leader robust across realistic assumptions  -> DECIDE
leading options effectively tied             -> HOLD + discriminating experiment
all options violate constraints               -> REJECT_ALL
```

Decision confidence is separate from confidence in any individual fact.

## 8. OUTPUT CONTRACT

### 1. Decision state

`DECIDE | CONDITIONAL | HOLD | REJECT_ALL`

### 2. Decision summary

2–5 sentences covering:

- recommendation/status;
- most important reason;
- strongest uncertainty.

### 3. Constraint ledger

| Constraint | Type | Options affected | Consequence |
|---|---|---|---|

### 4. Criteria frame

| Criterion | Importance | Evidence needed | Why it matters |
|---|---:|---|---|

### 5. Option viability

| Option | State | Constraint conflicts | Dependencies | Reversal cost |
|---|---|---|---|---|

### 6. Evidence ledger

For each option:

- supplied/observed evidence;
- source claims;
- inference;
- assumptions;
- unknowns;
- evidence quality.

### 7. Comparative analysis

| Option | Strengths | Weaknesses | Operational consequences | Main risk |
|---|---|---|---|---|

### 8. Recommendation

State:

- recommended option;
- why it wins under the configured criteria;
- strongest argument against it;
- confidence: `high | medium | low`;
- assumptions the recommendation depends on.

### 9. Reversal triggers

Concrete events/measurements that should reopen the decision.

### 10. Next validation action

Actions ordered by **information value**.

For each:

- uncertainty tested;
- expected evidence;
- cost/effort;
- decision consequence.

## 9. DISCRIMINATING EXPERIMENT CONTRACT

When the decision is `HOLD`, design the smallest useful experiment instead of forcing a winner.

For each experiment:

- hypothesis;
- metric/evidence;
- success threshold;
- failure threshold;
- duration/sample scope;
- cost/risk;
- which decision branch it resolves.

Do not recommend a proof-of-concept that cannot distinguish the competing options.

## 10. VERIFICATION CONTRACT

Before finalizing, verify:

- every option was checked against hard constraints first;
- shared criteria were applied consistently;
- material external claims have source/freshness state when required;
- weak evidence is visible;
- scores, if any, are summaries rather than evidence;
- second-order consequences were not omitted where material;
- recommendation state follows configured transition rules;
- reversal triggers are concrete;
- next validation action targets the highest-value uncertainty.

Local result:

- `DECISION_CONTRACT_PASS`
- `DECISION_CONTRACT_PASS_WITH_UNKNOWNS`
- `DECISION_CONTRACT_FAIL`

This is local workflow validation, not Prompt Quarry F4–F7 evidence.

## 11. ADAPTATION MAP

| Configuration | Example |
|---|---|
| Decision type | build vs buy |
| Hard constraints | EU data residency, 8-week deadline |
| Criteria | integration, TCO, operability, exit cost |
| Evidence policy | official docs + current pricing + internal benchmark |
| Freshness | current within 30 days |
| Decision states | DECIDE / CONDITIONAL / HOLD |
| Minimum evidence | B+ for security/compliance claims |
| Reversal trigger | traffic > X or vendor price > Y |

## 12. INTEGRATION SHAPES

This template can map into:

- ADR creation;
- architecture review board workflow;
- vendor/tool evaluation;
- dependency selection;
- migration planning;
- procurement technical assessment;
- engineering RFC;
- Prompt Quarry Generator configuration.

Keep hard constraints, evidence quality, and decision-state semantics explicit when changing representation.
