# Source Quarry — prompts.chat

Status: `SOURCE_ARCHITECTURE_CHARACTERIZED`

Snapshot date: `2026-09-15`

Observed source revision:

```text
repository  https://github.com/f/prompts.chat
branch      main
commit      f78a1c5136fa080155d928e0d7e2b4a41ddef03e
```

## Why this source is in MK0

`prompts.chat` is useful to Prompt Quarry primarily as a **comparative product-architecture, prompt-library and distribution source**. This snapshot is not a quality endorsement, certification input by default, or permission to collapse source material into Prompt Machine/Verlune artifacts.

The source exposes several mature product surfaces that are relevant to our platform design:

- a public prompt library and browsing surface;
- structured prompt records with categories, tags, versions and contribution workflows;
- multiple prompt/media artifact types;
- collections, votes, comments, examples and prompt-to-prompt connections;
- CLI, MCP and Claude Code plugin distribution;
- self-hosting and white-label configuration;
- session/API-key authenticated AI-assisted prompt improvement;
- explicit project governance;
- separate licensing treatment for source/site content and prompt data.

These are **observed source capabilities**. They do not imply that the source's prompts are behaviorally tested, improved, certified, portable, commercially validated, or suitable for direct reuse.

## Observed source architecture

### Platform stack

At the captured revision, the repository declares:

- Next.js 16;
- React 19;
- PostgreSQL;
- Prisma;
- NextAuth/Auth.js integration;
- MCP SDK integration;
- OpenAI integration;
- Vitest test tooling;
- Node 24.x.

### Prompt domain model

The Prisma schema models a prompt as more than a text blob. Observed fields/relations include:

- `title`, `slug`, `description`, `content`;
- prompt `type`;
- privacy/unlisted/deleted state;
- category and tags;
- versions;
- change requests;
- votes and pinned state;
- collections;
- comments and reports;
- user-submitted examples;
- incoming/outgoing prompt connections;
- `bestWithModels` metadata;
- `bestWithMCP` metadata;
- optional `workflowLink`.

Observed prompt types are:

```text
TEXT
IMAGE
VIDEO
AUDIO
STRUCTURED
SKILL
TASTE
```

`PromptVersion` provides version-numbered prompt content with a change note and author. `ChangeRequest` preserves original/proposed content and title plus review state. These are notable product-governance patterns, not evidence-certification semantics.

### Configuration and self-hosting

`prompts.config.ts` exposes white-label/product configuration for:

- branding;
- theme;
- authentication providers;
- locales;
- private prompts;
- change requests;
- categories;
- tags;
- AI search;
- AI generation;
- MCP;
- comments.

The source README documents self-hosting and a setup path, and positions PostgreSQL as its database.

### Distribution surfaces

The README documents three notable integration lanes:

```text
CLI
Claude Code plugin
MCP server — remote or local
```

This is strategically relevant to Prompt Machine because it demonstrates that a prompt/workflow library can be made available at the user's point of work rather than only through a website or ZIP.

### AI-assisted improvement

The captured `/api/improve-prompt` route:

- requires an authenticated session or valid API key;
- accepts a non-empty prompt up to 10,000 characters;
- accepts declared output format and output type;
- delegates to a source-local `improvePrompt` function;
- returns validation, authentication, rate-limit and generic failure responses.

This observation proves the existence and request boundary of an AI-assisted improvement surface. It does **not** establish the quality, safety, evaluation rigor or superiority of the generated improvement.

### Governance

The source governance document defines users, contributors, maintainers and a project lead. Day-to-day changes use pull-request review; larger decisions use a lazy-consensus process with a stated feedback window and final project-lead authority if consensus fails.

### Licensing boundary

The source README states a dual licensing boundary:

- source code and site-authored content: MIT;
- prompt content/data: CC0 1.0 Universal.

Any future reuse must still preserve our own provenance and licensing review. This source record is not a blanket instruction to ingest all prompt bodies.

## What Prompt Quarry should learn from it

High-value architecture signals for evaluation include:

1. **Prompt identity as a durable object**, not an anonymous text file.
2. **Version history and reviewed change requests** as first-class product features.
3. **Rich discovery metadata** such as category, tags, model hints and MCP hints.
4. **Graph relationships between prompts/workflows** instead of only flat collections.
5. **Distribution at the execution surface** through CLI/MCP/plugins.
6. **Self-hosting/white-label capability** as an optional later enterprise/community lane.
7. **Contribution and moderation workflows** separated from core artifact execution.
8. **Explicit licensing boundaries** between software and content/data.

## What must NOT be inferred

Do not convert the following into Prompt Quarry claims without independent evidence:

```text
large catalog        != high quality
stars/popularity     != behavioral validity
open source          != certified
MCP support          != model portability
version history      != improvement evidence
AI improvement API   != proven improvement
self-hostable        != enterprise readiness
public prompt body   != approved MK1 input
```

## Promotion boundary

For this source snapshot:

```text
prompts.chat source observation
        ↓
mk0/sources/prompts-chat
        ↓
mk0/analysis comparative architecture
        ↓
explicit design decision / experiment
        ↓
MK1 only if separately engineered and tested
```

No prompt or skill becomes `VALID`, `TESTED`, `IMPROVED`, `CERTIFIED` or `PORTABLE` merely because a similar capability exists in `prompts.chat`.

## Companion files

- `SOURCE_MAP.md` — exact observed surfaces and claim boundaries.
- `mk0/analysis/prompts-chat-product-architecture-benchmark.md` — derived comparison and adoption decisions.
