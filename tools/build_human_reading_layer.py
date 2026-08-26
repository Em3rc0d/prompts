from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from build_derived_premium_prompts import build_prompt, slugify


RULE = "=" * 88
SUBRULE = "-" * 88


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def clean_filename(value: str, fallback: str = "artifact") -> str:
    value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return (value[:96] or fallback).strip("-")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def as_lines(value, indent: str = "") -> list[str]:
    if value is None:
        return [indent + "(none)"]
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{indent}{key}:")
                lines.extend(as_lines(item, indent + "  "))
            else:
                lines.append(f"{indent}{key}: {item}")
        return lines or [indent + "(empty)"]
    if isinstance(value, list):
        if not value:
            return [indent + "(none)"]
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(indent + "-")
                lines.extend(as_lines(item, indent + "  "))
            else:
                lines.append(f"{indent}- {item}")
        return lines
    return [indent + str(value)]


def prompt_reader(row: dict, derived: dict | None) -> tuple[str, dict]:
    title = (row.get("title") or "Untitled prompt").strip()
    category = row.get("category") or "Uncategorized"
    access = row.get("access") or ("premium" if row.get("is_premium") else "free")
    source_url = row.get("official_url") or row.get("source_url") or "(unknown)"
    uuid = row.get("uuid") or row.get("id") or "unknown"

    if derived:
        usable = derived.get("content") or ""
        mode = derived.get("mode") or "general"
        variables = derived.get("variables") or []
        techniques = derived.get("techniques") or []
        source_body_status = "NOT PUBLIC — source RPC returned content: null"
        readable_origin = "REPOSITORY-AUTHORED RECONSTRUCTION"
        fidelity = "metadata-derived-not-source-reproduction"
        derived_path = "library/prompts/alpacka/derived-premium/catalog.jsonl"
    else:
        usable, mode, variables = build_prompt(row)
        techniques = [
            "role-assignment",
            "question-first",
            "variable-template",
            "stepwise-procedure",
            "task-decomposition",
            "explicit-constraints",
            "output-formatting",
            "self-check",
        ]
        source_body_status = "PUBLICLY AVAILABLE AT SOURCE, BUT NOT DUPLICATED IN THIS READER LAYER"
        readable_origin = "REPOSITORY-AUTHORED READER VERSION"
        fidelity = "metadata-and-corpus-pattern-derived-not-source-reproduction"
        derived_path = "(not applicable; generated for human reading from the source metadata record)"

    signals = row.get("structural_signals") or {}
    content_hash = row.get("content_sha256") or (derived or {}).get("content_sha256") or "(not stored)"

    lines = [
        "PROMPT QUARRY — HUMAN READING COPY",
        RULE,
        f"TITLE              : {title}",
        "TYPE               : Prompt",
        f"CATEGORY           : {category}",
        f"SOURCE ACCESS      : {str(access).upper()}",
        f"SOURCE BODY STATUS : {source_body_status}",
        f"READABLE CONTENT   : {readable_origin}",
        f"FIDELITY           : {fidelity}",
        f"SOURCE UUID        : {uuid}",
        f"OFFICIAL SOURCE    : {source_url}",
        "MACHINE RECORD     : quarry/normalized/alpacka-ai-prompt-metadata.jsonl",
        f"DERIVED RECORD     : {derived_path}",
        f"CONTENT HASH       : {content_hash}",
        "",
        "WHAT THIS FILE MEANS",
        SUBRULE,
        "This TXT is the human-reading view of the artifact. The JSON/JSONL and raw evidence remain",
        "untouched elsewhere in the repository. Source-observed facts and repository-authored usable",
        "content are deliberately labeled separately so they cannot be confused later.",
        "",
        "USEFUL INPUTS / VARIABLES",
        SUBRULE,
    ]
    lines.extend(as_lines(variables))
    lines.extend(["", "PROMPT TO USE", SUBRULE, usable.rstrip(), "", "TECHNIQUES", SUBRULE])
    lines.extend(as_lines(techniques))
    if signals:
        lines.extend(["", "SOURCE-OBSERVED STRUCTURAL SIGNALS", SUBRULE])
        lines.extend(as_lines(signals))
    lines.extend([
        "",
        "PROVENANCE",
        SUBRULE,
        f"Official source: {source_url}",
        f"Source record ID: {row.get('id')}",
        f"Verification: {row.get('verification')}",
        f"Capture mode: {row.get('capture_mode')}",
        "",
        "IMPORTANT",
        SUBRULE,
        "The usable text above is not represented as the original premium prompt body. For free source",
        "records, the public source remains the authority for exact wording. The reader layer exists so a",
        "person can understand and reuse the repository without opening JSON files.",
    ])
    return "\n".join(lines), {"mode": mode, "variables": variables, "techniques": techniques}


def build_skill_reader(row: dict) -> str:
    name = row.get("skill_name") or row.get("id") or "Unnamed skill"
    description = row.get("description") or "No concise description observed."
    category = row.get("category") or "Uncategorized"
    variables = row.get("variables") or []
    signals = row.get("structural_signals") or {}

    operational = [
        f"ROLE\nActúa como una capacidad especializada en: {description}",
        "",
        "INTAKE",
        "- Identifica el objetivo concreto del usuario.",
        "- Solicita sólo el contexto faltante que cambie materialmente el resultado.",
        "- Confirma restricciones, formato y criterio de éxito cuando no sean evidentes.",
        "",
        "RULES",
        "- No inventes datos que el usuario no haya dado.",
        "- Separa hechos, supuestos y recomendaciones.",
        "- Prioriza claridad y utilidad práctica.",
        "- Si el dominio requiere verificación, señala qué debe comprobarse.",
        "",
        "OUTPUT",
        "- Entrega primero el resultado útil.",
        "- Después explica decisiones, riesgos y siguientes pasos cuando aporten valor.",
    ]

    lines = [
        "PROMPT QUARRY — HUMAN READING COPY",
        RULE,
        f"TITLE              : {name}",
        "TYPE               : Skill",
        f"CATEGORY           : {category}",
        f"ACCESS             : {str(row.get('access') or 'unknown').upper()}",
        f"OFFICIAL SOURCE    : {row.get('source_url') or '(unknown)'}",
        f"SOURCE BODY STATUS : OBSERVED PUBLICLY; NOT DUPLICATED VERBATIM HERE",
        "READABLE CONTENT   : REPOSITORY-AUTHORED RIRO-STYLE OPERATIONAL VERSION",
        f"SOURCE BODY LENGTH : {row.get('body_length')}",
        f"SOURCE BODY HASH   : {row.get('body_sha256')}",
        "MACHINE RECORD     : quarry/normalized/alpacka-ai-skills-metadata.jsonl",
        "",
        "WHAT THIS SKILL DOES",
        SUBRULE,
        description,
        "",
        "SOURCE-OBSERVED VARIABLES",
        SUBRULE,
    ]
    lines.extend(as_lines(variables))
    lines.extend(["", "SOURCE-OBSERVED STRUCTURE", SUBRULE])
    lines.extend(as_lines(signals))
    lines.extend(["", "USABLE REPOSITORY VERSION", SUBRULE])
    lines.extend(operational)
    lines.extend([
        "",
        "PROVENANCE",
        SUBRULE,
        f"Source ID: {row.get('id')}",
        f"Verification: {row.get('verification')}",
        f"Captured at: {row.get('captured_at')}",
        f"Raw source key: {(row.get('metadata') or {}).get('raw_source_key')}",
    ])
    return "\n".join(lines)


def build_generator_reader(row: dict, repo_root: Path) -> str:
    purpose = row.get("purpose") or row.get("id") or "generator-preview"
    mappings = {
        "growth-strategy-planning": "library/templates/business/growth-90-day-system.md",
        "lead-magnet-ideation": "library/templates/content/lead-magnet-design-system.md",
        "writing-style-specification": "library/templates/content/style-profile-extractor.md",
    }
    mapped = mappings.get(purpose)
    mapped_body = ""
    if mapped and (repo_root / mapped).exists():
        mapped_body = (repo_root / mapped).read_text(encoding="utf-8")

    lines = [
        "PROMPT QUARRY — HUMAN READING COPY",
        RULE,
        f"TITLE / PURPOSE     : {purpose}",
        "TYPE                : Generator Preview Reference",
        f"OFFICIAL SOURCE     : {row.get('source_url') or '(unknown)'}",
        f"ACCESS              : {row.get('access')}",
        "SOURCE BODY STATUS  : OBSERVED PUBLICLY; NOT DUPLICATED VERBATIM HERE",
        f"BODY LENGTH         : {row.get('body_length')}",
        f"BODY HASH           : {row.get('body_sha256')}",
        "MACHINE RECORD      : quarry/normalized/alpacka-ai-generator-previews.jsonl",
        "",
        "VARIABLES",
        SUBRULE,
    ]
    lines.extend(as_lines(row.get("variables") or []))
    lines.extend(["", "STRUCTURAL SIGNALS", SUBRULE])
    lines.extend(as_lines(row.get("structural_signals") or {}))
    lines.extend(["", "REPOSITORY-AUTHORED EQUIVALENT", SUBRULE])
    if mapped_body:
        lines.append(f"Canonical library path: {mapped}")
        lines.append("")
        lines.append(mapped_body.rstrip())
    else:
        lines.append("No promoted repository-authored equivalent has been linked yet.")
    return "\n".join(lines)


def build_blog_reader(row: dict) -> str:
    lines = [
        "PROMPT QUARRY — HUMAN READING COPY",
        RULE,
        f"TITLE           : {row.get('title')}",
        "TYPE            : Blog / Reference",
        f"CATEGORY        : {row.get('category')}",
        f"OFFICIAL SOURCE : {row.get('official_url') or row.get('source_url')}",
        f"PUBLISHED       : {row.get('published')}",
        f"CREATED         : {row.get('created_at')}",
        f"UPDATED         : {row.get('updated_at')}",
        f"CONTENT LENGTH  : {row.get('content_length')}",
        f"CONTENT HASH    : {row.get('content_sha256_prefix')}",
        "MACHINE RECORD  : quarry/normalized/alpacka-ai-blog-articles.jsonl",
        "",
        "ARTICLE OUTLINE",
        SUBRULE,
    ]
    headings = row.get("headings") or {}
    for key in ("h1", "h2", "h3"):
        vals = headings.get(key) or []
        if vals:
            lines.append(key.upper())
            lines.extend(f"- {v}" for v in vals)
    lines.extend([
        "",
        "NOTE",
        SUBRULE,
        "The article body is not mirrored here. This TXT preserves the readable source map, outline,",
        "metadata, hashes and direct official URL while the quarry keeps the machine-readable record.",
    ])
    return "\n".join(lines)


def operational_from_catalog(row: dict) -> str:
    summary = row.get("summary") or "No source body was directly observed."
    variables = row.get("variables") or []
    techniques = row.get("techniques") or []
    if row.get("artifact_type") != "prompt":
        return ""
    lines = [
        "Actúa como un especialista orientado al objetivo descrito abajo.",
        "",
        "OBJETIVO",
        summary,
        "",
        "ENTRADA",
    ]
    if variables:
        lines.extend(f"- {{{v}}}" for v in variables)
    else:
        lines.append("- {contexto del usuario}")
    lines.extend([
        "",
        "INSTRUCCIONES",
        "1. Conserva la intención descrita en el objetivo.",
        "2. Pide contexto faltante sólo cuando cambie materialmente la respuesta.",
        "3. Evita inventar hechos o atribuir al autor wording no observado.",
        "4. Entrega una versión clara, útil y directamente aplicable.",
        "",
        "TÉCNICAS OBSERVADAS / ASOCIADAS",
    ])
    lines.extend(f"- {t}" for t in techniques) if techniques else lines.append("- (none recorded)")
    return "\n".join(lines)


def build_catalog_reader(row: dict) -> str:
    lines = [
        "PROMPT QUARRY — HUMAN READING COPY",
        RULE,
        f"TITLE           : {row.get('title')}",
        f"TYPE            : {row.get('artifact_type')}",
        f"ID              : {row.get('id')}",
        f"AUTHOR          : {row.get('author')}",
        f"SOURCE          : {row.get('source_url')}",
        f"OFFICIAL POST   : {row.get('official_post_url')}",
        f"RAW URL         : {row.get('raw_url')}",
        f"VERIFICATION    : {row.get('verification')}",
        f"CAPTURE MODE    : {row.get('capture_mode')}",
        f"LANGUAGE        : {row.get('language')}",
        "MACHINE RECORD  : catalog/catalog.jsonl",
        "",
        "SUMMARY",
        SUBRULE,
        row.get("summary") or "(no summary)",
        "",
        "CATEGORIES",
        SUBRULE,
    ]
    lines.extend(as_lines(row.get("categories") or []))
    lines.extend(["", "TAGS", SUBRULE])
    lines.extend(as_lines(row.get("tags") or []))
    lines.extend(["", "TECHNIQUES", SUBRULE])
    lines.extend(as_lines(row.get("techniques") or []))
    lines.extend(["", "VARIABLES", SUBRULE])
    lines.extend(as_lines(row.get("variables") or []))
    if row.get("body"):
        lines.extend(["", "SOURCE BODY STORED IN CATALOG", SUBRULE, str(row.get("body"))])
    else:
        op = operational_from_catalog(row)
        if op:
            lines.extend(["", "USABLE REPOSITORY VERSION", SUBRULE, op])
    lines.extend(["", "PROVENANCE", SUBRULE])
    lines.extend(as_lines(row.get("provenance") or []))
    if row.get("metadata"):
        lines.extend(["", "ADDITIONAL METADATA", SUBRULE])
        lines.extend(as_lines(row.get("metadata")))
    return "\n".join(lines)


def convert_markdown_tree(repo_root: Path, output_root: Path, source_root: str, output_subdir: str) -> int:
    root = repo_root / source_root
    if not root.exists():
        return 0
    count = 0
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        out = output_root / output_subdir / rel.with_suffix(".txt")
        body = path.read_text(encoding="utf-8")
        header = [
            "PROMPT QUARRY — HUMAN READING COPY",
            RULE,
            f"SOURCE REPOSITORY FILE: {path.as_posix()}",
            "CONTENT ORIGIN       : REPOSITORY FILE (human-readable copy)",
            "",
        ]
        write_text(out, "\n".join(header) + body)
        count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="readable")
    args = parser.parse_args()

    repo = Path(".").resolve()
    out = repo / args.output
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    prompt_rows = read_jsonl(repo / "quarry/normalized/alpacka-ai-prompt-metadata.jsonl")
    premium_rows = read_jsonl(repo / "library/prompts/alpacka/derived-premium/catalog.jsonl")
    premium_by_uuid = {str(r.get("source_uuid")): r for r in premium_rows if r.get("source_uuid")}

    prompt_counts = Counter()
    prompt_index: defaultdict[str, list[tuple[str, str, str]]] = defaultdict(list)
    all_prompts: list[str] = []
    for row in sorted(prompt_rows, key=lambda r: ((r.get("category") or ""), (r.get("title") or ""), (r.get("uuid") or ""))):
        category = row.get("category") or "Uncategorized"
        cat_slug = slugify(category)
        uuid = str(row.get("uuid") or "unknown")
        title = row.get("title") or uuid
        filename = f"{clean_filename(title)}--{uuid[:8]}.txt"
        derived = premium_by_uuid.get(uuid)
        text, _ = prompt_reader(row, derived)
        path = out / "prompts" / "alpacka" / "categories" / cat_slug / filename
        write_text(path, text)
        prompt_counts[category] += 1
        prompt_index[category].append((title, filename, row.get("access") or "unknown"))
        all_prompts.append(text)

    for category, items in sorted(prompt_index.items()):
        cat_slug = slugify(category)
        lines = [f"PROMPTS — {category}", RULE, f"Total: {len(items)}", ""]
        for title, filename, access in items:
            lines.append(f"[{str(access).upper():7}] {title}")
            lines.append(f"          {filename}")
        write_text(out / "prompts" / "alpacka" / "categories" / cat_slug / "INDEX.txt", "\n".join(lines))

    prompt_root_index = [
        "ALPACKA PROMPTS — HUMAN INDEX",
        RULE,
        f"Total prompts: {len(prompt_rows)}",
        f"Free source records: {sum(1 for r in prompt_rows if r.get('access') == 'free')}",
        f"Premium source records: {sum(1 for r in prompt_rows if r.get('access') == 'premium')}",
        "",
        "Every prompt has one TXT file. Premium source bodies remain non-public, but each has a",
        "repository-authored usable reconstruction. Free exact source wording is not mirrored here; each",
        "free record has a repository-authored reader/use version plus its official URL and source hash.",
        "",
        "CATEGORIES",
        SUBRULE,
    ]
    for category, count in prompt_counts.most_common():
        prompt_root_index.append(f"- {category}: {count}  -> categories/{slugify(category)}/INDEX.txt")
    write_text(out / "prompts" / "alpacka" / "INDEX.txt", "\n".join(prompt_root_index))
    write_text(out / "prompts" / "alpacka" / "ALL_PROMPTS.txt", ("\n\n" + "#" * 96 + "\n\n").join(all_prompts))

    # Skills
    skill_rows = read_jsonl(repo / "quarry/normalized/alpacka-ai-skills-metadata.jsonl")
    skill_counts = Counter()
    all_skills: list[str] = []
    for row in sorted(skill_rows, key=lambda r: ((r.get("category") or ""), (r.get("skill_name") or ""))):
        category = row.get("category") or "Uncategorized"
        skill_counts[category] += 1
        name = row.get("skill_name") or row.get("id") or "skill"
        text = build_skill_reader(row)
        write_text(out / "skills" / "alpacka" / "categories" / slugify(category) / f"{clean_filename(name)}.txt", text)
        all_skills.append(text)
    skill_index = ["ALPACKA SKILLS — HUMAN INDEX", RULE, f"Total skills: {len(skill_rows)}", ""]
    skill_index.extend(f"- {cat}: {count}" for cat, count in skill_counts.most_common())
    write_text(out / "skills" / "alpacka" / "INDEX.txt", "\n".join(skill_index))
    write_text(out / "skills" / "alpacka" / "ALL_SKILLS.txt", ("\n\n" + "#" * 96 + "\n\n").join(all_skills))

    # Generator previews
    generator_rows = read_jsonl(repo / "quarry/normalized/alpacka-ai-generator-previews.jsonl")
    for row in generator_rows:
        purpose = row.get("purpose") or row.get("id") or "preview"
        write_text(out / "generator" / f"{clean_filename(purpose)}.txt", build_generator_reader(row, repo))

    # Blog references
    blog_rows = read_jsonl(repo / "quarry/normalized/alpacka-ai-blog-articles.jsonl")
    for row in blog_rows:
        name = row.get("slug") or row.get("id") or "article"
        write_text(out / "references" / "blog" / f"{clean_filename(name)}.txt", build_blog_reader(row))

    # Canonical catalog: one TXT per record, including Threads and source references.
    catalog_rows = read_jsonl(repo / "catalog/catalog.jsonl")
    catalog_type_counts = Counter()
    for row in catalog_rows:
        artifact_type = row.get("artifact_type") or "reference"
        catalog_type_counts[artifact_type] += 1
        title = row.get("title") or row.get("id") or "catalog-record"
        filename = f"{clean_filename(title)}--{clean_filename(str(row.get('id') or 'id'))[:24]}.txt"
        write_text(out / "catalog" / artifact_type / filename, build_catalog_reader(row))

    # Repository-owned Markdown and documentation/source maps, duplicated only for human TXT convenience.
    library_docs = convert_markdown_tree(repo, out, "library", "repository-artifacts")
    documentation_docs = convert_markdown_tree(repo, out, "docs", "documentation/docs")
    source_docs = convert_markdown_tree(repo, out, "sources", "documentation/sources")

    manifest = {
        "version": 1,
        "policy": "Machine/raw evidence is preserved. This directory is additive human-readable TXT material only.",
        "prompt_txt_records": len(prompt_rows),
        "prompt_source_free": sum(1 for r in prompt_rows if r.get("access") == "free"),
        "prompt_source_premium": sum(1 for r in prompt_rows if r.get("access") == "premium"),
        "premium_reader_reconstructions": len(premium_by_uuid),
        "skill_txt_records": len(skill_rows),
        "generator_txt_records": len(generator_rows),
        "blog_reference_txt_records": len(blog_rows),
        "canonical_catalog_txt_records": len(catalog_rows),
        "catalog_type_counts": dict(catalog_type_counts),
        "repository_markdown_txt_copies": library_docs,
        "documentation_txt_copies": documentation_docs,
        "source_map_txt_copies": source_docs,
        "prompt_category_counts": dict(prompt_counts.most_common()),
        "skill_category_counts": dict(skill_counts.most_common()),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    overview = [
        "PROMPT QUARRY — HUMAN READING LAYER",
        RULE,
        "",
        "PURPOSE",
        SUBRULE,
        "Open this directory when you want to READ the repository. Open quarry/, catalog/ and raw JSON",
        "when you want machine evidence, exact IDs, hashes or ingestion/debugging data.",
        "",
        "NOTHING WAS REPLACED",
        SUBRULE,
        "- raw evidence remains in quarry/raw/",
        "- normalized JSON/JSONL remains in quarry/normalized/",
        "- indexes/analysis/fixtures remain unchanged",
        "- canonical repository artifacts remain in library/",
        "- readable/ is an additive convenience layer",
        "",
        "START HERE",
        SUBRULE,
        "1. prompts/alpacka/INDEX.txt      -> all 530 prompt references by category",
        "2. prompts/alpacka/ALL_PROMPTS.txt -> single-file reading/search view",
        "3. skills/alpacka/INDEX.txt       -> all public skill references",
        "4. skills/alpacka/ALL_SKILLS.txt  -> single-file skill reading view",
        "5. generator/                     -> generator previews + linked repository equivalents",
        "6. references/blog/               -> readable blog outlines and official URLs",
        "7. catalog/                       -> one TXT per canonical catalog record, including Threads",
        "8. repository-artifacts/          -> TXT copies of repository-authored Markdown",
        "9. documentation/                 -> TXT copies of docs and source maps",
        "",
        "PROVENANCE RULE",
        SUBRULE,
        "SOURCE-OBSERVED != REPOSITORY-AUTHORED. Every TXT labels that boundary explicitly.",
        "",
        "COUNTS",
        SUBRULE,
    ]
    overview.extend(as_lines(manifest, ""))
    write_text(out / "README.txt", "\n".join(overview))

    top_index = [
        "READABLE ARTIFACT INDEX",
        RULE,
        f"Prompts: {len(prompt_rows)}",
        f"Skills: {len(skill_rows)}",
        f"Generator previews: {len(generator_rows)}",
        f"Blog references: {len(blog_rows)}",
        f"Canonical catalog records: {len(catalog_rows)}",
        f"Repository Markdown copies: {library_docs}",
        f"Documentation/source-map copies: {documentation_docs + source_docs}",
        "",
        "See README.txt for how to navigate this directory.",
    ]
    write_text(out / "INDEX.txt", "\n".join(top_index))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
