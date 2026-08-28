# 5-minute Quickstart

## 1. State the task

Write one sentence describing the outcome you want and identify the material the model may rely on.

## 2. Choose a template

- Software/code review: `templates/software-code-review.md`
- Technical research/decision: `templates/technical-research-decision.md`
- General structured work: `templates/general-structured-prompt.md`

## 3. Fill the contract

Replace every `[VARIABLE]`. Delete sections that do not apply. Never leave an instruction ambiguous if it affects correctness, safety, or output shape.

## 4. Run the static gate

Use `checklists/static-quality.md`. A prompt should not ship with undefined inputs, contradictory constraints, unsupported certainty, or an unspecified output contract.

## 5. Execute and observe

Run the prompt in your actual target runtime. Keep static validation separate from behavioral observation.

A clean static result may justify `VALID`. It does not establish `TESTED`, `IMPROVED`, `CERTIFIED`, or `PORTABLE`.

## 6. Iterate from evidence

When a failure appears, record the failure mode, change one meaningful design element, and compare behavior using the same task conditions whenever possible.
