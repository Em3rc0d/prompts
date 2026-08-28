# Prompt Quarry Developer Pack v1

Status: DRAFT

Prompt Quarry Developer Pack is a compact toolkit for structuring software and technical AI prompts with explicit inputs, constraints, outputs, uncertainty behavior, and quality gates.

It does not promise a universally best prompt. Pack assets keep their evidence state visible. `VALID` means static contracts passed; it does not mean runtime superiority, certification, or provider portability.

## Start here

1. Read `QUICKSTART.md`.
2. Pick the closest template in `templates/`.
3. Replace bracketed variables with your task context.
4. Run `checklists/static-quality.md`.
5. Execute the prompt in your chosen model/runtime.
6. Record runtime observations separately from static quality.

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

This pack contains Prompt Quarry-authored or Prompt Quarry-derived material. Raw harvested third-party bodies, private research internals, credentials, and synthetic outputs presented as real runtime evidence are forbidden from the bundle.
