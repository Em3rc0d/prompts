# Prompt Machine Developer Workflow Collection v1.2 — Product Specification

Status: `CANDIDATE IMPLEMENTED / STRUCTURE PASS / BEHAVIORAL TESTING REQUIRED / NOT FOR SALE`

Version target: `1.2.0`

Technical product ID: `pq-developer-pack`  
Customer-facing name: `Developer Workflow Collection`

The technical ID is retained for compatibility with existing repository and commerce contracts. It does not define the public brand.

## Product objective

Package four evidence-first engineering workflows so a buyer can choose a real task, reach the right workflow quickly, use either the prompt or installable skill surface where available, and understand the result and its evidence limits without reverse-engineering a ZIP.

The collection is a **Prompt Machine** product. **Prompt Quarry** is the internal engineering and certification factory that produces its evidence.

## Customer outcome

Target journey:

```text
OPEN COLLECTION
      ↓
START_HERE
      ↓
CHOOSE THE TASK
      ↓
OPEN ONE WORKFLOW
      ↓
PROVIDE REQUIRED INPUTS
      ↓
RUN PROMPT OR SKILL
      ↓
VERIFY RESULT + LIMITS
      ↓
REUSE / ADAPT / CHOOSE NEXT WORKFLOW
```

Within a ten-minute target journey, a developer should be able to select one workflow, install or copy it, bind real inputs, run it, and understand both the result and its evidence limits.

**Ten-minute activation is an acceptance target, not an observed claim.** It requires later customer/usability evidence.

## Workflow inventory

| Workflow ID | Customer task | Prompt lineage | Skill ID | Skill folder |
|---|---|---|---|---|
| `PQ-WF-0001` | Review a software change | `PQ-PROMPT-0002`, `PQ-PROMPT-0006` | `PQ-SKILL-0001` | `review-code-with-evidence` |
| `PQ-WF-0002` | Diagnose a bug or regression | `PQ-PROMPT-0001`, `PQ-PROMPT-0004` | `PQ-SKILL-0002` | `diagnose-bugs-with-evidence` |
| `PQ-WF-0003` | Make a technical decision | `PQ-PROMPT-0003`, `PQ-PROMPT-0007` | `PQ-SKILL-0003` | `make-technical-decisions` |
| `PQ-WF-0004` | Design a reusable AI workflow | `PQ-PROMPT-0005` + v1.2 successor | `PQ-SKILL-0004` | `design-ai-workflows` |

The skill is not a wrapper that merely says “use the prompt.” It translates the same operating contract into a discoverable workflow with focused instructions and only resources that materially improve execution.

## Customer experience contract

The final archive must open with one obvious entry point:

`START_HERE.md`

That entry point must answer:

1. What can I accomplish with this collection?
2. Which workflow should I choose for my current task?
3. What do I need before I run it?
4. Should I use the prompt surface or install the skill?
5. What output should I expect?
6. How do I verify the result?
7. What is tested, untested, or unsupported?
8. What should I open next?

A customer should not need to understand `MK0`, `MK1`, `PCP`, Prompt Quarry repository layout, prompt IDs, or certification implementation to begin using the product.

Technical identifiers may appear in evidence/provenance sections after the human-readable workflow name.

## Required product components

### 1. Start Here

Final release requires:

- task-to-workflow chooser;
- 5-minute quick path;
- prompt-vs-skill guidance;
- installation guidance where supported;
- verification guidance;
- evidence legend;
- links to each workflow and example;
- support/limitations entry point.

The current design artifact is `START_HERE.candidate.md`. It is not yet a release asset.

### 2. Prompt surface

Each workflow must include:

- one stable customer-facing prompt or configurable operating contract;
- explicit required and optional inputs;
- output and decision states;
- truth and authority boundaries;
- fallback behavior;
- source prompt ID/version in provenance metadata.

The v1.2 customer prompt surfaces for all workflows must be materialized only from governed versions. Frozen v1.1 baselines are not silently rewritten in place.

### 3. Skill surface

Each workflow skill must include:

- valid `SKILL.md` frontmatter with discriminating name and description;
- concise core workflow instructions;
- references only where progressive disclosure reduces irrelevant context;
- scripts only where deterministic execution materially improves reliability;
- exact prompt-lineage metadata in the release manifest;
- normal, non-trigger, missing-input, conflict, and adversarial evals;
- host-specific installation and invocation receipt before host support is claimed.

Current state: four skill candidates exist and the structural gate passes. Host behavioral evidence remains incomplete.

### 4. Example surface

Each workflow must have at least one customer-readable example showing:

```text
REALISTIC TASK
→ REQUIRED INPUTS
→ HOW TO RUN
→ OUTPUT SHAPE
→ WHAT TO VERIFY
→ WHAT THE WORKFLOW CANNOT ESTABLISH
```

Examples are educational fixtures, not substitutes for real behavioral evidence.

### 5. Evidence surface

Each workflow must include a customer-readable evidence card with:

- exact version/fingerprint;
- structural state;
- tested host/model/runtime only when observed;
- fixture summary;
- known limitations;
- certification decision;
- unsupported hosts marked `NOT_CERTIFIED`, never implied compatible.

Customer vocabulary should stay compact (`VERSIONED`, `STRUCTURE CHECKED`, `RUNTIME TESTED`, `IMPROVED`, `CERTIFIED`, `KNOWN LIMITATIONS`) while internal PCP details remain inspectable separately.

## Free / paid boundary

### Free Library

The currently released free developer entry remains useful by itself:

- Code Review;
- Bug Diagnosis;
- Technical Decision.

It is not intentionally crippled to force an upgrade.

### Paid collection

The paid v1.2 candidate must earn the $19 upgrade through:

- four related workflow systems;
- four skill surfaces;
- reusable operating contracts;
- guided task selection;
- examples;
- adaptation material;
- evidence cards;
- easier reuse across recurring software work.

If the paid collection is merely “more files,” it fails the value review.

## Prompt / skill parity

For the same fixture and evidence boundary, prompt and skill surfaces must:

- require materially equivalent inputs;
- preserve the same evidence labels;
- return compatible decision states;
- enforce the same authority rules;
- expose the same material unknowns;
- not contradict each other on fallback behavior.

Equivalent semantics do not require identical wording or prose length.

## Packaging contract

The final release archive must:

- have exactly one customer-facing root folder;
- put `START_HERE.md` at that root;
- contain only customer-facing assets;
- build deterministically;
- record source path, Git blob SHA, archive path, byte size, SHA-256, license class, and workflow ownership for every file;
- build each skill as its own deterministic ZIP containing exactly one top-level skill directory.

Proposed customer archive root:

`prompt-machine-developer-workflow-collection-v1.2.0`

This name becomes authoritative only when the deterministic archive receipt is created.

## Commercial contract

Launch price hypothesis: `USD $19 one-time`.

Checkout remains disabled until all required product and provider gates pass. The v1.1 provider identity and archive hash cannot authorize v1.2 delivery.

Buyer rights remain: use and adapt for authorized personal, team, product, and service workflows. Resale, sublicensing, redistribution, mirroring, publishing, or reconstructing a competing prompt/skill collection are not granted.

## Claim contract

Allowed now when directly evidenced:

- four skill candidates exist;
- skill structure validation passes;
- workflow/product specifications exist;
- frozen behavioral fixtures/work orders exist;
- current sale state is `NOT_FOR_SALE`.

Allowed only after corresponding receipts:

- final deterministic customer archive exists;
- tested on a named host/runtime;
- prompt/skill parity passes;
- improved relative to a frozen baseline;
- certified for a named workflow/target;
- portable across named hosts;
- ten-minute activation observed;
- customer purchase/revenue occurred.

Never allowed as blanket statements:

- works with every LLM;
- never hallucinates;
- guarantees correct decisions;
- replaces expert review;
- guaranteed productivity/revenue;
- production ready without scope.

Master public rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Current gates

```text
PRODUCT_MODEL_FROZEN          PASS
PCP_03_PROMPT_TEST_MATRIX     PASS
VERSIONED_BLOCKER_RESOLUTION  PASS
SKILL_CANDIDATES_IMPLEMENTED  PASS
SKILL_STRUCTURE               PASS
START_HERE_DESIGN             PASS

PCP_04_REAL_EXECUTION         OPEN
SKILL_TRIGGER_EVAL            OPEN
SKILL_FORWARD_TEST            OPEN
PROMPT_SKILL_PARITY           OPEN
CUSTOMER_PROMPT_SURFACES      INCOMPLETE
CUSTOMER_EXAMPLES             INCOMPLETE
EVIDENCE_CARDS                INCOMPLETE
PACK_VALUE_REVIEW             OPEN
DETERMINISTIC_ARCHIVE         OPEN
PROVIDER_CUSTODY              OPEN
PROVIDER_INTEGRATION          OPEN
LIVE_DELIVERY_CANARY          OPEN
PRODUCT_READY                 NO
READY_TO_SELL                 NO
```

## Exit criteria

The candidate may enter final deterministic packaging only when:

- PCP-04/05/06 decisions establish the governed customer prompt versions;
- all four customer prompt surfaces exist;
- all four skill packages preserve the intended contract;
- prompt/skill parity fixtures and required results are available;
- customer examples exist;
- customer evidence cards exist;
- `START_HERE.md` contains no candidate/pending instructions;
- Free/Paid distinction passes value review;
- no claim exceeds receipts.

It may become sellable only after behavioral, installation, product-value, archive, provider, and live-delivery gates pass.
