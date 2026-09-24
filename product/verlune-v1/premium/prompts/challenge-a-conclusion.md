# Challenge a Conclusion

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when an analysis or conclusion needs an adversarial review for unsupported leaps, alternative explanations, and missing evidence.

## Prompt

```text
CONCLUSION / CLAIM
{{claim}}

SUPPORTING ANALYSIS / EVIDENCE
{{evidence}}

SCOPE
{{scope}}

DECISION AT STAKE
{{decision_or_none}}

RULES
- Do not oppose the conclusion merely for balance.
- Identify the exact premises required for the conclusion to hold.
- Separate evidence weakness from logical weakness.
- Search for credible alternative explanations and boundary conditions.
- Do not invent counter-evidence.
- State when the conclusion remains the best-supported one after challenge.

PROCESS
1. Decompose the claim into premises.
2. Trace each premise to evidence.
3. Test alternative explanations.
4. Check scope, definitions, freshness, and selection effects.
5. Identify what evidence could falsify or strengthen the claim.
6. Reconstruct the weakest defensible conclusion.

OUTPUT
1. Original conclusion and required premises.
2. Support map.
3. Strongest challenges.
4. Alternative explanations.
5. Missing or decisive evidence.
6. Revised conclusion with appropriate confidence.
7. Claims that should not be made.

VERIFICATION
Challenges must be tied to actual evidence gaps or reasoning defects, not generic skepticism.
```
