# Prompt Quarry

Private research repository for collecting, classifying, characterizing and reusing AI prompts, skills and prompt-engineering patterns with explicit provenance.

## Principles

1. **Source first.** Every source observation keeps an original/official URL whenever available.
2. **Raw != normalized != derived.** Evidence, cleaned metadata, analysis and repository-authored artifacts live in different layers.
3. **Provenance survives deduplication.** Duplicate or related observations may converge analytically, but source history remains traceable.
4. **Prompt != skill != workflow.** Artifact type is explicit.
5. **Evidence before claims.** Unknown metadata stays unknown; runtime observations are not generalized beyond their receipts.
6. **No access-control bypass.** Collectors stop at authentication, CAPTCHA, paywalls or changed authorization boundaries.
7. **Minimize third-party body duplication.** Prefer URLs, metadata, fingerprints, structural features and repository-authored abstractions.
8. **Promotion is gated.** `library/` artifacts enter the canonical catalog only after schema validation.

## Evidence pipeline

```text
SOURCE
  ↓
quarry/raw/
  ↓
quarry/normalized/
  ↓
quarry/indexes/ + quarry/analysis/
  ↓
quarry/fixtures/
  ↓
quarry/promotions/
  ↓
catalog/ + library/
```

See `quarry/README.md` for the complete evidence contract.

## Repository map

```text
prompts/
├── catalog/
│   ├── catalog.jsonl
│   ├── sources.jsonl
│   ├── schema.json
│   └── taxonomy.yaml
├── library/
│   ├── prompts/
│   ├── skills/
│   ├── workflows/
│   ├── templates/
│   └── patterns/
├── quarry/
│   ├── raw/
│   ├── normalized/
│   ├── indexes/
│   ├── analysis/
│   ├── fixtures/
│   └── promotions/
├── sources/
│   └── alpacka-ai/
├── tools/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CLASSIFICATION.md
│   ├── PROVENANCE.md
│   └── GOLDEN_DATASET.md
└── .github/workflows/
```

## Canonical catalog record

Each catalog entry is designed to answer:

- What is the artifact type?
- What is it useful for?
- Where did it come from?
- Which source URL was observed?
- Was a body observed, summarized, fingerprinted or only indexed?
- Which models/tools does it target?
- Which prompt-engineering techniques does it use?
- What is source-observed versus repository-authored?

The schema is defined in `catalog/schema.json`.

## First characterized source family: Alpacka AI

Tracked public surfaces include:

- Threads: `https://www.threads.com/@alpacka.ai`
- Website: `https://www.alpackaai.xyz`
- Public prompt directory and detail routes
- Public Skills surface
- Public generator previews
- Blog/index surfaces

Alpacka is treated as a **source family**, never as the repository taxonomy.

### Prompt directory — certified harvest

- **530** public prompt UUID references
- **22** source-observed categories
- **52** free records whose public detail RPC returned content
- **478** premium records whose public detail RPC returned `content: null`
- **0** category mismatches between public directory cards and the detail RPC in the certified harvest

Prompt bodies are not persisted by the RPC harvester. Free bodies are processed in memory for hashes, variables and structural/technique features and then discarded.

Navigation: `library/prompts/alpacka/README.md`.

### Technique mining

Across the 52 public free prompt bodies, the current heuristic mining pass detected **18 reusable construction techniques**. High-frequency observations include variable templates, role assignment, stepwise procedure, task decomposition, context injection and tone definition.

Files:

- `quarry/analysis/alpacka-ai-free-technique-vectors.jsonl`
- `quarry/analysis/alpacka-ai-free-technique-matrix.json`

### Skills

**12** public skill references are normalized separately from prompts.

Aggregate observations:

- role definition: 12/12
- intake/question behavior: 12/12
- explicit rules: 12/12
- output contract: 9/12
- explicit process: 4/12

This evidence contributed to the repository-authored **RIRO — Role–Intake–Rules–Output** pattern.

### Generator previews

**3** public preview references are normalized as source evidence for:

- growth strategy planning
- lead-magnet ideation
- writing-style specification

Their source bodies remain in the raw evidence layer only; normalized records use fingerprints/features.

## Golden Dataset

The current free-prompt golden set contains **23 reference fixtures** selected deterministically from the 52-public-prompt source pool.

Coverage:

- **18** observed techniques
- **13** source categories represented in the free corpus
- **10** frequent architecture signatures

Fixtures contain source references, hashes and feature vectors rather than prompt bodies.

See `docs/GOLDEN_DATASET.md`.

## Repository-authored promoted artifacts

Current examples include:

- `library/patterns/skill-design/role-intake-rules-output.md`
- `library/templates/business/growth-90-day-system.md`
- `library/templates/content/lead-magnet-design-system.md`
- `library/templates/content/style-profile-extractor.md`
- `library/patterns/content/humanization-stack.md`

These artifacts remain traceable to their inspiration/evidence families while their bodies are explicitly repository-authored.

## Artifact types

| Type | Meaning |
|---|---|
| `prompt` | Direct instruction intended for an AI model |
| `skill` | Reusable capability containing instructions, context and/or procedures |
| `workflow` | Ordered multi-step process, potentially combining prompts/tools |
| `template` | Parameterized shell intended to be filled with variables |
| `pattern` | Generalized prompt-engineering technique extracted from observations |
| `guide` | Educational/explanatory material |
| `reference` | Useful source evidence that is not itself a prompt |

## Current status

**MK0 — source characterization and reusable-pattern extraction**

Completed evidence gates:

- public Alpacka prompt directory mapped
- 530/530 detail metadata harvested
- free/premium access boundary characterized
- category indexes generated
- free-prompt structural mining generated
- deep technique vectors generated
- public skills normalized and structurally characterized
- public generator previews normalized
- Golden Dataset fixture selection operational
- catalog promotion workflow is schema-gated and idempotent

Still open before treating the quarry as broadly mature:

- expand primary Threads ingestion when official access is configured
- add more independent source families
- improve technique detector characterization against hand-reviewed fixtures
- add deduplication/semantic-near-duplicate benchmarks
- continue source-driven promotion into original reusable library artifacts
