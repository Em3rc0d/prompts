# Prompt Quarry Launch Content v1

## Objective

Use prodAgentic + LinkedIn to generate qualified traffic for the Free Developer Starter Pack and learn whether that traffic can convert into Developer Pack v1 purchases.

The distribution system must optimize for useful technical proof, not generic AI hype.

## Campaign

Canonical campaign id:
`pq-launch-0`

Primary CTA:
`Get the free Prompt Quarry Developer Starter Pack.`

Secondary CTA:
`Developer Pack v1 is available for builders who want the reusable system behind it.`

## Content engine

```text
PROMPT QUARRY BUILD/EVIDENCE
        ↓
CONTENT ANGLE
        ↓
prodAgentic RESEARCH / DRAFT
        ↓
CLAIMS CHECK
        ↓
HUMAN APPROVAL
        ↓
PUBLISH
        ↓
TRACK
        ↓
LEARN
        ↓
NEXT CONTENT
```

prodAgentic must preserve the same principle as Prompt Quarry:

`AI proposes / Human decides / System executes / System proves.`

## Content pillars

### 1. Problem education
Teach why common developer prompts fail.

Examples:
- `Review this code` is not a review contract.
- Asking for an architecture recommendation without constraints invites generic output.
- A debugging prompt should ask for evidence, reproduction paths, and unknowns before fixes.

CTA: Free Pack.

### 2. Before / after
Show a short generic prompt beside a Prompt Quarry structured alternative.

Do not claim the structured version is behaviorally superior unless actual F4/F5 evidence supports that comparison.

Safe framing:
`Here is what becomes explicit in the structured version.`

### 3. Build in public
Show the engineering behind product integrity:
- release manifest;
- static VALID vs READY distinction;
- proprietary license boundary;
- deterministic release construction;
- why scraped prompts are not automatically commercial inventory.

Translate internals into customer relevance.

### 4. Free prompt demonstrations
Take one Starter Pack prompt and explain how to fill it with a realistic developer task.

The content should be useful even if the reader never buys.

### 5. Product philosophy
Position Prompt Quarry against volume-first prompt bundles.

Message:
`The goal isn't to own 5,000 prompts. The goal is to have the right reusable structure when the work matters.`

### 6. Evidence discipline
Explain:
- VALID != TESTED;
- TESTED != IMPROVED;
- CERTIFIED requires more than CI.

Commercial translation:
`We tell you what has actually been verified instead of turning every quality check into a marketing superlative.`

## Launch sequence — first 10 posts

### Post 1 — Why Prompt Quarry exists
Hook:
`I don't think developers need another folder with 1,000 AI prompts.`

Body:
Problem -> philosophy -> what Prompt Quarry builds.

CTA:
Free Starter Pack.

### Post 2 — Code review before/after
Show generic input versus structured review dimensions.

CTA:
Free Code Review prompt.

### Post 3 — The unknown rule
Theme:
`not observed == unknown`

Explain why this matters in technical AI work.

CTA:
Free Pack.

### Post 4 — Bug diagnosis workflow
Show how diagnosis differs from immediate fix-generation.

CTA:
Free Bug Diagnosis prompt.

### Post 5 — Why VALID is not TESTED
Build trust through evidence-state honesty.

CTA:
Free Pack / methodology teaser.

### Post 6 — Technical decision prompt
Demonstrate alternatives, tradeoffs, unknowns, and decision criteria.

CTA:
Free Technical Decision prompt.

### Post 7 — Inside Developer Pack v1
Show package map, not all proprietary content.

CTA:
Paid product page.

### Post 8 — Use/adapt vs resale
Explain the license simply.

CTA:
Developer Pack.

### Post 9 — Prompt count is a vanity metric
Contrast quantity with reusable structure.

CTA:
Free Pack.

### Post 10 — Launch
`Developer Pack v1 is commercially READY.`

Be explicit:
`READY is packaging/release readiness, not a claim of universal model performance.`

CTA:
$19 launch checkout.

## Post structure

Recommended default:

```text
HOOK
↓
TECHNICAL PROBLEM
↓
ONE CONCRETE INSIGHT
↓
EXAMPLE / ARTIFACT
↓
BOUNDARY OR LESSON
↓
CTA
```

Do not force every post into the same formula. prodAgentic should vary format while preserving claims.

## Claims guardrails for prodAgentic

Forbidden without evidence:
- `battle-tested`;
- `proven`;
- `best`;
- `guaranteed`;
- `works on every model`;
- `certified`;
- `outperforms generic prompts`.

Allowed where factually supported:
- `structured`;
- `statically validated` / `VALID` with explanation;
- `commercially READY` with explanation;
- `versioned`;
- `21 governed assets` for Developer Pack v1;
- `3 free prompts` for Starter Pack v1;
- `use and adapt; resale/redistribution prohibited`.

## Content evidence payload

Each prodAgentic content request for this campaign should include:

```json
{
  "campaign": "pq-launch-0",
  "product": "Prompt Quarry",
  "primary_cta": "Developer Starter Pack v1",
  "paid_offer": "Developer Pack v1",
  "paid_price": "$19 launch",
  "paid_release_state": "READY",
  "asset_maturity": "VALID",
  "forbidden_claims": [
    "tested",
    "improved",
    "certified",
    "portable",
    "battle-tested",
    "guaranteed"
  ]
}
```

This should become a durable campaign input, not something authors must remember manually every time.

## Distribution cadence

Initial hypothesis:
- 3 substantive LinkedIn posts per week;
- 1 product/demo post;
- 1 educational/problem post;
- 1 build/evidence/philosophy post.

Do not optimize for daily posting if quality/evidence degrades.

## Comment strategy

After publishing:
- answer genuine technical questions;
- capture objections verbatim for product learning;
- avoid turning every reply into a sales pitch;
- direct people to the Free Pack when it genuinely answers their need.

## Feedback loop

For each content item record:
- content id;
- topic/pillar;
- impressions if available;
- landing visits;
- Free Pack acquisitions;
- paid-product visits;
- purchases attributed where evidence supports attribution;
- qualitative replies/objections.

The goal is to discover which problems create qualified product interest, not merely which hooks maximize impressions.

## Launch rule

Do not wait for 30 posts before opening checkout.

The correct loop is:

```text
LANDING LIVE
+ FREE DELIVERY LIVE
+ CHECKOUT LIVE
+ ANALYTICS LIVE
        ↓
PUBLISH
        ↓
OBSERVE
        ↓
ITERATE
```

The first campaign exists to generate customer evidence for the next product decision.
