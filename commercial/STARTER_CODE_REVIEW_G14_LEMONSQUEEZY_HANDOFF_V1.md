# Starter Code Review — Lemon Squeezy G14 handoff

Status: `TEST PRODUCT PUBLISHED / PROVIDER METADATA PASS / TEST WEBHOOK + ORDER PENDING / PUBLIC SALE OFF`

This handoff is for the exact Prompt Machine Starter — Code Review Edition RC2.

## Frozen provider target

```text
store                    Prompt Quarry
mode                     Test mode
product                  Prompt Machine Starter — Code Review Edition
product id               1347702
price                    USD 9.00 one-time
subscription             NO
product status           Published
archive                  prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
archive bytes            19,161
archive SHA-256          1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
archive members          8
customer license         frozen inside archive
sale terms               frozen inside archive
public checkout          OFF
```

Do not substitute RC1 or the historical Starter Collection archive.

## Evidence already observed

The Lemon Squeezy Test-mode product is published at $9 one-time. The provider API observation matched:

```text
RC2 filename             PASS
provider-reported size   19,161 bytes / PASS
file status              published / PASS
test_mode                true / PASS
```

Lemon returned no file version. `File.version` is optional provider metadata and is not cryptographic identity.

A direct file download returned HTTP 403. This is expected for this phase because Lemon Squeezy documents file downloads as disabled for Test-mode purchases. Therefore:

```text
provider metadata        OBSERVED / PASS
Test-mode byte custody   NOT OBSERVABLE BY PROVIDER DESIGN
Live byte custody        NOT YET OBSERVED
```

Do not convert the Test-mode 403 into a custody FAIL or a custody PASS.

## Stable staging receiver

The deployed POST-only webhook endpoint is:

`https://prompt-quarry-stage.vercel.app/api/commerce/lemonsqueezy/starter-code-review-webhook`

A GET to this path returns HTTP 405, confirming the route exists while remaining method-restricted.

## One-command Test integration setup

The next bounded operator is:

```bash
python3 <(curl -fsSL 'https://raw.githubusercontent.com/Em3rc0d/prompts/feat/workflow-kits-product-model-20260902/tools/pm_g14_lemonsqueezy_test_setup.py') --apply-webhook
```

Behavior:

1. asks for the Test-mode Lemon API key using a hidden prompt if it is not already loaded;
2. discovers Store → Product → Variant → File and the reusable provider checkout URL;
3. validates product is Published, Test mode, one-time $9 and bound to the exact RC2 provider metadata;
4. generates a dedicated webhook signing secret and a separate provider-test checkout gate token;
5. creates exactly one Test-mode Lemon webhook for `order_created` at the stable staging URL;
6. writes the Vercel handoff to a chmod-0600 local file;
7. never prints or persists the Lemon API key;
8. records no real-money purchase and enables no public sale.

Expected state after a successful provider setup:

```text
state              ACTION_REQUIRED
stage              VERCEL_ENV_IMPORT
webhook_created    true
real_money_effect  false
```

The generated handoff file contains only the Test-mode environment required by `prompt-quarry-stage`, including exact provider IDs, the Test checkout URL and the two generated secrets. Secrets are excluded from receipts.

## After Vercel import

Once the generated environment is imported to `prompt-quarry-stage` and that project is redeployed, the remaining zero-real-money Test sequence is:

```text
Test webhook configured
        ↓
private provider-test checkout route
        ↓
Lemon Test checkout
        ↓
Test card / no real charge
        ↓
Test order_created
        ↓
signed webhook accepted by Prompt Machine
        ↓
G14 TEST-MODE integration PASS
```

Test-mode integration PASS is still not Live delivery evidence and is not revenue evidence.

## Live-only evidence later

Byte-level custody/delivery is intentionally deferred until a controlled Live canary because Lemon disables Test-mode file downloads. The Live verifier remains:

`tools/verify_lemonsqueezy_starter_code_review_file.py`

No Live canary, real purchase, public checkout, or store activation is authorized by this handoff.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
