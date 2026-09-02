# Prompt Machine — Revenue Experiment v1

Status: `DESIGNED / NOT STARTED / PUBLIC CHECKOUT OFF`

Date: `2026-09-02`

## 1. Objective

The first commercial objective is not to prove that Prompt Machine can generate prompts.

It is to prove that a real person will pay for a workflow collection after receiving useful free value.

Primary milestone:

```text
PQ-$1 = first real non-test paid purchase successfully delivered
```

Secondary milestones:

```text
PQ-10          = 10 distinct real paid customers
PQ-REPEAT-1    = first customer who returns for another paid Prompt Machine product
PQ-REFERRAL-1  = first attributable customer acquired through another user's referral/share
```

None of these milestones may be inferred from test orders, provider sandboxes, CTA clicks, downloads, or checkout sessions.

## 2. Initial offer ladder

```text
FREE LIBRARY                 USD 0
STARTER COLLECTION           USD 9 one-time
DEVELOPER COLLECTION         USD 19 one-time
SUBSCRIPTION                 DEFERRED
```

All prices are hypotheses until real willingness-to-pay evidence exists.

### Free Library — $0

Current useful standalone entry:

- Code Review
- Bug Diagnosis
- Technical Decision

The free layer is intentionally useful. It is not a crippled demo.

### Starter Collection — $9 one-time

This is the primary first-launch paid offer.

Candidate value:

- 2–3 premium workflow surfaces selected around one coherent job family;
- installable skill surfaces where structurally and behaviorally supported;
- real examples;
- `START_HERE` task routing;
- verification guidance;
- adaptation cheatsheet;
- explicit evidence and limitations.

The Starter Collection must solve complete tasks. It must not be the Developer Collection with arbitrary pieces removed merely to force an upgrade.

### Developer Collection — $19 one-time

This remains the broader premium offer and price anchor.

Candidate value:

- all four governed workflow families;
- four skill surfaces when corresponding gates pass;
- operating contracts;
- advanced adaptation guidance;
- examples;
- evidence cards;
- full collection navigation and orchestration.

The $19 offer should earn its price through broader reusable coverage, not through withholding the minimum needed to make the $9 product useful.

### Subscription

Subscription remains deferred until Prompt Machine observes a credible recurring value loop such as:

- customers returning for new workflows;
- meaningful update demand;
- repeat purchases;
- sustained collection usage;
- a release cadence customers would rationally pay to continue receiving.

Do not invent a monthly plan merely to create recurring revenue before recurring value exists.

## 3. Pricing experiment discipline

The primary first paid experiment is now **USD $9 one-time**.

The $19 Developer Collection remains visible as the premium/full option.

Preferred commercial ladder:

```text
$0 useful free value
        ↓
$9 low-friction first purchase
        ↓
$19 broader full collection
        ↓
repeat purchase / referral / future recurring model if earned
```

Freeze the $9 Starter price during the first launch cohort unless there is a material legal, tax, provider, or product defect. Do not change price after every failed visit; that would confound product demand with pricing noise.

Suggested first observation window:

```text
first 10 real Starter purchases OR first 30 days of public sale,
whichever occurs first
```

After the window, review the full funnel before changing price or package boundaries.

## 4. Why the free layer exists

The free layer is part of acquisition and trust, not an intentionally broken teaser.

A user should be able to apply one of the current free workflows to a real task without paying.

The $9 Starter must earn the first purchase through:

- less setup and trial-and-error;
- coherent workflow coverage around a repeated job;
- useful examples;
- easier navigation;
- installable surfaces where supported;
- visible verification and limitations.

The $19 Developer Collection must then earn the upgrade through:

- broader related workflow coverage;
- the full set of supported skill surfaces;
- reusable operating contracts;
- advanced adaptation guidance;
- deeper orchestration across recurring tasks;
- stronger evidence and known-limitations surfaces.

If customers cannot explain why each paid tier is worth more than the tier below it, the product ladder has failed the value test even if checkout technically works.

## 5. Acquisition model

Primary channels:

```text
LinkedIn
TikTok
technical / learning content
search / GitHub discovery
direct sharing / referrals
```

Content should lead with useful information, examples, lessons, or workflows—not with repeated purchase requests.

Preferred path:

```text
CONTENT
  ↓
Prompt Machine home
  ↓
free workflow
  ↓
real task activation
  ↓
Starter interest
  ↓
$9 purchase
  ↓
Developer Collection interest
  ↓
$19 purchase when broader value is needed
```

Direct-to-paid traffic is allowed, but the core product thesis assumes trust can be built by useful free value and transparent evidence.

Every campaign should use UTM attribution when practical.

## 6. Funnel events

Minimum observable events:

```text
landing_view
free_product_viewed
free_cta_clicked
collections_viewed
starter_product_viewed
starter_cta_clicked
paid_product_viewed
paid_cta_clicked
checkout_started          when provider integration exposes it safely
purchase_completed        only from accepted real purchase evidence
delivery_completed        only after exact customer artifact delivery is verified
```

Client-side events are intent evidence. Server/provider receipts are purchase evidence.

## 7. Metrics

### Acquisition

```text
landing → free view
landing → free CTA
content source → landing
```

### Activation proxy

A download is not task success.

Until the product has an explicit in-product completion signal, use conservative proxies such as:

- repeat visit;
- second workflow view/download;
- voluntary feedback describing a completed real task;
- attributable movement from free to collection inspection.

Do not label these proxies as proven productivity improvement.

### Commercial intent

```text
free users → collections viewed
collections viewed → Starter CTA
Starter viewed → Starter CTA
Starter customers → Developer Collection viewed
Developer Collection viewed → $19 CTA
```

### Revenue

```text
Starter CTA → checkout
checkout → accepted purchase
accepted purchase → verified delivery
$9 customer → $19 upgrade
revenue / visitor
revenue / activated user
refund rate
support contacts per purchase
```

### Expansion

```text
paid customer → repeat visit
paid customer → second collection purchase
paid customer → referral
```

## 8. Launch decision rules

Public sale remains disabled unless all required product and delivery gates pass for the specific SKU being sold.

At minimum:

```text
PRODUCT_READY                YES
DETERMINISTIC_ARCHIVE        PASS
PROVIDER_CUSTODY             PASS
PROVIDER_INTEGRATION         PASS
LIVE_DELIVERY_CANARY         PASS
PUBLIC_COPY_EVIDENCE_AUDIT   PASS
```

Behavioral maturity labels remain separately governed by PCP and skill certification.

If a collection is sold before full F6 certification is earned, customer-facing copy must accurately describe the lower evidence state and known limitations. Packaging must never imply a stronger maturity level than receipts establish.

## 9. First-launch cohort discipline

During the first observation window:

Keep stable where possible:

- $9 Starter price;
- Starter contents;
- $19 Developer Collection anchor;
- main value proposition;
- checkout provider;
- core landing CTA structure.

Changes are allowed for:

- broken delivery;
- security/privacy defects;
- misleading claims;
- severe usability failures;
- payment/provider failures.

Record every material change so conversion results can be interpreted against the version actually shown to customers.

## 10. What we learn from failure

No purchases does not automatically mean "lower the price."

Investigate in order:

1. **Traffic problem** — not enough relevant visitors.
2. **Message problem** — visitors do not understand the result or audience.
3. **Activation problem** — free users do not reach useful value.
4. **Trust problem** — users do not believe the product is worth relying on.
5. **Upgrade problem** — Starter does not look materially better than free.
6. **Price problem** — value is understood but $9 still blocks purchase.
7. **Checkout problem** — intent exists but payment/delivery fails.

For the $19 tier, separately test whether Starter customers perceive enough additional breadth to justify the upgrade.

Do not diagnose price before observing the earlier stages.

## 11. What we learn from success

One $9 purchase establishes only:

```text
someone paid once
```

It does not establish product-market fit.

Ten distinct customers establish stronger willingness-to-pay evidence but still do not prove repeatability at scale.

A customer who later upgrades from $9 to $19 is stronger evidence that the product ladder creates expanding value rather than merely extracting a small impulse purchase.

Repeat purchase, referral, low refund/support burden, and sustained conversion are stronger signals that Prompt Machine is becoming a business rather than a one-time novelty.

## 12. Expansion rule

Do not build dozens of profession-specific packs because those professions exist.

New collections enter the roadmap when observed demand shows recurring jobs-to-be-done that are:

- common enough to repeat;
- structured enough to workflowize;
- valuable enough that reducing setup/trial-and-error matters;
- safe and lawful to package at the intended level of authority;
- supportable with Prompt Quarry evidence.

Profession is metadata. Outcome is the primary product axis.

## 13. Content loop

The founder/content channel can publish:

- real workflow demonstrations;
- before/after task structure;
- AI mistakes and verification lessons;
- software and systems-engineering lessons;
- university/project-building experience;
- transparent build-in-public milestones;
- product evidence and limitations in accessible language.

Every useful content item should have one natural next step, usually:

```text
Try the related free workflow
```

not:

```text
Buy now
```

Trust should compound before monetization pressure does.

## 14. Revenue truth table

```text
free download          != revenue
Starter CTA click      != revenue
$19 CTA click          != revenue
checkout created       != revenue
provider test order    != revenue
live canary            != public revenue
accepted real purchase == purchase evidence
verified delivery      == fulfilled purchase evidence
```

## 15. Immediate commercial critical path

```text
Product Vision v3                     DONE
Outcome-first public web              IMPLEMENTED ON PRODUCT BRANCH
Collections surface                   IMPLEMENTED ON PRODUCT BRANCH
Price ladder $0 → $9 → $19            FROZEN AS LAUNCH HYPOTHESIS
Starter Collection scope              TO FREEZE
Funnel telemetry                      IMPLEMENTED / BACKEND OBSERVATION TBD
PCP-04 real execution                 OPEN
Paid collection product QA            OPEN
Provider + live delivery canary        OPEN
Public $9 Starter checkout            OFF
Public $19 Developer checkout         OFF
PQ-$1                                 NOT OBSERVED
```
