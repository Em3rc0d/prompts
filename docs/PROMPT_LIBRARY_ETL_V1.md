# Prompt Library ETL v1 — Quality Before Quantity

Status: `DESIGNED / STATIC-ONLY / NO MODEL CALLS / NO AUTOMATIC PRODUCT PROMOTION`

## Purpose

Prompt Quarry currently contains hundreds of repository-authored prompt reconstructions derived from public metadata and mined architecture patterns. Their existence is inventory, not proof of commercial quality.

This ETL converts that inventory into a governed review surface:

```text
EXTRACT
  ↓
TRANSFORM
  ↓
STATIC QUALITY GATE
  ↓
STRUCTURAL CLUSTERING
  ↓
REPRESENTATIVE REVIEW QUEUE
  ↓
STATIC QUALIFIED CANDIDATES
  ↓
SEPARATE PRODUCT / PCP PIPELINE
```

The ETL must never equate `generated`, `non-empty`, `valid JSON`, or `loaded` with `sellable`.

## Truth contract

```text
SOURCE REFERENCE            != SOURCE PROMPT BODY
RECONSTRUCTION              != SOURCE REPRODUCTION
GENERATED                   != USEFUL
USEFUL                      != DISTINCT
DISTINCT                    != TESTED
STATIC QUALIFIED            != BEHAVIORALLY PROVEN
STATIC QUALIFIED            != READY_TO_SELL
LOADED INTO ETL OUTPUT      != PRODUCT PROMOTION
```

No ETL state may create F4/F5/F6/F7 evidence.

## Inputs

### Source metadata

`quarry/normalized/alpacka-ai-prompt-metadata.jsonl`

Expected current contract:

- 530 source prompt references;
- 52 free references with public content observed by the harvester;
- 478 premium references whose source body is not public;
- provenance and access state preserved.

### Repository-authored reconstructions

`library/prompts/alpacka/derived-premium/catalog.jsonl`

Expected current contract:

- one reconstruction per premium source reference;
- `content_origin = repository-authored-reconstruction`;
- `source_body_status = not-public`;
- non-empty prompt content.

## E — Extract

Extract performs a strict one-to-one join between premium source references and repository-authored reconstructions.

It verifies:

1. source IDs and UUIDs are unique;
2. every premium reference has exactly one reconstruction;
3. every reconstruction maps back to an observed premium reference;
4. provenance labels do not represent reconstructed content as the unavailable source body;
5. content is non-empty and hashable.

Integrity failures are `REJECTED`; they are not repaired silently.

## T — Transform

Transform derives inspectable, deterministic quality signals without calling an LLM:

- canonical title/category/mode;
- risk class;
- prompt length and variable count;
- presence of objective, intake, process, constraints, output contract and verification;
- evidence/uncertainty discipline;
- instruction-vs-data boundary;
- high-stakes safety boundary;
- structural skeleton fingerprint;
- clone-cluster size.

### Structural skeleton

The skeleton intentionally removes record-specific decoration such as:

- the exact objective title;
- role wording;
- variable names;
- repeated intake-variable rows;

while preserving the actual process, rules and output architecture.

If two records collapse to the same skeleton, they are treated as members of the same structural family for review purposes.

This prevents us from confusing hundreds of title variants with hundreds of independently engineered workflows.

## Quality gate

The v1 deterministic score is diagnostic, not certification.

| Criterion | Points |
|---|---:|
| Provenance integrity | 15 |
| Explicit objective | 8 |
| Intake contract | 8 |
| Task process | 10 |
| Constraints/rules | 10 |
| Output contract | 10 |
| Verification/self-check | 5 |
| Evidence discipline | 10 |
| Uncertainty/fallback discipline | 8 |
| Instruction/data boundary | 10 |
| Structural differentiation | 6 |
| **Total** | **100** |

A score cannot override a blocking semantic defect.

### Blocking conditions

A record cannot become `STATIC_QUALIFIED_NOT_FOR_SALE` when any of these are true:

- provenance/integrity failure;
- missing objective, process, constraints or output contract;
- no explicit instruction-vs-data boundary;
- high-stakes category without a safety boundary;
- material structural clone cluster (`cluster_size > 5`);
- content too small to implement its claimed workflow.

High-stakes categories are always routed to explicit review even when structurally strong.

## States

### `REJECTED`

The record fails provenance or basic integrity. It does not continue.

### `REWORK_REQUIRED`

The record is a valid repository artifact but its static design is too generic, incomplete, ambiguous or clone-heavy for product consideration.

### `HIGH_STAKES_REVIEW_REQUIRED`

The record concerns a high-stakes category. Static structure may be useful, but automated qualification is forbidden.

### `STATIC_QUALIFIED_NOT_FOR_SALE`

The record clears the deterministic static gate. This means only that it is eligible for deeper semantic/product review.

It does **not** mean tested, certified, pack-eligible or ready to sell.

## L — Load

The ETL loads only review/evidence outputs under:

`quarry/etl/prompt-library-v1/`

Expected files:

- `quality-report.jsonl` — one static assessment per joined reconstruction;
- `clone-clusters.json` — structural-family summary;
- `representative-review.jsonl` — one preferred representative per structural family;
- `manifest.json` — counts, truth boundary and pipeline status.

The ETL does not write to the public product catalog and does not change commercial states.

## Quality-first expansion rule

Bulk review is forbidden while the base structural families are unresolved.

```text
478 reconstructions
      ↓
N structural skeletons
      ↓
review N representatives first
      ↓
fix architecture / generator
      ↓
regenerate
      ↓
re-run ETL
      ↓
only then review per-record semantic fit
```

This is the main economic rule of the pipeline: do not spend human or model effort reviewing the same structural defect hundreds of times.

## Current commercial boundary

```text
ETL automatic product promotions  = 0
ETL runtime model calls            = 0
ETL behavioral claims              = 0
ETL READY_TO_SELL claims           = 0
```

The separate Prompt Machine product/certification pipeline remains authoritative for any future release claim.
