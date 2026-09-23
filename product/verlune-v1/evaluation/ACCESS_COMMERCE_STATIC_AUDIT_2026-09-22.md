# Verlune v1 — Access / Commerce Static Audit

Status: `ACCESS_LAYER_IMPLEMENTED_CANDIDATE / BUILD_AND_PROVIDER_E2E_OPEN`

Original audit date: 2026-09-22  
Implementation update: 2026-09-23

## Result

The original audit correctly identified that the new Verlune Premium access layer did not exist. That implementation blocker has now changed state: the candidate access product is present in the repository, but it has **not** yet earned E2E qualification.

Implemented customer path:

```text
/unlock
→ server-side Lemon license validation
→ exact entitlement identity checks
→ browser instance activation/reuse
→ signed HttpOnly browser session
→ protected /app Premium library
→ protected exact asset delivery
→ logout / deactivation / periodic revalidation
```

The public landing and public live sale remain unchanged/frozen.

## Implemented in current repository

Present:
- `/unlock` customer route;
- server-side Lemon Squeezy License API validation/activation/deactivation client;
- exact store + product + variant + checkout-email checks;
- frozen activation-limit policy candidate: 3;
- signed Premium authorization cookie with no raw license key;
- signed non-authorizing browser-device reference for safe activation reuse;
- 7-day authorization-session maximum;
- entitlement revalidation threshold: 24 hours;
- fail-closed stale-session revalidation;
- protected `/app` Premium library;
- protected `/app/asset/:id` exact customer asset surface;
- protected `/app/access` session/device controls;
- server-only build materialization for Premium assets;
- Git-blob identity verification before protected asset delivery;
- build-time public/static leakage audit;
- candidate customer path includes all 17 Premium launch-core surfaces.

## Important implementation boundary

This repository state does **not** prove:
- TypeScript compilation;
- production build success;
- Vercel deployment success;
- Lemon provider configuration;
- valid license-key activation;
- revocation behavior in a real provider session;
- absence of Premium bytes from an actually built deployment;
- entitlement E2E;
- checkout/purchase E2E;
- live sale readiness.

Those observations still need to be executed.

## Provider capability check

The implementation follows the current Lemon Squeezy License API semantics:
- activate a license key and retain the returned instance ID;
- validate either the license or a specific instance;
- deactivate a specific instance;
- verify store/product/variant/customer identity;
- use the authenticated Lemon Squeezy API to retrieve a license key by numeric license-key ID for server-side periodic validation.

Official references:
- https://docs.lemonsqueezy.com/api/license-api
- https://docs.lemonsqueezy.com/api/license-api/activate-license-key
- https://docs.lemonsqueezy.com/api/license-api/validate-license-key
- https://docs.lemonsqueezy.com/api/license-api/deactivate-license-key
- https://docs.lemonsqueezy.com/api/license-keys/retrieve-license-key
- https://docs.lemonsqueezy.com/guides/tutorials/license-keys

## Frozen candidate policy

- entitlement credential: Lemon Squeezy license key generated for the new Premium variant;
- unlock inputs: license key + checkout email;
- validation/activation: server-side only;
- identity checks: exact store + product + variant + customer email;
- activation policy: 3 active browser instances;
- authorization credential: signed Secure/HttpOnly/SameSite=Lax cookie;
- authorization cookie contains no raw license key;
- authorization max age: 7 days;
- entitlement revalidation: at unlock and at least every 24 hours;
- disabled/expired/invalid entitlement: fail closed on revalidation;
- same-browser activation reuse: signed non-authorizing device reference;
- logout: clears authorization only;
- deactivate: releases provider instance then clears authorization + device reference;
- provider outage during required revalidation: fail closed while preserving retryable local state;
- Premium assets: protected server delivery, never intentionally bundled into public/static client assets;
- no username/password in v1.

## Provider identity still open

The **new Verlune Premium SKU identity is not frozen yet**.

Do not reuse historical provider IDs merely because previous Code Review/test-provider integration succeeded. The actual Premium product and variant must be configured with license keys enabled and activation limit 3, then their exact IDs frozen before E2E.

## Required next

1. Create/configure the actual Verlune Premium Lemon Squeezy product/variant with license keys enabled and activation limit 3.
2. Freeze exact store/product/variant IDs.
3. Configure server-only staging values and strong independent session/fingerprint secrets.
4. Run `npm run typecheck`.
5. Run `npm run build`, including the Premium build leakage audit.
6. Deploy the candidate to staging.
7. Execute `ACCESS_PRODUCT_TEST_PLAN_2026-09-23.json`.
8. Only after access-product PASS, execute Human Review H1-H11 on the real customer surface.
9. Run Lemon test-mode commerce E2E.
10. Run one controlled live-canary E2E before public sale.

## Gate

`ACCESS_LAYER_IMPLEMENTED_CANDIDATE = true`

`ACCESS_PRODUCT_E2E_PASS = false`

`ENTITLEMENT_E2E_PASS = false`

`READY_TO_SELL = false`
