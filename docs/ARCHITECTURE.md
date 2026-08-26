# Prompt Quarry Architecture

## Goal

Build a durable prompt-engineering system where source observations remain auditable, reusable knowledge is clearly derived, engineered prompts are testable, and automation never outruns evidence.

Prompt Quarry is divided into three explicit maturity stages:

```text
MK0 — Knowledge Quarry
What exists?
        ↓
MK1 — Prompt Forge
Can we build better prompts from it?
        ↓
MK2 — Prompt Engine
Can the system select, compose, test and improve prompts automatically?
```

These are capability boundaries, not folder-only boundaries.

---

# MK0 — Knowledge Quarry

MK0 owns evidence collection, normalization, characterization, source provenance, reusable-pattern extraction, Golden Fixtures and human readability.

## MK0 evidence pipeline

```text
External source
   |
   v
quarry/raw
   |  immutable observations: API responses, rendered-page candidates, source URLs
   v
quarry/normalized
   |  stable metadata, fingerprints, candidate type/category, access state
   v
quarry/indexes + quarry/analysis
   |  navigation, aggregate structure, technique vectors
   v
quarry/fixtures
   |  deterministic Golden/regression evidence
   +----------------------+----------------------+
   |                                             |
   v                                             v
quarry/promotions                        repository-authored derivation
   |                                             |
   v                                             v
catalog/catalog.jsonl                    library/patterns/templates/prompts
   |                                             |
   +----------------------+----------------------+
                          |
                          v
                    readable/*.txt
```

## MK0 layers

### 1. Source registry

`catalog/sources.jsonl` identifies source families independently of individual artifacts.

A source answers:

- who publishes it;
- which platform hosts it;
- canonical and discovery URLs;
- language;
- access method;
- known collection constraints.

### 2. Raw quarry

Raw collection is evidence, not automatically reusable library content.

Allowed raw observations include:

- official/public API objects;
- rendered-page candidates;
- source links;
- HTML/browser snapshots produced by a quarry run;
- manually supplied evidence.

Raw records are never silently rewritten.

### 3. Normalization

Normalization performs deterministic operations such as:

- Unicode/whitespace canonicalization;
- SHA-256 fingerprinting;
- candidate type/category/technique inference;
- exact deduplication;
- provenance merge;
- explicit access/content state.

Automatic classification is evidence about the classifier result, not proof of author intent.

### 4. Canonical catalog

`catalog/catalog.jsonl` is the canonical machine-readable index for reviewed source/derived artifacts.

A record may legitimately have `body: null` when the body was not observed. Missing source content is not silently filled with guessed source wording.

### 5. Library

`library/` contains reusable repository artifacts and derived datasets.

Promotion requires:

1. artifact identity established;
2. source/provenance preserved;
3. classification understood;
4. duplicates reconciled where possible;
5. source-vs-derived body status explicit;
6. validation passing.

### 6. Human reading layer

`readable/` is an additive materialization for people.

It exists so the repository can be read without opening JSON/JSONL while preserving links to machine evidence and provenance.

It never replaces `raw`, `normalized`, `catalog` or `library`.

## MK0 identity

Preferred identifiers:

- Threads: platform shortcode/media ID;
- website: canonical item URL/slug/UUID;
- otherwise: deterministic fingerprint-based local ID.

Identity must not depend on classification labels that can change later.

## MK0 deduplication

Exact-body duplicates use canonical SHA-256. Deduplication never deletes provenance.

```text
same body + different URLs
    -> one canonical analytical identity when appropriate
    -> multiple preserved provenance observations
```

Near-duplicate semantic merging requires characterization and is not treated as exact deduplication.

## MK0 failure semantics

- `401/403`: stop; do not bypass authentication/access control.
- `429`: stop/back off; do not evade rate limits.
- missing metadata: preserve unknown/null rather than guessing.
- inaccessible source body: preserve source URL and evidence state.
- dynamic website: use rendered/browser/network characterization rather than claiming static HTML is complete.
- validation failure: do not disable the gate to force promotion.

## MK0 output boundary

MK0 supplies MK1 with characterized knowledge products:

- Golden/regression fixtures;
- technique vectors;
- taxonomy;
- reviewed patterns/templates;
- source metadata and provenance;
- failure characterization.

MK1 should not use raw scraping output as an implicit prompt template library.

---

# MK1 — Prompt Forge

MK1 owns prompt engineering, behavioral testing and certification.

## MK1 pipeline

```text
Task / product brief
       |
       v
Intent + domain + risk classification
       |
       v
Retrieve MK0 patterns / evidence / fixtures
       |
       v
Architecture selection
       |
       v
Candidate assembly
       |
       v
Static contract + critic gate
       |
       v
Fixture execution
       |
       v
Baseline comparison
       |
       v
Quality rubric
   +---+---+
   |       |
 reject  certify
           |
           v
   MK1 certified artifact + receipt
```

## MK1 canonical construction model

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

This is a selection vocabulary, not a requirement to include every section in every prompt.

Architecture is successful when it improves task reliability with minimum useful complexity.

## MK1 evidence semantics

Use these terms precisely:

- `DRAFT`: authored but unvalidated;
- `VALID`: passes static contract checks;
- `TESTED`: executed against a named fixture set;
- `CANDIDATE`: complete evaluation receipt available;
- `CERTIFIED`: passes certification gate;
- `REJECTED`: blocking failure / insufficient score;
- `DEPRECATED`: superseded or invalidated certified artifact.

`GENERATED` is not a quality state.

`IMPROVED` is a comparative claim and requires a fair baseline receipt.

## MK1 canonical documents

- `mk1/README.md`
- `mk1/specs/PROMPT_CONTRACT.md`
- `mk1/rubrics/PROMPT_QUALITY_RUBRIC.md`
- `mk1/fixtures/README.md`

---

# MK2 — Prompt Engine

MK2 owns automatic prompt selection/composition/evaluation decisions at runtime.

## MK2 conceptual pipeline

```text
Task
 |
 v
Router: intent / domain / risk
 |
 +--> retrieve MK1 certified artifact -----+
 |                                         |
 +--> no strong match -> compose candidate |
                         |                 |
                         v                 |
                    MK1 Forge gate         |
                         |                 |
                         +---------> candidate pool
                                      |
                                      v
                             evaluator / selector
                                      |
                                      v
                                  execution
                                      |
                                      v
                             receipt / feedback
```

MK2 cannot call itself an engine merely because it selects a prompt by keyword or asks a model to rewrite one.

Required capabilities include:

- task/risk classification;
- version-aware retrieval;
- architecture composition;
- evaluation planning;
- comparable candidate selection;
- runtime/model adaptation;
- durable receipts;
- feedback-to-regression loop.

## Feedback architecture

Meaningful MK2 runtime failures must flow backward into evidence rather than becoming endless ad-hoc patches:

```text
runtime failure
      ↓
characterize evidence
      ↓
MK0 fixture / knowledge update
      ↓
MK1 candidate revision
      ↓
MK1 certification
      ↓
MK2 selection/runtime update
```

## MK2 entry gate

Core MK2 implementation should wait until MK1 demonstrates:

- stable prompt artifact contracts;
- versioned fixture sets;
- reproducible certification receipts;
- multiple certified prompt families;
- fair baseline comparisons;
- version/deprecation semantics.

Until those receipts exist, MK2 remains architectural intent.

---

# Repository-wide invariants

1. **Evidence before claims.**
2. **UNKNOWN != PASS.**
3. **Observed != derived != engineered != tested != certified != improved.**
4. **Human-readable views never replace machine evidence.**
5. **Provenance survives transformation.**
6. **Meaningful failures become fixtures/regressions.**
7. **No access-control bypass.**
8. **A green CI gate proves only what that gate actually checks.**

See `docs/ROADMAP.md` for phase sequencing and exit gates.
