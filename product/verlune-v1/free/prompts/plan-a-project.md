# Plan a Project

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when you know the outcome you want but need a realistic path from start to finish.

## Prompt

```text
Turn this project into an executable plan.

PROJECT
{{project}}

DESIRED OUTCOME
{{definition_of_success}}

DEADLINE
{{deadline_or_none}}

RESOURCES
{{people_budget_tools_time_or_unknown}}

CONSTRAINTS
{{constraints_or_none}}

CURRENT STATE
{{what_already_exists}}

RULES
- Do not invent resources, approvals, dependencies, or dates.
- Identify unknowns that can change the plan.
- Put dependencies before dependent work.
- Prefer small verifiable milestones over vague phases.
- Distinguish must-have work from optional work.
- Identify the highest-risk assumptions early.

OUTPUT
1. Outcome and completion criteria.
2. Assumptions / unknowns.
3. Milestones in dependency order.
4. Concrete next actions.
5. Risks and early validations.
6. What can wait.
7. First checkpoint and evidence of completion.

If the goal is not defined well enough to plan, ask only the minimum questions needed.
```
