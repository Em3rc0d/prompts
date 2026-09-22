# Verlune v1 — Launch Scope Freeze Candidate

Status: `SCOPE_CANDIDATE / LANDING_FROZEN`

Date: 2026-09-22

## Decision

The public landing must not be rewritten around the new Verlune product model until the v1 product package passes the human review gate defined in `HUMAN_REVIEW_GATE.md`.

The catalog may contain more ideas than launch requires. Only the **launch core** is reviewed for v1.

## Launch core

### Free

Eight structured prompts — one visible entry point per primary category:

1. Development & Tech — **Explain Code Clearly**
2. Study & Learning — **Learn a Difficult Topic**
3. Research & Analysis — **Research a Topic**
4. Business & Operations — **Analyze a Business Problem**
5. Writing & Communication — **Improve Writing**
6. Content & Marketing — **Improve a Content Draft**
7. Planning & Productivity — **Plan a Project**
8. Career & Job Search — **Prepare for an Interview**

Three selected workflows:

- **Compare Options**
- **Guided Study Session**
- **Bug Diagnosis**

Free is intended to prove breadth and usefulness. Every released Free asset must solve its stated task without requiring payment.

### Premium

Eight Premium Prompts — one deeper paid entry point per primary category:

1. Development & Tech — **Requirements Analysis**
2. Study & Learning — **Exam Preparation**
3. Research & Analysis — **Evidence Synthesis**
4. Business & Operations — **SOP Drafting**
5. Writing & Communication — **Rewrite for Audience and Intent**
6. Content & Marketing — **Content Strategy Brief**
7. Planning & Productivity — **Risk-Aware Project Plan**
8. Career & Job Search — **Tailor a Resume to a Role**

Five Premium Workflows:

- **Evidence-first Code Review**
- **Evidence-first Deep Research**
- **Decision Analysis**
- **Master a Topic**
- **Content Strategy System**

Premium creation tools:

- **Prompt Builder**
- **Workflow Builder**

Premium support toolkit:

- **Adaptation Guide**
- **Evaluation Toolkit**

## Backlog — explicitly not launch-blocking

The following remain candidates for later releases unless promoted through the same gates:

Premium prompts:

- Safe Refactoring Plan
- Active Recall Coach
- Source Quality Review
- Customer Problem Analysis
- Document Critique
- Audience and Angle Research
- Prioritize Under Constraints
- Interview Preparation System

Premium workflows:

- Root Cause Analysis
- Project Planning and Risk

They must not appear in launch item counts or public value claims until promoted.

## Why the launch core is bounded

A bigger visible library is not automatically a better product.

Every public asset creates:

- design work;
- runtime evaluation work;
- human-review work;
- compatibility claims to police;
- maintenance/versioning burden;
- customer expectations.

The v1 launch core is therefore optimized for:

```text
BREADTH ACROSS REAL WORK
+
ENOUGH PREMIUM DEPTH TO JUSTIFY A TEST PURCHASE
+
BUILD-YOUR-OWN CAPABILITY
+
REVIEWABLE EVIDENCE
```

not maximum item count.

## Tier boundary

### Free

`USE VERLUNE`

Free demonstrates that structured prompts/workflows are materially more useful than a blank chat for common tasks.

### Premium

`USE + GO DEEPER + ADAPT + BUILD + TEST`

Premium earns the USD 9 launch hypothesis through the combination of:

- deeper assets;
- more advanced workflows;
- Prompt Builder;
- Workflow Builder;
- adaptation;
- evaluation.

No single Premium prompt carries the entire commercial value proposition.

## Landing freeze

Until human review passes:

- do not replace the current public home positioning with the new library/toolkit promise;
- do not publicly advertise launch-core item counts;
- do not expose candidates as available assets;
- do not switch the primary paid SKU to the new Premium model;
- do not enable new public purchase claims.

Allowed before PASS:

- internal product construction;
- controlled runtime tests;
- private review;
- branch/preview work clearly marked non-public if needed.

## Exit condition

This scope may advance to landing redesign only when:

```text
PRODUCT_MODEL_REVIEW          PASS
FREE_CORE_REVIEW              PASS
PREMIUM_CORE_REVIEW           PASS
PROMPT_BUILDER_REVIEW         PASS
WORKFLOW_BUILDER_REVIEW       PASS
FREE_VS_PREMIUM_REVIEW        PASS
$9_VALUE_REVIEW               PASS
CLAIM_BOUNDARY_REVIEW         PASS
HUMAN_FINAL_REVIEW            PASS

=> LANDING_REDESIGN_AUTHORIZED
```

The landing redesign is a consequence of product approval, not a substitute for it.
