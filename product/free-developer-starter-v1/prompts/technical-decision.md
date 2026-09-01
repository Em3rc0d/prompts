# Technical Decision — Starter Prompt

Use this when you need to choose between technical options without turning preference into evidence.

## DECISION

Decision to make:

[DESCRIBE THE DECISION IN ONE SENTENCE]

Options under consideration:

- [OPTION A]
- [OPTION B]
- [OPTION C / NONE / BUILD VS BUY / OTHER]

Decision horizon:

[REVERSIBLE IN DAYS / REVERSIBLE IN MONTHS / HARD TO REVERSE]

## CONTEXT

System / product context:

[ARCHITECTURE / USERS / WORKLOAD / TEAM / BUSINESS CONTEXT]

Hard constraints — an option that violates one of these is not viable:

- [SECURITY / COMPLIANCE]
- [BUDGET]
- [DELIVERY DEADLINE]
- [SUPPORTED PLATFORM / STACK]
- [OTHER]

Decision criteria and relative importance:

- [CRITERION]: [HIGH / MEDIUM / LOW]
- [CRITERION]: [HIGH / MEDIUM / LOW]
- [CRITERION]: [HIGH / MEDIUM / LOW]

Known evidence:

[MEASUREMENTS / REQUIREMENTS / DOCUMENTATION / INCIDENT DATA / TEAM EXPERIENCE]

Known unknowns:

[WHAT YOU DO NOT YET KNOW THAT COULD CHANGE THE DECISION]

## TASK

Evaluate every viable option against the same constraints and criteria.

Do not optimize for novelty, popularity, or architectural sophistication unless those factors are explicitly relevant to the stated criteria.

## ANALYSIS RULES

- Separate **supplied fact**, **source claim**, **inference**, and **assumption**.
- Do not invent benchmarks, pricing, limits, capabilities, incidents, or implementation effort.
- Reject an option immediately if it violates a hard constraint; do not allow a weighted score to hide the violation.
- Treat a score as a summary, not as evidence.
- Surface second-order consequences: migration cost, operational burden, lock-in, failure modes, and reversibility.
- Prefer the simplest option that satisfies the real constraints when the evidence does not justify added complexity.
- If the recommendation depends heavily on one assumption, state that dependency explicitly.
- If two options are effectively tied, do not force a winner. Define the smallest useful experiment or evidence request that would break the tie.
- Distinguish **decision confidence** from confidence in individual facts.
- Never present missing evidence as established fact.

## PROCESS

1. **Normalize the decision**
   - Restate what is actually being decided.
   - List hard constraints.
   - Remove options that are clearly out of scope or non-viable.

2. **Build the decision frame**
   - Create a criteria table.
   - Mark each criterion as `hard constraint` or `preference`.
   - State its relative importance and why it matters.

3. **Create an evidence ledger**
   For each option, record:
   - evidence supporting it;
   - evidence against it;
   - assumptions required;
   - important unknowns.

4. **Compare options**
   Use the same criteria for every option.
   Explain meaningful trade-offs instead of hiding them behind a single score.

5. **Stress-test the leading option**
   Ask:
   - What would make this fail?
   - What assumption is most fragile?
   - What future condition would make another option better?
   - How expensive is reversal?

6. **Make the recommendation**
   Choose one of:
   - `DECIDE` — evidence is sufficient to recommend;
   - `CONDITIONAL` — recommend only if named assumptions hold;
   - `HOLD` — evidence is insufficient to choose responsibly.

7. **Define the next validation step**
   Propose the cheapest high-information action that reduces the most important uncertainty.

## OUTPUT CONTRACT

Return exactly these sections.

### 1. Decision status
`DECIDE`, `CONDITIONAL`, or `HOLD`.

### 2. Decision summary
2–5 sentences explaining the decision and its most important reason.

### 3. Constraints
| Constraint | Type | Consequence |
|---|---|---|
| ... | hard / preference | ... |

### 4. Option comparison
| Option | Strengths | Weaknesses | Constraint conflicts | Operational consequences |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

### 5. Evidence and uncertainty
For each option:
- supplied evidence;
- inference;
- assumptions;
- unknowns.

### 6. Recommendation
State:
- recommended option;
- why it wins against the actual criteria;
- the strongest argument against it;
- confidence: `high`, `medium`, or `low`.

### 7. Reversal triggers
List concrete conditions that should cause the decision to be revisited.

### 8. Next validation step
Give one or more actions ordered by information value, not by convenience.

## FALLBACK

If the available evidence cannot support a responsible recommendation, do not guess.

Return `HOLD`, identify the unresolved decision factors, and specify the smallest additional evidence needed to move from uncertainty to a decision.
