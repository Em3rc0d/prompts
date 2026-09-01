# MK0 Harvester Control Plane

Status: `DRAFT_CONTRACT_V1`

The Harvester is the acquisition and triage control plane for Prompt Quarry MK0. It discovers public prompt/skill/instruction/capability artifacts, records what was actually observed, normalizes machine-readable metadata, deduplicates candidates, characterizes techniques, computes confidence and quality signals, and routes uncertain cases to governed human review.

It does **not** promote an item directly to `GOLDEN`, infer unavailable source bodies, bypass access controls, or treat a confidence score as truth.

## Pipeline

```text
DISCOVERED
  -> OBSERVED
  -> NORMALIZED
  -> DEDUPED
  -> CHARACTERIZED
  -> SCORED
      -> GOLDEN_CANDIDATE        confidence >= 0.95 and no critical uncertainty
      -> HUMAN_REVIEW_REQUIRED   0.90 <= confidence < 0.95 or review-triggering uncertainty
      -> HOLD                    confidence < 0.90 with retained potential value
      -> REJECTED                policy/provenance/integrity failure or low-value duplicate
```

`GOLDEN_CANDIDATE != GOLDEN`.

Promotion to `GOLDEN` is a separate governed operation recorded under `mk0/promotions/`.

## Threshold contract

- `confidence >= 0.95`: machine may route to `GOLDEN_CANDIDATE` only when all mandatory gates pass.
- `0.90 <= confidence < 0.95`: route to `HUMAN_REVIEW_REQUIRED`.
- `confidence < 0.90`: no automatic candidate promotion; route to `HOLD` or `REJECTED` according to explicit rules.
- Critical uncertainty overrides confidence.
- Provenance/legal/access facts are not probabilistically upgraded. Unknown remains `UNKNOWN`.

## Machine authority boundary

The Harvester may:

- discover public references;
- fetch publicly accessible content when allowed;
- record metadata and hashes;
- normalize and fingerprint;
- classify source/artifact type;
- extract prompt-engineering techniques;
- estimate classification confidence and quality;
- route records into the candidate queue.

The Harvester may not:

- bypass authentication, paywalls, CAPTCHAs, robots/access restrictions, or other authorization boundaries;
- reconstruct unavailable third-party wording and label it observed;
- infer a license as reusable when license status is unknown;
- promote directly to `GOLDEN`;
- claim F4/F5/F6/F7 evidence from source quality or human preference.

## Contracts

- `SOURCE_RECORD.schema.json` — canonical observed/normalized source record.
- `CANDIDATE_RECORD.schema.json` — scored queue record and routing decision.
- `HUMAN_REVIEW.schema.json` — immutable human adjudication receipt.
- `POLICY.json` — machine routing policy and thresholds.
- `HUMAN_REVIEW_CONTRACT.md` — reviewer authority, decision semantics, and escalation rules.

## Storage mapping

```text
mk0/raw/              immutable/raw observations where policy permits
mk0/normalized/       canonical normalized records
mk0/catalog/          discoverable indexes
mk0/analysis/         derived characterization and aggregate findings
mk0/harvester/        schemas, policy, validators, queue tooling
mk0/promotions/       governed promotion receipts
mk0/golden-dataset/   promoted Golden artifacts only
```

## Core invariant

```text
OBSERVED FACT != INFERENCE != DERIVED KNOWLEDGE != GOLDEN PROMOTION
```

The system must preserve these boundaries mechanically.