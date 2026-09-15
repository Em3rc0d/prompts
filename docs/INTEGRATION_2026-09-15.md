# Repository Integration — 2026-09-15

Status: `INTEGRATION_BRANCH_ACTIVE / MAIN_UNTOUCHED`

Branch:

`integration/prompt-machine-consolidated-20260915`

## Objective

Consolidate the repository's strongest compatible history into one reviewable branch without rewriting evidence history, silently discarding divergent commits, changing current commercial truth, or promoting release/certification labels.

## Baseline

The consolidation branch was created from the exact `main` head that existed at the start of this integration:

```text
main
SHA d4427e50ca4ec2b2f089b6b0e7469ebe78ffd983
```

`main` was not updated by this integration.

## Primary train

The selected primary train is:

```text
feat/workflow-kits-product-model-20260902
SHA 1c6b740a34037086c5b8730ff0392f7881be4585
```

GitHub comparison established:

```text
merge base  d4427e50ca4ec2b2f089b6b0e7469ebe78ffd983
status      ahead
behind      0
commits     +1257
```

Therefore the primary train is a direct descendant of the starting `main` baseline and was integrated into the consolidation branch by non-forced fast-forward.

## Preserved divergent F7 history

The standalone branch:

`feat/mk1-certified-portable-split`

contained one relevant divergent commit:

```text
1f6fe248370d733f3b90d7a1e48ec1954183d4c9
mk1: materialize F7 zero-state manifest
```

The current primary train already contains an effective F7 zero-state manifest with the same current semantics/content. Dropping the divergent commit would lose ancestry; replaying its tree over the current branch would risk reverting newer work.

The consolidation therefore created an **ancestry-only merge commit**:

```text
5cd5806677010ff0617a6e90bfc76ecd78d27de2
```

Parents:

```text
1c6b740a34037086c5b8730ff0392f7881be4585
1f6fe248370d733f3b90d7a1e48ec1954183d4c9
```

Tree policy:

```text
current primary-train tree retained exactly
no F6/F7 state promotion
no certification claim added
```

This preserves history without changing effective artifact state.

## Other historical branches

Repository comparison showed that the major work required for this consolidation — including the Prompt Generator line, PCP baseline evolution and MK0 physical-boundary refactor — is already contained in the selected primary train.

Older divergent research branches are not blindly merged. Their unique ideas must be evaluated source-by-source before any future history/content import; superseded files must not overwrite current canonical structures merely to make every branch an ancestor.

## prompts.chat integration

External source:

```text
repository  f/prompts.chat
revision    f78a1c5136fa080155d928e0d7e2b4a41ddef03e
captured    2026-09-15
```

Integrated as MK0 comparative source evidence:

- `mk0/sources/prompts-chat/README.md`
- `mk0/sources/prompts-chat/SOURCE_MAP.md`
- `mk0/analysis/prompts-chat-product-architecture-benchmark.md`

Truth boundary:

```text
source observation
    !=
repository-derived architecture lesson
    !=
MK1 engineered artifact
    !=
certified product
```

No bulk prompt-body import was performed. No `prompts.chat` prompt is promoted to MK1 by this integration.

## Brand reconciliation

Current customer-facing architecture was already adopted on 2026-09-08:

```text
CUSTOMER-FACING  Verlune
PRODUCT          Verlune Code Review
PRODUCT ENGINE   Prompt Machine
EVIDENCE FACTORY Prompt Quarry
```

The old root README and `docs/PRODUCT_VISION_V3.md` still contained pre-Verlune customer-brand wording. This integration reconciles active navigation/documentation while preserving the historical strategy document as a superseded snapshot rather than rewriting its history.

Current commercial truth remains anchored in:

1. `commercial/STATUS_CURRENT.md`
2. `commercial/VERLUNE_BRAND_ARCHITECTURE_V1.md`
3. exact release/certification receipts referenced from those files.

## Explicit non-effects

This repository integration does **not** change:

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
real revenue        0
PQ-$1               NOT OBSERVED
```

It does not grant new F4/F5/F6/F7 labels, alter the exact certified workflow bytes, claim cross-model portability, or convert provider Test observations into Live readiness.

## Validation requirements before main

The integration is reviewable only after all applicable checks are inspected on the final branch head.

At minimum verify:

1. branch ancestry and diff against `main`;
2. no unintended deletion of current product/evidence surfaces;
3. no active brand copy that incorrectly presents Prompt Machine/Prompt Quarry as the public buyer brand;
4. MK0 source path consistency;
5. current web/type/build validations applicable to changed files;
6. no commercial state promotion caused by documentation-only integration;
7. final PR remains unmerged until explicitly reviewed.

## Merge policy

Target PR:

```text
integration/prompt-machine-consolidated-20260915
    → main
```

Opening the PR is allowed after branch validation. Merging the PR into `main` is a separate decision and is not implied by this integration record.
