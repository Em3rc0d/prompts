# Worked Transformation — From “Review this code” to a Team Review Contract

Status: `DRAFT EXAMPLE`

Purpose: demonstrate that Developer Pack v1.1 is a construction system, not merely a collection of finished prompts.

This example does not claim behavioral superiority. It shows how to configure the reusable `templates/software-code-review-system.md` interface for a concrete team workflow.

---

## 1. Starting request

A team begins with:

> Review this PR and tell me if anything is wrong.

Problems:

- no definition of material risk;
- no evidence threshold;
- no repository/runtime context;
- no agreement on security/data concerns;
- no ship-decision policy;
- no stable output that can be reused in PR review.

## 2. Extract the workflow requirements

Team context:

- TypeScript / Next.js application;
- PostgreSQL persistence;
- authenticated customer routes;
- review is advisory to a human reviewer;
- team wants correctness, security, data-integrity, compatibility, and regression findings;
- style feedback is handled by linting and should not appear;
- test claims must come from supplied CI/test evidence.

Team policy:

```text
reporting threshold     CONFIRMED or LIKELY
minimum severity        MEDIUM
max findings            8
ship authority          HUMAN_DECIDES
confirmed HIGH+         recommend BLOCK
likely HIGH             recommend REVIEW_REQUIRED
medium/low bounded      recommend SHIP_WITH_FIXES
no material evidence    NO_MATERIAL_ISSUE_FOUND
```

## 3. Configure the reusable template

### Review policy

```text
workflow_name    pq-team-pr-review
review_target    PR / diff
consumer         author + human reviewer
ship_authority   HUMAN_DECIDES
```

### Required inputs

```text
- PR diff or changed files
- change intent / acceptance criteria
- relevant runtime context
```

Conditional inputs:

```text
- schema/API contract when changed
- auth model for protected routes
- migration when persistence changes
- supplied CI/test output if available
```

### Enabled lenses

```text
[x] correctness
[x] regression risk
[x] security / trust boundary
[x] data integrity
[x] API / schema compatibility
[x] tests / verification
[ ] pure style
```

### Evidence policy

```text
CONFIRMED = directly supported by code/context
LIKELY    = strong inference with one material unobserved fact
QUESTION  = needs context before it can become a defect
```

### Verification policy

Every reported finding must include:

```text
location
+ evidence
+ failure mechanism
+ impact
+ smallest useful fix
+ verification
+ invalidating context
```

## 4. Resulting team operating prompt

The team can now instantiate the system as:

```text
You are running the pq-team-pr-review workflow.

INPUTS
- Review target: [PR DIFF / FILES]
- Change intent: [ACCEPTANCE CRITERIA]
- Runtime context: TypeScript, Next.js, PostgreSQL
- Relevant contracts: [API / SCHEMA / AUTH / NONE]
- Observed test evidence: [CI / TEST OUTPUT / NONE OBSERVED]

REVIEW POLICY
Review only for:
- correctness;
- regression risk;
- security/trust boundaries;
- data integrity;
- API/schema compatibility;
- verification gaps tied to concrete changed behavior.

Do not report pure style preferences.

EVIDENCE
Label findings CONFIRMED, LIKELY, or QUESTION.
Do not claim runtime behavior or passing tests without supplied evidence.
Every accepted finding must identify exact evidence and explain a concrete failure mechanism.

REPORTING THRESHOLD
- report CONFIRMED or LIKELY findings;
- report MEDIUM severity or higher;
- maximum 8 findings;
- include QUESTION only if it can change the ship recommendation.

SHIP POLICY
- confirmed HIGH/CRITICAL -> BLOCK;
- likely HIGH with material unknown -> REVIEW_REQUIRED;
- bounded MEDIUM findings -> SHIP_WITH_FIXES;
- no supported material finding -> NO_MATERIAL_ISSUE_FOUND.

OUTPUT
1. Review state
2. Executive assessment
3. Findings ordered by severity
4. Material missing context
5. Verification plan
6. Ship recommendation

For every finding return:
severity, evidence level, location, evidence, failure mechanism, impact, recommended fix, verification, invalidating context, confidence.

If context is insufficient for a responsible review, return REVIEW_REQUIRED and ask only for information capable of changing the assessment.
```

## 5. What the Paid system added

A finished Free Code Review prompt already gives a strong default workflow.

The Paid system adds the reusable design surface:

| Capability | Finished Free prompt | Configured Paid system |
|---|---:|---:|
| Immediate code review | yes | yes |
| Team-specific lenses | adapt manually | explicit configuration |
| Reporting threshold | fixed default | configurable |
| Severity policy | fixed default | replaceable team policy |
| Ship authority | implicit/human | explicit |
| Ship transitions | default | configurable rules |
| Integration shape | prompt | PR / CI / agent / generator |
| Repeatable team policy | possible by editing | first-class contract |
| Inspectable configuration | limited | explicit adaptation map |

The value difference is not “more words”. It is the ability to define and preserve a reusable review policy.

## 6. Inspection checklist

This transformation passes only if another engineer can answer:

- What inputs are required?
- Which review lenses are active?
- Which evidence levels can be reported?
- What severity threshold is used?
- Who actually decides whether to ship?
- What causes BLOCK vs REVIEW_REQUIRED?
- What must every finding contain?
- What evidence would invalidate a finding?

If those answers disappear when the prompt is shortened, they are operational semantics and should remain explicit.
