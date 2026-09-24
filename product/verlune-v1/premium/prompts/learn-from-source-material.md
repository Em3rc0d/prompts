# Learn From Source Material

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a specific document, lecture, chapter, or set of notes should be the authoritative basis for learning.

## Prompt

```text
SOURCE MATERIAL
{{material}}

LEARNING GOAL
{{goal}}

CURRENT LEVEL
{{level_or_unspecified}}

TIME / DEPTH
{{time_or_depth}}

RULES
- Treat the supplied material as the requested basis unless outside research is explicitly requested.
- Do not silently correct, expand, or reconcile the source with general knowledge.
- Preserve the source terminology and organization when useful.
- Separate source-derived explanation from any clearly requested outside context.
- Use examples only when they do not contradict or replace the source.
- Surface gaps or ambiguity in the source rather than filling them silently.

PROCESS
1. Map the source structure and key concepts.
2. Identify prerequisites implied by the source.
3. Explain the material at the requested level.
4. Generate retrieval questions.
5. Generate one application task grounded in the material.
6. Review errors against the source.
7. Summarize what the source does and does not establish.

OUTPUT
1. Source map.
2. Key concepts and relationships.
3. Focused explanation.
4. Retrieval questions.
5. Application task.
6. Answer/review guidance grounded in the source.
7. Source gaps, ambiguity, or unsupported extensions.

VERIFICATION
Every substantive teaching claim should trace to the supplied material unless explicitly labeled as outside context.
```
