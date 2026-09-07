# Prompt Machine Starter — Code Review Edition

Version: `1.0.0-rc1`

Status: `RELEASE CANDIDATE / NOT FOR SALE`

Prompt Machine Starter — Code Review Edition is a single governed workflow for reviewing software changes with explicit evidence discipline, calibrated uncertainty, and a human-controlled ship recommendation.

## What is included

- `WORKFLOW.md` — the exact Evidence-first Code Review v2.2 surface that completed the current certification path.
- `QUICKSTART.md` — the minimum operating procedure.
- `EVIDENCE.md` — what was tested, what is certified, and what remains unverified.
- `RELEASE-NOTICE.md` — release-candidate and licensing boundary.
- `MANIFEST.json` — exact package identity and integrity metadata.

## Intended outcome

Use the workflow to review a code change and receive a structured assessment that distinguishes observed evidence from inference, keeps material unknowns visible, and leaves the final ship decision with a human.

This is not an automatic approval system and it is not a security guarantee.

## Validated scope

The exact v2.2 workflow surface completed the frozen four-case regression matrix on `gemini-3.5-flash` with four clean observations and four human-review passes.

Other model families are unverified in the current release candidate. Do not describe this edition as model-agnostic or universally portable.

## Start here

1. Read `QUICKSTART.md`.
2. Copy the complete contents of `WORKFLOW.md` into a clean model conversation or compatible prompt surface.
3. Supply the required code/diff, change intent, and runtime context.
4. Add material contracts, invariants, and observed test evidence when available.
5. Treat the workflow output as advisory evidence; a human remains the final ship authority.

## Evidence boundary

Read `EVIDENCE.md` before making claims about this product. Packaging, certification scope, provider delivery, customer value, and revenue are separate evidence classes.

`MARKETING CLAIM <= OBSERVED EVIDENCE`
