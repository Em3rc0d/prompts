from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from collections import Counter
from pathlib import Path

from playwright.async_api import async_playwright


def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_public_item(item: dict) -> dict:
    description = item.get("description") or ""
    is_premium = bool(item.get("is_premium"))
    uuid = str(item.get("id") or "").strip()
    return {
        "id": f"alpacka_prompt_{uuid}",
        "uuid": uuid,
        "artifact_type": "prompt-reference",
        "source_id": "src_alpacka_web",
        "official_url": f"https://www.alpackaai.xyz/prompts/{uuid}",
        "title": item.get("title"),
        "category": item.get("category"),
        "is_premium": is_premium,
        "access": "premium" if is_premium else "free",
        "ai_tool": item.get("ai_tool"),
        "created_at": item.get("created_at"),
        "image_url": item.get("image_url"),
        "description_length": len(description),
        "description_sha256": sha256_text(description) if description else None,
        "verification": "source-api-observed",
        "capture_mode": "public-rpc-list-state",
        "metadata": {
            "rpc": "get_prompts_list",
            "description_storage_policy": "description-not-stored; fingerprint-only",
        },
    }


async def capture_list(root_url: str, timeout_seconds: int = 45) -> tuple[str, list[dict]]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="PromptQuarry/0.6 (+personal research; incremental public metadata sync)")
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        async def inspect_response(response):
            if "/rest/v1/rpc/get_prompts_list" not in response.url:
                return
            if future.done():
                return
            try:
                payload = await response.json()
                if not isinstance(payload, list):
                    raise RuntimeError("get_prompts_list did not return an array")
                future.set_result((response.url, payload))
            except Exception as exc:
                future.set_exception(exc)

        def on_response(response):
            asyncio.create_task(inspect_response(response))

        page.on("response", on_response)
        try:
            await page.goto(root_url, wait_until="domcontentloaded", timeout=60000)
            endpoint, payload = await asyncio.wait_for(future, timeout=timeout_seconds)
        finally:
            page.remove_listener("response", on_response)
            await browser.close()
        return endpoint, payload


def comparable_from_master(row: dict) -> dict:
    return {
        "title": row.get("title"),
        "category": row.get("category"),
        "access": row.get("access"),
        "ai_tool": row.get("ai_tool"),
        "created_at": row.get("created_at"),
        "image_url": row.get("image_url"),
        "description_length": row.get("description_length"),
        "description_sha256": row.get("description_sha256"),
    }


def comparable_from_state(row: dict) -> dict:
    return comparable_from_master(row)


def changed_fields(old: dict, new: dict) -> list[str]:
    before = comparable_from_master(old)
    after = comparable_from_state(new)
    return [key for key in after if before.get(key) != after.get(key)]


async def main_async(args) -> None:
    endpoint, payload = await capture_list(args.root_url)
    state = [normalize_public_item(item) for item in payload if item.get("id")]
    state.sort(key=lambda row: row["uuid"])

    master = read_jsonl(Path(args.master))
    master_by_uuid = {str(row.get("uuid")): row for row in master if row.get("uuid")}
    state_by_uuid = {row["uuid"]: row for row in state}

    added = []
    changed = []
    unchanged = []
    for uuid, current in state_by_uuid.items():
        previous = master_by_uuid.get(uuid)
        if previous is None:
            added.append(current)
            continue
        fields = changed_fields(previous, current)
        if fields:
            changed.append({
                "uuid": uuid,
                "title": current.get("title"),
                "category": current.get("category"),
                "access": current.get("access"),
                "changed_fields": fields,
                "official_url": current.get("official_url"),
            })
        else:
            unchanged.append(uuid)

    removed = []
    for uuid, previous in master_by_uuid.items():
        if uuid not in state_by_uuid:
            removed.append({
                "uuid": uuid,
                "title": previous.get("title"),
                "category": previous.get("category"),
                "access": previous.get("access"),
                "official_url": previous.get("official_url"),
            })

    queue_ids = {row["uuid"] for row in added} | {row["uuid"] for row in changed}
    queue = []
    for uuid in sorted(queue_ids):
        row = state_by_uuid[uuid]
        queue.append({
            "uuid": uuid,
            "id": row["id"],
            "official_url": row["official_url"],
            "title": row.get("title"),
            "category": row.get("category"),
            "access": row.get("access"),
            "reason": "added" if uuid not in master_by_uuid else "metadata-changed",
        })

    state_path = Path(args.state_output)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as handle:
        for row in state:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    queue_path = Path(args.queue_output)
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    with queue_path.open("w", encoding="utf-8") as handle:
        for row in queue:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    access_counts = Counter(row["access"] for row in state)
    category_counts = Counter(row.get("category") or "Uncategorized" for row in state)
    diff = {
        "rpc_endpoint": endpoint,
        "current_records": len(state),
        "master_records": len(master),
        "access_counts": dict(access_counts),
        "category_counts": dict(category_counts.most_common()),
        "added_count": len(added),
        "changed_count": len(changed),
        "removed_count": len(removed),
        "unchanged_count": len(unchanged),
        "enrichment_queue_count": len(queue),
        "added": [
            {k: row.get(k) for k in ("uuid", "title", "category", "access", "official_url")}
            for row in added
        ],
        "changed": changed,
        "removed": removed,
        "policy": "get_prompts_list is used as the cheap public metadata change detector. Only added/changed UUIDs are queued for detail enrichment; removed records are reported rather than silently deleted from historical evidence.",
    }
    diff_path = Path(args.diff_output)
    diff_path.parent.mkdir(parents=True, exist_ok=True)
    diff_path.write_text(json.dumps(diff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(diff, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-url", default="https://www.alpackaai.xyz/")
    parser.add_argument("--master", default="quarry/normalized/alpacka-ai-prompt-metadata.jsonl")
    parser.add_argument("--state-output", default="quarry/normalized/alpacka-ai-public-prompt-state.jsonl")
    parser.add_argument("--diff-output", default="quarry/analysis/alpacka-ai-public-prompt-sync-diff.json")
    parser.add_argument("--queue-output", default="quarry/normalized/alpacka-ai-prompt-enrichment-queue.jsonl")
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
