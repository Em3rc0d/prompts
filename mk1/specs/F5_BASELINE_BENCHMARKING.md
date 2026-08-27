# MK1 F5 — Paired Baseline Benchmarking

## Purpose

F5 answers one question only: **does the TESTED engineered prompt outperform a task-equivalent baseline under the same observed conditions?**

F4 proves behavioral acceptability. F5 is the first stage allowed to support the claim `improved`.

## Evidence boundary

F5 accepts only an artifact already in `TESTED` state with a real F4 receipt. It never upgrades a merely `VALID` prompt.

Every benchmark freezes:

- exact engineered prompt SHA-256;
- exact baseline prompt SHA-256;
- exact F4 fixture-set SHA-256;
- parent F4 receipt ID;
- provider, model and runtime parameters;
- repeat count;
- blind randomization reference;
- human reviewer identity and review timestamp;
- full paired outputs and human-check decisions.

Changing any frozen input invalidates the benchmark receipt.

## Baseline policy

The primary F5 baseline is a deterministic **task-equivalent minimal baseline** built from the same task brief. It must express the task goal and required variables, but it must not copy the engineered architecture, quality gates, fallback machinery or MK1 reliability sections.

This baseline answers: *does Prompt Forge engineering add value beyond a reasonable minimal prompt for the same task?*

External/MK0 baselines may be added later as additional benchmark participants, but they may not replace the deterministic primary baseline without a new benchmark version.

## Paired execution

For each artifact:

1. use the exact same fixture set for engineered and baseline;
2. use the exact same provider/model/runtime configuration;
3. execute at least **3 repeats per fixture per participant**;
4. preserve every observed output;
5. apply the same machine assertions and declared human checks;
6. perform a blind A/B preference review for each pair;
7. never use model self-judgment as the required human preference review.

With the current F4 matrix this means 10 fixtures × 3 repeats × 2 participants = **60 observed outputs per artifact** minimum.

## IMPROVED gate

A real F5 receipt is `IMPROVEMENT_PASS` only when all conditions hold:

- source artifact is `TESTED`;
- repeat count >= 3;
- every engineered blocking evaluation passes across every repeat (**100% blocking pass rate**);
- engineered has zero regressions where baseline passes but engineered fails;
- all human checks are resolved;
- blind review metadata is complete;
- baseline A/B wins = 0;
- engineered A/B wins are at least 30% of all pairs; remaining pairs may be ties;
- receipt integrity and all prompt/fixture fingerprints validate.

A total tie is **not** evidence of improvement. A higher average score cannot compensate for one blocking behavioral regression.

## State transition

`TESTED -> CANDIDATE` is allowed only from a real `IMPROVEMENT_PASS` receipt.

The promoted artifact receives:

- claims: `engineered`, `tested`, `improved`;
- `evaluation.baseline_id` = exact baseline ID;
- `evaluation.fixture_set_id` = benchmark fixture set;
- `evaluation.receipt_id` = F5 receipt ID;
- `evaluation.rubric_score` = engineered blocking pass percentage (must be 100 at this stage);
- `evaluation.blocking_failures` = `[]`.

`CANDIDATE` + `improved` still does **not** mean portable or universally superior. Cross-runtime certification is a separate gate.

## Claim discipline

- synthetic benchmark -> harness characterization only;
- real benchmark with any engineered blocking failure -> FAIL;
- real benchmark with any A/B baseline win -> FAIL for `improved`;
- real benchmark with only ties -> no `improved` claim;
- one runtime -> no portability claim;
- F5 never means universally “100% correct”.

The strongest valid statement after F5 is: **100% pass on the declared adversarial matrix for the identified runtime and demonstrably better than the frozen task-equivalent baseline under the paired benchmark contract.**
