# MK1 F4 — Behavioral Testing Contract

F4 is the first MK1 phase allowed to advance an engineered prompt from `VALID` to `TESTED`.

The boundary is strict:

```text
static lint / critic PASS != behavioral TESTED
```

## Two lanes

### F4A — harness characterization

F4A proves that the fixture parser, assertion evaluator and receipt semantics behave deterministically.

It may use synthetic outputs in CI.

A synthetic run must always emit:

```text
status = HARNESS_CHARACTERIZATION
eligible_for_tested = false
```

Synthetic success is evidence about the **test harness**, not about the prompt.

### F4B — real behavioral execution

F4B executes an identified `VALID` artifact against a declared, versioned fixture set using an identified runtime.

A real run records at minimum:

- artifact id/version and prompt fingerprint;
- fixture set id/version;
- runtime provider/model/profile;
- execution mode;
- observed output per fixture;
- machine assertion results;
- unresolved human review checks;
- blocking failures;
- durable receipt id.

Only an F4B run may set:

```text
status = BEHAVIORAL_PASS
eligible_for_tested = true
```

## Fixture semantics

Each fixture contains:

```text
fixture_id
class
severity
input.variables
expected.machine_assertions
expected.human_checks
provenance
```

Current machine assertion vocabulary:

- `contains_all`
- `contains_any`
- `not_contains_any`
- `question_count_at_most`
- `min_length`
- `max_length`

Machine assertions are intentionally small and auditable. They do not pretend to solve semantic evaluation.

## Human checks

Some behaviors cannot be reliably inferred from substring assertions, for example:

- material-meaning preservation;
- whether evidence really supports a claim;
- whether a recommendation is substantively useful;
- whether severity is proportionate.

Such checks remain explicit in `expected.human_checks`.

A real execution with unresolved human checks may produce evidence, but it is **not eligible** to advance the artifact to `TESTED`.

## Promotion rule

A candidate becomes `TESTED` only when all are true:

1. source artifact state is `VALID`;
2. F1 linter is `PASS`;
3. F3 critic is `PASS`;
4. fixture set is versioned and identifies the artifact;
5. execution mode is real (`api` or `manual-observed`), never `synthetic`;
6. runtime identity is present;
7. every blocking machine assertion passes;
8. every blocking human check is explicitly resolved PASS;
9. receipt is persisted;
10. artifact evaluation references that exact fixture set and receipt.

## State semantics

```text
VALID
  + F4 evidence that is incomplete
  = VALID

VALID
  + complete F4 behavioral receipt
  = TESTED
```

F4 does not compare against a baseline and therefore cannot produce `improved`.

Baseline comparison belongs to F5. Certification belongs to F6.
