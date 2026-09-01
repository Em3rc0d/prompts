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

## Free Pack v1.1 Vercel delivery-integrity preview

A dedicated isolated Vercel preview was created to test the canonical v1.1 buffer without changing the production alias.

Observed deployment:

```text
deployment_id   dpl_FSz16X8rci5GNGMxmee6PofqMgMZ
environment     preview
deployment      READY
runtime         Node.js / Next.js
```

Observed `GET /api/integrity` response at `2026-08-29T02:04:45Z`:

```text
http_status       200
status            PASS
version           1.1.0
size_bytes        23498
sha256            55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
expected_size     23498
expected_sha256   55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
match             true
```

The preview runtime reconstructs the customer ZIP buffer and calculates its SHA-256 before returning PASS. The download route shares the same verified `archive()` function.

A direct binary-body inspection of `/api/free-pack/v1` was **not observed** because the connected Vercel fetch client was redirected through preview SSO and did not preserve the authentication cookie required to inspect the binary response. Do not upgrade this evidence into a direct download observation.

Canonical receipt:

`.ci/free-developer-starter-v1/delivery-preview-v1.1.json`

Classification:

```text
FREE_V1_1_DELIVERY_PREVIEW     PASS
PRODUCTION_FREE_V1_1_DELIVERY  NOT_RECONCILED
PUBLIC_INCIDENT_CLOSED         NO
```

This preview establishes delivery integrity only. It does not establish F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE`.

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

The next paid iteration is a new governed release under `product/developer-pack-v1.1/`. The frozen v1.0 customer-visible assets remain untouched.

## Developer Pack v1.1 hardening status

State:

```text
package_state    DRAFT
asset_maturity   DRAFT
sale_status      NOT_FOR_SALE
F4_TESTED        NO
F5_IMPROVED      NO
F6_CERTIFIED     NO
F7_PORTABLE      NO
```

The current product-quality slice includes:

- `README.md` — v1.1 product thesis and release boundary;
- `SPEC.md` — Free-vs-Paid boundary and reusable operating architecture;
- `QUICKSTART.md` — customer-first 15-minute workflow configuration path;
- `LICENSE.md` — proprietary commercial use/adapt, no resale/redistribution;
- `quality/COMMERCIAL_VALUE_GATE.md` — blocking static customer-value gate;
- `templates/general-operating-contract.md` — reusable input/context/evidence/decision/output/verification architecture;
- `templates/software-code-review-system.md` — configurable review policy, lenses, evidence threshold, severity and ship transitions;
- `templates/technical-research-decision-system.md` — configurable constraints, criteria, source/freshness policy, evidence quality, reversibility and decision states;
- `contracts/workflow-contract.schema.json` — JSON Schema draft 2020-12 machine-readable workflow interface;
- `contracts/code-review-policy.example.json` — concrete machine-readable team review policy;
- `methodology/adaptation-playbook.md` — policy vs instance-data adaptation method and change-control rules;
- `checklists/workflow-static-review.md` — static inspection checklist and runtime-test readiness states;
- `examples/code-review-policy-transformation.md` — worked transformation from vague PR request to explicit team review policy;
- `tools/test_developer_pack_v1_1_quality.py` — static architecture regression guard;
- `.github/workflows/test-developer-pack-v1-1-quality.yml` — CI entrypoint for that guard.

### Structural inspection

The three core templates currently have repository sizes:

```text
general-operating-contract.md            7224 bytes
software-code-review-system.md           7740 bytes
technical-research-decision-system.md    8654 bytes
```

The static guard defines a 6000-byte minimum as a coarse anti-regression floor plus required operating-interface tokens. This size floor is not itself a quality proof; it only prevents accidental regression to minimal skeleton assets.

### Static guard correction

An inspection found a real test-design defect before any successful runner execution: the first version scanned the entire governance corpus for forbidden marketing phrases such as `battle-tested` and `proven superior`. The SPEC itself names those phrases as claims that must **not** be made, so a real runner would have false-failed.

The guard was corrected to scope unsupported-claim scanning to customer-facing usage/sales surfaces while allowing governance documents to describe forbidden claims as policy.

The guard was then expanded to parse and inspect the machine-readable contracts, adaptation playbook, Quickstart, checklist, and worked transformation.

### CI observation

Workflow run `33227419340` was triggered from commit `f6eec5510fada623408218b1e2a4c0fa54c35e7a`.

Observed job state:

```text
job          static-product-quality
conclusion   failure
runner_id    0
runner_name  ""
steps        []
```

Therefore:

```text
CI_PASS                  NOT OBSERVED
TEST_FAILURE             NOT OBSERVED
RUNNER EXECUTION         NOT OBSERVED
CURRENT CLASSIFICATION   CI INFRASTRUCTURE / RUNNER UNASSIGNED
```

Do not modify product content in response to that run unless a later execution actually runs validation steps and reports a product failure.

### Commercial distinction being enforced

The Paid Pack must demonstrate this statement through customer-visible assets:

> The Free Pack gives me three strong prompts. Developer Pack gives me the construction and governance system I can reuse to build many of my own workflows.

The Commercial Value Gate blocks release-candidate packaging unless the Paid system materially improves reuse breadth, parameterization, governance, verification, adaptation speed, integration value, and inspectability relative to the Free Pack.

Passing that static gate would still not establish behavioral superiority or F4–F7 evidence.

## Corrective actions

1. Harden Free Starter Pack prompts and Quickstart. — `DONE`
2. Recompute file identities and deterministic archive fingerprint from exact Git blobs. — `DONE`
3. Update Free release manifest to v1.1.0. — `DONE`
4. Update Next.js generated delivery snapshot and web copy. — `DONE`
5. Bind web acceptance test to v1.1 version/size/hash. — `DONE`
6. Execute isolated Vercel runtime integrity preview against Free v1.1 canonical buffer. — `DONE / PASS`
7. Redeploy exact governed full web source to Vercel production. — `PENDING / BLOCKED ON REPRODUCIBLE SOURCE DEPLOYMENT`
8. Observe production `/api/free-pack/v1` returning v1.1 canonical delivery. — `PENDING`
9. Replace manual Vercel bootstrap deployment process with Git-linked or otherwise reproducible full-source deployment. — `PENDING`
10. Design and govern Developer Pack v1.1 product-quality release. — `IN PROGRESS / CORE SYSTEM IMPLEMENTED`
11. Execute Developer Pack v1.1 static quality guard on an assigned GitHub runner. — `PENDING / CI RUNNER UNASSIGNED`
12. Score the Commercial Value Gate against the actual v1.1 assets and close any gaps. — `NEXT`
13. Add/migrate only remaining customer assets that create distinct customer capability. — `NEXT AFTER GATE SCORING`
14. Keep checkout disabled until paid v1.1 and launch smoke gates are verified. — `ENFORCED`

## Closure conditions

### Public artifact incident

This incident is closed only when the public Prompt Quarry endpoint serves Free Starter Pack v1.1 with the canonical fingerprint above and the deployment source is reconciled with the governed web tree.

### Paid product quality hold

The paid hold is lifted only after Developer Pack v1.1:

- completes intended customer asset migration/redesign;
- passes the Commercial Value Gate;
- produces a new deterministic candidate fingerprint;
- receives explicit distribution approval for that candidate;
- verifies its real delivery path;
- preserves the F4–F7 claim boundary.

`not observed == unknown`
