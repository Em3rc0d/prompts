# MK1 F6 target-runtime certification evidence

This directory stores **supplemental real F5 benchmark receipts** used for F6 certification on the same declared target runtime.

The primary F5 receipt that created each `CANDIDATE` remains in `mk1/candidates/f5/<bundle>/benchmark_receipt.json` and is automatically included by the F6 materializer.

Supplemental files should use the `.receipt.json` suffix and preserve the complete F5 receipt without manual rewriting.

Suggested layout:

```text
mk1/receipts/f6/
  pq_mk1_content_clear_rewrite/
    repetition-02.receipt.json
    repetition-03.receipt.json
```

Rules:

- no synthetic receipts;
- exact same provider + model + family as the primary F5 receipt;
- no duplicate receipt/execution ids;
- no reused blind randomization reference;
- no reused runtime identity-evidence reference;
- exact same prompt, artifact version, baseline, fixture-set and parent F4 lineage;
- every receipt independently `IMPROVEMENT_PASS` with 100% blocking pass, zero regressions, zero baseline wins and blinded human review.

At least three independent F5 receipts are required in total (primary plus supplemental evidence).

Partial evidence remains `PENDING_INDEPENDENT_RUNTIME_REPETITIONS`. It never produces `CERTIFIED` by itself.

Cross-provider receipts belong to `mk1/receipts/f7/` and are used only for the optional `PORTABLE` state.
