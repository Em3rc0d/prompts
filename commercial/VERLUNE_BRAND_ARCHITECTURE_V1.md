# Verlune Brand Architecture v1

Status: `ADOPTED_PRE_LIVE`

Date: 2026-09-08

## Decision

`Verlune` is the customer-facing masterbrand for the commercial product line.

The first customer-facing product name is:

`Verlune Code Review`

Internal engineering names remain intentionally separate:

```text
CUSTOMER-FACING
Verlune
└── Code Review

PRODUCT ENGINE
Prompt Machine
└── packaging / release / commerce orchestration

EVIDENCE FACTORY
Prompt Quarry
└── mining / experiments / evaluation / regression / certification
```

## Naming rules

- `Verlune` is the brand shown to buyers, on product packaging, receipts, invoices, storefronts and future public product surfaces.
- `Verlune Code Review` is the public product name for the first paid release.
- `Starter` remains an internal SKU/tier concept and is not required in the primary customer-facing title.
- `Prompt Machine` is retained as an internal product-engine/platform name where technical continuity matters.
- `Prompt Quarry` is retained as the internal evidence/certification factory name.
- Existing machine IDs, certification IDs and workflow IDs may retain `pm` / `pq` prefixes when changing them would destroy historical continuity. Those identifiers are not customer branding.
- Legal supplier/merchant identity remains the truthful identity verified by the commerce provider and is not replaced or obscured by the display brand.

## Customer surface rule

The released ZIP and public commerce surfaces must not expose `Prompt Machine` or `Prompt Quarry` as the buyer-facing product brand.

The package may preserve stable technical IDs whose provenance predates the brand decision, but descriptive copy, titles, filenames and public product names must use `Verlune`.

## First release identity

Target customer identity before provider validation:

```text
brand            Verlune
product          Verlune Code Review
version          1.0.0
price hypothesis USD 9 one-time
workflow         Evidence-first Code Review v2.2
model scope      gemini-3.5-flash
classification   MODEL_SPECIFIC
```

The certified workflow bytes are not changed by this branding decision.

## Brand promise boundary

Verlune should communicate trustworthy, evidence-backed AI work without implying universal correctness or portability.

The commercial invariant remains:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

A possible launch-line direction is `AI work, with proof.`; this is copy exploration, not a certified product claim or frozen legal tagline.

## Pre-Live consequence

Because the buyer-facing package identity changes, the previously frozen pre-Live `Prompt Machine ... 1.0.0` ZIP is superseded before any real sale. G12/G13 must be rerun and a new exact archive name, byte count, SHA-256 and payload fingerprint must be frozen for the Verlune-branded `1.0.0` package.

Historical RC/Test/provider evidence remains preserved and must not be rewritten as if it used the Verlune-branded final bytes.

## Naming diligence boundary

The owner selected `Verlune` after preliminary collision/domain screening. This record is a product/brand architecture decision, not legal trademark clearance. Formal trademark/domain/social-handle diligence remains a separate business/legal step before broader launch if required.
