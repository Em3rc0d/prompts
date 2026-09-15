# Prompt Machine — Capital Allocation Rules v1

Status: `OPERATING DISCIPLINE / PRE-REVENUE`

Date: `2026-09-03`

## 1. Purpose

Prompt Machine has limited founder time, model/runtime budget, engineering attention, and distribution capacity.

This document defines how those scarce resources are allocated before product-market fit.

The objective is not maximum activity. It is maximum **evidence gained per unit of time and money** while protecting product integrity.

## 2. Allocation principle

Every meaningful task must primarily serve at least one of these buckets:

```text
Q = QUALITY      reduce product / evidence / delivery risk
A = ACQUISITION  bring relevant people to Prompt Machine
V = ACTIVATION   help visitors obtain a useful result
M = MONETIZATION convert proven value into a paid transaction
R = RETENTION    create repeat use, upgrades, referrals, recurring value
```

A task with no credible connection to `Q`, `A`, `V`, `M`, or `R` is default `DEFER`.

## 3. Current phase weighting

Current phase: `PRE-REVENUE PRODUCT HARDENING`.

Priority order:

```text
Q > V > M > A > R
```

Reason:

- selling a broken or misleading product destroys trust;
- acquisition before activation wastes traffic;
- monetization cannot be interpreted until useful value exists;
- retention cannot be measured before customers exist.

This ordering is temporary and changes with evidence.

## 4. Phase-based reallocation

### Before first sale

Prioritize:

```text
1. quality / integrity blockers
2. activation path
3. payment + delivery readiness
4. first relevant traffic
5. everything else
```

### After `PQ-$1`

Prioritize:

```text
1. delivery defects
2. activation evidence
3. repeatable acquisition
4. conversion diagnosis
5. support burden
```

### After `PQ-10`

Prioritize based on observed bottleneck:

```text
traffic weak      → acquisition
activation weak   → product / onboarding
conversion weak   → value proposition / trust / offer / price diagnosis
refunds high      → product quality / expectation alignment
support high      → simplification / automation / documentation
upgrades weak     → Full value differentiation
repeat strong     → investigate recurring model
```

## 5. No speculative scaling rule

Do not materially scale any of the following before the prior gate has evidence:

```text
more traffic      before activation works
more SKUs         before first offer converts
more professions  before adjacent demand appears
subscription      before recurring value appears
marketplace       before repeatable buyer demand exists
team product      before team demand appears
paid ads          before organic/manual funnel is interpretable
large model runs  before small canaries validate semantics
```

## 6. Model/runtime budget rule

Model calls are an evidence expense.

Each behavioral campaign must state before execution:

```text
QUESTION
What uncertainty will these calls reduce?

MINIMUM SAMPLE
What is the smallest campaign that can answer it?

STOP CONDITION
What result makes us stop instead of automatically spending more?

OUTPUT
What artifact/evidence will be preserved?

NEXT DECISION
What decision becomes possible after review?
```

Default policy:

```text
1 canary
→ review
→ 1 adversarial canary if justified
→ review
→ small mode-family campaign
→ review
→ only then larger regression / portability campaign
```

No campaign is authorized merely because credits are available.

## 7. Founder-time rule

Founder time is currently more scarce than infrastructure.

Automate repeated work when:

```text
frequency × manual cost × expected project lifetime
```

is materially larger than the implementation and maintenance cost of automation.

Do not automate one-off uncertainty.

Prefer automation for:

- deterministic gates;
- evidence preservation;
- artifact generation;
- delivery verification;
- funnel instrumentation;
- repeated quality checks;
- repetitive publishing/distribution preparation when it does not reduce quality.

## 8. Build / buy / defer rule

For each supporting capability:

### BUILD when

- it is core to Prompt Machine's differentiated quality/trust system;
- off-the-shelf tools cannot preserve required evidence or contracts;
- reuse across many workflows will reduce marginal cost.

### BUY when

- capability is commodity infrastructure;
- vendor risk is acceptable;
- integration is cheaper than ownership;
- switching remains possible.

Typical buy candidates:

- payment processing;
- email delivery;
- hosting;
- analytics infrastructure where privacy/evidence boundaries permit;
- transactional file delivery.

### DEFER when

- customer demand is not observed;
- the feature serves a hypothetical future scale problem;
- it adds operational complexity before revenue.

## 9. Distribution budget rule

Until the first offer is proven, prefer channels with high learning density:

```text
founder-led outreach
GitHub / technical discovery
LinkedIn
TikTok / short-form demonstrations
useful technical content
referrals / direct sharing
```

The best early channel is not necessarily the one with the most impressions. It is the one that produces the most relevant users and the clearest feedback loop.

Track:

```text
source → relevant visit → free activation → Starter intent → purchase → delivery
```

Do not optimize vanity reach without downstream evidence.

## 10. Pricing allocation rule

Current prices remain hypotheses:

```text
Starter = USD 9
Full    = USD 19
```

Do not allocate significant effort to price optimization until:

- relevant traffic exists;
- activation is interpretable;
- trust surface is credible;
- checkout works;
- at least some purchase evidence exists.

When testing price later, change one major commercial variable at a time where practical.

## 11. Quality stop-the-line rule

Any of the following can stop release or spending regardless of commercial pressure:

- misleading evidence claim;
- unsafe authority boundary;
- known delivery corruption;
- payment without reliable fulfillment;
- privacy/security defect;
- model behavior materially violating the workflow contract;
- inability to reproduce the tested invocation;
- unsupported certification or portability claim.

Revenue pressure does not override truth.

## 12. Weekly capital question

At the beginning of each work cycle, answer:

```text
1. What is the largest current bottleneck?
2. What evidence proves it is the bottleneck?
3. What is the cheapest experiment that can reduce that uncertainty?
4. What do we stop doing until the result arrives?
5. What decision will the result unlock?
```

If those five answers are unclear, do not open a large workstream.

## 13. Current allocation decision

As of `2026-09-03`, the highest-value next uncertainty is behavioral quality of the newly frozen architecture/binding/invocation stack.

Therefore:

```text
AUTHORIZED NEXT EXPENSE
1 LOW-risk NORMAL canary

NOT AUTHORIZED YET
18-call pilot
84-call historical wave
portability campaign
bulk regeneration
new profession collections
subscription engineering
marketplace engineering
paid acquisition scaling
```

This is not anti-growth.

It is the shortest path to trustworthy growth.

## 14. Strategic rule

> **Spend only when the spend buys evidence, customer value, or reusable leverage.**

The goal is not to conserve every dollar.

The goal is to make each dollar and hour increase the probability of a durable business.
