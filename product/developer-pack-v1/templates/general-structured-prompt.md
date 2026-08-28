# General Structured Prompt

Maturity: `VALID` (static acceptance passed; no behavioral claim).

## PURPOSE
Achieve: [DESIRED_OUTCOME].

## ROLE
Act as: [ROLE_OR_OPERATING_PERSPECTIVE].

## CONTEXT
Use only: [ALLOWED_CONTEXT].
Treat missing or unsupported facts as unknown.

## INTAKE
Inputs:
- [INPUT_1]
- [INPUT_2]

If a required input is missing, state the blocker before proceeding.

## PROCESS
1. Interpret the task and constraints.
2. Identify assumptions that materially affect the answer.
3. Perform the task using the provided context.
4. Verify the result against the quality gate.

## RULES
- Must: [REQUIRED_BEHAVIOR].
- Must not: [FORBIDDEN_BEHAVIOR].
- Preserve: [IMPORTANT_BOUNDARY].

## OUTPUT CONTRACT
Return:
[FORMAT_AND_REQUIRED_SECTIONS]

## QUALITY GATE
Before finalizing, verify:
- the output answers the requested task;
- important claims are supported by allowed context;
- required sections are present;
- unsupported certainty is removed.

## FALLBACK
If the task cannot be completed reliably, return the partial result plus the exact missing information or unresolved uncertainty.
