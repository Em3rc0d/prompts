# Repurpose Source Material Across Channels

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when one authoritative source should become multiple channel-native content pieces without factual drift or repetitive copy.

## Prompt

```text
SOURCE MATERIAL
{{source}}

CHANNELS
{{channels}}

AUDIENCE
{{audience}}

GOAL
{{goal}}

CONTENT ALREADY PUBLISHED
{{existing_content_or_none}}

RULES
- Treat the source as the factual authority.
- Do not add claims, anecdotes, results, or examples not supported by the source.
- Adapt structure and emphasis to each channel rather than shortening the same copy.
- Avoid repeating hooks, angles, or framing already supplied as published.
- Preserve material caveats and uncertainty.
- Keep each output traceable to source sections.

PROCESS
1. Extract reusable facts, ideas, examples, and constraints.
2. Generate distinct channel-appropriate angles.
3. Assign one job to each content piece.
4. Draft channel-native outputs.
5. Run factual-drift and duplication checks.
6. Identify source material that should not be repurposed without more context.

OUTPUT
1. Source fact/idea inventory.
2. Channel plan with distinct jobs.
3. Drafts or outlines per channel.
4. Source trace for material claims.
5. Novelty / duplication check.
6. Claims requiring additional evidence.

VERIFICATION
No output may contain a factual claim that cannot be traced to the supplied source.
```
