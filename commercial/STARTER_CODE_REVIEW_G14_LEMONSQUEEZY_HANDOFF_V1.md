# Starter Code Review — Lemon Squeezy G14 handoff

Status: `TEST PRODUCT + WEBHOOK OBSERVED / VERCEL APPLY PENDING / PUBLIC SALE OFF`

This handoff is for the exact Prompt Machine Starter — Code Review Edition RC2.

## Frozen provider target

```text
store                    Prompt Quarry
mode                     Test mode
product                  Prompt Machine Starter — Code Review Edition
price                    USD 9.00 one-time
subscription             NO
archive                  prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
archive version          1.0.0-rc2
archive bytes            19,161
archive SHA-256          1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
archive members          8
customer license         frozen inside archive
sale terms               frozen inside archive
public checkout          OFF
```

Do not substitute RC1 or the historical Starter Collection archive.

## Observed provider state

Observed externally on 2026-09-08:

```text
Test product             Published
provider product id      1347702
$9 one-time variant      observed
RC2 filename             match
provider file size       19,161
provider file status     published
provider metadata        PASS
Test webhook id          132724
Test webhook event       order_created
Test webhook target      https://prompt-quarry-stage.vercel.app/api/commerce/lemonsqueezy/starter-code-review-webhook
```

The webhook signing secret is not stored in the repository.

## Test-mode byte boundary

Lemon Squeezy disables file downloads in Test mode. Therefore the observed HTTP 403 from the Test-mode file `download_url` is classified as an expected provider restriction, not a custody failure and not custody evidence.

```text
provider metadata        OBSERVED / PASS
Test webhook object      OBSERVED / PASS
Test-mode byte custody   NOT OBSERVABLE BY PROVIDER DESIGN
```

Exact provider-held byte custody remains a later controlled Live-canary property.

## One-command Vercel Test apply

The Lemon setup operator generated this owner-only handoff on the user's machine:

`~/.local/share/prompt-machine/g14/starter-code-review-test-vercel.env`

`tools/pm_g14_vercel_test_apply.py` consumes that file and, in one action:

1. verifies the handoff remains owner-only and `NOT_FOR_SALE` / `test`;
2. authenticates Vercel CLI if necessary;
3. upserts the eight required `prompt-quarry-stage` Production variables through stdin so secret values never appear in argv;
4. redeploys the staging production alias;
5. checks that the webhook route remains POST-only;
6. calls the private provider-test checkout gate with the local token;
7. emits only the final Lemon Test checkout URL.

It does not enable Lemon Live mode, does not enable public checkout and does not make a purchase.

## Remaining Test integration path

```text
Vercel env import
        ↓
staging redeploy
        ↓
private provider-test checkout redirect
        ↓
one zero-real-money Lemon Test order
        ↓
provider-signed order_created accepted
        ↓
G14 TEST-MODE integration decision
```

Only after Test integration is closed do we consider the separate Live canary for provider-held byte custody and delivery.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
