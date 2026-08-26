# Golden Dataset

The Prompt Quarry golden dataset is a **reference-and-feature fixture set**, not a mirror of third-party prompt bodies.

## Purpose

Golden fixtures provide stable evidence for testing:

- source ingestion
- prompt classification
- technique detection
- variable extraction
- architecture-signature detection
- category routing
- provenance handling
- deduplication and regression checks

## Current fixture family

`quarry/fixtures/alpacka-free-golden-fixtures.json`

The source pool is the set of Alpacka prompts whose bodies are publicly returned by the site's public detail RPC. Prompt bodies are analyzed in memory and discarded. The fixture stores only:

- source prompt ID / UUID
- title
- category
- official URL
- SHA-256 fingerprint
- content length
- technique vector
- architecture signature
- structural numeric features
- selection reason

## Selection policy

The fixture set is the union of:

1. the strongest representative for every observed technique;
2. the strongest representative for every observed source category;
3. a representative for each of the ten most frequent architecture signatures.

“Strongest” is deterministic and ranks candidates by:

1. technique breadth;
2. number of variable markers;
3. numbered procedure steps;
4. content length as the final tie-break signal.

This does **not** mean the selected prompt is subjectively the best prompt. It means it is a high-information fixture for testing the quarry.

## Immutability rule

A fixture's `content_sha256` is the evidence anchor. If a public source changes and the fingerprint changes, do not silently replace history. Treat the new observation as a new evidence state and record the transition.

## Provenance boundary

Golden fixtures are source references. Repository-authored patterns, skills and templates live under `library/` and must remain distinguishable from source observations.

Premium content is never part of the golden body corpus because the public RPC returns `content: null` for premium records. No authentication or paid-access boundary is bypassed.
