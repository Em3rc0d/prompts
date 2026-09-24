# Design an Operational Process

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a recurring business outcome needs a clear process with roles, states, handoffs, and controls.

## Prompt

```text
OUTCOME
{{desired_outcome}}

CURRENT PROCESS / CONTEXT
{{current_process_or_none}}

ROLES / SYSTEMS
{{roles_and_systems}}

CONSTRAINTS / POLICIES
{{constraints_or_unknown}}

KNOWN EXCEPTIONS
{{exceptions_or_none}}

RULES
- Design only from stated objectives, constraints, and known operating context.
- Separate existing policy from proposed process design.
- Do not invent authority, approvals, SLAs, controls, or system capabilities.
- Make ownership and handoffs explicit.
- Include blocked, exception, and rework paths where they materially affect the process.
- Prefer observable completion criteria over vague states such as done or reviewed.

PROCESS
1. Define trigger, outcome, and boundaries.
2. Identify actors, systems, inputs, and outputs.
3. Design the happy path.
4. Add decision, exception, blocked, and escalation states.
5. Define ownership and handoffs.
6. Attach controls and verification to material states.
7. Identify open policy or system decisions.

OUTPUT
1. Process objective and scope.
2. Roles / systems.
3. State and step flow.
4. Decision / exception rules.
5. Handoffs and ownership.
6. Controls / verification.
7. Open decisions and implementation risks.

VERIFICATION
Every rule or control must be either supplied as an existing constraint or clearly labeled as proposed.
```
