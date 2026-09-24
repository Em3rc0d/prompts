# SOP Drafting

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use to turn a real recurring process into an executable Standard Operating Procedure.

## Prompt

```text
Turn the process described below into an operational SOP that another person can follow without inventing missing policy.

PROCESS
{{process_description_notes_current_steps}}

OUTCOME
{{what_success_looks_like}}

ROLES
{{people_or_roles_involved}}

INPUTS / SYSTEMS
{{documents_tools_systems_or_none}}

CONSTRAINTS / POLICIES
{{rules_approvals_limits_or_none}}

KNOWN EXCEPTIONS
{{exceptions_or_none}}

RULES
- Preserve the actual process and stated policy.
- Do not invent approvals, permissions, legal requirements, SLAs, system capabilities, or responsibilities.
- Separate policy decisions from procedural steps.
- Identify missing information that could make the SOP unsafe or unusable.
- Make handoffs and ownership explicit.
- Include observable completion criteria.

PROCESS
1. Define trigger and completion state.
2. Identify prerequisites.
3. Normalize roles and ownership.
4. Order steps by dependency.
5. Define decision points.
6. Define exception/escalation behavior.
7. Define evidence/records of completion.
8. Identify unresolved policy questions.

OUTPUT
1. SOP title / purpose.
2. Scope.
3. Roles.
4. Preconditions / required inputs.
5. Procedure with numbered steps.
6. Decision points.
7. Exceptions / escalation.
8. Required records / evidence.
9. Completion criteria.
10. Open policy questions.
11. Revision risks: what future process changes would invalidate this SOP.

VERIFICATION
Check that a step requiring authority names the responsible role or is marked unresolved.
```
