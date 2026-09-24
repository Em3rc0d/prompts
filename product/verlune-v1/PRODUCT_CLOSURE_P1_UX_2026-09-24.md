# Verlune v1 — Product Closure P1 UX

Status: `IMPLEMENTED_CANDIDATE / STACKED_ON_P0`

Date: 2026-09-24

## Scope

This batch closes customer-facing UX inconsistencies identified in the full-site review without changing product scope, pricing, entitlement, or the Hero V4 rendering system.

Implemented:
- Home category cards are real links to the matching Free prompt instead of decorative affordances.
- The Developer Starter ZIP no longer competes with the Free Library in the hero; it remains available as a secondary Development & Tech resource.
- Premium Library sidebar navigation now truthfully navigates by the four rendered sections: Builders, Workflows, Prompts, Adapt & Evaluate.
- Global mobile navigation now has a dedicated accessible menu rather than wrapping the desktop links.
- The workflow-design Learn article now describes the actual 11-asset Free Library.
- Free asset metadata now includes per-asset descriptions and canonical URLs.
- `robots.txt` and `sitemap.xml` are implemented through Next metadata routes.
- Search indexing is fail-closed by default and requires explicit live configuration.

## SEO boundary

Default:
```text
NEXT_PUBLIC_INDEXING_MODE=off
NEXT_PUBLIC_SITE_URL=
```

Therefore staging/non-final environments return a no-index crawl policy and do not publish a public sitemap corpus.

Before production indexing:
- configure the final public site URL;
- explicitly switch indexing mode to `live`;
- verify canonical host and sitemap output on the final deployment.

## Explicitly not in this batch

- Hero V4.1 optical/material refinement;
- Premium Library visual redesign;
- editorial rendering of raw asset Markdown;
- live Premium commerce;
- production promotion;
- Human Visual Acceptance closure.

## Gate

```text
P1_HOME_AFFORDANCES             IMPLEMENTED
P1_FREE_HERO_CLARITY            IMPLEMENTED
P1_PREMIUM_NAV_TRUTH            IMPLEMENTED
P1_MOBILE_NAV                   IMPLEMENTED
P1_LEARN_CURRENT_COPY           IMPLEMENTED
P1_SEO_METADATA_ROUTES          IMPLEMENTED
INDEXING_DEFAULT                OFF
HERO_V4_1                       OPEN
HUMAN_VISUAL_ACCEPTANCE         OPEN
READY_TO_SELL                   false
```
