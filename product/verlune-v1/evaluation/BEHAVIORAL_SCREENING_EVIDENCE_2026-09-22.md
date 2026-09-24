# Verlune v1 — Behavioral Runtime Screening Evidence

Status: `OBSERVED_SCREENING_PASS / FORMAL_RELEASE_BINDING_OPEN`

Date: 2026-09-22

## Purpose

Record the runtime evidence gathered during the 2026-09-22 manual screening campaign without upgrading it into stronger release evidence than the execution method supports.

## Observed screening result

- raw observations: **104**
- PASS: **104**
- FAIL: **0**
- INCONCLUSIVE: **0**
- primary execution mode: `MANUAL-OBSERVED / SINGLE_CHAT_SEGMENTED`
- purpose: failure finding, behavioral screening, and coverage exploration

The suite exercised normal, incomplete, contradictory, noisy, adversarial, authority-boundary, evidence-discipline, causal-overreach, security, idempotency, learning-calibration, decision, research, and marketing-claim cases across the launch categories.

## Evidence boundary

These 104 observations are useful evidence that the Verlune methodology behaved well under the screened scenarios.

They are **not yet the formal 87-case release qualification** defined in `RUNTIME_TEST_PLAN.json`.

The release protocol requires the runtime execution to be bound to the exact frozen customer asset/version. Most screening batches used purpose-built test envelopes that represented the intended behavior but were not proven, case by case, to contain the exact bytes of the current customer asset.

Most later observations were also executed in single-chat segmented mode. That is acceptable for rapid behavioral screening, but it is weaker than isolated fresh-context execution because context leakage cannot be excluded.

Therefore:

```text
104/104 behavioral screening observations PASS
!=
87/87 formal exact-asset runtime release cases PASS
```

## What remains for formal runtime qualification

1. Bind each required case to the exact current customer asset bytes.
2. Record exact asset identity/hash with the fixture and runtime output.
3. Execute the frozen asset without rewriting it inside the test envelope.
4. Preserve PASS / FAIL / INCONCLUSIVE review against the frozen contract.
5. Use isolated reruns for representative/high-risk cases where context independence matters.
6. Record model/host scope before making portability claims.

## Claim boundary

Safe:

> Verlune v1 completed 104 manual behavioral screening observations with no observed blocking failure.

Not yet supported:

- 87/87 formal release qualification complete;
- universally robust;
- certified;
- production-proven;
- battle-tested across real users;
- portable across leading AI assistants.

## Related evidence

- `STATIC_SURFACE_AUDIT_2026-09-22.json`
- `RUNTIME_TEST_PLAN.json`
- `BUILDER_TEST_MATRIX.json`
- `BUILDER_FOLLOW_THROUGH_EVIDENCE_2026-09-22.md`

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
