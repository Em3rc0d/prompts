# Prompt Quarry — Product Manifest v1

Status: `DRAFT_PRODUCT_CONTRACT`

This document defines the first commercial packaging boundary for Prompt Quarry. It does not change MK0/MK1 evidence states and it does not promote any prompt to TESTED, IMPROVED, CERTIFIED, or PORTABLE.

## 1. Product thesis

Prompt Quarry is not sold as a dump of collected prompts. The commercial product packages repository-authored prompt engineering knowledge into reusable developer-facing assets with explicit provenance, quality state, and evidence boundaries.

The first product line is:

```text
Prompt Quarry Developer Pack v1
```

Its job is to help a developer or technical builder turn an underspecified AI task into a structured prompt contract, apply Prompt Quarry architecture patterns, and evaluate the resulting prompt without pretending that static quality equals behavioral proof.

## 2. Product invariant

```text
Source evidence
    ↓
MK0 characterized knowledge
    ↓
MK1 engineered artifacts
    ↓
commercial packaging
```

Commercial packaging MUST NOT erase provenance or inflate maturity claims.

The canonical evidence ladder remains:

```text
DRAFT → VALID → TESTED → CANDIDATE/IMPROVED → CERTIFIED → PORTABLE
```

A commercial asset may be useful before certification, but its exact evidence state must remain visible.

## 3. Initial customer

Primary customer profile:

- developers building LLM-backed features;
- technical founders and indie builders;
- AI engineers who need reusable prompt architecture rather than generic prompt lists;
- teams that want explicit task intake, constraints, output contracts, quality gates, and uncertainty behavior.

Developer Pack v1 is not positioned as autonomous prompt optimization. Automatic routing/composition belongs to MK2 and remains outside this product version.

## 4. Product surfaces

### 4.1 Free Pack

Purpose: demonstrate the Prompt Quarry method and create a low-friction evaluation surface.

Expected contents:

- short methodology guide;
- architecture vocabulary;
- one or more repository-authored example templates;
- task-brief/intake example;
- static evaluation checklist;
- explicit maturity/evidence legend.

The Free Pack MUST NOT expose third-party premium source bodies or imply that repository-authored reconstructions are observed source wording.

### 4.2 Developer Pack v1

Purpose: first paid developer-facing package.

Canonical specification: `product/developer-pack-v1/SPEC.md`.

The pack centers on reusable contracts and workflow assets rather than a volume claim such as “thousands of prompts.”

### 4.3 Future packs

Possible later packages may target specific prompt families, domains, runtime adapters, or certified artifacts. They are not part of v1 unless separately specified and evidenced.

## 5. What can be claimed in v1

Allowed product-level claims must be supported by repository state. Examples:

- repository-authored;
- provenance-aware;
- architecture-driven;
- statically validated when a corresponding static receipt exists;
- designed around explicit task, constraints, output, quality, and fallback contracts;
- backed by Prompt Quarry's MK0 characterized knowledge.

Claims such as `TESTED`, `IMPROVED`, `CERTIFIED`, `PORTABLE`, “better than baseline,” or cross-provider reliability require their canonical MK1 receipts.

## 6. What cannot be sold as evidence

The following are not substitutes for real MK1 evidence:

- CI success alone;
- generated examples;
- synthetic harness output;
- precheck observations that do not satisfy the declared execution protocol;
- reconstructed third-party premium prompt wording;
- model/provider assumptions without runtime identity evidence.

## 7. Commercial artifact contract

Every distributed asset should expose enough metadata to answer:

1. What is this artifact for?
2. Who authored it?
3. What Prompt Quarry stage produced it?
4. What maturity/evidence state does it have?
5. Which version is being distributed?
6. What dependencies or assumptions does it have?
7. What claims are explicitly out of scope?

Recommended package metadata fields:

```text
product_id
product_version
artifact_id
artifact_version
artifact_type
prompt_family
authority
provenance_class
maturity_state
claims
evidence_refs
source_commit
license_or_usage_terms
```

## 8. Distribution boundary

The commercial package should contain only material intentionally approved for distribution.

Do not package by recursively exporting the private repository. In particular, internal source-harvest data, private research machinery, CI internals, raw evidence, credentials, and non-distributable third-party bodies stay outside the product bundle unless explicitly reviewed and approved.

## 9. Versioning

Developer Pack uses semantic product versions beginning at `1.0.0` when the release gate is satisfied.

Before that gate, repository packaging work may use `v1-draft` / `0.x` language.

A product release must bind to a source commit so that distributed contents are reproducible.

## 10. Release gate for Developer Pack v1

Minimum release gate:

- package specification complete;
- distributable inventory explicit;
- all included assets have authority/provenance classification;
- no forbidden source bodies included;
- maturity labels match MK1 evidence;
- examples render correctly;
- package README and quickstart complete;
- machine-readable manifest validates;
- source commit recorded;
- commercial claims reviewed against evidence.

Generator v0 may be included only after its canonical static CI receipt is green. A green static receipt still does not grant TESTED/IMPROVED/CERTIFIED claims.

## 11. Success criterion

Developer Pack v1 succeeds when a developer can take a real task and use the pack to produce a clearer, inspectable, repository-authored prompt workflow while understanding exactly what has and has not been empirically proven.

That distinction is part of the product, not legal fine print.
