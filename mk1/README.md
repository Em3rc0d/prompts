# MK1 — Prompt Forge

> **Question:** Can we build better prompts from the knowledge characterized in MK0?

MK1 is the engineering layer of Prompt Quarry.

It does not exist to reproduce a source collection. It exists to design, assemble, test, compare and eventually certify **Prompt Quarry engineered** artifacts using MK0 as evidence and knowledge.

## Current status

```text
F0 — Contracts                         COMPLETE
F1 — Architecture selector + linter    COMPLETE / CI PASS
F2 — Candidate assembler               COMPLETE / 3 VALID CANDIDATES
F3 — Deeper critic                     NEXT
F4 — Behavioral fixture runner         PLANNED
F5 — Baseline comparator               PLANNED
F6 — Certification                     PLANNED
```

Current persisted F2 candidates:

- `candidates/f2/content_clear_rewrite/`
- `candidates/f2/software_code_review/`
- `candidates/f2/research_technical_decision/`

Each candidate currently satisfies:

```text
state = VALID
claims = [engineered]
lint = PASS
receipt_id = null
rubric_score = null
```

Therefore **no MK1 artifact is currently claimed as TESTED, CERTIFIED or IMPROVED**.

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
3. Select prompt architecture          ← F1 COMPLETE
        │
        ▼
4. Assemble candidate prompt           ← F2 COMPLETE
        │
        ▼
5. Static lint / contract validation   ← F1/F2 COMPLETE
        │
        ▼
6. Critic pass                         ← F3 NEXT
        │
        ▼
7. Fixture evaluation                  ← F4
        │
        ▼
8. Baseline comparison                 ← F5
        │
        ▼
9. Quality rubric                      ← F6
        │
   ┌────┴─────┐
   │          │
 REJECT     CERTIFY
   │          │
   └─revise   ▼
         MK1 CERTIFIED LIBRARY
```

## Candidate prompt architecture

MK1 uses the following block vocabulary:

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

Not every prompt needs every block. The selector chooses the smallest purposeful architecture and records why each block was selected.

Observed F1 examples:

- simple rewrite → `PURPOSE+CONTEXT+OUTPUT_CONTRACT+QUALITY_GATE`;
- code review/research → full reliability architecture;
- high-stakes legal → full architecture plus safety/confidence/fallback techniques.

## MK1 artifact states

A prompt moves through explicit states:

- `DRAFT` — authored/assembled, not statically valid yet;
- `VALID` — satisfies artifact schema and static lint rules;
- `TESTED` — executed against a declared behavioral fixture set;
- `CANDIDATE` — complete evaluation receipt and baseline comparison available;
- `CERTIFIED` — passes the MK1 quality gate;
- `REJECTED` — fails a blocking criterion;
- `DEPRECATED` — previously certified but superseded or invalidated.

`GENERATED` is not a quality state. Generation is an implementation event; a generated prompt can still be bad.

## What MK1 consumes from MK0

Preferred inputs:

- Golden Fixtures;
- technique vectors and aggregate architecture statistics;
- reviewed patterns such as RIRO;
- repository-authored templates;
- canonical taxonomy;
- source metadata for intent/domain discovery;
- human-review notes and regression incidents.

Raw source bodies are not treated as a hidden template library.

## F0 — Contract foundation

Canonical contracts:

- `specs/PROMPT_CONTRACT.md`
- `specs/TASK_BRIEF.schema.json`
- `specs/PROMPT_ARTIFACT.schema.json`
- `rubrics/PROMPT_QUALITY_RUBRIC.md`
- `fixtures/README.md`

These define state, provenance, versioning, task briefs, prompt artifacts, behavioral fixtures and certification semantics.

## F1 — Architecture selector + linter

Implementation:

- `../tools/mk1_architecture_selector.py`
- `../tools/mk1_prompt_linter.py`
- `fixtures/f1/selector-cases.json`
- `../tools/test_mk1_f1.py`
- `../.github/workflows/validate-mk1-f1.yml`

The F1 CI characterization gate passes:

- 5/5 architecture selector fixtures;
- 6/6 linter regression cases.

Guardrails include:

- undefined-variable rejection;
- section/architecture mismatch detection;
- high-stakes safety/fallback requirements;
- unsupported `improved` claim rejection;
- `CERTIFIED` score/receipt checks;
- invalid `GENERATED` quality-state rejection.

## F2 — Candidate assembler

Implementation:

- `../tools/mk1_candidate_assembler.py`
- `../tools/test_mk1_f2.py`
- `../tools/mk1_build_f2_candidates.py`
- `../.github/workflows/validate-mk1-f2.yml`
- `../.github/workflows/build-mk1-f2-candidates.yml`

A Task Brief is transformed into:

```text
brief
  ↓
architecture.json
  ↓
artifact.json
  ↓
lint.json
  ↓
prompt.txt
```

The three current F2 bundles are deterministic, human-readable and statically valid. Their `prompt.txt` files explicitly say that `VALID` does not mean tested/certified/improved.

## F3 — Next: deeper critic

F3 extends beyond the existing linter into a richer quality critic.

Planned checks:

- semantic contradictions across sections;
- vague or unverifiable output contracts;
- repeated/redundant instructions;
- unsupported assumptions;
- provenance/truth-boundary risks;
- high-stakes domain discipline;
- severity and remediation suggestions;
- regression fixtures for every meaningful defect.

## Certification principle

A prompt is **not** called `improved` merely because it is longer, cleaner or more sophisticated-looking.

An improvement claim requires:

- an identified baseline;
- the same evaluation fixture set;
- rubric scores/deltas;
- no hidden blocking regression;
- a durable receipt explaining the claim.

Without that receipt, the correct label remains **engineered candidate**.

## MK1 directories

```text
mk1/
├── README.md
├── specs/
├── rubrics/
├── fixtures/
├── briefs/
├── candidates/
│   └── f2/                # 3 current VALID engineered candidates
├── certified/             # future F6 artifacts
└── receipts/              # future F4-F6 evaluation receipts
```

MK1 ends when Prompt Quarry can reliably produce and certify reusable prompts for known tasks.

Automatic runtime task detection, retrieval, autonomous composition and adaptive selection belong to MK2.
