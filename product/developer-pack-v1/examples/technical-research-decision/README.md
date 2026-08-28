# Example — Technical Research Decision

This example demonstrates a structured decision prompt built from an explicit request and normalized task brief.

## Inputs

- `request.json`: original structured request.
- `task-brief.json`: normalized task contract.
- `prompt.md`: final example prompt.

## Architecture choice

The example uses `PURPOSE`, `CONTEXT`, `INTAKE`, `PROCESS`, `RULES`, `OUTPUT CONTRACT`, `QUALITY GATE`, and `FALLBACK`. The important controls are shared decision criteria, evidence/inference separation, hard-constraint rejection, and recommendation-changing conditions.

## Static quality result

The example is designed so that:
- required decision inputs are explicit;
- evidence gaps remain unknown;
- all viable options use the same criteria;
- the output exposes trade-offs and uncertainty;
- the recommendation is required to follow from evidence and constraints.

## Maturity

`DRAFT` until the Developer Pack static acceptance gate promotes it to `VALID`.

No runtime comparison is included, so this example is not `TESTED`, `IMPROVED`, `CERTIFIED`, or `PORTABLE`.

## Claim boundary

This example demonstrates an engineered decision-prompt contract. It does not prove model accuracy or superiority in a runtime.
