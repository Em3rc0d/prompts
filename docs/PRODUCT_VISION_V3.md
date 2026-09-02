# Prompt Machine — Product Vision v3

Status: `FROZEN STRATEGIC DIRECTION / CUSTOMER EXPERIENCE REFACTOR REQUIRED`

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

### Free Library

Purpose: acquisition, proof of usefulness, trust, sharing, and repeat usage.

A free workflow must be useful by itself. It is not intentionally crippled bait.

Success signals:

- download/use;
- task completion;
- return usage;
- referral/share;
- movement from free workflow to related collection.

### Paid Collections

A collection packages multiple related workflows around an outcome family.

Initial commercial experiment:

```text
Developer Workflow Collection
launch price hypothesis: USD 19 one-time
checkout: disabled until release gates pass
```

The paid upgrade must earn its price through breadth, orchestration, examples, reusable operating contracts, skills, adaptation guidance, and evidence—not by hiding the only useful version behind payment.

### Later monetization

Defer until real purchase evidence exists:

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
OUTCOME / COLLECTION
          ↓
USE A FREE WORKFLOW
          ↓
OBSERVE VALUE + TRUST
          ↓
PAID COLLECTION
          ↓
REPEAT USAGE / NEW COLLECTION
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

Free usefulness, infrastructure health, archive integrity, and beautiful packaging do not imply behavioral certification.

## 7. Website information architecture

Primary navigation should move toward:

```text
Workflows | Collections | Learn | How it works | Free
```

The home page should answer, in this order:

1. What does Prompt Machine help me accomplish?
2. What can I use right now?
3. How do I find the right workflow?
4. Why should I trust it?
5. What do I get by paying?
6. How do I start?

Do not open with internal architecture terminology.

## 8. Product hierarchy

```text
Prompt Machine                         platform / public brand
├── Free Library                       useful standalone workflows
├── Collections                        paid outcome-oriented libraries
│   └── Developer Workflow Collection  first commercial experiment
├── Workflow                           primary unit of customer value
├── Skill                              optional installable execution surface
├── Learn                              education + acquisition + trust
└── Evidence                           visible trust layer

Prompt Quarry                          internal factory
├── MK0                                knowledge quarry
├── MK1                                prompt forge
├── MK2                                future orchestration
└── PCP                                certification program
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
  → paid collection conversion
  → second purchase / expansion
```

Track at minimum:

- landing → free conversion;
- free → repeat use;
- free → paid intent;
- checkout conversion once enabled;
- revenue per collection;
- refund/support signal;
- most requested outcomes;
- content → product attribution where observable.

There is no honest pre-launch variable that guarantees a 99% purchase probability. Confidence is earned by observed conversion evidence.

## 10. Immediate execution order

```text
P0  Freeze this vision
P1  Refactor website positioning from developer-only to outcome-first
P2  Keep Developer Workflow Collection as the first paid experiment
P3  Build Collections surface without pretending future collections already exist
P4  Add Learning/content surface and distribution loop
P5  Complete real behavioral testing and release gates
P6  Enable USD 19 checkout only when product + delivery evidence permits it
P7  Measure PQ-$1, usage, repeat behavior, and demand before expanding catalog
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
