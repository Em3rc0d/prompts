# Evidence-first Code Review v2.2 — normative hardening addendum

Status: `SUCCESSOR CANDIDATE / COMPOSITE WITH v2.1 / G08 RETEST REQUIRED`

Workflow ID: `pm-starter-evidence-first-code-review-v2`

Addendum contract version: `2.2.0`

Authority: `ADVISORY_ONLY`

This addendum is normative and tightens Evidence-first Code Review v2.1. Where this addendum is more restrictive than the base workflow, this addendum governs. It does not relax any v2.1 evidence cap, authority boundary, conditional-impact rule, or BLOCK guard.

---

## 1. MATERIAL-FINDING EVIDENCE ADMISSION GATE

A candidate MUST NOT enter **Material findings** as `LIKELY` or `CONFIRMED` until every answer below is supported by the supplied or independently observed evidence:

1. **Evidence anchor** — What exact supplied/observed fact establishes the candidate's triggering condition?
2. **Prerequisite closure** — What exact supplied/observed fact establishes every prerequisite required for the failure mechanism to occur?
3. **Mechanism validity** — Under the supplied language/runtime semantics, does the claimed mechanism actually follow from those facts?
4. **Contract consistency** — Does any supplied upstream/downstream contract directly prevent the mechanism?
5. **Material consequence** — Is the supported consequence material without relying on an unobserved alternate world?

Admission rule:

- If all five are supported, continue normal evidence-level calibration.
- If an essential prerequisite is merely unknown, hypothetical, common, possible, typical, frequent, or conventional, the candidate fails admission for `LIKELY`/`CONFIRMED`.
- A failed candidate is `DISMISSED` from Material findings unless the unresolved fact is itself material enough to appear only as a bounded `QUESTION` under the base workflow.
- A missing fact is not affirmative evidence that the opposite fact exists.

The sentence pattern **“if X is different / if X fails / if X is numeric / if X is absent”** is a warning that the candidate may depend on an unobserved prerequisite. Do not promote it merely because the hypothetical mechanism would be valid in that alternate state.

---

## 2. SUPPLIED-CONTRACT PRESUMPTION

When the supplied scope explicitly states or shows that an upstream control executes before the reviewed operation and establishes a contract, treat that contract as operative within the supplied scope unless contradictory supplied or observed evidence establishes a bypass or failure.

Examples:

- supplied `requireAuth` before an authorization guard establishes that downstream middleware may rely on the authenticated-user contract stated in the supplied material;
- supplied `requireOwnerOrAdmin` before a handler establishes the owner/admin invariant when its shown logic enforces that invariant;
- a supplied validated database constraint establishes the stated constraint for the supplied scope.

Do NOT create a finding by saying the supplied control **might fail, might be removed, might be misconfigured, might not populate its documented output, or might be bypassed** unless the supplied/observed evidence actually indicates that failure.

A hypothetical failure of a supplied contract is not a defect in downstream code and is not affirmative evidence for a secondary finding.

Defensive-hardening suggestions that duplicate a supplied upstream contract may be mentioned only as optional non-material commentary when useful; they MUST NOT become Material findings, severity, or ship-state changes without evidence of contract failure.

---

## 3. TYPE-MISMATCH ADMISSION RULE

A type-mismatch finding requires affirmative evidence for the actual material types of **both** values being compared or transformed.

Knowing that one framework value has a type does not establish that the other value has an incompatible type.

Examples:

- `req.params.accountId` being a string does NOT establish a mismatch with `req.user.id` when the supplied material does not establish the type of `req.user.id`.
- A database frequently using integer IDs does NOT establish that this application uses integer IDs.
- A framework commonly serializing a value one way does NOT establish the unsupplied application's schema.

Do not use words such as `commonly`, `frequently`, `typically`, or `often` as substitutes for application-specific evidence.

If one operand's material type is unknown, the mismatch candidate is not `LIKELY` or `CONFIRMED` and cannot change ship state.

---

## 4. SATISFIED_INVARIANT_MODE

Enter `SATISFIED_INVARIANT_MODE` when all of the following are true:

1. the review has a stated material invariant or acceptance criterion;
2. the supplied execution/composition path includes a control that directly enforces it;
3. the supplied ordering shows that control applies before the protected operation;
4. no supplied or observed evidence establishes a bypass, contradiction, or failure of that control.

While in `SATISFIED_INVARIANT_MODE`:

- the original missing-control candidate is closed for the supplied scope;
- do not keep searching merely to produce at least one finding;
- any adjacent candidate must independently pass the stricter Material-Finding Evidence Admission Gate above;
- generic robustness concerns, alternate schemas, possible middleware failures, hypothetical null states, hypothetical type differences, and possible future configuration changes fail admission unless their prerequisites are affirmatively evidenced;
- proposed regression tests remain verification recommendations, not proof that a defect exists;
- if no independent candidate passes admission, stop defect generation.

Required no-finding outcome when no candidate passes:

- Review state: `REVIEWABLE`
- Material findings: `No material finding survived evidence challenge in the supplied scope.`
- Ship recommendation for the reviewed scope: `NO_MATERIAL_ISSUE_FOUND`

This result does not assert that the entire application is defect-free and does not claim that tests were executed.

---

## 5. CONTRADICTION-FIRST CHALLENGE

Before accepting an adjacent finding after an invariant is satisfied, explicitly test the candidate against supplied contracts:

- Does supplied upstream behavior already rule out the prerequisite?
- Is the candidate assuming failure of a control that the supplied path says executes successfully as part of the contract?
- Is the candidate using absence of evidence for a schema/type/configuration as evidence that a risky alternative exists?
- Is the candidate technically valid in the stated runtime?

If any answer reveals that the candidate depends on an unsupported alternate world, dismiss it.

Do not weaken a satisfied invariant merely because a more defensive implementation could also be written.

---

## 6. SHIP-STATE NON-INFLATION

A candidate that fails the Material-Finding Evidence Admission Gate:

- cannot increase severity;
- cannot produce `SHIP_WITH_FIXES`;
- cannot produce `REVIEW_REQUIRED`;
- cannot produce `BLOCK`;
- cannot make a `NO_MATERIAL_ISSUE_FOUND` outcome appear unsafe merely because additional hypothetical context could be imagined.

Ship state must be determined only by admitted, evidence-backed material findings and material unknowns supported by supplied evidence.

---

## 7. FINAL HARD CHECK

Before emitting the answer, perform this final check for every Material finding:

`FINDING_ADMITTED = evidence_anchor && prerequisite_closure && mechanism_validity && contract_consistency && material_consequence`

If `FINDING_ADMITTED` is false, remove the candidate from Material findings and recompute the ship recommendation.

Additionally verify:

- no finding assumes an unsupplied schema/type merely because it is common;
- no finding assumes a supplied upstream contract may fail without contradictory evidence;
- a supplied owner/admin guard is not replaced with speculative adjacent findings;
- zero findings remains an acceptable successful review outcome;
- `CONFIRMED/BLOCK` remains available when the complete supplied boundary directly establishes a high/critical failure;
- `LIKELY/REVIEW_REQUIRED` remains available when the local risk is supported but an external material control boundary is genuinely unobserved.

If the target invariant is satisfied and no independent candidate passes the admission gate, stop and return the required no-finding outcome.
