# Developer Pack v1.1 — Product Specification

Status: `DRAFT / NOT FOR SALE`

Target version: `1.1.0`

## 1. Product objective

Developer Pack v1.1 is the reusable system behind Prompt Quarry's finished developer prompts.

It should help a developer or engineering team convert a vague AI task into a governed workflow with explicit inputs, evidence rules, operating constraints, output contracts, fallback behavior, and verification.

The product is not a collection of clever prompt phrases.

## 2. Customer outcome

A customer should be able to:

1. choose an appropriate operating template;
2. parameterize it for a real engineering workflow;
3. identify which context and evidence can materially change the result;
4. define output and escalation contracts;
5. run the workflow repeatedly without silently changing its rules;
6. inspect whether an answer stayed inside the evidence boundary;
7. adapt the workflow for their team or product without starting from a blank page.

## 3. Free vs Paid boundary

### Free Developer Starter Pack v1.1

Provides three field-ready finished workflows:

- Code Review;
- Bug Diagnosis;
- Technical Decision.

The customer can use and adapt those workflows directly.

### Developer Pack v1.1

Must provide the reusable construction system:

- parameterized operating templates;
- task and evidence configuration patterns;
- reusable output-contract patterns;
- escalation/fallback design;
- review and validation procedures;
- worked transformations from vague request → governed workflow;
- adaptation guidance for teams/apps;
- release/evidence discipline.

If a Paid asset can be replaced by copying a Free prompt and changing nouns, that Paid asset fails the product-quality gate.

## 4. Core operating architecture

Every reusable template should expose, where applicable:

```text
INTENT
  ↓
INPUT CONTRACT
  ↓
CONTEXT BOUNDARY
  ↓
EVIDENCE POLICY
  ↓
OPERATING PROCESS
  ↓
DECISION / ESCALATION RULES
  ↓
OUTPUT CONTRACT
  ↓
VERIFICATION
  ↓
FALLBACK / UNKNOWN
```

These sections are interfaces, not decoration. A section should exist only when it changes execution or inspection.

## 5. Template requirements

A core template must:

- define the task in terms of an outcome rather than a persona alone;
- identify required vs optional inputs;
- distinguish supplied evidence from model inference;
- specify forbidden inference or unsupported certainty;
- define how missing material changes execution;
- include task-specific process steps;
- expose configurable rules instead of baking every choice into prose;
- define a stable output contract;
- include verification criteria;
- include a fallback state for insufficient evidence;
- support deliberate adaptation without requiring the customer to reverse-engineer the template.

## 6. Evidence semantics

Prompt Quarry evidence-state labels remain separate from prompt-local evidence labels.

### Product evidence state

```text
DRAFT → VALID → TESTED → IMPROVED → CERTIFIED → PORTABLE
```

### Prompt-local evidence

A template may define task-specific labels such as:

```text
OBSERVED / INFERRED / UNKNOWN
CONFIRMED / LIKELY / QUESTION
SOURCE_CLAIM / ASSUMPTION / RECOMMENDATION
```

Those labels govern an individual task response. They do not establish F4–F7 product maturity.

## 7. Commercial value requirements

Before release candidate, the Pack must pass `quality/COMMERCIAL_VALUE_GATE.md`.

The gate evaluates whether the Paid Pack materially improves:

- breadth of reuse;
- parameterization;
- governance;
- integration value;
- verification;
- adaptation speed;
- inspectability;

relative to the Free Starter Pack.

Prompt count and file count are not valid substitutes for customer value.

## 8. Initial v1.1 hardening targets

### General Operating Contract

Reusable across technical task families. It should define configurable intake, evidence, process, decision, output, and verification layers.

### Software Code Review System

Reusable across repositories, PRs, patches, languages, risk profiles, and review policies. It must support customizable severity, evidence threshold, review lenses, ship decisions, and verification.

### Technical Research / Decision System

Reusable for build-vs-buy, architecture, tool/vendor, migration, dependency, and platform decisions. It must support hard constraints, criteria, evidence quality, source freshness, uncertainty, reversibility, and decision triggers.

## 9. Packaging rule

Developer Pack v1.1 receives a new product identity and fingerprint.

No customer-visible v1.0 file is silently changed in-place to represent v1.1.

No v1.0 approval receipt can authorize v1.1 distribution.

## 10. Claim boundary

Allowed during draft development:

- structured;
- reusable by design;
- parameterized;
- governed;
- statically inspectable.

Not allowed absent corresponding evidence:

- battle-tested;
- proven superior;
- behaviorally improved;
- certified;
- universally portable;
- guaranteed to improve outputs.

## 11. Release exit criteria

A v1.1 candidate may be proposed only when:

- intended customer asset inventory is frozen;
- core templates satisfy this specification;
- Free-vs-Paid commercial value gate passes;
- examples demonstrate real transformations rather than trivial substitutions;
- static validation and packaging checks pass;
- license and evidence boundaries are present;
- deterministic build tooling produces an exact candidate fingerprint.
