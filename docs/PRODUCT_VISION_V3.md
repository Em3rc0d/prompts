# Prompt Machine — Product Vision v3

Status: `FROZEN STRATEGIC DIRECTION / CUSTOMER EXPERIENCE IMPLEMENTED ON PRODUCT BRANCH`

Date: `2026-09-02`

## 1. Product identity

**Prompt Machine is the customer-facing platform for finding and using reliable AI workflows.**

Customers should not need to understand prompt engineering, MK0, MK1, PCP, Prompt Quarry internals, fixture design, or certification machinery before receiving value.

**Prompt Quarry is the internal factory.** It acquires knowledge, engineers artifacts, tests them, records evidence, and decides what is eligible to become a customer-facing Prompt Machine workflow.

```text
INTERNAL FACTORY                          CUSTOMER PRODUCT

MK0 / Quarry / MK1 / PCP                  Prompt Machine
         │                                      │
         ├─ acquire evidence                    ├─ discover by goal
         ├─ engineer candidates                 ├─ use free workflows
         ├─ test and compare                    ├─ buy collections
         ├─ preserve provenance                 ├─ follow examples
         └─ certify claims                      └─ trust visible evidence
```

The factory is a trust mechanism. It is not the primary merchandising surface.

## 2. What we sell

We do **not** primarily sell prompt files.

We sell **reusable AI workflows that reduce trial-and-error and repetitive work**.

The customer value proposition is:

> Choose what you need to get done. Prompt Machine gives you a reusable workflow, examples, boundaries, and evidence so you can reach the result faster than starting from a blank chat.

A workflow can include:

- a ready-to-use prompt surface;
- an installable skill surface when supported;
- required-input guidance;
- examples;
- output contracts;
- fallback behavior;
- verification guidance;
- known limitations;
- version and evidence state.

The ZIP is only a delivery format. **The ZIP is not the product experience.**

## 3. How customers discover value

The primary discovery question is:

> **What are you trying to get done?**

Do not force the customer to classify themselves first as developer, student, manager, marketer, architect, lawyer, or another profession.

Professions are useful merchandising metadata, but the primary taxonomy is **job-to-be-done / outcome**.

Initial outcome groups:

1. **Build & Ship** — review work, debug problems, design solutions, validate changes.
2. **Research & Decide** — compare options, structure evidence, make defensible decisions.
3. **Learn & Create** — understand material, plan projects, transform knowledge into deliverables.
4. **Operate & Automate** — reduce repetitive administrative and operational work.

Future collections may serve additional domains, but expansion requires real demand and evidence rather than a claim that Prompt Machine is for everyone.

## 4. Commercial model

The initial commercial ladder is:

```text
FREE LIBRARY                 USD 0
STARTER COLLECTION           USD 9 one-time   ← primary first paid offer
FULL DEVELOPER COLLECTION    USD 19 one-time  ← broader premium / upsell
SUBSCRIPTION                 DEFERRED
```

Both paid prices are `PRICE_HYPOTHESIS` until real willingness-to-pay evidence exists.

### Free Library — $0

Purpose: acquisition, proof of usefulness, trust, sharing, and repeat usage.

A free workflow must be useful by itself. It is not intentionally crippled bait.

Success signals:

- download/use;
- task completion;
- return usage;
- referral/share;
- movement from free workflow to related collection.

### Starter Collection — $9 one-time hypothesis

The Starter Collection is the primary first-purchase experiment. It reduces first-purchase friction while still solving complete tasks.

Frozen initial scope:

- Evidence-first Code Review;
- Evidence-first Bug Diagnosis;
- the two corresponding skill candidates;
- `START_HERE` and task routing;
- worked examples;
- verification guidance;
- adaptation cheatsheet;
- visible evidence and limitations.

The Starter must not be an artificially crippled version of Full.

Scope freeze does **not** imply behavioral testing, certification, portability, packaging, provider custody, delivery readiness, or sale readiness.

### Full Developer Workflow Collection — $19 one-time hypothesis

The Full collection extends the developer system to four workflow families and four skill candidates, including Technical Decision and AI Workflow Design.

The $19 upgrade must earn its price through genuinely broader workflow coverage, reusable operating contracts, examples, adaptation guidance, orchestration, and evidence—not by withholding completion of Starter's jobs.

Public checkout remains disabled until the exact SKU's release and delivery gates pass.

### Later monetization

Defer until real purchase and recurring-value evidence exists:

- additional outcome collections;
- bundles;
- organization/team licenses;
- updates/subscription layer;
- workflow customization or implementation services;
- marketplace/distribution models.

Do not optimize subscription architecture before `PQ-$1` and repeat usage establish that customers want an ongoing relationship.

## 5. Customer funnel

```text
CONTENT / SEARCH / SOCIAL
          ↓
PROMPT MACHINE HOME
          ↓
"WHAT DO YOU WANT TO GET DONE?"
          ↓
OUTCOME / FREE WORKFLOW
          ↓
OBSERVE VALUE + TRUST
          ↓
$9 STARTER
          ↓
$19 FULL WHEN BROADER VALUE IS NEEDED
          ↓
REPEAT USAGE / REFERRAL / NEW COLLECTION
```

Content is part of the product distribution system.

The Learning layer should publish useful material about:

- using AI for real tasks;
- workflow examples;
- mistakes and failure modes;
- building projects and learning in public;
- engineering and university experience when relevant;
- before/after workflow transformations;
- evidence and verification practices.

Content must provide value before asking for a purchase.

## 6. Trust model

Prompt Machine should make trust visible without forcing users to read certification internals.

Customer-facing evidence vocabulary should stay compact:

- `VERSIONED`
- `STRUCTURE CHECKED`
- `RUNTIME TESTED` when earned
- `IMPROVED` when comparison evidence exists
- `CERTIFIED` only when certification gates pass
- `KNOWN LIMITATIONS`

Internal PCP/F4/F5/F6/F7 terminology may remain in engineering documentation and inspection surfaces.

Master rule:

```text
MARKETING CLAIM <= OBSERVED EVIDENCE
```

Free usefulness, infrastructure health, archive integrity, scope freeze, and beautiful packaging do not imply behavioral certification.

## 7. Website information architecture

Primary navigation should support:

```text
Workflows | Collections | Learn | How it works | Evidence | Free
```

Paid discovery should visibly distinguish:

```text
Free Library → Starter $9 hypothesis → Full $19 hypothesis
```

The home page should answer, in this order:

1. What does Prompt Machine help me accomplish?
2. What can I use right now?
3. How do I find the right workflow?
4. Why should I trust it?
5. What does Starter add?
6. What does Full add beyond Starter?
7. How do I start?

Do not open with internal architecture terminology.

## 8. Product hierarchy

```text
Prompt Machine                              platform / public brand
├── Free Library                            useful standalone workflows
├── Collections                             paid outcome-oriented libraries
│   └── Build & Ship / Developer
│       ├── Starter Collection              USD 9 hypothesis / primary first paid offer
│       └── Full Developer Collection       USD 19 hypothesis / broader upsell
├── Workflow                                primary unit of customer value
├── Skill                                   optional installable execution surface
├── Learn                                   education + acquisition + trust
└── Evidence                                visible trust layer

Prompt Quarry                               internal factory
├── MK0                                     knowledge quarry
├── MK1                                     prompt forge
├── MK2                                     future orchestration
└── PCP                                     certification program
```

## 9. Metrics

Revenue is the business objective, but customer value must lead the causal chain.

North-star product signal:

> **A user successfully applies a workflow to a real task and returns to Prompt Machine for another task.**

Commercial funnel metrics:

```text
visitor
  → free workflow use/download
  → activated user
  → repeat user
  → Starter view / intent
  → $9 purchase
  → Full view / intent
  → $19 upgrade
  → repeat purchase / referral
```

Track at minimum:

- landing → free conversion;
- free → repeat use;
- free → Starter intent;
- Starter view → Starter CTA;
- checkout conversion once enabled;
- $9 purchase → verified delivery;
- $9 → $19 upgrade behavior;
- revenue per collection;
- refund/support signal;
- most requested outcomes;
- content → product attribution where observable.

There is no honest pre-launch variable that guarantees a 99% purchase probability. Confidence is earned by observed conversion evidence.

## 10. Immediate execution order

```text
P0  Freeze this vision                                      DONE
P1  Refactor website from developer-only to outcome-first   DONE ON PRODUCT BRANCH
P2  Make $9 Starter the primary first paid hypothesis       DONE / SCOPE FROZEN
P3  Keep $19 Full as broader premium / upsell               DONE IN CUSTOMER UX
P4  Build Collections + Learn distribution surfaces         DONE ON PRODUCT BRANCH
P5  Observe staging identity + intent runtime                DONE
P6  Complete PCP-04 → PCP-07 behavioral evidence             OPEN
P7  Complete skill trigger / forward / parity evidence      OPEN
P8  Finalize customer surfaces + deterministic Starter       OPEN
P9  Provider custody + integration + live delivery canary    OPEN
P10 Enable USD 9 checkout only when evidence permits it      OFF
P11 Measure PQ-$1 and $9 → $19 behavior before expansion     NOT OBSERVED
```

## 11. Non-goals

Prompt Machine is not:

- a dump of thousands of scraped prompts;
- a claim that every workflow works for every model and profession;
- a ZIP customers must reverse-engineer;
- a marketplace before there is demand;
- a certification badge without evidence;
- a reason to expose or sell the internal source-acquisition factory.

## 12. Strategic sentence

> **Prompt Machine turns tasks people normally improvise with AI into reusable workflows they can discover, understand, trust, and apply.**
