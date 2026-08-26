from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REAL_EXECUTION_MODES = {"api", "manual-observed"}
ALL_EXECUTION_MODES = REAL_EXECUTION_MODES | {"synthetic"}
HUMAN_STATUSES = {"PASS", "FAIL"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def receipt_id(payload: dict) -> str:
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()[:16]
    return f"pq_mk1_f4_receipt_{digest}"


def norm(value: str) -> str:
    return " ".join(value.casefold().split())


def evaluate_assertion(output: str, assertion: dict) -> dict:
    kind = assertion["type"]
    normalized = norm(output)
    values = [norm(str(v)) for v in assertion.get("values", [])]

    if kind == "contains_all":
        missing = [v for v in values if v not in normalized]
        passed = not missing
        detail = {"missing": missing}
    elif kind == "contains_any":
        matches = [v for v in values if v in normalized]
        passed = bool(matches)
        detail = {"matches": matches}
    elif kind == "not_contains_any":
        forbidden = [v for v in values if v in normalized]
        passed = not forbidden
        detail = {"forbidden_matches": forbidden}
    elif kind == "question_count_at_most":
        limit = int(assertion["value"])
        observed = output.count("?") + output.count("¿")
        passed = observed <= limit
        detail = {"observed": observed, "limit": limit}
    elif kind == "min_length":
        limit = int(assertion["value"])
        observed = len(output.strip())
        passed = observed >= limit
        detail = {"observed": observed, "minimum": limit}
    elif kind == "max_length":
        limit = int(assertion["value"])
        observed = len(output.strip())
        passed = observed <= limit
        detail = {"observed": observed, "maximum": limit}
    else:
        raise ValueError(f"Unsupported F4 assertion type: {kind}")

    return {"type": kind, "pass": passed, "detail": detail}


def evaluate_case(fixture: dict, response: dict) -> dict:
    output = str(response.get("output", ""))
    machine_results = [
        evaluate_assertion(output, assertion)
        for assertion in fixture.get("expected", {}).get("machine_assertions", [])
    ]

    declared_human = response.get("human_checks", {}) or {}
    human_results = []
    unresolved = []
    failed_human = []
    for check in fixture.get("expected", {}).get("human_checks", []):
        value = declared_human.get(check)
        status = value.get("status") if isinstance(value, dict) else value
        note = value.get("note") if isinstance(value, dict) else None
        if status not in HUMAN_STATUSES:
            unresolved.append(check)
            human_results.append({"check": check, "status": "UNRESOLVED", "note": note})
        else:
            if status == "FAIL":
                failed_human.append(check)
            human_results.append({"check": check, "status": status, "note": note})

    machine_pass = all(row["pass"] for row in machine_results)
    human_pass = not unresolved and not failed_human
    passed = machine_pass and human_pass

    return {
        "fixture_id": fixture["fixture_id"],
        "class": fixture["class"],
        "severity": fixture.get("severity", "normal"),
        "pass": passed,
        "machine_pass": machine_pass,
        "human_pass": human_pass,
        "machine_assertions": machine_results,
        "human_checks": human_results,
        "unresolved_human_checks": unresolved,
        "failed_human_checks": failed_human,
        "output": output,
    }


def run_fixture_set(artifact: dict, fixture_set: dict, execution: dict) -> dict:
    mode = execution.get("mode")
    if mode not in ALL_EXECUTION_MODES:
        raise ValueError(f"Unsupported F4 execution mode: {mode!r}")
    if artifact.get("state") != "VALID":
        raise ValueError(f"F4 accepts VALID source artifacts only; got {artifact.get('state')!r}")
    if fixture_set.get("artifact_id") != artifact.get("id"):
        raise ValueError("Fixture set artifact_id does not match artifact")
    if fixture_set.get("artifact_version") != artifact.get("version"):
        raise ValueError("Fixture set artifact_version does not match artifact version")

    runtime = execution.get("runtime") or {}
    if mode in REAL_EXECUTION_MODES:
        missing_runtime = [key for key in ("provider", "model", "run_at") if not runtime.get(key)]
        if missing_runtime:
            raise ValueError(f"Real F4 execution missing runtime identity: {missing_runtime}")

    responses = execution.get("responses") or {}
    results = []
    for fixture in fixture_set.get("cases", []):
        response = responses.get(fixture["fixture_id"], {})
        results.append(evaluate_case(fixture, response))

    blocking_failures = [
        row["fixture_id"]
        for row in results
        if row["severity"] == "blocking" and not row["pass"]
    ]
    unresolved_human_checks = sum(
        len(row["unresolved_human_checks"])
        for row in results
        if row["severity"] == "blocking"
    )

    if mode == "synthetic":
        status = "HARNESS_CHARACTERIZATION"
        eligible = False
    elif blocking_failures or unresolved_human_checks:
        status = "BEHAVIORAL_FAIL"
        eligible = False
    else:
        status = "BEHAVIORAL_PASS"
        eligible = True

    receipt_core = {
        "mk_stage": "MK1",
        "phase": "F4",
        "artifact_id": artifact["id"],
        "artifact_version": artifact["version"],
        "fixture_set_id": fixture_set["fixture_set_id"],
        "fixture_set_version": fixture_set.get("version", "1"),
        "execution_id": execution.get("execution_id"),
        "execution_mode": mode,
        "runtime": runtime,
        "status": status,
        "eligible_for_tested": eligible,
        "blocking_failures": blocking_failures,
        "unresolved_blocking_human_checks": unresolved_human_checks,
        "fixture_count": len(results),
        "fixture_results": results,
        "state_policy": "Only real BEHAVIORAL_PASS receipts may support VALID -> TESTED. Synthetic runs never promote state.",
        "claim_policy": "F4 does not establish baseline superiority, CERTIFIED, or IMPROVED claims.",
    }
    receipt_core["receipt_id"] = receipt_id(receipt_core)
    return receipt_core


def find_fixture_set(document: dict, fixture_set_id: str) -> dict:
    for fixture_set in document.get("fixture_sets", []):
        if fixture_set.get("fixture_set_id") == fixture_set_id:
            item = dict(fixture_set)
            item.setdefault("version", document.get("version", "1"))
            return item
    raise KeyError(f"Unknown fixture set: {fixture_set_id}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--fixtures", default="mk1/fixtures/f4/fixture-sets.json")
    parser.add_argument("--fixture-set", required=True)
    parser.add_argument("--execution", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    artifact = load(Path(args.artifact))
    fixture_document = load(Path(args.fixtures))
    fixture_set = find_fixture_set(fixture_document, args.fixture_set)
    execution = load(Path(args.execution))
    receipt = run_fixture_set(artifact, fixture_set, execution)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
