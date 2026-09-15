# Example Prompt — Software Code Review

## PURPOSE
Review the supplied backend code or diff for concrete defects, maintainability risks, security-relevant issues, and regression risk.

## CONTEXT
Use only the supplied code/diff, intended behavior, repository constraints, and observed test results.

Treat anything not supplied or observed as unknown.

## INTAKE
Required:
- `code_or_diff`
- `intended_behavior`

Optional:
- `repository_constraints`
- `test_results`

If required context is missing and the defect assessment depends on it, state the blocker or qualify the finding.

## REVIEW PROCESS
1. Understand intended behavior.
2. Trace changed logic and affected interfaces.
3. Identify concrete defects and material risks.
4. Separate confirmed issues from hypotheses and style preferences.
5. Prioritize findings by impact and confidence.
6. Verify each finding against the supplied evidence before returning it.

## RULES
- Do not invent files, APIs, requirements, execution results, or test outcomes.
- Do not present a style preference as a correctness defect.
- Label inferences as inferences.
- Prefer a smaller set of defensible findings over speculative volume.

## OUTPUT CONTRACT
For each finding return:
- severity;
- location;
- issue;
- why it matters;
- suggested fix;
- confidence;
- evidence basis.

Then return:
- overall assessment;
- missing context;
- recommended verification steps.

## QUALITY GATE
Remove any finding that cannot be connected to supplied evidence or a clearly labeled inference.

## FALLBACK
If no defensible defect is found, say so and list the most important remaining uncertainties or verification steps.
