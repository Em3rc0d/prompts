PROMPT QUARRY — HUMAN READING COPY
========================================================================================
SOURCE REPOSITORY FILE: /home/runner/work/prompts/prompts/library/prompts/alpacka/derived-premium/README.md
CONTENT ORIGIN       : REPOSITORY FILE (human-readable copy)
# Derived premium prompt library

This directory makes the **478 premium Alpacka prompt references usable without pretending to possess their private/premium source bodies**.

## Contract

For each public premium reference:

```text
public UUID + title + category
          │
          ├── source body: NOT PUBLIC
          │
          ▼
repository-mined architecture patterns
          │
          ▼
REPOSITORY-AUTHORED RECONSTRUCTION
```

Every record in `catalog.jsonl` has a non-empty `content` field.

That content is **not** a reproduction, recovery or claim about the original Alpacka premium body. It is a Prompt Quarry artifact generated from public metadata plus construction patterns observed in the public/free corpus and public Skills corpus.

## Files

- `catalog.jsonl` — all derived premium prompts.
- `manifest.json` — coverage and generation receipt.
- `categories/*.jsonl` — the same derived records partitioned by source category.

## Required provenance fields

Each record includes:

- `source_prompt_id`
- `source_uuid`
- `source_url`
- `source_title`
- `source_category`
- `source_access: premium`
- `source_body_status: not-public`
- `content_origin: repository-authored-reconstruction`
- `fidelity: metadata-derived-not-source-reproduction`
- `content`
- `content_sha256`

## Reconstruction architecture

The builder uses a RIRO-like structure:

```text
ROLE
  ↓
OBJECTIVE
  ↓
INTAKE VARIABLES
  ↓
PROCESS
  ↓
RULES / CONSTRAINTS
  ↓
OUTPUT CONTRACT
  ↓
SELF-CHECK
```

It also detects intent signals in public titles such as plan, checklist, simulator, audit, generator, writing, optimization and learning to select a more appropriate procedure.

## Evidence boundary

The source API currently returns `content: null` for premium detail bodies. Prompt Quarry records that source fact honestly while providing a separate, non-null reusable artifact layer.
