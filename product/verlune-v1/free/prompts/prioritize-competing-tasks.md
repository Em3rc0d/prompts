# Prioritize Competing Tasks

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when several tasks compete for limited time and you need a transparent order rather than a vague priority list.

## Prompt

```text
TASKS
{{tasks}}

DEADLINES / TIME WINDOWS
{{deadlines_or_none}}

HARD CONSTRAINTS
{{constraints_or_none}}

DEPENDENCIES
{{dependencies_or_unknown}}

WHAT MATTERS MOST
{{outcome_or_priority_criteria}}

RULES
- Do not invent urgency, deadlines, effort estimates, dependencies, or business value.
- Separate hard constraints from preferences.
- Identify tasks that unblock other work.
- Surface missing information that could materially change the order.
- Prefer reversible low-cost progress when priorities are otherwise close.
- Do not pretend precision when effort or impact is unknown.

OUTPUT
1. Hard constraints and blockers.
2. Priority order with a short reason for each item.
3. Tasks that can be deferred safely.
4. Unknowns that could change the order.
5. Recommended first action.
6. A simple rule for re-prioritizing when new work appears.

VERIFICATION
Check that every ranking reason uses supplied constraints/criteria or is labeled as an assumption.
```
