# Produce an Executive Brief

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when complex material must become a concise decision-ready brief for an executive reader.

## Prompt

```text
SOURCE MATERIAL
{{source_material}}

AUDIENCE
{{executive_role}}

PURPOSE / DECISION
{{purpose}}

FACTS / TERMS THAT MUST REMAIN ACCURATE
{{required_facts}}

LENGTH / FORMAT
{{constraints_or_unspecified}}

RULES
- Preserve factual meaning and named terminology.
- Lead with what materially affects the reader's decision or understanding.
- Separate observed facts, interpretation, risks, and open questions.
- Do not invent causes, commitments, dates, owners, outcomes, or confidence.
- Remove implementation detail unless it materially changes the decision.
- Do not hide material uncertainty to make the brief sound cleaner.

PROCESS
1. Identify the executive question.
2. Extract decision-relevant facts.
3. Group material changes, implications, risks, and unknowns.
4. Remove detail that does not affect the reader.
5. Draft the brief in decreasing order of decision importance.
6. Audit factual preservation.

OUTPUT
1. Executive headline.
2. Situation / change.
3. Why it matters.
4. Evidence / key facts.
5. Risks and unknowns.
6. Decision / action required, only if supported.
7. Appendix note for omitted detail, if useful.

VERIFICATION
Trace every factual sentence back to the source material and verify that compression did not change meaning.
```
