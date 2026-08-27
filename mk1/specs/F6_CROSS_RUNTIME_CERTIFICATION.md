# MK1 F6 — Cross-runtime certification

F6 is the final MK1 promotion gate.

It does **not** prove that a prompt is universally correct. It proves that the exact frozen prompt preserved the F4/F5 behavioral and superiority contract across multiple independently identified runtime families.

## Source state

F6 accepts only an exact F5 `CANDIDATE` artifact carrying:

- `engineered`
- `tested`
- `improved`

The candidate must remain byte-identical in `prompt_body`, artifact id and artifact version to the `TESTED` artifact that produced its F5 evidence.

## Evidence model

The primary F5 receipt stored in the candidate bundle is always included as evidence.

Additional real F5 receipts live under:

`mk1/receipts/f6/`

They are supplemental cross-runtime evidence; they do not create additional candidate artifacts.

Every F5 receipt used by F6 must independently satisfy all F5 improvement rules:

1. `execution_mode` is `api` or `manual-observed`.
2. `status = IMPROVEMENT_PASS`.
3. `eligible_for_improved = true`.
4. exact artifact id/version.
5. exact engineered prompt SHA-256.
6. exact baseline id and prompt SHA-256.
7. exact fixture-set id/version/SHA-256.
8. exact parent F4 receipt lineage.
9. engineered blocking pass rate = `1.0`.
10. rubric score = `100.0`.
11. zero engineered failures.
12. zero regressions.
13. zero unresolved engineered human checks.
14. zero baseline A/B wins.
15. material engineered blind wins.
16. complete runtime identity: provider/model/family/run_at.
17. blinded human review with reviewer reference, review timestamp and randomization reference.

## Runtime diversity gate

Certification requires at least **three distinct declared runtime families**.

The following cannot be counted twice:

- same F5 receipt id,
- same execution id,
- same blind randomization reference,
- same runtime family (case-insensitive).

The F5 receipt that originally created the `CANDIDATE` must be present in the evidence set.

## State transition

`CANDIDATE -> CERTIFIED`

A certified artifact carries exactly:

- `engineered`
- `tested`
- `improved`
- `certified`

Its evaluation receipt becomes the F6 certification receipt and its rubric score remains 100.

## Certification receipt

F6 produces a deterministic integrity-protected receipt containing:

- artifact id/version,
- engineered prompt SHA-256,
- baseline id/SHA-256,
- fixture-set id/version/SHA-256,
- parent F4 receipt id,
- source F5 candidate receipt id,
- all accepted F5 evidence receipt ids,
- runtime identities,
- review identities,
- runtime-family count and inventory,
- certification timestamp derived deterministically from the evidence,
- certification status and claim policy.

Changing the prompt, baseline, fixture set, evidence receipt, runtime identity, review metadata or receipt inventory invalidates deterministic reconstruction.

## Zero and partial evidence states

F6 is allowed to be green without producing a false certification:

- `NO_F5_CANDIDATES`: no improved candidate exists yet.
- `PENDING_RUNTIME_EVIDENCE`: candidate exists, but fewer than three distinct valid runtime families are available.
- `CERTIFIED_ARTIFACTS_MATERIALIZED`: at least one candidate satisfies the full F6 gate.

A pending state is not a failure and is not certification.

## Meaning of CERTIFIED

`CERTIFIED` means:

> Under the frozen MK1 fixture, baseline, review and runtime-evidence protocol, this exact prompt achieved 100% blocking pass, retained F5 superiority with zero observed regressions/baseline wins, and repeated that result across at least three distinct declared runtime families.

It does **not** mean:

- correct for every possible input,
- correct for every future model,
- mathematically proven,
- permanently certified after prompt drift,
- superior outside the declared benchmark scope.
