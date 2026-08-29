# Prompt Quarry Product Quality Audit v1

Status: `OPEN / REMEDIATION IN PROGRESS`

## Incident

Severity: `CRITICAL — PUBLIC ARTIFACT DIVERGENCE`

The first Vercel bootstrap deployment exposed a Free Starter Pack ZIP whose prompt bodies were abbreviated relative to the governed repository source. A customer inspecting the public download could therefore receive an artifact that did not represent the product source of truth.

The incident was detected during direct product inspection before public launch and before paid checkout was enabled.

## What failed

```text
GOVERNED SOURCE
   !=
MANUALLY ASSEMBLED BOOTSTRAP DEPLOYMENT PAYLOAD
   ->
PUBLIC FREE ZIP DIVERGED
```

The failure was not a Prompt Quarry evidence-state claim failure. It was a distribution-integrity failure.

The first bootstrap deployment was manually assembled to establish a public Vercel URL. During that assembly, customer-visible Free Pack content was shortened instead of being copied byte-for-byte from the governed source.

## New truth rule

```text
DEPLOYMENT_READY != ARTIFACT_INTEGRITY
```

A Vercel `READY` state proves that Vercel built and deployed the submitted files. It does not prove that the submitted files equal the governed product source.

Public distribution is acceptable only when:

```text
GOVERNED SOURCE
  -> RELEASE MANIFEST
  -> GENERATED DELIVERY SNAPSHOT
  -> DETERMINISTIC ARCHIVE
  -> RUNTIME HASH CHECK
  -> PUBLIC RESPONSE
```

all identify the same artifact.

## Free Pack remediation

The Starter Pack has been hardened as `v1.1.0`.

The customer payload remains intentionally small — exactly seven files — but the three prompts are now field-ready workflow contracts rather than short prompt descriptions.

### Code Review

Adds:
- review target and change intent;
- runtime context and invariants;
- evidence levels (`CONFIRMED`, `LIKELY`, `QUESTION`);
- severity rubric;
- behavioral review process;
- finding-level evidence/failure/fix/verification contract;
- explicit ship decision;
- insufficient-context fallback.

### Bug Diagnosis

Adds:
- expected vs observed behavior;
- reproduction/environment/evidence intake;
- `OBSERVED / INFERRED / UNKNOWN / DISPROVED` labels;
- observation ledger;
- ranked hypothesis set;
- discriminating diagnostic checks;
- `DIAGNOSE_FIRST / MITIGATE_NOW / FIX_SUPPORTED` status;
- verification and remaining-unknowns contract.

### Technical Decision

Adds:
- decision horizon;
- hard constraints and weighted preferences;
- known evidence and known unknowns;
- evidence ledger;
- option comparison under shared criteria;
- stress test and reversibility;
- `DECIDE / CONDITIONAL / HOLD` status;
- reversal triggers;
- next highest-information validation step.

### Quickstart

Now teaches how to use, inspect, and deliberately adapt those contracts on a real task instead of merely listing setup steps.

## Free Pack v1.1 canonical identity

```text
product_id      pq-developer-starter
version         1.1.0
customer_files  7
archive_size    23498 bytes
archive_sha256  55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
```

This fingerprint was independently reconstructed from the seven current Git blobs using the same deterministic ZIP contract used by the Next.js delivery route.

The previous v1.0 archive fingerprint is historical only and must not be used for current public distribution.

## Paid Developer Pack decision

`Developer Pack v1.0.0` remains historically:

```text
package_state    READY
asset_maturity   VALID
```

Those statements describe its governed package/release history and are not retroactively rewritten.

However, the product is now:

```text
SALE_STATUS      WITHHELD_FROM_SALE
REASON           PRODUCT_QUALITY_HARDENING_REQUIRED
```

The current checkout remains fail-closed.

The next paid iteration must be a new governed release (`v1.1.x` or later). Do not silently edit the frozen v1.0 customer-visible assets, because doing so would invalidate their approved fingerprint/release identity.

The paid hardening gate must answer a commercial question in addition to static validity:

> Would a developer who used the Free Pack immediately understand why the paid system is materially more reusable, operational, and valuable than three good prompts?

Until the answer is supported by product inspection and a new governed release, do not enable payment.

## Corrective actions

1. Harden Free Starter Pack prompts and Quickstart. — `DONE`
2. Recompute file identities and deterministic archive fingerprint from exact Git blobs. — `DONE`
3. Update Free release manifest to v1.1.0. — `DONE`
4. Update Next.js generated delivery snapshot and web copy. — `DONE`
5. Bind web acceptance test to v1.1 version/size/hash. — `DONE`
6. Redeploy exact governed web source to Vercel. — `PENDING`
7. Observe public `/api/free-pack/v1` returning v1.1 headers and runtime-verified hash. — `PENDING`
8. Replace manual Vercel bootstrap deployment process with Git-linked or otherwise reproducible source deployment. — `PENDING`
9. Design and govern Developer Pack v1.1 product-quality release. — `NEXT AFTER FREE REMEDIATION`
10. Keep Lemon Squeezy checkout disabled until paid v1.1 and C5 are verified. — `ENFORCED`

## Closure condition

This incident is closed only when the public Prompt Quarry endpoint serves Free Starter Pack v1.1 with the canonical fingerprint above and the deployment source is reconciled with the governed web tree.

`not observed == unknown`
