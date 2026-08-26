# Prompt Quarry Architecture

## Goal

Build a durable research repository where every reusable AI artifact can be traced back to its source and studied independently of the platform where it was discovered.

## Pipeline

```text
External source
   |
   v
quarry/raw
   |  immutable observations: API responses, rendered-page candidates, source URLs
   v
quarry/normalized
   |  canonical text, fingerprints, candidate type/category, duplicate grouping
   v
review / validation
   |  evidence state + provenance + taxonomy checks
   v
catalog/catalog.jsonl
   |  canonical index
   v
library/
      prompts/
      skills/
      workflows/
      templates/
      patterns/
```

## Layers

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

Raw collection is evidence, not library content.

Allowed raw observations include:

- official API objects;
- rendered page candidates;
- source links;
- HTML snapshots produced by a local quarry run;
- manually supplied evidence.

Raw records are never silently rewritten.

### 3. Normalization

Normalization performs deterministic operations:

- Unicode/whitespace canonicalization;
- SHA-256 body fingerprinting;
- candidate type inference;
- candidate category/technique inference;
- exact deduplication;
- provenance merge.

Automatic classification is explicitly marked as a candidate and must not masquerade as verified human classification.

### 4. Canonical catalog

`catalog/catalog.jsonl` is the machine-readable truth index.

It stores both observed and derived fields, but evidence state makes the distinction visible. A record may legitimately have `body: null` when only a primary URL or secondary reference has been observed.

### 5. Library

The library is the curated reusable layer. Promotion requires:

1. artifact identity established;
2. source/provenance preserved;
3. classification reviewed;
4. duplicates reconciled;
5. body status understood;
6. catalog validation passing.

## Identity

Preferred identifiers:

- Threads: platform shortcode or media ID;
- website: canonical item URL/slug if available;
- otherwise: deterministic fingerprint-based local ID.

The identity rule prevents category changes from changing artifact IDs.

## Deduplication

Exact-body duplicates use canonical SHA-256. Deduplication never deletes provenance.

```text
same body + different URLs
    -> one canonical artifact
    -> multiple provenance entries
```

Near-duplicate semantic merging is intentionally not automatic in MK0.

## Failure semantics

- `401/403`: stop; do not bypass authentication/access control.
- `429`: stop or back off; do not evade rate limits.
- missing metadata: store `null`, not a guessed value.
- inaccessible body: preserve official URL and mark evidence state accordingly.
- dynamic website: use rendered-browser collector rather than pretending static HTML is complete.

## MK0 boundary

MK0 establishes the quarry, evidence contract, source registry, collectors, catalog seed, deduplication strategy and validation gate. It does not claim that the complete Alpacka corpus has already been retrieved.
