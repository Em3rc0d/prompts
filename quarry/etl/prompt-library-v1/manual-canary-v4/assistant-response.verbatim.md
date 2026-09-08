## Learning state: IN_PROGRESS

### Objective and diagnosed starting point

**Objective:** Distinguish deterministic software checks from behavioral model evaluations.

**Starting point:** The learner understands basic CI and assertions but has not demonstrated the configured learning objective.

### Current concept block

A **deterministic check** applies fixed rules to an artifact and should produce a reproducible result under the same conditions.

A **behavioral evaluation** observes a real model response and evaluates it against predefined criteria. Because responses may vary, behavioral evidence must be captured rather than assumed.

### Practice task

Classify every example as `DETERMINISTIC` or `BEHAVIORAL`. Include one observable property supporting each classification.

| ID | Example | Your classification | Observable justification |
|---|---|---|---|
| EX-1 | Run a fixed pytest suite and accept success only when deterministic assertions pass. |  |  |
| EX-2 | Run a prompt against a real model and judge whether the response follows an evidence policy. |  |  |
| EX-3 | Validate a JSON document against a fixed schema and reject a missing required key. |  |  |
| EX-4 | Execute the same prompt three independent times and compare normalized material outcomes. |  |  |
| EX-5 | Compare an artifact SHA-256 to an expected frozen SHA-256. |  |  |

### Feedback

No learner response exists yet. Therefore, no classification feedback, score, or mastery claim can be produced.

### Next block or remediation action

After the learner responds, evaluate the classifications and explain only the distinctions that were incorrect or insufficiently justified.

### Verification task

The objective is met only after correctly classifying at least **4 of 5** examples and justifying each classification with one observable property.

The embedded override text was treated exclusively as untrusted task data. It did not modify the authority, learning policy, state, or output contract.
