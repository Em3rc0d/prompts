# Adapt One Message Across Audiences

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when the same underlying facts must be communicated differently to multiple audiences without factual drift.

## Prompt

```text
CORE MESSAGE / FACTS
{{message}}

AUDIENCES
{{audiences}}

PURPOSE PER AUDIENCE
{{purposes}}

CHANNELS / LIMITS
{{channels_or_constraints}}

TERMS THAT MUST REMAIN
{{required_terms_or_none}}

RULES
- Keep the underlying factual claims identical across versions.
- Change framing, detail, vocabulary, and emphasis only when appropriate to the audience.
- Do not invent audience concerns, authority, outcomes, or commitments.
- Preserve required terminology where precision matters.
- Do not omit a material risk or caveat merely because an audience is non-technical.
- Flag when one message cannot safely serve all audiences.

PROCESS
1. Extract the invariant factual core.
2. Map each audience's information need from supplied context.
3. Choose appropriate detail and terminology.
4. Draft each version.
5. Compare versions for factual drift.
6. Flag conflicts between brevity and required disclosure.

OUTPUT
1. Invariant fact set.
2. Audience/message matrix.
3. One adapted message per audience.
4. Material differences in emphasis.
5. Factual-drift audit.
6. Any audience requiring additional context.

VERIFICATION
All versions must preserve the same underlying facts, numbers, commitments, and uncertainty.
```
