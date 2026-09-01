# MK1 Prompt Generator v0

> **Principle:** MK0 teaches. MK1 creates. F5 proves.

## Purpose

MK1 Prompt Generator v0 is the design-time orchestrator that turns a user/task request into a new Prompt Quarry engineered prompt candidate while preserving a strict truth boundary between source observation, MK0-derived knowledge, and MK1-created artifacts.

It does **not** copy a source prompt body and it does **not** promote generated output beyond static validity.

## Pipeline

```text
request
  ↓
classify
  ↓
retrieve MK0 knowledge
  ↓
select techniques + architecture
  ↓
compose candidate
  ↓
F1 lint + F3 critic
  ↓
output prompt bundle
  ↓
F4 behavioral testing
  ↓
F5 proof against fair baselines
```

## Product boundary

This generator belongs to MK1 because it is an explicitly invoked **design-time forge**. It takes a declared request and deterministically produces a candidate for the existing MK1 quality ladder.

MK2 remains responsible for autonomous/runtime behavior such as continuously detecting tasks, deciding whether/when to generate, adaptive retrieval, online prompt routing, self-updating selection policies, and autonomous experiment loops.

```text
MK1: request → forge candidate
MK2: runtime → autonomously decide/retrieve/forge/route/adapt
```

## Classification

v0 classification is deterministic and heuristic. It infers:

- intent;
- domain;
- risk;
- complexity;
- interaction mode;
- language;
- default input contract;
- default output needs.

Every inferred field can be overridden explicitly in `PROMPT_GENERATOR_REQUEST.schema.json`.

A heuristic classification is not evidence about the external world. It is only a task-design decision.

## MK0 retrieval

The generator reads characterized MK0 knowledge, currently including:

- `mk0/MANIFEST.json`;
- `mk0/analysis/alpacka-ai-free-technique-matrix.json`;
- `mk0/golden-dataset/alpacka-free-golden-fixtures-manifest.json`;
- selected repository-authored MK0 patterns when the architecture warrants them.

The retrieval layer returns aggregate/structural knowledge and fingerprints. It does not treat raw bodies as a hidden template library.

### Critical rule

**Technique frequency is evidence, not an instruction.**

A technique is selected because task/risk/output requirements justify it. MK0 frequency and Golden Dataset coverage annotate that decision; they do not automatically add prompt sections.

This prevents “popular technique = always include it” overfitting.

## Composition

The generator reuses the existing MK1 contracts:

- F1 architecture selector;
- F2 candidate assembler;
- prompt artifact schema;
- structural linter;
- F3 static critic.

Generated artifacts remain provenance-bound to the exact MK0 knowledge snapshot through SHA-256 fingerprints.

## Output bundle

A successful generation writes:

```text
request.json
classification.json
task-brief.json
mk0-retrieval.json
technique-selection.json
architecture.json
artifact.json
lint.json
critic.json
evaluation-plan.json
prompt.txt
generation.json
```

`prompt.txt` is the human/operator-facing prompt. The JSON files are the machine-readable lineage required to reproduce why it was generated.

## State boundary

The generator may produce a statically valid artifact, but it cannot make behavioral claims.

```text
GENERATED
  ↓ static schema/lint/critic
VALID_STATIC
  ↓ F4 real behavioral evidence
TESTED
  ↓ F5 paired/blind baseline evidence
CANDIDATE / IMPROVED
  ↓ F6 repeated same-runtime F5 evidence
CERTIFIED
```

`VALID_STATIC != TESTED`.

`generator_status` is one of:

- `VALID_STATIC` — linter PASS, critic PASS;
- `WARN_STATIC` — linter PASS, critic WARN;
- `REJECTED_STATIC` — structural or critic failure.

The underlying artifact state remains governed by the canonical MK1 artifact lifecycle.

## F5 proof strategy

The generator records the intended proof contract but does not fabricate F5 evidence.

### Baseline A — required

`task-equivalent-minimal`

Purpose: prove that the engineered candidate adds material value over a fair minimal prompt for the exact same task.

### Baseline B — optional stronger benchmark

`best-comparable-mk0`

Purpose: when a genuinely task-equivalent MK0 prompt has exact observed source-body provenance and a valid reuse/evaluation contract, compare the new candidate against that prompt as an additional benchmark.

Guardrails:

- do not compare against an unrelated MK0 prompt;
- do not reconstruct unavailable premium/source bodies and label them observed;
- do not let Baseline B replace Baseline A;
- use the same task, fixtures, runtime and blind evaluation contract.

This yields the intended evidence logic:

```text
Candidate > Baseline A
    proves engineering adds value over minimal prompting

Candidate > Baseline B
    optionally proves the forge can outperform a comparable prompt from the knowledge quarry
```

## CLI

```bash
python tools/mk1_prompt_generator_v0.py \
  mk1/generator/examples/software-review.request.json \
  --output-dir /tmp/pq-generator-demo
```

The command exits non-zero only when the generated candidate is statically rejected.

## Non-claims

Generator v0 does not claim:

- semantic classification is universally correct;
- MK0 contains the best prompt for every task;
- the generated prompt is behaviorally better;
- the generated prompt is certified;
- the generated prompt is portable.

Those claims require the corresponding evidence gates.
