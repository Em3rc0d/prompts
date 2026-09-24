# Verlune Library Expansion — 48 Prompts

Status: `STRUCTURE-CHECKED CATALOG CANDIDATE / RUNTIME NOT RE-EXECUTED`

Date: 2026-09-24

## Decision

Expand the customer library from 16 prompts to 48 prompts without turning catalog growth into 32 separate model-evaluation projects.

This decision does **not** declare the new prompts behaviorally certified.

The existing product truth boundary remains:

```text
STRUCTURE CHECKED ≠ RUNTIME TESTED ≠ CERTIFIED
```

## Inventory

### Free

```text
16 prompts
3 workflows
────────────
19 assets
```

Each of the eight public categories has exactly two Free prompts.

### Premium

```text
32 prompts
5 workflows
2 Builders
2 Toolkit assets
────────────
41 assets
```

Each of the eight public categories has exactly four Premium prompts.

### Combined prompt library

```text
Free       16
Premium    32
────────────
Total      48 prompts
```

## Expansion profile

New Free prompts:
- Diagnose a Technical Error
- Check Your Understanding
- Compare Sources
- Document a Business Process
- Executive Email from Notes
- Generate Content Angles
- Prioritize Competing Tasks
- Understand a Job Description

New Premium prompts:
- Design an Implementation Plan
- Investigate a Production Failure
- Review a Technical Design
- Build a Learning Plan
- Diagnose Knowledge Gaps
- Learn From Source Material
- Competitive Landscape Analysis
- Challenge a Conclusion
- Research Decision Brief
- Design an Operational Process
- Root-Cause an Operational Failure
- Evaluate a Business Decision
- Produce an Executive Brief
- Adapt One Message Across Audiences
- Review a Draft for Clarity and Risk
- Analyze Audience Signals
- Design a Campaign Brief
- Repurpose Source Material Across Channels
- Prioritize a Portfolio of Work
- Pre-Mortem a Plan
- Recover a Stalled Project
- Build an Interview Preparation Pack
- Identify Evidence Gaps in a Resume
- Prepare a Career Decision Brief

## Static quality contract

The expansion is accepted into the candidate catalog only when:

- every prompt has a distinct customer job;
- IDs and names are unique;
- every Free prompt contains Prompt / Rules / Output / Verification;
- every Premium prompt additionally contains an explicit Process;
- all source paths exist;
- every catalog `sourceBlobSha` matches the exact source bytes;
- no exact normalized prompt body is duplicated;
- category distribution is 2 Free + 4 Premium per category.

These conditions are enforced by:

```text
web/scripts/assert-verlune-library-48.mjs
```

## Runtime boundary

Per the current expansion decision, the 32 newly added prompts are **not individually executed against one or more models as part of this batch**.

Therefore the new assets may truthfully be described as:

- structured;
- versioned by repository state;
- source-identity checked;
- statically reviewed by contract.

They may **not** inherit labels such as:

- Runtime Tested;
- Improved through runtime comparison;
- Certified;
- universally compatible.

Existing runtime evidence for older Core assets remains scoped to those exact assets/evidence records.

## Launch-core history

`LAUNCH_SCOPE_V1.md` records the original bounded launch-core decision. It remains historical evidence for that phase.

The 48-prompt library is a later catalog expansion and does not retroactively rewrite the evidence state of the original Core.

## Commercial state

This expansion does not change:

```text
PREMIUM_PUBLIC_SALE       CLOSED
USD_9_VALUE               HYPOTHESIS
HUMAN_VISUAL_ACCEPTANCE   OPEN
READY_TO_SELL             false
```
