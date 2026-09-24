# Pre-Mortem a Plan

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use before execution to identify plausible failure modes, weak assumptions, and missing controls without treating imagined failures as facts.

## Prompt

```text
PLAN
{{plan}}

SUCCESS CRITERIA
{{success_criteria}}

CONSTRAINTS
{{constraints}}

KNOWN RISKS
{{known_risks_or_none}}

DEPENDENCIES
{{dependencies_or_unknown}}

RULES
- Treat failure scenarios as hypotheses, not predictions.
- Focus on plausible mechanisms tied to the actual plan.
- Do not manufacture external threats just to make the list longer.
- Separate preventable failure modes from residual risk.
- Prefer controls and early-warning signals that can actually be observed.
- Identify assumptions that lack evidence.

PROCESS
1. Reconstruct the plan and critical path.
2. Assume the plan failed and generate plausible mechanisms.
3. Map each failure mode to assumptions, dependencies, or controls.
4. Assess detectability and reversibility qualitatively.
5. Define preventive actions and early-warning signals.
6. Identify which risks require redesign versus monitoring.

OUTPUT
1. Critical assumptions.
2. Failure-mode table.
3. Early-warning signals.
4. Preventive / mitigating actions.
5. Plan changes worth making before execution.
6. Residual risks.
7. Go / revise / evidence-needed state.

VERIFICATION
Every failure mode must connect to a real element of the plan or explicitly stated external dependency.
```
