# Prompt Machine Commercial System

Status: `CODE REVIEW EDITION RC2 — G14 TEST WEBHOOK OBSERVED / VERCEL APPLY PENDING / PUBLIC SALE OFF`

Current operational truth is in `STATUS_CURRENT.md`.

The first paid release candidate remains:

```text
Prompt Machine Starter — Code Review Edition
version         1.0.0-rc2
price           $9 one-time — hypothesis
workflow        Evidence-first Code Review v2.2
model scope     Gemini 3.5 Flash
classification MODEL_SPECIFIC
```

Canonical archive:

```text
prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
19,161 bytes
SHA-256 1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
8 members
license + sale terms frozen
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
G12 PASS — RC2
G13 PASS — RC2, 65/65
G14 TEST PRODUCT + WEBHOOK OBSERVED / VERCEL APPLY + TEST ORDER PENDING
```

Observed externally in Lemon Squeezy Test mode:

```text
Test product published       PASS
provider metadata            PASS
Test webhook id 132724       PASS
Test webhook event           order_created
Test-mode byte custody       NOT OBSERVABLE BY PROVIDER DESIGN
```

Remaining G14 evidence:

```text
Vercel Test env import                     NOT OBSERVED
Vercel Test redeploy                       NOT OBSERVED
private provider-test checkout redirect    NOT OBSERVED
provider test checkout/order               NOT OBSERVED
signed order_created accepted              NOT OBSERVED
Live provider byte custody                 NOT OBSERVED
Live delivery canary                       NOT OBSERVED
```

Operator UX invariant:

`one user action <= one command`

Current G14 operators:

- `tools/pm_g14_lemonsqueezy_probe.py` — read-only Test metadata.
- `tools/pm_g14_lemonsqueezy_test_setup.py` — bounded Test webhook setup.
- `tools/pm_g14_vercel_test_apply.py` — imports owner-only Vercel handoff, redeploys staging, verifies private checkout gate and emits only the Lemon Test checkout URL.
- `tools/verify_lemonsqueezy_starter_code_review_file.py` — later controlled Live byte-custody verification.

Commercial boundary:

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
PQ-$1               NOT OBSERVED
```

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
