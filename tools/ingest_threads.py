from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx

from common import canonicalize, sha256_text, utc_now, write_jsonl

API_HOST = "https://graph.threads.net"
DEFAULT_FIELDS = [
    "id",
    "media_type",
    "media_url",
    "permalink",
    "username",
    "text",
    "timestamp",
    "shortcode",
    "is_quote_post",
    "has_replies",
]


def next_request(payload: dict, current_url: str) -> tuple[str | None, dict | None]:
    paging = payload.get("paging") or {}
    if paging.get("next"):
        return paging["next"], None

    after = (paging.get("cursors") or {}).get("after")
    if not after:
        return None, None

    parsed = urlparse(current_url)
    existing = parse_qs(parsed.query)
    params = {key: value[-1] for key, value in existing.items()}
    params["after"] = after
    return parsed._replace(query="").geturl(), params


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect public Threads posts through Meta's official Threads API."
    )
    parser.add_argument("--username", default="alpacka.ai")
    parser.add_argument(
        "--output",
        default="quarry/raw/alpacka-ai/threads/posts.jsonl",
    )
    parser.add_argument("--max-pages", type=int, default=500)
    parser.add_argument("--delay-seconds", type=float, default=1.0)
    parser.add_argument(
        "--access-token-env",
        default="THREADS_ACCESS_TOKEN",
        help="Environment variable containing the OAuth token.",
    )
    args = parser.parse_args()

    token = os.getenv(args.access_token_env)
    if not token:
        raise SystemExit(
            f"Missing {args.access_token_env}. Keep tokens in environment/secrets, never in Git."
        )

    fields = ",".join(DEFAULT_FIELDS)
    url = f"{API_HOST}/profile_posts"
    params: dict | None = {
        "username": args.username,
        "fields": fields,
        "access_token": token,
    }

    captured_at = utc_now()
    records: list[dict] = []
    page_number = 0

    with httpx.Client(timeout=45.0, follow_redirects=True) as client:
        while url and page_number < args.max_pages:
            page_number += 1
            response = client.get(url, params=params)

            if response.status_code in {401, 403}:
                raise SystemExit(
                    f"Threads API authorization failed ({response.status_code}). "
                    "Check token scopes, including threads_profile_discovery when required."
                )
            if response.status_code == 429:
                raise SystemExit(
                    "Threads API rate limit encountered. Collection stopped without bypassing it."
                )

            response.raise_for_status()
            payload = response.json()

            for item in payload.get("data") or []:
                text = canonicalize(item.get("text") or "")
                permalink = item.get("permalink") or ""
                source_key = item.get("shortcode") or item.get("id") or sha256_text(permalink or text)[7:23]

                records.append(
                    {
                        "quarry_record_type": "threads_post",
                        "source_id": "src_alpacka_threads",
                        "source_key": str(source_key),
                        "source_url": permalink,
                        "official_post_url": permalink,
                        "raw_url": None,
                        "capture_mode": "api",
                        "verification": "source-body-observed",
                        "captured_at": captured_at,
                        "author": item.get("username") or args.username,
                        "published_at": item.get("timestamp"),
                        "body": text or None,
                        "fingerprint": sha256_text(text) if text else None,
                        "raw": item,
                    }
                )

            url, next_params = next_request(payload, str(response.url))
            if url:
                # OAuth token must remain present if `paging.next` does not already include it.
                params = next_params
                if params is not None:
                    params.setdefault("username", args.username)
                    params.setdefault("fields", fields)
                    params["access_token"] = token
                time.sleep(max(args.delay_seconds, 0.0))

    count = write_jsonl(args.output, records)
    print(
        json.dumps(
            {
                "status": "ok",
                "username": args.username,
                "pages": page_number,
                "records": count,
                "output": str(Path(args.output)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
