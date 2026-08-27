from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import quote_plus, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from jsonschema import Draft202012Validator, FormatChecker

REGISTRY_PATH = Path("mk0/harvester/DISCOVERY_REGISTRY.json")
SOURCE_SCHEMA_PATH = Path("mk0/harvester/SOURCE_RECORD.schema.json")
RAW_ROOT = Path("mk0/raw/harvester")
NORMALIZED_ROOT = Path("mk0/normalized/harvester")
USER_AGENT_FALLBACK = "PromptQuarry/0.6 (+public research; provenance-first)"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def stable_source_id(url: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
    return f"src-{digest}"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_content_type(value: str | None) -> str | None:
    if not value:
        return None
    return value.split(";", 1)[0].strip().casefold()


def robots_allowed(client: httpx.Client, url: str, user_agent: str) -> tuple[bool, str]:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        response = client.get(robots_url)
        if response.status_code >= 400:
            return True, f"robots.txt unavailable ({response.status_code}); no explicit disallow observed"
        parser = RobotFileParser()
        parser.set_url(robots_url)
        parser.parse(response.text.splitlines())
        allowed = parser.can_fetch(user_agent, url)
        return allowed, "robots.txt allows fetch" if allowed else "robots.txt disallows fetch"
    except httpx.HTTPError as exc:
        return False, f"robots.txt check failed closed: {type(exc).__name__}"


def infer_title(content: bytes, content_type: str | None, fallback: str | None = None) -> str | None:
    if content_type == "text/html":
        soup = BeautifulSoup(content, "html.parser")
        if soup.title:
            title = " ".join(soup.title.get_text(" ", strip=True).split())
            return title[:500] if title else fallback
    return fallback


def write_observation(source_id: str, content: bytes, suffix: str) -> str:
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    path = RAW_ROOT / f"{source_id}{suffix}"
    path.write_bytes(content)
    return path.as_posix()


def make_source_record(*, url: str, source_type: str, method: str, access_status: str,
                       body_status: str, license_status: str, title: str | None,
                       publisher: str | None, content: bytes | None,
                       http_status: int | None, content_type: str | None,
                       access_note: str, raw_ref: str | None) -> dict:
    return {
        "schema": "prompt-quarry-source-record-v1",
        "source_id": stable_source_id(url),
        "canonical_url": url,
        "source_type": source_type,
        "access_status": access_status,
        "body_observation_status": body_status,
        "authority": "third-party",
        "license_status": license_status,
        "title": title,
        "publisher": publisher,
        "language": None,
        "content_sha256": sha256_bytes(content) if content is not None and body_status == "OBSERVED" else None,
        "observed_at": utc_now(),
        "retrieval": {
            "method": method,
            "http_status": http_status,
            "content_type": content_type,
            "robots_or_access_note": access_note,
        },
        "provenance": {
            "source_identity_status": "VERIFIED",
            "observation_class": "SOURCE_OBSERVATION",
            "raw_record_ref": raw_ref,
        },
        "notes": None,
    }


def harvest_web_seed(client: httpx.Client, source: dict, network_policy: dict) -> dict:
    url = source["url"]
    parsed = urlparse(url)
    if parsed.scheme not in network_policy["allowed_schemes"]:
        return make_source_record(
            url=url, source_type=source["source_type"], method="web", access_status="BLOCKED",
            body_status="UNAVAILABLE", license_status=source["license_status"], title=None,
            publisher=parsed.netloc, content=None, http_status=None, content_type=None,
            access_note="scheme rejected by registry policy", raw_ref=None,
        )

    allowed, robots_note = robots_allowed(client, url, network_policy["user_agent"])
    if not allowed:
        return make_source_record(
            url=url, source_type=source["source_type"], method="web", access_status="BLOCKED",
            body_status="UNAVAILABLE", license_status=source["license_status"], title=None,
            publisher=parsed.netloc, content=None, http_status=None, content_type=None,
            access_note=robots_note, raw_ref=None,
        )

    response = client.get(url)
    content_type = normalize_content_type(response.headers.get("content-type"))
    if response.status_code in {401, 403}:
        status = "AUTH_REQUIRED" if response.status_code == 401 else "BLOCKED"
        return make_source_record(
            url=str(response.url), source_type=source["source_type"], method="web", access_status=status,
            body_status="UNAVAILABLE", license_status=source["license_status"], title=None,
            publisher=urlparse(str(response.url)).netloc, content=None, http_status=response.status_code,
            content_type=content_type, access_note=f"HTTP {response.status_code}; no bypass attempted", raw_ref=None,
        )
    if response.status_code >= 400:
        return make_source_record(
            url=str(response.url), source_type=source["source_type"], method="web", access_status="UNKNOWN",
            body_status="UNAVAILABLE", license_status=source["license_status"], title=None,
            publisher=urlparse(str(response.url)).netloc, content=None, http_status=response.status_code,
            content_type=content_type, access_note=f"HTTP {response.status_code}", raw_ref=None,
        )

    if content_type not in network_policy["allowed_content_types"]:
        return make_source_record(
            url=str(response.url), source_type=source["source_type"], method="web", access_status="PUBLIC",
            body_status="UNAVAILABLE", license_status=source["license_status"], title=None,
            publisher=urlparse(str(response.url)).netloc, content=None, http_status=response.status_code,
            content_type=content_type, access_note=f"content type not allowlisted: {content_type}", raw_ref=None,
        )

    content = response.content
    if len(content) > int(network_policy["max_response_bytes"]):
        return make_source_record(
            url=str(response.url), source_type=source["source_type"], method="web", access_status="PUBLIC",
            body_status="PARTIAL", license_status=source["license_status"], title=None,
            publisher=urlparse(str(response.url)).netloc, content=None, http_status=response.status_code,
            content_type=content_type, access_note="response exceeded max_response_bytes; body not stored", raw_ref=None,
        )

    suffix = ".html" if content_type == "text/html" else ".txt"
    final_url = str(response.url)
    sid = stable_source_id(final_url)
    raw_ref = write_observation(sid, content, suffix)
    return make_source_record(
        url=final_url, source_type=source["source_type"], method="web", access_status="PUBLIC",
        body_status="OBSERVED", license_status=source["license_status"],
        title=infer_title(content, content_type), publisher=urlparse(final_url).netloc,
        content=content, http_status=response.status_code, content_type=content_type,
        access_note=robots_note, raw_ref=raw_ref,
    )


def github_headers(user_agent: str) -> dict[str, str]:
    headers = {"user-agent": user_agent, "accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        headers["authorization"] = f"Bearer {token}"
    return headers


def discover_github_code(client: httpx.Client, source: dict, network_policy: dict) -> Iterable[dict]:
    query = quote_plus(source["query"])
    limit = max(1, min(int(source.get("max_results", 25)), 100))
    response = client.get(
        f"https://api.github.com/search/code?q={query}&per_page={limit}",
        headers=github_headers(network_policy["user_agent"]),
    )
    response.raise_for_status()
    for item in response.json().get("items", [])[:limit]:
        repository = item.get("repository", {})
        full_name = repository.get("full_name")
        path = item.get("path")
        if not full_name or not path:
            continue
        yield {
            "canonical_url": item.get("html_url"),
            "contents_api_url": f"https://api.github.com/repos/{full_name}/contents/{path}",
            "repository": full_name,
            "path": path,
            "source_type": source["source_type"],
            "license_status": source["license_status"],
        }


def harvest_github_item(client: httpx.Client, item: dict, network_policy: dict) -> dict:
    response = client.get(item["contents_api_url"], headers=github_headers(network_policy["user_agent"]))
    canonical_url = item["canonical_url"]
    if response.status_code in {401, 403}:
        return make_source_record(
            url=canonical_url, source_type=item["source_type"], method="github", access_status="BLOCKED",
            body_status="UNAVAILABLE", license_status=item["license_status"], title=Path(item["path"]).name,
            publisher=item["repository"], content=None, http_status=response.status_code,
            content_type="application/json", access_note=f"GitHub API HTTP {response.status_code}; no bypass attempted", raw_ref=None,
        )
    response.raise_for_status()
    payload = response.json()
    if payload.get("encoding") != "base64" or not isinstance(payload.get("content"), str):
        return make_source_record(
            url=canonical_url, source_type=item["source_type"], method="github", access_status="PUBLIC",
            body_status="PARTIAL", license_status=item["license_status"], title=Path(item["path"]).name,
            publisher=item["repository"], content=None, http_status=response.status_code,
            content_type="application/json", access_note="GitHub metadata observed but inline file body unavailable", raw_ref=None,
        )
    content = base64.b64decode(payload["content"], validate=False)
    if len(content) > int(network_policy["max_response_bytes"]):
        return make_source_record(
            url=canonical_url, source_type=item["source_type"], method="github", access_status="PUBLIC",
            body_status="PARTIAL", license_status=item["license_status"], title=Path(item["path"]).name,
            publisher=item["repository"], content=None, http_status=response.status_code,
            content_type="text/plain", access_note="file exceeded max_response_bytes; body not stored", raw_ref=None,
        )
    sid = stable_source_id(canonical_url)
    raw_ref = write_observation(sid, content, Path(item["path"]).suffix or ".txt")
    return make_source_record(
        url=canonical_url, source_type=item["source_type"], method="github", access_status="PUBLIC",
        body_status="OBSERVED", license_status=item["license_status"], title=Path(item["path"]).name,
        publisher=item["repository"], content=content, http_status=response.status_code,
        content_type="text/plain", access_note="public GitHub file observed through Contents API", raw_ref=raw_ref,
    )


def validate_records(records: list[dict]) -> None:
    schema = load_json(SOURCE_SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for index, record in enumerate(records):
        for error in validator.iter_errors(record):
            errors.append(f"record[{index}] {error.json_path}: {error.message}")
    if errors:
        raise ValueError("SOURCE_RECORD validation failed:\n" + "\n".join(errors))


def run(registry: dict, *, dry_run: bool = False) -> list[dict]:
    network_policy = registry["network_policy"]
    records: list[dict] = []
    if dry_run:
        return records
    headers = {"user-agent": network_policy.get("user_agent", USER_AGENT_FALLBACK)}
    with httpx.Client(
        timeout=float(network_policy["timeout_seconds"]),
        follow_redirects=bool(network_policy["follow_redirects"]),
        headers=headers,
    ) as client:
        for source in registry["sources"]:
            if not source.get("enabled", False):
                continue
            if source["adapter"] == "web_seed":
                records.append(harvest_web_seed(client, source, network_policy))
            elif source["adapter"] == "github_code_search":
                try:
                    items = list(discover_github_code(client, source, network_policy))
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code in {401, 403, 422}:
                        continue
                    raise
                for item in items:
                    records.append(harvest_github_item(client, item, network_policy))
                    time.sleep(float(network_policy["per_host_delay_seconds"]))
            else:
                raise ValueError(f"unknown adapter: {source['adapter']}")
            time.sleep(float(network_policy["per_host_delay_seconds"]))
    validate_records(records)
    return records


def persist(records: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt Quarry MK0 real discovery/harvest adapters")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=NORMALIZED_ROOT / "source-records.jsonl")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    registry = load_json(args.registry)
    records = run(registry, dry_run=args.dry_run)
    if not args.dry_run:
        persist(records, args.output)
    print(json.dumps({"records": len(records), "output": None if args.dry_run else str(args.output), "dry_run": args.dry_run}, indent=2))


if __name__ == "__main__":
    main()
