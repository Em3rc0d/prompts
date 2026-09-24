# Design an Implementation Plan

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when requirements are sufficiently understood and you need a staged implementation plan before coding.

## Prompt

```text
OBJECTIVE / REQUIREMENTS
{{requirements}}

CURRENT SYSTEM / CONSTRAINTS
{{architecture_stack_constraints_or_unknown}}

KNOWN RISKS
{{risks_or_none}}

DELIVERY BOUNDARY
{{what_is_in_and_out}}

RULES
- Do not invent requirements, dependencies, integrations, or production constraints.
- Separate facts about the current system from proposed design choices.
- Prefer the smallest implementation path that satisfies the stated requirements.
- Expose sequencing dependencies and irreversible decisions early.
- Do not begin implementation in the answer.
- Mark decisions that still require evidence or stakeholder input.

PROCESS
1. Restate scope and success criteria.
2. Map affected components, data, interfaces, and operational surfaces.
3. Identify decisions that must be closed before build.
4. Sequence implementation into dependency-aware increments.
5. Attach verification to each increment.
6. Identify rollback, migration, or compatibility concerns.
7. Classify implementation readiness.

OUTPUT
1. Scope and acceptance boundary.
2. Affected system map.
3. Open design decisions.
4. Implementation sequence with dependencies.
5. Verification per stage.
6. Risks / rollback considerations.
7. Readiness state: READY_TO_BUILD / READY_WITH_OPEN_DECISIONS / NOT_READY.

VERIFICATION
Every implementation step must trace to a stated requirement or clearly labeled technical proposal.
```
