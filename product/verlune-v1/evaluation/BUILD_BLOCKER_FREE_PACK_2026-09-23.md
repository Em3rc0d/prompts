# Verlune v1 — Local build blocker: Free Pack materialization

Date: 2026-09-23

Status: `PATCHED / OPERATOR RERUN REQUIRED`

## Observation

The first local access-product validation produced:

```text
npm run typecheck
PASS

npm run build
prebuild → scripts/fetch-free-pack.mjs
FREE PACK MATERIALIZE FAIL: HTTP 500
```

The build never reached Next.js compilation or the Premium leakage audit.

## External response observed

The configured default source was:

`https://prompt-quarry.vercel.app/api/free-pack/v1.1.0`

Observed response:

- HTTP: 500
- error: `free_pack_integrity_failure`
- observed size: `23498`
- observed SHA-256: `ba02210e8649ec1e601d65afae3b31e4985de1ab577483d5c155540f5f8f7dbf`
- frozen expected size: `23498`
- frozen expected SHA-256: `55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32`

## Root cause

The governed release contract defines byte ordering as lexicographic.

The API route sorted archive paths with JavaScript `localeCompare()`. That ordering places lowercase `prompts/...` before uppercase `QUICKSTART.md` / `README.md` under the observed runtime, while the governed deterministic builder uses raw lexical comparison.

Same payload size + different entry order produced a different ZIP byte hash and the route correctly failed closed.

A second architectural issue was also exposed: a local production build depended on the already-deployed production endpoint being healthy. That creates an unnecessary circular availability dependency.

## Patch

1. `web/app/api/free-pack/v1/route.ts`
   - replaced locale-sensitive sorting with raw deterministic lexical comparison.

2. `web/scripts/fetch-free-pack.mjs`
   - default materialization now rebuilds the archive from the governed local `MANIFEST.release.json` + exact source files;
   - verifies every asset size, Git blob SHA-1 and SHA-256;
   - verifies final archive size + SHA-256;
   - writes the same generated Base64 module;
   - network verification remains available only when `PQ_FREE_PACK_RELEASE_SOURCE` is explicitly supplied.

## Evidence boundary

This patch has not yet been observed passing on the operator's Windows/Node 24 environment.

Required rerun:

```powershell
git pull origin feat/verlune-product-model-v1-20260922-r2
cd web
npm run typecheck
npm run build
```

Expected prebuild evidence:

```text
FREE PACK MATERIALIZE: PASS
source=local-governed-manifest
assets=7
size=23498
sha256=55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32
```

Then the Next.js build and Premium post-build audit must also pass before the access build gate can close.
