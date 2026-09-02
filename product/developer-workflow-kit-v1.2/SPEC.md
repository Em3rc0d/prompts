# Prompt Quarry Developer Workflow Kit v1.2 — Product Specification

Status: `DRAFT / DESIGN FROZEN / IMPLEMENTATION NOT STARTED / NOT FOR SALE`

Version target: `1.2.0`

Product ID: `pq-developer-pack`

## Product objective

Package four evidence-first engineering workflows so a buyer can use each one
as either a copy/paste prompt or an installable Agent Skill without losing its
input, evidence, authority, output, verification, and fallback semantics.

## Customer outcome

Within a ten-minute target journey, a developer should be able to select one
workflow, install or copy it, bind real inputs, run it, and understand both the
result and its evidence limits.

This is an acceptance target. It is not yet observed.

## Workflow inventory

| Workflow ID | Customer name | Prompt lineage | Skill ID | Skill folder |
|---|---|---|---|---|
| `PQ-WF-0001` | Evidence-first Code Review | `PQ-PROMPT-0002`, `PQ-PROMPT-0006` | `PQ-SKILL-0001` | `review-code-with-evidence` |
| `PQ-WF-0002` | Evidence-first Bug Diagnosis | `PQ-PROMPT-0001`, `PQ-PROMPT-0004` | `PQ-SKILL-0002` | `diagnose-bugs-with-evidence` |
| `PQ-WF-0003` | Technical Research and Decision | `PQ-PROMPT-0003`, `PQ-PROMPT-0007` | `PQ-SKILL-0003` | `make-technical-decisions` |
| `PQ-WF-0004` | AI Workflow Contract Designer | `PQ-PROMPT-0005` | `PQ-SKILL-0004` | `design-ai-workflows` |

The skill is not a wrapper that tells the model to “use the prompt.” It must
translate the same operating contract into a discoverable workflow with focused
instructions and only the resources that materially improve execution.

## Required product components

### Prompt surface

Each workflow must include:

- one stable prompt or configurable operating contract;
- explicit required and optional inputs;
- output and decision states;
- truth and authority boundaries;
- fallback behavior;
- source prompt ID and version.

### Skill surface

Each workflow skill must include:

- valid `SKILL.md` frontmatter with discriminating name and description;
- concise core workflow instructions;
- references only where progressive disclosure reduces irrelevant context;
- scripts only where deterministic execution materially improves reliability;
- exact prompt-lineage metadata in the release manifest;
- normal, non-trigger, missing-input, conflict, and adversarial evals;
- host-specific installation and invocation receipt.

### Evidence surface

Each workflow must include a customer-readable evidence card:

- exact version and fingerprint;
- statically reviewed state;
- tested hosts and model/runtime versions;
- fixtures executed;
- known limitations;
- certification decision;
- unsupported hosts marked `NOT_CERTIFIED`, never implied compatible.

## Free/Paid boundary

Free v1.2 candidate contains the three current finished prompts and only
`PQ-SKILL-0001`. It demonstrates installation quality without exposing the full
configuration, governance, test, and adaptation system.

Paid v1.2 candidate contains all four workflow systems, all four skills,
contracts, examples, evidence, and adaptation material.

## Prompt/skill parity

For the same fixture and evidence boundary, prompt and skill surfaces must:

- require materially equivalent inputs;
- preserve the same evidence labels;
- return compatible decision states;
- enforce the same authority rules;
- expose the same material unknowns;
- not contradict each other on fallback behavior.

Equivalent semantics do not require identical wording or identical prose length.

## Packaging contract

The release archive must be deterministic and contain only customer-facing
assets. Every file records source path, Git blob SHA, archive path, byte size,
SHA-256, license class, and workflow ownership.

Every skill must also build as its own deterministic ZIP containing exactly one
top-level skill directory.

## Commercial contract

Launch price hypothesis: `USD $19 one-time`.

Checkout remains disabled until all product and provider gates pass. The v1.1
provider identity and archive hash cannot authorize v1.2 delivery.

Buyer rights remain: use and adapt for authorized personal, team, product, and
service workflows. Resale, sublicensing, redistribution, mirroring, publishing,
or reconstructing a competing prompt/skill pack are not granted.

## Claim contract

Allowed after structural build:

- four workflow kits;
- prompt and skill surfaces included;
- Agent Skills structured;
- deterministic archive;
- versioned evidence boundary.

Allowed only after matching receipts:

- tested on a named host/runtime;
- certified for a named workflow and target;
- portable across named hosts;
- ten-minute activation observed.

Never allowed as a blanket statement:

- works with every LLM;
- never hallucinates;
- guarantees correct decisions;
- replaces expert review;
- production ready without scope.

## Exit criteria

The candidate may enter deterministic packaging only when:

- PCP-03 test matrix is frozen;
- the `PQ-PROMPT-0005` static blocker is resolved in a new version;
- all four skill specifications are frozen;
- all four skill packages validate structurally;
- prompt/skill parity fixtures exist;
- customer evidence cards exist;
- Free/Paid distinction passes review;
- no F4–F7 claim exceeds receipts.

It may become sellable only after behavioral, installation, pack, provider, and
live-delivery gates pass.
