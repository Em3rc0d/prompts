# Verlune Product Model v1

Status: `PRODUCT_MODEL_CANDIDATE / NOT_FOR_SALE`

Date: 2026-09-22

## Product definition

> **Verlune is a library and toolkit for structured AI work. It provides reusable prompts and workflows across real-world categories, plus tools that help Premium users build and evaluate prompts and workflows for their own tasks. Verlune supplies the structure and methodology; users run the assets with their own compatible AI assistants.**

Commercial shorthand:

> **Use ours. Build yours. Work better with AI.**

This document defines the customer-facing product model. It does not make runtime, portability, sales, or customer-outcome claims by itself.

## Problem

The problem is not lack of prompts on the internet.

The recurring user failure is:

```text
REAL TASK
  ↓
BLANK CHAT
  ↓
IMPROVISED INSTRUCTIONS
  ↓
FLUENT RESULT
  ↓
MISSING CONTEXT / HIDDEN ASSUMPTIONS
  ↓
MANUAL CORRECTION
  ↓
START AGAIN NEXT TIME
```

Verlune replaces that loop with:

```text
TASK
  ↓
STRUCTURED PROMPT OR WORKFLOW
  ↓
REQUIRED INPUTS + CONTEXT
  ↓
RULES / CONSTRAINTS
  ↓
PROCESS
  ↓
EXPECTED OUTPUT
  ↓
UNKNOWN / FAILURE BEHAVIOR
  ↓
VERIFICATION
  ↓
REUSE
```

## Product principles

1. **Free is useful, not crippled.**
2. **Premium earns payment through depth, breadth, adaptation, creation and evaluation — not word count.**
3. **A prompt is not a workflow.**
4. **Premium does not mean "longer"; it means more capable and better governed.**
5. **The user should not need prompt-engineering vocabulary to use a Builder.**
6. **Verlune does not require its own LLM runtime for v1.**
7. **Users execute assets in their own compatible AI assistants.**
8. **Compatibility, testing and certification are separate claims.**
9. **Generated customer artifacts are not automatically Verlune Certified.**
10. **MARKETING CLAIM <= OBSERVED EVIDENCE.**
11. **The launch catalog stays intentionally small enough to test well.**
12. **No asset is promoted just to increase the visible item count.**

## Public artifact types

### Structured Prompt

A reusable instruction for a bounded task.

Minimum customer contract:

- purpose / outcome;
- required inputs;
- optional context when material;
- constraints;
- execution instructions;
- output shape;
- missing-information / fallback behavior;
- verification guidance.

### Premium Prompt

A prompt for a more complex or specialized task. A Premium Prompt may add:

- multi-stage execution;
- configurable behavior;
- evidence rules;
- decision criteria;
- stronger fallback behavior;
- advanced output contracts;
- adaptation guidance;
- worked examples;
- named runtime evidence and limitations.

Premium is a capability classification, not a claim that every Premium Prompt is certified.

### Workflow

A reusable process in which AI participates across multiple steps, states or decisions.

A workflow normally defines:

- trigger / start condition;
- required and optional inputs;
- process stages;
- rules / invariants;
- decision or escalation states;
- outputs;
- fallback / blocked behavior;
- verification.

### Premium Workflow

A deeper or specialized workflow that may additionally include:

- configurable policy;
- stronger evidence semantics;
- advanced decision states;
- worked examples;
- adaptation guidance;
- runtime test fixtures;
- evidence card;
- known limitations;
- versioned release identity.

## Customer-facing categories

Free and Premium use the same category system.

1. **Development & Tech**
2. **Study & Learning**
3. **Research & Analysis**
4. **Business & Operations**
5. **Writing & Communication**
6. **Content & Marketing**
7. **Planning & Productivity**
8. **Career & Job Search**

Categories organize customer discovery. They do not imply that every category has equal launch inventory.

Industry/profession-specific assets (for example hospitality, architecture, education administration or legal administration) should use secondary tags or later collections rather than fragmenting the primary navigation.

High-stakes domains require separate safety review before public promotion. A generic category does not authorize medical diagnosis, legal advice, regulated financial advice or other professional substitution.

## Tier model

### Verlune Free

Purpose: let a stranger solve real tasks and understand the Verlune method before paying.

Free may contain:

- structured prompts across the public categories;
- selected complete workflows;
- basic examples;
- verification guidance;
- a concise introduction to prompt/workflow anatomy.

Free assets must be genuinely usable. They must not be intentionally degraded to create an upgrade.

Conceptual boundary:

> **USE VERLUNE**

### Verlune Premium

Launch price hypothesis: **USD 9 one-time**.

Premium contains:

- Premium Prompt Library;
- Premium Workflow Library;
- Prompt Builder;
- Workflow Builder;
- adaptation guidance;
- evaluation toolkit;
- deeper examples and evidence surfaces.

Conceptual boundary:

> **USE VERLUNE + GO DEEPER + ADAPT + BUILD + TEST**

The purchase is for the paid product and entitlement described at checkout. Do not promise all future major releases, unlimited AI usage, cloud storage or a perpetual stream of new content unless a later commercial contract explicitly adds those obligations.

## Builders

### Prompt Builder

Customer intent:

> "I need AI to perform this task well and repeatedly."

The customer should be able to describe the task naturally. The Builder should gather only material missing information and produce a reusable prompt with explicit inputs, constraints, output and fallback/verification behavior.

The Builder must not require the customer to understand terms such as evidence semantics, operating contract or prompt architecture.

### Workflow Builder

Customer intent:

> "I repeatedly go through this process and AI participates in it."

The Builder should discover:

- trigger;
- outcome;
- required inputs;
- optional context;
- stages;
- decisions / states;
- boundaries;
- output consumer;
- fallback behavior;
- verification.

It then produces a reusable workflow contract.

### Builder execution model for v1

The Builder UI lives in Verlune, but model execution happens in the customer's own AI assistant.

```text
VERLUNE PREMIUM AREA
        ↓
PROMPT BUILDER / WORKFLOW BUILDER
        ↓
COPY / OPEN IN SUPPORTED ASSISTANT
        ↓
CUSTOMER'S AI
        ↓
GUIDED INTERVIEW
        ↓
CUSTOM ARTIFACT
```

The Markdown/source file may exist internally, but "open this .md file" is not the intended primary customer experience.

## Access architecture target

For v1, the preferred entitlement model is:

```text
PUBLIC VERLUNE
   ↓
LEMON SQUEEZY PURCHASE
   ↓
PURCHASE ENTITLEMENT / LICENSE
   ↓
VERLUNE UNLOCK
   ↓
SERVER-SIDE VALIDATION
   ↓
SECURE BROWSER SESSION
   ↓
PREMIUM AREA
```

Target constraints:

- no mandatory user-created password for v1;
- no custom password-reset system;
- purchase entitlement is the access proof;
- never expose provider secrets to the browser;
- entitlement validation remains fail-closed.

This is an architecture target until the exact live provider configuration and end-to-end flow are verified.

## Product surface

Target Premium navigation:

```text
Explore
├── All
├── Development & Tech
├── Study & Learning
├── Research & Analysis
├── Business & Operations
├── Writing & Communication
├── Content & Marketing
├── Planning & Productivity
└── Career & Job Search

Build
├── Prompt Builder
└── Workflow Builder

Learn
├── Prompt Anatomy
├── Workflow Anatomy
├── Adaptation
└── Evaluation

Access
└── License / entitlement state
```

## Evidence vocabulary

Customer-facing evidence labels may include:

- `VERSIONED`
- `STRUCTURE CHECKED`
- `RUNTIME TESTED`
- `IMPROVED`
- `CERTIFIED`
- `KNOWN LIMITATIONS`

A customer-built artifact may be labeled:

- `CUSTOM`
- `GENERATED`
- `STRUCTURE CHECKED`
- `USER TESTED`

It must not inherit `VERLUNE CERTIFIED` without the corresponding governed evidence.

## Explicit v1 exclusions

The initial product does **not** require:

- a Verlune-hosted chatbot;
- proprietary model hosting;
- AI credits;
- token billing;
- subscriptions;
- a prompt marketplace;
- social features;
- teams/collaboration;
- cloud workflow storage;
- a mobile app;
- a browser extension;
- thousands of prompts;
- universal model compatibility claims.

These remain future hypotheses, not launch requirements.

## Launch success definition

The first commercial objective is not catalog size.

The product succeeds at launch when an unknown user can:

1. understand what Verlune is;
2. find a relevant Free asset;
3. get a useful result;
4. understand why Premium is materially different;
5. purchase with low friction;
6. unlock Premium;
7. use a Premium prompt/workflow successfully;
8. create a useful custom prompt or workflow with a Builder;
9. understand what is verified and what remains uncertain.

The first genuine purchase is market evidence. Controlled tests, founder self-purchases, test-mode transactions and friendly favors are not substitutes for that evidence.
