# Learn a Difficult Topic

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when you want to understand a topic rather than receive a one-shot definition.

## Prompt

```text
Teach me the following topic so I can explain it back in my own words.

TOPIC
{{topic}}

MY CURRENT LEVEL
{{what_i_already_know_or_unsure}}

GOAL
{{exam_project_general_understanding_or_other}}

CONSTRAINTS
{{time_limit_depth_course_scope_or_none}}

RULES
- Start from what I already know.
- Do not add complexity before the prerequisite idea is clear.
- Distinguish definitions, intuition, examples, and exceptions.
- If the topic depends on something I appear not to know, explain that prerequisite briefly.
- Do not pretend I understood something just because it was explained once.

OUTPUT
1. Simple mental model.
2. Core concepts.
3. One worked example.
4. Common misconception.
5. Three recall questions without answers.
6. After I answer, evaluate my reasoning and identify the smallest gap to revisit.

If my request is too broad for one useful session, propose a small learning sequence before teaching.
```
