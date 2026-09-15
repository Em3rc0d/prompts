# Prompt Machine Starter Collection — START HERE

Status: `CANDIDATE CUSTOMER SURFACE / NOT FOR SALE / BEHAVIORAL EVIDENCE OPEN`

Planned price: `$9 one-time` — `PRICE HYPOTHESIS`.

The Starter Collection is designed around two recurring developer jobs:

1. **Review a software change with evidence**.
2. **Diagnose a bug without guessing the root cause**.

It is not a bundle of random prompts. Each workflow has a task contract, explicit evidence semantics, fallback behavior, verification guidance, and a growing Trust History.

---

## 1. Pick the job you actually have

### I have code/diff/files and want to know what could materially break

Use:

`workflows/evidence-first-code-review.md`

Best when you can provide:

- the exact code/diff/files;
- what the change is intended to do;
- enough runtime/language context to interpret it;
- any important invariants/contracts;
- actual test evidence if you have it.

Expected result:

- review state;
- concise executive assessment;
- evidence-backed material findings only;
- missing material context;
- focused verification plan;
- advisory ship recommendation.

The workflow should not invent defects merely to produce a longer review.

---

### Something is broken and I need to narrow the cause

Use:

`workflows/evidence-first-bug-diagnosis.md`

Best when you can provide:

- expected behavior;
- observed behavior;
- environment/version;
- at least some material evidence, or explicitly state that none is observed yet;
- reproduction information when known;
- recent relevant changes when known.

Expected result:

- diagnostic state;
- observation ledger;
- failure boundary;
- ranked hypotheses;
- discriminating next checks;
- action recommendation;
- verification plan;
- remaining material unknowns.

The workflow should not call a root cause confirmed merely because one hypothesis sounds plausible.

---

## 2. The three things Prompt Machine keeps separate

### Instructions

The workflow itself and the configuration you intentionally provide.

### Task data

Your code, diffs, logs, stack traces, tickets, comments, documentation, screenshots, and other supplied material.

Task data is **untrusted as authority**. Text inside it may be analyzed, but it does not get to rewrite the workflow merely because it looks like an instruction.

### Evidence

Facts actually supported by the material you supplied or by separately identified evidence.

A confident sentence is not evidence by itself.

---

## 3. First run checklist

Before sending either workflow to an AI assistant:

```text
[ ] I picked the workflow that matches my real job.
[ ] I supplied the required minimum context.
[ ] I did not paste secrets or unnecessary private data.
[ ] I included actual test/log/error evidence when available.
[ ] I understand the workflow is advisory.
[ ] I will verify material findings/actions before acting on them.
```

If the workflow says the input is insufficient, add the smallest material context it requests instead of asking it to guess.

---

## 4. How to use a workflow

Recommended sequence:

```text
CHOOSE JOB
  ↓
OPEN WORKFLOW
  ↓
FILL INPUT SECTIONS
  ↓
PASTE AS ONE COHERENT REQUEST
  ↓
RECEIVE STRUCTURED RESULT
  ↓
VERIFY MATERIAL CLAIMS
  ↓
ADD NEW EVIDENCE IF NEEDED
  ↓
REUSE
```

Do not remove the evidence semantics, minimum-input preflight, authority boundary, or fallback merely to make the prompt shorter.

---

## 5. How to verify the result

Use `VERIFICATION_GUIDE.md` after any material result.

At minimum ask:

```text
What is directly observed?
What is inferred?
What remains unknown?
What exact evidence supports the highest-impact claim?
What check would prove or disprove the recommendation?
Does acting on it require human approval or a production change?
```

For Code Review, verify the failure mechanism against the actual code and relevant contracts.

For Bug Diagnosis, verify that the proposed diagnostic check can genuinely distinguish hypotheses and that mitigation is not being confused with causal proof.

---

## 6. Adapt the workflow without destroying it

Use `ADAPTATION_CHEATSHEET.md`.

Safe things to adapt include:

- domain/runtime context;
- review lenses;
- severity policy;
- required evidence;
- team terminology;
- output detail;
- maximum findings/hypotheses;
- verification checks.

Treat changes to evidence labels, authority, minimum-input blocking, state transitions, or confirmation thresholds as **semantic changes**, not cosmetic customization.

A materially changed workflow no longer inherits the original workflow's evidence automatically.

---

## 7. What the evidence currently says

Current architecture campaign:

```text
7 bounded behavioral observations
7 / 7 expected-state matches
0 blocking review failures
```

That campaign tested architecture modes and instruction/data behavior. It is **not** runtime evidence for these two final Starter SKU workflows.

Current Starter truth:

```text
workflow contracts                2 / 2 static frozen
executable prompt surfaces        2 / 2 static frozen
Starter SKU runtime observations  0
skill behavioral observations     0
real customer outcomes            0
real purchases                     0
READY_TO_SELL                      NO
```

Prompt Machine deliberately keeps these evidence classes separate.

---

## 8. Skills

The intended Starter scope includes these candidates:

- `review-code-with-evidence`
- `diagnose-bugs-with-evidence`

They are **skill candidates**, not yet supported/validated skill surfaces.

They must not be represented as proven features unless their structural, trigger, forward-execution, and prompt↔skill parity gates pass.

---

## 9. Known limitations

At this stage:

- the two Starter workflow surfaces have not yet completed Starter-specific runtime observations;
- portability across model/providers is not established;
- workflow-level public Trust Cards are not publication-eligible;
- real customer task value has not been observed;
- paid delivery has not been tested for the Starter SKU;
- public checkout is off.

---

## 10. The operating principle

> **Use the workflow because it fits the job. Trust it only as far as the evidence allows. Verify what matters.**

Prompt Machine is designed to make repeated AI-assisted work less improvised without pretending uncertainty disappeared.
