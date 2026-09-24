# Astra Handoff — Verlune Hero V3

## Mission

Improve the Verlune homepage hero so its 3D visual fidelity materially approaches the approved cinematic master while preserving the product semantics and the existing stable web product.

You are not being asked for a generic redesign. You are being asked to implement a bounded Hero V3.

## Repository / branch

Repository:
`Em3rc0d/prompts`

Branch:
`feat/verlune-product-model-v1-20260922-r2`

Do not merge.

## Read first

1. `product/verlune-v1/HERO_V3_SPEC.md`
2. `product/verlune-v1/HERO_V3_IMPLEMENTATION_PLAN.md`
3. `product/verlune-v1/DESIGN_V2.md`
4. `product/verlune-v1/UI_CONTRACT_V2.md`
5. `product/verlune-v1/3D_SYSTEM_V1.md`
6. `web/components/verlune-visuals.tsx`
7. `web/app/page.tsx`
8. relevant hero sections of `web/app/globals.css`
9. `web/package.json`

## Visual diagnosis you must preserve

The current v2 hero is structurally correct but visually underpowered.

It currently reads as:
`flat DOM cards + CSS transforms + restrained glow`

The target must read more like:
`physical layered object + glass material + real lighting + foreground/midground/background + semantic orbital field + crisp DOM labels`

Do not solve this by adding random neon, more cards, code rain, fake dashboards, or decorative data.

## Required architecture

Use a hybrid approach:
- WebGL/R3F only for physical scene/material/light/depth;
- DOM for all readable semantic cards, hero copy and CTAs;
- fallback for mobile/reduced-motion/no-WebGL path.

Start with:
- `three`
- `@react-three/fiber`

Add postprocessing only if the non-postprocessed implementation cannot meet the target.

## Work order

1. Freeze baseline screenshots.
2. Create fallback/integration shell.
3. Implement central stack alone.
4. Tune material and lighting until the central object is already superior to v2.
5. Add perspective field/background depth.
6. Add semantic orbit geometry.
7. Add DOM Prompt/Workflow/Builder/Verify overlays.
8. Add finite entry assembly.
9. Implement quality tiers/fallback.
10. Run visual comparison.
11. Run typecheck/build/postbuild.
12. Record implementation evidence.

Do not jump to Phase 7 before the central object works.

## Non-negotiable visual requirements

- obvious physical thickness;
- layered slab separation;
- mint edge/rim light;
- neutral specular highlight;
- dark glass/translucent material;
- perspective floor;
- scene depth beyond one flat panel;
- central sculptural focus;
- orbit paths visibly related to the semantic cards;
- readable cards;
- calm premium composition.

## Non-negotiable product requirements

Do not change:
- product facts;
- pricing/commerce logic;
- entitlement;
- Free/Premium catalog contents;
- governed asset files;
- public claims;
- headline/copy unless required for layout and explicitly recorded.

Never add:
- fake usage;
- ratings;
- activity;
- certification;
- telemetry;
- execution status.

## Performance / a11y

- first meaningful hero frame must not depend on WebGL;
- dynamic-load 3D runtime;
- no large models/textures/video;
- no desktop scene copied verbatim to mobile;
- reduced motion must be complete;
- semantic information remains in DOM;
- no keyboard regression.

## Definition of done

Do not say “done” because the scene compiles.

Return evidence for:
- 1440 desktop;
- 1920 desktop;
- 768 tablet;
- 390 mobile;
- reduced motion;
- typecheck;
- production build;
- postbuild audits.

Also return a gap table:

| Dimension | v2 | Hero V3 | Remaining gap |
|---|---|---|---|
| depth | | | |
| material | | | |
| lighting | | | |
| composition | | | |
| orbit semantics | | | |
| atmospheric separation | | | |
| text legibility | | | |
| mobile | | | |

If a material gap remains, say so rather than declaring visual parity.

## Stop conditions

Stop and report before proceeding if:
- R3F breaks Next build/hydration;
- WebGL adds unacceptable first-load/layout regression;
- mobile cannot avoid loading the heavy scene;
- meeting the visual target would require fake product semantics;
- an unrelated access/commerce behavior changes.

## Final state

A successful implementation ends with:

```text
HERO_V3_IMPLEMENTED            true
TYPECHECK                      PASS
BUILD                          PASS
POSTBUILD_AUDITS               PASS
DESKTOP_VISUAL_REVIEW          READY
MOBILE_VISUAL_REVIEW           READY
HUMAN_VISUAL_ACCEPTANCE        OPEN
MERGE                          NOT AUTHORIZED
```
