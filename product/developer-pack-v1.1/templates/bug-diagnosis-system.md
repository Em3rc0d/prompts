# Bug Diagnosis System Template

Maturity: `DRAFT` — reusable operating template; no behavioral claim.

Use this when a team needs a repeatable debugging/incident-diagnosis workflow that preserves observations, hypotheses, diagnostic safety, and evidence thresholds across many defects.

Unlike the finished Free Bug Diagnosis prompt, this template exposes the diagnostic policy itself as configuration.

---

## 0. DIAGNOSTIC POLICY

Workflow name:

`[DIAGNOSTIC_POLICY_NAME]`

Diagnostic target:

`[BUG / INCIDENT / REGRESSION / PERFORMANCE DEGRADATION / DATA ISSUE / INTERMITTENT FAILURE]`

Consumer:

`[DEVELOPER / ON-CALL ENGINEER / INCIDENT COMMANDER / SUPPORT ESCALATION / AGENT / TICKET WORKFLOW]`

Operational authority:

`[ADVISORY_ONLY / HUMAN_DECIDES / INCIDENT_GATE]`

Primary outcome:

`[IDENTIFY ROOT CAUSE / NARROW HYPOTHESES / CHOOSE NEXT CHECK / MITIGATE SAFELY / VERIFY FIX]`

## 1. INPUT CONTRACT

### Required inputs

Configure the minimum evidence needed to begin:

- expected behavior: `[REQUIRED / OPTIONAL]`;
- observed behavior: `[REQUIRED / OPTIONAL]`;
- reproduction information: `[REQUIRED / OPTIONAL]`;
- environment/version: `[REQUIRED / OPTIONAL]`;
- evidence bundle: `[LOGS / ERRORS / STACK TRACE / CODE / METRICS / REQUEST IDS / OTHER]`.

### Optional context

Use when available and relevant:

- recent deployments/configuration changes;
- dependency changes;
- data/schema changes;
- blast radius / affected cohort;
- last known good point;
- prior incidents;
- monitoring anomalies;
- rollback/mitigation constraints.

Input state must be one of:

- `DIAGNOSABLE`
- `DIAGNOSABLE_WITH_UNKNOWNS`
- `INSUFFICIENT_EVIDENCE`

If required evidence is absent, ask only for information with clear diagnostic value.

## 2. EVIDENCE SEMANTICS

Default local labels:

- `OBSERVED` — directly present in supplied/retrieved evidence;
- `INFERRED` — logically suggested by observations;
- `UNKNOWN` — not established;
- `DISPROVED` — contradicted by supplied evidence;
- `CONFIRMED_CAUSE` — evidence links the mechanism to the observed failure and survives the configured confirmation rule.

Rules:

- never rewrite `INFERRED` or `UNKNOWN` as `OBSERVED`;
- timing/correlation alone does not establish causation;
- absence of a log line is not proof of absence unless logging coverage makes that inference valid;
- a plausible mechanism is still a hypothesis until evidence discriminates it;
- a fix appearing to work once does not by itself prove root cause.

### Root-cause confirmation threshold

Configure explicitly:

`[EXAMPLE: reproducible failure + discriminating check + mechanism-consistent fix/rollback + verification]`

A workflow must not output `CONFIRMED_CAUSE` unless this threshold is met.

## 3. SAFETY / CHANGE POLICY

Diagnostic actions may affect production. Configure what the workflow may recommend.

### Allowed without escalation

- `[READ-ONLY LOG/METRIC INSPECTION]`
- `[LOCAL/TEST REPRODUCTION]`
- `[NON-DESTRUCTIVE CONFIG CHECK]`

### Requires explicit human approval

- `[PRODUCTION CONFIG CHANGE]`
- `[ROLLBACK]`
- `[DATA REPAIR]`
- `[TRAFFIC SHIFT]`
- `[CACHE/QUEUE RESET]`
- `[SECURITY CONTROL CHANGE]`

### Forbidden diagnostic shortcuts

- destructive action when a reversible observation can provide equivalent information;
- deleting/rewriting production data solely to test a hypothesis;
- disabling security controls as a default diagnostic step;
- treating restart/redeploy success as proof of root cause;
- broad changes that destroy evidence before it is captured.

## 4. HYPOTHESIS POLICY

Configure maximum active hypotheses:

`[DEFAULT: 5]`

For every active hypothesis record:

- mechanism;
- observations explained;
- evidence against;
- unresolved facts;
- confidence;
- cheapest discriminating check.

Hypothesis ranking criteria:

1. explanatory coverage;
2. direct evidence strength;
3. number of unsupported assumptions;
4. consistency with timing/failure boundary;
5. discriminating-test availability.

Do not rank solely by familiarity or frequency in past incidents.

## 5. FAILURE-BOUNDARY PROCESS

Before recommending a fix, define where possible:

- last known good state;
- first known bad state;
- affected component/path;
- affected vs unaffected cohort;
- deterministic vs intermittent behavior;
- deployment/config/data boundary near onset;
- whether failure occurs before or after external dependencies.

Unknown boundaries should remain explicit.

## 6. DIAGNOSTIC PROCESS

### Phase A — observation ledger

List facts only. Associate each observation with its source.

### Phase B — normalize the failure

Separate:

- expected behavior;
- observed behavior;
- impact;
- reproduction state;
- environment.

### Phase C — generate bounded hypotheses

Generate at most the configured maximum. Avoid multiple phrasings of the same mechanism.

### Phase D — challenge each hypothesis

Ask:

- What does this explain?
- What does it fail to explain?
- Which observation contradicts it?
- Which assumption must be true?
- What test would sharply change its probability?

### Phase E — choose discriminating checks

Prefer checks with high information value and low risk.

For each check define:

- hypothesis/hypotheses tested;
- action;
- expected result if hypothesis is true;
- expected result if false;
- reversibility;
- production risk;
- evidence to capture before/after.

### Phase F — update diagnosis

Re-rank based on observed check results.

Do not preserve the original favorite hypothesis when new evidence contradicts it.

### Phase G — separate containment from cause correction

Classify actions as:

- `DIAGNOSTIC`
- `CONTAINMENT`
- `MITIGATION`
- `DURABLE_FIX`

A mitigation may be justified before root cause is confirmed, but label that distinction.

### Phase H — verify

Prove both:

1. the observed defect is no longer reproduced under the relevant conditions;
2. the proposed mechanism is consistent with the evidence/fix.

Add regression/monitoring checks where applicable.

## 7. DIAGNOSTIC STATE POLICY

Default states:

- `DIAGNOSE_FIRST`
- `MITIGATE_NOW`
- `FIX_SUPPORTED`
- `CAUSE_CONFIRMED`
- `INSUFFICIENT_EVIDENCE`

Suggested transitions:

```text
insufficient material evidence                     -> INSUFFICIENT_EVIDENCE
multiple viable hypotheses remain                  -> DIAGNOSE_FIRST
impact requires safe containment before certainty  -> MITIGATE_NOW
one fix is supported but confirmation incomplete   -> FIX_SUPPORTED
confirmation threshold satisfied                   -> CAUSE_CONFIRMED
```

Configure whether the workflow may recommend production-changing actions in each state.

## 8. OUTPUT CONTRACT

### 1. Diagnostic state

One configured state.

### 2. Current diagnosis

Summarize:

- observed failure;
- strongest current hypothesis;
- confidence;
- whether root cause is confirmed.

### 3. Observation ledger

| Observation | Evidence source | State | Consequence |
|---|---|---|---|
| ... | ... | OBSERVED | ... |

### 4. Failure boundary

Known / unknown:

- last good;
- first bad;
- affected path/cohort;
- deterministic/intermittent;
- relevant change boundary.

### 5. Ranked hypotheses

| Rank | Hypothesis | Evidence for | Evidence against | Assumptions | Confidence |
|---|---|---|---|---|---|

### 6. Next diagnostic checks

For each:

- action;
- hypotheses tested;
- true/false expected outcomes;
- information value;
- reversibility;
- production risk;
- evidence to capture.

### 7. Action recommendation

Classify as:

`DIAGNOSTIC | CONTAINMENT | MITIGATION | DURABLE_FIX`

Then state the smallest justified action and required approval.

### 8. Verification plan

Include applicable:

- reproduction check;
- targeted automated test;
- regression test;
- data/state verification;
- logs/metrics/monitoring confirmation;
- rollback verification.

### 9. Remaining unknowns

Only unknowns capable of changing diagnosis, action, or verification.

## 9. VERIFICATION CONTRACT

Before finalizing, verify:

- observation ledger contains no unlabeled assumptions;
- hypotheses are mechanically distinct rather than duplicate wording;
- reported confidence follows evidence, not familiarity;
- root cause is not called confirmed before the configured threshold;
- proposed diagnostic checks distinguish hypotheses;
- risky actions are labeled with approval requirements;
- mitigation is not described as causal proof;
- verification tests both symptom resolution and relevant mechanism;
- unresolved uncertainty is visible.

Local result:

- `DIAGNOSTIC_CONTRACT_PASS`
- `DIAGNOSTIC_CONTRACT_PASS_WITH_UNKNOWNS`
- `DIAGNOSTIC_CONTRACT_FAIL`

This is local workflow validation only. It does not establish Prompt Quarry F4/F5/F6/F7 evidence.

## 10. TEAM ADAPTATION MAP

| Configuration | Example |
|---|---|
| Required incident inputs | expected + observed + env + error/log evidence |
| Maximum hypotheses | 4 |
| Confirmation threshold | reproduce + discriminating test + fix + verify |
| Safe diagnostics | logs, metrics, read-only DB queries |
| Approval-required actions | rollback, data repair, traffic shift |
| State transitions | team incident policy |
| Output consumer | incident ticket + on-call engineer |
| Verification | reproduction + regression + monitoring |

## 11. INTEGRATION SHAPES

This system can map into:

- bug/incident ticket templates;
- on-call runbooks;
- support escalation workflows;
- incident-response agents;
- debugging assistants;
- post-incident evidence collection;
- Prompt Quarry Generator configuration.

When integrating, preserve the distinction between observation, hypothesis, mitigation, supported fix, and confirmed cause. Collapsing them into a single `diagnosis` string removes the governance value.
