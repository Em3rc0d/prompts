# Exam Preparation

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use to convert a syllabus, notes, or topic list into an evidence-based preparation cycle rather than a passive summary.

## Prompt

```text
Build and run an exam-preparation plan from the material I provide.

EXAM / SUBJECT
{{subject}}

SCOPE
{{syllabus_topics_notes_or_source_material}}

EXAM DATE
{{date_or_unknown}}

FORMAT
{{multiple_choice_written_problem_solving_or_unknown}}

CURRENT STATE
{{topics_i_know_topics_i_struggle_with_or_unsure}}

AVAILABLE STUDY TIME
{{time}}

RULES
- Base the plan on the supplied scope; do not invent examinable content.
- Prioritize retrieval, application, discrimination between similar concepts, and error correction over rereading.
- Distinguish confidence from demonstrated recall.
- Do not reveal answers before a retrieval attempt unless I explicitly request teaching first.
- Track recurring errors and revisit them.
- If source material is incomplete, identify the gap.

PROCESS
1. Build a topic map.
2. Run a short diagnostic.
3. Classify each topic: STRONG / FRAGILE / WEAK / UNKNOWN.
4. Prioritize by exam relevance, dependency, weakness, and available time.
5. Create study blocks with retrieval and feedback.
6. Generate representative practice.
7. Evaluate my answers using the supplied material.
8. Maintain an error ledger.
9. Reallocate time as evidence changes.

OUTPUT
A. Preparation map.
B. Prioritized schedule.
C. Current diagnostic.
D. Practice set for the next block.
E. Error ledger.
F. End-of-block update.
G. Final readiness summary: READY / PARTIAL / HIGH_RISK / INSUFFICIENT_EVIDENCE.

VERIFICATION
Do not mark a topic STRONG unless I demonstrate recall/application or provide equivalent evidence.
```
