# Human Review Contract v1

Status: `DRAFT_GOVERNANCE_CONTRACT`

This contract governs cases routed by the MK0 Harvester to `HUMAN_REVIEW_REQUIRED` and sampled `GOLDEN_CANDIDATE` records during calibration.

## Reviewer authority

A reviewer may decide:

- `APPROVE_CANDIDATE` — candidate remains or becomes `GOLDEN_CANDIDATE`.
- `REJECT` — candidate is not eligible for Golden promotion.
- `CORRECT_AND_REQUEUE` — machine characterization is materially wrong; corrected fields are recorded and the item is rescored/requeued.
- `HOLD` — insufficient information or unresolved ambiguity remains.
- `ESCALATE` — requires a separate legal/provenance/source-integrity decision before any quality decision.

A reviewer does **not** directly grant `TESTED`, `IMPROVED`, `CERTIFIED`, or `PORTABLE` MK1 maturity.

## Required review receipt

Every human decision must record:

- `review_id`
- `candidate_id`
- `candidate_fingerprint`
- `policy_version`
- `reviewer_role`
- `decision`
- `decision_reason_codes`
- `rationale`
- `reviewed_at`
- `machine_confidence_at_review`
- `machine_route_at_review`
- `corrections` when applicable
- `source_commit` when committed to the repository

A changed candidate fingerprint invalidates an earlier review for automatic promotion purposes. The updated candidate must be reviewed or rerouted again.

## Human-review triggers

Mandatory review occurs when:

```text
0.90 <= aggregate_confidence < 0.95
```

or when any configured critical override demands review, even if aggregate confidence is `>= 0.95`.

During the initial calibration window, a policy-defined sample of machine auto-candidates is also reviewed.

## Review semantics

### APPROVE_CANDIDATE

Means:

> The reviewer agrees that this artifact is sufficiently characterized and valuable to remain eligible as a Golden candidate.

It does not mean:

- source claims are true beyond what was observed;
- redistribution rights exist unless independently verified;
- the prompt outperforms a baseline;
- the prompt is certified on any model/provider;
- the artifact is already `GOLDEN`.

### REJECT

Must include one or more explicit reason codes, for example:

- `LOW_INFORMATION_VALUE`
- `NEAR_DUPLICATE`
- `POOR_STRUCTURE`
- `PROVENANCE_FAILURE`
- `ACCESS_OR_LICENSE_BLOCK`
- `MISCLASSIFIED_ARTIFACT`
- `SOURCE_INTEGRITY_FAILURE`
- `NOT_REPRESENTATIVE`

### CORRECT_AND_REQUEUE

Corrections must be field-level and machine-readable. The original machine output must remain recoverable for calibration analysis.

### HOLD

Use when the reviewer cannot responsibly decide. `HOLD` is not rejection and must preserve the unresolved reason.

### ESCALATE

Use when quality judgment should not proceed until a non-quality boundary is resolved, especially licensing, provenance, source identity, or observation status.

## Promotion to Golden

Human approval alone is not Golden promotion.

```text
GOLDEN_CANDIDATE
      +
mandatory provenance/integrity gates
      +
governed promotion receipt
      =
GOLDEN
```

Promotion receipts belong under `mk0/promotions/` and must identify the exact candidate fingerprint and review/evidence inputs used.

## Calibration feedback

Human decisions are evaluation data for the Harvester.

They may be used to:

- measure reviewer-machine agreement;
- identify systematic classifier errors;
- add regression fixtures;
- adjust routing policy in a new policy version;
- improve technique/architecture mappings.

They must not silently rewrite historical scores or receipts.

## Governance invariant

```text
HUMAN INSTINCT MAY OVERRIDE MACHINE ROUTING.
HUMAN INSTINCT MAY NOT ERASE PROVENANCE OR EVIDENCE BOUNDARIES.
```
