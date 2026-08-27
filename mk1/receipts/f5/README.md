# MK1 F5 benchmark receipts

This directory stores only **real paired F5 benchmark receipts**.

A persisted `*.receipt.json` here must be produced from:

- a source artifact already in `TESTED` state;
- the frozen task-equivalent F5 baseline;
- the exact F4 fixture set;
- one identified provider/model/runtime configuration;
- at least 3 repeats per fixture for both engineered and baseline participants;
- complete machine assertions and human checks;
- blinded human A/B preference review;
- immutable prompt, fixture and receipt fingerprints.

Synthetic characterization results do not belong here and cannot support `improved`.

Current evidence boundary: absence of a real receipt means **0 F5 IMPROVED/CANDIDATE artifacts**.
