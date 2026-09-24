# Competitive Landscape Analysis

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when you need a bounded, evidence-based view of competitors or alternatives without turning scattered signals into market certainty.

## Prompt

```text
MARKET / PROBLEM SPACE
{{market}}

TARGET CUSTOMER / USE CASE
{{customer_or_use_case}}

KNOWN COMPETITORS / ALTERNATIVES
{{competitors_or_none}}

EVIDENCE / SOURCES
{{sources}}

SCOPE
{{geography_time_period_segment}}

RULES
- Distinguish direct competitors, substitutes, adjacent tools, and non-consumption.
- Do not infer revenue, market share, traction, strategy, or customer satisfaction without evidence.
- Preserve dates because products and positioning change.
- Separate company claims from independent observations.
- Use comparable dimensions only when the underlying evidence is actually comparable.
- Surface missing competitors or data as unknown, not as absence.

PROCESS
1. Define the competitive job and scope.
2. Classify alternatives by type.
3. Extract comparable facts and positioning claims.
4. Map capability, business-model, and audience differences.
5. Identify convergence and differentiation.
6. Assess evidence quality and freshness.
7. Identify unanswered strategic questions.

OUTPUT
1. Landscape map.
2. Competitor comparison table.
3. Observed positioning and capability differences.
4. Evidence-backed differentiation opportunities.
5. Important unknowns / stale evidence.
6. Questions to validate before a strategic decision.

VERIFICATION
Every competitor claim must have a source/evidence note or be marked unknown/inference.
```
