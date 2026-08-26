PROMPT QUARRY — HUMAN READING LAYER
========================================================================================

PURPOSE
----------------------------------------------------------------------------------------
Open this directory when you want to READ the repository. Open quarry/, catalog/ and raw JSON
when you want machine evidence, exact IDs, hashes or ingestion/debugging data.

NOTHING WAS REPLACED
----------------------------------------------------------------------------------------
- raw evidence remains in quarry/raw/
- normalized JSON/JSONL remains in quarry/normalized/
- indexes/analysis/fixtures remain unchanged
- canonical repository artifacts remain in library/
- readable/ is an additive convenience layer

START HERE
----------------------------------------------------------------------------------------
1. prompts/alpacka/INDEX.txt      -> all 530 prompt references by category
2. prompts/alpacka/ALL_PROMPTS.txt -> single-file reading/search view
3. skills/alpacka/INDEX.txt       -> all public skill references
4. skills/alpacka/ALL_SKILLS.txt  -> single-file skill reading view
5. generator/                     -> generator previews + linked repository equivalents
6. references/blog/               -> readable blog outlines and official URLs
7. catalog/                       -> one TXT per canonical catalog record, including Threads
8. repository-artifacts/          -> TXT copies of repository-authored Markdown
9. documentation/                 -> TXT copies of docs and source maps

PROVENANCE RULE
----------------------------------------------------------------------------------------
SOURCE-OBSERVED != REPOSITORY-AUTHORED. Every TXT labels that boundary explicitly.

COUNTS
----------------------------------------------------------------------------------------
version: 1
policy: Machine/raw evidence is preserved. This directory is additive human-readable TXT material only.
prompt_txt_records: 530
prompt_source_free: 52
prompt_source_premium: 478
premium_reader_reconstructions: 478
skill_txt_records: 12
generator_txt_records: 3
blog_reference_txt_records: 2
canonical_catalog_txt_records: 21
catalog_type_counts:
  reference: 2
  prompt: 7
  skill: 1
  workflow: 1
  template: 7
  pattern: 3
repository_markdown_txt_copies: 20
documentation_txt_copies: 5
source_map_txt_copies: 3
prompt_category_counts:
  Marketing: 95
  Idiomas: 51
  Astrología: 47
  Abogados: 45
  Ideas de Negocio: 45
  Educación: 36
  Ganar Dinero: 30
  Salud: 23
  Empleo: 16
  Copywriting: 15
  Crear logos: 15
  Negocios: 15
  Desarrollo Personal: 12
  Imagen: 12
  Productividad: 12
  Programación: 12
  Finanzas Personales: 11
  Redes Sociales: 11
  E-commerce: 10
  IG reels: 9
  Profesores: 6
  Ingeniería: 2
skill_category_counts:
  MARKETING: 3
  ESCRITURA: 2
  NEGOCIOS: 2
  PRODUCTIVIDAD: 2
  DATOS: 1
  DESARROLLO: 1
  ESTUDIO: 1

STAGE ARCHITECTURE
----------------------------------------------------------------------------------------
10. stages/ROOT_OVERVIEW.txt        -> repository and MK0/MK1/MK2 overview
11. stages/ROADMAP.txt              -> roadmap and stage gates
12. stages/ARCHITECTURE.txt         -> full cross-stage architecture
13. stages/mk0/                     -> Knowledge Quarry documentation
14. stages/mk1/                     -> Prompt Forge contracts, rubric and fixtures
15. stages/mk2/                     -> future Prompt Engine boundary

