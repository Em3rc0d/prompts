# Research Decision Brief

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when research needs to become a concise decision input without hiding uncertainty or overstating evidence.

## Prompt

```text
DECISION
{{decision}}

RESEARCH / SOURCES
{{research}}

OPTIONS
{{options_or_unknown}}

CONSTRAINTS
{{constraints}}

DECISION MAKER
{{audience}}

RULES
- Separate research findings from decision criteria and recommendation logic.
- Do not convert weak or indirect evidence into certainty.
- Preserve material disagreement and unknowns.
- Distinguish reversible and irreversible consequences where relevant.
- Do not invent stakeholder preferences, costs, or probabilities.
- Make the brief useful even when the correct decision remains unresolved.

PROCESS
1. Normalize the decision and hard constraints.
2. Extract the findings that materially affect the decision.
3. Map findings to options.
4. Identify tradeoffs and unknowns.
5. Determine what can be concluded now.
6. Define the minimum additional evidence that could change the decision.

OUTPUT
1. Decision statement.
2. Executive evidence summary.
3. Option/evidence matrix.
4. Tradeoffs and constraints.
5. Unknowns and sensitivity.
6. Decision implication or bounded recommendation if supported.
7. Next evidence trigger.

VERIFICATION
Every decision implication must trace to a stated criterion plus supported evidence.
```
