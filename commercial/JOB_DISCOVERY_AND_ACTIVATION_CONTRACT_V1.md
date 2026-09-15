# Prompt Machine — Job Discovery and Activation Contract v1

Status: `OPERATING CONTRACT / HYPOTHESES NOT YET MARKET-VALIDATED`

Date: `2026-09-03`

## 1. Purpose

Prompt Machine should not expand by generating more prompts or profession packs by default. It should expand by identifying **valuable repetitive customer jobs** that can be converted into reliable reusable workflows and then learning from real use.

This contract defines:

1. what counts as a customer job worth investigating;
2. what evidence is required before a job becomes a workflow candidate;
3. what counts as user activation;
4. how customer use enters the Workflow Learning Loop without overfitting to noisy feedback;
5. when a workflow/job family earns more product investment.

Canonical path:

```text
DISCOVER valuable repetitive job
→ OBSERVE evidence of the job
→ QUALIFY
→ BUILD governed workflow candidate
→ STATIC CHECK
→ exact invocation
→ bounded runtime observation
→ review / failure mining
→ improve / regress when justified
→ real customer task use
→ activation / value evidence
→ paid offer when earned
→ repeat / referral evidence
→ scale the job family
```

## 2. Customer job definition

A `CUSTOMER_JOB` is a concrete outcome a person is trying to achieve under identifiable constraints.

Good job framing:

> "Review a code change and identify evidence-backed defects before merge."

Weak job framing:

> "Developer prompts."

Profession, industry, model, and tool are metadata. The primary unit is the outcome.

A job record should identify:

- desired outcome;
- trigger/context;
- current manual or improvised process;
- inputs normally available;
- expected output;
- verification method;
- frequency;
- pain/friction;
- consequence of poor execution;
- current alternatives;
- target user/persona metadata;
- evidence source.

## 3. Job lifecycle

```text
DISCOVERED
  ↓
OBSERVED
  ↓
QUALIFIED
  ↓
WORKFLOW_CANDIDATE
  ↓
PILOTED
  ├── PROVEN_FOR_CURRENT_SCOPE
  ├── NEEDS_MORE_EVIDENCE
  ├── REWORK
  └── REJECTED
```

Meanings:

- `DISCOVERED`: plausible job identified from research, conversation, support, community evidence, or founder observation.
- `OBSERVED`: at least one concrete instance/evidence source shows the job actually occurs.
- `QUALIFIED`: evidence supports spending bounded effort to workflowize it.
- `WORKFLOW_CANDIDATE`: a governed workflow contract exists for the job.
- `PILOTED`: at least one bounded execution or real-task use has been reviewed.
- `PROVEN_FOR_CURRENT_SCOPE`: enough evidence exists to continue investment for the explicitly bounded job/user scope; not universal product-market fit.
- `NEEDS_MORE_EVIDENCE`: signal exists, but next decision requires another bounded observation.
- `REWORK`: evidence reveals a material workflow/product problem.
- `REJECTED`: current evidence does not justify continued investment.

## 4. Qualification dimensions

A job should be considered through six separate dimensions:

```text
FREQUENCY
How often does this job recur for the same person or across reachable users?

PAIN
How much time, cognitive load, uncertainty, delay, or frustration does it create?

VALUE
What useful time, quality, risk reduction, or economic value can a better workflow create?

WORKFLOWIZABILITY
Can the job be represented with bounded inputs, procedure, output contract, state rules, and verification?

REACHABILITY
Can Prompt Machine realistically reach people who experience this job?

SAFE DELIVERABILITY
Can the workflow be delivered responsibly under our current authority, evidence, privacy, and domain-safety boundaries?
```

Qualitative Job Opportunity Score:

```text
Frequency
× Pain
× Value
× Workflowizability
× Reachability
× Safe Deliverability
```

This is a prioritization model, not a validated mathematical formula. Do not invent numeric precision or weights until evidence supports them.

Recommended rating values:

```text
HIGH
MEDIUM
LOW
UNKNOWN
BLOCKED
```

A single `BLOCKED` safety/deliverability dimension can stop advancement regardless of the other ratings.

## 5. Evidence that can qualify a job

Useful evidence classes include:

- repeated direct customer/user statements;
- observed repeated founder/manual work;
- support requests;
- search/community discussions;
- existing workaround behavior;
- repeated use of a free workflow;
- customer requests for adjacent capability;
- return use;
- actual purchase/upgrade behavior;
- task artifacts that show repeated structure.

Evidence must retain provenance.

A job does **not** become validated merely because:

- it sounds useful;
- an LLM generated the idea;
- one competitor offers it;
- a social post received views;
- one person said they "would pay";
- a prompt exists for it;
- it belongs to a large profession.

## 6. Minimum qualification gate

Before `QUALIFIED`, answer:

```text
JOB
What outcome is repeatedly sought?

WHO
Who experiences it?

WHEN
What triggers it?

CURRENT BEHAVIOR
How is it solved today?

PAIN / VALUE
Why does improvement matter?

WORKFLOW CONTRACT
Can inputs, outputs, constraints and verification be bounded?

EVIDENCE
What concrete observations support the opportunity?

NEXT EXPERIMENT
What is the smallest test capable of changing the decision?
```

Unknowns remain explicit.

## 7. Activation definition

Prompt Machine activation is **not** a page view, click, download, or checkout visit.

Canonical activation path:

```text
VISITOR
  ↓
FREE_ACQUIRED
  ↓
WORKFLOW_SELECTED
  ↓
REAL_TASK_STARTED
  ↓
REQUIRED_INPUTS_SUPPLIED
  ↓
WORKFLOW_RESULT_RECEIVED
  ↓
RESULT_VERIFICATION_UNDERSTOOD
  ↓
ACTIVATED
```

For v1, a user is `ACTIVATED` only when there is evidence that they applied a Prompt Machine workflow to a real task and reached a result they can inspect against the workflow's verification guidance.

`ACTIVATED` does not mean the result was correct, valuable, paid for, or repeated.

## 8. Value evidence after activation

Keep these signals distinct:

```text
ACTIVATED
real task reached an inspectable workflow result

TASK_SUCCESS_EVIDENCE
result was reported or observed as useful enough for the intended task

REPEAT_USE
same user returns for another real workflow/task

TRUST_SIGNAL
user explicitly relies on, recommends, saves, reuses, or cites the workflow because of observed value/trust

PURCHASE
provider-signed real paid transaction

DELIVERY
purchased artifact successfully fulfilled

UPGRADE
real purchase from Starter to broader paid collection

REFERRAL
another relevant user arrives through a traceable recommendation where instrumentation supports it
```

Do not collapse these into one "success" metric.

## 9. Task-success evidence

`TASK_SUCCESS_EVIDENCE` may be:

```text
USER_REPORTED_OUTCOME
user says the result solved or materially helped the real task

OBSERVED_TASK_OUTCOME
authorized evidence directly demonstrates task completion/usefulness
```

Self-report must remain labeled self-report.

A model grading its own answer is not customer task-success evidence.

## 10. Feedback ingestion

Customer feedback is evidence, not an automatic specification change.

```text
feedback
→ classify
→ connect to workflow/job/version
→ check recurrence/materiality
→ HUMAN_REVIEW
→ RETAIN / REWORK / EXPAND_EVIDENCE / product-surface change
```

Do not automatically rewrite a workflow because one user dislikes an output style or requests a feature.

Before changing workflow semantics, ask:

- is this a correctness failure or preference?
- is it specific to one task/context?
- is it recurring across evidence?
- does it violate the existing contract?
- could the change regress other observed cases?
- can routing/configuration solve it without mutating the architecture?

## 11. Guard against one-user overfitting

One observation can justify investigation. It rarely justifies a universal product change.

Default interpretation:

```text
1 signal
→ investigate / reproduce / classify

repeated aligned signals
→ stronger rework or product hypothesis

behavioral + customer-value + repeat evidence
→ candidate for job-family scaling
```

Material safety/correctness failures are exceptions: one severe observed failure may justify an immediate stop-line or rework.

## 12. Minimal instrumentation

Collect only what is required to understand the job and learning loop.

Useful identifiers where available/consented:

```text
anonymous session / user reference
job_id
workflow_id
workflow_version
invocation/reference ID when applicable
task_started
task_result_reached
verification_viewed / acknowledged where meaningful
user-reported usefulness
return use
purchase/delivery evidence reference
source/campaign metadata
```

Do not collect task contents or personal data merely because they would make analytics richer. Prefer event references, hashes, bounded metadata, and explicit consent where task evidence is retained.

## 13. What does not count as activation

```text
landing_view              != activation
free_cta_clicked          != activation
free_pack_acquired        != activation
workflow_page_view        != activation
copy_prompt_clicked       != activation
model_response_generated  != activation by itself
paid_product_viewed       != activation
checkout_started          != activation
```

These are useful funnel signals but cannot replace real-task use.

## 14. Monetization eligibility

A workflow/job family does not earn a paid expansion merely because behavioral tests pass.

Preferred progression:

```text
behaviorally bounded
→ real-task activation observed
→ value signal observed
→ repeat / adjacent-demand signal
→ paid offer hypothesis
→ real purchase + delivery
→ repeat / upgrade / referral learning
```

For the first Starter offer, founder-led selling may begin earlier as an explicit commercial experiment, but all outcomes remain evidence classes rather than proof of durable demand.

## 15. Scale gate

A job family earns expansion when evidence begins to support all of the following:

```text
REAL JOB EXISTS
WORKFLOW CAN EXECUTE IT
FAILURES ARE BOUNDED / LEARNABLE
USER CAN ACTIVATE
USER RECEIVES VALUE
REPEAT OR ADJACENT DEMAND EXISTS
COMMERCIAL SIGNAL EXISTS OR IS BEING TESTED
SUPPORT BURDEN IS ACCEPTABLE
```

If one layer is weak, invest in that layer before generating more neighboring workflows by default.

## 16. Current Prompt Machine implication

Prompt Machine is currently in `PRE-REVENUE PRODUCT HARDENING`.

The architecture/binding/learning infrastructure exists and seven low-risk behavioral observations are recorded. Real customer outcomes, repeat-use evidence and real purchases remain unobserved.

Therefore the next large strategic milestone is not "more prompts". It is building the bridge from governed workflows to real customer jobs:

```text
qualified job
→ governed workflow
→ real task
→ activation
→ value evidence
→ trust history
→ paid experiment
```

The manual architecture campaign may continue when usage budget permits, but customer-job discovery and activation instrumentation can advance without model spend.

## 17. Master rules

> **The unit of expansion is a proven job family, not a prompt count.**

> **A user is not activated because they downloaded something; they are activated when they use a workflow on a real task and reach an inspectable result.**

> **Feedback updates evidence first. It updates the workflow only after a governed decision.**

> **Spend the minimum evidence required to unlock the next decision.**
