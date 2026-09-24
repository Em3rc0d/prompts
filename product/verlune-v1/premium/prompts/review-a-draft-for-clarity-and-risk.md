# Review a Draft for Clarity and Risk

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a draft needs editing plus a disciplined check for ambiguity, unsupported claims, accidental commitments, or misleading certainty.

## Prompt

```text
DRAFT
{{draft}}

AUDIENCE
{{audience}}

PURPOSE
{{purpose}}

FACTS / CLAIMS THAT MUST REMAIN
{{facts}}

SENSITIVE OR HIGH-RISK AREAS
{{areas_or_none}}

RULES
- Do not optimize wording at the expense of factual accuracy.
- Separate clarity issues from factual, legal/commercial, reputational, or commitment risks.
- Do not invent a risk merely because a sentence sounds strong.
- Flag unsupported absolutes, hidden assumptions, ambiguous ownership, and accidental promises.
- Preserve the author's intended position unless it is unclear.
- Do not add disclaimers mechanically when a clearer sentence solves the issue.

PROCESS
1. Identify the message and intended reader action.
2. Audit factual claims and certainty language.
3. Find ambiguity, repetition, and unnecessary complexity.
4. Identify sentences that could create unintended commitments or interpretations.
5. Rewrite only where the improvement is material.
6. Compare revised meaning against the original.

OUTPUT
1. Risk/clarity findings by sentence or section.
2. Revised draft.
3. Three most important changes.
4. Claims or sentences that need human confirmation.
5. Meaning-preservation note.

VERIFICATION
No revision may strengthen a claim or commitment beyond what the original material supports.
```
