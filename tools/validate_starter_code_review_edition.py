#!/usr/bin/env python3
"""Independent pack-level QA for Starter — Code Review Edition v1."""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path

EXPECTED_MEMBERS = [
    "README.md",
    "QUICKSTART.md",
    "WORKFLOW.md",
    "EVIDENCE.md",
    "RELEASE-NOTICE.md",
    "MANIFEST.json",
]
EXPECTED_WORKFLOW_BYTES = 25295
EXPECTED_WORKFLOW_SHA256 = "6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977"
EXPECTED_MODEL = "gemini-3.5-flash"
EXPECTED_CERTIFICATION = "PM-CERT-STARTER-CR-V2.2-GEMINI-SCOPE-001"
EXPECTED_FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True)
    args = parser.parse_args()
    archive = Path(args.archive).resolve()

    checks: dict[str, bool] = {"archive_exists": archive.is_file()}
    if not archive.is_file():
        print(json.dumps({"verdict": "FAIL", "checks": checks}, indent=2, sort_keys=True))
        return 2

    with zipfile.ZipFile(archive, "r") as zf:
        infos = zf.infolist()
        names = [i.filename for i in infos]
        checks["member_order_exact"] = names == EXPECTED_MEMBERS
        checks["member_count_exact"] = len(names) == len(EXPECTED_MEMBERS)
        checks["members_unique"] = len(names) == len(set(names))
        checks["crc_integrity"] = zf.testzip() is None
        checks["fixed_timestamps"] = all(i.date_time == EXPECTED_FIXED_TIME for i in infos)
        checks["regular_file_modes"] = all(
            stat.S_IFMT((i.external_attr >> 16) & 0xFFFF) == stat.S_IFREG
            and (((i.external_attr >> 16) & 0o777) == 0o644)
            for i in infos
        )
        checks["no_directory_members"] = all(not n.endswith("/") for n in names)

        data = {name: zf.read(name) for name in names}
        workflow = data.get("WORKFLOW.md", b"")
        checks["workflow_bytes_exact"] = len(workflow) == EXPECTED_WORKFLOW_BYTES
        checks["workflow_sha256_exact"] = sha256(workflow) == EXPECTED_WORKFLOW_SHA256

        try:
            manifest = json.loads(data.get("MANIFEST.json", b"").decode("utf-8"))
            checks["manifest_parseable"] = True
        except Exception:
            manifest = {}
            checks["manifest_parseable"] = False

        checks["manifest_status_not_for_sale"] = manifest.get("status") == "RELEASE_CANDIDATE_NOT_FOR_SALE"
        checks["manifest_public_sale_false"] = manifest.get("public_sale") is False
        checks["manifest_customer_license_not_frozen"] = manifest.get("customer_license_frozen") is False
        checks["manifest_model_specific"] = manifest.get("portability_classification") == "MODEL_SPECIFIC"
        checks["manifest_validated_model_exact"] = manifest.get("validated_model") == EXPECTED_MODEL
        checks["manifest_certification_exact"] = manifest.get("certification_id") == EXPECTED_CERTIFICATION
        checks["manifest_claim_boundary_exact"] = manifest.get("claim_boundary") == "MODEL_SPECIFIC_GEMINI_3_5_FLASH_FROZEN_MATRIX_ONLY"
        checks["manifest_workflow_identity_exact"] = (
            (manifest.get("workflow") or {}).get("bytes") == EXPECTED_WORKFLOW_BYTES
            and (manifest.get("workflow") or {}).get("sha256") == EXPECTED_WORKFLOW_SHA256
        )

        declared_members = manifest.get("members") or {}
        checks["manifest_payload_member_set_exact"] = set(declared_members) == set(EXPECTED_MEMBERS) - {"MANIFEST.json"}
        for name in EXPECTED_MEMBERS:
            if name == "MANIFEST.json":
                continue
            declared = declared_members.get(name) or {}
            checks[f"{name}:declared_bytes_exact"] = declared.get("bytes") == len(data[name])
            checks[f"{name}:declared_sha256_exact"] = declared.get("sha256") == sha256(data[name])

        readme = data.get("README.md", b"").decode("utf-8", errors="replace")
        quickstart = data.get("QUICKSTART.md", b"").decode("utf-8", errors="replace")
        evidence = data.get("EVIDENCE.md", b"").decode("utf-8", errors="replace")
        notice = data.get("RELEASE-NOTICE.md", b"").decode("utf-8", errors="replace")
        customer_text = "\n".join([readme, quickstart, evidence, notice])

        checks["bug_diagnosis_not_packaged"] = "Evidence-first Bug Diagnosis" not in customer_text and "bug-diagnosis" not in " ".join(names).lower()
        checks["readme_names_gemini_scope"] = EXPECTED_MODEL in readme
        checks["quickstart_preserves_human_authority"] = "human remains the final ship authority" in quickstart
        checks["evidence_names_model_specific"] = "MODEL_SPECIFIC" in evidence and EXPECTED_MODEL in evidence
        checks["evidence_forbids_universal_portability"] = "model-agnostic" in evidence and "universally portable" in evidence
        checks["release_notice_not_for_sale"] = "NOT FOR SALE" in notice
        checks["release_notice_license_pending"] = "No standalone customer license has been frozen" in notice

    failed = [name for name, ok in checks.items() if not ok]
    result = {
        "schema": "prompt-machine-starter-code-review-edition-pack-qa-v1",
        "archive_name": archive.name,
        "archive_bytes": archive.stat().st_size,
        "archive_sha256": sha256(archive.read_bytes()),
        "checks": checks,
        "failed_checks": failed,
        "verdict": "PASS" if not failed else "FAIL",
        "claim_boundary": "PACK_QA_ONLY_NOT_PROVIDER_CUSTODY_DELIVERY_OR_REVENUE",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
