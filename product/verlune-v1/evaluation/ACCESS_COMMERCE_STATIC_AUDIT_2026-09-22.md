# Verlune v1 — Access / Commerce Static Audit

Status: `BLOCKED_BEFORE_E2E / ACCESS_LAYER_NOT_IMPLEMENTED_FOR_VERLUNE_PREMIUM`

Date: 2026-09-22

Frozen product candidate: `886060c1f991aadd4b458f05fc7c62056942e9ca`

## Result

The existing web application has mature historical commerce plumbing for legacy Developer Pack / Starter Code Review flows, but the new Verlune Premium access architecture described by the v1 product model is not implemented yet.

### Observed current code

Present:
- fail-closed commerce modes (`off | test | live`);
- server-side Lemon Squeezy checkout/webhook infrastructure for historical SKUs;
- signed webhook validation;
- product/store/variant/release identity checks;
- historical Code Review release identity;
- public-sale feature gates.

Absent from the current `web/` tree:
- `/unlock` customer route;
- Verlune Premium entitlement validation layer;
- license activation/validation flow for the new Premium SKU;
- signed secure Premium browser session;
- protected `/app` Premium library;
- revocation/revalidation behavior;
- a customer-visible device/session management policy;
- an E2E path from new Verlune Premium purchase → entitlement → unlock → protected content.

Therefore `ENTITLEMENT_E2E_PASS` cannot be truthfully executed yet.

## Provider capability check

Lemon Squeezy's current License API supports activation, validation and deactivation of license-key instances. The provider documentation also recommends validating product/store identity and, where useful, purchaser email.

Official references:
- https://docs.lemonsqueezy.com/api/license-api
- https://docs.lemonsqueezy.com/guides/tutorials/license-keys

## Access design decisions frozen for implementation candidate

These defaults are conservative and can be changed before public launch if product review finds friction:

- entitlement credential: Lemon Squeezy license key generated for the Premium variant;
- unlock inputs: license key + checkout email;
- activation: server-side only;
- identity checks: exact store + product + variant + customer email;
- browser credential: signed, Secure, HttpOnly, SameSite=Lax session cookie;
- cookie contains no raw license key;
- server stores only a keyed hash/fingerprint of the license key plus provider instance id/session metadata;
- session max age: 7 days;
- entitlement revalidation: at unlock and at least once every 24 hours for active sessions;
- disabled/expired/invalid provider status: fail closed on next revalidation;
- activation limit candidate: 3 concurrent instances/devices;
- logout: clears local session; explicit device deactivation may call provider deactivation when implemented;
- Premium assets: server-protected; never shipped in public/static client bundles;
- no username/password in v1;
- no universal lifetime-access language beyond the purchased-version license terms.

## Required before implementation can be called complete

1. Create/configure the actual Verlune Premium Lemon Squeezy product/variant with license keys enabled.
2. Freeze store/product/variant IDs and activation limit.
3. Implement `/unlock`, server-side activate/validate, signed session, `/app` authorization and logout/deactivation.
4. Add unit/integration tests for invalid key, wrong product, wrong email, expired/disabled key, session tampering and revocation.
5. Run test-mode E2E.
6. Run one controlled live-canary E2E before public sale.
7. Audit that Premium content is absent from unauthenticated responses/static bundles.

## Gate

`ENTITLEMENT_E2E_PASS = false`

This is a real implementation blocker, not a documentation blocker.
