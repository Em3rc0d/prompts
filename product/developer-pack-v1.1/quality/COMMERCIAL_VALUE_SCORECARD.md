# Developer Pack v1.1 — Commercial Value Scorecard

Status: `MANUAL STATIC INSPECTION — PASS`

Scope: current v1.1 product-quality slice only.

This scorecard applies `quality/COMMERCIAL_VALUE_GATE.md` to the actual customer-facing assets. It evaluates static product distinction from the Free Developer Starter Pack v1.1.

It does **not** establish behavioral superiority, market demand, willingness to pay, F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE`.

## Scoring scale

- `0` — no meaningful advantage over Free;
- `1` — partial advantage; customer value remains ambiguous;
- `2` — clear usable advantage that reduces real setup/review work.

Blocking requirements per core template:

```text
minimum total score      12 / 14
no dimension             0
parameterization         2
verification             2
governance               2
```

---

## 1. General Operating Contract

Asset:

`templates/general-operating-contract.md`

| Dimension | Score | Static evidence |
|---|---:|---|
| Reuse breadth | 2 | The template is domain-neutral and can map to prompts, forms, JSON/YAML contracts, tickets, ADRs, agent/tool invocations, and Generator inputs. |
| Parameterization | 2 | Required/optional inputs, allowed context, source classes, evidence labels/threshold, must/must-not rules, decision states, output contract, and verification are explicit configuration points. |
| Governance | 2 | It defines evidence promotion rules, context boundaries, decision/escalation states, forbidden assumptions, and fallback behavior. |
| Verification | 2 | `VERIFICATION CONTRACT` defines contract checks and explicit pass/fail states. |
| Adaptation speed | 2 | `ADAPTATION MAP` identifies exactly which policy surfaces to configure; `methodology/adaptation-playbook.md` explains policy vs instance data. |
| Integration value | 2 | Explicit mappings exist for prompt, form, JSON/YAML, ticket, ADR, agent/tool, and Prompt Quarry Generator representations. |
| Inspectability | 2 | Inputs, evidence policy, process, states, output contract, unknowns, and verification are all externally visible interfaces. |

Total:

```text
14 / 14 — PASS
```

Free prompt clone challenge:

A finished Free prompt can be edited into another finished prompt, but it does not expose this general task-independent construction interface as first-class reusable policy. Replacing nouns in a Free prompt does not reproduce the operating-contract abstraction.

## 2. Software Code Review System

Asset:

`templates/software-code-review-system.md`

| Dimension | Score | Static evidence |
|---|---:|---|
| Reuse breadth | 2 | The system supports PRs, diffs, files, modules, multiple languages/repos, human review, CI gates, agents, and security/reliability variants through configurable lenses. |
| Parameterization | 2 | Review lenses, evidence/reporting threshold, minimum severity, max findings, severity rubric, ship authority, ship states, and transition rules are explicit. |
| Governance | 2 | `CONFIRMED / LIKELY / QUESTION / DISMISSED`, candidate-finding challenge rules, no-invented-test rule, severity semantics, and ship transition policy are explicit. |
| Verification | 2 | Every finding requires evidence, failure mechanism, fix and verification; the system also has a `VERIFICATION CONTRACT` and local review-contract states. |
| Adaptation speed | 2 | `TEAM ADAPTATION MAP` plus `methodology/adaptation-playbook.md` turns team policy into named configuration instead of requiring a rewrite. |
| Integration value | 2 | Explicit integration shapes include PR instructions, contribution guides, CI review gates, code-review agents, issue generation, security prechecks, and Generator configuration. |
| Inspectability | 2 | Another engineer can inspect enabled lenses, thresholds, authority, severity policy, accepted findings, missing context, and ship transitions. |

Total:

```text
14 / 14 — PASS
```

Free prompt clone challenge:

The Free Code Review prompt provides a strong default review. The Paid system adds configurable review policy and reusable team semantics. The worked example `examples/code-review-policy-transformation.md` demonstrates that distinction by converting a vague PR request into a stable review contract.

## 3. Technical Research / Decision System

Asset:

`templates/technical-research-decision-system.md`

| Dimension | Score | Static evidence |
|---|---:|---|
| Reuse breadth | 2 | The system covers architecture, build-vs-buy, vendor, dependency, migration, platform, tooling, procurement, RFC, and ADR decisions. |
| Parameterization | 2 | Hard constraints, weighted criteria, allowed evidence classes, freshness, citation policy, evidence quality threshold, decision states, and reversal policy are configurable. |
| Governance | 2 | Hard constraints precede scoring; source claims/inference/assumptions remain separated; evidence-quality rules control `DECIDE`; `HOLD`/`REJECT_ALL` prevent forced winners. |
| Verification | 2 | `VERIFICATION CONTRACT` checks shared criteria, source/freshness state, evidence quality, decision transitions, reversal triggers, and validation actions. |
| Adaptation speed | 2 | `ADAPTATION MAP` exposes decision type, constraints, criteria, source policy, freshness, evidence threshold and triggers; the playbook explains how to configure them. |
| Integration value | 2 | Explicit mappings exist for ADRs, architecture review, vendor evaluation, dependency selection, migration planning, procurement, RFCs, and Generator configuration. |
| Inspectability | 2 | Constraint ledger, option viability, evidence ledger, comparative analysis, assumptions, decision state, reversal triggers, and next validation action are all explicit. |

Total:

```text
14 / 14 — PASS
```

Free prompt clone challenge:

The Free Technical Decision prompt provides a strong default comparison workflow. The Paid system adds a reusable team decision policy with source/freshness configuration, evidence-quality thresholds, option viability states, reusable transitions, and integration semantics. `examples/technical-decision-policy-transformation.md` demonstrates this on a database architecture decision.

---

## Pack-level blocking tests

### Free prompt clone test — PASS

Evidence:

- three reusable system templates expose policy surfaces rather than only finished prompts;
- `contracts/workflow-contract.schema.json` represents the operating interface in machine-readable form;
- the adaptation playbook separates reusable policy from per-run instance data.

A noun substitution on any Free prompt does not reproduce those capabilities.

### Worked transformation test — PASS

Evidence:

- `examples/code-review-policy-transformation.md`:
  `vague request → requirements → configured policy → operating prompt → inspection`;
- `examples/technical-decision-policy-transformation.md`:
  `vague database question → decision requirements → evidence/decision policy → operating prompt → inspection`.

These are policy transformations, not cosmetic before/after rewrites.

### Team adaptation test — PASS

Evidence:

- `methodology/adaptation-playbook.md` classifies fields as `INVARIANT`, `POLICY`, `INSTANCE_INPUT`, `OPTIONAL_CONTEXT`, and `DERIVED`;
- specialized templates include explicit adaptation maps;
- the code-review worked transformation shows a team-specific severity/evidence/ship policy.

### Machine/repeatable boundary test — PASS

Evidence:

- `contracts/workflow-contract.schema.json` is JSON Schema draft 2020-12;
- `contracts/code-review-policy.example.json` instantiates stable inputs, context, evidence, process, decision, output, verification and fallback semantics;
- `QUICKSTART.md` explains when machine-readable representation is useful.

### Customer value statement test — PASS

The current assets support the statement:

> The Free Pack gives me three strong prompts. Developer Pack gives me the construction and governance system I can reuse to build many of my own workflows.

The distinction is visible in templates, machine contracts, adaptation methodology, static review tooling, and worked transformations rather than being asserted only in sales copy.

---

## Gate result

```text
general_operating_contract       14 / 14  PASS
software_code_review_system      14 / 14  PASS
technical_decision_system        14 / 14  PASS

free_prompt_clone_test           PASS
worked_transformation_test       PASS
team_adaptation_test             PASS
machine_repeatable_boundary      PASS
customer_value_statement         PASS

COMMERCIAL_VALUE_GATE            PASS
inspection_mode                  MANUAL_STATIC
```

## What this PASS means

The current Developer Pack v1.1 architecture has a defensible static customer-value distinction from the Free Starter Pack.

## What this PASS does not mean

It does not authorize sale.

Current product state remains:

```text
package_state    DRAFT
sale_status      NOT_FOR_SALE
CI_PASS          NOT_OBSERVED
F4_TESTED        NO
F5_IMPROVED      NO
F6_CERTIFIED     NO
F7_PORTABLE      NO
```

Before release candidate, the intended customer inventory still needs to be frozen, the static guard must execute successfully in a real environment, deterministic packaging must create a new candidate fingerprint, distribution approval must bind to that exact candidate, and delivery must be reconciled with the governed source.
