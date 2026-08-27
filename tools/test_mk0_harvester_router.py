from copy import deepcopy

from mk0_harvester_router import apply_route, load_policy


def base_record(score: float) -> dict:
    return {
        "schema": "prompt-quarry-candidate-record-v1",
        "candidate_id": "cand-routing-fixture",
        "source_id": "src-routing-fixture",
        "candidate_fingerprint": "sha256:" + "0" * 64,
        "artifact_type": "prompt",
        "stage": "SCORED",
        "classification": {"domain": "software", "intent": "review", "family": "software_code_review", "language": "en"},
        "techniques": ["role", "constraints"],
        "architecture": ["structured-instructions"],
        "confidence": {
            "classification": score,
            "technique_extraction": score,
            "architecture_mapping": score,
            "deduplication": score,
            "aggregate": 0.0,
        },
        "quality": {
            "structural_quality": 0.9,
            "novelty": 0.8,
            "coverage_value": 0.9,
            "golden_value": 0.9,
        },
        "critical_flags": [],
        "route": "HOLD",
        "route_reasons": [],
        "policy_version": "1.0.0",
        "created_at": "2026-08-27T00:00:00Z",
    }


def test_exact_auto_candidate_boundary() -> None:
    policy = load_policy()
    routed = apply_route(base_record(0.95), policy)
    assert routed["route"] == "GOLDEN_CANDIDATE"
    assert routed["confidence"]["aggregate"] == 0.95


def test_human_review_upper_band() -> None:
    policy = load_policy()
    routed = apply_route(base_record(0.9499999), policy)
    assert routed["route"] == "HUMAN_REVIEW_REQUIRED"


def test_exact_human_review_lower_boundary() -> None:
    policy = load_policy()
    routed = apply_route(base_record(0.90), policy)
    assert routed["route"] == "HUMAN_REVIEW_REQUIRED"


def test_below_review_band_holds() -> None:
    policy = load_policy()
    routed = apply_route(base_record(0.8999999), policy)
    assert routed["route"] == "HOLD"


def test_minimum_dimension_prevents_average_masking() -> None:
    policy = load_policy()
    record = base_record(0.99)
    record["confidence"]["architecture_mapping"] = 0.89
    routed = apply_route(record, policy)
    assert routed["confidence"]["aggregate"] == 0.89
    assert routed["route"] == "HOLD"


def test_force_review_overrides_high_confidence() -> None:
    policy = load_policy()
    record = base_record(0.99)
    record["critical_flags"] = ["conflicting_classifiers"]
    routed = apply_route(record, policy)
    assert routed["route"] == "HUMAN_REVIEW_REQUIRED"


def test_unknown_license_blocks_auto_candidate() -> None:
    policy = load_policy()
    record = base_record(0.99)
    record["critical_flags"] = ["license_unknown_for_redistribution"]
    routed = apply_route(record, policy)
    assert routed["route"] == "HUMAN_REVIEW_REQUIRED"


def test_force_reject_beats_confidence() -> None:
    policy = load_policy()
    record = base_record(1.0)
    record["critical_flags"] = ["access_control_bypass_required"]
    routed = apply_route(record, policy)
    assert routed["route"] == "REJECTED"


def test_quality_does_not_change_confidence_route() -> None:
    policy = load_policy()
    record = base_record(0.91)
    record["quality"] = {key: 1.0 for key in record["quality"]}
    routed = apply_route(record, policy)
    assert routed["route"] == "HUMAN_REVIEW_REQUIRED"


def main() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in sorted(tests, key=lambda fn: fn.__name__):
        test()
        print(f"PASS {test.__name__}")
    print(f"HARVESTER ROUTER TESTS: PASS ({len(tests)})")


if __name__ == "__main__":
    main()
