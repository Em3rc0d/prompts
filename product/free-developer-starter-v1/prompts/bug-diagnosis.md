# Bug Diagnosis — Starter Prompt

Use this when you need to identify a root cause without jumping from the first symptom to the first plausible fix.

## INCIDENT / DEFECT CONTEXT

Expected behavior:

[WHAT SHOULD HAPPEN]

Observed behavior:

[WHAT ACTUALLY HAPPENS]

Reproduction steps:

[KNOWN STEPS / INTERMITTENT / NOT YET REPRODUCED]

Environment:

[APP VERSION / LANGUAGE / FRAMEWORK / OS / CLOUD / DATABASE / BROWSER / OTHER]

Evidence:

[ERRORS / LOGS / STACK TRACES / METRICS / RELEVANT CODE / SCREENSHOTS / REQUEST IDS]

Recent changes:

[DEPLOYMENTS / CONFIG / DEPENDENCIES / DATA / INFRASTRUCTURE / NONE KNOWN]

Impact:

[WHO / WHAT IS AFFECTED AND HOW SEVERELY]

## TASK

Diagnose the defect using the supplied evidence.

Build a small, ranked hypothesis set. Prefer diagnostic actions that distinguish between hypotheses before recommending broad code changes.

Do not call a root cause confirmed until the available evidence establishes it.

## EVIDENCE LABELS

Use:

- `OBSERVED` — directly present in supplied evidence.
- `INFERRED` — logically suggested by observations.
- `UNKNOWN` — not established.
- `DISPROVED` — contradicted by supplied evidence.

Never rewrite `INFERRED` or `UNKNOWN` as `OBSERVED`.

## DIAGNOSTIC PROCESS

1. **Create an observation ledger**
   List only facts directly supported by the supplied material.

2. **Define the failure boundary**
   Identify:
   - last known good point;
   - first known bad point;
   - affected path/component;
   - whether the problem is deterministic or intermittent, if known.

3. **Generate hypotheses**
   Produce at most 5 plausible causes.
   For each hypothesis state:
   - mechanism;
   - evidence for;
   - evidence against;
   - what is still unknown.

4. **Rank by evidence, not familiarity**
   Prefer hypotheses that explain more observations with fewer unsupported assumptions.

5. **Design discriminating checks**
   For each leading hypothesis propose a reversible diagnostic check.
   Prioritize checks that can rule in/out multiple hypotheses cheaply.

6. **Update the diagnosis**
   State which hypothesis is currently strongest and why.
   If no hypothesis is sufficiently supported, say so.

7. **Recommend a fix only when justified**
   Separate:
   - diagnostic action;
   - containment/mitigation;
   - durable fix.

8. **Define verification**
   Explain how to prove the defect is resolved and how to detect regression.

## RULES

- Do not invent logs, runtime behavior, versions, configuration, reproduction results, or infrastructure state.
- Do not assume correlation proves causation.
- Do not recommend destructive changes when a reversible diagnostic step can provide the needed evidence.
- Preserve production safety: flag actions that may alter data, availability, or security posture.
- If a recent change is suspicious, explain the causal mechanism instead of treating timing alone as proof.
- If multiple defects could explain the observations, keep them separate.
- If evidence is insufficient, ask only for information with clear diagnostic value.

## OUTPUT CONTRACT

### 1. Current diagnosis
2–5 sentences summarizing:
- observed failure;
- strongest hypothesis;
- diagnosis confidence.

### 2. Observation ledger
| Observation | Evidence source | Status |
|---|---|---|
| ... | ... | OBSERVED |

### 3. Ranked hypotheses
| Rank | Hypothesis | Evidence for | Evidence against | Confidence |
|---|---|---|---|---|
| 1 | ... | ... | ... | high / medium / low |

### 4. Next diagnostic checks
For each check:
- action;
- hypothesis it tests;
- expected result if true;
- expected result if false;
- risk / reversibility;
- information value: `high | medium | low`.

### 5. Fix recommendation
Use one status:
- `DIAGNOSE_FIRST`
- `MITIGATE_NOW`
- `FIX_SUPPORTED`

Then describe the smallest justified action.

### 6. Verification plan
Include:
- reproduction check;
- targeted test;
- regression check;
- relevant monitoring/log confirmation.

### 7. Remaining unknowns
List only unknowns that can still change the diagnosis or fix.

## FALLBACK

If the supplied evidence does not support a responsible root-cause recommendation, return `DIAGNOSE_FIRST`.

Do not guess. Identify the smallest additional evidence set that would most reduce uncertainty.
