# Prompt Quarry

The quarry is the evidence and mining layer behind the reusable artifacts in `library/`.

Its purpose is to preserve provenance, extract reusable structure and prevent source observations from being confused with repository-authored prompts, skills or templates.

## Pipeline

```text
PUBLIC SOURCE
     │
     ▼
raw/
     │ capture evidence
     ▼
normalized/
     │ stable metadata contracts
     ▼
analysis/
     │ fingerprints, structure, technique vectors
     ▼
fixtures/
     │ deterministic regression evidence
     ▼
promotions/
     │ reviewed staged knowledge
     ▼
catalog/ + library/
```

## `raw/`

Source captures before semantic promotion.

Current Alpacka surface evidence includes the public root/directory plus `/prompts`, `/skills`, `/generador`, `/blog`, `/terms`, `/privacy` and `/pricing`.

Raw evidence may contain text that was publicly rendered at capture time. Raw is evidence, **not** automatically reusable library content.

## `normalized/`

Stable, machine-friendly records with source provenance and explicit access state.

### Public prompt directory

- **530** prompt UUID records
- **22** source-observed categories
- **52** free prompts whose public detail RPC returns content
- **478** premium records whose public detail RPC returns `content: null`
- **0** category mismatches between directory cards and detail RPC during the certified harvest

Key files:

- `alpacka-ai-public-prompt-directory.jsonl`
- `alpacka-ai-prompt-metadata.jsonl`
- `alpacka-ai-prompt-metadata-manifest.json`

Free prompt bodies are never written by the metadata harvester. They are processed in memory for fingerprints and structural features and then discarded.

### Public skills

- **12** normalized public skill references
- all 12 observed as free on the public surface
- normalized records retain concise metadata, hashes, variables and structural signals rather than duplicating source bodies

Key files:

- `alpacka-ai-skills-metadata.jsonl`
- `alpacka-ai-skills-metadata-manifest.json`

### Public generator previews

- **3** normalized preview references
- purposes currently classified as growth strategy planning, lead-magnet ideation and writing-style specification

Key files:

- `alpacka-ai-generator-previews.jsonl`
- `alpacka-ai-generator-previews-manifest.json`

## `analysis/`

Knowledge extracted from source evidence without promoting source wording.

### Free-prompt structure

`alpacka-ai-free-structure-report.json`

Base structure statistics for all 52 public free prompts.

### Technique vectors

- `alpacka-ai-free-technique-vectors.jsonl`
- `alpacka-ai-free-technique-matrix.json`

The current deep pass detects 18 observed techniques. High-frequency signals include:

- variable templates
- role assignment
- stepwise procedures
- task decomposition
- context injection
- tone definition
- output formatting
- explicit constraints

Technique detection is heuristic evidence, not a claim about author intent.

### Skill architecture

`alpacka-ai-skill-structure-report.json`

Across the 12 public skill references:

- role definition: 12/12
- intake/question behavior: 12/12
- explicit rules: 12/12
- explicit output contract: 9/12
- explicit multi-step process: 4/12

This aggregate observation led to the repository-authored **RIRO** pattern under `library/patterns/skill-design/`.

## `fixtures/`

Stable evidence used for characterization and regression testing.

### Golden free-prompt fixtures

- source pool: **52** public free prompts
- selected fixtures: **23**
- techniques covered: **18**
- source categories covered: **13**
- top architecture signatures covered: **10**

Files:

- `alpacka-free-golden-fixtures.json`
- `alpacka-free-golden-fixtures-manifest.json`
- see also `docs/GOLDEN_DATASET.md`

Fixtures store URLs, UUIDs, hashes and feature vectors — not prompt bodies.

### Contract probes

Sanitized network probes document how public dynamic surfaces load data while intentionally excluding credentials and long text bodies.

Examples:

- `alpacka-detail-network-probe.json`
- `alpacka-blog-dynamic-probe.json` when available

## `promotions/`

Staging area for knowledge that has been transformed into repository-owned artifacts and is ready for catalog validation.

Promotion manifests are appended to `catalog/catalog.jsonl` through an idempotent validation workflow. A failed schema gate must not modify the catalog.

## Access boundary

The quarry follows the source's public access boundary.

For Alpacka prompt details, the public RPC currently exposes metadata for both free and premium records. It returns prompt content for free records and `null` for premium records. The quarry records this distinction and does not attempt to authenticate, subscribe, bypass paywalls or recover premium bodies.

## Provenance rule

```text
SOURCE OBSERVATION ≠ LIBRARY ARTIFACT
```

Every promoted artifact must remain traceable to its evidence, while its body must be clearly repository-authored or otherwise legitimately reusable.
