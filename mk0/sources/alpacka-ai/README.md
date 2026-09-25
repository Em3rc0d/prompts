# Source Quarry — Alpacka AI

Primary surfaces:

- Threads profile: `https://www.threads.com/@alpacka.ai`
- Website: `https://www.alpackaai.xyz`
- Prompt bank: `https://alpackaai.xyz/bank-prompts?utm_source=threads&utm_medium=social&utm_content=link_in_bio`

Observed website title: `Banco de Prompts de IA · +1.000 prompts para ChatGPT, Claude y Gemini | Alpacka`.

## What we preserve

For every discovered artifact we keep, when available: official URL, raw/API URL, platform, author, type, title, language, categories, tags, model targets, techniques, timestamps, capture method, verification state, fingerprint, summary and all provenance links.

## Access notes

Threads may return rate-limit responses to direct automated frontend access, so the preferred collection lane is the official Threads API when an authorized token is available.

The website is publicly reachable but item-level content is dynamically rendered. A browser-based collector is maintained under `tools/ingest_web.py` for quarry runs.

## Evidence states

- `source-body-observed`: primary source body retrieved directly.
- `source-url-observed`: official source URL verified; body not yet captured.
- `secondary-source-observed`: item referenced by another public source.
- `metadata-only`: only source/page metadata known.
- `blocked`: retrieval stopped at an access or rate barrier.

## Promotion rule

```text
source -> quarry/raw -> quarry/normalized -> validation -> library
```

Nothing should be promoted directly from an external source into the reusable library without normalization and provenance validation.
