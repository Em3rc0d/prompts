# MK0 Reference Corpus

Reference Corpus preserves potentially useful source material that is **not eligible to act as canonical Prompt Quarry knowledge by default**.

## Epistemic boundary

`REFERENCE_CORPUS_IS_NON_CANONICAL = true`

A reference artifact may be technically useful, well structured, detailed, or highly relevant to another project. None of those properties make it Prompt Quarry truth.

Reference material:

- may contain errors, bias, stale assumptions, incomplete context, or disputed approaches;
- may inform research, comparison, discovery, architecture analysis, or future projects;
- must preserve provenance, observed/reconstructed state, content hash, access boundary, and license status;
- must not define canonical prompt rules by itself;
- must not count as Golden Dataset evidence;
- must not count as F4/F5/F6/F7 behavioral evidence;
- must not be silently used to justify marketing or certification claims;
- must not auto-promote into Golden Dataset because of structural quality, confidence, similarity, or proximity in storage.

## Promotion rule

Promotion from Reference Corpus to Golden Dataset is **not a file move**. It requires a new governed decision:

1. identify a genuinely prompt-like or agent-instruction artifact, potentially at section level;
2. re-establish provenance and artifact identity;
3. reclassify through the Semantic Artifact Gate;
4. satisfy Golden research eligibility;
5. pass the applicable human/governed promotion path;
6. preserve redistribution and behavioral-certification boundaries independently.

Until all of those conditions are satisfied, the source remains `NON_CANONICAL_REFERENCE`.

## Storage principle

`NOT_GOLDEN_ELIGIBLE != NOT_USEFUL`

Useful architecture documentation, manuals, codebase guides, implementation plans, FAQs, logs, design specs, and other technical materials may therefore be retained here without contaminating Prompt Quarry's Golden Dataset.
