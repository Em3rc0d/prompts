# Tailor a Resume to a Role

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use to adapt a resume to a specific role without fabricating experience.

## Prompt

```text
Tailor my resume to this role using only evidence present in my real background.

JOB DESCRIPTION
{{job_description}}

CURRENT RESUME / EXPERIENCE
{{resume}}

OPTIONAL CONTEXT
{{target_seniority_location_portfolio_or_none}}

RULES
- Never invent employment, dates, responsibilities, tools, education, certifications, achievements, metrics, leadership, or domain experience.
- Do not alter facts just to match keywords.
- Distinguish direct match, transferable evidence, and genuine gap.
- Prioritize relevance and clarity over keyword stuffing.
- Preserve chronology unless I explicitly authorize a different resume format.
- Do not infer protected characteristics or recommend discriminatory presentation.

PROCESS
1. Extract the role's explicit requirements.
2. Identify implied priorities but label them inferred.
3. Map my evidence to each important requirement.
4. Identify genuine gaps.
5. Reorder/emphasize existing evidence for relevance.
6. Rewrite bullets using concrete action + context + result only when supported.
7. Audit every changed claim against the original evidence.

OUTPUT
1. Role priority map.
2. Evidence-to-requirement map.
3. Gaps / risks.
4. Tailored resume text.
5. Change log explaining material edits.
6. Claims requiring my confirmation.
7. Optional cover-letter talking points based only on supported evidence.

VERIFICATION
For every material claim in the tailored resume, identify where it is supported in the supplied background. If support is absent, remove or flag it.
```
