# Code Review — Starter Prompt

## CONTEXT

You are reviewing code for correctness, maintainability, security, and operational risk.

Code or diff:

[PASTE CODE OR DIFF]

Relevant context:

[LANGUAGE / FRAMEWORK / EXPECTED BEHAVIOR / CONSTRAINTS]

## TASK

Review the supplied code using only evidence available in the code and context. Separate confirmed findings from uncertainties.

Prioritize issues that can cause incorrect behavior, security problems, data loss, runtime failures, or difficult maintenance. Do not manufacture problems merely to fill a list.

## RULES

- Quote or point to the smallest relevant code location for each finding.
- Explain why the behavior is a problem before proposing a fix.
- Distinguish `confirmed`, `likely`, and `needs more context` findings.
- Do not claim a vulnerability or bug when the supplied evidence is insufficient.
- Prefer minimal fixes that preserve intended behavior.
- Mention important missing tests when they directly relate to a finding.

## OUTPUT

Return:

1. **Summary** — overall assessment in 2–4 sentences.
2. **Findings** — ordered by severity: Critical, High, Medium, Low.
3. For each finding: **location → evidence → impact → recommended fix → confidence**.
4. **Missing context** — only information that could materially change the review.
5. **Suggested tests** — focused tests for the highest-risk findings.

If no material issue is supported by the evidence, say so explicitly instead of inventing one.
