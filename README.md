# Prompt Quarry

Private research, engineering, and product repository for turning prompt/skill knowledge into governed reusable AI workflows with explicit provenance and evidence boundaries.

## System model

```text
MK0 — KNOWLEDGE QUARRY
"What exists, and what do we actually know about it?"
        │
        ▼
MK1 — PROMPT FORGE
"Can we engineer and evaluate reusable prompt artifacts?"
        │
        ▼
MK2 — PROMPT ENGINE
"Can the system automatically route, compose, test and improve them?"
```

- **MK0** owns source evidence, semantic artifact identity, characterization, normalized metadata, mined techniques, fixtures, provenance, and human-readable materialization.
- **MK1** owns prompt contracts, architecture selection, assembly, critique, runtime fixtures, baseline comparison, promotion receipts, and the Prompt Generator.
- **MK2** remains the future orchestration layer and is intentionally deferred until MK1 evidence is mature enough to support it.

Canonical stage entry points:

- `mk0/README.md`
- `mk1/README.md`
- `mk2/README.md`
- `docs/ROADMAP.md`

## Core principles

1. **Source first.** Keep original/official source identity whenever available.
2. **Raw != normalized != derived != engineered.** Do not collapse evidence and transformation layers.
3. **Provenance survives transformation and deduplication.**
4. **Prompt != skill != workflow.** Semantic artifact identity precedes structural scoring.
5. **Evidence before claims.** Unknown != pass; generated != valid; valid != tested; tested != improved; improved != certified; certified != portable.
6. **No access-control bypass.** Collectors stop at authentication, CAPTCHA, paywalls, or changed authorization boundaries.
7. **Minimize third-party body duplication.** Prefer metadata, URLs, fingerprints, structural observations, and repository-authored abstractions.
8. **Promotion is gated.** Failed or unobserved gates are never bypassed to make an artifact look ready.
9. **Human readability matters.** Machine evidence and human inspection surfaces are separate but both first-class.
10. **Meaningful failures become fixtures.** Regression evidence replaces ad-hoc patch accumulation.
11. **`not observed == unknown`.** This applies to model behavior, builds, deployment, payments, and product claims.

## Architecture

```text
EXTERNAL SOURCES
      │
      ▼
┌─────────────────────────────────────────┐
│ MK0 — KNOWLEDGE QUARRY                  │
│                                         │
│ acquire → identify → characterize       │
│         → normalize → derive            │
│         → fixtures / Golden data        │
│         → readable materialization      │
└──────────────────┬──────────────────────┘
                   │ governed knowledge
                   ▼
┌─────────────────────────────────────────┐
│ MK1 — PROMPT FORGE                      │
│                                         │
│ brief → architecture → candidate        │
│       → critic → runtime fixtures       │
│       → baseline → rubric → receipt     │
│       → promotion / rejection           │
└──────────────────┬──────────────────────┘
                   │ sufficiently evidenced artifacts
                   ▼
┌─────────────────────────────────────────┐
│ MK2 — PROMPT ENGINE                     │
│                                         │
│ route → retrieve/compose → evaluate     │
│       → select → execute → feedback     │
└─────────────────────────────────────────┘
```

See `docs/ARCHITECTURE.md` and `docs/ROADMAP.md` for the full design.

## Repository map

```text
prompts/
├── mk0/                    # source knowledge + characterization
├── mk1/                    # engineered artifacts + evidence pipeline
├── mk2/                    # deferred orchestration architecture
├── quarry/                 # raw / normalized / analysis / fixtures
├── library/                # governed reusable material
├── readable/               # human-readable materializations
├── product/                # Free Pack + Developer Pack product sources
├── commercial/             # landing / funnel / Golden Path / launch contracts
├── web/                    # Next.js public product surface
├── tools/                  # builders, validators, probes, harnesses
├── .ci/                    # durable CI / release / Golden Path receipts
├── .approvals/             # explicit approval evidence
└── .github/workflows/      # automation entry points
```

## Current integration state

The active integration train is:

```text
feat/mk1-prompt-generator-v0-20260827
```

It is tracked by draft PR `#2` into `main`.

`main` is intentionally not treated as the current product truth until that integration train is reconciled and promoted.

### MK0

MK0 has moved beyond simple corpus collection into semantic artifact and corpus governance. Reference material cannot silently become canonical Prompt Quarry truth, and structural quality evaluation is limited to artifacts whose semantic type is appropriate for that evaluation.

Use `mk0/README.md` and current characterization receipts for exact corpus state.

### MK1

The repository now contains infrastructure across the Forge pipeline rather than stopping at F2.

Prompt Generator v0 has a durable static CI receipt with:

```text
dependencies          PASS
compile               PASS
F1/F2 regression      PASS
generator tests       PASS
example generation    PASS
```

That receipt establishes static generator behavior only. It does **not** establish behavioral superiority or certification.

Canonical maturity ladder:

```text
DRAFT
  ↓
VALID
  ↓
TESTED
  ↓
CANDIDATE / IMPROVED
  ↓
CERTIFIED
  ↓
PORTABLE
```

No higher state may be inferred from CI success, generated examples, deployment health, or product packaging alone.

### MK2

`ARCHITECTURE ONLY / DEFERRED`

MK2 should not become the active implementation front until MK1 has enough real behavioral evidence, certified families, portability evidence, and lifecycle/version semantics to justify automatic orchestration.

## Product surfaces

### Free Developer Starter Pack v1.1.0

Current public state:

```text
DELIVERY          VERIFIED
VERSION           1.1.0
FILES             7
ZIP BYTES         23498
SHA-256           55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
```

Public surface:

`https://prompt-quarry.vercel.app/free/developer-starter-pack`

The Free Pack is useful product material, not behavioral certification evidence.

### Developer Pack v1.1

Current governed state:

```text
RELEASE_CANDIDATE RC1
NOT_FOR_SALE
13 customer-visible assets
static maturity: VALID_CANDIDATE
F4 TESTED:    NO
F5 IMPROVED:  NO
F6 CERTIFIED: NO
F7 PORTABLE:  NO
```

The RC1 source inventory is frozen and its deterministic builder exists. The remaining release blocker is physical archive evidence: successful deterministic execution, two byte-identical builds, recorded archive SHA-256/size, and approval bound to that exact artifact.

Do not enable paid checkout before that gate closes.

## Public Golden Path

Canonical production domain:

`https://prompt-quarry.vercel.app`

Required route behavior is defined by:

`commercial/GOLDEN_PATH_CONTRACT_V1.json`

Current durable resilience evidence:

`.ci/golden-path/wave2-production-20260829.json`

Observed infrastructure classification:

```text
HEALTHY_THROUGH_C200_WITHIN_TESTED_ENVELOPE
runtime_errors = 0
free artifact integrity preserved
checkout = intentional 503 HOLD
webhook GET = expected 405 route presence
```

This is serving/infrastructure evidence only. It is not F4/F5/F6/F7 evidence and it is not payment proof.

## Commercial status

The canonical commercial execution snapshot is:

`commercial/STATUS_V1.md`

Current sequence:

```text
Developer Pack RC1 deterministic build
        ↓
exact archive fingerprint + approval
        ↓
packaging/commercial READY
        ↓
provider provisioning + controlled test order
        ↓
signed provider webhook + exact paid delivery
        ↓
PQ-LAUNCH-0
        ↓
real non-test purchase
        ↓
PQ-$1
```

The public Free Pack path is live. The paid path is intentionally held.

## Current merge boundary

The draft integration PR should not be merged just because production serves correctly.

Before promotion to `main`, reconcile at least:

1. canonical docs/status against observed repository and production state;
2. branch-level CI and durable receipt inventory;
3. Developer Pack RC1 physical release evidence or an explicit decision to keep that gate post-merge;
4. obsolete branches as `MERGE`, `SUPERSEDED`, or `ARCHIVE`;
5. claims so no `TESTED`, `IMPROVED`, `CERTIFIED`, `PORTABLE`, payment, or revenue statement exceeds evidence.

Prompt Quarry treats the distinction between **implemented**, **observed**, **validated**, **behaviorally proven**, and **commercially ready** as part of the product itself.
