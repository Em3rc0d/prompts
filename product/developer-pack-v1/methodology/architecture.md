# Prompt Architecture

Prompt Quarry treats prompt architecture as a purposeful contract, not a section-count contest.

A useful architecture may contain:

`PURPOSE → ROLE → CONTEXT → INTAKE → ASSUMPTIONS → PROCESS → RULES → OUTPUT CONTRACT → QUALITY GATE → FALLBACK`

## Selection principle

Include a section only when it removes ambiguity or controls an important failure mode.

- `PURPOSE` defines the outcome.
- `ROLE` is useful when an operating perspective changes how the task should be performed.
- `CONTEXT` defines what the model may rely on.
- `INTAKE` makes required inputs explicit.
- `ASSUMPTIONS` exposes guesses that could change the result.
- `PROCESS` defines meaningful work stages.
- `RULES` encode hard constraints and prohibited behavior.
- `OUTPUT CONTRACT` specifies what a usable answer must contain.
- `QUALITY GATE` defines checks before finalization.
- `FALLBACK` defines behavior when evidence or inputs are insufficient.

## Design rule

Do not add complexity because a longer prompt looks sophisticated. Add structure when it makes behavior easier to understand, evaluate, or reproduce.

## Static vs behavioral quality

A well-structured prompt can still perform poorly in a runtime. Architecture supports static quality; actual model behavior must be observed separately.
