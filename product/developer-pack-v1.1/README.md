# Prompt Quarry — Developer Pack v1.1

Internal product status: `PACKAGING_READY / PROVIDER_TEST_PENDING / NOT FOR SALE`

Target version: `1.1.0`

This directory is the governed authoring and release source for Developer Pack v1.1. It does not replace or mutate the frozen `product/developer-pack-v1/` v1.0 release history.

## Product thesis

The Free Developer Starter Pack v1.1 gives developers three strong finished workflows.

Developer Pack v1.1 gives developers the reusable construction and governance system behind them:

```text
FREE
finished workflows
        ↓
PAID
reusable operating architecture
+ parameterized policy
+ evidence controls
+ decision / escalation semantics
+ machine-readable contracts
+ adaptation method
+ verification contracts
+ team/application integration
+ worked transformations
```

## RC1 customer inventory

Frozen in `CUSTOMER_INVENTORY.release-candidate.json`.

```text
customer-visible assets  13
source payload bytes      83879
source fingerprint        dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
```

The customer ZIP uses `README.customer.md` as `README.md`. Internal `README.md`, `SPEC.md`, inventory files, and `quality/*` are governance assets and are excluded.

## Core systems

- General Operating Contract
- Software Code Review System
- Bug Diagnosis System
- Technical Research / Decision System

The four core systems passed the manual static Commercial Value Gate at `14/14` each (`56/56` total). This is static product evidence only.

## Packaging evidence

Canonical builder:

`tools/build_developer_pack_v1_1_release_candidate.py`

Durable receipts:

- `.ci/developer-pack-v1.1/release-candidate.json`
- `.ci/developer-pack-v1.1/build-evidence.json`
- `.ci/developer-pack-v1.1/packaging-readiness.json`
- `.approvals/developer-pack-v1.1/DISTRIBUTION_APPROVAL.json`

The RC1 source, inventory, and builder were reconstructed from their exact Git blob identities and executed in two isolated clean roots.

Observed result:

```text
build_1 exit              0
build_2 exit              0
byte_identical            YES
receipt_equal             YES
customer_visible_assets   13
normalizations            8 / 8
archive_size              86763 bytes
archive_sha256            546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
source_fingerprint         dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
```

All builder gates passed:

```text
inventory_exact                 PASS
blob_identity                   PASS
source_fingerprint              PASS
normalization_exact             PASS
archive_members_exact           PASS
archive_crc                     PASS
customer_draft_markers_absent   PASS
deterministic_rules             PASS
```

The earlier GitHub Actions run remains classified separately as a pre-execution runner failure: its `build-candidate` job executed zero steps and produced zero artifacts. It is not used as release evidence.

## Current state

```text
builder_source             PASS / EXACT BLOB
inventory_freeze           PASS / EXACT BLOB
customer_payload           PASS / 13 EXACT BLOBS
commercial_value_gate      PASS (MANUAL_STATIC)
archive_execution          PASS
archive_determinism        PASS
archive_sha256             RECORDED
distribution_approval      APPROVED_FOR_CONTROLLED_PROVIDER_TEST
packaging_ready            YES
provider_test              PENDING
public_sale                NO
sale_status                NOT_FOR_SALE
```

`PACKAGING_READY` means the exact distributable artifact is reproducible and approved for the controlled provider test/delivery-validation stage. It does not authorize public sale by itself.

## Evidence boundary

```text
static_maturity   VALID_CANDIDATE
F4_TESTED         NO
F5_IMPROVED       NO
F6_CERTIFIED      NO
F7_PORTABLE       NO
```

`not observed == unknown`

Packaging determinism, CI success, deployment health, provider redirects, or payment UI must never be promoted into behavioral maturity claims.

## Next gate

The release path is now:

```text
PACKAGING_READY
    ↓
configure payment provider
    ↓
controlled test checkout
    ↓
signed provider order/webhook
    ↓
verify exact delivered artifact
    ↓
provider gate PASS
    ↓
public-sale decision / PQ-LAUNCH-0
```

The provider test must bind delivery to exactly:

```text
version   1.1.0
bytes     86763
sha256    546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
```

Checkout remains fail-closed until provider configuration and signed-order evidence are observed.
