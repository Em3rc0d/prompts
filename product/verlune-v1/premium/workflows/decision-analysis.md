# Decision Analysis

Status: `PREMIUM WORKFLOW CANDIDATE / EXISTING STATIC LINEAGE / NOT_FOR_SALE`

Workflow ID: `VP-WF-004`

Use for consequential but non-regulated choices involving options, constraints, evidence, trade-offs, uncertainty, and reversibility.

## Inputs

Required:

- decision;
- options or option-discovery boundary;
- desired outcome;
- hard constraints.

Useful:

- weighted criteria;
- evidence;
- deadline;
- budget;
- reversibility;
- switching cost;
- stakeholders.

## Authority

This workflow supports a human decision. It does not silently make commitments, purchases, deployments, legal/medical decisions, or other actions.

## Process

### 1. Decision contract

Define exactly:

- what is being decided;
- by whom;
- by when;
- what success means;
- what would make every current option unacceptable.

### 2. Constraint gate

Classify every hard constraint and eliminate options that demonstrably violate one.

Unknown compliance with a hard constraint is not a pass.

### 3. Criteria

Use a shared set of criteria.

For each criterion define:

- meaning;
- importance;
- evidence needed;
- whether it is a hard gate or trade-off.

Avoid fake precision. Numeric weights are optional and must have a stated interpretation.

### 4. Evidence ledger

For every material option/criterion claim use:

- `OBSERVED`
- `SOURCE_CLAIM`
- `INFERRED`
- `ASSUMPTION`
- `UNKNOWN`

### 5. Comparative analysis

Compare viable options using the same criteria.

Identify:

- advantages;
- costs;
- risks;
- dependencies;
- uncertainty;
- switching/reversal implications.

### 6. Decision state

Choose one:

- `DECIDE`
- `DECIDE_WITH_UNKNOWNS`
- `VALIDATE_FIRST`
- `HOLD`
- `REJECT_ALL`

### 7. Reversal policy

Define what new evidence should cause the decision to be revisited.

## Output

1. Decision contract.
2. Hard-constraint table.
3. Criteria and evidence needs.
4. Option comparison.
5. Evidence/assumption ledger.
6. Trade-offs.
7. Decision state.
8. Recommendation only when state permits.
9. Highest-value validation.
10. Reversal triggers.

## Verification

A recommendation must not:

- violate a hard constraint;
- depend on hidden assumptions;
- force a winner under insufficient evidence;
- use different criteria for different options without explanation.
