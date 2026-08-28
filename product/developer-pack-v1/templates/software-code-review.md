# Software Code Review Template

Maturity: `VALID` only after the static checklist passes.

## PURPOSE
Review [CODE_OR_DIFF] for correctness, maintainability, security-relevant defects, and regression risk.

## CONTEXT
Repository/runtime constraints:
[CONTEXT]

Do not invent files, APIs, execution results, or requirements that were not provided.

## REVIEW PROCESS
1. Understand intended behavior.
2. Trace changed logic and affected interfaces.
3. Identify concrete defects or risks.
4. Separate confirmed issues from questions or hypotheses.
5. Prioritize findings by impact and confidence.

## RULES
- Prefer specific findings tied to code evidence.
- Do not report style preferences as defects.
- Do not claim tests passed unless test evidence was actually observed.
- When context is insufficient, say what is unknown.

## OUTPUT CONTRACT
For each finding provide:
- severity;
- location;
- issue;
- why it matters;
- suggested fix;
- confidence.

Then provide:
- overall assessment;
- missing context;
- recommended verification steps.

## QUALITY GATE
Reject any finding that cannot be connected to supplied code/context or a clearly labeled inference.
