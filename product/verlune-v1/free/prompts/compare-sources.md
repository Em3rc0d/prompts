# Compare Sources

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when two or more sources discuss the same question and you need to understand agreement, disagreement, and relevance.

## Prompt

```text
QUESTION
{{question}}

SOURCES
{{sources_or_excerpts}}

SCOPE
{{population_time_period_geography_domain_or_none}}

WHY I AM COMPARING THEM
{{purpose}}

RULES
- Preserve source identity and do not merge claims before comparing them.
- Distinguish factual disagreement from differences in scope, definitions, methods, or time period.
- Do not treat repeated reporting of the same underlying evidence as independent confirmation.
- Do not invent author credentials, methods, dates, or source details.
- Prefer direct comparison of claims relevant to the stated question.
- Mark any conclusion that depends on inference rather than direct source support.

OUTPUT
1. Comparison table: source, relevant claim, evidence basis, scope, limitations.
2. Where the sources agree.
3. Where they materially disagree.
4. Where they are not actually comparable.
5. Which source is more relevant to the stated question and why, if that can be supported.
6. What remains unresolved.

VERIFICATION
Ensure every comparison traces to supplied source content and that missing metadata is not silently filled in.
```
