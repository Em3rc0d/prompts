# Prompt Machine Starter — Code Review Edition

Version: `1.0.0-rc2`

Status: `G14 RELEASE CANDIDATE / PUBLIC SALE OFF`

Prompt Machine Starter — Code Review Edition is a single governed workflow for reviewing software changes with explicit evidence discipline, calibrated uncertainty, and a human-controlled ship recommendation.

## What is included

- `WORKFLOW.md` — the exact Evidence-first Code Review v2.2 surface that completed the scoped certification path.
- `QUICKSTART.md` — the minimum operating procedure.
- `EVIDENCE.md` — what was tested, what is certified, and what remains unverified.
- `CUSTOMER-LICENSE.md` — customer usage rights and redistribution restrictions.
- `SALE-TERMS.md` — product-specific purchase, delivery, model-scope, and refund boundaries.
- `RELEASE-NOTICE.md` — current G14 release boundary.
- `MANIFEST.json` — exact package identity and integrity metadata.

## Intended outcome

Use the workflow to review a code change and receive a structured assessment that distinguishes observed evidence from inference, keeps material unknowns visible, and leaves the final ship decision with a human.

This is not an automatic approval system and it is not a security guarantee.

## Validated scope

The exact v2.2 workflow surface completed the frozen four-case regression matrix on `gemini-3.5-flash` with four clean observations and four human-review passes.

Other model families are unverified in the current release candidate. Do not describe this edition as model-agnostic or universally portable.

## Start here

1. Read `CUSTOMER-LICENSE.md` and `SALE-TERMS.md`.
2. Read `QUICKSTART.md`.
3. Copy the complete contents of `WORKFLOW.md` into a clean model conversation or compatible prompt surface.
4. Supply the required code/diff, change intent, and runtime context.
5. Add material contracts, invariants, and observed test evidence when available.
6. Treat the workflow output as advisory evidence; a human remains the final ship authority.

## Evidence boundary

Read `EVIDENCE.md` before making claims about this product. Packaging, certification scope, provider custody, customer delivery, customer value, and revenue are separate evidence classes.

This RC contains a frozen customer license, but public checkout remains OFF until G14 external provider and delivery evidence passes.

`MARKETING CLAIM <= OBSERVED EVIDENCE`
