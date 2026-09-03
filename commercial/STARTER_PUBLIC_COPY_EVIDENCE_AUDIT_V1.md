# Prompt Machine — Starter Public Copy Evidence Audit v1

Status: `CHECKLIST_DEFINED / CURRENT PUBLIC SALE OFF / AUDIT NOT YET RECEIPTED`

Date: `2026-09-03`

## Purpose

Public copy must never outrun the exact evidence available for the Starter Collection.

Master rule:

> **MARKETING CLAIM <= OBSERVED EVIDENCE**

This audit is a release gate. It is not marketing review for tone alone.

## Current evidence ceiling

As of this checklist definition:

```text
Starter scope                         FROZEN
workflow contracts                    2 / 2 STATIC PASS
executable prompt surfaces            2 / 2 STATIC PASS
required customer payload             9 / 9 STATIC PASS
deterministic archive                 PASS PACKAGING ONLY
Starter runtime observations          0
Starter skill behavioral observations 0
real customer task outcomes           0
real purchases                        0
provider custody                      NOT ESTABLISHED
live delivery                         NOT ESTABLISHED
public checkout                       OFF
READY_TO_SELL                         NO
```

Therefore public copy may describe design, scope, mechanics, static governance and packaging evidence precisely. It may not describe the Starter as runtime-proven, customer-proven, certified, portable, delivered, commercially validated, or ready for sale.

## Surfaces in scope

At minimum audit:

- `/`;
- `/collections`;
- `/starter-collection`;
- `/developer-pack` where it compares against Starter;
- `/free/developer-starter-pack` where it funnels toward Starter;
- `/license` when it describes product/evidence state;
- shared navigation/footer CTA copy;
- metadata/title/description for Starter-related routes.

## Required copy truths

The public Starter surface must preserve all materially applicable truths:

- `$9` is a **price hypothesis** until public sale begins;
- Starter is **not for sale** while checkout is blocked;
- scope freeze is not runtime evidence;
- architecture campaign evidence is not Starter SKU runtime evidence;
- deterministic packaging is not provider custody or customer delivery;
- skill candidates are not supported skills until skill evidence passes;
- synthetic worked examples are not customer evidence;
- no certification or portability claim exists today;
- no real customer outcome or revenue evidence exists today;
- actual software/release/production decisions remain human decisions.

## Prohibited or gated claims today

Fail the audit if current copy presents any of these as established facts:

```text
Starter is tested
Starter is proven
Starter is certified
Starter is production-ready
Starter is ready to sell
Starter is portable across models/providers
Starter prevents prompt injection
Starter is secure / safe without scope qualifier
customers trust/use/love Starter
customers save X time with Starter
Starter has a validated conversion rate
Starter has generated revenue
skills are supported/installable and validated
checkout is live
```

Equivalent wording counts even if the exact phrase is absent.

## Allowed scoped claims today

Examples of supportable wording:

- `Starter scope is frozen.`
- `Two governed workflow contracts are statically frozen.`
- `Two executable prompt surfaces pass static contract-parity checks.`
- `The customer payload contains 9 required assets.`
- `A deterministic 50,918-byte Starter archive has been reproduced byte-for-byte.`
- `Four Starter-specific behavioral canaries are prepared and disarmed.`
- `Runtime evidence for the Starter workflows has not yet been observed.`
- `Public checkout is off.`

If a number is used, it must point to an inspectable receipt or governed source.

## Trust History wording

Public Trust History must distinguish:

```text
STATIC ISSUE
RUNTIME FAIL
RUNTIME PASS
INCONCLUSIVE
UNKNOWN
LIMITATION
SUCCESSOR
REGRESSION
REAL-TASK OUTCOME
```

Do not relabel a static semantic defect as a runtime model failure.

Do not write `no failures` when runtime observations are zero.

When bounded observations later exist, prefer:

> No material failures were observed in the listed bounded cases.

and display the untested scope nearby.

## Checkout wording gate

While `public_checkout = BLOCKED`:

- no `Buy now` CTA may point to a live Starter checkout;
- no copy may say `available now` or equivalent;
- any price presentation must remain clearly hypothetical/planned;
- the primary action should lead to free value, evidence details, or comparison rather than fake purchase intent.

## Skill wording gate

Until skill trigger, forward execution and prompt-skill parity evidence exist:

Allowed:

- `skill candidate`;
- `planned skill surface`;
- `conditional on evidence`.

Not allowed:

- `included supported skill`;
- `validated skill`;
- `portable skill`;
- `works across supported hosts`.

## Evidence disclosure placement

Limitations must be visible on the relevant product surface, not hidden only in legal/footer copy.

At minimum the Starter page should make the following understandable without opening a legal document:

1. current sale state;
2. current evidence state;
3. what remains unobserved;
4. what `$9` means today;
5. that workflow results require verification/human judgment.

## Audit result states

Use exactly one:

- `PASS_CURRENT_EVIDENCE_BOUNDARY`
- `PASS_WITH_NON_BLOCKING_COPY_FIXES`
- `FAIL_MISLEADING_MATERIAL_CLAIM`
- `FAIL_SALE_STATE_MISMATCH`
- `FAIL_EVIDENCE_SCOPE_AMBIGUOUS`

A PASS is tied to the exact audited commit. Material evidence changes or public-copy changes make the receipt stale.

## Receipt requirements

A completed audit receipt must record:

- audited commit SHA;
- routes/files reviewed;
- current Starter Release Gate version;
- evidence receipts relied on;
- findings;
- fixes applied, if any;
- final audit state;
- reviewer;
- whether checkout was enabled during the audit;
- explicit statement that the audit does not create runtime/customer/revenue evidence.

## Publication rule

Passing this copy audit is necessary but not sufficient to enable public checkout.

```text
PUBLIC_COPY_EVIDENCE_AUDIT PASS
        !=
STARTER_PRODUCT_READY
        !=
PUBLIC CHECKOUT LIVE
        !=
PQ-$1
```

The audit exists to ensure that, when Prompt Machine eventually asks a customer to pay, the story being sold is the story the evidence can actually support.
