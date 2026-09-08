# Prompt Machine — Starter Public Copy Evidence Audit v1

Status: `CHECKLIST_ACTIVE / CURRENT PUBLIC SALE OFF / REAUDIT_REQUIRED_AFTER_RUNTIME_CORRECTION`

Date: `2026-09-04`

## Purpose

Public copy must never outrun the exact evidence available for the Starter Collection.

Master rule:

> **MARKETING CLAIM <= OBSERVED EVIDENCE**

This audit is a release gate. It is not marketing review for tone alone.

## Current evidence ceiling

As of the runtime protocol-contamination correction:

```text
Starter scope                         FROZEN
workflow contracts                    2 / 2 STATIC PASS
executable prompt surfaces            2 / 2 STATIC PASS
required customer payload             9 / 9 STATIC PASS
deterministic archive                 PASS PACKAGING ONLY
Starter runtime observations          1
clean independent runtime observations 0
Starter runtime passes                0
Starter runtime failures              0
Starter runtime inconclusive          1
runtime effective classification      INCONCLUSIVE_PROTOCOL_CONTAMINATION
Starter skill behavioral observations 0
real customer task outcomes           0
real purchases                        0
provider custody                      NOT ESTABLISHED
live delivery                         NOT ESTABLISHED
public checkout                       OFF
READY_TO_SELL                         NO
```

The raw output, original `FAIL / REWORK` human-review artifact, and original failure record remain preserved append-only. They do **not** support an effective workflow-failure claim because the active runtime conversation had prior exposure to evaluation expectations. The governed effective result is `INCONCLUSIVE / EXPAND_EVIDENCE`.

Therefore public copy may describe design, scope, mechanics, static governance, packaging evidence, and the bounded protocol-contaminated observation precisely. It may not describe the Starter as runtime-proven, runtime-failed, customer-proven, certified, portable, delivered, commercially validated, or ready for sale.

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
- the current Starter runtime ledger contains one observation, zero effective PASS, zero effective FAIL, and one effective INCONCLUSIVE;
- that observation is protocol-contaminated and therefore cannot support a behavioral PASS or FAIL claim;
- no clean independent Starter runtime observation exists yet;
- the same frozen Code Review candidate may be retested only on a clean independent surface after fresh explicit authorization;
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
Starter failed runtime validation
Starter has a confirmed workflow failure
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

Also fail if public copy still claims that Starter runtime observations are zero or that none of the prepared canaries has been executed.

Equivalent wording counts even if the exact phrase is absent.

## Allowed scoped claims today

Examples of supportable wording:

- `Starter scope is frozen.`
- `Two governed workflow contracts are statically frozen.`
- `Two executable prompt surfaces pass static contract-parity checks.`
- `The customer payload contains 9 required assets.`
- `A deterministic 50,918-byte Starter archive has been reproduced byte-for-byte.`
- `Four Starter-specific behavioral canaries are prepared and disarmed.`
- `One runtime observation is preserved; its effective result is INCONCLUSIVE_PROTOCOL_CONTAMINATION.`
- `Current effective runtime counts are 0 PASS, 0 FAIL, 1 INCONCLUSIVE.`
- `No clean independent Starter runtime observation exists yet.`
- `Public checkout is off.`

If a number is used, it must point to an inspectable receipt or governed source.

## Trust History wording

Public Trust History must distinguish:

```text
STATIC ISSUE
HISTORICAL REVIEW ARTIFACT
RUNTIME FAIL
RUNTIME PASS
INCONCLUSIVE
PROTOCOL CONTAMINATION
UNKNOWN
LIMITATION
SUCCESSOR
REGRESSION
REAL-TASK OUTCOME
```

Do not relabel a static semantic defect as a runtime model failure.

Do not relabel a protocol-contaminated observation as a workflow PASS or FAIL. Historical classification artifacts may be disclosed only with their superseding correction and current effective classification nearby.

Do not write `no failures` as a reliability claim when clean runtime evidence is absent. `0 effective failures` is a ledger count, not proof of reliability.

When bounded clean observations later exist, prefer:

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
3. why the first observation is inconclusive;
4. what remains unobserved;
5. what `$9` means today;
6. that workflow results require verification/human judgment.

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
- effective runtime counts including INCONCLUSIVE;
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
