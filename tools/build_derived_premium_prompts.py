from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


CATEGORY_ROLE = {
    "Abogados": "un analista jurídico cuidadoso y orientado a evidencia",
    "Astrología": "un intérprete de astrología orientado a reflexión y entretenimiento",
    "Copywriting": "un estratega senior de copywriting y conversión",
    "Crear logos": "un director de identidad visual y diseño de marcas",
    "Desarrollo Personal": "un coach de reflexión y desarrollo personal",
    "E-commerce": "un estratega de e-commerce, conversión y operaciones",
    "Educación": "un diseñador instruccional y tutor experto",
    "Empleo": "un consultor de carrera y selección",
    "Finanzas Personales": "un analista de finanzas personales orientado a escenarios",
    "Ganar Dinero": "un analista de modelos de ingreso y validación de oportunidades",
    "Ideas de Negocio": "un estratega de emprendimiento y validación de negocios",
    "IG reels": "un estratega de video corto y retención",
    "Idiomas": "un tutor de idiomas adaptativo",
    "Imagen": "un director creativo especializado en generación de imágenes",
    "Ingeniería": "un ingeniero de sistemas orientado a análisis y verificación",
    "Marketing": "un estratega de marketing basado en experimentos",
    "Negocios": "un consultor de estrategia y operaciones de negocio",
    "Productividad": "un diseñador de sistemas personales de productividad",
    "Profesores": "un diseñador instruccional para docentes",
    "Programación": "un ingeniero de software senior orientado a claridad y pruebas",
    "Redes Sociales": "un estratega de contenido y crecimiento en redes sociales",
    "Salud": "un asistente educativo de salud que prioriza seguridad y límites clínicos",
}

CATEGORY_INPUTS = {
    "Abogados": ["jurisdicción", "hechos relevantes", "objetivo", "documentos/evidencia disponibles"],
    "Astrología": ["datos o contexto que quieras interpretar", "pregunta principal", "nivel de detalle"],
    "Copywriting": ["producto/oferta", "audiencia", "objetivo de conversión", "tono", "canal"],
    "Crear logos": ["nombre de marca", "audiencia", "personalidad", "usos del logo", "restricciones visuales"],
    "Desarrollo Personal": ["situación actual", "objetivo", "restricciones", "horizonte temporal"],
    "E-commerce": ["producto", "mercado", "canal", "métricas actuales", "restricciones"],
    "Educación": ["tema", "nivel actual", "objetivo", "tiempo disponible", "preferencias de aprendizaje"],
    "Empleo": ["rol objetivo", "experiencia real", "vacante o contexto", "restricciones"],
    "Finanzas Personales": ["ingresos", "gastos", "deudas", "meta", "horizonte temporal"],
    "Ganar Dinero": ["habilidades", "recursos", "mercado", "tiempo disponible", "tolerancia al riesgo"],
    "Ideas de Negocio": ["problema", "audiencia", "recursos", "mercado", "restricciones"],
    "IG reels": ["tema", "audiencia", "plataforma", "objetivo", "tono"],
    "Idiomas": ["idioma", "nivel", "objetivo", "situación de uso", "tiempo disponible"],
    "Imagen": ["sujeto", "estilo", "composición", "iluminación", "formato"],
    "Ingeniería": ["problema", "sistema", "restricciones", "datos disponibles", "criterio de aceptación"],
    "Marketing": ["oferta", "audiencia", "canal", "objetivo", "baseline", "presupuesto/restricciones"],
    "Negocios": ["empresa/proyecto", "objetivo", "métricas", "restricciones", "horizonte"],
    "Productividad": ["objetivo", "carga actual", "tiempo", "herramientas", "restricciones"],
    "Profesores": ["materia", "nivel", "objetivo de aprendizaje", "duración", "restricciones de aula"],
    "Programación": ["contexto técnico", "código o arquitectura", "objetivo", "restricciones", "criterio de aceptación"],
    "Redes Sociales": ["nicho", "audiencia", "plataforma", "objetivo", "tono"],
    "Salud": ["objetivo educativo", "contexto general", "restricciones", "señales de alarma si existen"],
}

HIGH_STAKES = {"Abogados", "Finanzas Personales", "Salud"}


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "uncategorized"


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def infer_mode(title: str) -> tuple[str, list[str]]:
    low = title.casefold()
    rules = [
        (("checklist", "lista de verificación"), "checklist", ["Define los criterios de revisión.", "Evalúa cada criterio como PASS / RISK / UNKNOWN.", "Prioriza los riesgos y propone acciones concretas."]),
        (("plan", "estrategia", "mapa", "ruta"), "plan", ["Diagnostica el punto de partida.", "Define el resultado objetivo y las restricciones.", "Construye un plan por fases con prioridades y métricas.", "Cierra con las primeras acciones ejecutables."]),
        (("simulador", "simula", "roleplay", "entrevista"), "simulation", ["Define escenario y roles.", "Ejecuta la interacción por turnos.", "Después de cada bloque, señala oportunidades de mejora.", "Finaliza con evaluación y siguiente práctica."]),
        (("auditor", "auditoría", "analiza", "analista", "detector", "evaluador"), "audit", ["Establece criterios de evaluación.", "Separa observaciones de inferencias.", "Identifica fortalezas, riesgos y vacíos de información.", "Prioriza recomendaciones por impacto y evidencia."]),
        (("generador", "creador", "fábrica", "ideas", "opciones"), "generation", ["Aclara criterios antes de generar.", "Produce alternativas suficientemente distintas.", "Explica brevemente el razonamiento práctico de cada opción.", "Recomienda las mejores opciones según el objetivo."]),
        (("redactor", "escribe", "descripción", "guion", "email", "carta"), "writing", ["Define audiencia, propósito y tono.", "Construye una estructura antes de redactar.", "Redacta una versión principal clara y específica.", "Revisa precisión, redundancia y llamada a la acción cuando aplique."]),
        (("optimiza", "mejora", "refactor", "doctor"), "optimization", ["Diagnostica el estado actual.", "Identifica cuellos de botella o defectos.", "Propón mejoras priorizadas con trade-offs.", "Entrega una versión o plan mejorado y criterios de verificación."]),
        (("aprende", "tutor", "enseña", "curso"), "learning", ["Comprueba el nivel inicial.", "Identifica el 20% de conceptos de mayor impacto.", "Enseña por bloques cortos con práctica.", "Verifica comprensión y adapta el siguiente bloque."]),
    ]
    for tokens, mode, steps in rules:
        if any(token in low for token in tokens):
            return mode, steps
    return "general", [
        "Aclara el contexto y el resultado esperado.",
        "Descompón el problema en partes manejables.",
        "Resuelve cada parte con supuestos explícitos.",
        "Entrega una recomendación accionable y una verificación final.",
    ]


def build_prompt(row: dict) -> tuple[str, str, list[str]]:
    title = (row.get("title") or "Objetivo sin título").strip()
    category = row.get("category") or "General"
    role = CATEGORY_ROLE.get(category, "un especialista práctico y orientado a resultados")
    inputs = CATEGORY_INPUTS.get(category, ["contexto", "objetivo", "restricciones", "datos disponibles"])
    mode, steps = infer_mode(title)

    constraints = [
        "No inventes hechos, cifras, fuentes ni contexto que el usuario no haya proporcionado.",
        "Marca como supuesto cualquier inferencia necesaria para avanzar.",
        "Si falta información que cambie materialmente el resultado, pregunta antes de cerrar la respuesta.",
        "Prioriza una respuesta específica y accionable sobre consejos genéricos.",
    ]
    if category in HIGH_STAKES:
        constraints.append("Distingue información educativa/general de asesoría profesional individual y señala cuándo hace falta un profesional cualificado.")

    lines = [
        f"Actúa como {role}.",
        "",
        f"OBJETIVO\n{title}.",
        "",
        "INTAKE",
        "Antes de resolver, confirma o solicita sólo la información que falte de:",
    ]
    lines.extend(f"- {{{item}}}" for item in inputs)
    lines.extend(["", "PROCESO"])
    lines.extend(f"{idx}. {step}" for idx, step in enumerate(steps, 1))
    lines.extend(["", "REGLAS"])
    lines.extend(f"- {item}" for item in constraints)
    lines.extend([
        "",
        "FORMATO DE SALIDA",
        "1. Resumen ejecutivo.",
        "2. Análisis o propuesta principal.",
        "3. Riesgos, supuestos o vacíos de información.",
        "4. Próximos pasos priorizados.",
        "5. Checklist breve de auto-verificación.",
    ])
    return "\n".join(lines).strip() + "\n", mode, inputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="library/prompts/alpacka/derived-premium/catalog.jsonl")
    parser.add_argument("--manifest", default="library/prompts/alpacka/derived-premium/manifest.json")
    parser.add_argument("--categories-dir", default="library/prompts/alpacka/derived-premium/categories")
    args = parser.parse_args()

    source_rows = list(read_jsonl(Path(args.input)))
    premium = [row for row in source_rows if row.get("access") == "premium"]
    if not premium:
        raise SystemExit("No premium records found.")

    records = []
    for row in premium:
        content, mode, inputs = build_prompt(row)
        if not content.strip():
            raise SystemExit(f"Empty derived content for {row.get('uuid')}")
        records.append({
            "id": f"derived_{row['id']}",
            "artifact_type": "prompt",
            "source_prompt_id": row["id"],
            "source_uuid": row["uuid"],
            "source_url": row["official_url"],
            "source_title": row.get("title"),
            "source_category": row.get("category"),
            "source_access": "premium",
            "source_body_status": "not-public",
            "content_origin": "repository-authored-reconstruction",
            "fidelity": "metadata-derived-not-source-reproduction",
            "mode": mode,
            "variables": inputs,
            "techniques": [
                "role-assignment",
                "question-first",
                "variable-template",
                "stepwise-procedure",
                "task-decomposition",
                "explicit-constraints",
                "output-formatting",
                "self-check",
            ],
            "content": content,
            "content_sha256": sha256_text(content),
            "provenance": {
                "relation": "derived-from-public-metadata",
                "note": "Usable repository-authored reconstruction generated from public title/category plus quarry-observed architecture patterns. It is not the source premium prompt body.",
            },
        })

    records.sort(key=lambda row: (row.get("source_category") or "", row.get("source_title") or "", row["source_uuid"]))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in records:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    categories_dir = Path(args.categories_dir)
    categories_dir.mkdir(parents=True, exist_ok=True)
    for old in categories_dir.glob("*.jsonl"):
        old.unlink()
    by_category: dict[str, list[dict]] = {}
    for row in records:
        by_category.setdefault(row.get("source_category") or "Uncategorized", []).append(row)
    for category, rows in sorted(by_category.items()):
        path = categories_dir / f"{slugify(category)}.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    modes = Counter(row["mode"] for row in records)
    category_counts = Counter(row.get("source_category") or "Uncategorized" for row in records)
    manifest = {
        "source_records": len(source_rows),
        "premium_source_records": len(premium),
        "derived_records": len(records),
        "empty_content_records": sum(1 for row in records if not row["content"].strip()),
        "categories": dict(category_counts.most_common()),
        "modes": dict(modes.most_common()),
        "content_policy": "Every premium reference receives non-empty repository-authored usable content. Derived content is never labeled or represented as the original premium body.",
        "source_body_policy": "The public detail RPC returns null for premium bodies; this builder does not bypass that boundary.",
        "generator_basis": "Public source title/category plus repository-mined prompt architecture patterns from the free corpus and public Skills corpus.",
    }
    if manifest["derived_records"] != manifest["premium_source_records"] or manifest["empty_content_records"] != 0:
        raise SystemExit(f"Derived coverage check failed: {manifest}")
    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
