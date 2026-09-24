# Understand a Job Description

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when you want to translate a job posting into clear requirements before deciding how to prepare or apply.

## Prompt

```text
JOB DESCRIPTION
{{job_description}}

MY BACKGROUND
{{resume_experience_or_optional}}

WHAT I NEED
{{understand_role_prepare_apply_or_unspecified}}

RULES
- Base the analysis on the supplied job description.
- Separate explicit requirements from preferences and inferred expectations.
- Do not invent employer priorities, interview process, salary, culture, or hidden criteria.
- If background is provided, distinguish demonstrated evidence from gaps and unknowns.
- Do not rewrite the resume unless asked.
- Call out ambiguous or overloaded terms.

OUTPUT
1. Role purpose in plain language.
2. Core responsibilities.
3. Required vs preferred qualifications.
4. Tools / domain knowledge explicitly requested.
5. Likely evidence the candidate should be ready to show, clearly labeled as inference when applicable.
6. If background is provided: matches, gaps, and unknowns.
7. Highest-value preparation questions.

VERIFICATION
Check that employer requirements are quoted or faithfully paraphrased from the posting, not inferred as facts.
```
