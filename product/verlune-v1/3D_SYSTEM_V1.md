# Verlune 3D System v1

Status: `IMPLEMENTED CANDIDATE / FEATURE BRANCH ONLY`
Date: 2026-09-23

## Purpose

Define the semantic 3D language implemented in the Verlune v2 feature-branch redesign.

3D is not a decoration layer. It materializes structure, transformation, state and verification.

## Implementation priority

1. CSS 3D transforms + DOM.
2. SVG + CSS where path semantics are clearer.
3. Canvas/WebGL only if an observed implementation limitation justifies it.

Current implementation uses CSS/DOM and does not require a 3D engine.

## Semantic primitives

### StructureBlock

Represents a Prompt, Workflow, Builder or verification object.

Properties:
- dark low-gloss surface;
- restrained mint edge;
- shallow perceived extrusion;
- readable front face;
- no toy/plastic appearance.

### GraphPlane

Represents the structured context around a group of related objects.

Properties:
- subtle grid;
- fades before page edges;
- never carries unique information.

### Connector

Represents a real relationship or flow.

Use only for:
- valid stage connection;
- transfer;
- dependency;
- fallback;
- verification path.

### VerificationSeal

Represents an actual check or verification state.

Never use it as a generic quality badge.

## Depth levels

- Z0 — page field.
- Z1 — reading/navigation surface.
- Z2 — semantic graph plane.
- Z3 — focused StructureBlock.

Do not exceed four meaningful depth levels in one scene.

## Perspective

Desktop:
- mild perspective;
- primary readable faces remain close to frontal;
- rotation target <= approximately 8 degrees.

Mobile:
- no perspective dependency;
- transform into a vertical semantic stack;
- all labels remain legible without rotation.

## Motion verbs

- ASSEMBLE — fragments align into structured blocks.
- CONNECT — semantic relationships become visible.
- FOCUS — selected object gains subtle z-depth.
- VERIFY — a state resolves into the verification state.
- TRANSFER — a structured object moves directionally toward execution/reuse.

Forbidden:
- infinite idle floating;
- continuous rotation;
- camera fly-through;
- orbit controls;
- physics bounce;
- decorative particles.

## Timing

- micro feedback: 120ms;
- standard UI: 180ms;
- graph transition: 260ms;
- scene transformation: 420ms target.

Reduced-motion mode removes nonessential transforms and preserves all information.

## Current code mapping

`web/components/verlune-visuals.tsx`
- `VerluneGraph`
- `ArtifactMiniObject`
- `AssetStructureMap`

`web/app/globals.css`
- `.vGraph*`
- `.vMiniObject*`
- `.vStructureMap*`

## Validation

Before public release:
- validate at 390 / 768 / 1440 / 1920;
- confirm reduced-motion parity;
- verify no graph label becomes unreadable;
- profile initial paint and idle CPU;
- confirm 3D does not delay meaningful first content;
- visually compare Home, Premium Library and Asset Detail for material consistency.
