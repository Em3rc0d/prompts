# Check Your Understanding

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use after studying a topic when you want to find what you can actually explain, retrieve, and apply.

## Prompt

```text
TOPIC
{{topic}}

WHAT I HAVE STUDIED
{{notes_material_or_summary}}

MY CURRENT EXPLANATION
{{what_i_think_i_understand_or_blank}}

TARGET LEVEL
{{course_exam_job_practical_use_or_unspecified}}

RULES
- Test understanding rather than rewarding fluent wording.
- Ask or generate a small set of questions that cover recall, explanation, application, and one transfer case.
- Do not mark an answer correct just because it uses relevant vocabulary.
- Point out the exact misconception or missing link when an answer is weak.
- Use only the supplied material unless external knowledge is explicitly requested.
- If the source material itself is incomplete or contradictory, say so.

OUTPUT
1. A short diagnostic set of questions.
2. For each answer provided: correct / partial / incorrect / unsupported, with a brief reason.
3. Knowledge gaps ranked by importance.
4. One targeted review task per important gap.
5. A final transfer question that uses the idea in a new situation.

VERIFICATION
Do not claim mastery. Report only what the supplied answers demonstrate.
```
