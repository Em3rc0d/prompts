#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import os
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path

EXPECTED_FREE_SHA256 = "55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32"
EXPECTED_FREE_SIZE = 23498
EXPECTED_FREE_VERSION = "1.1.0"

STATIC_ROUTES = [
    "/",
    "/free/developer-starter-pack",
    "/developer-pack",
    "/license",
]
FREE_ROUTE = "/api/free-pack/v1.1.0"
CHECKOUT_ROUTE = "/api/commerce/developer-pack/checkout"

ATTRIBUTION = {
    "source": "golden-path",
    "medium": "stress",
    "campaign": "pq-golden-path-0",
    "content": "resilience-v1",
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        return None


@dataclass
class Sample:
    route: str
    status: int
    latency_ms: float
    bytes: int
    error: str | None = None
    integrity_ok: bool | None = None


def pct(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    pos = max(0, min(len(ordered) - 1, math.ceil(q * len(ordered)) - 1))
    return round(ordered[pos], 2)


def target(base: str, path: str, query: dict[str, str] | None = None) -> str:
    url = urllib.parse.urljoin(base.rstrip("/") + "/", path.lstrip("/"))
    if query:
        url += "?" + urllib.parse.urlencode(query)
    return url


def request_once(base: str, path: str, *, timeout: float, unique: int, no_redirect: bool = False) -> Sample:
    query = dict(ATTRIBUTION) if path in (FREE_ROUTE, CHECKOUT_ROUTE) else {}
    query["stress_case"] = str(unique)
    url = target(base, path, query)
    req = urllib.request.Request(url, headers={
        "User-Agent": "PromptQuarryGoldenPathStress/1.0",
        "Cache-Control": "no-cache",
    })
    opener = urllib.request.build_opener(NoRedirect) if no_redirect else urllib.request.build_opener()
    started = time.perf_counter()
    try:
        with opener.open(req, timeout=timeout) as response:
            body = response.read()
            status = response.status
            headers = {k.lower(): v for k, v in response.headers.items()}
    except urllib.error.HTTPError as exc:
        body = exc.read()
        status = exc.code
        headers = {k.lower(): v for k, v in exc.headers.items()}
    except Exception as exc:  # network/timeout bucket
        return Sample(path, 0, round((time.perf_counter() - started) * 1000, 2), 0, type(exc).__name__)

    elapsed = round((time.perf_counter() - started) * 1000, 2)
    integrity_ok: bool | None = None
    error: str | None = None
    if path == FREE_ROUTE and status == 200:
        observed = hashlib.sha256(body).hexdigest()
        integrity_ok = (
            len(body) == EXPECTED_FREE_SIZE
            and observed == EXPECTED_FREE_SHA256
            and headers.get("x-prompt-quarry-version") == EXPECTED_FREE_VERSION
            and headers.get("x-prompt-quarry-sha256") == EXPECTED_FREE_SHA256
        )
        if not integrity_ok:
            error = "integrity_mismatch"
    return Sample(path, status, elapsed, len(body), error, integrity_ok)


def run_phase(base: str, route: str, *, requests: int, concurrency: int, timeout: float, offset: int) -> dict:
    started = time.perf_counter()
    samples: list[Sample] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [
            pool.submit(request_once, base, route, timeout=timeout, unique=offset + i)
            for i in range(requests)
        ]
        for future in concurrent.futures.as_completed(futures):
            samples.append(future.result())
    wall = time.perf_counter() - started
    latencies = [s.latency_ms for s in samples if s.status]
    statuses = Counter(str(s.status) for s in samples)
    errors = Counter(s.error for s in samples if s.error)
    integrity_failures = sum(1 for s in samples if s.integrity_ok is False)
    success = sum(1 for s in samples if 200 <= s.status < 400 and not s.error)
    return {
        "route": route,
        "requests": requests,
        "concurrency": concurrency,
        "wall_seconds": round(wall, 3),
        "throughput_rps": round(requests / wall, 2) if wall else None,
        "success_rate": round(success / requests, 4),
        "status_counts": dict(statuses),
        "error_counts": {str(k): v for k, v in errors.items()},
        "integrity_failures": integrity_failures,
        "latency_ms": {
            "min": round(min(latencies), 2) if latencies else None,
            "mean": round(statistics.mean(latencies), 2) if latencies else None,
            "p50": pct(latencies, 0.50),
            "p95": pct(latencies, 0.95),
            "p99": pct(latencies, 0.99),
            "max": round(max(latencies), 2) if latencies else None,
        },
    }


def baseline(base: str, timeout: float) -> dict:
    result: dict[str, object] = {"routes": {}, "golden_path_pass": True, "breaks": []}
    routes: dict[str, object] = result["routes"]  # type: ignore[assignment]

    for idx, route in enumerate(STATIC_ROUTES):
        sample = request_once(base, route, timeout=timeout, unique=idx)
        routes[route] = asdict(sample)
        if sample.status != 200:
            result["golden_path_pass"] = False
            result["breaks"].append(f"{route}:HTTP_{sample.status}")  # type: ignore[union-attr]

    free = request_once(base, FREE_ROUTE, timeout=timeout, unique=1000)
    routes[FREE_ROUTE] = asdict(free)
    if free.status != 200 or free.integrity_ok is not True:
        result["golden_path_pass"] = False
        result["breaks"].append(f"{FREE_ROUTE}:DELIVERY_INTEGRITY")  # type: ignore[union-attr]

    checkout = request_once(base, CHECKOUT_ROUTE, timeout=timeout, unique=2000, no_redirect=True)
    routes[CHECKOUT_ROUTE] = asdict(checkout)
    if checkout.status not in (301, 302, 303, 307, 308):
        result["golden_path_pass"] = False
        result["breaks"].append(f"{CHECKOUT_ROUTE}:HTTP_{checkout.status}")  # type: ignore[union-attr]

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Bounded production stress test for Prompt Quarry Golden Path")
    parser.add_argument("--base-url", default=os.getenv("PQ_BASE_URL", "https://prompt-quarry.vercel.app"))
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--output", default=".ci/golden-path/latest.json")
    parser.add_argument("--max-concurrency", type=int, default=20)
    parser.add_argument("--requests-per-phase", type=int, default=60)
    args = parser.parse_args()

    parsed = urllib.parse.urlparse(args.base_url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise SystemExit("Golden Path stress requires an absolute HTTPS base URL")

    report = {
        "schema_version": "1.0",
        "test": "pq-golden-path-resilience-v1",
        "base_url": args.base_url,
        "started_at_epoch": int(time.time()),
        "evidence_boundary": "HTTP/runtime resilience only; no F4/F5/F6/F7 model-behavior claim.",
        "baseline": baseline(args.base_url, args.timeout),
        "phases": [],
    }

    # Stress static/customer navigation surfaces first.
    offset = 10_000
    for route in STATIC_ROUTES:
        report["phases"].append(run_phase(
            args.base_url,
            route,
            requests=max(20, args.requests_per_phase // 2),
            concurrency=min(10, args.max_concurrency),
            timeout=args.timeout,
            offset=offset,
        ))
        offset += 1000

    # Escalating pressure on the dynamic deterministic delivery path.
    for concurrency in [1, 5, 10, args.max_concurrency]:
        report["phases"].append(run_phase(
            args.base_url,
            FREE_ROUTE,
            requests=args.requests_per_phase,
            concurrency=concurrency,
            timeout=args.timeout,
            offset=offset,
        ))
        offset += 10_000

    failures: list[str] = []
    if not report["baseline"]["golden_path_pass"]:
        failures.extend(report["baseline"]["breaks"])

    for phase in report["phases"]:
        if phase["success_rate"] < 0.99:
            failures.append(f"{phase['route']}@c{phase['concurrency']}:success_rate={phase['success_rate']}")
        if phase["integrity_failures"]:
            failures.append(f"{phase['route']}@c{phase['concurrency']}:integrity_failures={phase['integrity_failures']}")
        p95 = phase["latency_ms"]["p95"]
        if p95 is not None and p95 > 3000:
            failures.append(f"{phase['route']}@c{phase['concurrency']}:p95_ms={p95}")

    report["result"] = "FAIL" if failures else "PASS"
    report["failures"] = failures
    report["completed_at_epoch"] = int(time.time())

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
