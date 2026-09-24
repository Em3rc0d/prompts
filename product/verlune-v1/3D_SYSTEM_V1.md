# Verlune 3D System v1

Status: IMPLEMENTED CANDIDATE / VALIDATION REQUIRED
Date: 2026-09-23

## Purpose

Define the semantic 3D language used by Verlune v2.

3D exists to make structure, transformation, hierarchy, and verification visible. It is not ambient decoration.

## Object grammar

### StructureBlock
Represents a Prompt, Workflow, Builder artifact, or verification object.

Rules:
- dark low-gloss material;
- mint edge light;
- subtle extrusion;
- labels stay readable;
- no toy/plastic styling.

### GraphPlane
Represents process context and relations between objects.

Rules:
- grid is subordinate to content;
- no fake analytics;
- grid density reduces on small screens.

### Connector
Represents a real flow or dependency.

Rules:
- every connection must correspond to a product concept;
- no decorative spaghetti lines.

### VerificationSeal
Represents an actual check/boundary.

Rules:
- mint confirmation only after a real verification state in interactive UI;
- never imply certification where none exists.

## Material recipe

Base:
- #090D0F / #0D1316 / #11191D
- low-gloss dark surfaces
- 1px borders with mint-alpha 0.2–0.5

Accent:
- #BFE3D0
- stronger active highlight: #77F2BA

Light:
- single dominant mint edge light;
- neutral white specular highlight;
- no rainbow reflections;
- glow only around active semantic states.

## Perspective

Desktop:
- CSS perspective ~1100px;
- primary object rotation <= 8 degrees;
- layered z-depth remains readable.

Mobile:
- perspective simplified;
- semantic vertical stack preferred;
- no orbit/camera control.

## Motion

Allowed:
- ASSEMBLE
- CONNECT
- FOCUS
- VERIFY
- TRANSFER

Timing:
- micro: 120ms
- UI: 180ms
- graph: 260ms
- scene: 420ms

Forbidden:
- infinite floating loops;
- idle spin;
- camera fly-through;
- physics bounce;
- decorative particles;
- interaction that requires 3D to understand content.

## Implementation priority

1. DOM + CSS 3D
2. SVG + CSS
3. Canvas/WebGL only if a measured implementation limit requires it

Current implementation uses DOM/CSS primitives so:
- text stays semantic;
- first frame works before animation;
- responsive fallback is cheap;
- reduced-motion can remove transforms.

## Accessibility

- 3D never carries unique information;
- each graph has a textual/ARIA equivalent;
- reduced-motion removes scene animation/perspective shifts;
- focus/selection must remain visible without glow;
- color is not the only state signal.

## Performance

- no external 3D runtime;
- no texture packs;
- no video background;
- no continuous animation after entry except subtle nonessential effects;
- no layout shifts from scene hydration.

## Implemented primitives

- VerluneGraph
- ArtifactMiniObject
- AssetStructureMap

These map to the UI contract and may evolve only if visual validation shows a real usability or performance reason.
