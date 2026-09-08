# Evidence and claim boundary

This file defines the strongest claims supported for Prompt Machine Starter — Code Review Edition `1.0.0`.

## Exact workflow identity

```text
workflow_id  pm-starter-evidence-first-code-review-v2
contract     2.2.0
bytes        25,295
sha256       6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
authority    ADVISORY_ONLY
```

`WORKFLOW.md` is generated from the exact certified composite identity: Evidence-first Code Review v2.1 base plus the normative v2.2 hardening addendum in the frozen composition order.

Version `1.0.0` changes only the customer packaging layer relative to the preceding release candidates. It does not change the certified `WORKFLOW.md` bytes.

## Observed behavioral evidence

Final regression batch:

```text
batch                 PM-STARTER-CR-V2-G08-BATCH-0003
provider              GOOGLE_GEMINI_API
model                 gemini-3.5-flash
required cases        4
clean observations    4
human-review PASS     4/4
automatic retries     0
evaluation at runtime NO
expected at runtime   NO
result                PASS
```

The tested matrix observed these properties:

- uncertainty remained visible when a material external authorization boundary was not supplied;
- embedded instructions inside task data did not become workflow authority;
- a supplied owner/admin guard could satisfy the target invariant without forcing a substitute finding;
- a complete supplied no-guard boundary could support `CONFIRMED / BLOCK`;
- conditional downstream impacts stayed conditional;
- the required output contract completed in the final passing matrix.

## G09 classification

Current portability classification: `MODEL_SPECIFIC`.

Behavior is validated only for the demonstrated Gemini 3.5 Flash scope. No second model family has a clean behavioral observation in this certification cycle.

Therefore this release must not be described as:

- universally portable;
- model-agnostic;
- working on every model;
- provider-independent across all providers.

## Certification

Certification ID:

`PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`

Decision:

`PASS_FOR_EXACT_DECLARED_SCOPE`

The certification covers the exact v2.2 surface and frozen four-case Gemini 3.5 Flash evidence scope. It does not certify all code-review scenarios, all models, universal software security, customer outcomes, or willingness to pay.

## Historical failures are part of the evidence

This workflow was not declared successful after its first result. The preserved path includes an over-certainty failure, failure mining, a versioned successor, truncation/runtime configuration failure, repeated speculative-finding failures, hardening, and the final 4/4 passing regression batch.

Certification is tied to the final workflow candidate and final passing evidence, not to an erased history.

## Packaging and license evidence

Version `1.0.0` freezes the customer-facing usage license, sale terms, operating guide, evidence notes, and exact certified workflow identity into one deterministic package.

Package integrity does **not** broaden the behavioral certification. In particular, it does not prove:

- universal model portability;
- automatic correctness or security of reviewed software;
- a particular customer or business outcome;
- that a human ship decision can be skipped.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
