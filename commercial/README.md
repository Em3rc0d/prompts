# Prompt Machine Commercial System

Status: `CODE REVIEW EDITION 1.0.0 FINAL ARTIFACT — G12/G13 PASS / HISTORICAL TEST INTEGRATION PASS / FINAL PROVIDER VALIDATION PENDING`

Current operational truth is in `STATUS_CURRENT.md`.

The first paid release is being prepared around:

```text
Prompt Machine Starter — Code Review Edition
version         1.0.0
price           $9 one-time — hypothesis
workflow        Evidence-first Code Review v2.2
model scope     Gemini 3.5 Flash
classification MODEL_SPECIFIC
```

Canonical final archive:

```text
prompt-machine-starter-code-review-edition-v1.0.0.zip
18,955 bytes
SHA-256 9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3
8 members
Pack QA 67/67 PASS
license + sale terms frozen
```

The certified workflow remains unchanged:

```text
WORKFLOW.md bytes   25,295
WORKFLOW.md SHA-256 6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
```

Current gate state:

```text
G05 FAIL / REWORK — historical baseline preserved
G06 CLOSED
G07 PASS
G08 PASS — 4/4 frozen final regression cases
G09 MODEL_SPECIFIC / PASS_FOR_DEMONSTRATED_SCOPE
G10 KEEP / RECORDED
G11 PASS_FOR_EXACT_DECLARED_SCOPE
G12 PASS — final 1.0.0
G13 PASS — final 1.0.0, 67/67
G14 historical RC2 Test integration PASS / final 1.0.0 provider validation pending
```

Historical Test integration demonstrated the full provider path through a paid Test order and provider-signed `order_created`, but that order carried RC2 packaging. RC2 is evidence only and must not be sold or copied to Live.

Canonical historical Test identity was reconciled through the Lemon API:

```text
store_id     462419
product_id   1347720
variant_id   2105176
order        4624191
old 1347702  NOT_FOUND / superseded
```

Test IDs must never be reused as Live IDs.

Operator UX invariant:

`one user action <= one command`

Current final-artifact tooling:

- `tools/pm_operator.py` — deterministic final release check in isolated worktree.
- `tools/pm_g14_lemonsqueezy_probe.py` — final 1.0.0 Test metadata discovery.
- `tools/pm_g14_lemonsqueezy_test_setup.py` — bounded Test integration setup for final 1.0.0.
- `tools/pm_g14_lemonsqueezy_live_preflight.py` — read-only Live identity/metadata/byte preflight.
- `tools/verify_lemonsqueezy_starter_code_review_file.py` — hardened exact final byte-custody verification.

Current pre-Live frontier:

```text
customer-visible Lemon branding           PENDING
final 1.0.0 Test file upload/revalidation  PENDING
legitimate store activation                PENDING
NEW Live provider IDs/API key              PENDING
Live byte custody                          PENDING
Live buyer delivery                        PENDING
```

The Test checkout displayed `By Prompt Quarry`, while Prompt Machine is the intended customer-facing product/platform. That display-brand decision must be reconciled before buyer-facing Live checkout. Provider legal/business identity must remain truthful and must not be bypassed.

Commercial boundary:

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
real revenue        0
PQ-$1               NOT OBSERVED
```

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
