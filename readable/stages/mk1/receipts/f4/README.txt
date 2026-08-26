PROMPT QUARRY — HUMAN READING COPY
========================================================================================
STAGE / DOCUMENT     : MK1
SOURCE REPOSITORY FILE: mk1/receipts/f4/README.md
CONTENT ORIGIN       : REPOSITORY DOCUMENTATION / ARTIFACT

# MK1 F4 Behavioral Receipts

This directory is reserved for observed behavioral execution receipts.

No file in this directory should be created from a synthetic harness run and then presented as evidence that a prompt is `TESTED`.

## Prepare an execution envelope

Example:

```bash
python tools/mk1_prepare_f4_execution.py \
  --fixture-set pq_mk1_fs_software_code_review_v1 \
  --mode manual-observed \
  --provider openai \
  --model <observed-model-id> \
  --run-at <ISO-8601-time> \
  --execution-id <unique-run-id> \
  --output mk1/receipts/f4/executions/<unique-run-id>.json
```

The generated envelope contains the exact immutable fixture input, an empty observed-output field and every unresolved manual check.

## Execute

Run the exact F2 prompt artifact against every fixture input under the declared runtime conditions.

Record the actual output verbatim in the execution envelope. Do not edit fixture inputs after seeing model behavior.

If a fixture needs correction, version the fixture set and execute again.

## Review

Resolve every declared human check as `PASS` or `FAIL` with a short evidence note.

Unresolved blocking human checks prevent `TESTED` eligibility.

## Produce a receipt

Example:

```bash
python tools/mk1_behavioral_runner.py \
  --artifact mk1/candidates/f2/software_code_review/artifact.json \
  --fixture-set pq_mk1_fs_software_code_review_v1 \
  --execution mk1/receipts/f4/executions/<unique-run-id>.json \
  --output mk1/receipts/f4/<unique-run-id>.receipt.json
```

A valid real run may emit:

```text
status = BEHAVIORAL_PASS
eligible_for_tested = true
```

Only that receipt may support a copied/versioned F4 artifact whose state changes from `VALID` to `TESTED` and whose evaluation fields reference the exact fixture set and receipt.

## Evidence boundary

F4 proves behavior against a declared fixture set under one identified runtime profile.

It does **not** prove:

- superiority over a baseline;
- general model independence;
- universal reliability;
- certification;
- improvement.

Those claims require later evidence in F5/F6.
