# MK0 — Knowledge Quarry

> **Question:** What exists, what did we actually observe, and what reusable knowledge can we extract from it?

MK0 is the physical evidence and knowledge foundation of Prompt Quarry. It owns the source-derived material, normalized observations, indexes, analysis, Golden Dataset, reviewed reusable knowledge, source maps and human-readable projections that MK1 consumes.

MK0 is **not** a prompt-generation stage. New Prompt Quarry prompts and skills are engineered in MK1.

## Physical architecture

```text
mk0/
├── raw/                # source observations / harvest evidence
├── normalized/         # normalized machine-readable observations
├── catalog/            # identities, taxonomy, source registry, provenance
├── indexes/            # navigation and retrieval indexes
├── analysis/           # aggregate mining, technique vectors, architecture signals
├── golden-dataset/     # reviewed deterministic fixtures / regression evidence
├── promotions/         # reviewed promotion staging
├── library/            # repository-authored reusable knowledge, patterns, templates
├── sources/            # source-family maps and source-specific knowledge
├── readable/           # additive human-readable materialization
├── MANIFEST.json       # machine-readable MK0 contract
└── README.md
```

Shared execution infrastructure remains at repository root:

```text
tools/               collectors, miners, builders, validators
docs/                cross-stage architecture and program documentation
.github/workflows/    CI / harvest / validation automation
```

Those directories may operate on MK0, MK1 and MK2; they are not part of MK0's canonical data boundary.

## Knowledge flow

```text
EXTERNAL SOURCES
      │
      ▼
mk0/raw
      │
      ▼
mk0/normalized
      │
      ├── mk0/catalog
      ├── mk0/indexes
      ├── mk0/analysis
      └── provenance
      │
      ▼
mk0/golden-dataset
      │
      ▼
mk0/library + mk0/sources
      │
      ▼
mk0/readable
      │
      ▼
MK1 — Prompt / Skill Forge
```

## Truth boundaries

```text
SOURCE OBSERVATION
    ≠
REPOSITORY-AUTHORED DERIVATION
    ≠
MK1 ENGINEERED ARTIFACT
```

Examples:

- an observed public UUID/title/category is source evidence;
- an extracted technique vector is MK0 analysis;
- a reconstruction authored from public metadata is MK0 derived knowledge, not observed source wording;
- RIRO is reviewed reusable MK0 knowledge;
- a new Prompt Quarry prompt or skill built from those signals belongs to MK1.

## Current characterized baseline

The current MK0 snapshot records:

- 530 public prompt references;
- 22 source-observed categories;
- 52 free records whose public detail endpoint returned prompt content;
- 478 premium source records whose public detail endpoint returned `content: null`;
- 478/478 non-empty repository-authored reconstructions for those premium references;
- 12 public Skill references;
- 3 public generator-preview references;
- 2 normalized public blog references;
- 18 observed prompt-construction techniques in the free-prompt mining pass;
- a reviewed Golden Dataset;
- an additive TXT/human-reading layer.

These are receipts for the characterized snapshot, not universal claims about everything available on the source platform.

## Canonical MK0 paths

| Responsibility | Canonical path |
|---|---|
| Raw evidence | `mk0/raw/` |
| Normalized observations | `mk0/normalized/` |
| Source registry / canonical catalog | `mk0/catalog/` |
| Source and category indexes | `mk0/indexes/` |
| Mining / aggregate analysis | `mk0/analysis/` |
| Golden Dataset / regression evidence | `mk0/golden-dataset/` |
| Reviewed promotion staging | `mk0/promotions/` |
| Reusable patterns/templates/derived knowledge | `mk0/library/` |
| Source-family maps | `mk0/sources/` |
| Human-readable projection | `mk0/readable/` |

## What MK1 may consume

MK1 should consume stable MK0 knowledge products, not silently depend on arbitrary raw source bodies. Preferred inputs are:

1. `mk0/golden-dataset/` — deterministic reviewed evidence;
2. `mk0/analysis/` — technique and architecture signals;
3. `mk0/catalog/` — canonical identities, taxonomy and provenance;
4. `mk0/library/` — reviewed reusable construction knowledge;
5. `mk0/indexes/` and `mk0/sources/` — retrieval/navigation context.

`mk0/raw/` remains available for audit, reproducibility and debugging.

## MK0 quality rules

- Evidence before claims.
- `UNKNOWN != PASS`.
- Source body unavailable means unavailable; never infer it as observed.
- Provenance survives deduplication.
- Raw evidence is not silently rewritten.
- Source text and repository-authored text remain distinguishable.
- Human-readable material is additive; it never replaces machine evidence.
- A failed validation gate must not silently promote an artifact.

## Boundary with MK1

MK0 asks:

> **What exists and what have we learned from it?**

MK1 asks:

> **Can we engineer, test and certify better prompts and skills from that knowledge?**

MK0 can keep evolving as a versioned quarry while already-built MK1 artifacts preserve their own lineage and fingerprints.
