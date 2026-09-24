# Design a Campaign Brief

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a marketing campaign needs a coherent brief grounded in a real offer, audience, constraints, and evidence.

## Prompt

```text
OFFER / PRODUCT
{{offer}}

AUDIENCE
{{audience}}

CAMPAIGN GOAL
{{goal}}

CHANNELS
{{channels}}

EVIDENCE / INSIGHTS
{{evidence}}

CONSTRAINTS
{{budget_timing_brand_compliance_or_unknown}}

RULES
- Do not invent product claims, audience insights, budgets, performance targets, or proof.
- Separate known audience evidence from campaign hypotheses.
- Make the campaign idea serve the stated goal rather than chase novelty.
- Keep channel roles explicit.
- Define measurable signals without fabricating benchmarks.
- Flag claims that require evidence or approval before publication.

PROCESS
1. Clarify campaign objective and conversion/behavior path.
2. Extract evidence-backed audience tension or need.
3. Define message hierarchy.
4. Assign roles to channels and formats.
5. Design creative territories and proof requirements.
6. Define measurement and learning loop.
7. Identify launch blockers.

OUTPUT
1. Campaign objective.
2. Audience evidence and hypothesis.
3. Message hierarchy.
4. Channel/format plan.
5. Creative territories.
6. Proof / claim requirements.
7. Measurement plan.
8. Open risks / approvals.

VERIFICATION
Every campaign claim and audience insight must be evidence-backed or explicitly marked as hypothesis.
```
