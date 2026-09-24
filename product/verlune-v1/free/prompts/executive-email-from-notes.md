# Executive Email from Notes

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when technical or operational notes need to become a concise email for a non-technical stakeholder.

## Prompt

```text
NOTES
{{notes}}

AUDIENCE
{{recipient_role_or_context}}

PURPOSE
{{status_update_request_decision_other}}

TERMS THAT MUST REMAIN ACCURATE
{{names_versions_numbers_or_none}}

RULES
- Preserve all factual meaning and required terminology.
- Translate technical language only when doing so does not change its meaning.
- Separate completed work, observed results, pending items, and risks when those exist.
- Do not invent dates, commitments, causes, owners, next steps, or outcomes.
- Keep the tone professional, calm, and concise.
- Do not hide uncertainty that matters to the recipient.

OUTPUT
1. Subject line.
2. Email body in concise executive prose.
3. Optional short closing only if the notes support one.

VERIFICATION
Check that every factual statement in the email can be traced to the supplied notes.
```
