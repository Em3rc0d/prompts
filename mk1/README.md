# MK1 — Prompt Forge

> **Question:** Can we build better prompts from the knowledge characterized in MK0?

MK1 is the engineering layer of Prompt Quarry.

It does not exist to reproduce a source collection. It exists to design, assemble, test, compare and certify **Prompt Quarry engineered** artifacts using MK0 as evidence and knowledge.

## Core rule

```text
MK1 != copy(MK0)

MK1 =
  characterized patterns from MK0
+ domain/task requirements
+ explicit architecture
+ constraints and output contracts
+ tests
+ critique
+ measurable comparison
```

## Prompt Forge pipeline

```text
USER / PRODUCT BRIEF
        │
        ▼
1. Intent + domain classification
        │
        ▼
2. Retrieve MK0 evidence/patterns/fixtures
        │
        ▼
3. Select prompt architecture
        │
        ▼
4. Assemble candidate prompt
        │
        ▼
5. Static lint / contract validation
        │
        ▼
6. Critic pass
        │
        ▼
7. Fixture evaluation
        │
        ▼
8. Baseline comparison
        │
        ▼
9. Quality rubric
        │
   ┌────┴─────┐
   │          │
 REJECT     CERTIFY
   │          │
   └─revise   ▼
         MK1 CERTIFIED LIBRARY
```

## Candidate prompt architecture

MK1 starts with the following canonical construction model:

```text
PURPOSE
↓
ROLE
↓
CONTEXT
↓
INTAKE
↓
ASSUMPTIONS
↓
PROCESS
↓
RULES / CONSTRAINTS
↓
OUTPUT CONTRACT
↓
QUALITY GATE
↓
FALLBACK / UNCERTAINTY BEHAVIOR
```

Not every prompt needs every block. The Forge must justify omission rather than adding ceremonial sections that do not improve task performance.

## MK1 artifact states

A prompt moves through explicit states:

- `DRAFT` — human- or system-authored candidate, untested;
- `VALID` — satisfies the prompt contract and static rules;
- `TESTED` — executed against its declared fixture set;
- `CANDIDATE` — has a complete evaluation receipt and baseline comparison;
- `CERTIFIED` — passes the MK1 quality gate;
- `REJECTED` — fails a blocking criterion;
- `DEPRECATED` — previously certified but superseded or invalidated.

`GENERATED` is not a quality state. Generation is an implementation event; a generated prompt can still be bad.

## What MK1 may use from MK0

Preferred inputs:

- Golden Fixtures;
- technique vectors and aggregate architecture statistics;
- reviewed patterns such as RIRO;
- repository-authored templates;
- canonical taxonomy;
- source metadata for intent/domain discovery;
- human-review notes and regression incidents.

Raw source bodies should not be treated as a hidden template library.

## MK1 output contract

Each engineered prompt must have both:

1. a machine-readable record for evaluation/versioning;
2. a human-readable prompt file that can be understood and used directly.

See `specs/PROMPT_CONTRACT.md`.

## Certification principle

A prompt is **not** called "improved" merely because it is longer, cleaner or more sophisticated-looking.

An improvement claim requires:

- an identified baseline;
- an evaluation fixture set;
- rubric scores;
- no regression on blocking dimensions;
- a concrete reason for the improvement claim.

If there is no baseline receipt, the correct label is **engineered candidate**, not **improved prompt**.

## Initial MK1 work packages

### F1 — Contract

- canonical prompt schema;
- human-readable format;
- version identity;
- provenance back to MK0 inputs.

### F2 — Architecture selector

Given a task, choose the smallest useful set of blocks/techniques.

### F3 — Assembler

Build a candidate from selected architecture + task brief.

### F4 — Static critic

Detect contradictions, missing variables, vague output contracts, unsupported assumptions, unnecessary verbosity and unsafe high-stakes behavior.

### F5 — Fixture runner

Evaluate the candidate against declared MK0/MK1 fixtures.

### F6 — Baseline comparator

Compare candidate performance against a simpler/reference prompt under the same test conditions.

### F7 — Certification gate

Apply the quality rubric and produce a durable receipt.

## MK1 directories

```text
mk1/
├── README.md
├── specs/
│   └── PROMPT_CONTRACT.md
├── rubrics/
│   └── PROMPT_QUALITY_RUBRIC.md
├── fixtures/
│   └── README.md
├── candidates/        # future generated/test candidates
├── certified/         # future certified prompt artifacts
└── receipts/          # future evaluation receipts
```

Empty implementation directories are intentionally not pre-filled with fake outputs. MK1 documentation defines the contract before the Forge begins producing claims.

## MK1 boundary

MK1 ends when Prompt Quarry can reliably produce and certify reusable prompts for known tasks.

Automatic task detection, dynamic retrieval, autonomous composition and continuous self-improvement belong to MK2.
