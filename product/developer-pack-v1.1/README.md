# Prompt Quarry — Developer Pack v1.1

Internal product status: `RELEASE_CANDIDATE RC1 / NOT FOR SALE`

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

Frozen in:

`CUSTOMER_INVENTORY.release-candidate.json`

Customer-visible payload: `13 assets`.

Source fingerprint:

`sha256:dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa`

The customer ZIP uses `README.customer.md` as `README.md`. Internal `README.md`, `SPEC.md`, inventory files, and `quality/*` are governance assets and are excluded.

## Core systems

- General Operating Contract
- Software Code Review System
- Bug Diagnosis System
- Technical Research / Decision System

The four core systems passed the manual static Commercial Value Gate at `14/14` each (`56/56` total). This is static product evidence only.

## Packaging

Canonical builder:

`tools/build_developer_pack_v1_1_release_candidate.py`

The builder must:

1. verify every frozen Git blob identity;
2. verify the source fingerprint;
3. apply only declared exact customer-state normalizations;
4. fail if any declared normalization is missing or duplicated;
5. archive exactly the frozen customer inventory;
6. fail if customer `DRAFT` markers leak into the ZIP;
7. verify ZIP members and CRC;
8. emit `.ci/developer-pack-v1.1/release-candidate.json` with archive SHA-256.

The CI workflow runs the builder twice and requires byte-identical archives.

## Current blocker

GitHub Actions is currently creating the `build-candidate` job but not assigning/executing steps (`steps=null`, `logs_url=null`). Therefore:

```text
builder_source             READY
inventory_freeze           PASS
commercial_value_gate      PASS (MANUAL_STATIC)
archive_execution          NOT_OBSERVED
archive_sha256             UNKNOWN
distribution_approval      BLOCKED
READY                      NO
sale_status                NOT_FOR_SALE
```

A CI conclusion of `failure` with zero executed steps is not treated as product or builder failure.

## Evidence boundary

```text
static_maturity   VALID_CANDIDATE
F4_TESTED         NO
F5_IMPROVED       NO
F6_CERTIFIED      NO
F7_PORTABLE       NO
```

`not observed == unknown`

No `READY`, `TESTED`, `IMPROVED`, `CERTIFIED`, `PORTABLE`, or behavioral-superiority claim is permitted until the corresponding gate is observed.

## Exit to READY

RC1 can become READY only after:

1. deterministic builder executes successfully;
2. two independent builds produce the same ZIP bytes;
3. archive SHA-256 and size are recorded;
4. distribution approval binds to that exact source fingerprint + archive SHA;
5. the delivered paid artifact is verified against the approved fingerprint.

Checkout remains off until those gates pass.
