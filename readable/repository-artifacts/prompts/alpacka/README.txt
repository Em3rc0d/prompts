PROMPT QUARRY — HUMAN READING COPY
========================================================================================
SOURCE REPOSITORY FILE: /home/runner/work/prompts/prompts/library/prompts/alpacka/README.md
CONTENT ORIGIN       : REPOSITORY FILE (human-readable copy)
# Alpacka public prompt reference index

This directory is a provenance-first navigation layer over public Alpacka prompt metadata plus a separate repository-authored reusable layer.

The source boundary remains explicit: the public detail RPC returns the original body for free records and `content: null` for premium records. Prompt Quarry does **not** claim to recover those private/premium bodies. Instead, every premium reference now has a separate non-empty repository-authored reconstruction under `derived-premium/`.

- Total source prompt references: **530**
- Free source records: **52**
- Premium source references: **478**
- Premium repository-authored reconstructions: **478**
- Derived premium records with empty content: **0**
- Categories: **22**

## Evidence and reuse ladder

```text
PUBLIC DIRECTORY / RPC
        ↓
quarry/normalized/alpacka-ai-prompt-metadata.jsonl
        ↓
CATEGORY INDEXES
        ↓
STRUCTURE + TECHNIQUE MINING
        ↓
GOLDEN FIXTURES
        ↓
        ├── promoted reusable patterns/templates
        └── 478 derived-premium reconstructions
```

The layers are intentionally separate: source observations are evidence; derived/library artifacts are our reusable work.

## Premium usable layer

Files:

- `library/prompts/alpacka/derived-premium/catalog.jsonl`
- `library/prompts/alpacka/derived-premium/manifest.json`
- `library/prompts/alpacka/derived-premium/categories/*.jsonl`
- `library/prompts/alpacka/derived-premium/README.md`

Every derived record contains a non-empty `content` string and preserves:

- source UUID
- source URL
- source title
- source category
- `source_body_status: not-public`
- `content_origin: repository-authored-reconstruction`
- `fidelity: metadata-derived-not-source-reproduction`
- content fingerprint

The reconstruction builder uses public title/category plus construction patterns mined from the 52 free prompts and the public Skills corpus. It selects procedures based on intent signals such as plan, checklist, simulation, audit, generation, writing, optimization and learning.

## Categories

| Category | Total | Free | Index |
| --- | ---: | ---: | --- |
| Marketing | 95 | 8 | `quarry/indexes/alpacka-ai/categories/marketing.jsonl` |
| Idiomas | 51 | 6 | `quarry/indexes/alpacka-ai/categories/idiomas.jsonl` |
| Astrología | 47 | 12 | `quarry/indexes/alpacka-ai/categories/astrologia.jsonl` |
| Abogados | 45 | 3 | `quarry/indexes/alpacka-ai/categories/abogados.jsonl` |
| Ideas de Negocio | 45 | 0 | `quarry/indexes/alpacka-ai/categories/ideas-de-negocio.jsonl` |
| Educación | 36 | 2 | `quarry/indexes/alpacka-ai/categories/educacion.jsonl` |
| Ganar Dinero | 30 | 0 | `quarry/indexes/alpacka-ai/categories/ganar-dinero.jsonl` |
| Salud | 23 | 6 | `quarry/indexes/alpacka-ai/categories/salud.jsonl` |
| Empleo | 16 | 5 | `quarry/indexes/alpacka-ai/categories/empleo.jsonl` |
| Copywriting | 15 | 2 | `quarry/indexes/alpacka-ai/categories/copywriting.jsonl` |
| Crear logos | 15 | 0 | `quarry/indexes/alpacka-ai/categories/crear-logos.jsonl` |
| Negocios | 15 | 1 | `quarry/indexes/alpacka-ai/categories/negocios.jsonl` |
| Desarrollo Personal | 12 | 0 | `quarry/indexes/alpacka-ai/categories/desarrollo-personal.jsonl` |
| Imagen | 12 | 2 | `quarry/indexes/alpacka-ai/categories/imagen.jsonl` |
| Productividad | 12 | 0 | `quarry/indexes/alpacka-ai/categories/productividad.jsonl` |
| Programación | 12 | 0 | `quarry/indexes/alpacka-ai/categories/programacion.jsonl` |
| Finanzas Personales | 11 | 1 | `quarry/indexes/alpacka-ai/categories/finanzas-personales.jsonl` |
| Redes Sociales | 11 | 1 | `quarry/indexes/alpacka-ai/categories/redes-sociales.jsonl` |
| E-commerce | 10 | 0 | `quarry/indexes/alpacka-ai/categories/e-commerce.jsonl` |
| IG reels | 9 | 3 | `quarry/indexes/alpacka-ai/categories/ig-reels.jsonl` |
| Profesores | 6 | 0 | `quarry/indexes/alpacka-ai/categories/profesores.jsonl` |
| Ingeniería | 2 | 0 | `quarry/indexes/alpacka-ai/categories/ingenieria.jsonl` |

## Structural mining

Base aggregate structure:
- `quarry/analysis/alpacka-ai-free-structure-report.json`

Deeper technique vectors and category matrix:
- `quarry/analysis/alpacka-ai-free-technique-vectors.jsonl`
- `quarry/analysis/alpacka-ai-free-technique-matrix.json`

The deeper pass classifies reusable construction techniques such as role assignment, variable templates, decomposition, explicit constraints, output formatting, self-checks, audience/tone definition and evidence requirements. Free prompt bodies are fetched from the public RPC, analyzed in memory and discarded.

## Golden fixtures

- `quarry/fixtures/alpacka-free-golden-fixtures.json`
- `quarry/fixtures/alpacka-free-golden-fixtures-manifest.json`
- `docs/GOLDEN_DATASET.md`

The fixture set covers observed techniques, source categories and frequent architecture signatures without storing prompt bodies. It is intended for parser/classifier regression tests and future Prompt Engine evaluation.

## Promoted repository artifacts

Examples currently promoted from aggregate source observations include:
- `library/patterns/skill-design/role-intake-rules-output.md`
- `library/templates/business/growth-90-day-system.md`
- `library/templates/content/lead-magnet-design-system.md`
- `library/templates/content/style-profile-extractor.md`

These are repository-authored artifacts. Their catalog provenance points back to the observed source family, but their wording and operating contracts are our own.

## Provenance boundary

Every source record retains its official Alpacka URL. The quarry distinguishes source-observed metadata from repository-authored content. The 478 derived premium prompts are usable Prompt Quarry artifacts and must never be represented as recovered copies of Alpacka's premium source bodies.
