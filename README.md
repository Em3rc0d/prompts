# Prompt Machine

**Reusable AI workflows for real tasks — engineered and evidenced by Prompt Quarry.**

Prompt Machine is the customer-facing product direction of this repository: a platform where people discover AI workflows by **what they need to get done**, use useful workflows for free, and upgrade only when broader reusable coverage earns the price.

Prompt Quarry is the internal factory that acquires knowledge, engineers artifacts, tests behavior, preserves provenance, and governs what Prompt Machine is allowed to claim.

Canonical strategy: [`docs/PRODUCT_VISION_V3.md`](docs/PRODUCT_VISION_V3.md).
Commercial experiment: [`commercial/REVENUE_EXPERIMENT_V1.md`](commercial/REVENUE_EXPERIMENT_V1.md).

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

Current launch hypothesis:

```text
FREE LIBRARY                 USD 0
STARTER COLLECTION           USD 9 one-time   ← primary first paid offer
FULL DEVELOPER COLLECTION    USD 19 one-time  ← broader premium / upsell
SUBSCRIPTION                 DEFERRED
```

Both paid prices remain `PRICE_HYPOTHESIS`. Public checkout remains disabled.

### Free Library — $0

The free layer must be useful by itself. It exists to create value, trust, repeat usage, and evidence of demand—not to intentionally cripple the customer experience.

Current concrete free release:

```text
Prompt Machine Free Developer Workflows
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

The historical route `/free/developer-starter-pack` remains for compatibility. Naming compatibility does not redefine the paid Starter Collection.

### Starter Collection — $9 one-time hypothesis

The Starter Collection is the primary first-purchase experiment.

Frozen commercial scope:

- Evidence-first Code Review workflow;
- Evidence-first Bug Diagnosis workflow;
- `review-code-with-evidence` skill candidate;
- `diagnose-bugs-with-evidence` skill candidate;
- `START_HERE` entrypoint and task chooser;
- worked examples;
- verification guidance;
- adaptation cheatsheet;
- explicit evidence and limitations.

```text
product id       pq-developer-starter-collection
candidate        1.2.0-candidate
workflow families 2
skill candidates 2
launch price      USD 9 one-time (PRICE_HYPOTHESIS)
scope             FROZEN
checkout          DISABLED
sale state        NOT_FOR_SALE
```

`SCOPE FROZEN` is a product decision only. It does not imply runtime testing, certification, portability, deterministic packaging, provider custody, or readiness to sell.

### Full Developer Workflow Collection — $19 one-time hypothesis

The full collection is the broader upsell only when additional coverage earns it.

```text
product id         pq-developer-pack
candidate          1.2.0-candidate
workflow families  4
skill candidates   4
launch price        USD 19 one-time (PRICE_HYPOTHESIS)
checkout            DISABLED
sale state          NOT_FOR_SALE
```

Full adds Technical Decision and AI Workflow Design coverage, the complete four-skill candidate set, broader operating contracts, examples, adaptation guidance, and collection-level orchestration.

The $19 tier must win on **additional value**, not artificial restrictions in Free or Starter.

No public checkout should be enabled before the exact SKU's release and delivery gates close.

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
$9 Starter intent / purchase
        ↓
$19 Full intent / upgrade when needed
        ↓
repeat purchase / referral / expansion
```

The product should measure observed movement through this funnel rather than assume market demand before launch.

Primary commercial milestone:

```text
PQ-$1 = first real non-test paid purchase successfully delivered
```

A CTA click, checkout creation, provider test order, or synthetic smoke event does not satisfy `PQ-$1`.

## Observability

The customer-facing app forwards only allowlisted intent events to:

`POST /api/analytics/intent`

Server runtime emits:

```text
PM_INTENT_EVENT
evidence_class = UNTRUSTED_CLIENT_INTENT
```

The intent path is now runtime-observed on the isolated staging project. Synthetic staging events are explicitly not customer demand and not purchase evidence.

Important evidence boundaries:

```text
client intent                 != purchase evidence
free artifact serve           != revenue
checkout created              != revenue
provider test order           != revenue
accepted real paid provider event == purchase evidence
```

The anonymous browser session identifier stays browser-session-only and is not intentionally sent to the server intent sink.

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
scope frozen != behavior proven
build pass != deployed
deployed != used
CTA != revenue
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
PCP04_REAL_EXECUTIONS       0 / 84

F4_TESTED                   NO
F5_IMPROVED                 NO
F6_CERTIFIED                NO
F7_PORTABLE                 NO
```

The 84-observation requirement includes three independent executions of every repeatability fixture. Synthetic or incomplete receipts cannot promote F4.

## Skills

The full Developer Workflow Collection candidate contains four installable skill candidates:

- `review-code-with-evidence`
- `diagnose-bugs-with-evidence`
- `make-technical-decisions`
- `design-ai-workflows`

Starter's frozen commercial scope contains the first two only.

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

- `/` — outcome-first landing and `$0 → $9 → $19` ladder
- `/collections` — Starter + Full collection discovery
- `/free/developer-starter-pack` — current free developer workflows
- `/starter-collection` — $9 Starter scope/status
- `/developer-pack` — $19 Full collection status; compatibility route
- `/learn` — education/acquisition layer
- `/license` — license summary

Frontend validation:

`.github/workflows/validate-prompt-machine-web.yml`

Staging deployment:

`.github/workflows/deploy-prompt-machine-staging.yml`

The deployment workflow is hard-bound to the isolated `prompt-quarry-stage` Vercel project, verifies Prompt Machine identity, and requires an HTTP 202 synthetic intent smoke before passing. The separate public production project is not targeted by this workflow.

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
→ Starter intent
→ $9 purchase
→ Full intent / $19 upgrade
→ repeat purchase / referral
```

There is no honest pre-launch variable that guarantees people will buy. Confidence grows through observed activation, repeat usage, conversion, purchases, support/refund signals, and demand for additional outcomes.

## Current critical path

```text
Prompt Machine positioning      DONE ON PRODUCT BRANCH
        ↓
$0 → $9 → $19 customer UX       IMPLEMENTED + STAGING OBSERVED
        ↓
Starter commercial scope        FROZEN / NOT FOR SALE
        ↓
PCP-04 real baseline execution  0 / 84
        ↓
failure mining + improvement    OPEN
        ↓
skill behavioral/parity tests   OPEN
        ↓
final customer surfaces         OPEN
        ↓
Starter deterministic archive   OPEN
        ↓
provider + delivery canary       OPEN
        ↓
USD 9 public experiment          NOT ENABLED
        ↓
PQ-$1 + observed conversion      NOT OBSERVED
        ↓
USD 19 upgrade behavior          NOT OBSERVED
```

We do not call Prompt Machine commercially successful before a real customer pays, and we do not call a workflow certified before its evidence earns that label.
