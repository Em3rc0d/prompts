# Worked Example — Evidence-first Bug Diagnosis

**SYNTHETIC EXAMPLE — NOT A RUNTIME OBSERVATION — NOT CUSTOMER EVIDENCE**

Purpose: demonstrate how to provide a bounded debugging case and how the workflow should separate observations, hypotheses, checks, mitigation, and confirmed cause.

The response below is an authored illustrative fixture. It is not evidence that a model produced this result.

---

## Example input

### Expected behavior

After `POST /profile` returns success, the next `GET /profile` should show the updated display name.

### Observed behavior

Some requests immediately after the update return the old display name for several seconds.

### Environment / version

- Node.js API;
- PostgreSQL;
- one primary database and one read replica;
- application version `2.4.0`.

### Evidence

Relevant code/config summary supplied with the incident:

```text
POST /profile writes to DB_PRIMARY.
GET /profile reads from DB_REPLICA.
Replica monitoring shows replay delay between 0–5 seconds during the incident window.
No application error is returned by POST or GET.
```

### Reproduction information

Intermittent. Most visible when GET is called immediately after POST.

### Recent changes

Profile reads were moved from primary to replica in version `2.4.0`.

### Impact

Users sometimes see stale profile data immediately after saving.

---

## Illustrative expected result shape

### 1. Diagnostic state

`DIAGNOSE_FIRST`

### 2. Current diagnosis

The strongest current hypothesis is read-after-write inconsistency caused by reading the profile from a replica that can lag the primary. The supplied evidence supports this mechanism strongly, but it does not yet prove that the stale responses observed in the affected requests came from a lagging replica at that exact moment. Root cause is not yet confirmed.

### 3. Observation ledger

| Observation | Evidence source | State | Consequence |
|---|---|---|---|
| POST writes to primary | supplied code/config summary | OBSERVED | write is committed on primary path |
| GET reads from replica | supplied code/config summary | OBSERVED | immediate read can observe replica state |
| replica delay reaches 0–5s | supplied monitoring summary | OBSERVED | temporary staleness is technically possible |
| symptom is strongest immediately after write | reproduction description | OBSERVED | timing is consistent with replica lag |
| replica lag caused the exact stale requests | not directly traced | UNKNOWN | mechanism remains unconfirmed |

### 4. Failure boundary

- Last known good: before profile reads moved to replica, based on supplied recent-change context.
- First known bad: version `2.4.0`, if the supplied incident history is complete.
- Affected path: immediate read after profile update.
- Deterministic/intermittent: intermittent.
- Relevant change boundary: profile GET moved from primary to replica.

### 5. Ranked hypotheses

| Rank | Hypothesis | Evidence for | Evidence against | Assumptions / unknowns | Confidence |
|---|---|---|---|---|---|
| 1 | Replica lag causes stale read-after-write responses | GET uses replica; measured lag; timing matches; change introduced replica reads | no request-level trace tying an affected GET to replica replay position | affected requests actually reached a lagging replica | high |
| 2 | Application cache returns stale profile | stale-read symptom could match caching | no cache evidence supplied; change boundary points to replica routing | whether any profile cache exists | low |
| 3 | POST returns before transaction is durable/visible | could produce immediate stale reads | POST writes primary and no transaction evidence suggests failure | exact transaction/commit behavior | low |

### 6. Next diagnostic checks

**Check 1 — Compare immediate primary vs replica reads for the same profile**

- Hypotheses tested: 1 vs alternatives.
- Action: in a safe test/staging environment, update a profile and immediately read the same row from primary and replica while recording timestamps/replay position.
- If hypothesis 1 is true: primary should show the new value while the replica may temporarily show the old value during lag.
- If false: both should show the same state while the application still reproduces staleness.
- Information value: `high`
- Reversibility: high.
- Production risk: low in test/staging; production diagnostics should remain read-only.

**Check 2 — Add request-level read-source/replay metadata temporarily**

- Hypotheses tested: 1.
- Action: capture which read target served an affected request and relevant replica-delay metadata without changing data.
- If hypothesis 1 is true: stale responses should correlate with a replica behind the relevant write.
- If false: stale responses occur without corresponding lag.
- Information value: `high`
- Reversibility: high.
- Production risk: low if implemented as bounded observability.

### 7. Action recommendation

`DIAGNOSTIC`

Run the read-source / primary-vs-replica checks before claiming the cause is confirmed. If immediate consistency is a required product invariant and impact is material, a human may separately consider a temporary mitigation such as routing the post-write read to primary; that mitigation should not be described as causal proof by itself.

### 8. Verification plan

If replica lag is confirmed and a durable consistency strategy is implemented:

1. reproduce the original immediate POST→GET sequence;
2. verify the returned profile is current under the relevant consistency policy;
3. run a regression case during induced/bounded replica delay in a safe environment;
4. monitor stale-read indicators after rollout;
5. verify fallback/rollback behavior if the routing strategy changes.

### 9. Remaining material unknowns

- whether affected GET requests were served by a lagging replica at the exact failure moment;
- whether another cache exists in the profile read path;
- the exact consistency guarantee required by the product.

---

## Why this example matters

The workflow does **not** jump from “replica lag looks plausible” to `CAUSE_CONFIRMED`.

It preserves:

```text
OBSERVATION
→ HYPOTHESIS
→ DISCRIMINATING CHECK
→ ACTION CLASS
→ VERIFICATION
```

and keeps mitigation separate from causal proof.

Again: this file is a **synthetic worked example**, not behavioral evidence for the Starter workflow.
