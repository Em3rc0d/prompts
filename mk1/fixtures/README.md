# MK1 Fixtures

MK1 fixtures test engineered prompt behavior.

They are different from MK0 source fixtures:

```text
MK0 fixture
  proves / characterizes what we observed

MK1 fixture
  tests whether an engineered prompt behaves correctly
```

MK1 may reuse MK0 Golden Dataset evidence when it is relevant, but it must translate that evidence into a task-specific evaluation case rather than treating source examples as unquestioned expected answers.

## Minimum fixture set per prompt

A prompt seeking certification should normally include several of these fixture classes.

### 1. Happy path

Representative complete input with a clearly useful expected result.

### 2. Minimal valid input

Smallest input that should still allow useful execution.

Purpose: detect unnecessary intake and fragile dependencies.

### 3. Missing critical input

Omit information that materially changes the answer.

Expected behavior may be a targeted question, uncertainty label or bounded response rather than fabrication.

### 4. Ambiguous input

Provide multiple plausible interpretations.

Expected behavior: clarify or explicitly choose/label an assumption.

### 5. Contradictory input

Supply conflicting facts or requirements.

Expected behavior: surface the conflict rather than silently choosing one.

### 6. Boundary / edge case

Task-specific case near the supported boundary.

### 7. Noise / irrelevant context

Add distracting information.

Expected behavior: preserve focus on the declared task.

### 8. Regression fixture

A previously observed failure that must never reappear.

Every meaningful production or evaluation incident should be considered for permanent regression-fixture status.

### 9. High-stakes boundary

Required when the prompt operates in consequential legal, medical, financial or safety-relevant domains.

Expected behavior includes appropriate uncertainty, evidence discipline and escalation boundaries.

## Fixture record

Recommended machine contract:

```yaml
fixture_id: pq_mk1_fixture_<id>
prompt_contract: pq_mk1_<id>
class: happy-path | minimal | missing-critical | ambiguous | contradictory | edge | noise | regression | high-stakes
name: human-readable fixture title

input:
  variables: {}
  user_context: null

expected:
  required_behaviors: []
  forbidden_behaviors: []
  required_output_elements: []
  notes: []

severity: normal | blocking
provenance:
  mk0_fixture_ids: []
  incident_ids: []
```

Do not over-specify exact wording unless wording itself is the behavior under test.

## Fixture-set identity

A certification run references a versioned fixture set.

Example:

```text
pq_mk1_fs_code_review_v1
```

If the fixture set materially changes, old certification receipts remain attached to the version they actually executed.

## Baseline fairness

Candidate and baseline prompts must receive:

- the same fixture input;
- the same evaluation criteria;
- equivalent model/runtime conditions when runtime comparison is involved.

Do not claim superiority from tests that advantaged the candidate with extra context unavailable to the baseline.

## Golden Dataset relationship

MK0 Golden Dataset is the source-characterization benchmark.

MK1 fixture sets are product-behavior benchmarks.

Together:

```text
MK0 Golden Dataset
       │
       ├── teaches architecture / failure patterns
       └── provides stable evidence references
                    │
                    ▼
              MK1 fixture design
                    │
                    ▼
           prompt behavior evaluation
```
