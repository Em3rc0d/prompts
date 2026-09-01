# Commerce Hardening Evidence — 2026-09-01

Status: `HARDENED_ON_BRANCH / FULL_WEB_BUILD_NOT_OBSERVED`

## Release identity

```text
product_id          pq-developer-pack
version             1.1.0
archive_size        86763
archive_sha256      546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
source_fingerprint  dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
source_commit       f0accde4aa12ecf4eae530249cb56175e5a28b66
```

## Implemented commerce semantics

```text
provider_test -> provider_test_order_accepted
live_canary   -> live_delivery_canary_order_accepted
live          -> purchase_completed
```

Only the public-live state can produce `purchase_completed`.

## Executed validation

Observed in an isolated validation harness against the current commerce module graph:

```text
TypeScript isolated module-graph typecheck   PASS
Python provider verifier py_compile          PASS
Python provider verifier CLI entrypoint      PASS
provider verifier missing API key behavior   FAIL-CLOSED / PASS
webhook adversarial contract                 16 / 16 PASS
```

Adversarial cases covered:

1. provider-test accepted with the provider-test event;
2. live canary accepted with the canary event;
3. public live alone emits `purchase_completed`;
4. invalid signature rejected;
5. unsupported event ignored;
6. unpaid order ignored;
7. store mismatch ignored;
8. product mismatch ignored;
9. variant mismatch ignored;
10. live order rejected during provider test;
11. test order rejected in live mode;
12. tampered release hash rejected;
13. missing release metadata rejected;
14. wrong signed gate rejected;
15. invalid mode/gate configuration fails closed;
16. malformed payload/order shape rejected.

## Evidence boundary

The isolated TypeScript check used the current commerce modules with minimal environment declarations. It is not a substitute for the repository's production acceptance commands.

```text
full repository npm run typecheck   NOT_OBSERVED
full Next.js npm run build          NOT_OBSERVED
current branch preview deployment   NOT_OBSERVED
production hardening deployment     NOT_OBSERVED
provider custody                    NOT_OBSERVED
provider integration test           NOT_OBSERVED
live delivery canary                NOT_OBSERVED
public sale                         NO
PQ-LAUNCH-0                         NO
PQ-$1                               NO
```

The latest Vercel deployments visible during this validation were created on 2026-08-29 and therefore predate the current commerce hardening. They are not used as evidence for these commits.

Canonical protocol: `commercial/LEMONSQUEEZY_PROVIDER_GATE_V1.md`.

Canonical status: `commercial/STATUS_V1.md`.

`not observed == unknown`
