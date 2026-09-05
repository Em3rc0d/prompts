# Prompt Machine Funnel v1

Status: `OPERATING FUNNEL / PRE-REVENUE`

Date: `2026-09-03`

## Objective

Turn qualified attention into real workflow use, trustworthy evidence, the first verified Starter purchase, successful delivery, and eventually repeat/upgrade behavior.

The shortest credible path is not `visit → checkout`. It is:

```text
CONTENT / DISCOVERY
      ↓
PROMPT MACHINE LANDING
      ↓
FREE WORKFLOW ACQUIRED
      ↓
REAL TASK STARTED
      ↓
ACTIVATED
      ↓
VALUE / TRUST EVIDENCE
      ↓
STARTER $9 OFFER
      ↓
CHECKOUT
      ↓
PROVIDER-SIGNED PURCHASE
      ↓
VERIFIED DELIVERY
      ↓
STARTER CUSTOMER
      ↓
REPEAT USE / ADJACENT NEED
      ↓
FULL $19 OFFER
      ↓
UPGRADE / REFERRAL
```

Primary commercial milestone:

`PQ-$1 = first real non-test paid purchase successfully delivered.`

## Stage 1 — Discovery

### Job
Reach people who actually experience a job Prompt Machine can help with.

Discovery channels may include:

- useful technical content;
- GitHub;
- founder-led outreach;
- referrals;
- search;
- communities;
- demonstrations built from real workflow evidence.

Content should lead with the customer job and outcome, not internal MK0/MK1/PCP terminology.

Useful message pattern:

> Stop improvising the same AI task. Use a workflow with explicit inputs, outputs, verification, limitations, and an inspectable evidence history.

## Stage 2 — Landing

A first-time visitor should quickly understand:

1. what problem Prompt Machine solves;
2. which workflow/job applies to them;
3. what they can use for free;
4. why the workflow is different from a random prompt;
5. what the $9 Starter adds;
6. what the $19 Full Collection adds;
7. what evidence exists and what remains unproven.

Primary CTA during pre-revenue validation:

`Try a free workflow on a real task.`

Paid checkout remains off until the corresponding release gate opens.

## Stage 3 — Free acquisition

Free is the acquisition and activation surface.

It must be independently useful and easy to understand.

A free acquisition can mean obtaining/accessing a workflow or collection. It is not activation.

```text
FREE_ACQUIRED != ACTIVATED
```

## Stage 4 — Real-task activation

Activation is defined by `commercial/JOB_DISCOVERY_AND_ACTIVATION_CONTRACT_V1.md`.

Canonical sequence:

```text
WORKFLOW_SELECTED
→ REAL_TASK_STARTED
→ REQUIRED_INPUTS_SUPPLIED
→ WORKFLOW_RESULT_RECEIVED
→ RESULT_VERIFICATION_UNDERSTOOD
→ ACTIVATED
```

A download, page view, prompt copy, or model response without a real task does not count as activation.

## Stage 5 — Value and trust

After activation, Prompt Machine needs evidence that the workflow was useful and understandable.

Relevant signals remain separate:

- `USER_REPORTED_OUTCOME`;
- `OBSERVED_TASK_OUTCOME` where authorized;
- repeat use;
- explicit trust/recommendation signal;
- support friction;
- known failure/limitation encountered.

Trust is strengthened by honest workflow history:

```text
what was tested
what passed
what failed
what changed
what regression passed
what is still unknown
```

Canonical policy: `docs/WORKFLOW_TRUST_HISTORY_V1.md`.

## Stage 6 — Starter $9 offer

Starter is the primary first purchase hypothesis.

Current frozen scope:

- Evidence-first Code Review;
- Evidence-first Bug Diagnosis;
- two Skill candidates;
- `START_HERE` + task chooser;
- worked examples;
- verification guidance;
- adaptation cheatsheet;
- evidence/limitations.

The ideal upgrade trigger is not artificial scarcity. It is a real need for a lower-friction, better-packaged set of workflows after the user has understood the free value.

## Stage 7 — Checkout

Checkout requirements:

- one-time payment;
- clear final price;
- exact product/version;
- license visibility;
- no fake urgency/scarcity;
- provider-signed purchase evidence;
- deterministic mapping from purchase to fulfillment;
- test orders distinguishable from real orders.

A checkout start is intent, not revenue.

## Stage 8 — Delivery

Post-purchase path:

```text
PROVIDER-SIGNED PAYMENT
→ VERIFIED FULFILLMENT
→ START_HERE
→ CHOOSE WORKFLOW
→ APPLY TO REAL TASK
→ VERIFY RESULT
```

A payment without successful fulfillment is a product failure, not a completed success story.

## Stage 9 — Starter customer

The first objective after delivery is successful use, not an immediate second sale.

Track:

- delivery success;
- paid-workflow activation;
- task-success evidence;
- confusion/support burden;
- return use.

## Stage 10 — Full $19 expansion

Full Developer Collection is an upsell/expansion hypothesis, not the default first purchase.

Upgrade becomes credible when a Starter customer exhibits broader adjacent need, reuse/adaptation demand, or desire for the full workflow system.

```text
STARTER PURCHASE != FULL DEMAND
```

## Stage 11 — Repeat / referral

The strongest early compounding signals are:

- user returns for another real task;
- user requests an adjacent workflow in the same job family;
- user upgrades;
- user refers another relevant user;
- support burden remains acceptable.

These signals influence which job family earns expansion.

## Funnel evidence hierarchy

```text
PAGE VIEW
  < CTA CLICK
  < FREE ACQUISITION
  < REAL TASK START
  < ACTIVATION
  < TASK-SUCCESS EVIDENCE
  < RETURN USE
  < CHECKOUT START
  < PROVIDER-SIGNED PURCHASE
  < VERIFIED DELIVERY
  < UPGRADE / REFERRAL
```

This is not a single quality score. Each event answers a different question.

## Funnel failure diagnostics

| Symptom | Likely problem | First action |
|---|---|---|
| Impressions but few relevant visits | weak job/message/channel fit | improve discovery message and targeting |
| Visits but few free workflow selections | unclear outcome/value | simplify job-based navigation and free promise |
| Free acquisition but no real-task starts | onboarding/input friction | improve Start Here and task chooser |
| Real-task starts but no activation | workflow/input/output friction | inspect binding, instructions and verification UX |
| Activation but weak usefulness | workflow/job mismatch or behavior failure | review real-task evidence before changing price |
| Value but no Starter interest | paid value gradient unclear | improve Starter packaging/bridge |
| Starter views but no checkout starts | offer/price/trust mismatch | inspect objections and evidence presentation |
| Checkout starts but no purchases | checkout/payment trust friction | inspect provider UX and pricing friction |
| Purchases but delivery failures | fulfillment defect | stop acquisition and repair delivery |
| Delivery but no paid activation | onboarding/product mismatch | fix paid Start Here before scaling |
| Starter use but no Full interest | Full value not needed/clear | do not force expansion; learn adjacent demand |

## First-sale operating hypotheses

Founder-led early path may be tested with small numbers, for example:

```text
relevant contacts
→ Free tries
→ real-task activations
→ value signals
→ Starter views
→ one real $9 purchase
```

Any numerical conversion assumptions are hypotheses only. At low volume, individual behavior and objections are more useful than statistically weak percentages.

## Current state

```text
PUBLIC CHECKOUT                 OFF
REAL CUSTOMER OUTCOMES          0
REAL PURCHASES                  0
PQ-$1                           NOT OBSERVED
BEHAVIORAL WORKFLOW OBSERVATIONS 7
EXPECTED-STATE MATCHES          7 / 7
READY_TO_SELL                   NO
```

## Core principle

> **The funnel is successful when a relevant person finds the right workflow, uses it on a real task, can verify the result, receives enough value to trust Prompt Machine, and eventually chooses to pay — not when traffic or downloads increase in isolation.**
