# Verlune v1 — Premium Access Product Candidate

Status: `IMPLEMENTED_IN_REPOSITORY / BUILD_AND_PROVIDER_E2E_OPEN`

Date: 2026-09-23

## Customer path

```text
purchase
→ receive Lemon Squeezy license key
→ /unlock
→ validate key + checkout email + exact product identity server-side
→ activate or reuse this browser's provider instance
→ signed private browser session
→ /app
→ find Premium asset
→ copy full asset
→ run in user's AI
→ verify / reuse
```

The public landing is intentionally unchanged. This is the candidate access product required before H11 can be tested honestly.

## Implemented surfaces

- `/unlock` — customer unlock form;
- `/app` — protected Premium library;
- `/app/asset/:id` — protected exact asset delivery;
- `/app/access` — browser/session controls;
- `POST /api/verlune/unlock` — entitlement validation + activation;
- `GET /api/verlune/session/revalidate` — periodic entitlement check;
- `POST /api/verlune/logout` — local authorization logout;
- `POST /api/verlune/deactivate` — provider instance deactivation.

## Premium delivery boundary

The launch-core Premium bodies are copied during build into `web/.verlune-private/premium/`.

They are not imported into client components. The protected asset route reads them server-side and recomputes Git blob identity before serving them.

A post-build audit is configured to:
- require all 17 launch-core Premium surfaces in private materialization;
- require the protected access routes;
- scan `public/` and `.next/static/` for protected asset markers;
- fail if those markers appear in public/static client artifacts.

This audit has been implemented but **has not yet been executed successfully in an observed checkout/build environment**.

## Entitlement design

Required provider identity:
- exact Premium store ID;
- exact Premium product ID;
- exact Premium variant ID;
- activation limit: 3;
- checkout email.

The historical Verlune Code Review provider identity must not be silently reused as the new Premium SKU identity.

Unlock validates entitlement before activating a new browser instance.

A provider instance ID is retained through a signed **non-authorizing device reference** so a browser does not consume a new activation every time its seven-day authorization session expires.

The device reference cannot unlock Premium by itself.

## Browser authorization

Authorization session:
- signed;
- HttpOnly;
- Secure in production;
- SameSite=Lax;
- no raw license key;
- maximum age: 7 days;
- provider revalidation required at least every 24 hours.

Server-side periodic validation retrieves the raw key from Lemon Squeezy by numeric license-key ID using the private API key, verifies its keyed fingerprint, then validates the exact provider instance.

If the provider cannot be reached when revalidation is required, Premium fails closed. The local session is retained only so the user can retry without destroying recoverable state.

## Logout vs deactivate

`Log out`
- removes authorization from the current browser;
- keeps a signed non-authorizing device reference;
- same browser can later reuse the provider activation after valid license/email verification.

`Deactivate this browser`
- calls Lemon Squeezy deactivation;
- releases the provider activation;
- clears authorization + device reference after provider success.

## Current blockers

The access implementation is **not E2E-qualified yet**.

Still required:
1. create/freeze the actual new Verlune Premium Lemon Squeezy product + variant with license keys enabled and activation limit 3;
2. freeze its exact store/product/variant IDs;
3. configure server-only staging environment values and strong independent secrets;
4. run typecheck + production build + leakage audit;
5. deploy candidate access surface to staging;
6. execute the frozen access test plan;
7. run Human Review H1-H11 against this customer surface;
8. only later run commerce test E2E and controlled live canary.

## Gate

`ACCESS_LAYER_IMPLEMENTED_CANDIDATE = true`

`ACCESS_PRODUCT_E2E_PASS = false`

`ENTITLEMENT_E2E_PASS = false`

`READY_TO_SELL = false`
