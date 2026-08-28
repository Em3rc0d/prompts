from mk0_harvester_router import apply_route, load_policy


def base_record(score: float, disposition: str = "GOLDEN_EVALUATION") -> dict:
    epistemic = {
        "GOLDEN_EVALUATION": (True, "CANONICAL_CANDIDATE_ONLY", "PROMPT"),
        "REFERENCE_CORPUS": (False, "NON_CANONICAL_REFERENCE", "DOCUMENTATION"),
        "REJECT": (False, "NON_USABLE", "NOISY_HTML"),
        "HUMAN_REVIEW": (False, "UNRESOLVED", "AMBIGUOUS"),
    }
    canonical, authority, artifact_class = epistemic[disposition]
    return {
        "schema": "prompt-quarry-candidate-record-v1",
        "candidate_id": "cand-routing-fixture",
        "source_id": "src-routing-fixture",
        "candidate_fingerprint": "sha256:" + "0" * 64,
        "artifact_type": "prompt",
        "semantic_gate": {
            "artifact_class": artifact_class,
            "confidence": 0.99,
            "disposition": disposition,
            "canonical": canonical,
            "authority": authority,
            "reason": "routing fixture",
        },
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
        "policy_version": "1.2.0",
        "created_at": "2026-08-28T00:00:00Z",
    }


def test_exact_auto_candidate_boundary() -> None:
    routed = apply_route(base_record(0.95), load_policy())
    assert routed["route"] == "GOLDEN_CANDIDATE"
    assert routed["confidence"]["aggregate"] == 0.95


def test_human_review_upper_band() -> None:
    assert apply_route(base_record(0.9499999), load_policy())["route"] == "HUMAN_REVIEW_REQUIRED"


def test_exact_human_review_lower_boundary() -> None:
    assert apply_route(base_record(0.90), load_policy())["route"] == "HUMAN_REVIEW_REQUIRED"


def test_below_review_band_holds() -> None:
    assert apply_route(base_record(0.8999999), load_policy())["route"] == "HOLD"


def test_minimum_dimension_prevents_average_masking() -> None:
    record = base_record(0.99)
    record["confidence"]["architecture_mapping"] = 0.89
    routed = apply_route(record, load_policy())
    assert routed["confidence"]["aggregate"] == 0.89
    assert routed["route"] == "HOLD"


def test_force_review_overrides_high_confidence() -> None:
    record = base_record(0.99)
    record["critical_flags"] = ["conflicting_classifiers"]
    assert apply_route(record, load_policy())["route"] == "HUMAN_REVIEW_REQUIRED"


def test_force_review_overrides_low_confidence_ambiguity() -> None:
    record = base_record(0.72, "HUMAN_REVIEW")
    record["critical_flags"] = ["conflicting_classifiers"]
    assert apply_route(record, load_policy())["route"] == "HUMAN_REVIEW_REQUIRED"


def test_unknown_license_does_not_block_internal_golden_candidacy() -> None:
    record = base_record(0.99)
    record["critical_flags"] = ["license_unknown_for_redistribution"]
    routed = apply_route(record, load_policy())
    assert routed["route"] == "GOLDEN_CANDIDATE"
    assert routed["eligibility"]["golden_research_eligibility"]["eligible"] is True
    assert routed["eligibility"]["distribution_eligibility"]["eligible"] is False


def test_force_reject_beats_confidence() -> None:
    record = base_record(1.0)
    record["critical_flags"] = ["access_control_bypass_required"]
    assert apply_route(record, load_policy())["route"] == "REJECTED"


def test_quality_does_not_change_confidence_route() -> None:
    record = base_record(0.91)
    record["quality"] = {key: 1.0 for key in record["quality"]}
    assert apply_route(record, load_policy())["route"] == "HUMAN_REVIEW_REQUIRED"


def test_reference_corpus_never_routes_to_golden_even_at_perfect_score() -> None:
    routed = apply_route(base_record(1.0, "REFERENCE_CORPUS"), load_policy())
    assert routed["route"] == "HOLD"
    assert routed["eligibility"]["golden_research_eligibility"]["eligible"] is False
    assert routed["semantic_gate"]["canonical"] is False
    assert routed["semantic_gate"]["authority"] == "NON_CANONICAL_REFERENCE"


def test_rejected_artifact_never_routes_to_golden_even_at_perfect_score() -> None:
    routed = apply_route(base_record(1.0, "REJECT"), load_policy())
    assert routed["route"] == "REJECTED"
    assert routed["eligibility"]["golden_research_eligibility"]["eligible"] is False


def test_ambiguous_artifact_requires_human_review_at_review_threshold() -> None:
    routed = apply_route(base_record(0.90, "HUMAN_REVIEW"), load_policy())
    assert routed["route"] == "HUMAN_REVIEW_REQUIRED"
    assert routed["semantic_gate"]["canonical"] is False


def test_low_confidence_ambiguous_artifact_holds_without_override() -> None:
    routed = apply_route(base_record(0.8999999, "HUMAN_REVIEW"), load_policy())
    assert routed["route"] == "HOLD"
    assert routed["semantic_gate"]["canonical"] is False
    assert "confidence_below_human_review_threshold" in routed["route_reasons"]


def main() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in sorted(tests, key=lambda fn: fn.__name__):
        test()
        print(f"PASS {test.__name__}")
    print(f"HARVESTER ROUTER TESTS: PASS ({len(tests)})")


if __name__ == "__main__":
    main()
