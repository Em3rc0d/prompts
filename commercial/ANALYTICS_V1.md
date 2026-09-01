# Prompt Quarry Analytics v1

## Objective

Measure whether Prompt Quarry can convert qualified attention into product use and paid demand without building a large analytics stack.

## North-star event

`purchase_completed`

`PQ-$1` requires at least one real `purchase_completed` event reconciled with real provider revenue.

Analytics alone cannot prove revenue if it disagrees with checkout-provider records.

## Funnel events

```text
landing_view
free_cta_clicked
free_pack_acquired
paid_product_viewed
paid_cta_clicked
checkout_started
purchase_completed
paid_pack_downloaded
```

Optional after launch:
```text
free_pack_prompt_opened
upgrade_link_clicked
customer_feedback_submitted
```

## Event contract

Every event should support where available:

```json
{
  "event": "paid_cta_clicked",
  "timestamp": "ISO-8601",
  "session_id": "anonymous-or-consented-session-id",
  "product_id": "pq-developer-pack",
  "product_version": "1.0.0",
  "source": "linkedin",
  "medium": "organic",
  "campaign": "pq-launch-0",
  "content": "code-review-before-after"
}
```

Do not collect sensitive personal data merely because analytics software permits it.

## Acquisition taxonomy

Canonical UTM-like fields:
- `source`: linkedin, github, direct, referral, other;
- `medium`: organic, profile, post, dm, referral;
- `campaign`: e.g. `pq-launch-0`;
- `content`: specific content asset identifier.

prodAgentic-generated content should attach a stable `content` identifier so Prompt Quarry can connect content production to funnel behavior.

## Core metrics

### Landing -> Free
`free_pack_acquired / unique_landing_visitors`

Question answered:
`Does the free offer create enough interest?`

### Free -> Paid interest
`paid_product_viewed / free_pack_acquired`

Question answered:
`Does free usage create curiosity about the system?`

### Paid page -> Checkout
`checkout_started / paid_product_viewed`

Question answered:
`Does the paid offer justify a transaction attempt?`

### Checkout -> Purchase
`purchase_completed / checkout_started`

Question answered:
`Is checkout/trust friction preventing purchase?`

### Overall
`purchase_completed / unique_landing_visitors`

Useful only after enough traffic exists. Before then, inspect individual behavior and objections.

## Revenue metrics

Minimum:
- gross sales;
- refunds;
- net provider payout estimate;
- number of paid orders;
- average order value.

For v1 there is one paid SKU, so complex revenue attribution is unnecessary.

## Evidence hierarchy

```text
CHECKOUT PROVIDER TRANSACTION
    > SERVER/WEBHOOK CONFIRMATION
    > CLIENT purchase_completed EVENT
    > BUTTON CLICK
```

A button click is intent, not revenue.
A client-side success event is telemetry, not authoritative payment evidence.

## First-sale dashboard

Until 10 real purchases, a simple table is enough:

| Date | Source | Landing | Free | Paid view | Checkout | Purchase | Revenue |
|---|---:|---:|---:|---:|---:|---:|---:|

Also maintain a qualitative log:
- objections;
- questions;
- why people downloaded;
- why buyers purchased;
- confusion during onboarding.

## Decision rules

### Traffic but no Free acquisitions
Do not build more paid-product features. Fix acquisition promise/landing clarity.

### Free acquisitions but no paid interest
Inspect the Starter Pack's upgrade bridge and whether the paid difference is understandable.

### Paid interest but no checkout starts
Test offer and price messaging.

### Checkout starts but no purchases
Inspect checkout trust, payment support, mobile UX, and pricing friction.

### Purchases but poor activation
Fix delivery/onboarding before scaling acquisition.

## Privacy rule

Collect the minimum information required to understand the funnel. Do not fingerprint users across unrelated contexts or collect hidden sensitive attributes.

## Launch analytics gate

Before public launch verify:
- each funnel event fires once per intended action;
- UTMs survive landing navigation;
- checkout source can be reconciled where supported;
- test events are distinguishable from real production data;
- real revenue is verified from checkout records, not inferred from analytics.
