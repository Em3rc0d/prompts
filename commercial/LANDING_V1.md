# Prompt Machine Landing v1

Status: `CUSTOMER COPY CONTRACT / PAID CHECKOUT OFF`

Date: `2026-09-03`

## Goal

A first-time visitor should understand Prompt Machine, identify a relevant workflow by desired outcome, try something useful for free, understand why the workflow is trustworthy, and intentionally inspect the `$9 Starter` or `$19 Full` collection without needing to understand Prompt Quarry internals.

Prompt Quarry is the factory. Prompt Machine is the product.

## Information architecture

```text
NAV
HERO
CUSTOMER JOBS / OUTCOMES
FREE VALUE
HOW PROMPT MACHINE WORKS
WHY WE TRUST THESE WORKFLOWS
STARTER $9
FULL $19
FREE vs STARTER vs FULL
KNOWN LIMITATIONS / EVIDENCE
FAQ
FINAL CTA
FOOTER
```

## Navigation

Customer-facing navigation should prioritize outcomes, not internal architecture.

Suggested:

- Workflows
- Collections
- How it works
- Evidence

Primary CTA while paid checkout is off:

`Try a free workflow`

Do not expose MK0, PCP, architecture-mother terminology, or internal Quarry stages as the main navigation model.

---

## Hero

### Eyebrow

`REUSABLE AI WORKFLOWS`

### H1

`Stop improvising the same AI task.`

### Supporting line

`Prompt Machine turns repeatable work into structured workflows with clear inputs, outputs, verification, limitations, and an evidence history.`

### Primary CTA

`Try a workflow free`

### Secondary CTA

`Explore collections`

### Trust line

`No magic-prompt claims. We show what was tested, what failed, what changed, and what is still unknown.`

---

## Customer jobs / outcomes

### Heading

`Start with what you need to get done.`

Prompt Machine should organize discovery around jobs/outcomes first.

Initial outcome groups:

- Build & Ship
- Research & Decide
- Learn & Create
- Operate & Automate

The first commercial wedge is developer/technical work, but profession is metadata rather than the primary product taxonomy.

Example cards:

**Review code with evidence**
Identify concrete issues without inventing findings simply to fill a checklist.

**Diagnose a bug**
Separate observed evidence, hypotheses, unknowns, and next verification steps.

**Make a technical decision**
Compare options without silently upgrading assumptions into facts.

---

## Free value

### Heading

`Use Prompt Machine on a real task before you buy.`

The Free surface should provide independently useful workflows and a low-friction path to first real-task activation.

Desired sequence:

```text
CHOOSE WORKFLOW
→ SUPPLY REAL TASK CONTEXT
→ RUN
→ GET STRUCTURED RESULT
→ VERIFY
```

The objective is not a download count. It is an activated user who reached an inspectable result on a real task.

### CTA

`Try a free workflow`

### Microcopy

`$0 · useful on its own · paid upgrade optional`

---

## How Prompt Machine works

### Heading

`A workflow, not a prompt dump.`

A customer-facing workflow should make the important operating decisions visible:

**Task contract**
What outcome it is intended to produce, what inputs it needs, and when it should stop/block.

**Execution**
The prompt/skill surface needed to run the workflow.

**Verification**
How the user can inspect whether the result is useful enough for the intended task.

**Limitations**
What is untested, unknown, unsafe, unsupported, or outside scope.

**Evidence history**
What has been observed, what failed, what changed, and what regression evidence exists.

---

## Why we trust these workflows

### Heading

`Trust should have a history.`

Prompt Machine does not hide every failure and show only green badges.

Future eligible workflow pages can present a bounded Trust History:

```text
WHAT WE TESTED
WHAT PASSED
WHAT FAILED
WHAT WE LEARNED
WHAT CHANGED
WHAT WE RETESTED
KNOWN LIMITATIONS
```

The internal forensic history stays richer than the customer projection, but the public story must remain traceable to reviewed evidence.

Example evidence-safe copy pattern:

> `This workflow was observed in N identified cases. A prior version failed X, the failure led to Y change, and the successor passed the specified regression set. These tests do not establish universal model portability.`

Never use this pattern until the referenced evidence actually exists.

Canonical policy: `docs/WORKFLOW_TRUST_HISTORY_V1.md`.

---

## Starter Collection — $9 hypothesis

### Badge

`SCOPE FROZEN · NOT YET FOR SALE`

### Heading

`The first paid collection for the jobs you repeat most.`

### Intended scope

- Evidence-first Code Review;
- Evidence-first Bug Diagnosis;
- two Skill candidates;
- `START_HERE` + task chooser;
- worked examples;
- verification guidance;
- adaptation cheatsheet;
- explicit evidence and limitations.

### Price

`$9 one-time` — price hypothesis.

### Current CTA

While checkout remains off:

`See what Starter will include`

Do not render a fake purchase button or imply that the product is currently sellable.

---

## Full Developer Collection — $19 hypothesis

### Badge

`PLANNED PREMIUM COLLECTION · NOT YET FOR SALE`

### Heading

`The broader workflow system.`

### Intended scope

- Code Review;
- Bug Diagnosis;
- Technical Decision;
- AI Workflow Designer;
- four Skill surfaces;
- workflow/task contracts;
- advanced adaptation;
- worked examples;
- evidence cards / Trust History;
- full collection navigation.

### Price

`$19 one-time` — price hypothesis.

### Current CTA

`Explore Full Collection`

---

## Free vs Starter vs Full

| | Free | Starter | Full |
|---|---|---|---|
| Price | $0 | $9 hypothesis | $19 hypothesis |
| Purpose | first useful real-task win | primary first purchase | broader premium system |
| Core developer workflows | selected free value | Code Review + Bug Diagnosis | broader four-workflow set |
| Start Here / task routing | lightweight | yes | yes |
| Worked examples | selected | yes | yes |
| Verification guidance | yes | richer | richer |
| Adaptation guidance | limited | cheatsheet | advanced |
| Skill surfaces | not guaranteed | 2 candidates | 4 candidates |
| Evidence/limitations | visible | visible | visible |
| Trust History | where evidence exists | where evidence exists | where evidence exists |
| Ready to sell today | free access only | no | no |

Do not claim a paid tier is `READY` until its separate product, delivery, evidence, and commerce gates pass.

---

## Evidence / limitations

### Heading

`We separate what is built from what is proven.`

Current governed manual architecture campaign:

```text
7 behavioral observations
7 / 7 expected-state matches
0 blocking review failures
```

This is promising evidence for the tested cases. It is **not** certification, universal reliability, portability, customer-value evidence, or readiness to sell.

Current broader truth:

```text
REAL CUSTOMER OUTCOMES   0
REAL PURCHASES            0
PUBLIC CHECKOUT           OFF
READY_TO_SELL             NO
```

This disclosure is part of the product philosophy, not hidden disclaimer text.

---

## FAQ

### Is Prompt Machine a prompt marketplace?

No. Prompt Machine is being built around reusable workflows for real jobs. Prompt Quarry is the internal factory that produces and improves them.

### Are these workflows guaranteed to work?

No. Evidence and limitations are bounded to what has actually been observed. Prompt Machine does not claim universal behavior without evidence.

### Are the workflows certified?

Not currently. Static checks, runtime observations, regression evidence, portability, customer value, and certification are separate states.

### Why show failures?

Because a documented failure, correction, and successful regression can provide more meaningful trust than a list of unexplained passes. Material failures are preserved rather than silently deleted.

### Why pay if Free is useful?

Free should solve real tasks. Starter and Full are intended to reduce repeated setup/friction and provide broader workflow systems, examples, adaptation, skills, and evidence surfaces when that additional value is worth paying for.

### Is this a subscription?

No. The initial paid hypotheses are `$9` and `$19` one-time collections. Subscription is deferred until recurring customer value is observed.

---

## Final CTA

### Heading

`Start with a real task.`

Primary:

`Try a free workflow`

Secondary:

`Explore Starter and Full`

---

## Visual direction

Prompt Machine should feel like a trustworthy engineering/productivity system, not an AI hype storefront.

Use:

- strong readable typography;
- outcome-first workflow cards;
- compact evidence summaries;
- version/state labels;
- clear limitations;
- before/failure/change/retest timelines where useful;
- restrained motion;
- accessible interaction states.

Avoid:

- robot stock imagery;
- fake testimonials;
- fake sale counters;
- fake crossed-out prices;
- unsupported portability/model-logo claims;
- opaque "97% quality" scores without a validated scoring methodology;
- excessive internal factory jargon on customer pages.

## Mobile requirements

On a phone, the first viewport should communicate:

1. the job/outcome orientation;
2. that these are reusable workflows rather than random prompts;
3. a free real-task CTA;
4. one concise evidence/trust cue.

No comparison table should be required to understand the core value proposition.

## Master rule

> **The landing page may tell the workflow's story only after the evidence ledger can support that story.**
