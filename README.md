# Verlune / Prompt Machine / Prompt Quarry

This repository contains the product-engineering and evidence system behind the first **Verlune** release.

Current identity boundary:

```text
CUSTOMER-FACING
Verlune
└── Verlune Code Review

PRODUCT ENGINE
Prompt Machine
└── packaging / release / commerce orchestration

EVIDENCE FACTORY
Prompt Quarry
└── MK0 / MK1 / PCP / experiments / evaluation / certification
```

**Prompt Machine and Prompt Quarry are internal engineering identities.** Stable historical IDs may retain `pm` / `pq` prefixes where changing them would damage provenance, but buyer-facing product copy must use `Verlune`.

Current canonical entrypoints:

- [`commercial/STATUS_CURRENT.md`](commercial/STATUS_CURRENT.md) — operational/commercial truth.
- [`commercial/VERLUNE_BRAND_ARCHITECTURE_V1.md`](commercial/VERLUNE_BRAND_ARCHITECTURE_V1.md) — adopted brand boundary.
- [`docs/INTEGRATION_2026-09-15.md`](docs/INTEGRATION_2026-09-15.md) — current repository consolidation record.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — MK0/MK1/MK2 capability roadmap.
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — provenance/truth rules.

`docs/PRODUCT_VISION_V3.md` is preserved as a historical pre-Verlune strategy snapshot. Its customer-brand wording is no longer authoritative.

---

## First customer product

```text
brand            Verlune
product          Verlune Code Review
version          1.0.0
price            USD 9 one-time — PRICE_HYPOTHESIS
workflow count   1
archive          verlune-code-review-v1.0.0.zip
bytes            18,859
sha256           4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649
payload fp       46554b5aa36166e6bee7f07b572fa4bece29811270e014cb96381099c87ca430
pack QA          77/77 PASS
```

The canonical workflow identity remains:

```text
workflow_id      pm-starter-evidence-first-code-review-v2
contract         2.2.0
bytes            25,295
sha256           6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
authority        ADVISORY_ONLY
```

The historical `pm-` identifier is preserved for evidence continuity; it is not buyer-facing branding.

Commercial observations above are sourced from the last reconciled release record dated `2026-09-08`. The 2026-09-15 repository integration does not pretend to refresh external provider state.

## Commercial truth boundary

Current recorded state remains conservative:

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
real revenue        0
PQ-$1               NOT OBSERVED
```

Repository consolidation, documentation cleanup, package integrity, Test provider observations or a passing build do not independently change those values.

Master invariant:

```text
MARKETING CLAIM <= OBSERVED EVIDENCE
```

---

## Evidence and release gates

Current first-product gate state recorded in `commercial/STATUS_CURRENT.md`:

```text
G05 Baseline Execution    FAIL / REWORK — historical defect preserved
G06 Failure Mining        CLOSED
G07 Improvement           PASS
G08 Regression            PASS — 4/4 required final cases
G09 Portability           MODEL_SPECIFIC / PASS_FOR_DEMONSTRATED_SCOPE
G10 Human Value Review    KEEP / RECORDED
G11 Certification         PASS_FOR_EXACT_DECLARED_SCOPE
G12 Pack Rebuild          PASS — Verlune 1.0.0
G13 Pack-level QA         PASS — Verlune 1.0.0, 77/77
G14 Provider Gates        HISTORICAL RC2 TEST PATH PASS / VERLUNE TEST PROVIDER VALIDATION PENDING
```

Behavioral evidence is scoped to the declared model/runtime evidence. `MODEL_SPECIFIC` is not cross-model portability.

The next external/commercial frontier recorded by the repository is still provider/live validation. The integration branch must not silently turn Test-path evidence into Live readiness.

---

# Internal system

## Prompt Quarry

Prompt Quarry is the evidence and engineering factory. It keeps source observation, repository derivation and engineered artifacts separate.

```text
EXTERNAL SOURCES
      │
      ▼
MK0 — KNOWLEDGE QUARRY
source evidence → normalization → analysis → fixtures → reviewed knowledge
      │
      ▼
MK1 — PROMPT / WORKFLOW FORGE
brief → architecture → candidate → critique → runtime evidence → comparison
      │
      ▼
PCP — CERTIFICATION PROGRAM
frozen contract → execution → review → regression → scoped certification
      │
      ▼
ELIGIBLE PRODUCT ARTIFACT
      │
      ▼
Prompt Machine release/commerce orchestration
      │
      ▼
Verlune customer product
```

Truth boundary:

```text
SOURCE OBSERVATION
    !=
REPOSITORY-DERIVED KNOWLEDGE
    !=
ENGINEERED ARTIFACT
    !=
TESTED
    !=
IMPROVED
    !=
CERTIFIED
    !=
PORTABLE
    !=
READY_TO_SELL
```

### MK0 — Knowledge Quarry

> What exists, what did we actually observe, and what reusable knowledge can be extracted?

Canonical root: `mk0/`.

MK0 owns:

- raw/source observations;
- normalized evidence;
- source registry/provenance;
- indexes and analysis;
- Golden Dataset/regression evidence;
- reviewed reusable knowledge;
- source-family maps;
- human-readable projections.

External source characterization now includes the revision-bound `prompts.chat` architecture benchmark:

- [`mk0/sources/prompts-chat/README.md`](mk0/sources/prompts-chat/README.md)
- [`mk0/sources/prompts-chat/SOURCE_MAP.md`](mk0/sources/prompts-chat/SOURCE_MAP.md)
- [`mk0/analysis/prompts-chat-product-architecture-benchmark.md`](mk0/analysis/prompts-chat-product-architecture-benchmark.md)

That benchmark informs architecture; it does not promote upstream prompts into MK1.

### MK1 — Prompt / Workflow Forge

> Can we engineer, test and compare reusable AI artifacts from governed knowledge?

Canonical evidence ladder:

```text
DRAFT
  ↓
VALID
  ↓ real behavioral evidence
TESTED
  ↓ fair baseline comparison
CANDIDATE / IMPROVED
  ↓ repeated same-target evidence
CERTIFIED
  ↓ optional cross-provider evidence
PORTABLE
```

`CERTIFIED` and `PORTABLE` are intentionally distinct. See:

- `mk1/specs/F6_TARGET_RUNTIME_CERTIFICATION.md`
- `mk1/specs/F7_PORTABILITY.md`

### MK2 — Prompt Engine

MK2 is the future orchestration layer for routing, retrieval/composition, evaluation, selection and feedback.

Current policy remains: **architecture/deferred until the lower-stage evidence contracts justify orchestration.**

### PCP — Prompt Certification Program

PCP owns product-facing certification evidence such as frozen baselines, behavioral test matrices, execution receipts, failure mining, improvement/regression and scoped release decisions.

A historical or failed execution remains part of the evidence record; it is not rewritten away to make a release look cleaner.

---

## Prompt Machine

Prompt Machine is the internal product engine between evidence and commercial delivery.

Its responsibilities include:

- selecting eligible artifacts from governed evidence;
- assembling deterministic customer packages;
- preserving version/fingerprint lineage;
- release-state gating;
- provider/store integration;
- delivery verification;
- customer-surface orchestration;
- commercial observability without inflating claims.

It is **not** the public masterbrand.

---

## External architecture benchmark: prompts.chat

The captured source revision is:

```text
f/prompts.chat
main@f78a1c5136fa080155d928e0d7e2b4a41ddef03e
```

Observed architecture includes first-class prompt versions/change requests, categories/tags, collections, prompt connections, model/MCP hints, CLI/MCP/plugin distribution, self-hosting/white-label configuration and authenticated AI-assisted improvement.

Prompt Quarry derives several useful product hypotheses from that source while preserving stricter evidence rules:

```text
catalog size        != quality
popularity          != behavioral validity
AI generation       != improvement evidence
model hints         != portability
MCP support         != certification
community feedback  != certification
```

Current near-term implications are deliberately narrow: improve source registration, artifact metadata and customer-readable version projections; evaluate CLI/MCP/plugin delivery only after commercial proof and only if exact version/fingerprint identity survives the adapter.

---

## Repository map

```text
prompts/
├── commercial/             # brand, provider, release and sale-state truth
├── certification/          # PCP/product certification evidence and receipts
├── product/                # customer product sources/candidates/packages
├── web/                    # customer-facing web implementation
├── mk0/                    # Knowledge Quarry — source evidence + derived knowledge
│   ├── raw/
│   ├── normalized/
│   ├── catalog/
│   ├── indexes/
│   ├── analysis/
│   ├── golden-dataset/
│   ├── promotions/
│   ├── library/
│   ├── sources/
│   └── readable/
├── mk1/                    # engineered candidate/evaluation/certification machinery
├── mk2/                    # deferred orchestration architecture
├── tools/                  # builders, validators, probes and harnesses
├── docs/                   # cross-stage architecture and integration records
├── .ci/                    # durable CI/release receipts
├── .approvals/             # explicit approvals
└── .github/workflows/      # automation entrypoints
```

Legacy paths may remain inside immutable historical evidence. Active consumers should use the canonical MK0 paths.

---

## Repository integration state — 2026-09-15

The review branch is:

```text
integration/prompt-machine-consolidated-20260915
```

It was created from the exact starting `main` head:

```text
d4427e50ca4ec2b2f089b6b0e7469ebe78ffd983
```

Then the primary product/evidence train was fast-forwarded from:

```text
feat/workflow-kits-product-model-20260902
1c6b740a34037086c5b8730ff0392f7881be4585
```

GitHub comparison showed that train was `1257` commits ahead and `0` behind the starting `main` baseline.

The standalone F7 history commit `1f6fe248370d733f3b90d7a1e48ec1954183d4c9` was preserved through an ancestry-only merge without altering the effective current tree or promoting certification state.

See [`docs/INTEGRATION_2026-09-15.md`](docs/INTEGRATION_2026-09-15.md) for the exact integration contract.

**`main` remains the review target, not an automatically updated branch.** Opening a PR does not authorize merging it.

---

## Current critical path

The repository integration does not replace the product-release frontier.

Recorded commercial path remains approximately:

```text
reconcile exact Verlune Test product/file metadata
        ↓
provider activation/identity approval observed
        ↓
copy exact Verlune 1.0.0 into Live
        ↓
freeze Live provider IDs/credentials outside repo
        ↓
verify provider-served bytes + exact SHA
        ↓
Live webhook/private canary gate
        ↓
buyer delivery canary only if separately authorized
        ↓
public checkout only when release evidence permits
        ↓
first real paid delivery / PQ-$1
```

No repository cleanup step may skip those gates.
