# Diagnose a Technical Error

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when you have an error message, failing command, or bounded technical symptom and need a disciplined diagnosis.

## Prompt

```text
ERROR / SYMPTOM
{{exact_error_or_symptom}}

WHAT I WAS TRYING TO DO
{{intended_action}}

RELEVANT CONTEXT
{{language_framework_environment_versions_or_unknown}}

RECENT CHANGES
{{recent_changes_or_none}}

AVAILABLE EVIDENCE
{{logs_snippets_commands_results_or_none}}

RULES
- Start from the supplied error and evidence, not from a favorite fix.
- Separate observations, plausible causes, and confirmed causes.
- Rank hypotheses by fit with the evidence and ease of falsification.
- Do not invent logs, versions, configuration, commands already run, or system state.
- Prefer the smallest safe diagnostic step that can distinguish between leading hypotheses.
- If the evidence is insufficient, say what evidence would materially reduce uncertainty.
- Do not recommend destructive commands without clearly identifying the risk.

OUTPUT
1. Observed facts.
2. Top hypotheses ranked with reasons.
3. Smallest diagnostic check for each leading hypothesis.
4. Likely fix only when supported by the evidence.
5. Risks / rollback notes for any proposed change.
6. What remains unknown.

VERIFICATION
Check that every proposed cause is labeled as hypothesis unless the supplied evidence actually establishes it.
```
