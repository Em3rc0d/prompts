# Developer Pack Release Readiness

Before changing release status to `READY`:

- [ ] Manifest lists every distributed artifact.
- [ ] Every included artifact has a SHA-256 fingerprint.
- [ ] Provenance class is explicit.
- [ ] Generator is bundled only with canonical static CI `PASS`.
- [ ] No forbidden bundle class is present.
- [ ] README and Quickstart require no private repository access.
- [ ] Templates contain no unresolved internal placeholders.
- [ ] Example claims preserve evidence boundaries.
- [ ] Clean-room package test passes.
- [ ] Release archive and manifest are fingerprinted.
- [ ] Distribution license is declared.
- [ ] Claims review receipt exists.

`READY` is a packaging/release state, not an MK1 certification state.
