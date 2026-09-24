# Document a Business Process

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when a recurring business process already exists and you need to capture it clearly without redesigning it.

## Prompt

```text
PROCESS NAME
{{process_name}}

HOW IT CURRENTLY WORKS
{{notes_steps_messages_or_observations}}

PEOPLE / ROLES INVOLVED
{{roles_or_unknown}}

KNOWN RULES / CONSTRAINTS
{{rules_or_none}}

KNOWN EXCEPTIONS
{{exceptions_or_none}}

RULES
- Document the process as described before suggesting improvements.
- Separate observed steps from assumptions about what should happen.
- Do not invent approvals, policies, owners, systems, SLAs, or exceptions.
- Identify unclear handoffs, missing inputs, and undefined outcomes.
- Use role names rather than inventing specific people.
- If different versions of the process conflict, preserve the conflict as an open point.

OUTPUT
1. Purpose and trigger.
2. Inputs required.
3. Current steps in order.
4. Roles and handoffs.
5. Decision points / exceptions that are explicitly known.
6. Outputs / completion condition.
7. Open questions or undocumented rules.

VERIFICATION
Check that every documented step is supported by the supplied process description or clearly labeled as an open question.
```
