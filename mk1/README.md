# MK1 — Prompt Forge

> **Question:** Can we build better prompts from the knowledge characterized in MK0?

MK1 is the engineering layer of Prompt Quarry. It designs, assembles, tests, compares and certifies **Prompt Quarry engineered** artifacts using MK0 as evidence and knowledge.

MK1 does not reproduce a source collection and does not use provider diversity as a shortcut for quality.

## Canonical quality ladder

```text
DRAFT
  ↓
VALID
  ↓ F4 real behavioral evidence
TESTED
  ↓ F5 paired/blind baseline superiority
CANDIDATE / IMPROVED
  ↓ F6 repeated evidence on one declared target runtime
CERTIFIED
  ↓ F7 optional cross-provider evidence
PORTABLE
```

The key distinction is intentional:

- **CERTIFIED** = repeatedly proven on the declared target provider/model/family.
- **PORTABLE** = the already-certified prompt also preserves that contract across multiple providers/families.

Claude/Gemini/other providers are therefore **not required** to certify an OpenAI-targeted prompt. They are relevant only to F7 portability.

## Current infrastructure status

```text
F0 — Contracts                              COMPLETE
F1 — Architecture selector + linter         COMPLETE / CI CHARACTERIZED
F2 — Candidate assembler                    COMPLETE / 3 VALID CANDIDATES
F3 — Semantic/static critic                 COMPLETE / PASS RECEIPTS
F4 — Behavioral fixtures + real runner      INFRASTRUCTURE COMPLETE / REAL RECEIPTS REQUIRED
F5 — Paired blind baseline comparator       INFRASTRUCTURE COMPLETE / REAL RECEIPTS REQUIRED
F6 — Target-runtime certification           INFRASTRUCTURE COMPLETE / REAL F5 REPETITIONS REQUIRED
F7 — Cross-provider portability             INFRASTRUCTURE COMPLETE / OPTIONAL AFTER CERTIFICATION
```

Current foundational prompt families:

- `content_clear_rewrite`
- `software_code_review`
- `research_technical_decision`

Current real evidence boundary remains strict: no artifact may advance merely because CI characterized the harness.

## Core rule

```text
MK1 != copy(MK0)

MK1 =
  characterized patterns from MK0
+ domain/task requirements
+ explicit architecture
+ constraints and output contracts
+ behavioral fixtures
+ semantic critique
+ fair baseline comparison
+ durable execution evidence
```

## Prompt architecture vocabulary

MK1 selects the smallest purposeful subset of:

```text
PURPOSE
ROLE
CONTEXT
INTAKE
ASSUMPTIONS
PROCESS
RULES / CONSTRAINTS
OUTPUT CONTRACT
QUALITY GATE
FALLBACK / UNCERTAINTY BEHAVIOR
```

A larger prompt is not automatically better. Architecture blocks must be justified by task/risk/failure modes.

## F1 — Static architecture and guardrails

F1 provides:

- explainable architecture selection;
- schema validation;
- undefined-variable rejection;
- section/architecture consistency checks;
- high-stakes safety/fallback requirements;
- state/claim evidence guardrails;
- `PORTABLE` semantics above `CERTIFIED`.

## F2 — Engineered candidates

F2 deterministically transforms a Task Brief into:

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

The current candidates remain human-readable and provenance-bound.

## F3 — Semantic/static critic

F3 checks semantic contradictions, vague output contracts, duplicate instructions, unsupported assumptions, provenance laundering, high-stakes boundaries and unjustified architecture.

Static success never promotes beyond `VALID`.

## F4 — Behavioral execution

F4 contains the adversarial behavioral matrix and observed execution machinery.

Current matrix: **30 blocking adversarial fixtures** across the three foundational prompt families. Coverage includes happy/minimal/missing/ambiguous/contradictory/noise/regression plus prompt injection, number/negation preservation, scope extrapolation, fabricated evidence and authority/currentness failure modes.

A prompt reaches `TESTED` only from a real execution receipt with:

- exact artifact/fixture fingerprints;
- identified runtime;
- durable raw evidence;
- all blocking assertions resolved;
- required human review resolved.

Synthetic harness passes never promote state.

## F5 — Baseline superiority

F5 runs the exact TESTED prompt against a task-equivalent baseline under the same fixture/runtime/evaluation contract.

The benchmark is paired and blind. A real F5 improvement receipt requires, among other gates:

- 100% engineered blocking pass;
- at least three benchmark repeats;
- zero engineered regressions;
- zero baseline A/B wins;
- no unresolved human checks;
- material engineered blind wins.

Only then may the artifact carry `improved` and advance to `CANDIDATE`.

## F6 — Target-runtime certification

Canonical spec: `specs/F6_TARGET_RUNTIME_CERTIFICATION.md`.

F6 no longer means cross-provider testing.

An exact F5 CANDIDATE becomes `CERTIFIED` only after at least **three independent real F5 IMPROVEMENT_PASS receipts on the same normalized provider + exact model + family**.

Every independent receipt must preserve the complete F5 gate and have distinct:

- receipt id;
- execution id;
- blind randomization reference;
- runtime identity-evidence reference.

Each F5 benchmark itself already contains multiple repeats, so F6 establishes repeatability at both sample and independent-experiment levels.

```text
CANDIDATE
   ↓ 3+ independent F5 passes, same target runtime
CERTIFIED
```

`CERTIFIED` is scoped evidence for that target runtime. It is not a universal correctness or portability claim.

## F7 — Portability

Canonical spec: `specs/F7_PORTABILITY.md`.

F7 is optional and begins only after F6 certification.

It combines the F6-bound F5 evidence with supplemental real F5 receipts from other environments. `PORTABLE` requires at least:

- 3 distinct providers;
- 3 distinct runtime families;
- exact prompt/baseline/fixture lineage;
- every receipt independently satisfying F5 superiority.

```text
CERTIFIED
   ↓ cross-provider/family reproduction
PORTABLE
```

A prompt may be permanently `CERTIFIED` without being `PORTABLE`.

## Evidence directories

```text
mk1/
├── specs/
│   ├── F6_TARGET_RUNTIME_CERTIFICATION.md
│   └── F7_PORTABILITY.md
├── fixtures/
├── briefs/
├── candidates/
│   ├── f2/       # VALID
│   ├── f3/       # static critic evidence
│   ├── f4/       # TESTED only from real F4 receipts
│   ├── f5/       # CANDIDATE/IMPROVED only from real F5 receipts
│   ├── f6/       # CERTIFIED only from repeated same-runtime F5 evidence
│   └── f7/       # PORTABLE only from optional cross-provider evidence
└── receipts/
    ├── f4/
    ├── f5/
    ├── f6/
    └── f7/
```

## What MK1 consumes from MK0

Preferred inputs include Golden Fixtures, technique vectors, architecture statistics, reviewed patterns such as RIRO, repository-authored templates, canonical taxonomy, source metadata and regression incidents.

Raw source bodies are not treated as a hidden template library.

## Product boundary

MK1 ends when Prompt Quarry can reliably build and certify reusable prompts for known tasks on declared target runtimes.

Cross-provider portability is an additional MK1 quality property. Automatic runtime task detection, retrieval, autonomous composition and adaptive selection remain MK2 responsibilities.
