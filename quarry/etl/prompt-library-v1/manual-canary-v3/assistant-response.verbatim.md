## Learning state: IN_PROGRESS

### Objective and diagnosed starting point

**Objective:** Distinguish deterministic software checks from behavioral model evaluations.

**Starting point:** The learner understands basic CI and assertions but has not yet designed prompt-evaluation campaigns. Mastery has not been demonstrated.

### Current concept block

A **deterministic check** evaluates an artifact using fixed rules. With the same input and environment, its result should remain reproducible.

A **behavioral evaluation** observes how a real model responds and judges that response against predefined criteria. Its outcome may vary, so it requires captured evidence and sometimes repeated executions.

### Practice task

Classify each example as:

- `DETERMINISTIC`
- `BEHAVIORAL`

For every answer, include **one observable property** that justifies the classification.

| ID | Example | Your classification | Observable justification |
|---|---|---|---|
| EX-1 | Run a fixed pytest suite and accept success only when deterministic assertions pass. |  |  |
| EX-2 | Run a prompt against a real model and judge whether the response follows an evidence policy. |  |  |
| EX-3 | Validate a JSON document against a fixed schema and reject a missing required key. |  |  |
| EX-4 | Execute the same prompt three independent times and compare normalized material outcomes. |  |  |
| EX-5 | Compare an artifact SHA-256 to an expected frozen SHA-256. |  |  |

### Feedback

No feedback or mastery determination is available yet because the learner has not submitted classifications.

### Next block or remediation action

After submission, review each classification using the distinction between fixed-rule reproducibility and observed model behavior. Explain only the items that were incorrect or insufficiently justified.

### Verification task

Correctly classify at least **4 of 5** examples and justify each classification with one observable property. Until that evidence exists, the learning state remains `IN_PROGRESS`.
