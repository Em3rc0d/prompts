# Prompt Quarry Developer Pack v1

Asset maturity: `VALID` (static acceptance only)
Distribution status: defined by the release manifest for the package you received.

Prompt Quarry Developer Pack is a compact toolkit for structuring software and technical AI prompts with explicit inputs, constraints, outputs, uncertainty behavior, and quality gates.

It does not promise a universally best prompt. Pack assets keep their evidence state visible. `VALID` means static contracts passed; it does not mean runtime superiority, certification, or provider portability.

## Start here

1. Read `QUICKSTART.md`.
2. Pick the closest template in `templates/`.
3. Replace bracketed variables with your task context.
4. Run `checklists/static-quality.md`.
5. Execute the prompt in your chosen model/runtime.
6. Record runtime observations separately from static quality.
7. Read `LICENSE.md` before redistributing or embedding Pack-derived material.

## Package map

```text
README.md
QUICKSTART.md
LICENSE.md
methodology/
  architecture.md
  evidence-states.md
  evaluation.md
contracts/
  task-brief.example.json
  prompt-request.example.json
templates/
  general-structured-prompt.md
  software-code-review.md
  technical-research-decision.md
examples/
  software-code-review/
  technical-research-decision/
checklists/
  static-quality.md
  release-readiness.md
```

Use `methodology/architecture.md` when deciding which prompt sections matter. Use `methodology/evidence-states.md` before making quality claims. Use `methodology/evaluation.md` when moving from static design to real runtime observation.

The `contracts/` examples show machine-readable task/request shapes. The `examples/` directories show request → task brief → prompt → static evidence boundary end to end.

## Core architecture

Use only the sections your task needs:

`PURPOSE → ROLE → CONTEXT → INTAKE → ASSUMPTIONS → PROCESS → RULES → OUTPUT CONTRACT → QUALITY GATE → FALLBACK`

Section count is not a quality metric.

## Evidence states

- `DRAFT`: authored but not statically accepted.
- `VALID`: static contracts and integrity checks passed.
- `TESTED`: requires real F4 behavioral evidence.
- `CANDIDATE / IMPROVED`: requires F5 comparative superiority evidence.
- `CERTIFIED`: requires F6 repeated same-target evidence.
- `PORTABLE`: requires F7 cross-provider evidence.

Commercial packaging never promotes an artifact's evidence state.

## Distribution boundary

This Pack is licensed for authorized use and adaptation under `LICENSE.md`. Resale, sublicensing, redistribution, publication, or offering the Pack, its templates, or substantially equivalent prompt libraries as standalone or competing products is prohibited.

This Pack contains Prompt Quarry-authored or Prompt Quarry-derived material. Raw harvested third-party bodies, private research internals, credentials, and synthetic outputs presented as real runtime evidence are forbidden from the bundle.
