# Improve Writing

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when you already have a draft and want a clearer version without changing its meaning.

## Prompt

```text
Improve the draft below for a real reader.

DRAFT
{{draft}}

AUDIENCE
{{audience}}

PURPOSE
{{what_the_text_should_achieve}}

VOICE / TONE
{{desired_voice_or_keep_current}}

MUST PRESERVE
{{facts_terms_names_constraints_or_none}}

RULES
- Preserve factual meaning and required terminology.
- Do not invent credentials, experiences, examples, evidence, or claims.
- Remove repetition and generic filler.
- Prefer clear, natural wording over inflated language.
- Preserve intentional nuance.
- If a sentence is ambiguous and rewriting it could change meaning, flag it instead of guessing.

OUTPUT
1. Revised text.
2. Three most important changes.
3. Any ambiguity or fact that needs my confirmation.

FINAL CHECK
Confirm that required facts/terms were preserved and that no unsupported claim was added.
```
