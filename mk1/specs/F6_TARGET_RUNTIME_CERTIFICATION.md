# MK1 F6 — Target-runtime certification

F6 is the MK1 certification gate.

Its purpose is to prove that an exact Prompt Quarry engineered prompt is not merely successful once: it repeatedly preserves its F4 behavioral contract and F5 superiority on a declared **target runtime**.

F6 is deliberately separate from cross-provider portability. Portability belongs to F7.

## Source state

F6 accepts only an exact F5 `CANDIDATE` carrying:

- `engineered`
- `tested`
- `improved`

The prompt body, artifact id/version, baseline and fixture set remain frozen.

## Certification evidence

Certification requires at least **three independent real F5 IMPROVEMENT_PASS receipts** for the exact same:

- provider;
- model;
- runtime family;
- engineered prompt SHA-256;
- baseline SHA-256;
- fixture-set SHA-256;
- parent F4 TESTED receipt.

Every F5 receipt must independently retain:

- real execution mode (`api` or `manual-observed`);
- 100% blocking pass;
- rubric score 100;
- zero engineered failures;
- zero regressions;
- zero unresolved engineered human checks;
- zero baseline blind A/B wins;
- material engineered blind wins;
- complete runtime identity evidence;
- blinded human review.

The three certification executions must also have distinct:

- F5 receipt ids;
- execution ids;
- blind randomization references;
- runtime identity-evidence references.

Each F5 benchmark already requires at least three internal repeats. F6 therefore certifies repeatability at two levels: repeated samples inside each benchmark and repeated independent benchmark executions.

## Target runtime

The first/primary F5 receipt defines the target runtime:

```text
provider + exact model + family
```

Every additional F6 receipt must match that normalized identity exactly.

Provider/model/family drift is rejected rather than silently counted as additional confidence. Cross-provider/model diversity belongs to F7.

## State transition

```text
CANDIDATE
    ↓ F6
CERTIFIED
```

A certified artifact carries:

- `engineered`
- `tested`
- `improved`
- `certified`

## Meaning of CERTIFIED

`CERTIFIED` means:

> Under the frozen MK1 fixture, baseline, review and evidence protocol, this exact prompt achieved 100% blocking pass, retained measured F5 superiority with zero observed regressions/baseline wins, and reproduced that result across at least three independent blinded benchmark executions on the same declared target provider/model/family.

It does **not** mean:

- universally correct;
- portable to every provider;
- correct for every possible input;
- permanently certified after prompt, baseline, fixture or runtime drift.

## Portability

After certification, F7 may test the same exact prompt on other provider/model families.

```text
CERTIFIED
    ↓ F7 cross-provider evidence
PORTABLE
```

`PORTABLE` is an additional property. It is never required for `CERTIFIED`.

## Zero/partial evidence states

F6 may remain green without inventing certification:

- `NO_F5_CANDIDATES`
- `PENDING_INDEPENDENT_RUNTIME_REPETITIONS`
- `CERTIFIED_ARTIFACTS_MATERIALIZED`

A pending state is not certification.
