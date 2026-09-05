from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

ETL_VERSION = "1.0.0"
HIGH_STAKES_CATEGORIES = {"Abogados", "Salud", "Finanzas Personales"}
CORE_SECTIONS = {
    "objective": ("OBJETIVO",),
    "intake": ("INTAKE", "ENTRADA", "INFORMACIÓN NECESARIA", "INFORMACION NECESARIA"),
    "process": ("PROCESO", "PROCESS", "MÉTODO", "METODO"),
    "constraints": ("REGLAS", "RESTRICCIONES", "CONSTRAINTS"),
    "output": ("FORMATO DE SALIDA", "OUTPUT CONTRACT", "SALIDA", "ENTREGABLE"),
}


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                rows.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_heading(line: str) -> str:
    value = line.strip().upper().rstrip(":")
    value = re.sub(r"^[#*\-\d.\s]+", "", value)
    return value.strip()


def has_heading(body: str, aliases: tuple[str, ...]) -> bool:
    expected = {alias.upper().rstrip(":") for alias in aliases}
    return any(normalize_heading(line) in expected for line in body.splitlines())


def has_any(body: str, *terms: str) -> bool:
    low = body.casefold()
    return any(term.casefold() in low for term in terms)


def instruction_data_boundary(body: str) -> bool:
    low = body.casefold()
    patterns = [
        r"instrucciones?\s+(?:embebidas?|incluidas?|contenidas?)\s+.*(?:datos?|evidencia|c[oó]digo|logs?)",
        r"(?:trata|tratar|considere|considera)\s+.*(?:c[oó]digo|logs?|documentos?|tickets?|contenido).*\s+como\s+datos",
        r"(?:no|nunca)\s+(?:sigas?|obedezcas?|ejecutes?)\s+instrucciones?.*(?:dentro|embebidas?|contenidas?)",
        r"instructions?\s+(?:inside|embedded in).*(?:data|code|logs?|documents?)",
        r"treat.*(?:code|logs?|documents?|tickets?|content).*as\s+data",
    ]
    return any(re.search(pattern, low, re.I | re.S) for pattern in patterns)


def evidence_discipline(body: str) -> bool:
    return has_any(
        body,
        "no inventes",
        "no inventar",
        "supuesto",
        "supuestos",
        "inferencia",
        "evidencia",
        "unknown",
        "desconocido",
    )


def uncertainty_discipline(body: str) -> bool:
    return has_any(
        body,
        "si falta información",
        "si falta informacion",
        "si no hay suficiente",
        "pregunta antes",
        "marca como supuesto",
        "vacíos de información",
        "vacios de informacion",
        "unknown",
        "incertidumbre",
    )


def verification_present(body: str) -> bool:
    return has_any(
        body,
        "auto-verificación",
        "auto-verificacion",
        "verificación",
        "verificacion",
        "checklist",
        "quality gate",
    )


def high_stakes_safety(body: str) -> bool:
    return has_any(body, "profesional cualificado", "profesional calificado") and has_any(
        body, "información educativa", "informacion educativa", "educativa/general", "asesoría profesional", "asesoria profesional"
    )


def skeletonize(body: str, source_title: str | None = None) -> str:
    """Remove record-specific decoration while preserving workflow architecture.

    This fingerprint is intentionally aggressive. It is used to detect when many
    records are mostly title/role/variable variants of the same generated shell.
    It is not a semantic-equivalence claim.
    """

    text = body
    if source_title:
        text = re.sub(re.escape(source_title), "<OBJECTIVE>", text, flags=re.I)

    lines: list[str] = []
    previous_variable = False
    after_objective_heading = False

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        upper = normalize_heading(line)
        if upper == "OBJETIVO":
            lines.append("OBJETIVO")
            after_objective_heading = True
            previous_variable = False
            continue

        if after_objective_heading:
            lines.append("<OBJECTIVE>")
            after_objective_heading = False
            previous_variable = False
            continue

        if re.match(r"^act[uú]a\s+como\b", line, re.I):
            lines.append("ACTUA COMO <ROLE>")
            previous_variable = False
            continue

        normalized = re.sub(r"\{[^{}]+\}", "{VAR}", line)
        if normalized == "- {VAR}":
            if previous_variable:
                continue
            lines.append("- {VAR}")
            previous_variable = True
            continue

        previous_variable = False
        normalized = re.sub(r"\s+", " ", normalized).casefold().strip()
        lines.append(normalized)

    return "\n".join(lines)


def validate_unique(rows: list[dict], field: str, label: str) -> None:
    seen: set[str] = set()
    duplicates: list[str] = []
    for row in rows:
        value = row.get(field)
        if not value:
            continue
        value = str(value)
        if value in seen:
            duplicates.append(value)
        seen.add(value)
    if duplicates:
        raise SystemExit(f"Duplicate {label}: {sorted(set(duplicates))[:10]}")


def structural_signals(body: str) -> dict:
    return {
        "objective": has_heading(body, CORE_SECTIONS["objective"]),
        "intake": has_heading(body, CORE_SECTIONS["intake"]),
        "process": has_heading(body, CORE_SECTIONS["process"]),
        "constraints": has_heading(body, CORE_SECTIONS["constraints"]),
        "output_contract": has_heading(body, CORE_SECTIONS["output"]),
        "verification": verification_present(body),
        "evidence_discipline": evidence_discipline(body),
        "uncertainty_discipline": uncertainty_discipline(body),
        "instruction_data_boundary": instruction_data_boundary(body),
    }


def differentiation_points(cluster_size: int) -> int:
    if cluster_size <= 1:
        return 6
    if cluster_size <= 3:
        return 4
    if cluster_size <= 5:
        return 2
    return 0


def score_record(signals: dict, cluster_size: int, provenance_ok: bool) -> tuple[int, dict[str, int]]:
    points = {
        "provenance_integrity": 15 if provenance_ok else 0,
        "objective": 8 if signals["objective"] else 0,
        "intake": 8 if signals["intake"] else 0,
        "process": 10 if signals["process"] else 0,
        "constraints": 10 if signals["constraints"] else 0,
        "output_contract": 10 if signals["output_contract"] else 0,
        "verification": 5 if signals["verification"] else 0,
        "evidence_discipline": 10 if signals["evidence_discipline"] else 0,
        "uncertainty_discipline": 8 if signals["uncertainty_discipline"] else 0,
        "instruction_data_boundary": 10 if signals["instruction_data_boundary"] else 0,
        "structural_differentiation": differentiation_points(cluster_size),
    }
    score = sum(points.values())
    assert score <= 100, points
    return score, points


def assess(
    source: dict,
    derived: dict,
    cluster_size: int,
    skeleton_sha256: str,
) -> dict:
    body = str(derived.get("content") or "")
    signals = structural_signals(body)
    high_stakes = source.get("category") in HIGH_STAKES_CATEGORIES

    integrity_failures: list[str] = []
    if source.get("access") != "premium":
        integrity_failures.append("SOURCE_NOT_PREMIUM")
    if derived.get("source_access") != "premium":
        integrity_failures.append("DERIVED_ACCESS_MISMATCH")
    if derived.get("source_prompt_id") != source.get("id"):
        integrity_failures.append("SOURCE_ID_MISMATCH")
    if derived.get("source_uuid") != source.get("uuid"):
        integrity_failures.append("SOURCE_UUID_MISMATCH")
    if derived.get("source_body_status") != "not-public":
        integrity_failures.append("SOURCE_BODY_BOUNDARY_MISMATCH")
    if derived.get("content_origin") != "repository-authored-reconstruction":
        integrity_failures.append("CONTENT_ORIGIN_MISMATCH")
    if not body.strip():
        integrity_failures.append("EMPTY_CONTENT")

    provenance_ok = not integrity_failures
    score, score_breakdown = score_record(signals, cluster_size, provenance_ok)

    blockers: list[str] = []
    for name in ("objective", "process", "constraints", "output_contract"):
        if not signals[name]:
            blockers.append(f"MISSING_{name.upper()}")
    if len(body.strip()) < 400:
        blockers.append("CONTENT_TOO_SMALL_FOR_WORKFLOW")
    if not signals["instruction_data_boundary"]:
        blockers.append("MISSING_INSTRUCTION_DATA_BOUNDARY")
    if cluster_size > 5:
        blockers.append("MATERIAL_TEMPLATE_CLONE_CLUSTER")
    if high_stakes and not high_stakes_safety(body):
        blockers.append("HIGH_STAKES_SAFETY_BOUNDARY_MISSING")

    if integrity_failures:
        state = "REJECTED"
    elif high_stakes:
        state = "HIGH_STAKES_REVIEW_REQUIRED"
    elif score >= 90 and not blockers:
        state = "STATIC_QUALIFIED_NOT_FOR_SALE"
    else:
        state = "REWORK_REQUIRED"

    return {
        "etl_version": ETL_VERSION,
        "candidate_id": derived.get("id"),
        "source_prompt_id": source.get("id"),
        "source_uuid": source.get("uuid"),
        "title": source.get("title"),
        "category": source.get("category"),
        "mode": derived.get("mode"),
        "risk_class": "HIGH_STAKES" if high_stakes else "STANDARD",
        "state": state,
        "static_quality_score": score,
        "score_breakdown": score_breakdown,
        "signals": signals,
        "high_stakes_safety_boundary": high_stakes_safety(body) if high_stakes else None,
        "word_count": len(re.findall(r"\S+", body)),
        "character_count": len(body),
        "variable_count": len(derived.get("variables") or []),
        "content_sha256": sha256_text(body),
        "skeleton_sha256": skeleton_sha256,
        "clone_cluster_size": cluster_size,
        "integrity_failures": integrity_failures,
        "blocking_reasons": blockers,
        "product_eligible": False,
        "ready_to_sell": False,
        "behavioral_evidence": False,
    }


def choose_representative(rows: list[dict]) -> dict:
    """Prefer standard-risk, then stronger static score, then deterministic ID."""
    ordered = sorted(
        rows,
        key=lambda row: (
            1 if row["risk_class"] == "HIGH_STAKES" else 0,
            -row["static_quality_score"],
            row.get("category") or "",
            row.get("title") or "",
            row.get("candidate_id") or "",
        ),
    )
    return ordered[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Quality-first deterministic ETL for Prompt Quarry reconstructions.")
    parser.add_argument(
        "--source",
        default="quarry/normalized/alpacka-ai-prompt-metadata.jsonl",
        help="Normalized source prompt metadata JSONL.",
    )
    parser.add_argument(
        "--derived",
        default="library/prompts/alpacka/derived-premium/catalog.jsonl",
        help="Repository-authored reconstruction catalog JSONL.",
    )
    parser.add_argument(
        "--output-dir",
        default="quarry/etl/prompt-library-v1",
        help="Review/evidence output directory. Never a product catalog path.",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    derived_path = Path(args.derived)
    output_dir = Path(args.output_dir)

    sources = read_jsonl(source_path)
    derived_rows = read_jsonl(derived_path)
    premium_sources = [row for row in sources if row.get("access") == "premium"]

    validate_unique(sources, "id", "source IDs")
    validate_unique(sources, "uuid", "source UUIDs")
    validate_unique(derived_rows, "id", "derived IDs")
    validate_unique(derived_rows, "source_prompt_id", "derived source_prompt_id values")
    validate_unique(derived_rows, "source_uuid", "derived source_uuid values")

    source_by_id = {row["id"]: row for row in premium_sources}
    derived_by_source = {row.get("source_prompt_id"): row for row in derived_rows}

    missing_derived = sorted(set(source_by_id) - set(derived_by_source))
    orphan_derived = sorted(set(derived_by_source) - set(source_by_id))
    if missing_derived or orphan_derived:
        raise SystemExit(
            f"Join integrity failed: missing_derived={missing_derived[:10]} orphan_derived={orphan_derived[:10]}"
        )

    skeleton_by_source: dict[str, str] = {}
    cluster_members: dict[str, list[str]] = defaultdict(list)
    for source_id, source in source_by_id.items():
        derived = derived_by_source[source_id]
        body = str(derived.get("content") or "")
        skeleton = skeletonize(body, source.get("title"))
        skeleton_sha = sha256_text(skeleton)
        skeleton_by_source[source_id] = skeleton_sha
        cluster_members[skeleton_sha].append(source_id)

    quality_rows: list[dict] = []
    by_cluster_assessments: dict[str, list[dict]] = defaultdict(list)
    for source_id in sorted(source_by_id):
        source = source_by_id[source_id]
        derived = derived_by_source[source_id]
        skeleton_sha = skeleton_by_source[source_id]
        assessment = assess(source, derived, len(cluster_members[skeleton_sha]), skeleton_sha)
        quality_rows.append(assessment)
        by_cluster_assessments[skeleton_sha].append(assessment)

    cluster_rows: list[dict] = []
    representatives: list[dict] = []
    for skeleton_sha, members in sorted(by_cluster_assessments.items()):
        representative = choose_representative(members)
        representatives.append({
            "skeleton_sha256": skeleton_sha,
            "cluster_size": len(members),
            "representative_candidate_id": representative["candidate_id"],
            "representative_source_prompt_id": representative["source_prompt_id"],
            "representative_title": representative["title"],
            "representative_category": representative["category"],
            "representative_mode": representative["mode"],
            "representative_static_quality_score": representative["static_quality_score"],
            "representative_state": representative["state"],
            "review_scope": "STRUCTURAL_REPRESENTATIVE_ONLY",
            "product_eligible": False,
            "ready_to_sell": False,
        })
        cluster_rows.append({
            "skeleton_sha256": skeleton_sha,
            "cluster_size": len(members),
            "modes": sorted({row.get("mode") for row in members if row.get("mode")}),
            "categories": sorted({row.get("category") for row in members if row.get("category")}),
            "state_counts": dict(Counter(row["state"] for row in members)),
            "score_min": min(row["static_quality_score"] for row in members),
            "score_max": max(row["static_quality_score"] for row in members),
            "representative_candidate_id": representative["candidate_id"],
            "representative_title": representative["title"],
            "member_candidate_ids": sorted(row["candidate_id"] for row in members),
        })

    representatives.sort(
        key=lambda row: (
            -row["representative_static_quality_score"],
            row["cluster_size"],
            row["representative_category"] or "",
            row["representative_title"] or "",
        )
    )
    cluster_rows.sort(key=lambda row: (-row["cluster_size"], row["skeleton_sha256"]))

    state_counts = Counter(row["state"] for row in quality_rows)
    high_stakes_count = sum(1 for row in quality_rows if row["risk_class"] == "HIGH_STAKES")
    clone_heavy_count = sum(1 for row in quality_rows if row["clone_cluster_size"] > 5)
    missing_instruction_boundary_count = sum(
        1 for row in quality_rows if not row["signals"]["instruction_data_boundary"]
    )

    manifest = {
        "schema": "prompt-machine-library-etl-v1",
        "etl_version": ETL_VERSION,
        "status": "STATIC_SCREEN_COMPLETE",
        "source_path": str(source_path),
        "derived_path": str(derived_path),
        "source_records": len(sources),
        "premium_source_records": len(premium_sources),
        "derived_records": len(derived_rows),
        "joined_records": len(quality_rows),
        "structural_skeletons": len(cluster_rows),
        "representative_review_records": len(representatives),
        "state_counts": dict(state_counts),
        "high_stakes_records": high_stakes_count,
        "clone_heavy_records": clone_heavy_count,
        "missing_instruction_data_boundary_records": missing_instruction_boundary_count,
        "largest_clone_cluster": max((row["cluster_size"] for row in cluster_rows), default=0),
        "automatic_sellable_promotions": 0,
        "external_model_calls": 0,
        "behavioral_claims_created": 0,
        "ready_to_sell_claims_created": 0,
        "quality_first_rule": "Review one representative per structural skeleton before spending effort on every generated record.",
        "claim_boundary": "STATIC_QUALIFIED_NOT_FOR_SALE is static eligibility only; it is not F4/F5/F6/F7 evidence and not product readiness.",
    }

    if manifest["premium_source_records"] != manifest["derived_records"]:
        raise SystemExit(f"Coverage mismatch: {manifest}")
    if manifest["joined_records"] != manifest["premium_source_records"]:
        raise SystemExit(f"Join mismatch: {manifest}")
    if manifest["automatic_sellable_promotions"] != 0:
        raise SystemExit("ETL must never auto-promote a prompt to sellable state.")

    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / "quality-report.jsonl", quality_rows)
    write_jsonl(output_dir / "representative-review.jsonl", representatives)
    (output_dir / "clone-clusters.json").write_text(
        json.dumps(cluster_rows, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
