# Prompt Quarry Roadmap

Prompt Quarry evolves through explicit capability stages.

The stages are architectural maturity levels, not marketing labels.

```text
MK0 — KNOWLEDGE QUARRY
"What exists?"
        │
        ▼
MK1 — PROMPT FORGE
"Can we build better prompts from it?"
        │
        ▼
MK2 — PROMPT ENGINE
"Can the system select, compose, test and improve prompts automatically?"
```

## MK0 — Knowledge Quarry

### Mission

Build a trustworthy knowledge base of prompt/skill/workflow evidence, reusable patterns and regression fixtures.

### Current status

**ACTIVE / USABLE FOUNDATION**

Current receipts include:

- public Alpacka prompt directory characterized;
- 530 prompt references mapped;
- 52 free prompt bodies structurally analyzed in memory;
- 478 premium source records characterized with explicit access boundary;
- 478 repository-authored usable reconstructions produced for those premium references;
- 22 prompt categories mapped;
- 12 public Skills characterized;
- generator and blog surfaces characterized;
- technique mining operational;
- Golden Dataset operational;
- human-readable TXT layer operational;
- provenance and validation gates operational.

### MK0 next improvements

- primary Threads ingestion when official access is configured;
- additional independent source families;
- semantic near-duplicate benchmark;
- hand-reviewed characterization set for technique detector precision/recall;
- more failure/regression fixtures;
- source snapshot/version semantics for incremental sync.

MK0 may continue evolving while MK1 begins. MK1 must reference the specific MK0 evidence/version used for a certification receipt.

---

## MK1 — Prompt Forge

### Mission

Produce Prompt Quarry engineered prompts that are functional, understandable, testable and evidence-backed.

### Phase F0 — Contracts

Status: **STARTED**

Deliverables:

- `mk1/README.md`;
- prompt artifact contract;
- quality rubric;
- fixture strategy;
- state/version semantics.

Exit gate:

- a human and a machine can determine exactly what an MK1 candidate contains and what evidence is required for certification.

### Phase F1 — First canonical architecture

Deliverables:

- architecture/block selector;
- rules for when to use/omit PURPOSE, ROLE, CONTEXT, INTAKE, ASSUMPTIONS, PROCESS, CONSTRAINTS, OUTPUT, QUALITY and FALLBACK;
- static prompt linter.

Exit gate:

- architecture decisions are explainable and no longer equivalent to "always use the same long template".

### Phase F2 — Candidate assembler

Deliverables:

- deterministic candidate assembly from a task brief + selected blocks;
- stable prompt IDs/versioning;
- machine + human-readable outputs.

Exit gate:

- repeated generation from the same contract is traceable and structurally valid.

### Phase F3 — Critic and static validation

Deliverables:

- contradiction detector;
- undefined variable detector;
- vague-output detector;
- redundant-instruction detector;
- provenance/truth-boundary checks;
- high-stakes boundary checks.

Exit gate:

- known static defects become test fixtures and cannot silently reach certification.

### Phase F4 — Fixture runner

Deliverables:

- task-specific MK1 fixture sets;
- happy/minimal/missing/ambiguous/contradictory/regression cases;
- versioned execution receipts.

Exit gate:

- candidate behavior can be compared on stable cases.

### Phase F5 — Baseline comparator

Deliverables:

- baseline artifact declaration;
- same-fixture candidate/baseline execution;
- dimension deltas;
- regression reporting.

Exit gate:

- "improved" becomes an evidence-backed label rather than aesthetic judgment.

### Phase F6 — Certification

Deliverables:

- rubric evaluator;
- blocking-failure gate;
- durable certification receipt;
- `CERTIFIED` / `REJECTED` / `DEPRECATED` state transitions;
- first multi-domain certified prompt set.

Exit gate:

- Prompt Quarry can reliably answer: **why is this prompt certified and what did it beat?**

---

## MK2 — Prompt Engine

### Mission

Select or compose the right prompt for a task and evaluate that decision automatically.

### Entry gate

MK2 begins only after MK1 has:

- stable contracts;
- versioned fixtures;
- repeatable certification;
- multiple certified prompt families;
- baseline comparison receipts;
- deprecation/version behavior.

### Expected phases

- E1 Task/Domain/Risk Router;
- E2 Certified Prompt Retriever;
- E3 Architecture Composer;
- E4 Evaluation Planner;
- E5 Candidate Tournament;
- E6 Model/Runtime Adapter;
- E7 Feedback + Regression Loop.

## Cross-stage rule

The most important architectural flow is circular but controlled:

```text
MK2 runtime failure
        ↓
characterize evidence
        ↓
MK0 fixture / knowledge
        ↓
MK1 candidate revision
        ↓
MK1 certification
        ↓
MK2 selection/runtime update
```

We do not patch MK2 symptoms forever. Meaningful failures become permanent knowledge and regression evidence.

## Naming rule

Use these labels precisely:

- **source-observed** — directly supported by source evidence;
- **derived** — inferred/aggregated from evidence;
- **engineered** — repository-authored artifact designed from knowledge;
- **tested** — executed against an identified fixture set;
- **certified** — passes the declared MK1 gate;
- **improved** — supported by a fair baseline comparison receipt.

These words are part of the evidence contract, not interchangeable adjectives.
