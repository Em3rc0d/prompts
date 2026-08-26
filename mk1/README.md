# MK1 — Prompt Forge

> **Question:** Can we build better prompts from the knowledge characterized in MK0?

MK1 is the engineering layer of Prompt Quarry.

It does not exist to reproduce a source collection. It exists to design, assemble, test, compare and eventually certify **Prompt Quarry engineered** artifacts using MK0 as evidence and knowledge.

## Current status

```text
F0 — Contracts                         COMPLETE
F1 — Architecture selector + linter    COMPLETE / CI PASS
F2 — Candidate assembler               COMPLETE / 3 VALID CANDIDATES
F3 — Semantic/static critic            COMPLETE / 3 PASS RECEIPTS
F4A — Behavioral harness               COMPLETE / CI CHARACTERIZATION PASS
F4B — Real behavioral execution        PIPELINE COMPLETE / REAL RECEIPT REQUIRED
F5 — Baseline comparator               PLANNED / BLOCKED ON F4B
F6 — Certification                     PLANNED
```

Current persisted F2 candidates:

- `candidates/f2/content_clear_rewrite/`
- `candidates/f2/software_code_review/`
- `candidates/f2/research_technical_decision/`

Current persisted F3 receipts:

- `candidates/f3/manifest.json`
- `candidates/f3/INDEX.txt`
- `candidates/f3/reports/*.critic.json`
- `candidates/f3/reports/*.critic.txt`

All three F3 receipts currently report:

```text
critic_status = PASS
blocking = 0
errors = 0
warnings = 0
```

Current F4B repository evidence:

```text
real *.receipt.json files = 0
persisted TESTED artifacts = 0
```

The underlying prompt artifacts therefore still satisfy:

```text
state = VALID
claims = [engineered]
lint = PASS
receipt_id = null
rubric_score = null
```

Therefore **no MK1 artifact is currently claimed as TESTED, CANDIDATE, CERTIFIED or IMPROVED**.

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
6. Semantic/static critic              ← F3 COMPLETE
        │
        ▼
7. Behavioral fixture evaluation       ← F4A COMPLETE / F4B REAL RUN NEXT
        │
        ▼
8. Baseline comparison                 ← F5 BLOCKED ON F4B
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
- `TESTED` — executed against a declared behavioral fixture set under an identified runtime, with required reviews resolved;
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

F3 found a real assembler defect: some brief constraints were duplicated in both CONTEXT and CONSTRAINTS. The assembler was corrected, output contracts were strengthened by intent, and the duplicate-instruction case became a regression fixture rather than an accepted warning.

## F3 — Semantic/static critic

Status: **COMPLETE — RECEIPTS PERSISTED**

Implementation:

- `../tools/mk1_prompt_critic.py`
- `../tools/test_mk1_f3.py`
- `../tools/mk1_build_f3_critic_reports.py`
- `../.github/workflows/validate-mk1-f3.yml`
- `../.github/workflows/build-mk1-f3-critic-reports.yml`
- `candidates/f3/`

F3 checks include semantic contradictions, vague output contracts, duplicate instructions, unsupported assumptions, provenance/truth-boundary risks, high-stakes boundary quality and architecture overfit.

Current materialized F3 baseline: 3 reports, all PASS with zero blockers/errors/warnings.

Important: **F3 remains static evidence. It does not change artifact state beyond VALID.**

## F4 — Behavioral fixtures and execution

F4 is split deliberately into two lanes.

### F4A — harness characterization

Status: **COMPLETE — CI PASS**

Implementation:

- `specs/F4_BEHAVIORAL_TESTING.md`
- `fixtures/f4/fixture-sets.json`
- `../tools/mk1_behavioral_runner.py`
- `../tools/mk1_prepare_f4_execution.py`
- `../tools/mk1_promote_tested.py`
- `../tools/mk1_materialize_f4_tested.py`
- `../tools/validate_mk1_f4_repository.py`
- `../tools/test_mk1_f4.py`
- `../.github/workflows/validate-mk1-f4.yml`
- `receipts/f4/README.md`

Current fixture inventory:

```text
3 versioned fixture sets
15 behavioral fixtures
classes:
  happy-path
  minimal
  missing-critical
  ambiguous
  contradictory
  edge
  noise
  regression
```

The F4A gate proves the harness and state-transition semantics:

- synthetic PASS can never promote state;
- runtime identity is required for real execution;
- machine assertion failure blocks promotion;
- unresolved blocking human review blocks promotion;
- artifact/receipt version mismatch is rejected;
- only a real `BEHAVIORAL_PASS` receipt may become eligible for `TESTED`;
- a persisted `TESTED` artifact must exactly equal the deterministic promotion of its F2 source + persisted receipt.

### F4B — real behavioral execution

Status: **PIPELINE COMPLETE / AWAITING FIRST REAL RECEIPT**

Automation:

- `../.github/workflows/build-mk1-f4-tested.yml`

The workflow is triggered only by root-level:

```text
mk1/receipts/f4/*.receipt.json
```

Execution envelopes or documentation do not trigger TESTED materialization.

The workflow requires at least one receipt and re-runs F1 → F4 gates before materializing. Every generated `artifact.json` is schema-validated and must retain:

```text
state = TESTED
claims = [engineered, tested]
baseline_id = null
rubric_score = null
```

The repository evidence validator also fails if a TESTED artifact exists without a matching persisted real receipt or if it differs from deterministic reconstruction.

The next evidence-producing step is therefore narrow and explicit:

1. choose the exact F2 artifact + fixture set;
2. execute it under an identified real runtime;
3. record actual outputs verbatim;
4. resolve every declared blocking human check;
5. generate the F4 receipt;
6. persist `<run>.receipt.json` under `mk1/receipts/f4/`;
7. let the F4B workflow materialize the TESTED bundle.

Until step 6 happens:

```text
all three prompt artifacts remain VALID
TESTED count = 0
```

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
│   ├── f1/
│   └── f4/
├── briefs/
├── candidates/
│   ├── f2/                # 3 current VALID engineered candidates
│   ├── f3/                # persisted static critic receipts
│   └── f4/                # generated only from eligible real F4 receipts
├── certified/             # future F6 artifacts
└── receipts/
    └── f4/                # observed behavioral receipts; currently none
```

MK1 ends when Prompt Quarry can reliably produce and certify reusable prompts for known tasks.

Automatic runtime task detection, retrieval, autonomous composition and adaptive selection belong to MK2.
