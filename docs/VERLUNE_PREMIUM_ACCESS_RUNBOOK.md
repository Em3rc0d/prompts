# Verlune Premium access + payment activation runbook

Status: implementation-ready, public sale fail-closed.

This runbook activates the already implemented path:

```text
Mercado Pago approved payment
        ↓
canonical Verlune entitlement
        ↓
one deterministic VLK1 Access Key per normalized email
        ↓
Resend delivers that same key
        ↓
email + Access Key unlock
        ↓
provider read-back / revalidation
        ↓
Premium session
```

## Invariants

- Price authority is server-side: `S/ 17.00` (`VERLUNE_PREMIUM_PRICE_PEN_MINOR=1700`).
- One normalized email + `verlune-premium-v1` maps to one entitlement ID.
- One entitlement maps to one deterministic `VLK1` Access Key.
- Recovery re-sends the same key; it does not mint another.
- A second checkout for an email with a still-valid Premium payment is rejected with `premium_already_owned` before creating a new Mercado Pago payment.
- Refunds, reversals, amount/account/environment mismatches fail closed.
- `VERLUNE_ACCESS_KEY_SECRET_V1` is a versioned root secret. Do not rotate or delete V1 after customers exist. Introduce a V2 scheme instead.
- Public sale remains `NOT_FOR_SALE` until TEST and LIVE canaries pass.

## 1. Upstash / Redis REST

Create a durable Redis database and copy its HTTPS REST URL and standard token.

Set:

```text
VERLUNE_ENTITLEMENT_KV_REST_URL=https://...
VERLUNE_ENTITLEMENT_KV_REST_TOKEN=...
```

The implementation sends Redis commands as JSON arrays over HTTPS and authenticates with `Authorization: Bearer <token>`.

Do not use the read-only token because entitlement creation and recovery throttling require writes.

## 2. Verlune Access Key root secret

Generate a high-entropy secret outside the repository. Example:

```bash
openssl rand -base64 48
```

Set:

```text
VERLUNE_ACCESS_KEY_SECRET_V1=<generated secret>
```

Back this value up in the production secret manager. Losing/changing it changes every V1 Access Key.

Also keep:

```text
VERLUNE_SESSION_SECRET=<32+ character secret>
VERLUNE_LICENSE_FINGERPRINT_SECRET=<32+ character secret>
VERLUNE_SESSION_MAX_AGE_SECONDS=604800
VERLUNE_SESSION_REVALIDATE_SECONDS=900
```

## 3. Resend

Verify the sending domain in Resend and create an API key with send permission.

Set:

```text
RESEND_API_KEY=re_...
VERLUNE_ACCESS_FROM_EMAIL=Verlune <access@your-domain>
NEXT_PUBLIC_SITE_URL=https://your-production-domain
```

Initial purchase delivery uses a stable idempotency key per entitlement/version so checkout + webhook retries do not intentionally create duplicate grant emails.

Recovery is rate-limited per entitlement in Redis and sends the same canonical Access Key.

## 4. Mercado Pago TEST

Set:

```text
VERLUNE_PREMIUM_COMMERCE_MODE=test
VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=NOT_FOR_SALE
VERLUNE_PREMIUM_PROVIDER_TEST_TOKEN=<private browser gate>

MP_ENVIRONMENT=test
MP_ALLOW_LIVE=false
MP_ACCESS_TOKEN=<test token>
MP_PUBLIC_KEY=<test public key>
MP_COLLECTOR_ID=<test collector/account id>
MP_WEBHOOK_SECRET=<test webhook signature secret>
MP_NOTIFICATION_URL=https://<test-host>/api/commerce/mercado-pago/webhook
```

TEST acceptance must prove both card and Yape:

```text
payment created
→ Mercado Pago approved
→ provider read-back passes
→ webhook signature passes
→ entitlement exists
→ Resend delivers VLK1 key
→ email + VLK1 key unlocks
→ same email recovery returns same key
→ second purchase attempt is rejected before a new charge
→ refund/reversal blocks entitlement
```

Do not promote to LIVE if any line is unobserved.

## 5. LIVE activation

Replace only provider/environment values with LIVE credentials and verify the production Resend domain + Redis database first.

Keep sale closed while running the controlled canary:

```text
VERLUNE_PREMIUM_COMMERCE_MODE=live
VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=NOT_FOR_SALE
MP_ENVIRONMENT=live
MP_ALLOW_LIVE=true
```

Run one controlled real `S/ 17.00` purchase and verify:

```text
Mercado Pago approved
→ real signed webhook
→ entitlement active
→ one Access Key email received
→ key unlocks Premium in clean browser
→ logout
→ same key unlocks again
→ recovery email contains exactly the same key
```

Only after that evidence passes:

```text
VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=LIVE
```

## Required production variables

```text
NEXT_PUBLIC_SITE_URL

VERLUNE_PREMIUM_PRICE_PEN_MINOR
VERLUNE_PREMIUM_COMMERCE_MODE
VERLUNE_PREMIUM_PUBLIC_SALE_STATUS

MP_ENVIRONMENT
MP_ALLOW_LIVE
MP_ACCESS_TOKEN
MP_PUBLIC_KEY
MP_COLLECTOR_ID
MP_WEBHOOK_SECRET
MP_NOTIFICATION_URL

VERLUNE_ACCESS_KEY_SECRET_V1
VERLUNE_ENTITLEMENT_KV_REST_URL
VERLUNE_ENTITLEMENT_KV_REST_TOKEN

RESEND_API_KEY
VERLUNE_ACCESS_FROM_EMAIL

VERLUNE_SESSION_SECRET
VERLUNE_LICENSE_FINGERPRINT_SECRET
VERLUNE_SESSION_MAX_AGE_SECONDS
VERLUNE_SESSION_REVALIDATE_SECONDS
```

## Release boundary

Code/build readiness does not claim provider E2E evidence. The sale switch is intentionally separate from configuration so credentials alone cannot silently open public sales.
