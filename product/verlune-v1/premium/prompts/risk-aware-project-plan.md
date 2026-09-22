# Risk-Aware Project Plan

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a project needs sequencing, dependencies, uncertainty reduction, and explicit go/no-go gates.

## Prompt

```text
Build a project plan that exposes assumptions and reduces the highest risks before expensive execution.

PROJECT
{{project}}

TARGET OUTCOME
{{outcome}}

CURRENT STATE
{{current_state}}

DEADLINE / WINDOW
{{deadline_or_none}}

RESOURCES
{{people_budget_tools_time}}

CONSTRAINTS
{{constraints}}

KNOWN DEPENDENCIES
{{dependencies_or_unknown}}

RULES
- Do not invent resources, approvals, delivery dates, dependencies, or stakeholder commitments.
- Separate confirmed dependencies from assumed ones.
- Prioritize risk-reducing evidence before irreversible work.
- Define completion with observable artifacts or outcomes.
- Identify decisions that must be closed before implementation.
- Do not turn every uncertainty into a blocker; distinguish material from non-material unknowns.

PROCESS
1. Define completion criteria.
2. Map major workstreams.
3. Map dependencies.
4. Identify assumptions.
5. Identify technical, operational, commercial, schedule, and external risks where relevant.
6. Rank risks by impact and uncertainty, not dramatic wording.
7. Design early validation gates.
8. Sequence milestones.
9. Define owner/input/output for near-term actions.
10. Define conditions for re-planning.

OUTPUT
1. Outcome and scope.
2. Known / assumed / unknown.
3. Dependency map.
4. Risk register.
5. Validation gates.
6. Milestones.
7. First 10 executable actions.
8. Decisions required.
9. Re-plan triggers.
10. Current project state: READY / READY_WITH_RISKS / VALIDATE_FIRST / BLOCKED.

VERIFICATION
Every blocking dependency or risk must explain what evidence makes it blocking.
```
