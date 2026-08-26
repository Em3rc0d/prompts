# Prompt Quarry

Private research and engineering repository for collecting, characterizing and transforming prompt/skill knowledge into tested reusable AI artifacts with explicit provenance.

## Product stages

Prompt Quarry has three explicit maturity layers:

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
"Can the system automatically select,
 compose, test and improve prompts
 for a specific task?"
```

- **MK0** owns evidence, source characterization, normalized metadata, technique mining, Golden Dataset, derived knowledge and the human-reading layer.
- **MK1** engineers Prompt Quarry candidates and only calls them `CERTIFIED` after behavioral fixtures, rubric evaluation and durable receipts.
- **MK2** is the future orchestration engine for automatic retrieval/composition/evaluation after MK1 is mature.

Stage entry points:

- `mk0/README.md`
- `mk1/README.md`
- `mk2/README.md`
- `docs/ROADMAP.md`

## Principles

1. **Source first.** Every source observation keeps an original/official URL whenever available.
2. **Raw != normalized != derived != engineered.** Evidence, metadata, analysis and repository-authored artifacts remain semantically distinct.
3. **Provenance survives transformation and deduplication.**
4. **Prompt != skill != workflow.** Artifact type is explicit.
5. **Evidence before claims.** Unknown != pass; generated != valid; valid != tested; tested != certified; engineered != improved without a baseline receipt.
6. **No access-control bypass.** Collectors stop at authentication, CAPTCHA, paywalls or changed authorization boundaries.
7. **Minimize third-party body duplication.** Prefer URLs, metadata, fingerprints, structural features and repository-authored abstractions.
8. **Promotion/certification is gated.** A failed gate must not be bypassed to make an artifact look ready.
9. **Human readability is a product requirement.** JSON/JSONL remains machine evidence; `readable/` provides additive TXT views for people.
10. **Meaningful failures become fixtures.** Do not accumulate ad-hoc patches without regression evidence.

## Architecture

```text
EXTERNAL SOURCES
      │
      ▼
┌─────────────────────────────────────────┐
│ MK0 — KNOWLEDGE QUARRY                  │
│                                         │
│ raw → normalized → indexes/analysis     │
│              → fixtures / Golden Data   │
│              → patterns/templates       │
│              → readable TXT             │
└──────────────────┬──────────────────────┘
                   │ characterized knowledge
                   ▼
┌─────────────────────────────────────────┐
│ MK1 — PROMPT FORGE                      │
│                                         │
│ brief → architecture → candidate        │
│       → critic → fixtures               │
│       → baseline → rubric → receipt     │
│       → CERTIFIED / REJECTED            │
└──────────────────┬──────────────────────┘
                   │ certified artifacts
                   ▼
┌─────────────────────────────────────────┐
│ MK2 — PROMPT ENGINE                     │
│                                         │
│ route → retrieve/compose → evaluate     │
│       → select → execute → feedback     │
└─────────────────────────────────────────┘
```

See `docs/ARCHITECTURE.md` and `docs/ROADMAP.md`.

## Repository map

```text
prompts/
├── mk0/
│   └── README.md
├── mk1/
│   ├── README.md
│   ├── specs/
│   ├── rubrics/
│   ├── fixtures/
│   ├── briefs/
│   └── candidates/
├── mk2/
│   └── README.md
├── catalog/
├── library/
├── quarry/
│   ├── raw/
│   ├── normalized/
│   ├── indexes/
│   ├── analysis/
│   ├── fixtures/
│   └── promotions/
├── readable/
├── sources/
├── tools/
├── docs/
└── .github/workflows/
```

## MK0 — current characterized foundation

All current source mining and knowledge characterization belongs to MK0.

### Alpacka receipts

- **530** public prompt UUID references;
- **22** source-observed categories;
- **52** free records whose public detail RPC returned content;
- **478** premium source records whose public detail RPC returned `content: null`;
- **0** category mismatches in the certified detail harvest;
- **478/478** non-empty repository-authored reconstructions for those premium references;
- **12** public Skill references;
- **3** generator-preview references;
- **2** normalized blog references;
- **18** prompt-construction techniques observed in the current free-corpus mining pass;
- Golden Dataset and human TXT materialization operational.

The premium source `null` remains evidence about source access; it is never relabeled as observed source wording. Repository-authored reconstructions remain explicitly `derived`.

Key paths:

- `quarry/normalized/alpacka-ai-prompt-metadata.jsonl`
- `quarry/analysis/`
- `quarry/fixtures/`
- `library/prompts/alpacka/derived-premium/`
- `readable/`

## MK1 — Prompt Forge status

### F0 — Contracts: COMPLETE

The Forge has explicit Task Brief, Prompt Artifact, fixture and quality/certification contracts.

Key files:

- `mk1/specs/PROMPT_CONTRACT.md`
- `mk1/specs/TASK_BRIEF.schema.json`
- `mk1/specs/PROMPT_ARTIFACT.schema.json`
- `mk1/rubrics/PROMPT_QUALITY_RUBRIC.md`
- `mk1/fixtures/README.md`

### F1 — Architecture selector + static guardrails: COMPLETE / CI PASS

Implemented:

- explainable architecture selector;
- static linter;
- 5 selector characterization fixtures;
- 6 linter regression cases;
- dedicated CI gate.

The selector deliberately keeps simple tasks compact and gives reliability/safety blocks to complex or high-stakes tasks.

### F2 — Candidate assembler: COMPLETE / 3 VALID CANDIDATES

The Forge now performs:

```text
Task Brief
   ↓
architecture selection
   ↓
deterministic prompt assembly
   ↓
static lint
   ↓
VALID candidate bundle
```

First persisted candidate bundles:

- `mk1/candidates/f2/content_clear_rewrite/`
- `mk1/candidates/f2/software_code_review/`
- `mk1/candidates/f2/research_technical_decision/`

Each bundle contains:

```text
artifact.json
architecture.json
lint.json
prompt.txt
```

All three are `VALID`, `lint=PASS`, `0 warnings`, and claim only `engineered`.

**They are deliberately NOT labeled TESTED, CERTIFIED or IMPROVED yet.** Those labels require F4–F6 evidence.

### F3 — Critic: NEXT

Next work deepens static quality analysis beyond the current linter:

- contradiction detection;
- vague-output detection;
- instruction redundancy;
- unsupported-assumption checks;
- provenance/truth-boundary checks;
- high-stakes critic reports;
- permanent regression fixtures.

Canonical construction vocabulary remains:

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

Not every task needs every block. Section count is not a quality metric.

## MK2 — Prompt Engine status

**Architecture only — not implemented.**

MK2 waits for MK1 behavioral fixtures, baseline comparisons, repeatable certification, multiple certified prompt families and version/deprecation semantics.

## Current program status

```text
MK0: ACTIVE / USABLE FOUNDATION
MK1: F0 COMPLETE
     F1 COMPLETE / CI PASS
     F2 COMPLETE / 3 VALID ENGINEERED CANDIDATES
     F3 NEXT
MK2: ARCHITECTURE ONLY / DEFERRED
```

No MK1 prompt is currently claimed as `CERTIFIED` or empirically `IMPROVED`.
