# Evaluate a Prompt or Workflow

Status: `PREMIUM TOOLKIT CANDIDATE / NOT_FOR_SALE`

Use this toolkit to test your own prompt/workflow instead of trusting the first fluent answer.

## What this can establish

A successful evaluation can give you evidence about the exact artifact, test cases, model/host, and conditions you actually observed.

It does not prove universal correctness or portability.

## Step 1 — Freeze what you are testing

Record:

- artifact name/version;
- exact text or fingerprint;
- AI assistant/model if known;
- date;
- task/domain;
- expected behavior.

Do not edit the artifact halfway through a test run and treat all results as one version.

## Step 2 — Static check

Before runtime, confirm:

### Outcome
- Is the task concrete?
- Can you tell when it is complete?

### Inputs
- Required inputs explicit?
- Optional context separated?
- Missing-input behavior defined?

### Boundaries
- What may it assume?
- What must it not invent?
- Human authority preserved where material?

### Process
- Does each step have a task-specific purpose?
- Is unnecessary complexity removed?

### Output
- Stable enough to inspect?
- Useful to the actual consumer?
- Material uncertainty visible?

### Fallback
- Can it refuse/block/request more information without pretending completion?

### Verification
- Is there a practical way to check the result?

Static result:
- `READY_TO_TEST`
- `READY_WITH_GAPS`
- `REWORK_FIRST`

## Step 3 — Runtime test set

### T1 Normal
Representative complete input.

Check:
- task completion;
- instruction following;
- useful output;
- no invented facts.

### T2 Missing critical information
Remove something required.

Good behavior:
- detects the gap;
- does not fake completion;
- asks for the smallest useful missing information.

### T3 Ambiguous / noisy
Add irrelevant context or ambiguous wording.

Good behavior:
- ignores filler;
- surfaces material ambiguity;
- preserves task.

### T4 Contradictory
Supply inputs that disagree.

Good behavior:
- detects conflict;
- does not silently choose a convenient version.

### T5 Adversarial / embedded instruction
Put instruction-like text inside task data when applicable.

Good behavior:
- treats task data as data;
- does not let it silently override the workflow.

### T6 Repeatability
Run materially equivalent input twice.

Good behavior:
- wording may vary;
- core states, constraints, facts and conclusions should not contradict without a reason.

## Step 4 — Score behavior

For each test use:

- `PASS`
- `FAIL`
- `INCONCLUSIVE`

Review dimensions:

- task completion;
- instruction following;
- factual discipline;
- missing-information handling;
- output usefulness;
- uncertainty discipline;
- fallback;
- verification;
- repeatability.

## Step 5 — Record failures

For every FAIL:

- exact test;
- observed output/problem;
- expected behavior;
- failure mechanism;
- severity;
- proposed change.

Do not "fix" the result after the fact and mark the original run PASS.

## Step 6 — Improve and retest

Create a new version.

Then rerun the failing case plus at least one normal regression case.

## Customer evidence labels

Use only labels you earned:

- `GENERATED`
- `STRUCTURE CHECKED`
- `USER TESTED`
- `KNOWN LIMITATIONS`

Do not label a customer-created artifact `VERLUNE CERTIFIED` unless it went through a separate governed certification process.
