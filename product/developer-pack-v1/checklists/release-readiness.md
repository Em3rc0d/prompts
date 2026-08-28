# Developer Pack Release Readiness

Before changing release status to `READY`, the automated release-candidate pipeline must prove:

- [x] Manifest lists every distributed artifact.
- [x] Every included artifact is `VALID` and has a SHA-256 fingerprint.
- [x] Provenance class is explicit.
- [x] Generator evidence remains bound to canonical static CI `PASS`.
- [x] No forbidden bundle class is present.
- [x] README and Quickstart require no private repository access.
- [x] Example claims preserve evidence boundaries.
- [x] Deterministic manifest-only clean-room payload export passes.
- [x] Release payload archive is fingerprinted.
- [x] Release manifest canonical projection is fingerprinted.
- [x] Claims review receipt exists and is `PASS`.
- [x] Clean-room release-candidate receipt exists and is `PASS`.
- [x] Candidate is bound to an exact source commit and deterministic source timestamp.

Final human/commercial gate:

- [ ] An explicit `release/DISTRIBUTION_APPROVAL.json` exists, validates against `product/specs/DISTRIBUTION_APPROVAL.schema.json`, binds the current release-candidate source commit, declares the chosen distribution license, and records commercial approval.

The example file `release/DISTRIBUTION_APPROVAL.example.json` is not approval and cannot unlock `READY`.

`READY` is a packaging and commercial release-readiness state. It does not establish `TESTED`/F4, `IMPROVED`/F5, `CERTIFIED`/F6, or `PORTABLE`/F7.
