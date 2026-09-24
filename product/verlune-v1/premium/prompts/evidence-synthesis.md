# Evidence Synthesis

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when multiple sources need to be combined without flattening disagreement or overstating certainty.

## Prompt

```text
Synthesize the evidence I provide for the question below.

QUESTION
{{question}}

SOURCES / EXCERPTS / RESULTS
{{sources}}

SCOPE
{{population_time_period_geography_domain_or_none}}

DECISION OR USE
{{why_the_synthesis_is_needed}}

RULES
- Treat source statements as source claims unless independently established.
- Preserve source identity.
- Separate direct evidence, source interpretation, your inference, and unknowns.
- Do not count repeated reporting of the same underlying evidence as independent confirmation.
- Identify material differences in population, timeframe, definitions, methods, or context.
- Do not force consensus.
- Do not invent missing source details.
- Flag stale evidence when freshness matters.

PROCESS
1. Normalize the exact question.
2. Extract material claims from each source.
3. Group claims by proposition, not by document order.
4. Identify agreement, contradiction, and incomparable evidence.
5. Assess source relevance and limitations.
6. Identify what conclusions the evidence can and cannot support.
7. Produce the weakest defensible synthesis.

OUTPUT
1. Question and scope.
2. Evidence map:
   | Proposition | Supporting sources | Contradicting sources | Limitations | State |
3. Areas of agreement.
4. Material disagreement.
5. Evidence gaps.
6. Synthesis with explicit confidence language.
7. What would most improve confidence.
8. Claims that should NOT be made from the current evidence.

VERIFICATION
Every synthesis statement must trace to the evidence map or be clearly labeled as inference.
```
