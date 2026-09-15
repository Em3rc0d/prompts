# Prompt Quarry Product Model v2

Status: `DECISION FROZEN / IMPLEMENTATION NOT STARTED / NOT FOR SALE`

Observed at: `2026-09-02T12:45:01Z`

## Decision

Prompt Quarry is the factory. The customer-facing product is a **Certified AI
Workflow Kit**.

```text
WORKFLOW
  ├── Prompt      copy/paste execution surface
  ├── Skill       installable, discoverable execution surface
  ├── Contract    inputs, outputs, evidence, authority, fallback
  ├── Fixtures    normal, missing, noisy, conflicting, adversarial cases
  ├── Receipts    what was actually tested and where
  └── Guide       install, configure, run, inspect, adapt
```

Prompts and skills are both sold, but neither is the commercial unit by itself.
The kit is the unit because it turns reusable wording into an installable and
inspectable working capability.

## What we sell

| Candidate unit | Decision | Reason |
|---|---|---|
| Raw prompt collection | `REJECT` | Easy to copy, difficult to trust, weak differentiation |
| Prompt | `KEEP AS INTERFACE` | Lowest-friction use in any chat or model UI |
| Skill | `KEEP AS INTERFACE` | Repeatable discovery, packaged resources, scripts, and workflow behavior |
| Workflow Kit | `SELL` | Combines immediate use, repeatability, adaptation, and evidence |
| Prompt generator access | `DEFER` | Requires mature certified families and reliable selection/evaluation |
| Subscription | `DEFER UNTIL PQ-$1` | One-time demand must be demonstrated first |

## Category and positioning

Category:

`Evidence-first AI workflow kits for software teams.`

Core promise after certification:

> Install the workflow as a skill or use it as a structured prompt. Configure
> its policy, run it on real engineering work, and inspect what it knows,
> assumes, recommends, and cannot prove.

Prompt Quarry must not lead with prompt count. It leads with four outcomes:

1. less setup work;
2. less behavior drift across repeated runs;
3. explicit evidence and authority boundaries;
4. inspectable outputs that fit engineering decisions.

## Initial customer

Primary buyer:

- individual developer using AI repeatedly for code review, diagnosis, and
  technical decisions;
- technical lead standardizing AI-assisted workflows for a small team;
- builder integrating a repeatable workflow into an agent, form, ticket, PR,
  or internal tool.

The first release does not target prompt collectors, large-enterprise
procurement, nontechnical consumer templates, or buyers seeking autonomous
production changes.

## Product ladder

### Free — Developer Starter v1.2 candidate

Price: `$0`

Purpose: demonstrate real value and prove that installation is understandable.

Candidate contents:

- three finished prompts: Code Review, Bug Diagnosis, Technical Decision;
- one installable skill: `review-code-with-evidence`;
- one worked example;
- quickstart and evidence boundary;
- no card, account, or checkout requirement.

Free remains useful. It demonstrates the prompt surface and one complete skill
surface without replacing the Paid construction system.

### Paid — Developer Workflow Kit v1.2 candidate

Product ID: `pq-developer-pack`

Launch price hypothesis: `USD $19 one-time`

Candidate contents:

- four governed workflows;
- four copy/paste prompt or operating-contract surfaces;
- four installable Agent Skills;
- configuration contracts;
- worked transformations;
- test fixtures and evidence receipts;
- adaptation and team-integration guidance;
- proprietary commercial-use license.

The four workflows are:

1. Evidence-first Code Review;
2. Evidence-first Bug Diagnosis;
3. Technical Research and Decision;
4. AI Workflow Contract Designer.

Individual skill sales, larger bundles, team licenses, and recurring updates are
post-`PQ-$1` experiments, not initial-launch scope.

## Why Paid is materially larger than Free

```text
FREE
3 finished prompts
+ 1 installable skill
+ immediate use

PAID
4 configurable workflow systems
+ 4 installable skills
+ machine-readable contracts
+ evidence and authority policy
+ adaptation method
+ fixtures and receipts
+ team/application integration
```

Paid value is the ability to preserve workflow semantics across repeated work,
not extra words or hidden prompt bodies.

## Compatibility claims

The package format targets the open Agent Skills structure used by current
OpenAI skills: a versioned folder with required `SKILL.md` and optional scripts,
references, assets, and UI metadata.

Allowed before runtime certification:

- `Agent Skills structured`;
- `designed for Codex skill installation`;
- `prompt fallback included`;
- `host support stated per receipt`.

Forbidden without evidence:

- `works with every LLM`;
- `portable across all agents`;
- `automatically triggers correctly`;
- `production ready`;
- `certified`;
- `proven to improve results`.

Structural compatibility and behavioral portability are different gates.

## Definition of solid

A prompt is solid only when its specification, static audit, fixtures, baseline,
and certification decision exist.

A skill is solid only when, in addition:

- its description triggers on intended requests and stays inactive elsewhere;
- `SKILL.md` preserves the workflow contract;
- referenced files exist and are loaded only when relevant;
- scripts, when present, run deterministically and safely;
- missing, conflicting, and adversarial input behavior is tested;
- installation and invocation are observed on every claimed host;
- its exact release fingerprint is recorded.

## Delivery contract

The Paid ZIP candidate should expose:

```text
prompt-quarry-developer-workflow-kit-v1.2.0/
├── START-HERE.md
├── LICENSE.md
├── prompts/
├── skills/
├── contracts/
├── examples/
├── evidence/
└── CHANGELOG.md
```

Every `skills/<name>/` directory must be independently installable. The full ZIP
must also be understandable by a buyer who never installs a skill and uses only
the prompt surfaces.

## Ten-minute activation target

A first-time customer should be able to:

1. open `START-HERE.md`;
2. select one workflow by desired outcome;
3. either copy its prompt or install its skill;
4. supply a real task;
5. receive the declared output shape;
6. understand the evidence state and next action.

This is a target for later observation, not a current performance claim.

## Commercial release gate

```text
PROMPT_CERTIFICATION          PASS
SKILL_STRUCTURE              PASS
SKILL_TRIGGER_EVAL           PASS
SKILL_FORWARD_TEST           PASS
INSTALLATION_CANARY          PASS
PROMPT_SKILL_PARITY          PASS
PACK_VALUE_REVIEW            PASS
DETERMINISTIC_ARCHIVE        PASS
PROVIDER_CUSTODY             PASS
PROVIDER_INTEGRATION         PASS
LIVE_DELIVERY_CANARY         PASS
```

Only then:

```text
PRODUCT_READY = YES
READY_TO_SELL = YES
```

## Current boundary

Developer Pack v1.1.0 RC1 remains immutable and `NOT_FOR_SALE`. This decision
creates a new v1.2.0 candidate; it does not relabel v1.1, change its 13 blobs,
enable checkout, deploy the landing, or create provider/revenue evidence.

## Execution order

```text
PCP-03 prompt test matrix
  ↓
versioned resolution of static blocker
  ↓
four skill specifications
  ↓
skill source packages
  ↓
prompt + skill forward tests
  ↓
Free/Paid v1.2 deterministic builds
  ↓
pack QA
  ↓
provider gates
  ↓
public release
```

## Primary references

- OpenAI, “Build skills”: https://developers.openai.com/codex/build-skills
- OpenAI API, “Skills”: https://developers.openai.com/api/docs/guides/tools-skills
- OpenAI, “Testing Agent Skills Systematically with Evals”:
  https://developers.openai.com/blog/eval-skills
- Vercel, “Agent Skills”: https://vercel.com/docs/agent-resources/skills
