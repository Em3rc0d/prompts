# Root-Cause an Operational Failure

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when an operational problem repeats and you need to distinguish symptoms, contributing conditions, and supported root causes.

## Prompt

```text
PROBLEM / FAILURE
{{failure}}

OBSERVED INCIDENTS
{{incidents_or_examples}}

PROCESS / SYSTEM CONTEXT
{{process_context}}

KNOWN CHANGES
{{changes_or_none}}

AVAILABLE EVIDENCE
{{evidence}}

RULES
- Do not call the nearest visible error the root cause.
- Separate event facts, contributing conditions, hypotheses, and confirmed causal links.
- Look for process, information, ownership, tooling, and control failures without assuming one category.
- Do not invent frequency, impact, policy, or causal evidence.
- Prefer causes that explain multiple observed incidents when evidence supports them.
- Distinguish containment from prevention.

PROCESS
1. Reconstruct the failure pattern.
2. Map where the expected process diverged.
3. Generate candidate causes.
4. Test each cause against observed incidents and counterexamples.
5. Identify systemic contributors and missing controls.
6. Define corrective actions proportional to confidence.
7. Specify recurrence evidence to monitor.

OUTPUT
1. Observed failure pattern.
2. Cause map with confidence.
3. Contributing conditions.
4. Containment actions.
5. Corrective / preventive actions.
6. Evidence still required.
7. Recurrence indicators.

VERIFICATION
A root-cause statement must explain the observed failure and be supported by more than temporal correlation.
```
