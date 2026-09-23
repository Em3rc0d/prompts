# Verlune public claim static audit — 2026-09-22

Status: `SOURCE_STATIC_PASS / LIVE_DEPLOYMENT_NOT_OBSERVED`

Candidate branch reviewed: `feat/verlune-product-model-v1-20260922-r2`

## Scope

Reviewed customer-facing source for:
- home;
- Free workflows;
- Code Review;
- license;
- Learn/evidence pages;
- public product metadata and purchase-state projection.

## Findings

### Current public positioning

The source still presents the narrow developer-oriented Verlune surface: reusable developer workflows, the Free developer set, and the historical `Verlune Code Review` paid product.

It does **not** expose the new v1 library/toolkit catalog, Premium Builders, launch-core counts, or a new Premium purchase claim.

This is consistent with the landing freeze.

### Evidence claims

The Code Review page binds its public evidence copy to the historical packaged product identity:
- version 1.0.0;
- archive SHA-256 `4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649`;
- workflow SHA-256 `6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977`;
- 77/77 Pack QA;
- 4/4 human-review regression passes;
- Gemini 3.5 Flash scope.

The copy explicitly says model-specific evidence is not universal portability and does not guarantee correctness/security/compliance.

### Purchase claims

The purchase CTA is fail-closed in source:
- it requires commerce mode `live`;
- `NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS=LIVE`;
- and an HTTPS live checkout URL.

When those conditions are absent, the customer is told public purchasing is not open.

### New Verlune Premium claims

No new v1 Premium claim is currently authorized or exposed in the reviewed source.

## Static disposition

`PASS_STATIC_CLAIM_BOUNDARY`

No source change is required to preserve the current landing freeze.

## Limitation

The public URLs were not retrievable by the available web inspection tool during this audit, so this result verifies repository source, **not the bytes currently deployed at the public hostname**.

Therefore:

`PUBLIC_SITE_CLAIM_AUDIT_PASS = NOT_YET`

until the deployed surface is observed and matched to the reviewed source/release.
