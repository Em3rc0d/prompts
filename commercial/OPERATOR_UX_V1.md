# Prompt Machine Operator UX v1

## Purpose

Prompt Machine may keep a rigorous internal evidence and release pipeline without turning the product owner into a manual runner.

The operator experience is governed by this rule:

> **COMPLEXITY INSIDE THE SYSTEM; ONE ACTION AT THE OPERATOR BOUNDARY.**

This document constrains human-facing execution for governed Prompt Machine release work.

## Operator invariant

For any bounded release/checkpoint action that can be automated safely:

- the product owner runs **at most one command**;
- that command performs its own preflight;
- it must not require the owner to manually chain `git pull`, `git status`, hash checks, individual case commands, receipt collection, or repeated retries;
- local uncommitted work must not be overwritten or silently discarded;
- the command must fail closed before external effects when prerequisites are not satisfied;
- the command must report one of:
  - `PASS`
  - `BLOCKED`
  - `ACTION_REQUIRED`
- if external authorization or a provider-side action is required, the command stops at that boundary and reports the exact next requirement;
- authorization for one bounded external action must never imply authorization for another.

## Clean-execution rule

The operator entrypoint must prefer an isolated temporary checkout/worktree of the exact remote branch or commit over modifying the user's active working tree.

This protects local changes and removes the need for manual stash/pull/pop ceremonies.

## No hidden convenience tradeoff

Reducing operator friction must not weaken evidence quality. The entrypoint may automate:

- repository synchronization;
- exact ref resolution;
- clean worktree creation;
- deterministic build;
- static and offline QA;
- preflight checks;
- bounded runtime invocation after explicit authorization;
- receipt collection;
- final status rendering.

It must not automate without explicit authorization:

- provider purchases;
- live checkout enablement;
- public release;
- irreversible provider configuration;
- repository merge;
- any runtime batch whose policy requires fresh authorization.

## Human-facing output

Default output should be compact and decision-oriented:

```text
PROMPT MACHINE OPERATOR
state: PASS | BLOCKED | ACTION_REQUIRED
stage: <gate/stage>
head: <exact commit>
external_effects: 0 | <bounded count>
next: <one concise next action or NONE>
```

Detailed logs and receipts may be written to disk for audit, but should not be required reading for routine operation.

## Release principle

The quality target remains unchanged:

`MARKETING CLAIM <= OBSERVED EVIDENCE`

Operator UX changes **how work is executed**, not what evidence is required.
