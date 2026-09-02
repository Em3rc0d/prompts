# Prompt Machine

**Reusable AI workflows for real tasks — engineered and evidenced by Prompt Quarry.**

Prompt Machine is the customer-facing product direction of this repository: a platform where people discover AI workflows by **what they need to get done**, use useful workflows for free, and upgrade to curated collections when broader coverage earns the price.

Prompt Quarry is the internal factory that acquires knowledge, engineers artifacts, tests behavior, preserves provenance, and governs what Prompt Machine is allowed to claim.

Canonical strategy: [`docs/PRODUCT_VISION_V3.md`](docs/PRODUCT_VISION_V3.md).

```text
CUSTOMER
   │
   ▼
PROMPT MACHINE
choose outcome → use workflow → verify → reuse → collection
   │
   │ powered by
   ▼
PROMPT QUARRY
MK0 → MK1 → PCP → evidence → eligible product artifact
```

## What this project is becoming

Prompt Machine is **not a store of raw prompt files**.

The primary unit of customer value is a **workflow**: a reusable way to perform a task with clear inputs, process, output, fallback, boundaries, and verification guidance.

The primary merchandising unit is a **collection**: related workflows grouped around an outcome.

Initial outcome taxonomy:

- **Build & Ship** — review work, diagnose problems, design solutions, validate changes.
- **Research & Decide** — compare options, structure evidence, make defensible decisions.
- **Learn & Create** — turn knowledge into projects and useful deliverables.
- **Operate & Automate** — reduce repetitive administrative and operational work.

Professions remain useful metadata, but discovery begins with:

> **What are you trying to get done?**

## Commercial model

### Free Library

The free layer must be useful by itself. It exists to create value, trust, repeat usage, and evidence of demand—not to intentionally cripple the customer experience.

Current concrete free release:

```text
Developer Starter / Free Library
version           1.1.0
workflows         3
customer files    7
archive bytes     23,498
SHA-256           55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
delivery          VERIFIED
```

Available workflows:

1. Code Review
2. Bug Diagnosis
3. Technical Decision

Public compatibility route:

`https://prompt-quarry.vercel.app/free/developer-starter-pack`

The current domain is a legacy naming surface. A domain migration is separate from the product-architecture decision.

### Paid Collections

First commercial experiment:

```text
Developer Workflow Collection
candidate          1.2.0-candidate
workflow families  4
skill candidates   4
launch price        USD 19 one-time (hypothesis)
checkout            DISABLED
sale state          NOT_FOR_SALE
```

The paid collection is expected to earn the upgrade through broader workflow coverage, reusable operating contracts, skills, examples, adaptation guidance, and evidence—not by hiding the only useful version behind payment.

No public checkout should be enabled before release and delivery gates close.

## Customer funnel

```text
content / search / social
        ↓
Prompt Machine home
        ↓
"What do you want to get done?"
        ↓
free workflow / outcome
        ↓
real task usage
        ↓
repeat usage + trust
        ↓
paid collection intent
        ↓
checkout
        ↓
repeat purchase / expansion
```

The product should measure observed movement through this funnel rather than assume market demand before launch.

## Trust model

Prompt Quarry exists so Prompt Machine can make conservative, inspectable claims.

Master rule:

```text
MARKETING CLAIM <= OBSERVED EVIDENCE
```

Canonical maturity ladder for engineered artifacts:

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

Important distinctions:

```text
generated != valid
valid != tested
tested != improved
improved != certified
certified != portable
packaged != behaviorally proven
build pass != deployed
provider test != customer purchase
not observed == unknown
```

## Internal factory

### MK0 — Knowledge Quarry

> What exists, and what do we actually know about it?

Owns source evidence, semantic artifact identity, characterization, normalized metadata, mined techniques, fixtures, provenance, and human-readable materialization.

### MK1 — Prompt Forge

> Can we engineer and evaluate reusable workflow artifacts?

Owns prompt contracts, architecture selection, assembly, static critique, runtime fixtures, baseline comparison, promotion receipts, and generator infrastructure.

### MK2 — Prompt Engine

> Can the system automatically route, compose, test, and improve workflows?

`ARCHITECTURE ONLY / DEFERRED` until MK1 and certification evidence are mature enough to justify orchestration.

### PCP — Prompt Certification Program

Owns frozen baselines, specifications, static audit, behavioral test matrices, real execution receipts, failure mining, improvements, regression, portability, and certification decisions.

Current PCP execution boundary on this product branch:

```text
PROMPT_INVENTORY_AUDITED    PASS
PROMPT_SPEC_COMPLETE        PASS
STATIC_AUDIT_COMPLETE       PASS
PROMPT_TEST_MATRIX          PASS
PCP04_FIXTURES              PASS
PCP04_WORK_ORDERS           PASS
PCP04_REQUIRED_EXECUTIONS   84
PCP04_REAL_EXECUTIONS       NOT_COMPLETED

F4_TESTED                   NO
F5_IMPROVED                 NO
F6_CERTIFIED                NO
F7_PORTABLE                 NO
```

The 84-observation requirement includes three independent executions of every repeatability fixture. Synthetic or incomplete receipts cannot promote F4.

## Skills

The first Developer Workflow Collection candidate contains four installable skill candidates:

- `review-code-with-evidence`
- `diagnose-bugs-with-evidence`
- `make-technical-decisions`
- `design-ai-workflows`

Current evidence:

```text
SKILL_STRUCTURE             PASS
TRIGGER/NON-TRIGGER INPUTS  DEFINED
HOST BEHAVIORAL TEST        NOT_COMPLETED
PROMPT/SKILL PARITY         NOT_COMPLETED
PORTABILITY                 NOT_COMPLETED
```

A structurally valid skill is not implicitly host-tested or portable.

## Public web

`web/` is the Prompt Machine customer-facing application.

Primary routes on this branch:

- `/` — outcome-first landing
- `/collections` — collection discovery
- `/free/developer-starter-pack` — current free developer workflows
- `/developer-pack` — Developer Workflow Collection status; compatibility route
- `/license` — license summary

Frontend validation:

`.github/workflows/validate-prompt-machine-web.yml`

Acceptance runs TypeScript typecheck and a production Next.js build, including the existing governed Free Pack materialization and Golden Path build assertion.

See [`web/README.md`](web/README.md).

## Repository map

```text
prompts/
├── web/                    # Prompt Machine customer surface
├── product/                # customer product sources / candidates
├── commercial/             # funnel, commerce, provider and launch contracts
├── certification/          # PCP + skill certification evidence
├── mk0/                    # internal source knowledge + characterization
├── mk1/                    # internal prompt/workflow engineering
├── mk2/                    # deferred orchestration architecture
├── quarry/                 # raw / normalized / analysis / fixtures
├── library/                # governed reusable material
├── readable/               # human-readable materializations
├── tools/                  # builders, validators, probes and harnesses
├── .ci/                    # durable CI / release receipts
├── .approvals/             # explicit approval evidence
└── .github/workflows/      # automation entry points
```

## Revenue objective, product discipline

Prompt Machine exists to become a real revenue channel. Revenue is the business outcome, but it must come from customer value rather than from inflating the catalog or claims.

North-star product signal:

> **A person successfully uses a workflow on a real task and comes back for another task.**

Commercial signals follow:

```text
visitor
→ free activation
→ repeat user
→ paid intent
→ purchase
→ second purchase / expansion
```

There is no honest pre-launch variable that guarantees people will buy. Confidence grows through observed activation, repeat usage, conversion, purchases, support/refund signals, and demand for additional outcomes.

## Current critical path

```text
Prompt Machine positioning      DONE ON PRODUCT BRANCH
        ↓
outcome/collection UX           IN PROGRESS
        ↓
PCP-04 real baseline execution  OPEN
        ↓
failure mining + improvement    OPEN
        ↓
skill behavioral/parity tests   OPEN
        ↓
paid collection release QA      OPEN
        ↓
provider + delivery canary       OPEN
        ↓
USD 19 public experiment         NOT ENABLED
        ↓
PQ-$1 + observed conversion      NOT OBSERVED
```

We do not call Prompt Machine commercially successful before the first real customer pays, and we do not call a workflow certified before its evidence earns that label.
