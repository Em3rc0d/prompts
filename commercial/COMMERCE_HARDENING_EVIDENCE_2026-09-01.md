# Commerce Hardening Evidence — 2026-09-01

Status: `COMMERCE_BUILD_READY / PROVIDER_EVIDENCE_PENDING / NOT_DEPLOYED`

## Release identity

```text
product_id          pq-developer-pack
version             1.1.0
archive_size        86763
archive_sha256      546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
source_fingerprint  dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
source_commit       f0accde4aa12ecf4eae530249cb56175e5a28b66
```

## Commerce semantics

```text
provider_test -> provider_test_order_accepted
live_canary   -> live_delivery_canary_order_accepted
live          -> purchase_completed
```

Only the public-live state can produce `purchase_completed`.

## Local adversarial validation

```text
TypeScript isolated module-graph typecheck   PASS
Python provider verifier py_compile          PASS
Python provider verifier CLI entrypoint      PASS
provider verifier missing API key            FAIL-CLOSED / PASS
webhook adversarial contract                 16 / 16 PASS
```

The adversarial contract covers valid provider-test/canary/public-live events plus invalid signature, unsupported event, unpaid order, store/product/variant mismatch, test/live mismatch, tampered or missing release identity, wrong commerce gate, invalid mode/gate configuration, malformed JSON, and missing order shape.

## Clean-checkout CI evidence

Validated branch head:

```text
7d910cfbba537ac62dc8e8186b43282483b37dd0
```

### Test Commerce v0

```text
workflow_run     33509477412
job              commerce-acceptance
conclusion       SUCCESS
compile tooling  PASS
contract test    PASS
```

### Test Commercial Web v0

```text
workflow_run                   33509477240
job                            nextjs-acceptance
conclusion                     SUCCESS
npm install                    PASS
npm run typecheck              PASS
npm run build                  PASS
Free Pack materialization      PASS
Free Pack bytes                23498
Free Pack sha256               55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
Next.js compilation            PASS
Golden Path build parity       PASS
required build routes          7
commercial boundary validator  PASS
```

The build was executed by GitHub Actions on a clean Ubuntu runner with Node 22. The Free Pack build materializer fetched the canonical public v1.1.0 release and verified its exact size/hash before Next.js compilation.

## Defects discovered and closed during acceptance

1. Clean-checkout typecheck initially could not resolve the build-materialized `@/generated/free-pack-archive` module. A declaration file now supplies compile-time shape while `prebuild` remains responsible for materializing and verifying actual bytes.
2. Commerce acceptance still encoded the obsolete `test_mode_not_allowed`/single-checkout contract. It now validates `provider_test`, `live_canary`, and `live` semantics.
3. Commercial Web acceptance still expected the removed `NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL`. It now requires the server commerce gate and default `NOT_FOR_SALE` public state.
4. Commercial Web acceptance encoded a historical `Geist` font choice as a release invariant. It now validates the actual metadata, semantic navigation, accessibility labels, and Prompt Quarry brand shell instead of a non-semantic visual implementation detail.

No release gate was weakened to obtain green CI; stale assertions were replaced with current security/evidence invariants.

## Evidence boundary

```text
full repository npm run typecheck   PASS
full Next.js npm run build          PASS
Golden Path build parity            PASS
commercial web boundaries           PASS
commerce acceptance                 PASS
current branch preview deployment   NOT_OBSERVED
production hardening deployment     NOT_OBSERVED
provider custody                    NOT_OBSERVED
provider integration test           NOT_OBSERVED
live delivery canary                NOT_OBSERVED
public sale                         NO
PQ-LAUNCH-0                         NO
PQ-$1                               NO
```

The currently observed Vercel production deployment predates this hardening and is not evidence for these commits.

Canonical protocol: `commercial/LEMONSQUEEZY_PROVIDER_GATE_V1.md`.

Canonical status: `commercial/STATUS_V1.md`.

`not observed == unknown`
