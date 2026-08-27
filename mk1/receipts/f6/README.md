# MK1 F6 cross-runtime evidence

This directory stores **supplemental real F5 benchmark receipts** used only for F6 cross-runtime certification.

The primary F5 receipt that created each `CANDIDATE` remains in its `mk1/candidates/f5/<bundle>/benchmark_receipt.json` bundle and is automatically included by the F6 materializer.

Supplemental files should use the `.receipt.json` suffix and preserve the complete F5 receipt without manual rewriting.

Suggested layout:

```text
mk1/receipts/f6/
  pq_mk1_content_clear_rewrite/
    runtime-family-b.receipt.json
    runtime-family-c.receipt.json
```

Rules:

- no synthetic receipts;
- no duplicate receipt/execution ids;
- no reused blind randomization reference;
- no duplicate runtime family;
- exact same prompt, artifact version, baseline, fixture-set and parent F4 lineage;
- every receipt must independently be `IMPROVEMENT_PASS` with 100% blocking pass, zero regressions, zero baseline wins and blinded human review.

Partial evidence is allowed and remains `PENDING_RUNTIME_EVIDENCE`. It never produces `CERTIFIED` by itself.
