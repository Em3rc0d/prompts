# pq-launch-0

Status: `DRAFTS_READY / HOLD_FOR_C5`

This directory is the durable launch package for Prompt Quarry's first LinkedIn/prodAgentic campaign.

## Publish gate

Do not publish any item in this campaign until `PQ-LAUNCH-0` passes:

```text
DEPLOYED PREMIUM WEB
+ PUBLIC VERIFIED FREE PACK
+ LIVE/TESTABLE CHECKOUT
+ REAL PROVIDER TEST ORDER
+ SIGNED WEBHOOK OBSERVED
+ CORRECT PAID DELIVERY VERIFIED
```

A repository build, a checkout click, or a fabricated webhook is not enough.

## Campaign payload

`CAMPAIGN.json` contains the canonical product/evidence/claims boundary that must accompany content generation or revision.

## First release set

1. `01-why-prompt-quarry-exists.md`
   - content id: `pq-launch-0-p01-why`
   - pillar: product philosophy
   - CTA: Free Developer Starter Pack

2. `02-code-review-before-after.md`
   - content id: `pq-launch-0-p02-code-review`
   - pillar: before/after structure
   - CTA: Free Code Review prompt

3. `03-not-observed-unknown.md`
   - content id: `pq-launch-0-p03-unknown`
   - pillar: evidence discipline
   - CTA: Free Developer Starter Pack

## Attribution convention

```text
utm_source=linkedin
utm_medium=organic
utm_campaign=pq-launch-0
utm_content=<content-id>
```

The Prompt Quarry web funnel preserves these campaign fields through Free Pack acquisition and the Lemon Squeezy checkout custom-data bridge where deployed/configured.

## Launch order

Publish one item, observe qualified behavior/questions, then publish the next. Do not preload the full ten-post sequence before learning from the first traffic.

Recommended initial order:

```text
P01 Why Prompt Quarry exists
  ↓ observe
P02 Code Review before/after
  ↓ observe
P03 not observed == unknown
```

## Claims boundary

The campaign may describe Developer Pack v1 as commercially `READY` and included assets as statically `VALID`, with explanation.

It must not convert those states into unsupported behavioral claims. F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, and F7 `PORTABLE` remain separate evidence gates.
