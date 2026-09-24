# Generate Content Angles

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when you have a real topic, source, or piece of work and need distinct content angles without inventing authority.

## Prompt

```text
SOURCE / TOPIC
{{source_material_or_topic}}

AUDIENCE
{{audience}}

CHANNEL
{{channel_or_unspecified}}

GOAL
{{what_the_content_should_help_the_audience_do_or_understand}}

ANGLES ALREADY USED
{{used_angles_or_none}}

RULES
- Ground every angle in the supplied source, topic, or real experience.
- Avoid repeating angles already listed as used.
- Make each angle meaningfully different in question, tension, or audience value—not just wording.
- Do not invent results, credentials, customers, metrics, anecdotes, or controversy.
- Prefer specific practical tensions over generic motivational framing.
- Do not write full posts unless asked.

OUTPUT
1. 8 distinct angles.
2. For each: hook idea, core question, audience value, and evidence/source it depends on.
3. Flag any angle that would require additional evidence before publication.
4. Identify the 2 angles most different from the rest and explain why.

VERIFICATION
Remove any angle that depends on a claim not supported by the supplied material.
```
