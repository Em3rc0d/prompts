# Verlune Hero V3 — implementation and validation

Date: 2026-09-24. Branch: `feat/verlune-product-model-v1-20260922-r2`. This is a feature-branch candidate, not a visual acceptance or release approval.

## Scope and architecture

- Only the homepage hero was replaced. The existing headline, body copy, CTAs and routes are unchanged. The three product proof items were moved below the visual in DOM order so mobile sees the visual directly after the CTAs.
- Server-rendered DOM owns all product text, links, four semantic cards and the static scene fallback. A small client gate lazy-loads React Three Fiber only when the scene enters the viewport at widths of at least 900px, WebGL2 is available and reduced motion is off.
- WebGL owns four beveled extruded slabs, seal, physical dark materials, mint/neutral lights, a perspective grid, sparse depth planes and two or three orbital relation paths. The canvas draws on demand, with a finite 460ms assembly; no idle animation, external model, texture, video, Drei or postprocessing.
- DPR is capped at 1.6 on desktop and 1.25 at 900–1199px. At under 900px, in reduced motion, without JavaScript or without WebGL2, a fixed-size static scene and the same DOM cards remain visible. The fallback is an intentional graphic treatment, not the approved 3D fidelity target.
- Added runtime dependencies: `three`, `@react-three/fiber`. Added dev types: `@types/three`.
- `ArtifactMiniObject`, `AssetStructureMap` and the Premium Library's `VerluneGraph` remain unchanged. No commerce, entitlement, catalog, pricing, asset-content or public-claim file was edited.

## V2 → V3 visual review

The approved image `ChatGPT Image 23 sept 2026, 10_57_23 p.m..png` is a visual reference only. This table evaluates the actual WebGL capture, except tablet/mobile and reduced motion, which intentionally use the fallback.

| Dimension | Current V2 | Hero V3 candidate | Remaining gap to approved image |
| --- | --- | --- | --- |
| Central depth | Three translated CSS planes | Four distinct modeled slabs | Far fewer layers and interior detail |
| Slab thickness | Border/shadow illusion | Visible extruded sides and bevels | Sides still uniform and somewhat synthetic |
| Material quality | Flat dark gradients | Physically lit dark transparent surfaces | Less nuanced than polished dark glass |
| Glass/translucency | Simulated CSS opacity | Real mesh transparency and layered overlap | No convincing refraction or optical distortion |
| Edge lighting | Uniform borders | Separate mint/neutral rim treatment | Less variation and sparkle along edges |
| Specular response | Static gradients | Physical material responds to lights | Neutral highlights remain subdued |
| Scene perspective | Local transformed grid | Perspective camera and 3D floor grid | Shallower field than the reference |
| Fore/mid/background | Mostly one bordered panel | Cards, core, orbital paths and distant planes | Background planes look sparse and plain |
| Atmosphere | Radial gradient | Spatial field and low-contrast depth elements | Lacks cinematic scattering/soft depth |
| Orbit semantics | Two flat ellipses | 2–3 world-space paths and four nodes | Card-to-node correspondence is approximate |
| Floating cards | Small CSS cards in panel | Four DOM glass cards on distinct axes | Lighting/depth relation to 3D core can improve |
| Central focal hierarchy | Small core competes with cards | Larger central modeled object | Cards approach core at 1024px |
| Text legibility | Good | Preserved; all readable text remains DOM | No material regression observed |
| Premium perception | Structured but visually flat | More tangible, spatial composition | Still materially short of photographic target |
| Tablet 768 | Desktop cluster scaled down | Static wide scene with readable cards | Static layers lack true glass response |
| Mobile 390 | Miniaturized desktop cluster | Vertical scene followed by 2×2 semantic cards | Scene appears after CTAs, below initial fold |

The iteration closes a real depth/geometry gap, but **visual parity is not established**. A richer glass/refraction and atmospheric treatment remains for human art direction review. Bloom was not added because the structural scene does not depend on it and a global glow would hide the remaining material gap.

## Captures and runtime checks

Screenshots in `hero-v3-evidence/final/`:

- `1920.png`, `1440.png`: WebGL2 active, one canvas, four DOM cards, no console/page errors.
- `768.png`, `390.png`: no Canvas mounted; `768-hero.png` and `390-hero.png` show the complete below-the-fold composition.
- `reduced-1920.png`: no Canvas mounted, content and four DOM cards present.
- `fallback-1920.png`: WebGL2 explicitly unavailable; deliberate static scene and CTAs remain.

Playwright Chromium (software WebGL2) captured the production build at viewport DPR 1. Browser records in the same folder report zero page/console errors, document width equal to viewport width and layout shift score 0 for the observed loading window. All four semantic cards and the `/free` and `/unlock` links were present at every requested size. In a separate 1440px DPR 2 check, the Canvas backing ratio was capped at 1.6. An additional 1024px medium-tier browser check mounted the Canvas without errors or overflow. With JavaScript disabled, the static hero, text, semantic cards and both CTA destinations remained in the HTML. These checks do not measure performance on actual mobile hardware or prove the rendering of every GPU/driver.

Production browser route smoke: `/`, `/free`, `/free/asset/VF-P-DEV-001`, `/app` (expected redirect to `/unlock`) and `/unlock` returned successful pages without browser errors. No authenticated Premium or commerce transaction was exercised.

## Build gates

Baseline at `60a82df612530fa9da4aca3ea8cfc09d2b5ebb28`: typecheck, build, golden path, Premium and V2 audits PASS.

Hero V3 candidate: `npm run typecheck` PASS; `npm run build` PASS; golden path, Premium, V2 and new bounded Hero V3 build audits PASS. The V2 audit now checks the V3 homepage scene while continuing to require `VerluneGraph` in Premium. The new audit checks server-rendered copy/CTAs, dynamic WebGL gating, static/semantic fallback and responsive/reduced-motion boundaries; it does not claim visual quality.

## Open states

`HERO_V3_IMPLEMENTED=true` · `HUMAN_VISUAL_ACCEPTANCE=OPEN` · `MERGE=NOT_AUTHORIZED` · `READY_TO_SELL=unchanged`.
