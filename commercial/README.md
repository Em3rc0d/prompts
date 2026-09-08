# Prompt Machine Commercial System

Status: `CODE REVIEW EDITION RC2 — G14 TEST INTEGRATION PASS / LIVE CUSTODY + DELIVERY PENDING / PUBLIC SALE OFF`

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
G14 TEST INTEGRATION PASS / LIVE CUSTODY + DELIVERY PENDING
```

Observed G14 Test path:

```text
Test product published                    PASS
provider metadata                         PASS
Test webhook                              PASS
Vercel env + redeploy                     PASS
private provider-test checkout            PASS
paid Test order                           PASS
provider-signed order_created             PASS
webhook HTTP                              200
runtime event                             provider_test_order_accepted
release identity                          RC2 / 19,161 / SHA-256 MATCH
```

Test-mode byte custody is unavailable by provider design and is not inferred from this Test order. Live byte custody and delivery remain unobserved.

A historical provider-ID discrepancy is intentionally preserved: an earlier dashboard URL exposed `1347702`, while the provider-signed accepted order carried product `1347720` and variant `2105176`. Reconcile and freeze the actual Live provider IDs before any Live canary.

Operator UX invariant:

`one user action <= one command`

Current G14 operators:

- `tools/pm_g14_lemonsqueezy_probe.py` — read-only Test metadata.
- `tools/pm_g14_lemonsqueezy_test_setup.py` — bounded Test webhook setup.
- `tools/pm_g14_vercel_test_apply.py` — Vercel Test handoff + redeploy + private checkout verification.
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
