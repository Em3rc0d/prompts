# Prompt Machine Starter — Code Review Edition

Version: `1.0.0`

Prompt Machine Starter — Code Review Edition is a governed workflow package for reviewing software changes with explicit evidence discipline, calibrated uncertainty, and a human-controlled ship recommendation.

## What is included

- `WORKFLOW.md` — the exact Evidence-first Code Review v2.2 surface covered by the declared certification scope.
- `QUICKSTART.md` — the minimum operating procedure.
- `EVIDENCE.md` — what was tested, what is certified, and what remains outside the demonstrated scope.
- `CUSTOMER-LICENSE.md` — customer usage rights and redistribution restrictions.
- `SALE-TERMS.md` — product-specific purchase, delivery, model-scope, and refund boundaries.
- `RELEASE-NOTICE.md` — release identity and scope notes.
- `MANIFEST.json` — exact package identity and integrity metadata.

## Intended outcome

Use the workflow to review a code change and receive a structured assessment that distinguishes observed evidence from inference, keeps material unknowns visible, and leaves the final ship decision with a human.

This is not an automatic approval system and it is not a security guarantee.

## Validated scope

The exact v2.2 workflow surface completed the frozen four-case regression matrix on `gemini-3.5-flash` with four clean observations and four human-review passes.

Other model families are unverified in the current certification scope. Do not describe this edition as model-agnostic or universally portable.

## Start here

1. Read `CUSTOMER-LICENSE.md` and `SALE-TERMS.md`.
2. Read `QUICKSTART.md`.
3. Copy the complete contents of `WORKFLOW.md` into a clean model conversation or compatible prompt surface.
4. Supply the required code/diff, change intent, and runtime context.
5. Add material contracts, invariants, and observed test evidence when available.
6. Treat the workflow output as advisory evidence; a human remains the final ship authority.

## Evidence boundary

Read `EVIDENCE.md` before making claims about this product. The behavioral certification is intentionally narrow and does not establish universal portability, automatic software correctness, security, compliance, or business outcomes.

`MARKETING CLAIM <= OBSERVED EVIDENCE`
