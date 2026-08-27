PROMPT QUARRY — HUMAN READING COPY
========================================================================================
STAGE / DOCUMENT     : MK0
SOURCE REPOSITORY FILE: mk0/README.md
CONTENT ORIGIN       : REPOSITORY DOCUMENTATION / ARTIFACT

# MK0 — Knowledge Quarry

> **Question:** What exists, what did we actually observe, and what reusable knowledge can we extract from it?

MK0 is the evidence, characterization and knowledge-mining foundation of Prompt Quarry.

Everything built before the Prompt Forge belongs logically to MK0, even when the physical files remain in existing top-level directories. We intentionally do **not** move those files merely to make the tree look cleaner: provenance, Git history and stable paths matter more than cosmetic restructuring.

## MK0 mission

MK0 turns external observations into a durable, inspectable and reusable knowledge base without confusing source material with repository-authored artifacts.

```text
EXTERNAL SOURCES
      │
      ▼
raw evidence
      │
      ▼
normalized metadata
      │
      ├── indexes
      ├── structural analysis
      ├── technique vectors
      └── provenance
      │
      ▼
Golden Dataset / fixtures
      │
      ▼
repository-authored patterns, templates and reconstructions
      │
      ▼
human-readable TXT layer
```

## Physical paths that belong to MK0

MK0 is an architectural boundary, not a single folder.

| MK0 responsibility | Current repository path |
|---|---|
| Source registry | `catalog/sources.jsonl` |
| Canonical evidence catalog | `catalog/catalog.jsonl` |
| Taxonomy/schema | `catalog/schema.json`, `catalog/taxonomy.yaml` |
| Raw evidence | `quarry/raw/` |
| Normalized observations | `quarry/normalized/` |
| Source/category indexes | `quarry/indexes/` |
| Mining and aggregate analysis | `quarry/analysis/` |
| Golden/regression evidence | `quarry/fixtures/` |
| Reviewed promotion staging | `quarry/promotions/` |
| Source-family maps | `sources/` |
| Reusable knowledge derived during quarry work | `library/` |
| Human-reading materialization | `readable/` |
| Collectors/miners/builders | `tools/` |
| Evidence and architecture docs | `docs/` |
| Validation/harvest automation | `.github/workflows/` |

## MK0 contains source-observed and derived knowledge

Two things can coexist in MK0, but they must never be confused:

```text
SOURCE OBSERVATION
    ≠
REPOSITORY-AUTHORED DERIVATION
```

For example:

- a public Alpacka UUID/title/category is a source observation;
- a hash or technique vector is derived analysis;
- a Prompt Quarry reconstruction created from public metadata is repository-authored content;
- RIRO is a repository-authored pattern extracted from aggregate evidence.

Every layer must preserve that distinction explicitly.

## Current characterized Alpacka evidence

The current MK0 baseline includes:

- 530 public prompt references;
- 22 source-observed categories;
- 52 free records whose public detail endpoint returned content;
- 478 premium source records whose public detail endpoint returned `content: null`;
- 478/478 non-empty repository-authored usable reconstructions for those premium references;
- 12 public Skill references;
- 3 public generator preview references;
- 2 normalized public blog references;
- 18 observed prompt-construction techniques in the free-prompt mining pass;
- a Golden Dataset selected from the free-prompt evidence;
- a complete TXT human-reading layer without deleting raw/JSON evidence.

These counts are receipts for the current characterized source snapshot, not universal claims about everything that exists on the source platform.

## MK0 outputs that MK1 is allowed to consume

MK1 should preferentially consume stable knowledge products rather than raw scraped material:

1. `quarry/fixtures/` — deterministic evidence fixtures;
2. `quarry/analysis/` — technique and architecture signals;
3. `catalog/` — canonical identities, provenance and taxonomy;
4. `library/patterns/` — reviewed reusable construction patterns;
5. `library/templates/` — repository-authored reusable templates;
6. category/source indexes — retrieval/navigation context.

Raw observations remain available for audit and debugging but should not become an implicit prompt-generation dependency.

## MK0 quality rules

- Evidence before claims.
- `UNKNOWN != PASS`.
- Source body unavailable means unavailable; never infer it as observed.
- Provenance survives deduplication.
- Raw is not silently rewritten.
- Source text and repository-authored text remain distinguishable.
- Human-readable material is additive; it never replaces machine evidence.
- A failed validation gate must not silently promote an artifact.

## MK0 relationship to MK1

MK0 asks:

> **What exists and what have we learned from it?**

MK1 asks:

> **Can we engineer a better, testable artifact from that knowledge?**

MK0 does not need to stop evolving when MK1 begins. It becomes a versioned knowledge foundation. New source observations can continue to improve future MK1 prompt generations without changing the meaning of already-certified MK1 artifacts.

## Exit from quarry into forge

An observation is ready to influence MK1 when at least one of these is true:

- it is a reviewed Golden Fixture;
- it contributes to a characterized aggregate technique/pattern;
- it is a repository-authored MK0 pattern/template with explicit provenance;
- it has stable taxonomy and a clearly understood evidence state.

A source URL alone is not sufficient evidence that its wording or architecture should be copied into MK1.
