# Prepare a Career Decision Brief

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when comparing career options such as roles, offers, paths, or learning investments against explicit personal criteria.

## Prompt

```text
DECISION
{{career_decision}}

OPTIONS
{{options}}

MY CRITERIA
{{criteria}}

KNOWN FACTS
{{facts}}

UNCERTAINTIES
{{unknowns}}

TIME / REVERSIBILITY
{{timing_and_reversibility}}

RULES
- Use only the user's stated priorities and supplied facts.
- Do not invent salary, culture, promotion probability, job stability, or future demand.
- Separate hard constraints from preferences.
- Show when an option is attractive only under an uncertain assumption.
- Do not force a recommendation when key evidence is missing.
- Prefer reversible information-gathering steps when uncertainty is material.

PROCESS
1. Normalize the decision and criteria.
2. Classify hard constraints vs preferences.
3. Map facts and unknowns per option.
4. Evaluate tradeoffs and reversibility.
5. Identify assumptions that drive the outcome.
6. Determine what evidence would most change the decision.
7. Produce a bounded decision state.

OUTPUT
1. Decision frame.
2. Criteria and constraints.
3. Option comparison.
4. Key tradeoffs.
5. Assumptions / unknowns.
6. Decision state: DECIDABLE / NEEDS_EVIDENCE / EXPERIMENT_FIRST / NO_VALID_OPTION.
7. Next evidence-gathering action.

VERIFICATION
Every comparison must use the user's stated criteria and supplied facts; uncertainty must remain visible.
```
