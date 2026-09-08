# Prompt Machine Commercial System

Customer-facing masterbrand: **Verlune**

Internal architecture:

```text
Verlune        customer-facing brand
Prompt Machine product/release engine
Prompt Quarry  evidence/certification factory
```

Status: `VERLUNE CODE REVIEW 1.0.0 — G12/G13 PASS / HISTORICAL TEST PATH PASS / STORE BRANDING PASS / ACTIVATION IN REVIEW / VERLUNE PRODUCT VALIDATION PENDING`

Current operational truth is in `STATUS_CURRENT.md`.

## First paid product

```text
Verlune Code Review
version         1.0.0
price           $9 one-time — hypothesis
workflow        Evidence-first Code Review v2.2
model scope     Gemini 3.5 Flash
classification MODEL_SPECIFIC
```

Canonical customer archive:

```text
verlune-code-review-v1.0.0.zip
18,859 bytes
SHA-256 4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649
payload fingerprint 46554b5aa36166e6bee7f07b572fa4bece29811270e014cb96381099c87ca430
8 members
Pack QA 77/77 PASS
license + sale terms frozen
```

Certified workflow remains unchanged:

```text
WORKFLOW.md bytes   25,295
WORKFLOW.md SHA-256 6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977
```

The customer surface contains `Verlune` and excludes customer-facing `Prompt Machine`, `Prompt Quarry`, release-candidate wording and transient launch state.

## Gate state

```text
G05 FAIL / REWORK — historical baseline preserved
G06 CLOSED
G07 PASS
G08 PASS — 4/4 frozen final regression cases
G09 MODEL_SPECIFIC / PASS_FOR_DEMONSTRATED_SCOPE
G10 KEEP / RECORDED
G11 PASS_FOR_EXACT_DECLARED_SCOPE
G12 PASS — Verlune 1.0.0
G13 PASS — Verlune 1.0.0, 77/77
G14 historical RC2 Test path PASS / Verlune Test provider validation pending
```

Historical Test integration demonstrated the complete commerce/webhook path, but the accepted Test order carried RC2 packaging and the old customer-facing brand. It remains evidence only and must not be described as provider validation of the Verlune package.

Canonical historical Test identity:

```text
store_id     462419
product_id   1347720
variant_id   2105176
order        4624191
old 1347702  NOT_FOUND / superseded
```

Test IDs must never be reused as Live IDs.

## Current Lemon observation

```text
mode                    Test
store name              Verlune
logo                    OBSERVED
activation application  SUBMITTED
identity verification   IN_REVIEW
provider approval       PENDING
```

Receipt:

`commercial/VERLUNE_G14_LEMON_BRAND_AND_ACTIVATION_SUBMITTED_2026-09-08.json`

This observation does not prove that the Test product or downloadable archive has been migrated to Verlune, and it does not imply Live readiness.

Operator UX invariant:

`one user action <= one command`

Current tooling is bound to the Verlune artifact while retaining stable internal Prompt Machine identifiers where evidence continuity requires them:

- `tools/pm_operator.py`
- `tools/pm_g14_lemonsqueezy_probe.py`
- `tools/pm_g14_lemonsqueezy_test_setup.py`
- `tools/pm_g14_lemonsqueezy_live_preflight.py`
- `tools/verify_lemonsqueezy_starter_code_review_file.py`

## Current external frontier

```text
Verlune Lemon store name + logo          PASS / OBSERVED
Verlune Code Review product rename       PENDING
Verlune 1.0.0 Test file upload           PENDING
read-only Test metadata revalidation      PENDING
store activation application             SUBMITTED / IN REVIEW
provider approval                        PENDING
NEW Live provider IDs/API key             PENDING
Live byte custody                         PENDING
Live buyer delivery                       PENDING
```

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
