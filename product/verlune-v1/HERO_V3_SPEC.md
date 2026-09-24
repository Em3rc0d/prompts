# Verlune Hero V3 — Visual / Technical Specification

Status: AUTHORIZED PLAN / IMPLEMENTATION NOT STARTED
Date: 2026-09-23
Target: homepage hero first; reusable scene language may later support Premium.

## 1. Why V3 exists

The current v2 implementation communicates the product correctly but does not match the approved visual master in perceived depth, material quality, lighting, atmosphere, or spatial composition.

Observed limitation:
- current `VerluneGraph` is DOM + CSS 3D;
- it provides readable semantic structure;
- it does not provide convincing glass thickness, refraction/specular response, layered light, cinematic depth, volumetric-feeling atmosphere, or a strong physical center of gravity.

V3 must preserve v2 product semantics while materially improving visual fidelity.

## 2. North-star visual target

The approved direction is the user-reviewed cinematic Verlune hero:
- dark editorial canvas;
- mint functional accent;
- sculptural central stack;
- translucent / glass-like layered planes;
- luminous edge treatment;
- perspective grid floor;
- restrained orbital connectors;
- floating Prompt / Workflow / Builder / Verify surfaces;
- atmospheric depth and highlights;
- premium, calm, computational—not game UI or cyberpunk noise.

The image is a visual target only. It is not a factual source.

## 3. Contract precedence for Hero V3

This specification is the more specific contract for the homepage Hero V3 and supersedes the earlier CSS/DOM-first implementation priority **for this hero only**.

Explicit bounded changes:
- WebGL/R3F is now authorized for the homepage hero when isolated behind a progressive fallback;
- finite/static ambient depth points are permitted as spatial cues;
- continuous decorative particle systems remain forbidden;
- the rest of Verlune remains under the existing V2 DOM/CSS-first contracts unless separately authorized.

This does not relax product-truth, accessibility, responsive, or performance boundaries.

## 4. Architecture decision

Use a HYBRID scene.

### WebGL / R3F owns
- central 3D stack;
- physical planes and edge geometry;
- camera and perspective;
- point / directional / rim light;
- perspective floor/grid;
- orbital geometry;
- static/finite ambient depth points;
- background depth objects;
- optional post-processing bloom if measured and justified.

### DOM owns
- headline, copy and CTAs;
- Prompt / Workflow / Builder / Verify text cards;
- semantic labels;
- links and interactive controls;
- accessible text alternatives.

Reason:
- WebGL produces the materiality and lighting the current implementation cannot;
- DOM keeps text crisp, selectable, responsive, accessible and SEO-safe;
- only the hero carries runtime 3D complexity.

## 5. Scene composition

Desktop hero remains approximately 5/12 text + 7/12 visual.

### Z0 — page field
Very dark neutral field. No decorative gradient noise.

### Z1 — perspective field
Receding grid / coordinate plane under the central object.
Purpose: establish spatial scale and process field.

### Z2 — background structure
Sparse translucent vertical/rectangular planes.
Purpose: depth only; must never imply fake data.

### Z3 — orbit / relation field
2–3 thin elliptical paths around the core.
Nodes are sparse and correspond visually to the semantic cards.

### Z4 — central Verlune stack
Primary focal object:
- 3–4 stacked rounded square/rectangular slabs;
- real thickness;
- dark transparent material;
- mint edge light;
- neutral specular highlight;
- subtle separation shadows;
- top slab carries Verlune core/seal;
- stack should occupy ~42–52% of visual scene height on desktop.

### Z5 — semantic cards
Four DOM overlays:
- PROMPT — Structured input
- WORKFLOW — Stages + decisions
- BUILDER — Build yours
- VERIFY — Verify

Cards use perspective/translate/rotate only for placement.
No continuous floating.

## 6. Material system

### Core slab
Candidate:
- dark transparent physical material;
- transmission-like appearance without requiring environment texture packs;
- roughness approximately 0.28–0.42;
- metalness near 0;
- opacity/transmission tuned for edge visibility;
- bevelled geometry or edge line pass.

### Card glass
DOM:
- rgba dark surface;
- 1px mint-alpha border;
- backdrop blur only where supported;
- pseudo-element highlight;
- subtle directional shadow.

### Light
Primary:
- mint rim/key light.

Secondary:
- neutral white specular accent.

Forbidden:
- rainbow reflections;
- saturated blue/purple cyberpunk mix;
- bloom that reduces text legibility.

## 7. Lighting

Desktop target:
- one mint key/rim source;
- one low-intensity neutral fill;
- one weak top/side highlight;
- emissive edge geometry on central stack;
- optional selective bloom only on emissive geometry and nodes.

The scene should read clearly with bloom disabled. Bloom enhances; it must not create the structure.

## 8. Motion

Motion is secondary to the first frame.

Entry only:
1. background field fades in;
2. central slabs assemble over 360–520ms;
3. orbit connectors draw/fade;
4. DOM cards enter with small z/y offset;
5. verify seal resolves last.

Idle:
- no object spinning;
- no camera orbit;
- no perpetual card bobbing;
- optional very low-amplitude light breathing or node drift only if CPU impact is negligible and it does not violate reduced motion.

Reduced motion:
- static first frame;
- no assembly;
- no camera/perspective animation;
- all semantic information identical.

## 9. Responsive model

### >= 1200
Full hybrid 3D scene.

### 900–1199
Same scene with lower render quality:
- fewer depth objects;
- simpler shadows;
- reduced DPR cap;
- simplified orbit geometry.

### 600–899
Prefer static CSS/SVG/DOM fallback or low-cost canvas scene.
No postprocessing.

### < 600
No runtime WebGL required.
Use vertical semantic stack / still illustration treatment.

### prefers-reduced-motion
Use static fallback unless runtime scene has zero motion and no accessibility/performance penalty.

## 10. Performance boundaries

Target budgets:
- hero text and CTA must render without waiting for WebGL;
- no layout shift when scene hydrates;
- dynamic import the runtime 3D scene;
- no external model files;
- no texture packs;
- no background video;
- DPR capped;
- scene must stop unnecessary frame work when not visible where feasible;
- mobile fallback must not load the full 3D dependency path if avoidable.

Dependency preference:
1. `three`
2. `@react-three/fiber`
3. `@react-three/postprocessing` only if selective bloom is proven necessary

Do not add `@react-three/drei` by default; add only for a concrete implementation need.

## 11. Accessibility

- Canvas is decorative/semantic-supporting, never the only carrier of information.
- Existing hero copy remains server-rendered DOM.
- Scene gets a concise text alternative.
- DOM cards must not create duplicate screen-reader noise when equivalent text is already present.
- Keyboard flow unchanged.
- Reduced motion respected.
- Color is never sole state encoding.

## 12. Product truth boundaries

Do not add:
- fake activity;
- fake analytics;
- fake system status;
- fake usage counts;
- fake ratings;
- fake certification;
- fake workflow execution;
- decorative data streams presented as real.

The scene represents product concepts, not live telemetry.

## 13. Visual acceptance criteria

At 1440×1000 and 1920×1080, reviewers should observe:

1. Central stack has obvious physical thickness and layered depth.
2. Edge light and specular highlights make materials read as glass/physical planes rather than CSS cards.
3. Scene has foreground / midground / background separation.
4. Prompt / Workflow / Builder / Verify remain readable.
5. Scene has a stronger focal hierarchy than the v2 screenshot.
6. No element resembles fake analytics or decorative code rain.
7. The hero remains calm despite greater depth.
8. Left copy remains at least as legible and dominant as v2.
9. Mobile does not look like a shrunk desktop 3D scene.
10. Reduced-motion view communicates the same product meaning.

## 14. Gate

V3 may replace v2 only after:
- visual target comparison;
- 1440 + 1920 desktop review;
- 390 + 768 responsive review;
- reduced-motion check;
- typecheck/build/postbuild PASS;
- no regression to entitlement/product truth surfaces.

`V3_VISUAL_ACCEPTANCE = OPEN`
