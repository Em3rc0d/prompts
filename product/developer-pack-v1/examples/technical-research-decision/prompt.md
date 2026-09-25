# Example Prompt — Technical Research Decision

## PURPOSE
Evaluate [DECISION] across [OPTIONS] and recommend the best-supported option for the supplied context.

## CONTEXT
Use only the supplied decision criteria, evidence, hard constraints, and known unknowns.

Missing evidence remains unknown.

## INTAKE
Required:
- `decision`
- `options`
- `decision_criteria`
- `evidence`

Optional:
- `hard_constraints`
- `known_unknowns`

## PROCESS
1. Restate the decision and hard constraints.
2. Identify viable options.
3. Apply the same decision criteria to each viable option.
4. Separate supplied evidence from inference.
5. Identify trade-offs, dependencies, and important unknowns.
6. Reject any option that violates a hard constraint.
7. Recommend the best-supported option.
8. State what new evidence or changed condition would alter the recommendation.

## RULES
- Do not fill evidence gaps with assumed facts.
- Do not change evaluation criteria selectively between options.
- Do not hide material uncertainty to make the recommendation sound stronger.
- Label inference separately from supplied evidence.

## OUTPUT CONTRACT
Return:
1. decision summary;
2. criteria table or structured comparison;
3. key evidence by option;
4. trade-offs and unknowns;
5. rejected options and reasons, if any;
6. recommendation;
7. confidence and rationale;
8. conditions that would change the recommendation.

## QUALITY GATE
The recommendation must follow from the stated criteria, constraints, and evidence. Remove unsupported certainty before finalizing.

## FALLBACK
If evidence is insufficient to choose responsibly, return the leading options, the unresolved decision factors, and the smallest additional evidence needed to decide.
