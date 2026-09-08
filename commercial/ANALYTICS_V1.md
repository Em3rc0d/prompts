# Prompt Machine Analytics v1

Status: `MINIMAL INSTRUMENTATION CONTRACT / PRE-REVENUE`

Date: `2026-09-03`

## Objective

Measure whether Prompt Machine can move a relevant person from discovery to **real-task workflow use**, observable value, paid demand, verified delivery, and repeat behavior without building an invasive analytics stack.

Analytics supports decisions. It does not create stronger evidence classes than the underlying event/source actually provides.

## North-star direction

The strongest long-term signal is:

```text
real task
→ activated workflow use
→ useful/verifiable result
→ return use
→ purchase / upgrade / referral when value earns it
```

The first commercial milestone remains:

`PQ-$1 = first real non-test paid purchase successfully delivered.`

A client analytics event cannot establish PQ-$1 if provider/payment/delivery evidence does not agree.

## Core event taxonomy

### Discovery / acquisition

```text
landing_view
workflow_catalog_viewed
free_cta_clicked
free_workflow_acquired
workflow_selected
```

### Activation

```text
real_task_started
required_inputs_supplied
workflow_result_reached
verification_guidance_viewed
activation_completed
```

### Value / trust

```text
task_outcome_reported
workflow_helpful_reported
workflow_limitation_reported
workflow_failure_reported
trust_history_viewed
repeat_workflow_use
adjacent_workflow_requested
```

### Monetization

```text
starter_product_viewed
starter_cta_clicked
starter_checkout_started
starter_purchase_client_event
starter_delivery_observed
full_product_viewed
full_cta_clicked
full_checkout_started
full_purchase_client_event
full_delivery_observed
```

### Expansion

```text
starter_to_full_upgrade_observed
referral_observed
return_use_observed
```

Event names may evolve with implementation, but evidence semantics must remain stable.

## Activation contract

`activation_completed` is permitted only when the implementation has evidence for the canonical sequence:

```text
WORKFLOW_SELECTED
→ REAL_TASK_STARTED
→ REQUIRED_INPUTS_SUPPLIED
→ WORKFLOW_RESULT_RECEIVED
→ RESULT_VERIFICATION_UNDERSTOOD
```

If instrumentation cannot establish all of these, record the lower-level events rather than inventing activation.

```text
free_workflow_acquired != activation_completed
workflow_result_reached != task success
```

Canonical definition: `commercial/JOB_DISCOVERY_AND_ACTIVATION_CONTRACT_V1.md`.

## Event contract

Use minimum metadata required for attribution and diagnosis.

Example:

```json
{
  "event": "real_task_started",
  "timestamp": "ISO-8601",
  "session_id": "anonymous-or-consented-id",
  "job_id": "code-review",
  "workflow_id": "evidence-first-code-review",
  "workflow_version": "known-version-or-null",
  "product_tier": "free",
  "source": "linkedin",
  "medium": "organic",
  "campaign": "pm-launch-0",
  "content": "code-review-evidence-story"
}
```

Do not include task contents, source code, private documents, or personal data merely for analytics convenience.

## Acquisition taxonomy

Canonical attribution fields where useful:

- `source`: linkedin, github, direct, referral, search, community, other;
- `medium`: organic, profile, post, dm, referral, search;
- `campaign`: stable campaign identifier;
- `content`: stable content asset identifier;
- `job_id`: customer job being communicated;
- `workflow_id`: workflow selected when known.

Content derived from Trust History should use a stable content ID so discovery can later be connected to activation/value evidence without misrepresenting the underlying claims.

## Evidence hierarchy

### Revenue

```text
PROVIDER-SIGNED TRANSACTION
    > SERVER/WEBHOOK CONFIRMATION
    > CLIENT PURCHASE EVENT
    > CHECKOUT START
    > CTA CLICK
```

Provider-signed accepted payment is purchase evidence. Client events are telemetry.

### Delivery

```text
VERIFIED FULFILLMENT / PROVIDER DELIVERY EVIDENCE
    > SERVER DELIVERY LOG
    > CLIENT DOWNLOAD/OPEN EVENT
```

### Workflow/customer value

```text
AUTHORIZED OBSERVED TASK OUTCOME
    > USER_REPORTED_OUTCOME
    > ACTIVATION_COMPLETED
    > RESULT_REACHED
    > REAL_TASK_STARTED
    > FREE_ACQUISITION
```

These are different evidence classes, not a universal confidence ranking. The hierarchy only prevents weaker telemetry from impersonating a stronger event.

## Core metrics

### Landing → Free acquisition

`free_workflow_acquired / unique_relevant_landing_visitors`

Question:

`Does the free offer attract the intended job/user?`

### Free acquisition → Real task

`real_task_started / free_workflow_acquired`

Question:

`Does the user actually try the workflow rather than merely collect it?`

### Real task → Activation

`activation_completed / real_task_started`

Question:

`Can users provide inputs, obtain a result, and understand verification?`

### Activation → Value signal

`task_outcome_reported_positive / activation_completed`

Use carefully because outcome reporting is optional/self-selected unless observed through another authorized source.

Question:

`Does activated use appear useful enough for the intended task?`

### Activation/value → Starter interest

`starter_product_viewed / activated_users`

Question:

`Does real free value create credible interest in the $9 Starter?`

### Starter page → Checkout

`starter_checkout_started / starter_product_viewed`

Question:

`Does the Starter offer justify a transaction attempt?`

### Checkout → Purchase

Use authoritative provider orders as denominator/numerator source where possible.

Question:

`Is transaction friction preventing paid conversion?`

### Purchase → Delivery

`verified_starter_deliveries / provider_signed_starter_purchases`

Question:

`Does every accepted purchase produce correct fulfillment?`

### Starter → Full

`provider_signed_full_upgrades / eligible_starter_customers`

Question:

`Does broader adjacent value earn a $19 upgrade?`

### Return use

`users_with_return_use / activated_users`

Question:

`Does Prompt Machine solve enough recurring work to earn reuse?`

## Revenue metrics

Minimum:

- real Starter orders;
- real Full orders/upgrades;
- gross sales;
- refunds;
- provider fees where known;
- delivery failures;
- net provider payout estimate where available;
- average order value.

Do not merge test transactions into real revenue metrics.

## Trust-history analytics

A future `Why we trust this workflow` surface may generate events such as:

```text
trust_history_viewed
historical_failure_expanded
regression_evidence_viewed
known_limitation_viewed
```

These measure whether evidence content is being inspected. They do **not** prove that evidence caused trust or conversion.

Any causal claim requires a separately designed experiment.

## First-sale dashboard

Until sample size justifies aggregation, keep an interpretable row-level or daily table:

| Date | Source | Job | Free | Real task | Activated | Value signal | Starter view | Checkout | Purchase | Delivery | Return/Upgrade |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|

Also maintain a qualitative evidence log:

- customer job described;
- activation friction;
- useful outcome reports;
- observed limitations/failures;
- objections;
- why people did/did not buy;
- support burden;
- repeat/adjacent requests.

## Decision rules

### Traffic but no Free acquisition

Do not build more inventory. Inspect job-message fit and landing clarity.

### Free acquisition but no real-task starts

Fix Start Here, task chooser, or required-input clarity.

### Real-task starts but weak activation

Inspect workflow execution/input/output/verification friction.

### Activation but weak value

Review job/workflow fit and behavioral evidence before touching price.

### Value but weak Starter interest

Inspect paid value gradient and packaging.

### Starter interest but no checkout

Inspect offer, trust evidence, and price hypothesis.

### Checkout but no provider-signed purchases

Inspect checkout/payment friction.

### Purchases but delivery failures

Stop acquisition/checkout expansion until fulfillment is repaired.

### Delivery but no paid activation

Fix paid onboarding before scaling acquisition.

### Starter activation but no Full interest

Do not force an upsell. Learn whether the broader collection solves real adjacent jobs.

### Repeat use appears

Prioritize the recurring job family and inspect whether it earns further workflow investment.

## Privacy rule

Collect the minimum information needed to understand the funnel and learning loop.

Do not:

- fingerprint people across unrelated contexts;
- collect hidden sensitive attributes;
- retain private task data by default;
- infer customer outcomes from model output alone;
- publish customer evidence without authorization/redaction.

## Launch analytics gate

Before public paid launch verify:

- each intended event fires with stable semantics;
- activation cannot be emitted from download/view alone;
- attribution survives intended navigation where applicable;
- test and real events are distinguishable;
- provider-signed purchase evidence can be reconciled;
- delivery evidence can be reconciled;
- Starter and Full events are not conflated;
- no sensitive task contents are sent to analytics;
- customer-value events retain evidence class (self-report vs observed).

## Truth boundary

```text
VIEW != INTEREST
INTEREST != USE
USE != ACTIVATION
ACTIVATION != TASK SUCCESS
TASK SUCCESS != RETURN USE
CHECKOUT != PURCHASE
PURCHASE != DELIVERY
DELIVERY != RETENTION
TRUST-HISTORY VIEW != TRUST CAUSED
```

Measure each transition honestly so Prompt Machine learns what is actually broken instead of optimizing vanity numbers.
