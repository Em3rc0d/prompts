from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from common import canonicalize, read_jsonl, sha256_text, slugify, write_jsonl


def classify(text: str) -> tuple[str, float, list[str], list[str]]:
    low = text.lower()
    techniques: list[str] = []
    categories: list[str] = []

    if re.search(r"\b(act[uú]a como|eres un|role:)\b", low):
        techniques.append("role-assignment")
    if re.search(r"\b(paso 1|paso 2|step 1|step 2|primero|despu[eé]s|finalmente)\b", low):
        techniques.append("stepwise-procedure")
    if any(token in low for token in ("formato", "json", "tabla", "estructura de salida")):
        techniques.append("output-formatting")
    if "[" in text and "]" in text:
        techniques.append("variable-template")
    if any(token in low for token in ("fuentes", "cita", "evidencia")):
        techniques.append("source-requirement")

    if any(token in low for token in ("código", "codigo", "debug", "api", "arquitectura", "software")):
        categories.append("software/coding")
    if any(token in low for token in ("marketing", "ventas", "cliente", "negocio")):
        categories.append("business/marketing")
    if any(token in low for token in ("reescribe", "texto", "redacción", "redaccion", "editor")):
        categories.append("content/editing")
    if any(token in low for token in ("investiga", "research", "analiza", "fuentes")):
        categories.append("research/analysis")

    steps = len(re.findall(r"(?:^|\n)\s*(?:\d+[.)]|[-*])\s+", text))
    prompt_signal = bool(re.search(r"\b(prompt|act[uú]a como|tu tarea|debes|genera|crea|analiza|reescribe)\b", low))
    if steps >= 4 and len(text) > 500:
        return "workflow", 0.72, categories, techniques
    if prompt_signal:
        return "prompt", 0.78, categories, techniques
    return "reference", 0.45, categories, techniques


def normalize_record(raw: dict) -> dict:
    text = canonicalize(raw.get("body") or "")
    artifact_type, confidence, categories, techniques = classify(text)
    source_key = raw.get("source_key") or sha256_text(raw.get("source_url") or text)[7:23]
    source_id = raw.get("source_id") or "unknown"

    return {
        "id": f"candidate_{slugify(source_id)}_{slugify(str(source_key), 40)}",
        "artifact_type": artifact_type,
        "classification_confidence": confidence,
        "title": raw.get("title"),
        "source_id": source_id,
        "source_url": raw.get("source_url") or "https://invalid.local/unknown",
        "official_post_url": raw.get("official_post_url"),
        "raw_url": raw.get("raw_url"),
        "source_snapshot_path": raw.get("source_snapshot_path"),
        "author": raw.get("author"),
        "published_at": raw.get("published_at"),
        "captured_at": raw.get("captured_at"),
        "capture_mode": raw.get("capture_mode", "derived-analysis"),
        "verification": raw.get("verification", "unverified"),
        "language": "es" if re.search(r"\b(que|para|como|de|el|la)\b", text.lower()) else "unknown",
        "model_targets": [],
        "categories": sorted(set(categories)),
        "tags": [],
        "techniques": sorted(set(techniques)),
        "body": text or None,
        "summary": None,
        "variables": sorted(set(re.findall(r"\[([^\]]{1,80})\]", text))),
        "observed_titles": [],
        "fingerprint": sha256_text(text) if text else None,
        "duplicate_of": None,
        "provenance": [{"url": raw.get("source_url") or "https://invalid.local/unknown", "relation": "primary", "note": None}],
        "metadata": {
            "quarry_record_type": raw.get("quarry_record_type"),
            "classification_status": "candidate-needs-review",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize raw quarry JSONL into review candidates.")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--output", default="quarry/normalized/candidates.jsonl")
    args = parser.parse_args()

    merged: dict[str, dict] = {}
    for input_path in args.inputs:
        for raw in read_jsonl(input_path):
            record = normalize_record(raw)
            key = record.get("fingerprint") or record["id"]
            if key not in merged:
                merged[key] = record
            else:
                existing = merged[key]
                url = record["source_url"]
                if not any(p["url"] == url for p in existing["provenance"]):
                    existing["provenance"].append({"url": url, "relation": "discovery", "note": "Duplicate observation."})

    count = write_jsonl(args.output, merged.values())
    print(json.dumps({"status": "ok", "records": count, "output": str(Path(args.output))}, indent=2))


if __name__ == "__main__":
    main()
