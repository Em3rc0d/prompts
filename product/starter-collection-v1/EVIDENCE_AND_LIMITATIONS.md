# Starter Collection — Evidence & Limitations

Status: `CUSTOMER SURFACE CANDIDATE / NOT FOR SALE`

Last updated: `2026-09-03`

Prompt Machine separates what is **built**, what is **observed**, and what remains **unknown**. This file states the current evidence boundary for the Starter Collection without converting internal progress into unsupported product claims.

## Current Starter truth

```text
Frozen Starter workflow contracts          2 / 2
Frozen executable prompt surfaces          2 / 2
Starter SKU runtime observations           0
Starter skill behavioral observations      0
Real customer task outcomes                0
Repeat-use observations                    0
Real purchases                              0
Verified Starter deliveries                0
Cross-provider portability                 NOT ESTABLISHED
Certification                              NOT ESTABLISHED
READY_TO_SELL                              NO
Public checkout                            OFF
```

## Architecture evidence already observed

Prompt Machine has a separate governed architecture campaign with:

```text
7 bounded behavioral observations
7 / 7 observed states matching predeclared expected states
0 blocking review failures
3 embedded-override cases observed
```

Those observations are useful evidence about the architecture/binding approach and instruction/data behavior in the tested cases.

They are **not** silently counted as runtime evidence for the final Starter Code Review or Bug Diagnosis workflows.

```text
architecture evidence != Starter SKU evidence
```

## What has been statically closed for Starter

### Evidence-first Code Review

- customer job defined;
- required-input preflight defined;
- evidence labels defined;
- finding and severity semantics defined;
- advisory ship-state semantics defined;
- instruction/data boundary present;
- output contract defined;
- verification contract defined;
- executable customer prompt surface statically aligned to the frozen contract.

### Evidence-first Bug Diagnosis

- customer job defined;
- required-input preflight defined;
- observation/hypothesis semantics defined;
- root-cause confirmation threshold defined;
- production-action approval boundary defined;
- instruction/data boundary present;
- diagnostic states defined;
- output contract defined;
- verification contract defined;
- executable customer prompt surface statically aligned to the frozen contract.

Static contract/surface checks tell us that the intended semantics are represented consistently. They do **not** tell us how a model will behave at runtime.

## Runtime evidence still required

The next evidence class for the Starter workflows is bounded Starter-specific runtime observation.

The intended progression is:

```text
frozen contract
→ frozen executable surface
→ exact bounded invocation
→ runtime observation
→ human review
→ RETAIN / REWORK / RETIRE / EXPAND_EVIDENCE
→ successor/regression when required
```

No automatic wave is authorized.

## Worked examples

The included worked examples are explicitly labeled:

`SYNTHETIC EXAMPLE — NOT A RUNTIME OBSERVATION — NOT CUSTOMER EVIDENCE`

They exist to teach input/output shape and verification discipline. They must never be presented as proof that a model or customer produced the illustrated result.

## Skill candidates

The planned Starter scope includes:

- `review-code-with-evidence`;
- `diagnose-bugs-with-evidence`.

At the current evidence state these remain **skill candidates**.

Before they can be represented as supported Starter features, the claimed skill surfaces need evidence for:

```text
STRUCTURAL VALIDITY
TRIGGER BEHAVIOR
FORWARD / EXECUTION BEHAVIOR
PROMPT ↔ SKILL PARITY
KNOWN LIMITATIONS
```

If those gates are not completed before first launch, the honest launch option is to omit the unsupported skill feature rather than overclaim it.

## Known limitations

Current material limitations include:

1. The final Starter Code Review workflow has no Starter-specific runtime observation yet.
2. The final Starter Bug Diagnosis workflow has no Starter-specific runtime observation yet.
3. Cross-model/provider portability has not been established.
4. No public workflow-level Trust Card is publication-eligible yet.
5. No real customer task outcome has been observed.
6. No repeat-use or referral evidence has been observed.
7. The `$9` price is a hypothesis, not validated willingness-to-pay evidence.
8. Starter provider custody and paid delivery have not been verified.
9. Public Starter checkout is intentionally disabled.
10. Skill candidates are not yet behaviorally supported features.

## What we will not claim from the current evidence

The current state does not support claims such as:

- certified;
- guaranteed;
- universally reliable;
- immune to prompt injection;
- works on every model/provider;
- proven to improve every code review or diagnosis;
- validated by customers at scale;
- ready to sell;
- revenue proven.

## Trust History

Prompt Machine preserves PASS, FAIL, INCONCLUSIVE, rework, successor, regression, limitation, customer-outcome, purchase, and delivery evidence as separate events.

A future public workflow Trust Card may tell a story such as:

```text
WHAT WE TESTED
WHAT PASSED
WHAT FAILED
WHAT CHANGED
WHAT WE RETESTED
WHAT REMAINS UNKNOWN
```

but only after those events actually exist and the card passes deterministic + human claim review.

The objective is not to hide failures. A material failure that leads to a documented correction and successful regression can become stronger trust evidence than unexplained green checks.

## Customer verification boundary

Even after future runtime evidence exists, Prompt Machine workflows remain advisory unless explicitly stated otherwise.

For material engineering decisions:

- inspect the evidence supporting the result;
- verify high-impact findings/actions;
- preserve uncertainty;
- keep production, merge, deployment, rollback, data-repair, and security-control authority with the authorized human/system gate.

## Master rule

```text
MARKETING CLAIM <= OBSERVED EVIDENCE
```

> Prompt Machine does not ask you to trust a workflow because it looks sophisticated. It records what the workflow has actually earned the right to claim.
