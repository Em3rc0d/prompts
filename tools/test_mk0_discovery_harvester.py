from __future__ import annotations

from pathlib import Path

from mk0_discovery_harvester import (
    load_json,
    make_source_record,
    stable_source_id,
    validate_records,
)


def observed_record() -> dict:
    content = b"# public prompt fixture\nDo the task with explicit constraints.\n"
    return make_source_record(
        url="https://example.com/public/prompt.md",
        source_type="prompt",
        method="web",
        access_status="PUBLIC",
        body_status="OBSERVED",
        license_status="UNKNOWN",
        title="Fixture",
        publisher="example.com",
        content=content,
        http_status=200,
        content_type="text/markdown",
        access_note="robots.txt allows fetch",
        raw_ref="mk0/raw/harvester/src-fixture.txt",
    )


def test_source_id_is_stable() -> None:
    url = "https://example.com/a"
    assert stable_source_id(url) == stable_source_id(url)
    assert stable_source_id(url) != stable_source_id(url + "b")


def test_observed_record_has_content_hash() -> None:
    record = observed_record()
    assert record["content_sha256"].startswith("sha256:")
    assert record["body_observation_status"] == "OBSERVED"
    validate_records([record])


def test_unavailable_record_cannot_carry_hash() -> None:
    record = observed_record()
    record["body_observation_status"] = "UNAVAILABLE"
    try:
        validate_records([record])
    except ValueError:
        return
    raise AssertionError("UNAVAILABLE record with observed body hash must fail")


def test_blocked_web_200_is_rejected_by_contract() -> None:
    record = make_source_record(
        url="https://example.com/private",
        source_type="prompt",
        method="web",
        access_status="BLOCKED",
        body_status="UNAVAILABLE",
        license_status="UNKNOWN",
        title=None,
        publisher="example.com",
        content=None,
        http_status=200,
        content_type="text/html",
        access_note="blocked",
        raw_ref=None,
    )
    try:
        validate_records([record])
    except ValueError:
        return
    raise AssertionError("blocked web HTTP 200 record must fail closed")


def test_registry_has_only_https_web_seeds() -> None:
    registry = load_json(Path("mk0/harvester/DISCOVERY_REGISTRY.json"))
    for source in registry["sources"]:
        if source["adapter"] == "web_seed":
            assert source["url"].startswith("https://")


def test_registry_does_not_assert_reusable_license() -> None:
    registry = load_json(Path("mk0/harvester/DISCOVERY_REGISTRY.json"))
    for source in registry["sources"]:
        assert source["license_status"] == "UNKNOWN"


def main() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in sorted(tests, key=lambda fn: fn.__name__):
        test()
        print(f"PASS {test.__name__}")
    print(f"DISCOVERY HARVESTER TESTS: PASS ({len(tests)})")


if __name__ == "__main__":
    main()
