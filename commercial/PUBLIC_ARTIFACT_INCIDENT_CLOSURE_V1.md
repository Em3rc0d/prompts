# Prompt Quarry — Public Artifact Incident Closure v1

Status: `CLOSED`

Closed at: `2026-08-29T03:51:46Z`

## Incident

The original Prompt Quarry Vercel bootstrap deployment served a Free Developer Starter Pack whose prompt bodies were abbreviated relative to the governed repository source.

This was a distribution-integrity failure:

```text
GOVERNED SOURCE
  !=
BOOTSTRAP DELIVERY PAYLOAD
  ->
PUBLIC ARTIFACT DIVERGENCE
```

The affected production deployment was replaced before paid checkout was enabled.

## Closure deployment

```text
deployment_id   dpl_4dsGJa3mosi48EPevw3qHzKw1Bg7
target          production
state           READY
primary_alias   prompt-quarry.vercel.app
```

The public release surface is governed in:

`release/public-web-v1.1/`

The release snapshot exposes a versioned immutable artifact endpoint:

`/api/free-pack/v1.1.0`

The legacy endpoint:

`/api/free-pack/v1`

now resolves to the v1.1.0 artifact so existing bookmarks and older CTAs do not continue serving the historical bootstrap payload.

## Production observation

The production page was directly observed at:

`/free/developer-starter-pack`

Observed customer-visible state:

```text
Free Pack visible version     v1.1
Artifact visible version      v1.1.0
Download href                 /api/free-pack/v1.1.0
HTTP status                   200
```

The production ZIP body was directly observed at `/api/free-pack/v1.1.0`.

Observed delivery identity:

```text
product_id        pq-developer-starter
version           1.1.0
customer_files    7
content_type      application/zip
content_length    23498
archive_sha256    55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
```

Observed response headers included:

```text
Content-Disposition: attachment; filename="prompt-quarry-developer-starter-v1.1.0.zip"
ETag: "sha256-55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32"
X-Prompt-Quarry-Version: 1.1.0
X-Prompt-Quarry-SHA256: 55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
```

The observed ZIP body contains the governed full-length customer assets, including:

- `LICENSE.md`
- `OFFER.md`
- `QUICKSTART.md`
- `README.md`
- `prompts/code-review.md`
- `prompts/bug-diagnosis.md`
- `prompts/technical-decision.md`

The three prompts were inspected in the public response and are the field-ready v1.1 workflow contracts, not the previous abbreviated one-line versions.

## Canonical receipt

`.ci/free-developer-starter-v1/production-delivery-v1.1.json`

Receipt status:

`PASS`

## Closure decision

```text
PUBLIC_FREE_V1_1_DELIVERY          PASS
PRODUCTION_ALIAS_RECONCILED        YES
VERSIONED_ARTIFACT_ENDPOINT        YES
LEGACY_ENDPOINT_RECONCILED         YES
PUBLIC_ARTIFACT_DIVERGENCE         CLOSED
```

## Evidence boundary

This closure establishes production distribution integrity only.

It does **not** establish:

```text
F4 TESTED       NO
F5 IMPROVED     NO
F6 CERTIFIED    NO
F7 PORTABLE     NO
```

`not observed == unknown`
