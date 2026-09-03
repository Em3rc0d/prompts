# Prompt Machine — Workflow Learning Loop v1

Status: `DESIGNED / STATICALLY GOVERNED / BEHAVIORAL LOOP NOT YET STARTED`

Date: `2026-09-03`

## 1. Purpose

Prompt Machine should improve because real workflows are used, reviewed, paid for, and revisited — not because the repository accumulates more prompt text.

The smallest compounding unit is a **workflow learning cycle**:

```text
CUSTOMER JOB
    ↓
WORKFLOW VERSION
    ↓
EXACT INVOCATION
    ↓
OBSERVATION
    ↓
REVIEW / FAILURE MINING
    ↓
DECISION
    ↓
SUCCESSOR OR RETAIN
    ↓
REGRESSION
    ↓
EVIDENCE / PRODUCT ELIGIBILITY
    ↺
```

The loop is deliberately fail-closed. A new observation may create knowledge; it may not create a maturity or marketing claim by itself.

## 2. Core rule

```text
OBSERVATION != INTERPRETATION
INTERPRETATION != IMPROVEMENT
IMPROVEMENT != REGRESSION PASS
REGRESSION PASS != CERTIFICATION
CERTIFICATION != CUSTOMER VALUE
CUSTOMER VALUE != REVENUE
REVENUE != RETENTION
```

Every transition must preserve the evidence class that actually supports it.

## 3. Workflow lifecycle

Canonical lifecycle states:

```text
CANDIDATE
  ↓
STATIC_CHECKED
  ↓
INVOCATION_FROZEN
  ↓
RUNTIME_OBSERVED
  ↓
REVIEWED
  ├── RETAIN
  ├── REWORK
  └── RETIRE

REWORK
  ↓
SUCCESSOR_BUILT
  ↓
REGRESSION_REQUIRED
  ↓
REGRESSION_PASS
  ↓
EVIDENCE_ELIGIBLE
  ↓
PRODUCT_ELIGIBLE
```

`PRODUCT_ELIGIBLE` is still not `READY_TO_SELL`. Packaging, delivery, provider custody, public-copy evidence, and commerce gates remain separate.

## 4. Observation classes

The learning loop accepts multiple evidence classes but never collapses them into one score.

```text
UNTRUSTED_CLIENT_INTENT
  click/view/CTA activity; useful for funnel diagnosis only

USER_REPORTED_OUTCOME
  voluntary user report about usefulness or task completion; valuable but self-reported

RUNTIME_OBSERVATION
  exact workflow invocation observed against an identified real runtime

HUMAN_REVIEW
  explicit assessment of an observed output against a frozen evaluation contract

REGRESSION_EVIDENCE
  successor compared against relevant prior failure and normal cases

PROVIDER_SIGNED_PURCHASE_EVIDENCE
  accepted real paid transaction from the commerce provider

DELIVERY_EVIDENCE
  verified fulfillment of the purchased artifact

RETURN_USE_EVIDENCE
  observable later use of Prompt Machine for another task when instrumentation supports it
```

No class may be silently upgraded into another.

## 5. Observation record

Every learning observation must identify:

- `observation_id`;
- workflow ID and version;
- invocation ID / composite fingerprint when applicable;
- evidence class;
- source / runtime identity;
- timestamp;
- raw evidence reference or hash;
- what was actually observed;
- explicit non-claims.

A record may say `output returned PASS`. It may not say `workflow is reliable` unless a separate governed decision supports that claim.

## 6. Review and failure mining

A review packet evaluates one or more observations against a frozen contract.

Failure taxonomy v1:

```text
INSTRUCTION_DATA_BOUNDARY_FAILURE
UNSUPPORTED_MATERIAL_CLAIM
MISSING_REQUIRED_INPUT_NOT_BLOCKED
WRONG_STATE
OUTPUT_CONTRACT_FAILURE
AUTHORITY_ESCALATION
UNCERTAINTY_COLLAPSE
CONTRADICTION_MISHANDLED
VERIFICATION_GAP
TASK_FAILURE
UX_FRICTION
NO_FAILURE_OBSERVED
```

A failure record must preserve:

```text
BEFORE
OBSERVED FAILURE
WHY IT MATTERS
HYPOTHESIS
PROPOSED CHANGE
REGRESSION CASES REQUIRED
```

The hypothesis is not evidence that the proposed change works.

## 7. Decision packet

After review, one explicit decision is emitted:

```text
RETAIN
REWORK
RETIRE
EXPAND_EVIDENCE
```

Decision meanings:

- `RETAIN`: no material change justified by current evidence; does not mean perfect.
- `REWORK`: at least one material failure or recurring friction justifies a successor.
- `RETIRE`: workflow should stop being promoted or advanced.
- `EXPAND_EVIDENCE`: current evidence is insufficient to choose RETAIN/REWORK/RETIRE; collect a bounded additional observation set.

Every decision must cite the observation/review IDs that support it and list unresolved unknowns.

## 8. Successor discipline

Never overwrite a behaviorally observed version.

```text
v1.0 observed
   ↓ failure
v1.1 successor
   ↓ regression
compare v1.0 ↔ v1.1
```

Required successor record:

- predecessor ID/version/hash;
- change hypothesis;
- exact changed semantics;
- intended failure addressed;
- possible regressions introduced;
- required regression set.

## 9. Regression gate

A successor may not inherit its predecessor's evidence.

Minimum regression set includes:

1. the exact case that motivated the successor;
2. at least one normal case;
3. any adversarial/instruction-data case touched by the change;
4. any state/output-contract case touched by the change.

Regression result:

```text
PASS
FAIL
INCONCLUSIVE
```

Only `PASS` may make the successor `EVIDENCE_ELIGIBLE`.

## 10. Customer-value loop

Behavioral correctness is only one part of learning.

After public usage begins, workflow decisions should also consider:

```text
DISCOVERY
Can the target user find the workflow?

ACTIVATION
Can they supply the required inputs and reach a useful result?

VERIFICATION
Can they understand whether the result is safe/useful enough for the intended task?

RETURN
Do they come back for another real task?

PAYMENT
Does broader/reduced-friction value earn a purchase?

SUPPORT BURDEN
Does the workflow create confusion, refunds, or repetitive support work?
```

These dimensions remain separate from model-behavior evidence.

## 11. Capital allocation from the loop

The loop chooses what deserves the next unit of time or money.

```text
failure in usefulness      → improve workflow/customer surface
failure in discovery       → improve distribution/message
failure in activation      → improve onboarding/input binding
failure in trust           → improve examples/evidence/verification
failure in monetization    → inspect value ladder before price
failure in retention       → inspect repeat jobs and ongoing value
insufficient evidence      → smallest bounded experiment
```

Do not respond to weak revenue by generating more inventory by default.

## 12. Scaling rule

A workflow family earns scale only after the small loop works.

```text
1 useful workflow
→ repeated successful use
→ bounded failures understood
→ successor/regression mechanism works
→ first paid demand
→ repeat/referral signal
→ THEN more workflows in the same job family
```

The scale unit is a proven **job family**, not a profession and not a prompt count.

## 13. Immediate Prompt Machine application

Current next observation remains deliberately small:

```text
PM-INV-CHECKLIST-NORMAL-0003
```

It is prepared but not executed.

When a real runtime observation is eventually authorized, the required path is:

```text
1 runtime observation
→ HUMAN_REVIEW
→ RETAIN / REWORK / RETIRE / EXPAND_EVIDENCE
→ only then decide whether to execute EMBEDDED_OVERRIDE
```

No automatic wave is allowed.

## 14. North-star loop

The strongest long-term signal is not prompt count or page views.

> A person uses a Prompt Machine workflow on a real task, receives a useful verifiable result, returns for another task, and the evidence from those interactions makes the system better.

Commercial compounding appears when that loop also produces purchases, upgrades, referrals, and low support burden.

## 15. Truth boundary

```text
MORE DATA      != MORE VALUE
MORE WORKFLOWS != MORE PRODUCT-MARKET FIT
MORE TESTS     != BETTER WORKFLOW
MORE TRAFFIC   != BETTER BUSINESS

BETTER EVIDENCE
+ BETTER DECISIONS
+ BETTER WORKFLOWS
+ BETTER DISTRIBUTION
+ VERIFIED CUSTOMER VALUE
= COMPOUNDING SYSTEM
```
