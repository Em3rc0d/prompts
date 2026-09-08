# Starter Collection — Verification Guide

Status: `CUSTOMER SURFACE CANDIDATE / NOT FOR SALE`

Prompt Machine does not treat a model response as proof merely because it is structured or confident.

Use this guide after any material Code Review or Bug Diagnosis result.

## Universal verification questions

1. What is directly supported by supplied evidence?
2. What is inference?
3. What remains unknown?
4. Which claim has the highest consequence if wrong?
5. What exact evidence supports that claim?
6. What check can prove or disprove it?
7. Does the recommendation require a human production/ship decision?

## Code Review

For each material finding verify:

- the cited location exists in the supplied change;
- the described failure mechanism follows from the code/context;
- severity matches plausible impact;
- any runtime/test claim is backed by actual supplied evidence;
- the recommended fix addresses the mechanism rather than only the symptom;
- the verification step would detect the regression.

Treat `LIKELY` and `QUESTION` as unresolved until the missing material fact is established.

`NO_MATERIAL_ISSUE_FOUND` means no material issue was supported in the supplied scope. It does not prove defect-free software.

## Bug Diagnosis

Verify that:

- the observation ledger contains observations, not unlabeled assumptions;
- hypotheses are distinct mechanisms;
- ranking follows evidence rather than familiarity;
- proposed checks have different expected outcomes when hypotheses are true/false;
- risky actions are labeled with approval requirements;
- mitigation is not treated as causal proof;
- `CAUSE_CONFIRMED` is used only when the confirmation threshold is actually supported;
- verification checks both symptom resolution and the proposed mechanism.

## Stop conditions

Do not act automatically when:

- the highest-impact claim is unsupported;
- required context is missing;
- a production-changing action lacks authorization;
- destructive action is proposed before a reversible diagnostic can answer the question;
- the answer silently upgrades an inference into an observation;
- the answer claims tests/deployment/runtime state that were never supplied.

## Evidence update

If new evidence changes the situation, supply it explicitly and rerun/re-evaluate the workflow. Do not pretend the original response already knew facts that arrived later.

> **Verification is part of the workflow, not an optional disclaimer after it.**
