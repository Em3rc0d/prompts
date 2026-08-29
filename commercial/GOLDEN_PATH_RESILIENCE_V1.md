# Prompt Quarry Golden Path Resilience v1

Status: `WAVE 1 REPAIRED / WAVE 2 OBSERVED`

## Production target

`https://prompt-quarry.vercel.app`

Production deployment: `dpl_5WxCPP6mTuwe9NCwxa3Wnzh77kvk`

## Wave 1 repair

The production build now materializes the canonical Free Pack during `prebuild` and fails if size or SHA-256 diverge.

Canonical Free Pack v1.1.0:

- size: `23,498 bytes`
- SHA-256: `55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32`

The Next.js `postbuild` route-parity gate requires:

- `/free/developer-starter-pack`
- `/developer-pack`
- `/license`
- `/api/free-pack/v1`
- `/api/free-pack/v1.1.0`
- `/api/commerce/developer-pack/checkout`
- `/api/commerce/lemonsqueezy/webhook`

Production build observation:

```text
FREE PACK MATERIALIZE: PASS
GOLDEN PATH BUILD PARITY: PASS
required_routes=7
```

Runtime baseline after repair:

```text
/                                      200
/api/free-pack/v1.1.0                  200 + canonical SHA
/api/commerce/developer-pack/checkout  503 checkout_not_configured / NOT_FOR_SALE
/api/commerce/lemonsqueezy/webhook GET 405 route present, POST-only
```

A checkout `503` is currently correct fail-closed behavior because the paid Developer Pack remains `DRAFT / NOT FOR SALE`. A `404` would be a deployment defect.

## Wave 2 bounded resilience

External Vercel load drivers targeted only Prompt Quarry production. Lemon Squeezy was not load-tested.

Observed Free Pack concurrency envelope:

| Concurrency | Requests | Failures | Integrity failures | p95 | RPS |
|---:|---:|---:|---:|---:|---:|
| 1 | 15 | 0 | 0 | 139.3 ms | 15.94 |
| 5 | 25 | 0 | 0 | 163.3 ms | 28.22 |
| 10 | 40 | 0 | 0 | 130.6 ms | 55.03 |
| 20 | 60 | 0 | 0 | 168.1 ms | 73.95 |
| 40 | 80 | 0 | 0 | 449.3 ms | 102.56 |
| 60 | 120 | 0 | 0 | 146.5 ms | 176.02 |
| 80 | 160 | 0 | 0 | 168.1 ms | 249.16 |
| 120 | 240 | 0 | 0 | 592.2 ms | 198.91 |
| 160 | 320 | 0 | 0 | 349.0 ms | 360.03 |
| 200 | 400 | 0 | 0 | 342.8 ms | 412.64 |

Static landing C10: 30/30 successful, p95 `67.4 ms`.

Post-load Vercel telemetry in the observed window:

```text
200  1497
405  2   expected method probe
503  2   expected commerce fail-closed probe
runtime errors 0
```

Classification:

`HEALTHY_THROUGH_C200_WITHIN_TESTED_ENVELOPE`

No first break was observed. Testing stopped deliberately rather than escalating without a product need.

## What this proves

It supports an infrastructure claim only:

> The repaired Prompt Quarry public surface and Free Pack delivery remained healthy and byte-integral through the bounded production load envelope observed on 2026-08-29, including concurrency 200.

It does not prove:

- unlimited capacity;
- future Vercel behavior;
- Lemon Squeezy/payment capacity;
- F4 TESTED prompt behavior;
- F5 IMPROVED;
- F6 CERTIFIED;
- F7 PORTABLE.

`not observed == unknown`

## Remaining Golden Path blocker

Real commerce remains intentionally blocked until Developer Pack v1.1 is release-approved and Lemon Squeezy is provisioned. The next provider acceptance sequence is:

```text
configure real/test checkout
→ checkout route 302
→ signed order_created webhook
→ purchase_completed evidence
→ paid delivery verification
→ PQ-LAUNCH-0
→ first real revenue
```
