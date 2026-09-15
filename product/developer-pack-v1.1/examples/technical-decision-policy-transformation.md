# Worked Transformation — From “Which database should we use?” to a Governed Architecture Decision

Status: `DRAFT EXAMPLE`

Purpose: demonstrate how `templates/technical-research-decision-system.md` becomes a reusable team decision workflow rather than a one-off recommendation prompt.

This example demonstrates static construction and governance only. It does not claim that any model recommendation is behaviorally superior.

---

## 1. Starting request

A team begins with:

> Which database should we use for the new service: PostgreSQL or DynamoDB?

Why this is not yet a decision contract:

- the actual workload is undefined;
- no hard constraints are separated from preferences;
- no decision horizon or reversal cost exists;
- no source/freshness policy exists;
- no evidence quality threshold exists;
- there is pressure to force a winner even if critical facts are unknown.

## 2. Extract the decision requirements

Scenario:

- new customer-facing transaction service;
- relational entities and cross-entity consistency are expected;
- team already operates PostgreSQL;
- service must ship in eight weeks;
- expected first-year load is uncertain;
- cloud platform supports both options;
- the architecture decision will be recorded in an ADR.

Hard constraints:

```text
security controls must satisfy current platform policy
no data-store technology that the team cannot operate safely by launch
eight-week delivery window
required transaction semantics must be supported by the chosen design
```

Preferences:

```text
low operational learning cost       HIGH
predictable first-year cost          MEDIUM
elastic scaling headroom             MEDIUM
simple local development             MEDIUM
reversibility / migration path       HIGH
```

Evidence policy:

```text
internal requirements/data        allowed
official current documentation    allowed
current vendor pricing            allowed
team production experience        allowed
marketing comparison pages        SOURCE_CLAIM only
freshness                         current at decision time for pricing/limits
```

Decision policy:

```text
DECIDE       sufficient evidence on every critical criterion
CONDITIONAL  leader exists but named assumption can reverse it
HOLD         critical decision factor remains unresolved
REJECT_ALL   all candidates violate a hard constraint
```

## 3. Configure the reusable template

### Decision identity

```text
decision_name      customer-transaction-store-v1
decision_owner     platform + service team
options            PostgreSQL / DynamoDB
decision_horizon   expensive_to_reverse
decision_deadline  before implementation milestone
```

### Evidence quality rule

```text
A = direct service/team measurement
B = current authoritative source directly applicable
C = useful but indirect/general evidence
D = assumption/anecdote

No DECIDE if a critical criterion depends only on C/D evidence.
```

### Viability policy

Each option is first classified:

```text
VIABLE
CONDITIONALLY_VIABLE
NON_VIABLE
```

Hard-constraint violations are not repaired by weighted scores.

### Reversal policy

The ADR must record triggers such as:

```text
transaction model changes materially
measured workload invalidates capacity assumptions
operational burden exceeds agreed threshold
vendor/platform economics change materially
compliance requirement changes
```

## 4. Resulting team operating prompt

```text
Run the customer-transaction-store-v1 decision workflow.

DECISION
Choose between PostgreSQL and DynamoDB for the new customer transaction service.
The decision is expensive to reverse and must be recorded in an ADR.

HARD CONSTRAINTS
- must satisfy current platform security policy;
- team must be able to operate the system safely by the eight-week launch;
- chosen design must support required transaction semantics;
- an option violating a hard constraint is NON_VIABLE.

PREFERENCES
- low operational learning cost: HIGH;
- reversibility/migration path: HIGH;
- predictable first-year cost: MEDIUM;
- scaling headroom: MEDIUM;
- simple local development: MEDIUM.

EVIDENCE POLICY
Use supplied requirements, current official documentation, current vendor pricing, and supplied team operational experience.
Label material evidence as SUPPLIED_FACT, OBSERVED, SOURCE_CLAIM, INFERRED, ASSUMPTION, or UNKNOWN.
Pricing/limits must be current at decision time.
Do not treat vendor marketing language as observed evidence.

EVIDENCE QUALITY
A = direct system/team measurement.
B = current authoritative evidence directly applicable.
C = indirect/general evidence.
D = assumption/anecdote.
Do not return DECIDE if a critical criterion depends only on C/D evidence.

PROCESS
1. Normalize the actual architecture decision.
2. Filter every option through hard constraints.
3. Build an evidence ledger for viable options.
4. Compare viable options using the same preference criteria.
5. Surface migration, operating burden, lock-in, failure modes, and reversal cost.
6. Stress-test the leading option and its most fragile assumption.
7. Return DECIDE, CONDITIONAL, HOLD, or REJECT_ALL according to evidence.
8. If HOLD, design the smallest experiment or evidence request that can break the tie.

OUTPUT
1. Decision state
2. Decision summary
3. Constraint ledger
4. Criteria frame
5. Option viability
6. Evidence ledger
7. Comparative analysis
8. Recommendation and strongest counterargument
9. Reversal triggers
10. Next validation action ordered by information value

Never invent benchmark results, prices, limits, workload measurements, or team capabilities.
```

## 5. What the Paid system added

The Free Technical Decision prompt is already a strong finished decision workflow.

The Paid system adds a reusable architecture-review policy surface:

| Capability | Finished Free prompt | Configured Paid system |
|---|---:|---:|
| Compare concrete options | yes | yes |
| Hard-constraint filtering | yes | configurable policy |
| Team decision criteria | edit manually | first-class configuration |
| Source classes | generic evidence input | explicit allowed-source policy |
| Freshness | contextual | explicit configurable requirement |
| Evidence quality threshold | not a reusable team policy | A/B/C/D policy + transition rule |
| Decision states | DECIDE / CONDITIONAL / HOLD | configurable + REJECT_ALL |
| Decision authority/owner | contextual | explicit workflow identity |
| Reversal triggers | included | reusable ADR policy |
| Machine representation | no | workflow JSON Schema |
| Team-wide reuse | adapt finished prompt | stable contract + adaptation method |

The value difference is the ability to preserve a decision policy across many architecture/tool/vendor decisions.

## 6. Inspection checklist

Another engineer should be able to answer from the configured workflow:

- What is a hard constraint vs a preference?
- Which evidence sources are allowed?
- Which claims require current evidence?
- What quality of evidence permits `DECIDE`?
- What makes an option `NON_VIABLE`?
- When must the workflow return `HOLD`?
- Which future events reopen the ADR?
- What evidence request has the highest information value?

If those semantics are not explicit, the workflow is not yet a governed team decision contract.
