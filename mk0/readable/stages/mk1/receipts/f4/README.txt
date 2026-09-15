PROMPT QUARRY — HUMAN READING COPY
========================================================================================
STAGE / DOCUMENT     : MK1
SOURCE REPOSITORY FILE: mk1/receipts/f4/README.md
CONTENT ORIGIN       : REPOSITORY DOCUMENTATION / ARTIFACT

# MK1 F4 Behavioral Receipts

This directory is reserved for observed behavioral execution receipts.

No file in this directory should be created from a synthetic harness run and then presented as evidence that a prompt is `TESTED`.

Current repository state:

```text
real *.receipt.json files = 0
TESTED artifacts = 0
```

## Prepare an execution envelope

Example:

```bash
python tools/mk1_prepare_f4_execution.py \
  --fixture-set pq_mk1_fs_software_code_review_v1 \
  --mode manual-observed \
  --provider openai \
  --model <observed-model-id> \
  --run-at <ISO-8601-execution-time> \
  --reviewer-ref owner-reviewer-01 \
  --reviewed-at <ISO-8601-review-time> \
  --execution-id <unique-run-id> \
  --output mk1/receipts/f4/executions/<unique-run-id>.json
```

The generated envelope contains the exact immutable fixture input, an empty observed-output field, human-review metadata and every unresolved manual check.

Execution envelopes live below `executions/` and **do not trigger TESTED artifact materialization**.

## Execute

Run the exact F2 prompt artifact against every fixture input under the declared runtime conditions.

Record the actual output verbatim in the execution envelope. Every real fixture requires a non-empty observed output.

Do not edit fixture inputs after seeing model behavior. If a fixture needs correction, version the fixture set and execute again.

## Review

Follow `mk1/specs/F4_HUMAN_REVIEW_PROTOCOL.md`.

Resolve every declared human check as `PASS` or `FAIL` with a concrete evidence note.

Unresolved blocking human checks prevent `TESTED` eligibility.

A model-generated self-judgment is not silently relabeled as human review. Real receipts with declared human checks require:

```text
reviewer_type = human
reviewer_ref  = non-empty stable reviewer reference
reviewed_at   = observed review timestamp
```

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

The receipt binds execution evidence through:

```text
artifact_prompt_fingerprint = SHA-256(exact prompt_body)
fixture_set_fingerprint      = SHA-256(canonical fixture set)
receipt_id                   = content-derived immutable receipt id
```

Changing prompt content, fixture content or receipt content after execution invalidates the relevant integrity check.

The root-level suffix is intentional:

```text
mk1/receipts/f4/*.receipt.json
```

Only these persisted receipt files trigger `.github/workflows/build-mk1-f4-tested.yml`.

## Automatic F4B promotion

When a root-level real receipt is committed, the F4B workflow:

1. validates the canonical quarry;
2. re-runs F1, F2, F3 and F4 characterization gates;
3. rejects unknown artifact IDs or version mismatches;
4. verifies the exact prompt fingerprint;
5. verifies the exact fixture-set fingerprint;
6. verifies receipt-content integrity;
7. rejects synthetic/non-real receipts;
8. rejects missing runtime or human-review metadata;
9. rejects unresolved blocking checks, empty outputs or blocking fixture failures;
10. materializes `mk1/candidates/f4/<artifact>/`;
11. schema-validates the generated TESTED artifact;
12. validates deterministic reconstruction from F2 source + receipt;
13. commits the generated F4 bundle.

Generated F4 bundles retain evidence layers:

```text
artifact.json
behavioral_receipt.json
source.json
prompt.txt
architecture.json
lint.json
critic.json
```

The resulting artifact is allowed to say:

```text
state = TESTED
claims = [engineered, tested]
```

It is still required to say:

```text
baseline_id = null
rubric_score = null
```

because baseline comparison is F5 and certification is F6.

## Repository evidence guard

`tools/validate_mk1_f4_repository.py` fails if a persisted TESTED artifact or receipt:

- has no matching persisted real evidence;
- references another artifact/version;
- uses a prompt fingerprint that no longer matches the F2 source;
- uses a fixture fingerprint that no longer matches the versioned fixture set;
- has been altered without regenerating its receipt id;
- cannot be reconstructed exactly through the canonical promotion function;
- appears while no real F4 receipt exists.

This makes `TESTED` a reproducible evidence state rather than a manually editable label.

## Evidence boundary

F4 proves behavior against a declared fixture set under one identified runtime profile.

It does **not** prove:

- superiority over a baseline;
- general model independence;
- universal reliability;
- certification;
- improvement.

Those claims require later evidence in F5/F6.
