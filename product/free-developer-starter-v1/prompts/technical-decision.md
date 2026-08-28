# Technical Decision — Starter Prompt

## CONTEXT

Decision to make:

[DESCRIBE THE TECHNICAL DECISION]

Options:

[OPTION A / OPTION B / OTHER OPTIONS]

Constraints and priorities:

[BUDGET / TEAM / SCALE / SECURITY / DELIVERY TIME / OPERATIONS / OTHER]

Known evidence:

[MEASUREMENTS / DOCUMENTATION / EXPERIENCE / REQUIREMENTS]

## TASK

Compare the options against the stated constraints and recommend a decision only to the extent supported by the evidence.

## RULES

- Make decision criteria explicit before scoring options.
- Separate supplied facts from assumptions.
- Do not hide meaningful trade-offs behind a single score.
- State where missing evidence could change the recommendation.
- Prefer the simplest option that satisfies the actual constraints; do not reward complexity by default.
- If two options are effectively tied, explain what experiment or information would break the tie.

## OUTPUT

Return:

1. **Decision criteria** and relative importance.
2. **Option comparison** with strengths, weaknesses, and operational consequences.
3. **Recommendation** with rationale.
4. **Key assumptions and uncertainties**.
5. **Reversal triggers** — conditions under which the decision should be revisited.
6. **Next validation step** — the cheapest useful check before committing deeply.

Do not present uncertain or missing evidence as established fact.
