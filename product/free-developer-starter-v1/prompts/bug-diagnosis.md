# Bug Diagnosis — Starter Prompt

## CONTEXT

Expected behavior:

[WHAT SHOULD HAPPEN]

Observed behavior:

[WHAT ACTUALLY HAPPENS]

Evidence:

[ERROR MESSAGES / LOGS / RELEVANT CODE / ENVIRONMENT / RECENT CHANGES]

## TASK

Analyze the software defect methodically. Build a small set of plausible causes, rank them by the supplied evidence, and propose checks that distinguish between them.

## RULES

- Separate observed facts from inferred causes.
- Do not invent logs, runtime behavior, versions, configuration, or reproduction results.
- Prefer explanations that account for all supplied symptoms with few unsupported assumptions.
- For each hypothesis, identify supporting evidence and what observation would rule it out.
- Recommend reversible diagnostic checks before broad code changes when possible.
- If evidence is insufficient, state exactly what additional information is needed.

## OUTPUT

Return:

1. **Observed facts**.
2. **Top hypotheses**, ranked with confidence.
3. **Next diagnostic checks**, ordered by information value.
4. **Most likely fix**, only if supported by evidence.
5. **Verification plan** — how to confirm the defect is resolved and check for regression.

Do not call a root cause confirmed unless the supplied evidence establishes it.
