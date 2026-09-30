# Verlune Premium — Mercado Pago commerce v1

Date: 2026-09-29

## Product decision

Verlune Premium v1 is priced at **US$5 one time**. For the Peru Mercado Pago account the launch amount is frozen server-side at **S/ 17.00** via `VERLUNE_PREMIUM_PRICE_PEN_MINOR=1700`.

Mercado Pago is the active Premium payment provider. Lemon Squeezy is not in the Verlune Premium purchase path.

## Checkout

```text
/premium
  -> /checkout
  -> Mercado Pago JS tokenization
  -> POST /api/commerce/verlune-premium/payment
  -> POST /v1/payments
  -> canonical GET /v1/payments/:id
  -> signed Verlune Premium session when approved
  -> /app
```

Supported v1 UI paths:

- card through Mercado Pago Card Payment Brick;
- Yape through Mercado Pago JS token generation.

PAN, CVV, Yape phone and Yape OTP are not accepted as backend fields. The backend receives provider tokens only.

## Server authority

The browser is not authoritative for price, currency, product identity, merchant account or payment state.

Before access is granted, the canonical Mercado Pago payment must match:

- product metadata `verlune-premium-v1`;
- description `Verlune Premium`;
- server price `S/ 17.00`;
- currency `PEN`;
- configured collector;
- configured TEST/LIVE environment;
- expected checkout email when recovery is used;
- zero refund amount;
- status `approved`.

Every create call sends `X-Idempotency-Key`.

## Entitlement

There is no serverless SQLite ledger in this implementation. The reference `m-pago` SQLite store is intentionally not copied into Vercel because ephemeral/serverless files are not durable.

For v1, Mercado Pago is the entitlement authority:

- successful checkout creates an HttpOnly signed Premium session;
- recovery uses checkout email + Mercado Pago payment ID;
- periodic revalidation reads the provider payment again;
- refunded/reversed/non-approved/mismatched payments fail closed.

This keeps the first paid release operational without introducing a new database solely for payment state.

## Webhook

`POST /api/commerce/mercado-pago/webhook` verifies Mercado Pago HMAC signature using the same manifest contract as the reviewed `em3rc0dTh/m-pago` integration, then performs provider read-back. Webhook state is not trusted as the access authority.

## Release boundary

Source implementation is not provider certification.

Required before calling the path production-proven:

1. Mercado Pago TEST credentials configured.
2. Card TEST approved and read-back verified.
3. Yape TEST approved and read-back verified.
4. HTTPS webhook signature observed.
5. LIVE credentials configured with `MP_ALLOW_LIVE=true`.
6. One controlled LIVE purchase succeeds end-to-end.
7. Only then set `VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=LIVE`.

`not observed == unknown`
