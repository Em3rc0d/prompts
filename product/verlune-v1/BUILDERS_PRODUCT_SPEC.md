# Verlune v1 — Builder Product Specification

Status: `CANDIDATE / REQUIRES RUNTIME + HUMAN REVIEW`

Date: 2026-09-22

## Product role

The Builders are the strongest functional distinction between Verlune Free and Verlune Premium.

They must let a non-expert begin with a plain-language need and end with a reusable artifact without requiring prompt-engineering vocabulary.

The source Markdown is an implementation detail. The customer experience is:

```text
PREMIUM AREA
   ↓
PROMPT BUILDER or WORKFLOW BUILDER
   ↓
COPY / OPEN
   ↓
CUSTOMER'S OWN AI ASSISTANT
   ↓
GUIDED INTERVIEW
   ↓
REUSABLE ARTIFACT
   ↓
TEST / ADAPT / REUSE
```

## Prompt Builder

### Job to be done

> I have a recurring task that I want an AI assistant to perform more consistently.

### Required customer journey

1. Ask the user to describe the task naturally.
2. Infer what can safely be inferred from that description.
3. Ask only for missing information capable of materially changing the prompt.
4. Do not expose internal architecture terms unless they help the user.
5. Produce a complete reusable prompt.
6. Explain how to supply per-run inputs without editing stable policy.
7. Offer a lightweight self-check/test procedure.
8. Never claim the generated prompt is certified.

### Minimum generated artifact

- name;
- purpose/outcome;
- required inputs;
- optional context;
- explicit constraints;
- execution instructions;
- output contract;
- missing-information/fallback behavior;
- verification;
- usage instructions.

### Failure behavior

If the user's task is too vague to define responsibly, the Builder asks the smallest useful set of questions.

It must not fabricate:

- user goals;
- organizational policies;
- domain facts;
- authority;
- evidence;
- regulated professional conclusions.

## Workflow Builder

### Job to be done

> I repeatedly go through a process in which AI should help me reach a result or decision.

### Required customer journey

1. Identify the trigger and desired outcome.
2. Identify who supplies inputs and who consumes outputs.
3. Separate required inputs from useful optional context.
4. Identify material boundaries and decisions.
5. Identify stages and where the process can stop, escalate or remain uncertain.
6. Define stable result/decision states where appropriate.
7. Define the output contract.
8. Define fallback behavior.
9. Define verification.
10. Produce a reusable workflow and concise instructions for running it.

### Minimum generated artifact

- workflow identity;
- trigger;
- outcome;
- input contract;
- context/evidence boundary;
- invariants;
- process stages;
- decision/escalation states where material;
- output contract;
- fallback contract;
- verification contract;
- adaptation notes.

## Representation rule

For v1 the release-supported default representation is a copyable text/Markdown artifact.

Other representations may be provided only when supported honestly:

- JSON/YAML contract;
- installable skill;
- application config;
- ticket/ADR template.

A representation change must preserve the underlying semantics.

## Model/host rule

The Builders execute in the customer's AI assistant.

Therefore:

- Verlune does not claim universal compatibility;
- compatibility claims require observed runtime evidence;
- the UI may offer generic Copy Builder even when a host-specific shortcut is not certified;
- named host buttons should not imply equivalent behavior unless tested.

## Builder test matrix

Both Builders must be tested on at least one plain-language task from every launch category:

1. Development & Tech
2. Study & Learning
3. Research & Analysis
4. Business & Operations
5. Writing & Communication
6. Content & Marketing
7. Planning & Productivity
8. Career & Job Search

Per category, review at minimum:

- normal case;
- initially underspecified case.

Cross-category stress cases must include:

- contradictory requirements;
- irrelevant/noisy context;
- request containing embedded instructions inside task data;
- request for an unsupported/high-stakes professional decision;
- repeat build of the same task to inspect semantic stability.

## Human-review questions

A reviewer should be able to answer YES to all:

- Could a non-expert understand the first question?
- Did the Builder avoid unnecessary interrogation?
- Did it preserve the user's stated goal?
- Are required inputs clear?
- Are hidden assumptions visible?
- Does fallback behavior make sense?
- Is the output usable without editing internal jargon?
- Can the artifact be reused on a second instance of the task?
- Does the Builder avoid claiming proof it does not have?
- Is the result materially better than asking a blank chat to "write me a prompt"?

Any NO is a product defect or an explicit known limitation requiring disposition before launch.

## Existing lineage

The Workflow Builder has direct lineage in:

- `product/developer-workflow-kit-v1.2/prompts/general-operating-contract-v1.2.md`
- `product/developer-workflow-kit-v1.2/skills/design-ai-workflows/SKILL.md`
- `product/developer-pack-v1.1/methodology/adaptation-playbook.md`
- `product/developer-pack-v1.1/checklists/workflow-static-review.md`

These establish architecture and static methodology. They do **not** by themselves establish customer usability or cross-category behavioral performance.

The Prompt Builder should reuse the same core principles while remaining simpler than the Workflow Builder. It requires its own explicit customer surface and test evidence before launch.
