# Code Review — Starter Prompt

Use this when you want a review that prioritizes defects and evidence instead of producing a long list of style opinions.

## REVIEW TARGET

Code, diff, or files:

[PASTE CODE / DIFF / RELEVANT FILES]

Change intent:

[WHAT THIS CHANGE IS SUPPOSED TO DO]

Relevant runtime context:

[LANGUAGE / FRAMEWORK / VERSION / DATABASE / CLOUD / DEPLOYMENT MODEL]

Expected behavior and invariants:

[WHAT MUST REMAIN TRUE]

Known constraints:

[PERFORMANCE / SECURITY / BACKWARD COMPATIBILITY / DELIVERY / OTHER]

Observed test evidence, if any:

[TEST OUTPUT / CI RESULT / REPRODUCTION RESULT / NONE OBSERVED]

## TASK

Review the supplied material for concrete correctness, security, data-integrity, reliability, performance, operability, and maintainability risks.

Prioritize findings that can change system behavior or materially increase engineering risk.

Do not manufacture findings merely to fill categories.

## EVIDENCE LEVELS

Label every finding as one of:

- `CONFIRMED` — directly supported by supplied code/context.
- `LIKELY` — strong inference, but one material fact is still unobserved.
- `QUESTION` — requires additional context before it can be treated as a defect.

Never promote `LIKELY` or `QUESTION` to `CONFIRMED` for rhetorical strength.

## SEVERITY RUBRIC

- `CRITICAL` — plausible catastrophic impact such as major security compromise, irreversible data loss, or broad production outage.
- `HIGH` — likely incorrect behavior, serious security exposure, data corruption, or major reliability failure.
- `MEDIUM` — meaningful defect or operational/maintenance risk with bounded impact.
- `LOW` — minor issue worth fixing but unlikely to materially affect correctness or operations.

Style preference alone is not a defect.

## REVIEW PROCESS

1. **Reconstruct intent**
   - State what the code appears intended to do.
   - Identify missing context that could materially change the review.

2. **Trace behavior**
   Inspect the relevant paths for:
   - incorrect control flow;
   - invalid state transitions;
   - broken error handling;
   - data consistency issues;
   - unsafe trust boundaries;
   - concurrency / ordering problems;
   - resource leaks or unbounded work;
   - compatibility/regression risk.

3. **Check interfaces and assumptions**
   Look for contracts that the change depends on:
   - API shape;
   - database constraints;
   - authentication/authorization;
   - nullability and input validation;
   - idempotency;
   - retries/timeouts;
   - external service behavior.

4. **Challenge each candidate finding**
   Before reporting it, answer:
   - What exact code supports this finding?
   - What concrete failure can result?
   - Is that failure confirmed or inferred?
   - What additional context could invalidate the finding?

5. **Prioritize**
   Report the smallest set of findings that materially matter.
   Do not bury high-impact issues under low-value commentary.

## RULES

- Cite the smallest useful code location or snippet for every finding.
- Explain the failure mechanism before suggesting a fix.
- Do not claim a test passed unless actual test evidence was supplied.
- Do not claim a vulnerability solely because a risky pattern exists; connect it to a reachable threat or missing control.
- Prefer minimal fixes that preserve intended behavior.
- Call out missing tests only when they are tied to a concrete risk or changed behavior.
- If a recommendation changes public behavior, schema, API compatibility, security posture, or persistence semantics, state that consequence explicitly.
- If no material issue is supported by evidence, say so.

## OUTPUT CONTRACT

### 1. Executive assessment
2–5 sentences:
- what the change does;
- overall risk;
- highest-priority concern, if any.

### 2. Findings
For each finding use:

**[SEVERITY] Title**

- Evidence level: `CONFIRMED | LIKELY | QUESTION`
- Location: `[FILE / SYMBOL / LINE OR SNIPPET]`
- Evidence: what in the supplied material supports the finding
- Failure mode: what can go wrong
- Impact: why it matters
- Recommended fix: smallest useful corrective action
- Verification: how to prove the fix works
- Confidence: `high | medium | low`

Order findings from highest to lowest severity.

### 3. Missing context
Only list information that could materially change a finding or the overall assessment.

### 4. Verification plan
Provide focused tests/checks for the highest-risk paths:
- happy path;
- relevant edge case;
- failure/retry path where applicable;
- regression case.

### 5. Ship decision
Choose one:
- `BLOCK` — confirmed high/critical risk should be resolved before shipping;
- `REVIEW` — material uncertainty remains;
- `SHIP_WITH_FIXES` — bounded issues can be corrected without redesign;
- `NO_MATERIAL_ISSUE_FOUND` — no material issue is supported by the supplied evidence.

## FALLBACK

If the supplied code/context is too incomplete for a responsible review, do not invent defects.

Return `REVIEW`, explain the missing context, and identify the minimum additional material needed for a useful review.
