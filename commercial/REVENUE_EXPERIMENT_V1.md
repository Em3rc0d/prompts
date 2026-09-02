# Prompt Machine — Revenue Experiment v1

Status: `DESIGNED / NOT STARTED / PUBLIC CHECKOUT OFF`

Date: `2026-09-02`

## 1. Objective

Prompt Machine must prove that a real person will pay for a reusable AI workflow after receiving useful free value.

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

Pricing evidence state for both paid tiers:

```text
PRICE HYPOTHESIS
```

The $9 Starter is the primary first-launch paid offer. The $19 Developer Collection remains the broader premium option and price anchor. Subscription is deferred until recurring value is observed.

### Free Library — $0

Current useful standalone entry:

- Code Review
- Bug Diagnosis
- Technical Decision

The free layer is intentionally useful. It is not a crippled demo.

### Starter Collection — $9 one-time

Candidate value:

- 2–3 premium workflow surfaces around one coherent job family;
- installable skill surfaces only where evidence supports them;
- real examples;
- `START_HERE` task routing;
- verification guidance;
- adaptation guidance;
- explicit evidence and limitations.

The Starter must solve complete tasks. It must not be a deliberately broken subset of the $19 product.

### Developer Collection — $19 one-time

Candidate value:

- all four governed workflow families;
- four skill surfaces when corresponding gates pass;
- operating contracts;
- advanced adaptation guidance;
- examples and evidence cards;
- full collection navigation and orchestration.

The $19 tier must earn the upgrade through broader reusable coverage.

## 3. Pricing experiment discipline

Preferred ladder:

```text
$0 useful free value
        ↓
$9 low-friction first purchase
        ↓
$19 broader full collection
        ↓
repeat purchase / referral / future recurring model if earned
```

Freeze the $9 price and Starter contents during the first observation cohort except for material product, legal, security, delivery, or provider defects.

Suggested first observation window:

```text
first 10 real Starter purchases OR first 30 days of public sale,
whichever occurs first
```

Do not change price after every failed visit. Diagnose the complete funnel first.

## 4. Value ladder

The free layer exists for acquisition, trust, and real utility.

The $9 Starter must earn payment through less setup, coherent workflow coverage, examples, navigation, verification, and supported installable surfaces.

The $19 Developer Collection must earn the upgrade through broader coverage, deeper orchestration, stronger adaptation surfaces, and the full supported skill set.

If customers cannot explain why each tier is worth more than the tier below it, the ladder has failed even if checkout works technically.

## 5. Acquisition model

Primary channels:

```text
LinkedIn
TikTok
technical / learning content
search / GitHub discovery
direct sharing / referrals
```

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

Content should lead with useful information and demonstrations, not repeated purchase requests. Campaigns should use UTM attribution when practical.

## 6. Observable funnel

Minimum funnel events:

```text
landing_view
free_product_viewed
free_cta_clicked
free_pack_acquired
collections_viewed
starter_product_viewed
starter_cta_clicked
paid_product_viewed
paid_cta_clicked
checkout_started
purchase_completed
delivery_completed
```

Evidence classes are deliberately separated:

```text
browser/client intent          = UNTRUSTED_CLIENT_INTENT
verified free artifact serve   = SERVER_DELIVERY_EVIDENCE
checkout creation              = SERVER_CHECKOUT_EVIDENCE
accepted paid provider event   = PROVIDER_SIGNED_PURCHASE_EVIDENCE
verified artifact fulfillment  = DELIVERY_EVIDENCE
```

Client-side events are intent evidence only. They may be counted and segmented, but they can never manufacture revenue evidence.

Prompt Machine's anonymous browser session identifier remains browser-session-only. The server intent sink must not receive it. Intent logs must avoid intentionally collecting names, email addresses, request headers, IP fields, or user-agent values.

## 7. Metrics

### Acquisition

```text
landing → free view
landing → free CTA
content source → landing
```

### Activation proxies

A download is not proof of task success. Until explicit completion evidence exists, conservative proxies include repeat visits, a second workflow interaction, voluntary feedback describing a completed task, and movement from Free to paid collection inspection.

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

## 8. Launch gates

Public sale remains disabled unless the required product and delivery gates pass for the exact SKU being sold.

At minimum:

```text
PRODUCT_READY                YES
DETERMINISTIC_ARCHIVE        PASS
PROVIDER_CUSTODY             PASS
PROVIDER_INTEGRATION         PASS
LIVE_DELIVERY_CANARY         PASS
PUBLIC_COPY_EVIDENCE_AUDIT   PASS
```

Behavioral maturity remains separately governed by PCP and skill certification.

Master rule:

```text
MARKETING CLAIM <= OBSERVED EVIDENCE
```

## 9. First-launch cohort discipline

Keep stable where possible:

- $9 Starter price;
- Starter contents;
- $19 Developer Collection anchor;
- main value proposition;
- checkout provider;
- primary CTA structure.

Changes are allowed for broken delivery, security/privacy defects, misleading claims, severe usability failures, or payment/provider failures. Record material changes so results remain interpretable.

## 10. Failure diagnosis

No purchases does not automatically mean "lower the price."

Investigate in order:

1. traffic;
2. message;
3. activation;
4. trust;
5. upgrade value;
6. price;
7. checkout/delivery.

For the $19 tier, separately test whether Starter customers perceive enough additional value to upgrade.

## 11. Success interpretation

One $9 purchase establishes only:

```text
someone paid once
```

Ten distinct customers are stronger willingness-to-pay evidence but still do not prove product-market fit.

A later $9 → $19 upgrade, repeat purchase, referral, low refund rate, and low support burden are progressively stronger business signals.

## 12. Expansion rule

Do not build profession-specific collections simply because professions exist.

A new collection enters the roadmap when observed demand identifies a recurring job-to-be-done that is common, workflowizable, valuable, safe/lawful at the intended authority level, and supportable with Prompt Quarry evidence.

Profession is metadata. Outcome is the primary product axis.

## 13. Content loop

Useful content can show workflow demonstrations, AI verification mistakes, before/after task structure, engineering lessons, build-in-public milestones, and product evidence/limitations.

Preferred next step:

```text
Try the related free workflow
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
Price ladder $0 → $9 → $19            PRICE HYPOTHESIS FROZEN
Server-observed intent sink           IMPLEMENTED ON PRODUCT BRANCH
Starter Collection scope              TO FREEZE
PCP-04 real execution                 OPEN
Paid collection product QA            OPEN
Preview/staging verification          OPEN
Provider + live delivery canary       OPEN
Public $9 Starter checkout            OFF
Public $19 Developer checkout         OFF
PQ-$1                                 NOT OBSERVED
```
