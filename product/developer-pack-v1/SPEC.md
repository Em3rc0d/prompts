# Prompt Quarry Developer Pack v1 — Specification

Status: `DRAFT_PRODUCT_SPEC`
Product ID: `pq-developer-pack`
Target release: `1.0.0`

## 1. Promise

Developer Pack v1 provides a compact, inspectable system for designing better-structured prompts for software and technical AI workflows using Prompt Quarry's repository-authored architecture and evaluation contracts.

It is a toolkit, not a magic-prompt collection and not an autonomous MK2 engine.

## 2. User outcome

A user should be able to move through:

```text
raw task
  ↓
task brief / intake
  ↓
architecture choice
  ↓
prompt construction
  ↓
static review
  ↓
execution/evaluation guidance
```

without needing access to the private Prompt Quarry research repository.

## 3. v1 scope

### Included capability families

1. Task intake and normalization.
2. Prompt architecture selection guidance.
3. Prompt construction templates.
4. Software/code-review oriented example workflow.
5. Technical research/decision oriented example workflow.
6. Static quality and failure-mode checklist.
7. Evidence-state and provenance guidance.
8. Optional Generator v0 surface after canonical static CI PASS.

### Explicitly out of scope

- autonomous runtime routing;
- autonomous retrieval/composition from the full private quarry;
- automatic self-improvement;
- universal provider portability;
- claims of empirical superiority without F5 receipts;
- certification without F6 evidence;
- redistribution of third-party premium prompt bodies.

## 4. Canonical architecture vocabulary

The pack teaches the smallest purposeful subset of:

```text
PURPOSE
ROLE
CONTEXT
INTAKE
ASSUMPTIONS
PROCESS
RULES / CONSTRAINTS
OUTPUT CONTRACT
QUALITY GATE
FALLBACK / UNCERTAINTY BEHAVIOR
```

Section count is not a quality metric.

## 5. Proposed distributable structure

```text
prompt-quarry-developer-pack-v1/
├── README.md
├── QUICKSTART.md
├── MANIFEST.json
├── methodology/
│   ├── architecture.md
│   ├── evidence-states.md
│   └── evaluation.md
├── contracts/
│   ├── task-brief.example.json
│   └── prompt-request.example.json
├── templates/
│   ├── general-structured-prompt.md
│   ├── software-code-review.md
│   └── technical-research-decision.md
├── examples/
│   ├── software-code-review/
│   └── technical-research-decision/
└── checklists/
    ├── static-quality.md
    └── release-readiness.md
```

This is a commercial distribution layout, not a mirror of internal repository paths.

## 6. Asset classes

Each packaged asset MUST be classified as one of:

- `product-authored`: created specifically for the commercial package;
- `mk1-derived`: distributable adaptation of a Prompt Quarry engineered artifact;
- `mk0-derived`: repository-authored abstraction informed by characterized knowledge;
- `example`: demonstration data/output with no elevated evidence claim.

Third-party source wording is not a product asset class.

## 7. Maturity labels

Every prompt-like asset included in the pack must expose its current state:

```text
DRAFT
VALID
TESTED
CANDIDATE / IMPROVED
CERTIFIED
PORTABLE
```

For v1, `VALID` assets are distributable if clearly labeled and commercially reviewed. Distribution does not promote their MK1 state.

## 8. Generator v0 integration gate

Generator v0 is an optional v1 component.

It enters the pack only when:

- canonical Generator v0 CI receipt = `PASS`;
- compile = success;
- F1/F2 regression = success;
- generator tests = success;
- example generation = success;
- generated artifacts remain `VALID`/`engineered` unless higher real evidence exists.

The current canonical receipt must be treated as authoritative until replaced by a newer receipt.

## 9. Example requirements

Each example should include:

- original task/request;
- normalized task brief;
- chosen architecture and rationale;
- final prompt/template;
- static quality result or checklist;
- maturity label;
- claim boundary.

Examples must not fabricate runtime observations.

## 10. README requirements

The customer-facing README must explain:

- what the pack solves;
- a 5-minute quickstart;
- package structure;
- architecture vocabulary;
- how to customize a template;
- how to evaluate before production use;
- evidence-state meanings;
- known limitations.

Avoid marketing language that conflicts with evidence.

## 11. Machine-readable manifest

`MANIFEST.json` will be the release inventory and should contain at least:

```json
{
  "schema": "prompt-quarry-product-manifest-v1",
  "product_id": "pq-developer-pack",
  "version": "1.0.0",
  "source_commit": "<release commit>",
  "release_status": "DRAFT|READY",
  "artifacts": [],
  "claim_boundary": "..."
}
```

Every artifact entry should include path, type, authority/provenance class, maturity state, claims, and evidence references where applicable.

## 12. Quality gates

### Q1 — provenance
No asset has ambiguous authorship/source class.

### Q2 — distribution safety
No internal-only or non-distributable third-party body is accidentally bundled.

### Q3 — static integrity
Examples/templates are internally consistent, variables are defined, and output contracts are usable.

### Q4 — evidence integrity
No label exceeds the strongest receipt supporting it.

### Q5 — reproducibility
Manifest binds the release to an exact source commit and inventory.

### Q6 — usability
A developer can complete the quickstart without access to Prompt Quarry internals.

## 13. Commercial acceptance test

Before `1.0.0`, perform a clean-room package test:

1. export only files listed in `MANIFEST.json`;
2. place them outside the repository;
3. follow QUICKSTART from scratch;
4. ensure no internal path is required;
5. verify all example inputs are present;
6. verify claims against evidence references;
7. hash/fingerprint the final distributable archive.

## 14. v1 definition of done

```text
[ ] canonical Generator v0 receipt PASS (required only if Generator is bundled)
[ ] Product Manifest approved
[ ] distributable MANIFEST.json populated
[ ] customer README complete
[ ] QUICKSTART complete
[ ] templates complete
[ ] examples complete
[ ] checklists complete
[ ] provenance/evidence review PASS
[ ] clean-room acceptance PASS
[ ] release archive fingerprinted
```

Only after these gates should the package be called Developer Pack `1.0.0`.
