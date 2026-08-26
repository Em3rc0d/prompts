from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

KNOWN_CATEGORIES = [
    # Categories observed directly in the current rendered directory.
    "Finanzas Personales",
    "Redes Sociales",
    "Ideas de Negocio",
    "Desarrollo Personal",
    "Ganar Dinero",
    "Crear logos",
    "IG reels",
    "E-commerce",
    "Marketing",
    "Idiomas",
    "Abogados",
    "Programación",
    "Copywriting",
    "Profesores",
    "Ingeniería",
    "Empleo",
    "Productividad",
    "Educación",
    "Negocios",
    "Imagen",
    "Astrología",
    "Salud",
    # Historical/other source-family labels retained for compatibility.
    "Creación de Contenido",
    "Canal de YouTube Sin Rostro",
    "Crecimiento Personal",
    "Conseguir Empleo",
    "SEO y Contenido",
    "Marketing y Ventas",
    "Aprender Inglés",
    "Aprender Francés",
    "Vibe Coding",
    "Copywriting y Contenido",
    "Creatividad",
    "Fitness",
]


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def prompt_uuid(url: str) -> str | None:
    match = re.search(r"/prompts/([0-9a-fA-F-]{36})(?:$|[/?#])", url)
    return match.group(1).lower() if match else None


def infer_category(label: str) -> str | None:
    low = label.casefold()
    for category in sorted(KNOWN_CATEGORIES, key=len, reverse=True):
        if low.startswith(category.casefold() + " ") or low == category.casefold():
            return category
    return None


def clean_label(label: str) -> str:
    return " ".join(label.split()).strip()


def infer_access(label: str) -> str | None:
    match = re.search(r"\b(Gratis|Premium)\s*$", label, re.I)
    return match.group(1).lower() if match else None


def infer_model(label: str) -> str | None:
    for value in ("Cualquier modelo", "ChatGPT", "Claude", "Gemini", "Midjourney"):
        if re.search(re.escape(value), label, re.I):
            return value
    return None


def strip_markers(label: str, category: str | None, model: str | None, access: str | None) -> str:
    text = label
    if category and text.casefold().startswith(category.casefold()):
        text = text[len(category):].strip()
    if access:
        text = re.sub(rf"\b{re.escape(access)}\s*$", "", text, flags=re.I).strip()
    if model:
        text = re.sub(rf"\b{re.escape(model)}\b\s*$", "", text, flags=re.I).strip()
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/normalized/alpacka-ai-public-prompt-directory.jsonl")
    parser.add_argument("--manifest", default="quarry/normalized/alpacka-ai-public-prompt-directory-manifest.json")
    args = parser.parse_args()

    records = []
    category_counts: Counter[str] = Counter()
    access_counts: Counter[str] = Counter()
    model_counts: Counter[str] = Counter()
    unclassified = 0

    for row in read_jsonl(Path(args.input)):
        url = row.get("url") or ""
        uuid = prompt_uuid(url)
        if not uuid:
            continue
        label = clean_label(row.get("label") or "")
        category = infer_category(label)
        access = infer_access(label)
        model = infer_model(label)
        card_text = strip_markers(label, category, model, access)

        if category:
            category_counts[category] += 1
        else:
            unclassified += 1
        if access:
            access_counts[access] += 1
        if model:
            model_counts[model] += 1

        records.append({
            "id": f"alpacka_prompt_{uuid}",
            "uuid": uuid,
            "artifact_type": "prompt-reference",
            "source_id": "src_alpacka_web",
            "source_url": url,
            "official_url": url,
            "category_observed": category,
            "access_observed": access,
            "model_observed": model,
            "card_text_observed": card_text,
            "raw_label_observed": label,
            "verification": "source-url-observed",
            "capture_mode": "rendered-directory-card",
            "captured_at": row.get("captured_at"),
            "metadata": {
                "body_status": "not-fetched",
                "title_status": "embedded-in-card-text",
                "source_page": row.get("source_url"),
            },
        })

    records.sort(key=lambda r: (r.get("category_observed") or "~", r["uuid"]))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "records": len(records),
        "categories_observed": dict(category_counts.most_common()),
        "access_observed": dict(access_counts.most_common()),
        "models_observed": dict(model_counts.most_common()),
        "unclassified_category": unclassified,
        "source": str(args.input),
        "notes": [
            "Entries are public directory-card references, not verified prompt bodies.",
            "Categories are source-observed directory labels, not repository-invented classifications.",
            "card_text_observed preserves the public title/description text as one field until a detail-page metadata contract is verified.",
            "Premium content is indexed by public metadata only; no paid access is bypassed.",
        ],
    }
    manifest_path = Path(args.manifest)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
