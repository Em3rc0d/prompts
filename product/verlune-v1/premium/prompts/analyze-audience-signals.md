# Analyze Audience Signals

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when comments, analytics, interviews, search data, or other audience evidence need to inform content decisions.

## Prompt

```text
AUDIENCE EVIDENCE
{{comments_metrics_interviews_search_data_other}}

CHANNEL / CONTEXT
{{channel_context}}

CURRENT CONTENT / OFFER
{{current_content_or_offer}}

QUESTION
{{what_we_need_to_learn}}

RULES
- Separate observed signals from interpretation and hypotheses.
- Do not generalize from a small or biased sample without saying so.
- Do not infer demographics, intent, purchasing power, or sentiment beyond the evidence.
- Treat engagement metrics as behavior signals, not proof of preference or commercial value.
- Look for repeated needs, questions, language, friction, and counter-signals.
- Preserve contradictory evidence.

PROCESS
1. Normalize the evidence by source.
2. Extract recurring signals.
3. Separate frequency from importance.
4. Map signals to possible audience jobs or questions.
5. Identify weak, biased, or missing evidence.
6. Generate bounded content hypotheses.
7. Define what to test next.

OUTPUT
1. Observed signal table.
2. Audience needs/questions supported by evidence.
3. Interpretations and confidence.
4. Contradictions / weak evidence.
5. Content hypotheses.
6. Recommended tests and success signals.

VERIFICATION
Every audience conclusion must point to observed evidence and include limitations when sample or source quality matters.
```
