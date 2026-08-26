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
  ├── quarry/promotions/ → catalog + reviewed library artifacts
  └── repository-authored derivation → reusable library datasets
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
│   │   └── alpacka/derived-premium/   # 478 usable reconstructions
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

## First characterized source family: Alpacka AI

Tracked public surfaces include Threads, the website, public prompt directory/detail routes, Skills, generator previews and blog/index surfaces.

Alpacka is treated as a **source family**, never as the repository taxonomy.

### Prompt directory — certified harvest

- **530** public prompt UUID references
- **22** source-observed categories
- **52** free records whose public detail RPC returned content
- **478** premium source records whose public detail RPC returned `content: null`
- **0** category mismatches between public directory cards and the detail RPC in the certified harvest

The `null` value above is a source-access observation. It no longer means our reusable library is empty for those records.

### Premium reusable reconstruction layer

Prompt Quarry now contains **478/478 non-empty repository-authored reconstructions** for the premium references, with **0 empty `content` records**.

Files:

- `library/prompts/alpacka/derived-premium/catalog.jsonl`
- `library/prompts/alpacka/derived-premium/manifest.json`
- `library/prompts/alpacka/derived-premium/categories/*.jsonl`

Each record explicitly states:

- `source_body_status: not-public`
- `content_origin: repository-authored-reconstruction`
- `fidelity: metadata-derived-not-source-reproduction`

This preserves the evidence boundary while keeping the dataset useful.

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

**3** public preview references are normalized as source evidence for growth strategy planning, lead-magnet ideation and writing-style specification.

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

## Current status

**MK0 — source characterization and reusable-pattern extraction**

Completed evidence gates now include:

- public Alpacka prompt directory mapped
- 530/530 detail metadata harvested
- free/premium access boundary characterized
- category indexes generated
- free-prompt structural and technique mining generated
- public skills normalized and structurally characterized
- public generator previews normalized
- Golden Dataset fixture selection operational
- **478/478 premium references converted into non-null repository-authored reusable prompts**
- catalog promotion workflow schema-gated and idempotent

Still open before treating the quarry as broadly mature:

- expand primary Threads ingestion when official access is configured
- add more independent source families
- improve technique detector characterization against hand-reviewed fixtures
- add deduplication/semantic-near-duplicate benchmarks
- continue source-driven promotion into original reusable library artifacts
