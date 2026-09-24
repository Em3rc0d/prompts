# Verlune Hero V3 — Implementation Plan

Status: READY FOR ASTRA IMPLEMENTATION
Date: 2026-09-23
Branch: `feat/verlune-product-model-v1-20260922-r2`

## 1. Goal

Replace only the homepage hero visual system with a higher-fidelity hybrid scene while preserving current product copy, navigation, routes, commerce, entitlement, Free/Premium catalogs, and truth boundaries.

Do not redesign unrelated surfaces during this task.

## 2. Current implementation to replace/refactor

Current:
- `web/components/verlune-visuals.tsx`
  - `VerluneGraph`
  - `ArtifactMiniObject`
  - `AssetStructureMap`
- `web/app/page.tsx`
- hero-related sections in `web/app/globals.css`

Do not break `ArtifactMiniObject` or `AssetStructureMap`, because Free/Premium/Asset Detail depend on them.

Refactor `VerluneGraph` behind a compatible public API or introduce a new hero-specific component.

## 3. Proposed file architecture

```text
web/
  components/
    hero-v3/
      VerluneHeroScene.tsx          # integration shell; server-safe boundary
      VerluneHeroCanvas.client.tsx  # dynamic WebGL runtime
      HeroSceneFallback.tsx         # DOM/SVG fallback
      HeroSemanticCards.tsx         # crisp DOM overlays
      scene/
        CentralStack.tsx
        SceneLighting.tsx
        PerspectiveField.tsx
        OrbitSystem.tsx
        AmbientDepth.tsx
        VerluneCore.tsx
      hero-v3.css                   # optional colocated styles; otherwise globals
```

If project conventions make a separate CSS file undesirable, keep styles in `globals.css`, but isolate them under `.vHero3*`.

## 4. Dependency spike

Before full implementation, add only:
- `three`
- `@react-three/fiber`

Build a minimal spike:
- one beveled/rounded slab;
- one rim/key light;
- one camera;
- one floor/grid;
- no postprocessing.

Evaluate:
- visual material quality;
- bundle/build compatibility with Next 16;
- hydration;
- deployment;
- mobile fallback.

Only if the target cannot be reached without bloom, add:
- `@react-three/postprocessing`
- `postprocessing`

Do not add large asset/model libraries.

## 5. Phase sequence

### Phase 0 — Freeze baseline
Capture current hero at:
- 1440×1000
- 1920×1080
- 768×1024
- 390×844

Record current bundle/build state.

### Phase 1 — Integration shell
- Keep current hero text/CTA untouched.
- Add `VerluneHeroScene` in the existing right-hand visual slot.
- Implement deterministic fallback first.
- Ensure first frame does not wait on WebGL.

Acceptance:
- no layout shift;
- fallback looks intentional;
- typecheck/build PASS.

### Phase 2 — Central physical object
Implement:
- 3–4 stacked slabs;
- real thickness/bevel;
- Verlune core seal;
- mint edge geometry;
- separation shadows.

Do not add cards yet.

Acceptance:
- object already reads as materially deeper than v2 with orbit/cards disabled.

### Phase 3 — Lighting + spatial field
Add:
- mint key/rim;
- neutral fill/specular;
- perspective floor/grid;
- sparse background translucent planes;
- bounded node lights.

Acceptance:
- clear foreground/midground/background;
- no cyberpunk clutter.

### Phase 4 — Orbit semantics
Add:
- 2–3 elliptical connector paths;
- sparse semantic nodes;
- relation between central object and overlay-card anchors.

No random spaghetti.

### Phase 5 — DOM semantic cards
Build `HeroSemanticCards`:
- Prompt
- Workflow
- Builder
- Verify

Requirements:
- crisp DOM text;
- glass material recipe;
- desktop spatial placement;
- tablet/mobile recomposition;
- no interaction required to understand scene.

### Phase 6 — Entry motion
Implement one finite ASSEMBLE sequence.
No continuous spinning/floating.

Respect:
- `prefers-reduced-motion`
- static fallback.

### Phase 7 — Optional selective bloom
Only after Phase 2–6 screenshots.

Add postprocessing only if:
- emissive edges still fail to read as luminous;
- measurable cost remains acceptable;
- mobile path remains excluded.

### Phase 8 — Quality tiers
Create scene quality profiles:
- HIGH: >=1200 desktop
- MEDIUM: 900–1199
- FALLBACK: <900 or constrained/reduced-motion case

Quality controls:
- DPR cap;
- background object count;
- shadows;
- postprocess;
- node count.

### Phase 9 — Visual validation
Compare implementation to the approved target by dimensions:
- composition;
- central-object scale;
- depth;
- materiality;
- glow;
- orbit readability;
- card placement;
- atmospheric separation;
- copy legibility.

Do not use an overall subjective PASS until dimension-level review is recorded.

### Phase 10 — Regression
Run:
- `npm run typecheck`
- `npm run build`
- existing postbuild audits

Then verify:
- Home
- Free
- Premium
- Unlock
- one Premium asset

No merge.

## 6. Implementation invariants

Must preserve:
- homepage headline/copy unless separately authorized;
- Free/Premium facts;
- product routes;
- access/session behavior;
- governed asset identities;
- current build audits;
- no fake social proof;
- no fake telemetry.

Must not:
- replace full page with Canvas;
- render important copy inside WebGL;
- load video;
- use external 3D models;
- add continuous animation loops for decoration;
- redesign Premium Library during this task.

## 7. Technical acceptance

Required:
- SSR hero text works with JS disabled;
- Canvas failure still leaves complete hero;
- no console errors;
- no hydration warnings;
- no layout shift attributable to scene;
- no mandatory WebGL on mobile;
- reduced-motion mode complete;
- typecheck/build/postbuild PASS.

## 8. Visual acceptance

The implementation must visibly close these v2 gaps:
- physical thickness;
- transparent/glass material;
- edge/specular lighting;
- atmospheric depth;
- scene-scale perspective;
- central focal dominance;
- floating-card depth;
- controlled glow;
- spatial relationship between cards and core.

If the result is merely “the same v2 scene with more glow”, reject the iteration.
