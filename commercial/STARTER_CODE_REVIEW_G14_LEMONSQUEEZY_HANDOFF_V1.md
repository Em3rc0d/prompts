# Starter Code Review — Lemon Squeezy G14 handoff

Status: `TEST-MODE PROVIDER HANDOFF / PUBLIC SALE OFF`

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

## Human dashboard action

Lemon Squeezy currently requires product/file configuration through its dashboard for this release path. In **Test mode**:

1. Create a product named exactly `Prompt Machine Starter — Code Review Edition`.
2. Configure a non-subscription one-time variant at USD 9.00.
3. Attach the exact RC2 archive to that variant.
4. Set the file version to `1.0.0-rc2` and publish the file.
5. Do not activate public/live sale as part of this handoff.

No provider ID needs to be copied manually. `tools/pm_g14_lemonsqueezy_probe.py` discovers the store, product, variant and file through the API.

## One-command custody check

After the dashboard action, run from any checkout of this repository:

```bash
git fetch --quiet origin feat/workflow-kits-product-model-20260902 && git show origin/feat/workflow-kits-product-model-20260902:tools/pm_g14_lemonsqueezy_probe.py | python3 - --verify-bytes --out "$HOME/.local/share/prompt-machine/g14/lemonsqueezy-test-custody.json"
```

If `LEMONSQUEEZY_API_KEY` is not already exported, the probe asks for it using a hidden terminal prompt. The key is never echoed or persisted by the probe.

Expected success boundary:

```text
state             PASS
stage             PROVIDER_CUSTODY
custody_evidence  true
observed_bytes    19161
observed_sha256   1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88
provider effects  0
```

A metadata-only pass is not custody evidence. Custody requires retrieving the provider-held bytes and matching exact size + SHA-256.

## After custody

Custody PASS does not enable public sale. The remaining G14 sequence is:

```text
provider custody PASS
        ↓
test checkout / order
        ↓
signed webhook observation
        ↓
delivery-canary boundary
        ↓
G14 decision
        ↓
public-sale decision (separate)
```

Test-mode file downloads to purchasers can be limited by Lemon Squeezy's test behavior, so delivery evidence must be classified carefully and must not be promoted from a test order alone.

Master rule:

`MARKETING CLAIM <= OBSERVED EVIDENCE`
