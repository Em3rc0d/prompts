# Investigate a Production Failure

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a live or production-like system is failing and you need an evidence-first investigation without prematurely declaring root cause.

## Prompt

```text
INCIDENT / SYMPTOMS
{{incident_description}}

TIMELINE
{{known_timeline_or_unknown}}

OBSERVABILITY EVIDENCE
{{logs_metrics_traces_errors_or_none}}

RECENT CHANGES
{{deploys_config_data_dependency_changes_or_none}}

SYSTEM CONTEXT
{{architecture_dependencies_environment}}

RULES
- Preserve the distinction between symptom, correlation, contributing factor, and root cause.
- Do not invent events, logs, deploys, traffic patterns, or dependency behavior.
- Prefer hypotheses that explain the observed timeline and all material evidence.
- Prioritize safe evidence collection before speculative remediation.
- Separate mitigation from root-cause investigation.
- Call out missing telemetry that prevents confidence.
- Do not mark the incident resolved without explicit recovery evidence.

PROCESS
1. Build the factual incident timeline.
2. Normalize symptoms and affected scope.
3. Correlate changes and telemetry without assuming causality.
4. Generate and rank falsifiable hypotheses.
5. Define the smallest discriminating checks.
6. Identify safe mitigation options and their risks.
7. Define evidence required for root cause and recovery.

OUTPUT
1. Incident facts and timeline.
2. Impact / scope supported by evidence.
3. Ranked hypothesis table: hypothesis, supporting evidence, conflicting evidence, next check.
4. Immediate mitigation options.
5. Root-cause evidence still required.
6. Recovery verification checklist.
7. Current state: INVESTIGATING / MITIGATED_NOT_PROVEN / ROOT_CAUSE_SUPPORTED / RECOVERY_VERIFIED.

VERIFICATION
Do not promote a hypothesis to root cause unless the available evidence explains the failure and discriminates against credible alternatives.
```
