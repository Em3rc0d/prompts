# PCP Static Quality Rubric v1 — P1–P15

Status: `FROZEN FOR PCP-02`

This rubric defines the pre-behavioral static audit used by the Prompt Quarry
Certification Program. It does not replace the existing MK1 certification rubric.

## Reconciliation decision

The working certification plan named P1–P15 but did not define every criterion.
The repository already had two authoritative inputs:

- `mk1/rubrics/PROMPT_QUALITY_RUBRIC.md` at blob
  `fe5f4239a87f43c206626122a3053ebdcc166e92` — eight artifact-quality
  dimensions and blocking failures;
- `product/developer-pack-v1.1/quality/COMMERCIAL_VALUE_GATE.md` at blob
  `8f3aa83bb9708b27b621156edb6c4928653051cf` — differentiation,
  reuse, documentation, pack, and commercial-value requirements.

P1–P15 is therefore a repository-authored static preflight that composes those
existing contracts. It is not represented as a recovered historical rubric.

## Status semantics

- `PASS` — the frozen source satisfies the criterion on static inspection.
- `WARN` — usable, but a specific ambiguity, inefficiency, or weakness should
  become a fixture or improvement candidate.
- `FAIL` — a blocking static defect exists. Certification cannot proceed for the
  artifact until a versioned change resolves it.
- `NOT_APPLICABLE` — the criterion cannot reasonably apply; rationale is
  mandatory and the status never counts as a pass.

`STATIC_AUDIT_COMPLETE = PASS` means every required rating and rationale exists.
It does not mean every prompt passed, and it does not establish F4–F7.

## Criteria

| ID | Criterion | Static question |
|---|---|---|
| P1 | Purpose / Task Fit | Is the intended job and outcome explicit and aligned with the declared spec? |
| P2 | Clarity | Can the target user understand the instructions, variables, states, and terms without material ambiguity? |
| P3 | Structure / Instruction Architecture | Are sections purposeful, coherent, ordered, and free of contradictory mandatory rules? |
| P4 | Input Contract | Are required, optional, missing, contradictory, and ambiguous inputs handled explicitly? |
| P5 | Context & Evidence Design | Are allowed context, provenance, evidence classes, freshness, and material assumptions governed appropriately? |
| P6 | Output Contract | Are required outputs, fields, states, ordering, and completion semantics explicit and consumable? |
| P7 | Safety & Authority Boundary | Are unsafe, destructive, high-impact, or unauthorized actions bounded and escalated? |
| P8 | Truthfulness & Uncertainty | Does the prompt prevent fabrication and preserve fact, source claim, inference, assumption, and unknown states? |
| P9 | Robustness & Fallback | Does the prompt degrade coherently for incomplete, ambiguous, conflicting, adversarial, or unsupported inputs? |
| P10 | Efficiency & Usability | Is instruction cost proportionate to value, with low redundancy and manageable setup friction? |
| P11 | Differentiation | Does the artifact provide a distinct capability rather than cosmetic wording or a near-duplicate? |
| P12 | Documentation | Can a user understand when, how, and with what evidence limits to use the artifact? |
| P13 | Reusability & Adaptability | Can the artifact be reused or deliberately adapted without silently changing its operating semantics? |
| P14 | Pack Fit | Does the artifact have a clear role, progression, and boundary within its Free or Paid pack? |
| P15 | Commercial Value | Does the artifact create defensible user value for its tier without relying on unproven behavioral claims? |

## Mapping to existing contracts

| Existing MK1 dimension | PCP criteria |
|---|---|
| Task fit | P1, P2 |
| Input / context design | P4, P5 |
| Instruction architecture | P3 |
| Constraints / truth boundary | P7, P8 |
| Output contract | P6 |
| Robustness / fallback | P9 |
| Evidence / domain discipline | P5, P8 |
| Efficiency / usability | P10 |

P11–P15 extend static inspection to the product and commercial layer; they do
not add behavioral evidence.

## Blocking rules

Any of the following forces at least one `FAIL`:

1. instructions require fabrication or provenance laundering;
2. core purpose or output contract is undefined;
3. required variables are unresolved in a finished workflow;
4. mandatory rules can produce incompatible outputs under the same state;
5. unsafe or high-impact actions exceed stated authority;
6. a Paid artifact is only a cosmetic Free clone;
7. a claim of tested, improved, certified, or portable exceeds evidence.

Any `FAIL` blocks certification for that artifact. Warnings must enter PCP-03 as
fixtures or explicit improvement hypotheses; they may not disappear silently.

## Evidence boundary

Static inspection may establish only the quality of the written contract.

```text
STATIC PASS != F4 TESTED
STATIC PASS != F5 IMPROVED
STATIC PASS != F6 CERTIFIED
STATIC PASS != F7 PORTABLE
```
