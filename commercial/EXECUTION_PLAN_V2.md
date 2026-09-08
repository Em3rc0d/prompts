# Prompt Machine — First Revenue Execution Plan v2

Status: `CURRENT / PRE-REVENUE / PUBLIC CHECKOUT OFF`

Date: `2026-09-03`

Supersedes for current execution decisions: `commercial/EXECUTION_PLAN_V1.md`.

`EXECUTION_PLAN_V1.md` remains historical evidence of the earlier Prompt Quarry / $19-first commercial model. It must not be rewritten to pretend the current product architecture existed at that time.

## 1. Objective

Earn the first trustworthy paid chain without weakening product or evidence discipline:

```text
RELEVANT USER
  ↓
REAL CUSTOMER JOB
  ↓
FREE WORKFLOW USE
  ↓
ACTIVATION
  ↓
VALUE / TRUST SIGNAL
  ↓
STARTER $9
  ↓
PROVIDER-SIGNED PURCHASE
  ↓
VERIFIED DELIVERY
  ↓
PQ-$1
```

`PQ-$1` means the first real non-test paid purchase successfully delivered.

The objective is not merely to make a checkout button work. The objective is to make a bounded useful product earn a real purchase and deliver correctly.

## 2. Current truth

```text
Prompt Machine product identity             DEFINED
Prompt Quarry internal factory              DEFINED
$0 → $9 → $19 ladder                         PRICE HYPOTHESIS FROZEN
Starter commercial scope                    FROZEN
Starter public page                         IMPLEMENTED / NOT FOR SALE
architecture behavioral observations       7
architecture expected-state matches        7 / 7
architecture blocking review failures      0
Starter SKU workflow runtime observations  0
Starter skill behavioral evidence          0
Starter deterministic paid archive         NOT BUILT
Starter provider custody                    NOT OBSERVED
Starter live delivery canary                NOT OBSERVED
real customer task outcomes                 0
real purchases                              0
public Starter checkout                     OFF
READY_TO_SELL                               NO
```

The seven existing observations are useful architecture evidence. They are not silently promoted into Starter Code Review / Bug Diagnosis product evidence.

## 3. Commercial unit

Primary launch SKU:

```text
STARTER COLLECTION
price hypothesis: USD 9 one-time
```

Frozen intended scope:

- Evidence-first Code Review workflow;
- Evidence-first Bug Diagnosis workflow;
- `review-code-with-evidence` skill candidate;
- `diagnose-bugs-with-evidence` skill candidate;
- `START_HERE` / task chooser;
- worked examples;
- verification guidance;
- adaptation cheatsheet;
- explicit evidence / limitations.

The Starter must solve complete jobs. It is not an intentionally crippled teaser for the $19 collection.

## 4. Critical path

```text
A. CURRENT PRODUCT TRUTH
        ↓
B. FINAL STARTER WORKFLOW CONTRACTS
        ↓
C. STARTER-SPECIFIC BEHAVIORAL EVIDENCE
        ↓
D. SKILL EVIDENCE OR REMOVE UNSUPPORTED SKILL CLAIMS
        ↓
E. CUSTOMER SURFACES + EXAMPLES + TRUST CARDS
        ↓
F. DETERMINISTIC STARTER ARTIFACT
        ↓
G. PROVIDER TEST CUSTODY + INTEGRATION
        ↓
H. LIVE DELIVERY CANARY
        ↓
I. PUBLIC COPY EVIDENCE AUDIT
        ↓
J. ENABLE $9 CHECKOUT
        ↓
K. FOUNDER-LED FIRST CUSTOMER EXPERIMENT
        ↓
L. PQ-$1
        ↓
M. ACTIVATION / REPEAT / $9→$19 LEARNING
```

Every gate is fail-closed.

## 5. Gate A — Current product truth

State: `PASS`

Required truths are explicit:

- Prompt Machine is the product;
- Prompt Quarry is internal;
- Starter is the first paid experiment;
- prices are hypotheses;
- public checkout is off;
- seven architecture observations exist;
- those observations are not Starter SKU evidence;
- customer value and revenue remain unobserved.

Canonical references:

- `docs/PRODUCT_OPERATING_MODEL_V1.md`
- `commercial/REVENUE_EXPERIMENT_V1.md`
- `commercial/JOB_DISCOVERY_AND_ACTIVATION_CONTRACT_V1.md`
- `docs/WORKFLOW_TRUST_HISTORY_V1.md`

## 6. Gate B — Final Starter workflow contracts

State: `OPEN`

For Code Review and Bug Diagnosis separately, freeze:

```text
CUSTOMER JOB
REQUIRED INPUTS
MINIMUM INPUT PREFLIGHT
AUTHORIZED CONFIGURATION
UNTRUSTED TASK DATA
NON-GOALS
STOP / BLOCK CONDITIONS
OUTPUT CONTRACT
VERIFICATION GUIDANCE
KNOWN LIMITATIONS
```

The final customer-facing workflow may reuse internal architecture, but the SKU contract must be explicit and inspectable.

Exit condition:

`2 / 2 Starter workflows have governed final customer contracts.`

## 7. Gate C — Starter-specific behavioral evidence

State: `OPEN / ZERO OBSERVATIONS`

Architecture canaries do not satisfy this gate.

Minimum first campaign should remain bounded:

```text
Code Review NORMAL
→ human review
→ Code Review adversarial only if justified
→ human review

Bug Diagnosis NORMAL
→ human review
→ Bug Diagnosis adversarial only if justified
→ human review
```

Do not run these until the current shared-plan reserve policy permits additional inference.

No automatic waves.

Exit condition is not a predetermined pass count. The evidence must be reviewed and either support the current version or cause REWORK / successor / regression.

## 8. Gate D — Skill truth

State: `OPEN`

Current skill candidates must not be sold as validated installable behavior until the claimed surfaces have corresponding evidence.

Required before including a skill as a supported Starter feature:

```text
STRUCTURAL VALIDITY
TRIGGER EVIDENCE
FORWARD / EXECUTION EVIDENCE
PROMPT ↔ SKILL PARITY FOR CLAIMED JOB
KNOWN LIMITATIONS
```

If this evidence is not worth buying before first launch, the honest alternative is to remove the skill claim from the initial paid artifact rather than delay forever or overclaim.

## 9. Gate E — Customer surfaces + Trust

State: `PARTIAL`

The Starter page exists and accurately says `NOT FOR SALE`.

Still required for the final SKU:

- `START_HERE`;
- task chooser;
- final workflow surfaces;
- worked examples;
- verification guidance;
- adaptation guidance;
- workflow-level Trust Cards derived from evidence;
- visible known limitations.

Trust Card publication path:

```text
ledger
→ deterministic card
→ validator
→ human claim review
→ PUBLICATION_ELIGIBLE
```

Campaign-level architecture evidence must not be rendered as certification of one Starter workflow.

## 10. Gate F — Deterministic Starter artifact

State: `NOT BUILT`

The paid Starter artifact needs a deterministic manifest/archive with:

- exact customer-visible file list;
- version;
- content hashes;
- archive hash;
- archive size;
- source commit;
- license;
- evidence state;
- `READY_TO_SELL = false` until downstream gates pass.

No archive identity may be invented before the artifact exists.

## 11. Gate G — Provider test custody + integration

State: `NOT STARTED FOR STARTER`

The existing commerce code is historically centered on the Developer Pack and cannot be treated as Starter provider evidence.

For Starter, implement only after Gate F provides a real artifact identity.

Required:

```text
provider test product/variant
$9 test price contract
SKU identity reconciliation
signed webhook verification
product / variant verification
artifact version/hash binding where supported
verified fulfillment path
```

Provider test orders are test evidence, not revenue.

## 12. Gate H — Live delivery canary

State: `NOT STARTED`

One explicitly authorized live canary must prove the real paid delivery path without opening public sale.

Required evidence:

```text
real live checkout path
provider-signed accepted event
correct Starter SKU/version
correct artifact delivered
artifact integrity verified
no private repository access required
```

A fabricated webhook cannot satisfy this gate.

## 13. Gate I — Public copy evidence audit

State: `OPEN`

Before sale, audit every material customer claim against the then-current evidence.

Required rule:

```text
MARKETING CLAIM <= OBSERVED EVIDENCE
```

Explicitly verify that copy does not convert:

- architecture evidence into SKU evidence;
- expected-state matches into certification;
- synthetic fixtures into customer evidence;
- provider test orders into revenue;
- one successful canary into universal reliability;
- untested skill candidates into supported features.

## 14. Gate J — Enable $9 checkout

State: `BLOCKED`

Public Starter checkout may become `LIVE` only when:

```text
STARTER_PRODUCT_READY              YES
DETERMINISTIC_STARTER_ARCHIVE      PASS
PROVIDER_CUSTODY                   PASS
PROVIDER_INTEGRATION               PASS
LIVE_DELIVERY_CANARY               PASS
PUBLIC_COPY_EVIDENCE_AUDIT         PASS
```

No one document or environment variable may bypass this set.

## 15. Gate K — Founder-led first customer experiment

State: `NOT STARTED`

Initial acquisition should remain small and interpretable.

Working hypothesis only:

```text
30 relevant contacts
→ 15 try Free
→ 8 use a real task
→ 5 report/produce value signal
→ 3 inspect Starter
→ 1 pays $9
```

These are hypotheses, not benchmarks.

Prioritize people who genuinely perform Code Review / Bug Diagnosis work. Do not optimize vanity traffic first.

## 16. Gate L — PQ-$1

State: `NOT OBSERVED`

Requires:

```text
real non-test purchase
+ non-zero provider revenue
+ correct Starter SKU/version
+ verified artifact delivery
```

Record the milestone without unnecessary customer/payment PII.

One purchase means only: `someone paid once`.

## 17. Gate M — Compounding evidence

After PQ-$1, the next goal is not automatically more inventory.

Observe:

```text
real-task activation
usefulness / task outcome
support friction
repeat use
referral
refunds
$9 → $19 upgrade interest / purchase
```

Use these signals to decide whether to improve the same job family, change onboarding, change offer positioning, or expand adjacent jobs.

## 18. Capital rule

Every next unit of engineering/model/provider spend must answer one of:

```text
Q — reduce quality/trust risk
A — acquire a relevant user
V — improve real-task activation/value
M — enable/understand monetization
R — improve repeat/referral/upgrade
```

Current weighting remains:

`Q > V > M > A > R`

## 19. Immediate work while inference is paused

Authorized zero-model-spend work:

1. formalize this Starter release gate;
2. finalize Code Review / Bug Diagnosis customer contracts from already-governed assets;
3. prepare Starter artifact layout without claiming an archive exists;
4. map exact activation events and voluntary task-outcome capture;
5. prepare workflow-level Trust Card inputs;
6. design provider integration around the Starter SKU, but do not provision or enable public sale prematurely.

## 20. Stop conditions

Defer unless evidence changes priority:

- profession packs;
- marketplace;
- subscription;
- account dashboard;
- recommendation engine;
- broad new prompt mining;
- paid acquisition scaling;
- 84-run PCP campaign;
- broad model portability campaign;
- new high-stakes categories.

## 21. Master operating rule

> **Architecture protects the business from lying to itself. Revenue proves whether the protected product is valuable enough that somebody will pay for it. We need both.**

The shortest path to revenue is not to skip gates. It is to make every gate answer a decision that matters to the first customer.