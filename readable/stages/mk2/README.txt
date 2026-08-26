PROMPT QUARRY — HUMAN READING COPY
========================================================================================
STAGE / DOCUMENT     : MK2
SOURCE REPOSITORY FILE: mk2/README.md
CONTENT ORIGIN       : REPOSITORY DOCUMENTATION

# MK2 — Prompt Engine

> **Question:** Can the system automatically select, compose, test and improve prompts for a specific task?

MK2 is the future autonomous orchestration layer.

MK2 is intentionally defined before implementation so we do not accidentally call a prompt generator an "engine" before it can actually make evidence-backed decisions.

## Dependency chain

```text
MK0 — Knowledge Quarry
What exists?
        │
        ▼
MK1 — Prompt Forge
Can we engineer and certify better prompts?
        │
        ▼
MK2 — Prompt Engine
Can the system select, compose, evaluate and adapt them automatically?
```

MK2 depends on stable MK1 contracts and evaluation receipts. It must not skip directly from raw source material to autonomous prompt mutation.

## Target behavior

Given a concrete task, MK2 should eventually be able to:

1. classify intent/domain/risk;
2. retrieve appropriate MK0 knowledge and MK1 certified building blocks;
3. choose an architecture;
4. compose or select a prompt;
5. select the correct fixture/evaluation profile;
6. execute candidate evaluation;
7. compare alternatives;
8. choose a certified prompt when one exists;
9. generate a new MK1 candidate when no suitable certified prompt exists;
10. preserve all decision/evaluation provenance.

## Conceptual pipeline

```text
TASK
 │
 ▼
Intent / Domain / Risk Router
 │
 ├── retrieve certified MK1 prompt
 │            │
 │            └──────────────┐
 │                           ▼
 └── no strong match → Compose Candidate
                              │
                              ▼
                         MK1 Forge Gate
                              │
                         ┌────┴────┐
                         │         │
                       FAIL      PASS
                         │         │
                         │         ▼
                         │    Candidate Pool
                         │         │
                         └─────────┤
                                   ▼
                           Evaluator / Selector
                                   │
                                   ▼
                               EXECUTION
                                   │
                                   ▼
                         receipt + feedback signal
```

## What makes MK2 different from MK1

MK1 can create and certify a prompt.

MK2 decides **which prompt/architecture should be used now** and can invoke MK1 to build a missing one.

That decision requires:

- retrieval;
- task/risk classification;
- version-aware prompt selection;
- runtime/evaluation receipts;
- controlled adaptation;
- rollback/deprecation semantics.

## Future modules

### E1 — Task Router

Classify task intent, domain, risk and required evidence level.

### E2 — Prompt Retriever

Rank MK1 certified artifacts against the task contract.

### E3 — Architecture Composer

Compose from certified patterns when retrieval does not produce a sufficient artifact.

### E4 — Evaluation Planner

Choose fixtures/rubrics appropriate to the task and risk class.

### E5 — Candidate Tournament

Evaluate multiple candidates under comparable conditions and select using evidence rather than aesthetic preference.

### E6 — Runtime Adapter

Adjust model-specific formatting/capabilities while preserving the task contract.

### E7 — Feedback / Regression Loop

Turn meaningful failures into fixtures and feed new knowledge back into MK0/MK1 characterization.

```text
runtime incident
      ↓
characterize failure
      ↓
fixture / evidence
      ↓
MK0 knowledge update
      ↓
MK1 revision + certification
      ↓
MK2 selection update
```

## Non-goals for early MK2

- uncontrolled self-modification;
- automatic claims that a new candidate is better without evaluation;
- replacing provenance with opaque embedding similarity;
- silently changing certified prompt contracts;
- treating model output preference as objective quality without a task rubric.

## MK2 readiness gate

Do not begin core MK2 implementation until MK1 can demonstrate:

- a stable prompt artifact contract;
- versioned fixture sets;
- durable evaluation receipts;
- a meaningful set of certified prompts in more than one domain;
- baseline comparison;
- repeatable certification logic;
- deprecation/version semantics.

Until those receipts exist, MK2 remains architecture, not product capability.
