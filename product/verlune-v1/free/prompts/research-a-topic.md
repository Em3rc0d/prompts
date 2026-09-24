# Research a Topic

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use for a bounded research question where sources and uncertainty matter.

## Prompt

```text
Research the topic below and produce a source-grounded overview.

QUESTION
{{research_question}}

SCOPE
{{geography_time_period_population_domain_or_none}}

PURPOSE
{{why_i_need_this}}

SOURCE REQUIREMENTS
{{preferred_or_required_sources_or_none}}

RULES
- Clarify the question only if ambiguity would materially change the research.
- Prefer primary or authoritative sources when they exist.
- Distinguish source claims from your synthesis.
- For changing facts, prefer current sources and state relevant dates.
- Surface meaningful disagreement instead of forcing consensus.
- Do not invent citations, studies, statistics, quotations, or URLs.
- If browsing/tools are unavailable, say so and limit the answer to what can actually be supported.

OUTPUT
1. Research question and scope.
2. Key findings.
3. Evidence/source notes for material claims.
4. Conflicting or uncertain evidence.
5. What remains unknown.
6. Practical conclusion appropriate to the evidence.
7. Highest-value next research step.

VERIFICATION
Check that every factual claim requiring external support has a real source or is clearly marked as unsupported/unknown.
```
