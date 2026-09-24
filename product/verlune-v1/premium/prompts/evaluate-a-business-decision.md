# Evaluate a Business Decision

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a bounded business choice needs explicit criteria, tradeoffs, and uncertainty before commitment.

## Prompt

```text
DECISION
{{decision}}

OPTIONS
{{options}}

HARD CONSTRAINTS
{{constraints}}

EVIDENCE
{{evidence_or_none}}

DECISION CRITERIA
{{criteria_or_unknown}}

REVERSIBILITY / DEADLINE
{{reversibility_and_timing_or_unknown}}

RULES
- Do not invent weights, costs, probabilities, market facts, or stakeholder preferences.
- Separate must-pass constraints from scored preferences.
- Show how each conclusion depends on evidence and criteria.
- Do not force a winner when evidence is insufficient.
- Identify reversible experiments when uncertainty is high.
- Surface criteria conflicts rather than averaging them away.

PROCESS
1. Normalize the decision and constraints.
2. Classify must-pass vs preference criteria.
3. Map evidence to each option.
4. Evaluate tradeoffs and uncertainty.
5. Check reversibility and downside.
6. Identify missing evidence that could change the choice.
7. Define decision or experiment state.

OUTPUT
1. Decision frame.
2. Constraint screen.
3. Option/criteria matrix.
4. Tradeoffs and uncertainty.
5. Reversibility / downside notes.
6. Decision state: DECIDABLE / EXPERIMENT_FIRST / NEEDS_EVIDENCE / NO_VALID_OPTION.
7. Next action.

VERIFICATION
Every option judgment must trace to an explicit criterion and supplied evidence or be labeled uncertain.
```
