# Start Here — Developer Workflow Collection v1.2 Candidate

Status: `CUSTOMER JOURNEY DESIGN / NOT A RELEASE ASSET / NOT FOR SALE`

This file defines the experience the final `START_HERE.md` must provide. It deliberately exposes incomplete pieces so the candidate cannot be mistaken for a finished customer archive.

## You do not need to read the whole collection

Start with the task you have **right now**.

| I need to... | Open this workflow | Skill candidate | Customer prompt surface |
|---|---|---|---|
| review a PR, diff, file, or change | **Code Review** | `skills/review-code-with-evidence/SKILL.md` | `PENDING_GOVERNED_V1_2_SURFACE` |
| diagnose a bug, regression, incident, or strange behavior | **Bug Diagnosis** | `skills/diagnose-bugs-with-evidence/SKILL.md` | `PENDING_GOVERNED_V1_2_SURFACE` |
| compare technical options or make an architecture/tooling decision | **Technical Decision** | `skills/make-technical-decisions/SKILL.md` | `PENDING_GOVERNED_V1_2_SURFACE` |
| turn a repeated AI-assisted task into a reusable workflow | **AI Workflow Design** | `skills/design-ai-workflows/SKILL.md` | `prompts/general-operating-contract-v1.2.md` |

**Release blocker:** the three `PENDING_GOVERNED_V1_2_SURFACE` entries must be replaced by versioned customer prompt files before final packaging. Do not ship this candidate file to customers.

---

## 5-minute path

### 1. Pick one task

Do not install everything first. Do not read every methodology file. Pick the row above that matches the task you are doing.

### 2. Choose your surface

**Use the prompt surface when:**

- you want copy/paste portability;
- your AI host does not support installable skills;
- you want to inspect the entire operating contract before using it.

**Use the skill surface when:**

- your declared host supports the skill format;
- you want the workflow to be discoverable/invokable by the host;
- that host has actually earned a support claim in the collection evidence.

Structure compatibility is not the same as behavioral support. If a host is not listed as tested, treat it as `NOT_CERTIFIED`.

### 3. Bring only the inputs that matter

Each workflow begins by identifying required inputs and material unknowns.

Do not paste secrets, credentials, private customer data, or regulated information merely because an AI workflow can accept text. Follow the data-handling rules of your organization and AI provider.

### 4. Run the workflow

The workflow should make these parts explicit where they matter:

```text
INPUT
  ↓
EVIDENCE / CONTEXT
  ↓
PROCESS
  ↓
DECISION OR RESULT
  ↓
UNKNOWN / FALLBACK
  ↓
VERIFICATION
```

The value is repeatability: the important operating rules should not depend on remembering the wording of yesterday's chat.

### 5. Verify before acting

Do not treat an AI answer as correct because it is fluent.

Check:

- What evidence supports the material claims?
- Which statements are inferred rather than observed?
- Are important unknowns visible?
- Does the result follow the workflow's output/decision contract?
- What real test, source, measurement, or human review should happen next?

---

# Choose your workflow

## A. Code Review

**Use when:** you have an actual software change to inspect.

Bring:

- code, diff, PR, or changed files;
- intended change / acceptance criteria;
- enough runtime/language context to interpret the change.

Expect:

- review state;
- evidence-ranked findings;
- severity and failure mechanism;
- missing context only when material;
- verification plan;
- ship recommendation within the declared authority boundary.

Do **not** use it as a bug diagnosis workflow when the main task is explaining an observed failure with competing causes.

Current skill candidate:

`skills/review-code-with-evidence/SKILL.md`

Customer prompt surface:

`PENDING_GOVERNED_V1_2_SURFACE`

---

## B. Bug Diagnosis

**Use when:** something is failing and you need to separate observations from hypotheses before choosing the next check or fix.

Bring where available:

- expected behavior;
- observed behavior;
- reproduction information;
- environment/version;
- logs/errors/code/metrics relevant to the failure.

Expect:

- diagnostic state;
- observation ledger;
- ranked hypotheses;
- discriminating checks;
- mitigation/fix classification;
- verification plan;
- unresolved material unknowns.

A plausible cause is not a confirmed root cause without the required evidence.

Current skill candidate:

`skills/diagnose-bugs-with-evidence/SKILL.md`

Customer prompt surface:

`PENDING_GOVERNED_V1_2_SURFACE`

---

## C. Technical Decision

**Use when:** you must choose between technologies, architectures, vendors, dependencies, migrations, build-vs-buy options, or implementation approaches.

Bring:

- the decision;
- candidate options;
- hard constraints;
- decision criteria;
- available evidence;
- deadline/reversibility context.

Expect:

- decision state;
- constraint check;
- option comparison;
- evidence and assumptions;
- recommendation when justified;
- reversal triggers;
- highest-value next validation action.

A popular option does not override a hard constraint.

Current skill candidate:

`skills/make-technical-decisions/SKILL.md`

Customer prompt surface:

`PENDING_GOVERNED_V1_2_SURFACE`

---

## D. AI Workflow Design

**Use when:** you repeatedly explain the same task to an AI and want to turn that repeated setup into an explicit operating contract.

Bring:

- recurring task/outcome;
- required inputs;
- important constraints;
- evidence/authority boundaries;
- desired output;
- failure/fallback behavior.

Expect a workflow contract that makes intake, evidence, execution, decision states, output, verification, and fallback semantics inspectable.

Current skill candidate:

`skills/design-ai-workflows/SKILL.md`

Current prompt surface:

`prompts/general-operating-contract-v1.2.md`

---

# Evidence legend

The final collection should use compact customer language:

| Label | What it is allowed to mean |
|---|---|
| `VERSIONED` | exact artifact/version is identifiable |
| `STRUCTURE CHECKED` | static/structural contract checks passed |
| `RUNTIME TESTED` | real execution evidence exists for the named runtime |
| `IMPROVED` | a versioned change has comparative evidence against its baseline |
| `CERTIFIED` | all required certification gates for the named scope passed |
| `KNOWN LIMITATIONS` | explicit unsupported or unresolved boundaries |

Never infer a stronger label from a weaker one.

Current collection-wide boundary:

```text
SKILL STRUCTURE       PASS
REAL PCP-04 EXECUTION INCOMPLETE
SKILL HOST TESTING    INCOMPLETE
PROMPT/SKILL PARITY   INCOMPLETE
FINAL ARCHIVE         NOT BUILT
PUBLIC SALE           OFF
```

---

# What should be in the final customer archive

Target root:

```text
prompt-machine-developer-workflow-collection-v1.2.0/
├── START_HERE.md
├── LICENSE.md
├── workflows/
│   ├── code-review/
│   │   ├── PROMPT.md
│   │   ├── EXAMPLE.md
│   │   └── EVIDENCE.md
│   ├── bug-diagnosis/
│   │   ├── PROMPT.md
│   │   ├── EXAMPLE.md
│   │   └── EVIDENCE.md
│   ├── technical-decision/
│   │   ├── PROMPT.md
│   │   ├── EXAMPLE.md
│   │   └── EVIDENCE.md
│   └── ai-workflow-design/
│       ├── PROMPT.md
│       ├── EXAMPLE.md
│       └── EVIDENCE.md
├── skills/
│   ├── review-code-with-evidence/
│   ├── diagnose-bugs-with-evidence/
│   ├── make-technical-decisions/
│   └── design-ai-workflows/
├── guides/
│   ├── INSTALL_SKILLS.md
│   ├── ADAPT_A_WORKFLOW.md
│   └── EVIDENCE_AND_LIMITS.md
└── MANIFEST.json
```

This layout is a target. It is not evidence that those release files already exist.

---

# Release condition for this entry point

Create the final `START_HERE.md` only when:

- all four customer prompt surfaces exist;
- every path in the chooser resolves inside the final package;
- examples exist;
- evidence cards exist;
- install guidance is scoped to hosts with support evidence;
- no `PENDING_*` marker remains;
- the archive root and manifest are frozen;
- product value review confirms that a new buyer can identify a useful first action without repository knowledge.

Until then:

`START_HERE.candidate.md != RELEASE_READY`
