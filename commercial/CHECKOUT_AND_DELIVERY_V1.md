# Prompt Quarry Checkout & Delivery v1

## Decision

Recommended v1 checkout provider: `Lemon Squeezy`.

Reasoning:
- one-time digital-product checkout is native;
- Merchant of Record model reduces indirect-tax operational burden;
- digital file delivery can be handled without building a custom commerce backend;
- future subscription support exists if Prompt Quarry Pro becomes justified;
- v1 can use hosted checkout and keep the Prompt Quarry landing independent.

This is an execution choice for first-sale validation, not an irreversible platform dependency.

## Architecture

```text
PROMPT QUARRY LANDING
      |
      +--> FREE CTA
      |      -> free download / optional email capture
      |
      +--> BUY CTA
             -> hosted checkout
             -> payment success
             -> provider receipt
             -> secured digital download
             -> Developer Pack v1 payload
```

## Free Pack delivery

### v0 mode
Use direct download from a public distribution artifact or simple download endpoint.

### v1 preferred mode
Optional email capture followed by immediate download.

Data minimum:
- email;
- acquisition source/UTM;
- consent state if marketing follow-up is enabled;
- timestamp.

Do not require:
- account creation;
- password;
- profile completion;
- long questionnaire.

Free acquisition must remain low-friction.

## Paid Pack delivery

The customer receives a frozen release payload built from the governed Developer Pack manifest, never a ZIP of the private repository.

### Required contents
Only customer-visible assets declared by the release manifest.

### Forbidden contents
- `.git/`;
- `.github/` workflows;
- `.ci/` internal receipts unless deliberately customer-facing;
- `.approvals/`;
- raw MK0 harvest data;
- internal research queues;
- credentials/secrets;
- tools/source infrastructure not included in the commercial manifest.

### Canonical package identity
At purchase time record internally where practical:
- product: `Prompt Quarry Developer Pack`;
- version: `1.0.0`;
- release manifest source commit;
- archive SHA-256;
- transaction/order identifier.

This gives Prompt Quarry a future way to answer: `What exact version did this customer receive?`

## Checkout product configuration

### Product
`Prompt Quarry Developer Pack v1`

### Type
One-time digital purchase.

### Launch price
`USD $19`

### Product description
`A reusable prompt engineering toolkit for developer and technical AI workflows, with templates, methodology, examples, structured contracts, and quality gates.`

### Checkout bullets
- instant digital access;
- versioned one-time purchase;
- use and adapt for your own authorized work/products;
- resale and redistribution prohibited;
- assets currently statically VALID; no universal performance guarantee.

## License acceptance

The checkout should link visibly to the commercial license.

The delivered archive must contain `LICENSE.md`.

The authoritative permission model remains:

```text
USE        YES
ADAPT      YES
INTEGRATE  YES, without exposing/repackaging the Pack
RESELL     NO
REDISTRIBUTE NO
SUBLICENSE NO
```

## Success page

### H1
`Developer Pack v1 is yours.`

### Instructions
1. Download the Pack.
2. Open `README.md`.
3. Follow `QUICKSTART.md`.
4. Start from the template/example closest to your real task.
5. Preserve uncertainty and evidence boundaries when adapting prompts.

### Secondary action
Optional only after first activation:
`Tell us what workflow you used it for.`

Do not immediately upsell another product before the customer can access what they bought.

## Failure handling

### Payment failed
- keep the entered checkout state where provider supports it;
- show a plain retry path;
- do not imply the customer was charged.

### Payment succeeded but download failed
Customer support priority: restore access, not debug the customer.

Record:
- order id;
- product/version;
- delivery failure;
- resolution.

### Duplicate purchase concern
Provide a human support path until product-account infrastructure is justified.

## Refund policy

Do not invent a custom guarantee in marketing until the actual checkout/refund policy is configured and legally/operationally reviewed.

The landing and checkout must describe only the policy actually offered by the provider/store.

## Provider abstraction

Do not hard-code commercial logic deep into Prompt Quarry.

The landing needs only a conceptual interface:

```text
FREE_DOWNLOAD_URL
PAID_CHECKOUT_URL
```

This allows Lemon Squeezy to be replaced later without rebuilding product semantics.

## Launch gate

Checkout is `READY` only when all are observed:
- live product configured;
- price matches offer document;
- correct payload uploaded;
- license visible;
- test checkout/sandbox flow completed if provider supports it;
- success page routes to correct delivery;
- analytics events fire;
- mobile checkout tested.

A checkout button pointing to a placeholder URL is not CHECKOUT_READY.
