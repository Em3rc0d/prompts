# Prompt Quarry

Private research repository for collecting, classifying, studying and reusing AI prompts, skills and prompt-engineering patterns with full provenance.

## Principles

1. **Source first.** Every artifact keeps its original source URL whenever available.
2. **Raw != normalized.** We preserve source evidence separately from derived analysis.
3. **Provenance survives deduplication.** Duplicate content may collapse into one normalized record, but every discovered source remains attached.
4. **Prompt != skill != workflow.** Artifact type is explicit, never inferred from folder alone.
5. **Evidence before claims.** Unknown metadata stays `null`/`unknown`; it is never invented.
6. **No access-control bypass.** Collectors stop on authentication, CAPTCHA, paywalls or rate-limit blocks.
7. **Private research orientation.** Third-party material keeps attribution and source links; derived summaries/pattern analysis are stored separately from source evidence.

## Repository map

```text
prompts/
├── README.md
├── catalog/
│   ├── catalog.jsonl          # canonical machine-readable index
│   ├── sources.jsonl          # source registry
│   └── taxonomy.yaml          # controlled vocabulary
├── library/
│   ├── prompts/               # normalized prompt records
│   ├── skills/                # reusable multi-step capabilities
│   ├── workflows/             # chained procedures / pipelines
│   ├── templates/             # reusable prompt shells
│   └── patterns/              # extracted prompt-engineering patterns
├── quarry/
│   ├── raw/                   # source observations / manifests
│   ├── normalized/            # cleaned records before promotion
│   └── fixtures/              # regression fixtures for ingestion
├── sources/
│   └── alpacka-ai/            # first source family
├── tools/
│   ├── ingest_threads.py
│   ├── ingest_web.py
│   ├── normalize.py
│   └── validate_catalog.py
└── docs/
    ├── ARCHITECTURE.md
    ├── CLASSIFICATION.md
    └── PROVENANCE.md
```

## Canonical record

Each catalog entry is designed to answer:

- What is this artifact?
- What is it useful for?
- Where did it come from?
- What exact official/source URL was observed?
- Was the body captured, summarized, or only indexed?
- Which model/tool is it intended for?
- Which prompt-engineering techniques does it use?
- Is it duplicated elsewhere?
- What was derived by us versus observed at source?

Example:

```json
{
  "id": "pq_alpacka_threads_DPwn67yDrZK",
  "artifact_type": "prompt",
  "title": "Rompe límites financieros",
  "source_id": "src_alpacka_threads",
  "source_url": "https://www.threads.com/@alpacka.ai/post/DPwn67yDrZK/...",
  "official_post_url": "https://www.threads.com/@alpacka.ai/post/DPwn67yDrZK/...",
  "raw_url": null,
  "capture_mode": "indexed-reference",
  "language": "es",
  "categories": ["personal-development", "finance"],
  "tags": ["beliefs", "reflection"],
  "techniques": ["structured-reflection"],
  "body": null,
  "summary": "Prompt-oriented post about identifying limiting money beliefs.",
  "provenance": [],
  "verification": "source-url-observed"
}
```

## First quarry: Alpacka AI

Tracked source surfaces:

- Threads: `https://www.threads.com/@alpacka.ai`
- Website: `https://www.alpackaai.xyz`
- Prompt bank: `https://alpackaai.xyz/bank-prompts`

The website identifies itself as a Spanish AI prompt bank with 1,000+ prompts for ChatGPT, Claude and Gemini. The repository treats Alpacka as a **source**, not as the repository taxonomy.

## Artifact types

| Type | Meaning |
|---|---|
| `prompt` | Direct instruction intended for an AI model |
| `skill` | Reusable capability containing instructions, context and/or procedures |
| `workflow` | Ordered multi-step process, potentially combining prompts/tools |
| `template` | Parameterized shell intended to be filled with variables |
| `pattern` | Generalized prompt-engineering technique extracted from examples |
| `guide` | Educational/explanatory material |
| `reference` | Useful source evidence that is not itself a prompt |

## Status

`MK0 — quarry bootstrap`

Current work: source registry, controlled taxonomy, collectors, provenance contract and first Alpacka evidence records.
