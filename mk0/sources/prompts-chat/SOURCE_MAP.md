# prompts.chat — Source Map

Snapshot: `f/prompts.chat@f78a1c5136fa080155d928e0d7e2b4a41ddef03e`

Captured: `2026-09-15`

This map records **what was directly observed in the source repository** and separates it from Prompt Quarry interpretation.

| Source surface | Observation used here | Evidence class |
|---|---|---|
| `README.md` | public library positioning, data formats, self-hosting, CLI, Claude Code plugin, MCP, dual-license statement | source observation |
| `package.json` | Next.js/React/Prisma/PostgreSQL-facing dependency stack, MCP SDK, OpenAI SDK, Vitest, Node 24 engine | source observation |
| `prisma/schema.prisma` | prompt/user/version/change-request/category/tag/collection/comment/report/connection domain model | source observation |
| `prompts.config.ts` | branding/theme/auth/i18n and feature toggles including private prompts, change requests, categories, tags, AI search/generation, MCP, comments | source observation |
| `src/app/api/improve-prompt/route.ts` | authenticated prompt-improvement request boundary and validation/error handling | source observation |
| `GOVERNANCE.md` | user/contributor/maintainer/project-lead roles and lazy-consensus governance pattern | source observation |

## Exact source revision

```text
repository  f/prompts.chat
branch      main
commit      f78a1c5136fa080155d928e0d7e2b4a41ddef03e
commit date 2026-09-09T10:27:04Z
```

The snapshot is revision-bound. Later upstream changes must not be silently attributed to this characterization.

## Directly observed product capabilities

### Library and data

The source README describes:

- a curated prompt collection;
- browser discovery;
- `prompts.csv`;
- `PROMPTS.md`;
- a Hugging Face dataset;
- contribution through the web product.

### Artifact/domain structure

The schema directly includes:

- prompt versions;
- reviewed change requests;
- categories and hierarchical category relations;
- tags;
- votes;
- pinned prompts;
- per-user collections;
- examples;
- reports;
- comments and comment votes;
- prompt-to-prompt connections;
- model hints;
- MCP hints;
- workflow links.

### Execution/distribution adjacency

The README directly documents:

- a CLI package invocation;
- a Claude Code plugin installation path;
- remote MCP configuration;
- local MCP configuration;
- self-hosting.

### Configurability

The checked-in config directly exposes:

- product branding;
- design/theme options;
- auth providers;
- locale inventory;
- product feature toggles.

### AI-assisted transformation

The checked API route directly proves an authenticated endpoint for improving a prompt. The route accepts:

```text
prompt
outputFormat = text | structured_json | structured_yaml
outputType   = text | image | video | sound
```

It does not, by itself, prove improvement quality.

## Repository-derived interpretation

The following are **Prompt Quarry analysis**, not source claims:

- prompts.chat is useful as a benchmark for prompt-library product architecture;
- first-class version/change-request models may be useful for a future workflow registry;
- MCP/CLI/plugin distribution should be evaluated as a lower-friction execution lane for Prompt Machine artifacts;
- graph relationships may be more useful than a flat pack-only mental model for multi-step workflows;
- white-label/self-hosting is a possible later organization/enterprise capability, not a current Verlune release requirement.

These derived conclusions live in:

`mk0/analysis/prompts-chat-product-architecture-benchmark.md`

## Excluded claims

This characterization does not assert:

- the total number of currently active prompt records;
- prompt success rates;
- model portability;
- safety quality;
- commercial conversion;
- enterprise readiness;
- superiority over Prompt Machine/Prompt Quarry;
- certification of any upstream prompt.

Popularity statements in the upstream README are not used as evidence of prompt quality.

## Licensing note

The source README states MIT for source/site-authored material and CC0 for prompt content/data. Prompt Quarry still treats provenance, license and promotion as explicit review boundaries. No bulk body import is performed by this integration.
