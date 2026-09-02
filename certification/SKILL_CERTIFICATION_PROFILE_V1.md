# Prompt Quarry Skill Certification Profile v1

Status: `ACTIVE / STRUCTURE PASS / HOST TESTING NEXT / NO SKILL CERTIFIED`

This profile extends the Prompt Certification Program to installable skills.
It adds skill-specific evidence; it does not promote the maturity of any source
prompt.

## Identity contract

Every candidate records:

```text
skill_id
name
version
workflow_id
prompt_lineage[]
source_files[]
source_fingerprint
target_hosts[]
license
```

Names use lowercase letters, digits, and hyphens, remain under 64 characters,
and describe a recognizable action.

## Structural gates

| Gate | Requirement |
|---|---|
| S1 Anatomy | One skill folder with required `SKILL.md`; no irrelevant files |
| S2 Frontmatter | Valid `name` and discriminating `description` |
| S3 Discovery | Description states the real trigger and avoids catchall scope |
| S4 Instructions | Core workflow preserves purpose, authority, evidence, output, and fallback |
| S5 Progressive disclosure | Conditional detail lives in linked references and is loaded only when relevant |
| S6 Resource integrity | Every referenced resource exists; every script and asset has a concrete role |
| S7 Script safety | Scripts are deterministic where required, validated, and do not expand authority |
| S8 Provenance | Prompt lineage, license, versions, and fingerprints are recorded |

Passing S1–S8 establishes only:

`STRUCTURALLY_VALID`

## Behavioral evaluation

### E1 — Intended trigger

The skill is selected for realistic requests that match its description.

### E2 — Non-trigger precision

The skill stays inactive for nearby but materially different requests. A broad
description that activates on unrelated work fails even if the workflow itself
is strong.

### E3 — Workflow completion

On a valid fixture, the skill obtains required inputs, follows the operating
contract, and returns the declared result.

### E4 — Missing and ambiguous information

The skill requests only material missing information or returns the configured
fallback state. It must not invent completion.

### E5 — Conflicting and adversarial input

The skill preserves higher-priority evidence, authority, safety, and output
boundaries when task material attempts to override them.

### E6 — Resource and script behavior

Conditional references load only when needed. Scripts, when present, execute
successfully on declared fixtures and fail safely on invalid input.

## Prompt/skill parity gate

For every workflow, run matched fixtures through both surfaces. The skill may
improve intake or orchestration, but it must not silently weaken:

- required inputs;
- evidence labels;
- allowed decision states;
- authority boundaries;
- material output fields;
- fallback and uncertainty behavior.

Any material difference is recorded as either an intentional versioned contract
change or a parity failure.

## Host evidence

Structural conformance does not prove that a host discovers, installs, invokes,
or executes the skill correctly.

For every claimed host record:

```text
host
host_version
model_or_runtime
installation_method
installation_result
intended_trigger_result
non_trigger_result
fixture_results
observed_at
receipt_id
```

An untested host is `NOT_CERTIFIED`, not implicitly supported.

## Maturity ladder

```text
DRAFT
  ↓
STRUCTURALLY_VALID
  ↓
HOST_TESTED
  ↓
WORKFLOW_CERTIFIED
  ↓
PORTABLE
```

- `HOST_TESTED` — installation, invocation, and declared fixtures pass on one
  named host/runtime.
- `WORKFLOW_CERTIFIED` — repeated matched prompt/skill evidence satisfies the
  workflow contract on the declared target.
- `PORTABLE` — qualifying evidence exists across every named supported host.

## Blocking failures

A candidate cannot advance when it has:

- vague or catchall discovery metadata;
- missing or invalid `SKILL.md` frontmatter;
- a referenced file that does not exist;
- an unfinished scaffold placeholder;
- a script that was not executed successfully;
- weakened truth, authority, safety, or fallback rules relative to its lineage;
- fabricated runtime, install, trigger, or portability evidence;
- a license or provenance ambiguity;
- a prompt/skill parity regression.

## Release requirements

Every released skill must have:

- a deterministic standalone ZIP with exactly one top-level folder;
- source and archive fingerprints;
- structural validation receipt;
- trigger/non-trigger eval receipt;
- independent forward-test receipt;
- host installation receipt;
- prompt/skill parity receipt;
- known-limitations and support statement.

## Current state

Deterministic structural validation is now complete against the exact v1.2
candidate files. The durable receipt is:

`certification/receipts/skill-structure.v1.json`

Observed CI evidence:

```text
workflow  Validate Workflow Kit Skills v1.2
run       33637606315
commit    ea3342ffdfa390f0bcb7582a1e1b2447057b780d
result    PASS
skills    4/4 PASS
warnings  0
trigger fixtures  32 DEFINED / UNEXECUTED
```

Current maturity remains deliberately bounded:

```text
PQ-SKILL-0001  STRUCTURALLY_VALID / HOST_TESTING_REQUIRED
PQ-SKILL-0002  STRUCTURALLY_VALID / HOST_TESTING_REQUIRED
PQ-SKILL-0003  STRUCTURALLY_VALID / HOST_TESTING_REQUIRED
PQ-SKILL-0004  STRUCTURALLY_VALID / HOST_TESTING_REQUIRED

SKILL_STRUCTURE_PASS      YES
SKILL_TRIGGER_FIXTURES    DEFINED / UNEXECUTED
SKILL_TRIGGER_EVAL_PASS   NO
SKILL_FORWARD_TEST_PASS   NO
PROMPT_SKILL_PARITY_PASS  NO
WORKFLOW_CERTIFIED        NO
PORTABLE                  NO
```

A structural PASS is not installation evidence and does not prove discovery,
execution quality, certification, portability, or sellability.
