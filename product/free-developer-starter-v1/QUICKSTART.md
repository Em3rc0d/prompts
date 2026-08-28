# Quickstart

1. Choose the prompt closest to your task in `prompts/`.
2. Replace every bracketed placeholder with concrete context.
3. Provide the smallest useful evidence set: code, errors, constraints, versions, or decision criteria.
4. Ask the model to distinguish observed facts from assumptions.
5. Review the answer before applying changes to production systems.

## Recommended flow

`CONTEXT → EVIDENCE → CONSTRAINTS → TASK → OUTPUT`

Do not add context merely to make a prompt longer. Add information only when it can change the answer.

## Evidence boundary

A well-structured prompt can reduce ambiguity, but structure alone does not prove runtime superiority. These Starter Pack prompts should not be described as `TESTED`, `IMPROVED`, `CERTIFIED`, or `PORTABLE` without the corresponding Prompt Quarry evidence.

## Want the full system?

Developer Pack v1 adds reusable prompt architecture, machine-readable task/request contracts, methodology, examples, quality checklists, and explicit evidence-state guidance.
