# Prompt Quarry — Developer Pack v1.1

Version: `1.1.0`

Static maturity: `VALID`

Developer Pack v1.1 is the reusable system behind Prompt Quarry's field-ready developer prompts.

The Free Developer Starter Pack gives you three finished workflows. Developer Pack gives you the construction and governance layer for building, adapting, reviewing, and integrating many workflows of your own.

## What is included

### Reusable systems

- `templates/general-operating-contract.md` — domain-neutral workflow construction contract.
- `templates/software-code-review-system.md` — configurable code-review policy and operating system.
- `templates/bug-diagnosis-system.md` — configurable diagnosis/incident workflow with evidence and safety thresholds.
- `templates/technical-research-decision-system.md` — configurable architecture/research/decision workflow.

### Machine-readable contracts

- `contracts/workflow-contract.schema.json` — JSON Schema for governed workflow contracts.
- `contracts/code-review-policy.example.json` — concrete code-review policy instance.

### Adaptation and inspection

- `methodology/adaptation-playbook.md` — how to turn reusable policy into a team workflow without collapsing evidence semantics.
- `checklists/workflow-static-review.md` — static contract inspection before runtime evaluation.

### Worked transformations

- `examples/code-review-policy-transformation.md`
- `examples/technical-decision-policy-transformation.md`

### Getting started and license

- `QUICKSTART.md`
- `LICENSE.md`

## Recommended path

```text
1. Pick a reusable system
2. Identify the consuming workflow
3. Configure policy vs per-run inputs
4. Define evidence and decision semantics
5. Bind a stable output contract
6. Run the static review checklist
7. Test the configured workflow on real cases
8. Record runtime evidence separately
```

Start with `QUICKSTART.md`.

## Free vs Paid boundary

```text
FREE
three strong finished workflows

PAID
reusable operating architecture
+ parameterized policy
+ machine-readable contracts
+ adaptation method
+ verification contracts
+ team/application integration
+ worked transformations
```

The value is not extra wording or prompt count. It is the ability to define and preserve workflow semantics across repeated engineering work.

## License

You may use and adapt the Pack for authorized work, applications, workflows, products, and services under `LICENSE.md`.

Resale, redistribution, sublicensing, mirroring, and competing prompt-pack reconstruction are not granted.

## Evidence boundary

`VALID` means the included assets passed Prompt Quarry's static product and contract review for this release candidate.

It does **not** mean the workflows are behaviorally proven.

```text
F4 TESTED        NO
F5 IMPROVED      NO
F6 CERTIFIED     NO
F7 PORTABLE      NO
```

`not observed == unknown`

Runtime and comparative claims require separate governed evidence.
