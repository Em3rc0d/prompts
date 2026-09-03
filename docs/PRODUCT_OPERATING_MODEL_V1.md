# Prompt Machine — Product Operating Model v1

Status: `OPERATING BASELINE / BUSINESS HYPOTHESIS / NOT REVENUE-PROVEN`

Date: `2026-09-03`

## 1. Purpose

This document defines the operating model for building Prompt Machine as a durable product business rather than a prompt catalog.

It does not claim product-market fit, profitability, or future revenue. It defines the system we will use to earn those outcomes with the smallest amount of avoidable waste.

The governing objective is:

> **Turn recurring AI-assisted jobs into reliable reusable workflows, prove that people use them, prove that some people pay for them, and compound the evidence into better products and distribution.**

The business must optimize for customer value first and economic evidence second. Volume of generated artifacts is not a goal.

## 2. The company-shaped system

Prompt Machine should be modeled as five connected engines:

```text
                    ┌──────────────────────────────┐
                    │      CUSTOMER PROBLEM       │
                    │ recurring job / desired     │
                    │ outcome / friction          │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
┌──────────────────┐      ┌───────────────────┐      ┌────────────────────┐
│  DISCOVERY       │ ───▶ │  VALUE ENGINE     │ ───▶ │  TRUST ENGINE      │
│  ENGINE          │      │  workflow solves  │      │ evidence + limits  │
│  content/search  │      │  real task        │      │ + verification     │
└────────┬─────────┘      └─────────┬─────────┘      └─────────┬──────────┘
         │                           │                           │
         │                           ▼                           │
         │                 ┌───────────────────┐                 │
         └────────────────▶│  REVENUE ENGINE   │◀────────────────┘
                           │  free → paid →     │
                           │  upgrade / repeat  │
                           └─────────┬─────────┘
                                     │
                                     ▼
                           ┌───────────────────┐
                           │ LEARNING ENGINE   │
                           │ observed usage,   │
                           │ failures, demand  │
                           └─────────┬─────────┘
                                     │
                                     └──────────────▶ improves every engine
```

Prompt Quarry is the internal production and evidence factory that powers the Value and Trust engines.

## 3. Primary product unit

The primary customer-facing product unit is the **Workflow**.

A Workflow is not only a prompt. It is a governed unit that may contain:

```text
WORKFLOW
├── task contract
│   ├── intended outcome
│   ├── required inputs
│   ├── non-goals
│   └── stop / fallback conditions
├── execution surface
│   ├── prompt surface
│   └── optional skill surface
├── examples
├── verification guidance
├── known limitations
├── evidence card
└── version + compatibility state
```

The Workflow must solve a recognizable job without requiring the customer to understand Prompt Quarry internals.

## 4. The stable abstraction

The durable abstraction is:

```text
CUSTOMER GOAL
      ↓
WORKFLOW CONTRACT
      ↓
AUTHORIZED CONFIGURATION
      +
UNTRUSTED TASK DATA
      ↓
EXECUTION
      ↓
RESULT
      ↓
VERIFY
      ↓
REUSE
```

This abstraction should remain stable even as:

- models change;
- providers change;
- prompt syntax changes;
- skill surfaces evolve;
- delivery formats change;
- pricing changes;
- new collections are introduced.

Anything tightly coupled to one model or one provider is an implementation detail, not the product identity.

## 5. What scales and what does not

### Scalable assets

Prompt Machine should invest in assets that become more useful as the library grows:

- shared architecture mothers;
- binding and invocation contracts;
- evaluation harnesses;
- evidence schemas;
- reusable examples and fixtures;
- workflow routing;
- collection navigation;
- delivery infrastructure;
- attribution and funnel instrumentation;
- content that maps directly to customer jobs;
- reusable quality gates;
- customer feedback mapped to workflow families.

### Non-scalable traps

Do not treat the following as growth:

- thousands of near-duplicate prompts;
- profession packs without observed demand;
- model-specific rewrites with no customer benefit;
- manual delivery that increases support load linearly;
- unsupported certification language;
- price changes after every weak traffic sample;
- feature expansion before activation evidence;
- subscriptions before recurring value exists;
- marketplace complexity before supply and demand exist.

## 6. Product hierarchy

```text
Prompt Machine
├── Free Library
│   └── Workflow
├── Collections
│   ├── Starter Collection
│   │   └── Workflow(s)
│   ├── Full Collection
│   │   └── Workflow(s)
│   └── future outcome collections
├── Learn
├── Evidence
└── Account / delivery layer when economically justified

Prompt Quarry
├── acquisition / provenance
├── architecture mothers
├── binding + invocation
├── runtime observation
├── failure mining
├── improvement
├── regression
├── portability checks
└── promotion gates
```

Collections are merchandising and packaging. Workflow is the reusable value primitive.

## 7. Revenue architecture

Initial ladder remains:

```text
FREE             USD 0
STARTER          USD 9 one-time   ← primary first purchase
FULL             USD 19 one-time  ← broader upgrade / anchor
SUBSCRIPTION     DEFERRED
```

The ladder must be understood as an experiment, not a permanent truth.

### Free

Free must create real value and reduce perceived risk.

It earns the right to monetize by producing one or more of:

- successful task completion;
- repeat usage;
- trust;
- sharing;
- demand for adjacent workflows;
- demand for easier setup or broader coverage.

### Starter

Starter should monetize **coherence and saved setup time**, not artificial restriction.

It should provide a customer with a small complete operating system for a tightly related set of jobs.

### Full

Full should monetize **breadth and orchestration**.

A customer should be able to explain the upgrade in plain language:

> Starter solves the jobs I needed first; Full gives me additional recurring jobs and a broader reusable system.

### Recurring revenue

Recurring revenue is permitted only after recurring customer value is observed.

Possible later recurring value sources:

- continuously maintained workflow compatibility;
- new certified workflow drops;
- team libraries;
- organization governance;
- workflow monitoring / automation;
- custom private collections;
- managed evidence or evaluation services.

No subscription should exist merely because subscription revenue is attractive.

## 8. Revenue flywheel

The intended compounding loop is:

```text
useful content / discovery
        ↓
free workflow used on real task
        ↓
observable value
        ↓
trust + repeat use
        ↓
paid collection
        ↓
real usage + failures + requests
        ↓
better workflows + better evidence
        ↓
stronger demonstrations / content
        ↓
more relevant discovery
        ↺
```

The strongest long-term moat is not secret wording. It is the accumulated combination of:

```text
customer-job knowledge
+ governed workflow architecture
+ observed failure data
+ improvement history
+ evidence
+ distribution
+ trusted delivery
```

## 9. Quality architecture

The required quality path is:

```text
RAW
  ↓
REVIEWED
  ↓
STRUCTURALLY VALID
  ↓
STATIC ARCHITECTURE BOUND
  ↓
EXACT INVOCATION PREPARED
  ↓
RUNTIME OBSERVED
  ↓
FAILURE MINED
  ↓
IMPROVED
  ↓
REGRESSION TESTED
  ↓
PORTABILITY OBSERVED WHEN CLAIMED
  ↓
PRODUCT ELIGIBLE
```

Static quality and behavioral quality remain different evidence classes.

```text
prepared != executed
executed != useful
useful once != reliable
reliable on one runtime != portable
portable != sellable
sellable != purchased
purchased != retained
```

## 10. Stable release strategy

Prompt Machine should prefer small release units with strong observability.

For a new workflow family:

```text
1. identify recurring customer job
2. define workflow contract
3. build static candidate
4. bind exact configuration
5. prepare exact invocation
6. one low-risk NORMAL canary
7. inspect manually
8. one adversarial / override canary if justified
9. small behavioral campaign
10. failure mining + successor
11. regression
12. customer surface
13. free or paid placement decision
14. observe real usage
```

Do not execute large campaigns before invocation semantics and small canaries are proven.

## 11. Economic discipline

Every material product investment should eventually answer one of four questions:

```text
ACQUIRE  — can we attract a relevant user efficiently?
ACTIVATE — can they get a useful result?
MONETIZE — will some activated users pay?
RETAIN   — do they return, upgrade, refer, or buy again?
```

If an engineering task cannot reasonably improve one of those dimensions or reduce material risk, its priority should be challenged.

### Economic variables

Do not fabricate values. Track them when evidence exists:

```text
V  = relevant visitors
A  = activated users
P9 = Starter purchases
P19 = Full purchases / upgrades
R  = gross revenue
RF = refunds
SC = support cost
PC = payment/provider cost
CC = content/acquisition cost
IC = infrastructure/model cost
```

Derived metrics:

```text
activation_rate       = A / V
starter_conversion    = P9 / A
full_upgrade_rate     = P19 / P9
gross_revenue         = 9*P9 + 19*P19
contribution_margin   = R - RF - SC - PC - CC - IC
revenue_per_visitor   = R / V
revenue_per_activated = R / A
```

Do not optimize these equations before sample sizes become interpretable.

## 12. Decision hierarchy

When choosing what to build next, use this order:

1. **Safety / legality / privacy / integrity blocker**
2. **Broken customer value**
3. **Broken purchase or delivery path**
4. **Activation friction**
5. **Trust / evidence weakness**
6. **Observed customer demand**
7. **Conversion improvement**
8. **Retention / expansion**
9. **New categories**
10. **Nice-to-have features**

This prevents novelty from outranking revenue-critical reliability.

## 13. Expansion rule

New collections are not created because a profession exists.

A new outcome collection requires evidence of:

```text
recurring job
+ meaningful pain / time cost
+ workflowizable task
+ safe authority boundary
+ reusable solution
+ plausible willingness to pay
+ supportable quality evidence
```

Prefer adjacent jobs from existing users before unrelated vertical expansion.

## 14. Productive engineering rule

The internal platform should reduce marginal cost per new workflow.

A healthy evolution looks like:

```text
workflow 1   expensive / manual
workflow 2   reuses architecture + tests
workflow 10  mostly configuration + evidence work
workflow 100 only possible if quality gates remain tractable
```

If every new workflow requires a new pipeline, new schema, new delivery method, and new certification logic, the platform is not compounding.

## 15. Customer experience invariant

The customer should see simplicity even when the factory is complex.

Customer-facing sequence:

```text
WHAT DO YOU NEED?
      ↓
USE THIS WORKFLOW
      ↓
GIVE IT THESE INPUTS
      ↓
EXPECT THIS KIND OF RESULT
      ↓
VERIFY THESE THINGS
      ↓
REUSE / ADAPT
```

Do not expose certification machinery unless the customer asks for evidence detail.

## 16. Evidence invariant

Master rule:

```text
MARKETING CLAIM <= OBSERVED EVIDENCE
```

Commercial copy may describe:

- the intended job;
- supplied workflow components;
- observed runtime behavior when actually observed;
- known limitations;
- price and delivery terms.

It may not convert preparation, static tests, synthetic events, or provider canaries into claims of customer success.

## 17. Current operating phase

Prompt Machine is currently in **pre-revenue product hardening**.

Observed state:

```text
public product model                   DEFINED
outcome-first UX                       IMPLEMENTED ON PRODUCT BRANCH
commercial ladder                      FROZEN AS HYPOTHESIS
Starter scope                          FROZEN / NOT FOR SALE
architecture mother static freeze      PASS
binding/invocation static freeze       PASS
first low-risk behavioral canary       PREPARED / NOT EXECUTED
public checkout                        OFF
real purchase evidence                 NONE
repeat purchase evidence               NONE
product-market fit                     NOT CLAIMED
```

The immediate business goal is not library size.

It is:

> **Earn the first trustworthy chain from relevant visitor → useful workflow → paid Starter → verified delivery.**

## 18. Phase gates

### Phase A — Reliable first product

Exit conditions:

- exact Starter workflow surfaces governed;
- runtime evidence sufficient for public claims;
- deterministic archive pass;
- provider custody pass;
- live delivery canary pass;
- public copy evidence audit pass.

### Phase B — First revenue

Exit conditions:

- `PQ-$1` observed;
- delivery verified;
- no unresolved payment/delivery blocker.

### Phase C — Repeatable first offer

Exit conditions:

- `PQ-10` observed or equivalent stronger evidence;
- interpretable activation/conversion data;
- support/refund burden understood;
- at least one useful acquisition channel identified.

### Phase D — Expansion

Requires evidence supporting one or more of:

- $9 → $19 upgrade;
- repeat purchase;
- referral;
- demand for adjacent collection;
- recurring value.

Only then invest materially in more collections, teams, subscriptions, or marketplace mechanics.

## 19. Operating scorecard

Maintain a compact truth table:

```text
QUALITY
architecture freeze
binding freeze
runtime observations
regression state
known limitations

PRODUCT
free activation
repeat usage
workflow completion evidence
support burden

COMMERCIAL
Starter views
checkout starts
accepted purchases
verified deliveries
Full upgrades
refunds

DISTRIBUTION
traffic by source
free activation by source
revenue by source
referrals
```

Unknown values remain `UNKNOWN`; they are never silently converted into zero or success.

## 20. Strategic invariant

> **Prompt Machine wins if each customer job teaches the factory how to produce a better reusable workflow, and each better workflow makes the next customer easier to acquire, activate, monetize, and retain.**

The goal is not a giant prompt inventory.

The goal is a **compounding workflow business**.
