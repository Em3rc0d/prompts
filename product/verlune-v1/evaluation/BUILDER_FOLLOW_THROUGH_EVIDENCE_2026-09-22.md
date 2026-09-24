# Verlune v1 — Builder Follow-Through Evidence

Status: `OBSERVED FOLLOW-THROUGH PASS / FULL BUILDER MATRIX OPEN`

Date: 2026-09-22

## Frozen Builder identities observed

### Prompt Builder

- Builder ID: `VP-BUILDER-001`
- customer surface: `product/verlune-v1/premium/builders/prompt-builder.md`
- Git blob SHA at observation: `9e89741f2802d2d49816acc74abd84a5d3178d9e`

### Workflow Builder

- Builder ID: `VP-BUILDER-002`
- customer surface: `product/verlune-v1/premium/builders/workflow-builder.md`
- Git blob SHA at observation: `3a479f0cc5411383b813394685b91649a1b603fc`

## Observation A — Workflow Builder customer-like run

The exact Workflow Builder surface was pasted into a clean consumer-AI conversation.

The user described a recurring operational problem in plain language: repeatedly checking invoice status from exported business-system spreadsheets and preparing a customer email.

Observed behavior:

- began with the required plain-language intake question;
- reconstructed the process without requiring workflow-design terminology;
- asked two small rounds of materially relevant questions;
- clarified source format, invoice-status evidence, recipient resolution, one-invoice-per-request behavior, customer identity, and human review;
- did not treat a generic email domain as proof of customer identity;
- preserved human approval before sending;
- produced a reusable workflow with inputs, stages, states, fallback, verification, reuse instructions, and quick tests.

Review dimensions:

- plain_language_intake: PASS
- question_efficiency: PASS
- goal_preservation: PASS
- required_inputs: PASS
- assumption_discipline: PASS
- fallback_quality: PASS
- output_usability: PASS
- verification_quality: PASS
- reuse_quality: PASS
- certification_boundary: PASS

Disposition: `PASS`

This observation is customer-like evidence, but it is not substituted for one of the frozen 32 category-matrix cases.

## Observation B — Generated Workflow, second clean instance

The workflow generated in Observation A was executed in a separate clean conversation with real XLSX business data.

Privacy note: raw company names, tax identifiers, invoice identifiers, amounts, payment dates, email addresses, and source spreadsheets are intentionally **not committed to this public evidence file**.

Observed behavior:

1. With no specific invoice identifier, the workflow returned `NEEDS_INFORMATION` instead of selecting an arbitrary record.
2. After a concrete invoice identifier was supplied, the instance reconciled the available spreadsheet sources.
3. It kept payment-status evidence separate from recipient-identity evidence.
4. It refused to infer a recipient from insufficient evidence.
5. It returned `NEEDS_RECIPIENT_REVIEW` and produced a bounded draft for human review.
6. It did not send the email.

Disposition: `PASS`

This closes the required follow-through observation for **one generated workflow**.

## Observation C — Generated Prompt, second clean instance

A Prompt Builder artifact was observed for a recurring writing task: converting technical change notes into a concise executive email for a non-technical client while preserving facts and avoiding invented commitments.

Generated artifact qualities observed:

- clear single job;
- required and optional inputs;
- stable instructions separated from per-run data;
- explicit missing-information behavior;
- output contract;
- verification;
- quick normal and ambiguous-input tests;
- explicit non-certification boundary.

The full Prompt Builder intake transcript was not retained in the evidence provided, so Prompt Builder intake/question-efficiency is **not** considered closed by this observation alone.

The generated prompt was then executed in a second clean conversation with terse technical notes. The new instance:

- did not immediately draft from ambiguous notes;
- asked only two material clarification questions;
- did not invent deployment environment, latency numbers, dates, commitments, or production status;
- preserved uncertain batch impact as unconfirmed;
- produced a concise client-readable email after clarification.

Disposition:

- generated_prompt_artifact_quality: `PASS`
- generated_prompt_second_instance_execution: `PASS`
- prompt_builder_intake_ux_from_this_observation: `NOT_FULLY_OBSERVED`

This closes the required follow-through observation for **one generated prompt**.

## Builder gate state after these observations

```text
Workflow Builder customer-like observed case    PASS
Generated workflow second-instance execution    PASS
Generated prompt second-instance execution      PASS

Prompt Builder full intake UX matrix             OPEN
32 category Builder scenarios                     OPEN
5 cross-category stress scenarios                 OPEN
cross-model portability                           OPEN
human product review H1-H11                       OPEN
```

## Claim boundary

These observations demonstrate that the current Builder architecture can produce a prompt and a workflow that remain usable in a second clean instance.

They do **not** establish:

- full Builder matrix completion;
- universal Builder robustness;
- cross-model portability;
- customer-market validation;
- certification;
- production readiness.

A generated customer artifact remains `GENERATED` unless stronger evidence is earned.
