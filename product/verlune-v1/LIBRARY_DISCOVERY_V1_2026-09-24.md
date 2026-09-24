# Verlune Library Discovery v1

Status: `IMPLEMENTED_CANDIDATE / STAGING_REQUIRED`

Date: 2026-09-24

## Problem

The expanded Verlune catalog now contains:

```text
48 prompts
8 workflows
2 Builders
2 Toolkit assets
────────────
60 assets
```

A flat wall of cards no longer scales as the primary discovery model.

The user should start from the job they need to do, then narrow the library only when useful.

## Discovery architecture

```text
/library
  ↓
curated collection or search
  ↓
tier / type / category filters
  ↓
asset metadata
  ├── Free → complete public asset
  └── Premium → Premium value/access surface

/free
  ↓
same explorer
  ↓
Free fixed tier

/app
  ↓
entitlement
  ↓
same explorer
  ↓
Premium fixed tier
  ↓
protected complete asset
```

## Public Library

`/library` is the public catalog surface.

It may expose:
- asset ID;
- customer-facing name;
- tier;
- type;
- customer-facing category;
- summary.

It must not expose Premium source bytes, raw Markdown, source paths, source blob hashes, or any other field that substitutes for entitlement.

## Filters

Discovery v1 supports:

- free-text search;
- tier: All / Free / Premium;
- type: Prompt / Workflow / Builder / Toolkit;
- category;
- curated collection.

Filters combine rather than silently replacing one another.

Results are revealed 12 at a time so the default experience does not become a 60-card wall.

## Curated collections

The initial collection layer is goal-oriented rather than merely repeating the category taxonomy:

- Start here;
- Premium essentials;
- Ship software;
- Research & decide;
- Learn & prepare;
- Operate & plan;
- Write & communicate;
- Content & audience.

Collections are navigation aids. They do not create new assets or new evidence claims.

## Default behavior

Public and Free surfaces start with `Start here`, which contains the original eight complete Free entry points.

The authenticated Premium surface starts with `Premium essentials`, which contains the original eight deeper Premium prompts plus Prompt Builder and Workflow Builder.

The complete catalog remains one click away through `All assets`.

## Truth boundary

```text
DISCOVERABLE ≠ FREE
DISCOVERABLE ≠ ENTITLED
CATALOGED ≠ RUNTIME TESTED
STRUCTURE CHECKED ≠ CERTIFIED
```

Premium metadata is deliberately discoverable before purchase. Premium asset content remains protected.

## Explicitly out of scope

Discovery v1 does not add:
- behavioral prompt testing;
- recommendation scoring;
- popularity ranking;
- star ratings;
- user profiles;
- saved favorites;
- personalization;
- AI-generated recommendations;
- fabricated usage counts.

## Gate

```text
UNIFIED_LIBRARY_ROUTE       IMPLEMENTED
SEARCH                      IMPLEMENTED
TIER_FILTER                 IMPLEMENTED
TYPE_FILTER                 IMPLEMENTED
CATEGORY_FILTER             IMPLEMENTED
CURATED_COLLECTIONS         IMPLEMENTED
FREE_REUSE                  IMPLEMENTED
PREMIUM_REUSE               IMPLEMENTED
PREMIUM_CONTENT_BOUNDARY    METADATA_ONLY_PUBLIC
BUILD_GATE                  OPEN
STAGING_REVIEW              OPEN
HUMAN_VISUAL_ACCEPTANCE     OPEN
```
