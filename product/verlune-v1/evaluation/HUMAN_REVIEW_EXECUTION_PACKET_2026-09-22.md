# Verlune v1 — External Human Review Execution Packet

Status: `READY / EXTERNAL REVIEWER REQUIRED`

Frozen product candidate: `886060c1f991aadd4b458f05fc7c62056942e9ca`

## Eligibility

The reviewer must not depend on Prompt Machine repository knowledge or prior explanations of Verlune's internal taxonomy. A reviewer deeply involved in constructing the product may provide useful feedback, but does not satisfy this external comprehension gate.

## Review environment

Present only customer-facing candidate surfaces, examples, evidence/limitations cards, and the candidate access experience. Do not show internal certification machinery unless the reviewer explicitly asks.

## H1–H11 script

1. **H1 Product comprehension** — Ask the reviewer, without coaching, to explain what Verlune is, Prompt vs Workflow, Free vs Premium, Builders, and where AI execution happens.
2. **H2 Free usefulness** — Use Free assets from at least three categories on real bounded tasks.
3. **H3 Premium depth** — Compare Premium assets against Free and record what capability difference the reviewer actually perceives.
4. **H4 Prompt vs Workflow** — Show both artifact types without explaining the distinction first.
5. **H5 Prompt Builder** — Start from a plain-language recurring bounded task and create a reusable prompt.
6. **H6 Workflow Builder** — Start from a plain-language recurring process; create a workflow and reuse it in a second clean instance.
7. **H7 Cross-category credibility** — Review at least one launch-core asset in all eight categories.
8. **H8 Free vs Premium purchase logic** — Ask verbatim: "Ignoring our internal effort, what do you actually get by paying?"
9. **H9 USD 9 threshold** — Ask verbatim: "Does this product make you reasonably think: 'this may solve enough recurring AI work that I'd pay USD 9 to try it'?" Record objections verbatim.
10. **H10 Trust boundary** — Verify tested/untested, generated/certified and model-scope boundaries are understandable without dominating the product.
11. **H11 Friction** — Observe FIND → UNDERSTAND INPUTS → USE IN AI → GET RESULT → VERIFY; for Premium also UNLOCK → FIND → USE → OPEN BUILDER → CREATE → REUSE.

## Blocking rule

No score averaging. Every H1–H11 section must pass for `PASS_FOR_LANDING_REDESIGN` or `PASS_WITH_NONBLOCKING_NOTES`.

## Evidence capture

Record:
- reviewer identifier or pseudonym;
- date/time;
- exact candidate commit;
- exact assets used;
- H1–H11 PASS/FAIL;
- failures;
- objections verbatim;
- rejected/demoted assets;
- final disposition.

## Current execution state

`NOT_EXECUTED` — no eligible external reviewer has been observed in this execution environment.
