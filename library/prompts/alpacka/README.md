# Alpacka public prompt reference index

This directory is a provenance-first navigation layer over public Alpacka prompt metadata.

It does **not** mirror premium prompt bodies. Premium entries remain metadata-only. Free prompt bodies are not stored either; they are processed in memory for fingerprints and structural features, then discarded.

- Total prompt references: **530**
- Free: **52**
- Premium metadata-only: **478**
- Categories: **22**

## Evidence ladder

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
REPOSITORY-AUTHORED library/ ARTIFACTS
```

The layers are intentionally separate: source observations are evidence; library artifacts are our reusable abstractions.

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

Every record retains its official Alpacka URL. The quarry distinguishes source-observed metadata from repository-authored patterns/templates. Derived library artifacts must cite their source IDs and must not claim to reproduce premium prompt content.
