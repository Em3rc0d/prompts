# Workflow Static Review Checklist

Status: `DRAFT / CUSTOMER-FACING QUALITY TOOL`

Use this checklist before runtime testing a Prompt Quarry workflow or one of your adaptations.

A static PASS means the workflow contract is coherent enough to test. It does **not** mean the workflow has been behaviorally TESTED, IMPROVED, CERTIFIED, or shown PORTABLE.

## A. Outcome

- [ ] The workflow states a concrete outcome rather than only assigning a persona.
- [ ] The outcome is narrow enough that a consumer can tell when the task is complete.
- [ ] Suggested implementation is not confused with the actual desired outcome.

## B. Inputs

- [ ] Required inputs are explicit.
- [ ] Optional inputs are separated from blockers.
- [ ] Missing required input behavior is defined.
- [ ] Ambiguous input behavior is defined when ambiguity can change the result.
- [ ] Filler context is not required merely to make the prompt look detailed.

## C. Context and provenance

- [ ] Allowed context/source classes are explicit.
- [ ] External research/tool use is either allowed or disallowed explicitly where relevant.
- [ ] Freshness requirements exist where stale information can change the result.
- [ ] Citation requirements exist where source claims matter.
- [ ] Unavailable information is treated as unknown rather than invented.

## D. Evidence semantics

- [ ] The workflow defines evidence/certainty labels appropriate to the task.
- [ ] Fact/source claim/inference/assumption are not silently collapsed.
- [ ] Strong conclusions have a stated evidence threshold.
- [ ] Missing evidence causes downgrade/hold/escalation instead of fabricated certainty.
- [ ] Local evidence labels are not confused with Prompt Quarry F4–F7 product evidence states.

## E. Constraints and policy

- [ ] Must / must-not behaviors are explicit where material.
- [ ] Important invariants are preserved.
- [ ] Conflicting priorities have an explicit order or trade-off rule.
- [ ] Team policy choices are configurable rather than hidden in adjectives like “strict” or “careful.”

## F. Process

- [ ] Each process step has a task-specific purpose.
- [ ] The workflow does not require unnecessary reasoning theater or generic filler.
- [ ] Candidate conclusions/findings are challenged before reporting where false positives matter.
- [ ] The process includes a way to surface fragile assumptions or contradictory evidence.

## G. Decision / escalation

- [ ] Stable decision or escalation states are named.
- [ ] Transitions into stronger states are defined by evidence/conditions.
- [ ] A `HOLD`, `BLOCKED`, `REVIEW_REQUIRED`, or equivalent state exists when forcing completion would be unsafe or misleading.
- [ ] Human vs automated authority is explicit where the workflow can affect shipping, production, security, data, or purchasing decisions.

## H. Output contract

- [ ] Required output sections are explicit.
- [ ] Each output section has a downstream consumer or inspection purpose.
- [ ] Material uncertainty remains visible in the output.
- [ ] The output is stable enough to compare across repeated runs where repeatability matters.
- [ ] Machine-readable output is used only when its field semantics are defined.

## I. Verification

- [ ] The workflow defines checks that can be applied to its own output.
- [ ] Verification distinguishes contract compliance from factual/runtime correctness.
- [ ] Domain-specific verification is requested where appropriate: tests, reproduction, measurements, source checks, monitoring, etc.
- [ ] A local contract PASS is not described as behavioral proof.

## J. Fallback

- [ ] The workflow defines what happens when evidence is insufficient.
- [ ] The fallback returns the smallest additional evidence/context needed.
- [ ] Safe partial results are preserved where useful.
- [ ] The fallback does not pad uncertainty with generic advice.

## K. Adaptability

- [ ] Policy values are distinguishable from per-run instance data.
- [ ] Another engineer can identify which fields to change for their team.
- [ ] Adaptation does not require reverse-engineering why every section exists.
- [ ] The workflow can be represented as prompt/config/form/schema without weakening core semantics where integration matters.

## L. Free-vs-Paid value check

For Developer Pack v1.1 core assets:

- [ ] The asset provides a reusable construction/governance capability, not merely another finished prompt.
- [ ] The asset cannot be replaced by copying a Free Starter prompt and changing domain nouns.
- [ ] Parameterization is explicit.
- [ ] Governance is explicit.
- [ ] Verification is explicit.
- [ ] Integration/adaptation value is visible.

## Static result

Choose one:

```text
STATIC_READY_FOR_RUNTIME_TEST
STATIC_READY_WITH_KNOWN_GAPS
STATIC_REWORK_REQUIRED
```

Record blocking gaps:

- `[GAP]`
- `[GAP]`

## Evidence boundary

This checklist reviews static workflow design only.

```text
STATIC_READY != F4 TESTED
F4 TESTED != F5 IMPROVED
F5 IMPROVED != F6 CERTIFIED
F6 CERTIFIED != F7 PORTABLE
```
