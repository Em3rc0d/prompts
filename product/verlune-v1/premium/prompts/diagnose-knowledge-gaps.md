# Diagnose Knowledge Gaps

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when someone has partial knowledge and you need to locate the specific concepts or skills preventing reliable performance.

## Prompt

```text
TARGET TOPIC / SKILL
{{target}}

EVIDENCE OF CURRENT PERFORMANCE
{{answers_work_samples_attempts_or_notes}}

EXPECTED LEVEL
{{expected_level}}

REFERENCE MATERIAL
{{source_material_or_none}}

RULES
- Diagnose from observed performance, not self-confidence alone.
- Distinguish missing knowledge, misconception, retrieval failure, and application failure.
- Do not infer gaps that are not evidenced.
- Prefer prerequisite explanations when one gap plausibly causes several downstream errors.
- Do not label mastery globally from a small sample.
- If reference material is supplied, use it as the authority for expected content.

PROCESS
1. Define the target performance.
2. Extract errors, hesitations, and successful evidence.
3. Map each issue to the smallest plausible knowledge dependency.
4. Test for upstream prerequisite gaps.
5. Rank gaps by leverage.
6. Design a focused repair and re-check.

OUTPUT
1. Demonstrated strengths.
2. Gap map: evidence, gap type, likely prerequisite, confidence.
3. Highest-leverage gaps.
4. Targeted repair tasks.
5. Re-check questions/tasks.
6. What remains untested.

VERIFICATION
Each diagnosed gap must cite the observed performance evidence that supports it.
```
