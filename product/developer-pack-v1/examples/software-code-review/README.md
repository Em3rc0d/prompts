# Example — Software Code Review

This example shows the path from a raw request to a normalized task brief and a reusable prompt artifact.

## Inputs

- `request.json`: original structured request.
- `task-brief.json`: normalized task contract.
- `prompt.md`: final example prompt.

## Architecture choice

The example uses `PURPOSE`, `CONTEXT`, `INTAKE`, `PROCESS`, `RULES`, `OUTPUT CONTRACT`, `QUALITY GATE`, and `FALLBACK` because code review benefits from explicit evidence boundaries, finding structure, and uncertainty behavior.

A decorative role section was not required.

## Static quality result

The prompt passed the Developer Pack static acceptance surface:
- inputs are explicit;
- unobserved runtime facts are forbidden;
- output fields are defined;
- uncertainty and missing context have explicit behavior;
- findings must connect to evidence.

## Maturity

`VALID` — static package acceptance passed.

No runtime output is included here, so this example does not establish `TESTED`, `IMPROVED`, `CERTIFIED`, or `PORTABLE`.

## Claim boundary

This is an authored demonstration of Prompt Quarry's static design contracts, not proof that the prompt outperforms another prompt in a model runtime.
