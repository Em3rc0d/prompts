# Prompt Quarry Certification Program

Status: `ACTIVE / PCP-00 PASS / PCP-01 PASS / PCP-02 PASS / PCP-03 NEXT`

This program converts the current Free and Paid product baselines into governed,
testable prompt artifacts. It does not change the frozen product files in place.

## Naming decision

The original working plan named its milestones `MK3.0` through `MK3.14`.
Prompt Quarry already uses `MK0`, `MK1`, and `MK2` for architectural maturity
layers, with MK2 intentionally deferred. To avoid implying that certification is
a new architecture layer after MK2, this directory uses `PCP-00` through
`PCP-14` (`Prompt Certification Program`). The original names remain aliases:

| Program milestone | Original alias | Outcome |
|---|---|---|
| `PCP-00` | `MK3.0` | Freeze and inventory |
| `PCP-01` | `MK3.1` | Prompt specification |
| `PCP-02` | `MK3.2` | Static quality audit |
| `PCP-03` | `MK3.3` | Test matrix design |
| `PCP-04` | `MK3.4` | Baseline execution |
| `PCP-05` | `MK3.5` | Failure mining |
| `PCP-06` | `MK3.6` | Improvement pass |
| `PCP-07` | `MK3.7` | Regression |
| `PCP-08` | `MK3.8` | Portability |
| `PCP-09` | `MK3.9` | Human value review |
| `PCP-10` | `MK3.10` | Certification decision |
| `PCP-11` | `MK3.11` | Rebuild Free Pack |
| `PCP-12` | `MK3.12` | Rebuild Paid Pack |
| `PCP-13` | `MK3.13` | Pack-level QA |
| `PCP-14` | `MK3.14` | Commercial release gate |

## Master invariant

```text
NO PROMPT MAY ENTER A RELEASE
WITHOUT A PROMPT_ID + SPEC + TEST EVIDENCE + CERTIFICATION DECISION
```

Prompt Quarry does not claim value because a prompt was generated or packaged.
It claims only the evidence state that the prompt has actually earned.

## Frozen PCP-00 baseline

The inventory is bound to the active integration train as observed on
`2026-09-01`:

```text
integration branch     feat/mk1-prompt-generator-v0-20260827
observed head          a70ee18f8a15e65ed08b153fa95f1397821d8014

Free Pack              pq-developer-starter 1.1.0
customer assets        7
prompt artifacts       3
archive SHA-256        55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32

Paid Pack              pq-developer-pack 1.1.0 RC1
customer assets        13
prompt artifacts       4
source fingerprint     dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
archive SHA-256        546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009

Total pack assets      20
Prompt artifacts       7
Non-prompt assets      13
Semantic families      4
```

The prompt inventory is `inventory/product-prompt-inventory.v1.json`. Its schema
is `specs/PRODUCT_PROMPT_INVENTORY.schema.json`, and the gate receipt is
`receipts/pcp-00-inventory-audit.v1.json`.

The frozen specifications are `specs/product-prompt-specifications.v1.json`.
Their schema is `specs/PRODUCT_PROMPT_SPECIFICATION_SET.schema.json`, and the
gate receipt is `receipts/pcp-01-spec-completeness.v1.json`.

## Artifact boundary

The inventory contains executable finished workflows and reusable operating
templates. It deliberately excludes licenses, product documentation, quickstarts,
checklists, examples, methodologies, and machine-readable contracts from the
prompt count. Those assets remain governed by the existing pack manifests.

Three Free/Paid pairs share a semantic family: Bug Diagnosis, Code Review, and
Technical Decision. They are not duplicates. The Free asset is a finished
workflow; the Paid asset exposes configurable operating policy. Both remain in
the baseline and are linked through `family_id`.

## Current evidence state

```text
PROMPT_INVENTORY_AUDITED    PASS
PROMPT_SPEC_COMPLETE        PASS
STATIC_AUDIT_COMPLETE       PASS
PROMPT_TEST_MATRIX          NOT_STARTED
F4_TESTED                   NO
F5_IMPROVED                 NO
F6_CERTIFIED                NO
F7_PORTABLE                 NO
PACK_VALUE_REVIEW           NOT_STARTED

PRODUCT_READY               NO
READY_TO_SELL                NO
```

`PACKAGING_READY` and `COMMERCE_BUILD_READY` remain separate, already evidenced
product-system states. They do not promote any prompt to `TESTED`, `IMPROVED`,
`CERTIFIED`, or `PORTABLE`.

## Change rule

The Free v1.1.0 payload and Paid v1.1.0 RC1 remain immutable historical
baselines. Any improvement produced by PCP-06 must create a new prompt version
with explicit `BEFORE -> FAILURE -> HYPOTHESIS -> AFTER -> RETEST` provenance.

## Next critical front

`PCP-03 / Test Matrix Design` is next. The static audit completed 105/105 P1-P15
ratings with `94 PASS / 10 WARN / 1 FAIL`. The single blocker is preserved against
`PQ-PROMPT-0005`: its `BLOCKED` input rule says to return only unblocking
information, while its fallback also requires preserving a safe partial result.
No prompt was modified. PCP-03 must turn that contradiction and the remaining
warnings into explicit fixtures before baseline execution.
