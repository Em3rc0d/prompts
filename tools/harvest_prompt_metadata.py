from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path

import httpx
from playwright.async_api import async_playwright


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def replace_uuid(value, old_uuid: str, new_uuid: str):
    if isinstance(value, dict):
        return {k: replace_uuid(v, old_uuid, new_uuid) for k, v in value.items()}
    if isinstance(value, list):
        return [replace_uuid(v, old_uuid, new_uuid) for v in value]
    if isinstance(value, str):
        return value.replace(old_uuid, new_uuid)
    return value


def extract_variables(content: str) -> list[str]:
    values: list[str] = []
    patterns = [
        r"\{\{\s*([^{}]{1,80}?)\s*\}\}",
        r"\[\s*([^\[\]\n]{1,80}?)\s*\]",
        r"<\s*([^<>\n]{1,80}?)\s*>",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            value = " ".join(match.group(1).split()).strip()
            if not value or value.lower().startswith(("http", "https")):
                continue
            if value not in values:
                values.append(value)
            if len(values) >= 25:
                return values
    return values


def structural_signals(content: str) -> dict:
    low = content.casefold()
    numbered_steps = len(re.findall(r"(?:^|\n)\s*\d+[.)]\s+", content))
    bullet_lines = len(re.findall(r"(?:^|\n)\s*[-*•]\s+", content))
    return {
        "role_assignment": bool(re.search(r"\b(act[uú]a como|eres un|eres una|tu rol)\b", low)),
        "stepwise_procedure": numbered_steps >= 2 or any(x in low for x in ("paso 1", "paso 2", "primero", "finalmente")),
        "output_contract": any(x in low for x in ("formato de salida", "devuelve", "entrega", "output", "tabla", "json")),
        "question_first": any(x in low for x in ("hazme preguntas", "pregunta antes", "preguntas de aclaración", "preguntas aclaratorias")),
        "explicit_constraints": any(x in low for x in ("no inventes", "debes", "no debes", "restricciones", "condiciones")),
        "numbered_steps": numbered_steps,
        "bullet_lines": bullet_lines,
        "line_count": len(content.splitlines()),
        "paragraph_count": len([p for p in re.split(r"\n\s*\n", content) if p.strip()]),
    }


async def capture_rpc_contract(page, first_url: str, timeout_seconds: int = 30):
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    async def inspect_request(request):
        if "/rest/v1/rpc/get_prompt_detail" not in request.url:
            return
        if future.done():
            return
        try:
            headers = await request.all_headers()
            body = request.post_data_json
            if callable(body):
                body = body()
            future.set_result({
                "endpoint": request.url,
                "headers": headers,
                "body": body,
            })
        except Exception as exc:
            future.set_exception(exc)

    def on_request(request):
        asyncio.create_task(inspect_request(request))

    page.on("request", on_request)
    await page.goto(first_url, wait_until="domcontentloaded", timeout=60000)
    try:
        return await asyncio.wait_for(future, timeout=timeout_seconds)
    finally:
        page.remove_listener("request", on_request)


def replay_headers(all_headers: dict[str, str]) -> dict[str, str]:
    allowed = {
        "apikey",
        "authorization",
        "content-type",
        "accept",
        "accept-profile",
        "content-profile",
        "prefer",
    }
    return {k: v for k, v in all_headers.items() if k.lower() in allowed}


async def main_async(args) -> None:
    directory = list(read_jsonl(Path(args.input)))
    if not directory:
        raise SystemExit("Prompt directory is empty.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="PromptQuarry/0.4 (+personal research; metadata-only harvest)")
        contract = await capture_rpc_contract(page, directory[0]["official_url"])
        await browser.close()

    endpoint = contract["endpoint"]
    template_body = contract["body"]
    if not isinstance(template_body, (dict, list)):
        raise SystemExit("Could not identify structured RPC request body.")
    first_uuid = directory[0]["uuid"]
    headers = replay_headers(contract["headers"])

    results = []
    status_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    free_with_content = 0
    premium_content_null = 0
    mismatches = []

    async with httpx.AsyncClient(timeout=30.0, headers=headers, follow_redirects=True) as client:
        for index, row in enumerate(directory, 1):
            uuid = row["uuid"]
            body = replace_uuid(deepcopy(template_body), first_uuid, uuid)
            response = await client.post(endpoint, json=body)

            if response.status_code == 429:
                await asyncio.sleep(3)
                response = await client.post(endpoint, json=body)
            if response.status_code in {401, 403}:
                raise SystemExit(f"RPC access boundary changed: HTTP {response.status_code}")
            response.raise_for_status()
            payload = response.json()
            content = payload.get("content")
            description = payload.get("description") or ""
            is_premium = bool(payload.get("is_premium"))

            if is_premium and content is None:
                premium_content_null += 1
            if (not is_premium) and isinstance(content, str) and content:
                free_with_content += 1

            api_category = payload.get("category")
            if api_category:
                category_counts[str(api_category)] += 1

            if row.get("category_observed") and api_category and row["category_observed"] != api_category:
                mismatches.append({
                    "uuid": uuid,
                    "directory_category": row["category_observed"],
                    "api_category": api_category,
                })

            record = {
                "id": row["id"],
                "uuid": uuid,
                "artifact_type": "prompt-reference",
                "source_id": "src_alpacka_web",
                "official_url": row["official_url"],
                "title": payload.get("title"),
                "category": api_category,
                "is_premium": is_premium,
                "access": "premium" if is_premium else "free",
                "ai_tool": payload.get("ai_tool"),
                "created_at": payload.get("created_at"),
                "image_url": payload.get("image_url"),
                "description_length": len(description),
                "description_sha256": sha256_text(description) if description else None,
                "content_available": isinstance(content, str) and bool(content),
                "content_length": len(content) if isinstance(content, str) else None,
                "content_sha256": sha256_text(content) if isinstance(content, str) and content else None,
                "variables": extract_variables(content) if isinstance(content, str) and content else [],
                "structural_signals": structural_signals(content) if isinstance(content, str) and content else None,
                "verification": "source-api-observed",
                "capture_mode": "public-rpc-metadata",
                "metadata": {
                    "rpc_endpoint": endpoint,
                    "content_storage_policy": "body-not-stored; fingerprint-and-structure-only",
                    "directory_access_observed": row.get("access_observed"),
                    "directory_category_observed": row.get("category_observed"),
                },
            }
            results.append(record)
            status_counts[record["access"]] += 1

            if args.delay_ms:
                await asyncio.sleep(args.delay_ms / 1000)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in results:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "records": len(results),
        "access_counts": dict(status_counts),
        "category_counts": dict(category_counts.most_common()),
        "free_with_public_content": free_with_content,
        "premium_with_null_content": premium_content_null,
        "category_mismatches": mismatches[:100],
        "category_mismatch_count": len(mismatches),
        "rpc_endpoint": endpoint,
        "content_storage_policy": "Prompt bodies are never written. Free bodies are processed in-memory only for length, SHA-256, variables and structural signals. Premium bodies are not available from the public RPC and remain null.",
    }
    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/normalized/alpacka-ai-prompt-metadata.jsonl")
    parser.add_argument("--manifest", default="quarry/normalized/alpacka-ai-prompt-metadata-manifest.json")
    parser.add_argument("--delay-ms", type=int, default=120)
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
