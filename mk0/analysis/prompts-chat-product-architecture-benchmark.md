# prompts.chat Product Architecture Benchmark

Status: `MK0_DERIVED_ANALYSIS`

Snapshot basis: `f/prompts.chat@f78a1c5136fa080155d928e0d7e2b4a41ddef03e`

Date: `2026-09-15`

This document compares observed `prompts.chat` architecture with the current Prompt Machine / Prompt Quarry / Verlune system. It is a design benchmark, not a product-quality ranking.

## 1. System roles are different

Observed upstream role:

```text
prompts.chat
public prompt library + contribution platform + integrations + self-hosting
```

Current repository role:

```text
CUSTOMER BRAND     Verlune
FIRST PRODUCT      Verlune Code Review
PRODUCT ENGINE     Prompt Machine
EVIDENCE FACTORY   Prompt Quarry
```

The main lesson is therefore **not** "turn Prompt Machine into prompts.chat". The useful question is which library/distribution patterns improve our evidence-backed workflow system without weakening the certification boundary.

## 2. Comparative matrix

| Dimension | prompts.chat — observed | Prompt Machine / Prompt Quarry — current | Decision |
|---|---|---|---|
| Primary public unit | Prompt records | Workflow/product artifact | Keep workflow as primary customer-value unit |
| Artifact types | Text, image, video, audio, structured, skill, taste | Prompts, skills, workflow packages, evidence artifacts | Preserve explicit artifact types; consider richer registry metadata |
| Versioning | `PromptVersion` with numeric version/change note | Git history + contract versions + hashes + release evidence | Add user-facing semantic version/change history later; do not replace immutable evidence hashes |
| Change contribution | First-class `ChangeRequest` | Engineering changes through repo/PR/evidence gates | Borrow reviewed-change-request concept for community/user proposals only after product demand |
| Discovery | Categories, tags, featured state, model hints | Outcome-oriented collections + internal taxonomy | Keep outcome-first merchandising; add tags/model hints only as secondary metadata |
| Relationships | Prompt connections + workflow link | Workflow composition exists mostly in engineered artifacts/docs | Evaluate explicit workflow graph relations in a future registry |
| Collections | Per-user prompt collection model | Product collections/packages | Distinguish personal saved collections from paid product collections if added |
| Distribution | Web, CSV/Markdown, CLI, Claude Code plugin, MCP | Web/ZIP/provider delivery + skills | Strong candidate: evaluate MCP/CLI/plugin delivery after exact artifact identity can be preserved |
| Self-hosting | Documented | Not current launch requirement | Defer; potentially useful organization/enterprise lane |
| White-label | Configurable branding/theme/auth/features | Verlune fixed customer brand; internal engines separate | Do not white-label first release; architecture pattern may matter later |
| Auth/private library | Session/API key, private prompts | Product/release flows; internal repo evidence | Relevant only if Prompt Machine becomes persistent user workspace |
| Moderation | Reports, delisting, comments, roles | Certification/evidence review, not community moderation | Separate community moderation from evidence certification if contribution opens later |
| AI improvement | Authenticated improvement API exists | Prompt Quarry engineering + evaluated promotion pipeline | Never equate generation with improvement; keep evidence gates |
| Governance | Maintainers + project lead + lazy consensus | Repository owner + explicit gates/approvals | Existing gate model is stronger for certification; governance docs can be formalized separately |
| Licensing | MIT code/site content + CC0 prompt data per README | Source-specific provenance and customer package licensing | Preserve source-by-source license metadata; never flatten licenses during mining |

## 3. Patterns worth adopting now

### A. First-class source-family registration

This integration itself adopts the pattern indirectly: external systems should have a durable source identity, exact source revision and explicit claim boundary.

Required state:

```text
source family
+ exact revision
+ observed surfaces
+ derived analysis
+ promotion boundary
```

This is compatible with MK0 and improves reproducibility.

### B. Rich artifact metadata without weakening evidence

Useful metadata candidates for future Prompt Machine registry surfaces:

- artifact type;
- semantic version;
- task/outcome category;
- tags;
- declared target model/runtime;
- compatible execution surfaces;
- parent/next workflow relationships;
- known limitations;
- evidence state;
- exact immutable fingerprint.

The last two are where Prompt Quarry should remain stricter than a conventional prompt library.

### C. Distribution close to the user's work surface

The source's CLI/MCP/plugin lanes reinforce a product hypothesis already compatible with Prompt Machine:

> a reliable workflow is more valuable when users can invoke it where they already work.

Candidate future lane:

```text
certified/versioned artifact
        ↓
Prompt Machine registry
        ↓
web | CLI | MCP | supported plugin/skill surface
        ↓
exact version + provenance retained
```

No such lane should ship until artifact identity and version pinning remain observable across the adapter.

### D. Explicit version/change history for customer comprehension

Prompt Quarry already has stronger low-level provenance through hashes, receipts and Git history. What is missing is a simple customer-facing projection such as:

```text
1.0.0  initial release
1.0.1  packaging/copy-only correction
1.1.0  behaviorally changed workflow — recertification required
```

This can coexist with immutable technical receipts.

## 4. Patterns to evaluate later

### A. User change requests

Potentially useful after real usage exists. A user proposal should never directly mutate a certified workflow.

Safer design:

```text
user suggestion
   ↓
CHANGE_REQUEST / feedback object
   ↓
triage
   ↓
new candidate branch/version
   ↓
MK1 + certification gates
   ↓
new release if earned
```

### B. Workflow graph

The upstream `PromptConnection` model suggests a durable graph instead of hiding sequencing inside prose.

Possible future Prompt Machine relation types:

```text
PRECEDES
FOLLOWS
REQUIRES
ALTERNATIVE_TO
VALIDATES
REFINES
```

This should be designed only when multiple workflow families create real orchestration demand.

### C. Personal/private library

Private prompts, pinned prompts and user collections are useful patterns for a SaaS workspace, but they are not required to sell or deliver Verlune Code Review. Building them now would expand scope before `PQ-$1`/real demand.

### D. Self-hosting / white-label

Potential later B2B path. It should remain deferred until there is observed organizational demand and a clear support/security model.

## 5. Patterns we should deliberately NOT copy

### A. Catalog size as value proof

Prompt Quarry's invariant remains:

```text
quantity != quality
popularity != behavior evidence
```

Large prompt inventory is useful for discovery/mining, but Verlune's differentiator should remain evidence-backed task completion.

### B. AI-generated "improvement" without measured superiority

An improvement endpoint is a product feature, not proof of improvement.

Prompt Quarry keeps the stricter ladder:

```text
generated
  != VALID
  != TESTED
  != IMPROVED
  != CERTIFIED
  != PORTABLE
```

### C. Model hints as portability proof

`bestWithModels` is useful metadata. It is not equivalent to our F7 portability evidence.

### D. Community moderation as certification

Votes, comments and reports can improve discovery/trust, but they cannot replace behavioral fixtures, blinded comparison, exact runtime identity or certification receipts.

## 6. Concrete product implications

### Near-term — Verlune Code Review

No scope expansion is required because of this benchmark.

Keep current commercial truth:

```text
PRODUCT_READY       NO
READY_TO_SELL       NO
PUBLIC_CHECKOUT     OFF
```

The source benchmark does not change G11/G12/G13/G14 status.

### Prompt Machine platform

After the first commercial proof, prioritize evaluation in this order:

1. customer-facing version history projected from immutable release evidence;
2. artifact registry metadata and exact-version addressing;
3. CLI/MCP adapter spike with fingerprint/version preservation;
4. workflow-relationship graph only when orchestration demand appears;
5. contribution/change-request layer only after recurring usage;
6. private/self-hosted/white-label capabilities only after organizational demand.

### Prompt Quarry

Prompt Quarry should remain stricter than the benchmark source in these areas:

- source provenance;
- truth boundaries;
- immutable fingerprints;
- runtime receipts;
- measured improvement;
- certification state;
- portability state.

## 7. Decision summary

```text
ADOPT NOW
- exact source snapshot registration
- richer registry metadata design
- customer-readable version projection concept

EVALUATE AFTER FIRST COMMERCIAL PROOF
- CLI/MCP/plugin delivery
- workflow graph
- reviewed user change requests

DEFER
- self-hosting
- white-label
- social/community platform expansion

DO NOT COPY AS TRUST SIGNALS
- catalog size
- popularity
- AI-generated improvement labels
- model hints without runtime evidence
```

The benchmark strengthens Prompt Machine by showing where a mature prompt library is operationally richer, while preserving Prompt Quarry's core advantage: **claims remain bounded by observed evidence**.
