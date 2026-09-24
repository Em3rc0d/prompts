# Prioritize a Portfolio of Work

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when multiple projects or initiatives compete for resources and dependencies make simple ranking misleading.

## Prompt

```text
INITIATIVES
{{initiatives}}

STRATEGIC OUTCOMES
{{outcomes}}

HARD CONSTRAINTS
{{constraints}}

DEPENDENCIES
{{dependencies}}

CAPACITY / TIME WINDOW
{{capacity_or_unknown}}

EVIDENCE
{{evidence_or_none}}

RULES
- Do not invent effort, ROI, urgency, dependencies, or strategic importance.
- Separate must-do commitments from discretionary initiatives.
- Model dependency and sequencing effects before scoring.
- Do not hide incompatible priorities inside an average score.
- Prefer explicit hold/kill states over pretending everything can proceed.
- Surface where missing evidence prevents prioritization.

PROCESS
1. Normalize initiatives and outcomes.
2. Apply hard constraints.
3. Map dependencies and shared bottlenecks.
4. Evaluate strategic contribution and evidence.
5. Identify conflicts, sequencing options, and capacity limits.
6. Classify proceed / hold / stop / evidence-needed.
7. Define re-prioritization triggers.

OUTPUT
1. Portfolio map.
2. Constraint and dependency analysis.
3. Priority sequence.
4. Proceed / hold / stop / evidence-needed states.
5. Capacity conflicts.
6. Unknowns that could change order.
7. Re-prioritization triggers.

VERIFICATION
Every priority must be explainable through supplied constraints, dependencies, and outcomes rather than an opaque score.
```
