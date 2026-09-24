# Analyze a Business Problem

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when a business symptom needs to be separated from assumptions before choosing an action.

## Prompt

```text
Help me analyze this business problem without jumping to a solution too early.

PROBLEM / SYMPTOM
{{what_is_happening}}

DESIRED OUTCOME
{{what_should_be_happening}}

KNOWN FACTS
{{data_observations_feedback_or_none}}

CONSTRAINTS
{{budget_time_people_rules_or_none}}

RULES
- Separate observations from interpretations.
- Do not invent market data, customer behavior, revenue, costs, or causes.
- Identify multiple plausible causes when the evidence does not support one.
- Prefer checks that can distinguish between causes.
- Respect the stated constraints.
- Do not recommend a large irreversible action when a smaller validation can answer the key uncertainty.

OUTPUT
1. Problem definition.
2. Facts vs assumptions.
3. Most plausible explanations, with reasoning.
4. Missing information that could change the analysis.
5. Smallest useful validation actions.
6. Options available now.
7. Recommended next step and why.

If evidence is too weak for a recommendation, return NEED_MORE_EVIDENCE and state exactly what to collect.
```
