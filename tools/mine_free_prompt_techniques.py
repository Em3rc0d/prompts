from __future__ import annotations

import argparse
import asyncio
import json
import re
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

import httpx
from playwright.async_api import async_playwright

from harvest_prompt_metadata import capture_rpc_contract, read_jsonl, replay_headers, replace_uuid, sha256_text


TECHNIQUE_ORDER = [
    "role-assignment",
    "context-injection",
    "question-first",
    "variable-template",
    "audience-definition",
    "tone-definition",
    "stepwise-procedure",
    "task-decomposition",
    "explicit-constraints",
    "output-formatting",
    "output-schema",
    "alternative-generation",
    "comparison",
    "examples-few-shot",
    "critique-revision",
    "self-check",
    "evidence-requirement",
    "confidence-labeling",
    "temporal-plan",
    "personalization",
]


def present(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, flags=re.I | re.M))


def count_numbered(text: str) -> int:
    return len(re.findall(r"(?:^|\n)\s*\d+[.)]\s+", text))


def count_bullets(text: str) -> int:
    return len(re.findall(r"(?:^|\n)\s*[-*•]\s+", text))


def variable_count(text: str) -> int:
    patterns = [
        r"\{\{\s*[^{}]{1,80}?\s*\}\}",
        r"\[\s*[^\[\]\n]{1,80}?\s*\]",
        r"<\s*[^<>\n]{1,80}?\s*>",
    ]
    return sum(len(re.findall(pattern, text)) for pattern in patterns)


def technique_vector(content: str) -> tuple[dict[str, bool], dict[str, int]]:
    low = content.casefold()
    numbered = count_numbered(content)
    bullets = count_bullets(content)
    vars_count = variable_count(content)

    techniques = {
        "role-assignment": present(r"\b(act[uú]a como|eres un|eres una|tu rol|asume el rol|comp[oó]rtate como)\b", low),
        "context-injection": present(r"\b(contexto|situaci[oó]n|datos|informaci[oó]n|antecedentes|a partir de)\b", low),
        "question-first": present(r"\b(hazme preguntas|pregunta antes|antes de (?:responder|empezar|crear)|preguntas (?:de )?aclaraci[oó]n|si falta .*pregunta|confirma primero)\b", low),
        "variable-template": vars_count > 0,
        "audience-definition": present(r"\b(audiencia|p[uú]blico objetivo|cliente ideal|lector|usuario objetivo|para qui[eé]n)\b", low),
        "tone-definition": present(r"\b(tono|voz|estilo|formal|informal|profesional|conversacional|persuasiv[oa])\b", low),
        "stepwise-procedure": numbered >= 2 or present(r"\b(paso\s*1|paso\s*2|paso a paso|primero.+despu[eé]s|finalmente)\b", low),
        "task-decomposition": numbered >= 3 or present(r"\b(divide|desglosa|separa en|por etapas|por fases|componentes|bloques)\b", low),
        "explicit-constraints": present(r"\b(no (?:inventes|debes|uses|incluyas|asumas)|debes|evita|nunca|obligatorio|restricciones?|condiciones?|m[aá]ximo|m[ií]nimo|solo|solamente)\b", low),
        "output-formatting": present(r"\b(formato|tabla|lista|secciones?|encabezados?|markdown|viñetas|bullet|estructura de salida)\b", low),
        "output-schema": present(r"\b(json|campos?|columnas?|schema|esquema|devuelve exactamente|formato de salida)\b", low),
        "alternative-generation": present(r"\b(opciones?|variantes?|alternativas?|versiones?|genera\s+\d+|prop[oó]n\s+\d+)\b", low),
        "comparison": present(r"\b(compara|comparaci[oó]n|versus|vs\.?|pros? y contras?|ventajas? y desventajas?)\b", low),
        "examples-few-shot": present(r"\b(ejemplo|por ejemplo|ej\.|como muestra|modelo de respuesta)\b", low),
        "critique-revision": present(r"\b(revisa|corrige|mejora|reescribe|audita|critica|eval[uú]a|optimiza)\b", low),
        "self-check": present(r"\b(checklist|verifica|comprueba|revisi[oó]n final|antes de entregar|aseg[uú]rate)\b", low),
        "evidence-requirement": present(r"\b(evidencia|fuentes?|datos reales|cita|referencias?|no inventes|verificable|comprobable)\b", low),
        "confidence-labeling": present(r"\b(confianza|nivel de certeza|incertidumbre|probabilidad|hip[oó]tesis|suposici[oó]n)\b", low),
        "temporal-plan": present(r"\b(plan de \d+ d[ií]as|\d+ d[ií]as|\d+ semanas|\d+ meses|semana 1|d[ií]a 1|cronograma|calendario)\b", low),
        "personalization": present(r"\b(personaliza|personalizado|seg[uú]n (?:mi|mis|tu|tus)|adaptado a|adapta .* a|en funci[oó]n de)\b", low),
    }

    features = {
        "numbered_steps": numbered,
        "bullet_lines": bullets,
        "variable_markers": vars_count,
        "question_marks": content.count("?"),
        "line_count": len(content.splitlines()),
        "paragraph_count": len([p for p in re.split(r"\n\s*\n", content) if p.strip()]),
        "characters": len(content),
    }
    return techniques, features


async def main_async(args) -> None:
    metadata = [row for row in read_jsonl(Path(args.input)) if row.get("access") == "free"]
    if not metadata:
        raise SystemExit("No free prompt metadata found.")

    first = metadata[0]
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="PromptQuarry/0.5 (+personal research; technique-vector mining)")
        contract = await capture_rpc_contract(page, first["official_url"])
        await browser.close()

    endpoint = contract["endpoint"]
    headers = replay_headers(contract["headers"])
    template_body = contract["body"]
    if not isinstance(template_body, (dict, list)):
        raise SystemExit("Could not identify structured RPC body.")
    first_uuid = first["uuid"]

    vectors = []
    technique_counts: Counter[str] = Counter()
    signature_counts: Counter[str] = Counter()
    category_technique: dict[str, Counter[str]] = defaultdict(Counter)
    category_count: Counter[str] = Counter()
    feature_totals: Counter[str] = Counter()

    async with httpx.AsyncClient(timeout=30.0, headers=headers, follow_redirects=True) as client:
        for row in metadata:
            uuid = row["uuid"]
            body = replace_uuid(deepcopy(template_body), first_uuid, uuid)
            response = await client.post(endpoint, json=body)
            if response.status_code == 429:
                await asyncio.sleep(3)
                response = await client.post(endpoint, json=body)
            if response.status_code in {401, 403}:
                raise SystemExit(f"RPC access boundary changed: HTTP {response.status_code}")
            response.raise_for_status()
            payload = response.json()
            if payload.get("is_premium"):
                raise SystemExit(f"Expected free record but RPC marks premium: {uuid}")
            content = payload.get("content")
            if not isinstance(content, str) or not content:
                raise SystemExit(f"Free prompt content unavailable: {uuid}")

            techniques, features = technique_vector(content)
            present_techniques = [name for name in TECHNIQUE_ORDER if techniques.get(name)]
            signature = "+".join(present_techniques) or "none"
            category = payload.get("category") or row.get("category") or "Uncategorized"

            for name in present_techniques:
                technique_counts[name] += 1
                category_technique[category][name] += 1
            signature_counts[signature] += 1
            category_count[category] += 1
            for key, value in features.items():
                feature_totals[key] += value

            vectors.append({
                "id": row["id"],
                "uuid": uuid,
                "title": payload.get("title"),
                "category": category,
                "official_url": row["official_url"],
                "content_sha256": sha256_text(content),
                "content_length": len(content),
                "techniques": present_techniques,
                "architecture_signature": signature,
                "features": features,
                "verification": "source-api-observed",
                "capture_mode": "in-memory-technique-mining",
                "body_stored": False,
            })

            if args.delay_ms:
                await asyncio.sleep(args.delay_ms / 1000)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for row in vectors:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    total = len(vectors)
    matrix = {
        "records": total,
        "source": str(args.input),
        "body_storage_policy": "Free prompt bodies are fetched from the public RPC, analyzed in memory and discarded. Only fingerprints, technique vectors and aggregate features are written.",
        "technique_presence": {
            name: {"count": count, "percent": round(count * 100 / total, 2)}
            for name, count in technique_counts.most_common()
        },
        "top_architecture_signatures": [
            {"signature": signature, "count": count, "percent": round(count * 100 / total, 2)}
            for signature, count in signature_counts.most_common(25)
        ],
        "category_counts": dict(category_count.most_common()),
        "category_technique_presence": {
            category: {
                name: {
                    "count": count,
                    "percent": round(count * 100 / category_count[category], 2),
                }
                for name, count in counts.most_common()
            }
            for category, counts in sorted(category_technique.items())
        },
        "average_features": {
            key: round(value / total, 2) for key, value in feature_totals.items()
        },
    }
    matrix_path = Path(args.matrix)
    matrix_path.parent.mkdir(parents=True, exist_ok=True)
    matrix_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(matrix, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/analysis/alpacka-ai-free-technique-vectors.jsonl")
    parser.add_argument("--matrix", default="quarry/analysis/alpacka-ai-free-technique-matrix.json")
    parser.add_argument("--delay-ms", type=int, default=150)
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
