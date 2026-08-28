# 5-minute Quickstart

## 1. State the task

Write one sentence describing the outcome you want and identify the material the model may rely on.

If you want a machine-readable starting point, copy `contracts/prompt-request.example.json` or `contracts/task-brief.example.json`.

## 2. Choose a template

- Software/code review: `templates/software-code-review.md`
- Technical research/decision: `templates/technical-research-decision.md`
- General structured work: `templates/general-structured-prompt.md`

If you want to see the full transformation first, open:
- `examples/software-code-review/README.md`
- `examples/technical-research-decision/README.md`

## 3. Fill the contract

Replace every `[VARIABLE]`. Delete sections that do not apply. Never leave an instruction ambiguous if it affects correctness, safety, or output shape.

For architecture guidance, use `methodology/architecture.md`.

## 4. Run the static gate

Use `checklists/static-quality.md`. A prompt should not ship with undefined inputs, contradictory constraints, unsupported certainty, or an unspecified output contract.

A clean static result may justify `VALID`. It does not establish `TESTED`, `IMPROVED`, `CERTIFIED`, or `PORTABLE`. See `methodology/evidence-states.md`.

## 5. Execute and observe

Run the prompt in your actual target runtime. Keep static validation separate from behavioral observation.

Use `methodology/evaluation.md` to record runtime conditions, observed outputs, criteria, and failure modes without converting expectations into evidence.

## 6. Iterate from evidence

When a failure appears, record the failure mode, change one meaningful design element, and compare behavior using the same task conditions whenever possible.
