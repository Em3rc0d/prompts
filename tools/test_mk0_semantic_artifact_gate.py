from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from mk0_semantic_artifact_gate import classify_artifact

CASES = [
    ("mk0/raw/harvester/src-1643157b768c76e76ecc.html", "repository", "NOISY_HTML", "REJECT"),
    ("mk0/raw/harvester/src-4c9c366da611189d8769.md", "instruction-markdown", "AGENT_INSTRUCTION", "GOLDEN_EVALUATION"),
    ("mk0/raw/harvester/src-27b01d1fd87f438f5d89.md", "prompt", "MANUAL", "REFERENCE_CORPUS"),
    ("mk0/raw/harvester/src-8abfb568bda87956c956.md", "instruction-markdown", "CODEBASE_GUIDE", "REFERENCE_CORPUS"),
    ("mk0/raw/harvester/src-4e0f8e564b0d5063567b.md", "prompt", "IMPLEMENTATION_PLAN", "REFERENCE_CORPUS"),
    ("mk0/raw/harvester/src-c6e607ab15f9054aa3cc.md", "prompt", "LOG_CHANGELOG", "REFERENCE_CORPUS"),
    ("mk0/raw/harvester/src-dfedca21bb332f623103.md", "prompt", "FAQ", "REFERENCE_CORPUS"),
    ("mk0/raw/harvester/src-4fe8873fee95c3ad878b.md", "prompt", "ARCHITECTURE_DOCUMENTATION", "REFERENCE_CORPUS"),
    ("mk0/raw/harvester/src-df5745120b8542f8e17d.md", "instruction-markdown", "AGENT_INSTRUCTION", "GOLDEN_EVALUATION"),
    ("mk0/raw/harvester/src-38dc369b08a2e7b09211.md", "instruction-markdown", "AGENT_INSTRUCTION", "GOLDEN_EVALUATION"),
]


def main():
    failures=[]
    for path, source_type, expected_class, expected_disposition in CASES:
        p=Path(path)
        if not p.exists():
            failures.append(f"missing calibration fixture: {path}")
            continue
        body=p.read_text(encoding="utf-8",errors="replace")
        result=classify_artifact(p.name, body, source_type)
        if result["artifact_class"] != expected_class or result["disposition"] != expected_disposition:
            failures.append(f"{path}: expected {expected_class}/{expected_disposition}, got {result}")
        if expected_disposition == "REFERENCE_CORPUS":
            if result["canonical"] is not False or result["authority"] != "NON_CANONICAL_REFERENCE":
                failures.append(f"{path}: reference corpus must be explicitly non-canonical, got {result}")
        if expected_disposition == "REJECT" and result["canonical"] is not False:
            failures.append(f"{path}: rejected artifacts cannot be canonical")
    if failures:
        raise AssertionError("semantic calibration failed:\n"+"\n".join(failures))
    print(f"PASS: {len(CASES)}/10 human-reviewed calibration fixtures reproduced with epistemic boundaries")


if __name__ == "__main__":
    main()
