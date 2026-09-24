# Identify Evidence Gaps in a Resume

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a resume contains claims that may be vague, weakly evidenced, or poorly matched to a target role.

## Prompt

```text
RESUME
{{resume}}

TARGET ROLE / JOB DESCRIPTION
{{role}}

SUPPORTING EVIDENCE
{{projects_metrics_examples_or_none}}

RULES
- Do not invent stronger evidence for the candidate.
- Distinguish missing evidence from missing experience.
- Flag vague impact, unsupported scale, unclear ownership, and skill claims without examples.
- Do not require metrics when a truthful qualitative outcome is more appropriate.
- Map evidence gaps to target-role requirements.
- Preserve uncertainty where supporting material is absent.

PROCESS
1. Extract resume claims.
2. Map each material claim to supplied evidence.
3. Map role requirements to candidate evidence.
4. Identify unsupported or under-specified claims.
5. Rank gaps by hiring relevance.
6. Suggest evidence to gather or wording to narrow.
7. Identify claims that should be removed rather than embellished.

OUTPUT
1. Claim/evidence audit.
2. Role requirement gaps.
3. Highest-priority evidence gaps.
4. Questions to recover truthful evidence.
5. Claims to narrow/remove.
6. Safe rewrite guidance without fabrication.

VERIFICATION
No suggested rewrite may introduce a fact, metric, responsibility, or outcome not present in the supplied evidence.
```
