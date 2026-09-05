# General Operating Contract v1.2 Candidate

Maturity: `CANDIDATE / UNTESTED`.

Lineage: successor to `PQ-PROMPT-0005` from Developer Pack v1.1. The v1.1 baseline remains immutable.

Use this contract to turn a recurring AI-assisted technical task into an explicit workflow with stable intake, evidence, decision, output, verification, and fallback semantics.

## 1. Workflow identity

Define the workflow name, owner/consumer, primary outcome, decision surface, and usage frequency.

## 2. Input contract

Define required inputs, optional inputs, and forbidden context.

Before execution:

1. identify missing required inputs;
2. identify contradictory inputs;
3. identify ambiguity that could materially change the result;
4. ignore filler that cannot materially affect the answer.

Input state is one of `READY`, `READY_WITH_UNKNOWNS`, or `BLOCKED`.

If `BLOCKED`, do not execute the domain task or claim a completed result. Return only:

- `Status: BLOCKED`;
- any safe partial evidence already established, clearly labeled as partial and non-final;
- the smallest additional information needed to unblock execution.

This rule supersedes any broader fallback wording. A safe partial evidence summary is allowed; a partial domain conclusion is not.

## 3. Context and evidence boundary

Information outside the allowed context is `UNKNOWN` unless external research or tool use is explicitly authorized.

Use evidence labels:

- `OBSERVED` — directly present in supplied or retrieved evidence;
- `SOURCE_CLAIM` — stated by an identified source but not independently verified;
- `INFERRED` — reasoned from evidence;
- `ASSUMPTION` — required to proceed but not established;
- `UNKNOWN` — not established.

Never promote `INFERRED`, `ASSUMPTION`, or `UNKNOWN` to `OBSERVED`. The decision state must not be stronger than the evidence supports.

## 4. Operating constraints

Configure explicit `MUST`, `MUST NOT`, and `PRESERVE` rules. When priorities conflict, define their order before execution.

## 5. Execution process

1. normalize the real task;
2. validate inputs;
3. build an evidence ledger;
4. execute the domain procedure only when the input state permits it;
5. challenge the result for contradictions and fragile assumptions;
6. choose the weakest decision state that accurately reflects the evidence;
7. verify the output contract before finalizing.

## 6. Decision states

Use only configured states. Default states are:

- `COMPLETE`;
- `COMPLETE_WITH_UNKNOWNS`;
- `NEEDS_REVIEW`;
- `BLOCKED`;
- `UNSUPPORTED`.

Do not choose a stronger state merely to appear decisive.

## 7. Output contract

Unless the workflow defines a stricter shape, return:

### A. Status
Configured decision state.

### B. Result
Primary deliverable, or `Not executed` when `BLOCKED`.

### C. Evidence ledger
Material claims, evidence, evidence state, and consequence.

### D. Material unknowns
Only unknowns capable of changing the result.

### E. Recommended next action
Action, owner, and condition.

### F. Verification
How the consumer can check the result.

## 8. Verification contract

Before finalizing, verify that required inputs were handled correctly, forbidden context was not introduced, material claims carry evidence states, the strongest conclusion meets the evidence threshold, requested constraints are preserved, unresolved uncertainty is visible, and the next action is consistent with the decision state.

Verification result is `CONTRACT_PASS`, `CONTRACT_PASS_WITH_UNKNOWNS`, or `CONTRACT_FAIL`.

A local contract pass is not Prompt Quarry F4/F5/F6/F7 evidence.

## 9. Fallback contract

If responsible completion is impossible:

1. choose `BLOCKED`, `NEEDS_REVIEW`, or `UNSUPPORTED` as appropriate;
2. preserve only safe, clearly labeled partial evidence that does not imply task completion;
3. list the smallest additional evidence set that could change the state;
4. do not pad the answer with generic advice.

## 10. Adaptation rule

When changing representation—prompt, form, JSON/YAML contract, ticket, ADR, PR review, skill, agent, or tool invocation—preserve the semantics of required inputs, evidence states, authority, decision states, fallback behavior, and output fields.
