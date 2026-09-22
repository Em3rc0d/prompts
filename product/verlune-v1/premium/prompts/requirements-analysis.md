# Requirements Analysis

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a feature, project, process, or request needs to become implementation-ready requirements.

## Prompt

```text
Analyze the request below and turn it into an explicit requirements model without inventing missing business decisions.

REQUEST / SOURCE MATERIAL
{{request}}

CONTEXT
{{product_process_system_or_domain_context}}

KNOWN CONSTRAINTS
{{constraints_or_none}}

INTENDED CONSUMER
{{engineer_designer_vendor_team_other}}

RULES
- Preserve the stated objective.
- Separate explicit requirements from inferred requirements.
- Never convert an inference into a requirement without labeling it.
- Detect contradictions, ambiguous terms, hidden dependencies, undefined actors, missing states, and unverifiable acceptance criteria.
- Ask only questions that can materially change scope, behavior, data, authority, integration, or acceptance.
- Do not design implementation details unless they are required by a stated constraint.
- Distinguish MUST, SHOULD, COULD, and UNKNOWN where useful.

PROCESS
1. Reconstruct objective and actors.
2. Extract explicit functional requirements.
3. Extract explicit non-functional constraints.
4. Identify domain/data entities and important states.
5. Identify dependencies and integrations.
6. Detect contradictions and ambiguities.
7. Identify missing decisions.
8. Convert verifiable behavior into acceptance criteria.
9. Classify readiness.

READINESS STATES
- READY_FOR_DESIGN
- READY_WITH_OPEN_QUESTIONS
- NEEDS_CLARIFICATION
- OUT_OF_SCOPE_OR_UNSUPPORTED

OUTPUT
1. Objective and scope.
2. Actors / consumers.
3. Functional requirements.
4. Non-functional requirements.
5. Constraints / invariants.
6. Data/state implications.
7. Dependencies / integrations.
8. Ambiguities and contradictions.
9. Open questions ranked by impact.
10. Acceptance criteria.
11. Readiness state and next action.

VERIFICATION
Check that every requirement traces to supplied material or is explicitly labeled inferred/proposed.
```
