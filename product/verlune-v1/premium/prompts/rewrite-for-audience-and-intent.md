# Rewrite for Audience and Intent

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a draft must be transformed for a specific reader and purpose while preserving meaning and factual boundaries.

## Prompt

```text
Rewrite the draft for the specified reader and intent.

DRAFT
{{draft}}

AUDIENCE
{{audience}}

INTENDED ACTION / EFFECT
{{what_the_reader_should_understand_feel_or_do}}

CHANNEL / FORMAT
{{email_report_post_page_message_other}}

VOICE
{{voice}}

IMMUTABLE FACTS / TERMS
{{facts_terms_quotes_names_or_none}}

LENGTH / FORMAT CONSTRAINTS
{{constraints_or_none}}

RULES
- Preserve factual meaning and immutable terms.
- Do not invent proof, outcomes, urgency, authority, anecdotes, credentials, or customer claims.
- Adapt vocabulary, structure, emphasis, and rhythm to the audience.
- Keep necessary nuance; do not oversimplify a material qualification.
- Remove content that does not help the intended reader.
- If the requested intent conflicts with factual accuracy or supplied constraints, preserve accuracy and flag the conflict.

PROCESS
1. Infer the draft's current message.
2. Identify audience needs and likely friction.
3. Decide what to preserve, compress, move, clarify, or remove.
4. Rewrite.
5. Audit for factual drift and generic filler.
6. Compare the new text against the intended effect.

OUTPUT
1. Final rewritten text.
2. Audience/intent decisions made.
3. Material information removed or repositioned.
4. Any unresolved ambiguity.
5. Factual-preservation check.

VERIFICATION
Before finalizing:
- compare material claims against the original draft;
- confirm immutable facts/terms remain intact;
- confirm the rewrite matches the stated audience and channel;
- flag any sentence whose meaning may have changed materially;
- confirm no unsupported claim, evidence, urgency, credential, or outcome was added.
```
