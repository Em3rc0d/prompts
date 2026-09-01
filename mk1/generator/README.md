# MK1 Prompt Generator

> **MK0 teaches. MK1 creates. F5 proves.**

This directory contains operator-facing inputs and examples for the Prompt Quarry MK1 design-time forge.

## v0 flow

```text
request
  ↓
classify
  ↓
retrieve MK0 knowledge
  ↓
select techniques
  ↓
compose architecture
  ↓
assemble candidate
  ↓
F1 lint + F3 critic
  ↓
output prompt bundle
```

The generator creates a new Prompt Quarry artifact from a task request and MK0-derived knowledge. It does not copy observed prompt bodies as templates and it does not claim runtime superiority.

## Run

```bash
python tools/mk1_prompt_generator_v0.py \
  mk1/generator/examples/software-review.request.json \
  --output-dir /tmp/pq-generator-demo
```

## Minimum request

```json
{
  "request_id": "my_prompt_001",
  "request": "Create a prompt that reviews a software change and reports evidence-bound findings."
}
```

The v0 classifier infers intent, domain, risk, complexity, language, interaction, inputs and output needs. Any of those fields may be explicitly supplied through `mk1/specs/PROMPT_GENERATOR_REQUEST.schema.json` when deterministic operator control is preferred.

## Output

A generation bundle contains:

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

`prompt.txt` is the prompt intended for human/operator use. The JSON files preserve why it was created and which MK0 knowledge snapshot informed the design.

## Knowledge policy

MK0 technique frequency is evidence, not an inclusion rule.

```text
wrong:
  technique is frequent in MK0 → always include it

right:
  task contract requires technique
      + MK0 says whether/how strongly it was observed
      + Golden Dataset says whether the technique is structurally covered
```

The objective is the smallest architecture justified by the task, not the largest prompt possible.

## Evaluation

Generation is only the beginning:

```text
VALID_STATIC
  ↓ F4 real behavioral execution
TESTED
  ↓ F5 paired/blind comparison
CANDIDATE / IMPROVED
  ↓ F6 repeated same-runtime proof
CERTIFIED
```

F5 uses a required task-equivalent minimal baseline. A genuinely comparable observed MK0 prompt may be used as an additional stronger baseline only when exact source-body provenance supports that comparison.

## Boundary with MK2

MK1 generates when explicitly asked to forge a prompt.

MK2 will own autonomous runtime behavior: detecting tasks, deciding when to generate, adaptive retrieval, prompt routing, online experimentation and self-updating policies.
