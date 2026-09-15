PROMPT QUARRY — HUMAN READING COPY
========================================================================================
STAGE / DOCUMENT     : MK1
SOURCE REPOSITORY FILE: mk1/candidates/README.md
CONTENT ORIGIN       : REPOSITORY DOCUMENTATION / ARTIFACT

# MK1 Candidates

This directory stores **engineered candidate bundles**, not certified prompts.

Each generated candidate bundle should contain:

```text
<task-id>/
├── artifact.json       # canonical MK1 prompt artifact
├── architecture.json   # selector output + reasons
├── lint.json           # static validation receipt
└── prompt.txt          # human-readable prompt + status/provenance
```

Candidate state meanings:

- `DRAFT`: assembled but static lint has not passed;
- `VALID`: contract/schema/static lint passed;
- `TESTED`: behavior fixtures executed;
- `CANDIDATE`: complete evaluation receipt exists and is ready for certification decision.

A file under `mk1/candidates/` must **not** be interpreted as certified merely because it is committed to `main`.

Canonical certification outputs will eventually live under `mk1/certified/` together with durable receipts.

## Current F2 rule

The initial assembler may persist only candidates with:

```text
state = VALID
claims = [engineered]
lint.status = PASS
receipt_id = null
```

This intentionally prevents F2 from laundering static validity into runtime quality claims.
