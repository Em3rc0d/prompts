# Prompt Quarry Certification Program

Status: `ACTIVE / PCP-00..03 PASS / PCP-04 READY FOR REAL EXECUTION`

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

## PCP-03 — test matrix: PASS

The behavioral matrix is frozen in:

`fixtures/pcp-03-test-matrix.v1.json`

Every prompt is bound to ten case classes:

```text
NORMAL
MINIMAL
MISSING_REQUIRED
AMBIGUOUS
CONTRADICTORY
NOISY
ADVERSARIAL_OVERRIDE
EVIDENCE_DISCIPLINE
OUTPUT_CONTRACT
REPEATABILITY
```

Concrete reusable family inputs are frozen in:

`fixtures/pcp-04-family-cases.v1.json`

That fixture set contains:

```text
4 semantic families
40 concrete family cases
70 prompt-case assignments
```

Fixture completeness is test-design evidence only. It is not behavioral proof.

## PCP-04 — baseline execution: READY / NOT EXECUTED

The exact frozen baseline bytes and concrete cases are materialized into an
execution packet by:

`tools/prepare_pcp04_work_orders.py`

The real-execution receipt contract is:

`specs/PCP04_EXECUTION_RECEIPT.schema.json`

Receipts are aggregated by:

`tools/validate_pcp04_receipts.py`

The packet preparation receipt is:

`receipts/pcp-04-work-orders.v1.json`

Observed preparation evidence:

```text
workflow                  Prepare PCP-04 Work Orders
run                       33639114500
source commit             994b61adf2f54e922d1d8ccc6afd559269c52d47
result                    PASS
prompts                   7
work orders               70
real executions required  84
repeatability             3 independent runs / prompt
work-orders JSONL SHA256  9a4e3c87457295aa90f1280297d97270bb1e7ba0f0d92162b3d70dbc6aacd213
artifact                  9850041484
artifact SHA256           f13550df3abf86a1bc32ab360024b617c81a9ecea2eadf2c0acc339c1dc8caef
```

Why 84 executions instead of 70: each of the seven `REPEATABILITY` work orders
requires three independent observations rather than one. Their execution IDs
must be distinct and their reviewer-normalized material outcome signatures must
remain stable.

The receipt gate has its own CI characterization. It proves that:

- an empty campaign cannot promote;
- a synthetic receipt is rejected;
- a structurally valid but incomplete campaign remains `F4_TESTED = false`;
- individual receipts cannot self-declare prompt-level TESTED eligibility.

No real PCP-04 model execution receipt is currently persisted.

## Versioned blocker resolution

`PQ-PROMPT-0005` v1.1 remains immutable as the frozen baseline and still carries
the PCP-02 contradiction that must be observed during baseline execution.

A v1.2 successor exists at:

`../product/developer-workflow-kit-v1.2/prompts/general-operating-contract-v1.2.md`

Its `BLOCKED` semantics resolve the contradiction without rewriting history:
partial **evidence** may be preserved, but the domain task/result may not be
claimed complete. That successor is not yet behaviorally promoted; it belongs to
the forward improvement/regression path.

## Skill track

The four v1.2 skill candidates are now structurally valid. Durable structural
receipt:

`receipts/skill-structure.v1.json`

Current skill boundary:

```text
SKILL_STRUCTURE_PASS      YES
SKILL_TRIGGER_FIXTURES    DEFINED / UNEXECUTED
SKILL_TRIGGER_EVAL_PASS   NO
SKILL_FORWARD_TEST_PASS   NO
PROMPT_SKILL_PARITY_PASS  NO
WORKFLOW_CERTIFIED        NO
PORTABLE                  NO
```

Structural validity does not imply host installation, discovery, execution,
certification, portability, or product readiness.

## Current evidence state

```text
PROMPT_INVENTORY_AUDITED    PASS
PROMPT_SPEC_COMPLETE        PASS
STATIC_AUDIT_COMPLETE       PASS
PROMPT_TEST_MATRIX          PASS
PCP04_FIXTURES_FROZEN       PASS
PCP04_WORK_ORDERS_READY     PASS
PCP04_REAL_EXECUTIONS       0 / 84
F4_TESTED                   NO
F5_IMPROVED                 NO
F6_CERTIFIED                NO
F7_PORTABLE                 NO
PACK_VALUE_REVIEW           NOT_STARTED

PRODUCT_READY               NO
READY_TO_SELL               NO
```

`PACKAGING_READY` and `COMMERCE_BUILD_READY` remain separate, already evidenced
product-system states. They do not promote any prompt to `TESTED`, `IMPROVED`,
`CERTIFIED`, or `PORTABLE`.

## Change rule

The Free v1.1.0 payload and Paid v1.1.0 RC1 remain immutable historical
baselines. Any improvement produced by PCP-06 must create a new prompt version
with explicit:

```text
BEFORE -> FAILURE -> HYPOTHESIS -> AFTER -> RETEST
```

provenance.

## Next critical front

The only prompt-certification blocker before failure mining is now real PCP-04
execution:

```text
84 real baseline observations
        ↓
schema-valid receipts + verbatim outputs
        ↓
strict aggregate
        ↓
BASELINE_PASS / BASELINE_FAIL per prompt
        ↓
PCP-05 failure mining
        ↓
PCP-06 versioned improvements
```

A self-hosted WSL/Codex capability probe exists to determine whether the `vigia`
runner can execute this campaign without API-key infrastructure. Until a real
runtime actually accepts the work, the evidence state remains `NOT EXECUTED`.
