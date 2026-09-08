# Prompt Machine Commercial System

Status: `CODE REVIEW EDITION RC2 — G14 TEST PRODUCT PUBLISHED / METADATA PASS / TEST ORDER PENDING`

Prompt Machine is the customer-facing platform. Prompt Quarry is the internal factory that discovers, shapes, tests, improves, and certifies reusable AI workflows.

We do not sell raw prompt count. The commercial product is a governed workflow whose claims are bounded by observed evidence.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

## Read current truth first

1. `STATUS_CURRENT.md`
2. `STARTER_CODE_REVIEW_G14_TEST_PRODUCT_PUBLISHED_2026-09-08.json`
3. `STARTER_CODE_REVIEW_RELEASE_STATE_G14_PROVIDER_HANDOFF_2026-09-08.json`
4. `STARTER_CODE_REVIEW_EDITION_RELEASE_PROFILE_RC2_V1.json`
5. `STARTER_CODE_REVIEW_G12_PACK_REBUILD_RC2_PASS_2026-09-08.json`
6. `STARTER_CODE_REVIEW_G13_PACK_QA_RC2_PASS_2026-09-08.json`
7. `../certification/receipts/starter-code-review-v2.2-g11-certification.json`

Older snapshots and RC1 receipts are historical evidence and do not override current state.

## First paid release candidate

```text
Prompt Machine Starter — Code Review Edition
version         1.0.0-rc2
price           $9 one-time — hypothesis
workflow        Evidence-first Code Review v2.2
model scope     Gemini 3.5 Flash
classification MODEL_SPECIFIC
```

Bug Diagnosis remains excluded until it earns its own behavioral certification.

RC archive:

```text
prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip
19,161 bytes
SHA-256 1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
8 members
license + sale terms frozen
```

## Current quality pipeline

```text
G05  FAIL / REWORK — historical baseline preserved
G06  CLOSED
G07  PASS
G08  PASS — 4/4 frozen final regression cases
G09  MODEL_SPECIFIC / PASS_FOR_DEMONSTRATED_SCOPE
G10  KEEP / RECORDED
G11  PASS_FOR_EXACT_DECLARED_SCOPE
G12  PASS — RC2
G13  PASS — RC2, 65/65
G14  TEST PRODUCT PUBLISHED / METADATA PASS / TEST ORDER PENDING
```

G11 certification remains deliberately narrow: `PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001`.

## Observed G14 state

Lemon Squeezy Test mode now contains the exact $9 one-time Code Review Edition product in `Published` state. Provider metadata observed for RC2 matches the frozen filename, size `19,161`, published status and Test mode.

```text
Test product published       PASS
provider metadata            PASS
Test-mode byte custody       NOT OBSERVABLE BY PROVIDER DESIGN
test checkout/order          NOT YET OBSERVED
signed order_created         NOT YET OBSERVED
Live byte custody            NOT YET OBSERVED
```

Lemon Squeezy documents file downloads as disabled in Test mode, so an HTTP 403 from a Test-mode file download is not treated as a corrupted artifact or custody failure. Byte custody is reserved for a controlled later Live canary.

## Operator model

Operational UX rule:

`one user action <= one command`

- `tools/pm_operator.py` performs offline release checks in an isolated worktree.
- `tools/pm_g14_lemonsqueezy_probe.py` performs read-only Test-mode discovery and metadata validation. It no longer pretends byte custody can be observed in Test mode.
- `tools/pm_g14_lemonsqueezy_test_setup.py` discovers Store/Product/Variant/File and checkout identity, generates separate signing/gate secrets, and can create exactly one Test-mode `order_created` webhook when explicitly invoked with `--apply-webhook`.

The Lemon API key is neither printed nor persisted. Generated secrets are excluded from receipts and written only to a chmod-0600 local Vercel handoff file.

## G14 integration boundary

The staging webhook endpoint is deployed on the stable project domain:

`https://prompt-quarry-stage.vercel.app/api/commerce/lemonsqueezy/starter-code-review-webhook`

The route is present and POST-only. Commerce defaults remain fail closed:

```text
commerce mode      off
public sale        NOT_FOR_SALE
public checkout    OFF
```

Remaining evidence:

```text
Test webhook configured             NOT YET OBSERVED
provider test checkout/order        NOT YET OBSERVED
signed order_created accepted       NOT YET OBSERVED
Live provider byte custody          NOT YET OBSERVED
Live delivery canary                NOT YET OBSERVED
real purchase                       0
real revenue                        0
```

## Commercial hypothesis

```text
FREE       $0
STARTER    $9 one-time
FULL       $19 one-time
SUBSCRIPTION deferred
```

Primary milestone: `PQ-$1 = first real non-test paid purchase successfully delivered`.

Current commercial truth:

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
real purchases      0
PQ-$1               NOT OBSERVED
```

## Evidence boundaries

```text
provider metadata      != byte custody
Test mode               != Live delivery
provisioning            != delivery
provider_test           != revenue
runtime PASS            != universal certification
certification           != product readiness
packaging               != customer value
```

## Commercial principles

1. Sell outcomes and workflow leverage, not prompt count.
2. Preserve failures and corrections; do not rewrite history to look green.
3. Keep evaluation contracts out of model runtime inputs.
4. Require bounded authorization for provider/model side effects.
5. Human review remains required for behavioral certification decisions.
6. Never promote packaging or Test-mode metadata into custody, delivery, value, or revenue evidence.
7. Keep public claims behind current evidence.
8. Prefer one governed operator action over manual ceremonies.
9. Do not create subscriptions before one-time demand exists.
10. `not observed == unknown`.
