from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from mk1_prompt_generator_v0 import generate

REQUEST = Path("mk1/generator/examples/software-review.request.json")
SCHEMA = Path("product/specs/PRODUCT_MANIFEST.schema.json")
DEFAULT_OUTPUT = Path("product/developer-pack-v1/package")
CANONICAL_GENERATOR_RECEIPT = Path(".ci/mk1-prompt-generator-v0/latest.json")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def prompt_markdown(result: dict) -> str:
    artifact = result["artifact"]
    architecture = result["architecture"]
    return (
        "# Software Code Review Prompt\n\n"
        "**Maturity:** `VALID`  \n"
        "**Claims:** `engineered`, `valid`  \n"
        "**Boundary:** This prompt passed Prompt Quarry static contracts. It is not claimed as TESTED, IMPROVED, CERTIFIED, or PORTABLE.\n\n"
        f"**Architecture:** `{architecture['architecture_signature']}`\n\n"
        "## Prompt\n\n"
        + artifact["prompt_body"].strip()
        + "\n"
    )


def artifact_entry(
    artifact_id: str,
    physical_path: Path,
    manifest_path: Path,
    artifact_type: str,
    provenance_class: str,
    maturity_state: str,
    claims: list[str],
    evidence_refs: list[str],
    prompt_family: str | None = None,
) -> dict:
    entry = {
        "artifact_id": artifact_id,
        "path": manifest_path.as_posix(),
        "artifact_type": artifact_type,
        "authority": "prompt-quarry",
        "provenance_class": provenance_class,
        "maturity_state": maturity_state,
        "claims": claims,
        "evidence_refs": evidence_refs,
        "sha256": sha256_file(physical_path),
        "media_type": "text/markdown" if physical_path.suffix == ".md" else "application/json",
        "distribution": {
            "include": True,
            "customer_visible": True,
            "redistributable": True,
            "notes": "Prompt Quarry-authored or sanitized MK1-derived product asset; no third-party source body is bundled.",
        },
    }
    if prompt_family is not None:
        entry["prompt_family"] = prompt_family
    return entry


def validate_manifest(manifest: dict) -> None:
    schema = load_json(SCHEMA)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(manifest), key=lambda e: list(e.absolute_path))
    if errors:
        rendered = []
        for error in errors:
            where = ".".join(str(x) for x in error.absolute_path) or "<root>"
            rendered.append(f"{where}: {error.message}")
        raise ValueError("Developer Pack manifest validation failed:\n- " + "\n- ".join(rendered))


def enforce_export_boundary(root: Path) -> None:
    # MANIFEST.json may name the canonical build receipt as evidence metadata.
    # Customer-facing assets must never expose private quarry paths/source IDs.
    forbidden = ("mk0/", "quarry/", "src_alpacka", "golden-dataset/", ".ci/")
    violations = []
    for path in root.rglob("*"):
        if not path.is_file() or path.name == "MANIFEST.json":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [token for token in forbidden if token in text]
        if hits:
            violations.append(f"{path}: {hits}")
    if violations:
        raise ValueError("Private/internal provenance leaked into product export:\n- " + "\n- ".join(violations))


def build(output: Path, source_commit: str, source_branch: str) -> dict:
    if len(source_commit) != 40 or any(ch not in "0123456789abcdef" for ch in source_commit):
        raise ValueError("source_commit must be a lowercase 40-character Git SHA")

    receipt = load_json(CANONICAL_GENERATOR_RECEIPT)
    if receipt.get("status") != "PASS":
        raise ValueError("Generator v0 canonical receipt must be PASS before product build")

    result = generate(load_json(REQUEST))
    if result["generator_status"] not in {"VALID_STATIC", "WARN_STATIC"}:
        raise ValueError(f"Generator output is not distributable at VALID maturity: {result['generator_status']}")
    if result["artifact"]["state"] != "VALID":
        raise ValueError(f"Expected VALID artifact, got {result['artifact']['state']}")

    example = output / "examples" / "software-code-review"
    output.mkdir(parents=True, exist_ok=True)
    example.mkdir(parents=True, exist_ok=True)

    lint = result["lint"]
    critic = result["critic"]
    quality_payload = {
        "schema": "prompt-quarry-product-static-quality-v1",
        "generator_version": result["generator_version"],
        "generator_status": result["generator_status"],
        "artifact_id": result["artifact"]["id"],
        "artifact_state": result["artifact"]["state"],
        "lint": {
            "version": lint.get("linter_version"),
            "status": lint["status"],
            "error_count": lint["error_count"],
            "warning_count": lint["warning_count"],
            "blocking_count": lint["blocking_count"],
            "findings": lint["findings"],
        },
        "critic": {
            "version": critic.get("critic_version"),
            "status": critic["status"],
            "error_count": critic.get("error_count", 0),
            "warning_count": critic.get("warning_count", 0),
            "blocking_count": critic.get("blocking_count", 0),
            "findings": critic.get("findings", []),
        },
        "maturity_state": "VALID",
        "claims": ["engineered", "valid"],
        "claim_boundary": result["claim_boundary"],
    }
    evaluation_payload = {
        "schema": "prompt-quarry-product-evaluation-guidance-v1",
        "artifact_id": result["artifact"]["id"],
        "evaluation_plan": result["evaluation_plan"],
        "current_maturity": "VALID",
        "next_evidence_gate": "F4 real behavioral observation before TESTED may be claimed.",
        "claim_boundary": "This file is evaluation guidance, not behavioral evidence.",
    }
    metadata_payload = {
        "schema": "prompt-quarry-product-prompt-metadata-v1",
        "artifact_id": result["artifact"]["id"],
        "title": result["artifact"]["title"],
        "domain": result["artifact"]["domain"],
        "intent": result["artifact"]["intent"],
        "risk": result["artifact"]["risk"],
        "language": result["artifact"]["language"],
        "model_targets": result["artifact"]["model_targets"],
        "maturity_state": "VALID",
        "claims": ["engineered", "valid"],
        "architecture_signature": result["architecture"]["architecture_signature"],
        "techniques": result["architecture"]["techniques"],
        "claim_boundary": result["claim_boundary"],
    }

    payloads = {
        example / "request.json": result["request"],
        example / "task-brief.json": result["brief"],
        example / "architecture.json": result["architecture"],
        example / "static-quality.json": quality_payload,
        example / "evaluation-guidance.json": evaluation_payload,
        example / "prompt-metadata.json": metadata_payload,
    }
    for path, payload in payloads.items():
        write_json(path, payload)
    prompt_path = example / "prompt.md"
    prompt_path.write_text(prompt_markdown(result), encoding="utf-8")

    enforce_export_boundary(output)

    evidence_ref = f"generator-ci:{receipt['source_commit']}"
    rel = lambda path: path.relative_to(output)
    artifacts = [
        artifact_entry("pq-devpack-code-review-request", example / "request.json", rel(example / "request.json"), "prompt-request-example", "example", "DRAFT", ["engineered"], []),
        artifact_entry("pq-devpack-code-review-brief", example / "task-brief.json", rel(example / "task-brief.json"), "task-brief-example", "mk1-derived", "VALID", ["engineered", "valid"], [evidence_ref]),
        artifact_entry("pq-devpack-code-review-architecture", example / "architecture.json", rel(example / "architecture.json"), "example", "mk1-derived", "VALID", ["engineered", "valid"], [evidence_ref]),
        artifact_entry("pq-devpack-code-review-prompt", prompt_path, rel(prompt_path), "prompt-artifact", "mk1-derived", "VALID", ["engineered", "valid"], [evidence_ref], "software_code_review"),
        artifact_entry("pq-devpack-code-review-quality", example / "static-quality.json", rel(example / "static-quality.json"), "example", "mk1-derived", "VALID", ["engineered", "valid"], [evidence_ref]),
        artifact_entry("pq-devpack-code-review-evaluation", example / "evaluation-guidance.json", rel(example / "evaluation-guidance.json"), "example", "product-authored", "DRAFT", ["engineered"], []),
        artifact_entry("pq-devpack-code-review-metadata", example / "prompt-metadata.json", rel(example / "prompt-metadata.json"), "example", "mk1-derived", "VALID", ["engineered", "valid"], [evidence_ref]),
    ]

    manifest = {
        "schema": "prompt-quarry-product-manifest-v1",
        "product_id": "pq-developer-pack",
        "product_name": "Prompt Quarry Developer Pack",
        "version": "0.1.0-draft",
        "release_status": "DRAFT",
        "source_branch": source_branch,
        "source_commit": source_commit,
        "generated_at": utc_now(),
        "pack_root": "prompt-quarry-developer-pack-v1/",
        "generator_v0": {
            "bundled": False,
            "gate": "canonical-static-ci-pass-required-before-bundling",
            "canonical_receipt": ".ci/mk1-prompt-generator-v0/latest.json",
            "receipt_status": receipt["status"],
            "receipt_source_commit": receipt["source_commit"],
        },
        "artifacts": artifacts,
        "forbidden_bundle_classes": [
            "credentials",
            "private-research-internals",
            "raw-third-party-premium-bodies",
            "unreviewed-source-harvest-data",
            "synthetic-output-presented-as-real-runtime-evidence",
        ],
        "claim_boundary": "Commercial distribution does not promote MK1 maturity. This draft contains a sanitized VALID software-code-review example only. TESTED requires F4 real evidence; IMPROVED/CANDIDATE requires F5 superiority; CERTIFIED requires F6 repeated same-target evidence; PORTABLE requires F7 cross-provider evidence.",
    }
    validate_manifest(manifest)
    write_json(output / "MANIFEST.json", manifest)
    enforce_export_boundary(output)

    build_receipt = {
        "schema": "prompt-quarry-developer-pack-build-receipt-v1",
        "status": "PASS",
        "source_commit": source_commit,
        "generator_receipt_source_commit": receipt["source_commit"],
        "generator_status": result["generator_status"],
        "artifact_state": result["artifact"]["state"],
        "exported_artifacts": len(artifacts),
        "manifest_sha256": sha256_file(output / "MANIFEST.json"),
        "export_boundary": "PASS",
        "claim_boundary": "Build PASS establishes reproducible sanitized product assembly and static validity only; it does not establish behavioral superiority or certification.",
    }
    write_json(output / "BUILD-RECEIPT.json", build_receipt)
    return build_receipt


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Prompt Quarry Developer Pack v1 draft")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source-branch", default="feat/mk1-prompt-generator-v0-20260827")
    args = parser.parse_args()
    receipt = build(args.output, args.source_commit, args.source_branch)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
