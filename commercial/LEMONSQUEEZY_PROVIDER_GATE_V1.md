# Lemon Squeezy Provider Gate v1

Status: `IMPLEMENTED CONTRACT / PROVIDER EVIDENCE PENDING`

Purpose: define the only allowed path from the deterministic Developer Pack v1.1.0 RC1 artifact to public commerce without allowing test traffic, delivery canaries, or provider configuration to masquerade as revenue.

## Frozen release identity

```text
product_id          pq-developer-pack
version             1.1.0
archive_name        prompt-quarry-developer-pack-v1.1.0.zip
archive_size        86763
archive_sha256      546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
source_fingerprint  dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa
source_commit       f0accde4aa12ecf4eae530249cb56175e5a28b66
```

Any mutation of a frozen customer source blob requires a new release candidate and new archive identity. Provider evidence for another archive does not satisfy this gate.

## Evidence levels

### G0 — PACKAGING_READY

Already established by deterministic dual build evidence.

Required truth:

```text
13 exact source blobs
inventory exact
builder exact
build #1 exit 0
build #2 exit 0
byte-identical archives
archive size/hash frozen
controlled provider-test approval
```

This is product packaging evidence only. It is not provider evidence, customer delivery evidence, or revenue evidence.

### G1 — PROVIDER_CUSTODY_PASS

Lemon Squeezy must contain the expected product, variant, and exactly one published file for the approved archive.

Verify with:

```bash
python tools/verify_lemonsqueezy_provider_file.py --mode test
```

When an API download URL is available, additionally verify provider-held bytes:

```bash
python tools/verify_lemonsqueezy_provider_file.py --mode test --verify-bytes
```

The verifier checks provider object identity, test/live mode, file name, version, size, publication status, and optionally exact SHA-256 bytes.

`PROVIDER_CUSTODY_PASS` does not prove a customer downloaded the artifact after checkout.

### G2 — PROVIDER_INTEGRATION_PASS

Run Lemon Squeezy in Test Mode while public sale remains disabled.

Required application state:

```text
DEVELOPER_PACK_COMMERCE_MODE=test
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE
LEMONSQUEEZY_PROVIDER_TEST_TOKEN=<secret>
```

The controlled checkout request must include the private header:

```text
x-pq-provider-test-token
```

The checkout route writes exact release identity into Lemon Squeezy checkout custom data with:

```text
pq_gate=provider_test
pq_product_id=pq-developer-pack
pq_product_version=1.1.0
pq_archive_sha256=546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
pq_archive_size=86763
```

A provider-signed `order_created` webhook is accepted only when all of these are true:

```text
signature valid
header event == order_created
payload event == order_created
data type == orders
order status == paid
store id exact
product id exact
variant id exact
test_mode == true
release custom data exact
pq_gate == provider_test
```

Accepted evidence event:

```text
provider_test_order_accepted
```

It must never emit `purchase_completed`.

Lemon Squeezy disables file downloads for Test Mode purchases. Therefore G2 intentionally does not claim customer delivery. The test gate proves checkout + webhook integration and release binding only.

### G3 — LIVE_DELIVERY_CANARY_PASS

Because Test Mode cannot prove a customer file download, one controlled live canary is required before public sale.

Required application state:

```text
DEVELOPER_PACK_COMMERCE_MODE=live
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=NOT_FOR_SALE
LEMONSQUEEZY_LIVE_CANARY_TOKEN=<secret>
```

The controlled checkout request must include:

```text
x-pq-live-canary-token
```

The checkout custom data must contain:

```text
pq_gate=live_canary
```

A valid live provider webhook may then emit only:

```text
live_delivery_canary_order_accepted
```

It must not emit `purchase_completed` while public sale remains disabled.

After that controlled order, download the customer-delivered artifact through the actual customer delivery path and verify:

```text
size    86763
sha256  546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009
```

The canary is operational evidence, not public revenue evidence.

### G4 — PUBLIC_COMMERCE_READY

Only after G1, G2, and G3 are durable PASS may the release owner explicitly promote public sale.

Required application state:

```text
DEVELOPER_PACK_COMMERCE_MODE=live
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS=LIVE
```

In this state the public paid CTA may route to checkout and checkout custom data uses:

```text
pq_gate=live
```

Only a valid non-test provider order bound to `pq_gate=live` can emit:

```text
purchase_completed
```

A provider-test order or live canary order can never satisfy `PQ-$1`.

## State machine

```text
PACKAGING_READY
      |
      v
PROVIDER_CUSTODY_PASS
      |
      v
PROVIDER_INTEGRATION_PASS
      |
      v
LIVE_DELIVERY_CANARY_PASS
      |
      v
PUBLIC_COMMERCE_READY
      |
      v
PQ-LAUNCH-0
      |
      v
real public non-test purchase + exact delivery
      |
      v
PQ-$1
```

No state may be skipped by inference.

## Fail-closed configuration matrix

| Commerce mode | Public sale | Required private token | Signed gate | Accepted evidence event |
|---|---|---|---|---|
| `off` | any | n/a | none | none |
| `test` | `NOT_FOR_SALE` | provider-test token | `provider_test` | `provider_test_order_accepted` |
| `test` | `LIVE` | n/a | invalid configuration | none |
| `live` | `NOT_FOR_SALE` | live-canary token | `live_canary` | `live_delivery_canary_order_accepted` |
| `live` | `LIVE` | none | `live` | `purchase_completed` |

Unknown commerce modes parse to `off`.

## Configuration surface

```text
NEXT_PUBLIC_FREE_PACK_URL
NEXT_PUBLIC_DEVELOPER_PACK_SALE_STATUS
NEXT_PUBLIC_ANALYTICS_MODE
DEVELOPER_PACK_COMMERCE_MODE
LEMONSQUEEZY_DEVELOPER_PACK_TEST_CHECKOUT_URL
LEMONSQUEEZY_DEVELOPER_PACK_LIVE_CHECKOUT_URL
LEMONSQUEEZY_PROVIDER_TEST_TOKEN
LEMONSQUEEZY_LIVE_CANARY_TOKEN
LEMONSQUEEZY_WEBHOOK_SECRET
LEMONSQUEEZY_STORE_ID
LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID
LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID
```

Provider API verification additionally uses:

```text
LEMONSQUEEZY_API_KEY
```

Secrets must remain server-side and must never be exposed as `NEXT_PUBLIC_*` values.

## Provider-specific evidence boundary

Official Lemon Squeezy behavior used by this protocol:

- Test Mode supports checkout and webhook/API integration testing.
- File downloads are disabled for Test Mode purchases.
- Webhook requests include `X-Signature`; checkout custom data is returned in webhook `meta.custom_data`.
- File objects expose variant identity, file name, extension, download URL, size, version, status, and `test_mode`.
- Test and live environments are separate; live operation requires a live store and live credentials.

References:

- https://docs.lemonsqueezy.com/help/getting-started/test-mode
- https://docs.lemonsqueezy.com/help/webhooks/webhook-requests
- https://docs.lemonsqueezy.com/api/files/the-file-object
- https://docs.lemonsqueezy.com/guides/developer-guide/testing-going-live

## Invariants

```text
TEST != REVENUE
CANARY != PUBLIC REVENUE
PROVIDER FILE API DOWNLOAD != CUSTOMER DELIVERY
CHECKOUT REDIRECT != PURCHASE
VALID WEBHOOK != EXACT CUSTOMER DELIVERY
PACKAGING_READY != PROVIDER_READY
not observed == unknown
```

Do not reopen MK2, landing redesign, or mutate the frozen RC1 while this gate is active.
