# Review a Technical Design

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a proposed technical design needs a structured review before implementation.

## Prompt

```text
DESIGN
{{design_document_or_proposal}}

REQUIREMENTS / CONSTRAINTS
{{requirements_constraints}}

CURRENT SYSTEM
{{current_architecture_or_unknown}}

REVIEW FOCUS
{{reliability_security_scalability_maintainability_cost_other}}

RULES
- Evaluate the design against supplied requirements and constraints, not generic preferences.
- Separate correctness risks from style preferences and optional improvements.
- Do not invent traffic, data sensitivity, SLAs, dependencies, or organizational constraints.
- Identify hidden coupling, unowned state, migration risk, failure modes, and operational burden when visible.
- Treat missing context as an uncertainty, not as evidence of a flaw.
- Prefer concrete change recommendations tied to material risk.

PROCESS
1. Reconstruct the design intent and invariants.
2. Trace each major component and interface to requirements.
3. Inspect data/state ownership and failure paths.
4. Review the requested quality attributes.
5. Identify assumptions and missing evidence.
6. Classify findings by materiality.
7. Determine review state.

OUTPUT
1. Design intent and scope.
2. What is well-supported by the current design.
3. Material findings with evidence and consequence.
4. Assumptions / unknowns.
5. Required changes before implementation.
6. Optional improvements.
7. Review state: READY / READY_WITH_CHANGES / NEEDS_REDESIGN / INCONCLUSIVE.

VERIFICATION
Every material finding must point to a specific design element, requirement, missing invariant, or failure path.
```
