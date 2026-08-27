# MK1 F7 portability evidence

This directory stores supplemental real F5 `IMPROVEMENT_PASS` receipts from provider/model families beyond the F6 target runtime.

F7 starts only after an exact artifact is already `CERTIFIED` by F6.

The F6 bundle contributes its bound same-runtime F5 evidence automatically. Supplemental F7 receipts are added until the full evidence inventory covers at least three distinct providers and three distinct runtime families.

Rules:

- no synthetic evidence;
- exact same prompt, artifact version, baseline, fixture set and parent F4 lineage;
- every receipt independently passes the complete F5 superiority gate;
- blinded human review is mandatory;
- no duplicate receipt/execution/randomization/runtime-evidence refs;
- provider and family diversity is normalized before counting.

Partial evidence remains `PENDING_PORTABILITY_EVIDENCE` and does not affect the artifact's existing `CERTIFIED` state.
