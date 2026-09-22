# Compare Options

Status: `FREE WORKFLOW CANDIDATE / NOT_FOR_SALE`

Use when you need to compare alternatives without letting popularity or presentation hide constraints.

## Start condition

You have a real choice between two or more options.

## Inputs

Required:

- decision/question;
- candidate options;
- most important constraint or success criterion.

Useful when available:

- deadline;
- budget/resources;
- must-have requirements;
- evidence about each option;
- reversibility.

## Workflow

### 1. Normalize the decision

State what is actually being chosen and what success means.

### 2. Identify hard constraints

List conditions that an option must satisfy. An option that violates a hard constraint is not rescued by a high score elsewhere.

### 3. Separate facts from assumptions

For each option classify important statements as:

- `OBSERVED` — supported by supplied evidence;
- `SOURCE_CLAIM` — stated by an identified source;
- `INFERRED` — reasoned but not directly established;
- `UNKNOWN` — not established.

Do not invent evidence.

### 4. Compare on shared criteria

Use the same material criteria for every viable option.

Do not add a criterion only because it favors one option.

### 5. Check uncertainty and reversibility

Identify what could change the result and how expensive it is to reverse the choice.

### 6. Choose a state

Return exactly one:

- `DECIDE` — evidence is sufficient for a recommendation;
- `DECIDE_WITH_UNKNOWNS` — a recommendation is reasonable but material uncertainty remains;
- `VALIDATE_FIRST` — one missing check could materially change the choice;
- `REJECT_ALL` — no option satisfies the hard constraints.

## Output

1. Decision and success condition.
2. Hard constraints.
3. Comparison table.
4. Evidence / assumptions / unknowns.
5. Trade-offs.
6. Decision state.
7. Recommendation only when justified.
8. Highest-value next validation.
9. Reversal trigger: what new evidence should cause the decision to be reconsidered.

## Verification

Before finishing, check that the recommendation:

- respects all hard constraints;
- uses shared criteria;
- does not turn unknowns into facts;
- does not force a winner when `VALIDATE_FIRST` or `REJECT_ALL` is more accurate.
