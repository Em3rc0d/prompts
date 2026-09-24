
# Verlune Visual Contract v2

Status: DESIGN CANDIDATE / MOCKUPS AUTHORIZED / FRONTEND IMPLEMENTATION FROZEN UNTIL HUMAN REVIEW
Date: 2026-09-23

## 1. Purpose

Define the visual, interaction, motion, responsive, accessibility and validation rules for Verlune v2 before implementation.

The goal is not “more animation”. The goal is to make Verlune easier to understand, more memorable, more tactile and more commercially credible without increasing cognitive noise or weakening trust.

## 2. Provenance vocabulary

Use these labels when a design decision needs provenance:

- OFFICIAL — explicitly approved product or brand rule.
- OBSERVED — directly seen in the current product or reviewer behavior.
- INFERRED — derived from product structure or evidence.
- INSPIRED — adapted from an external principle without copying a branded implementation.
- GENERATED — newly proposed for v2 and requiring validation.

## 3. Product idea the interface must communicate

OFFICIAL:
Verlune is a library and toolkit for structured AI work.

Customer shorthand:
Use ours. Build yours. Work better with AI.

The interface must visually communicate:

UNSTRUCTURED NEED
→ STRUCTURED PROMPT / WORKFLOW
→ AI EXECUTION
→ VERIFICATION
→ REUSABLE WORK

It must distinguish:
- Prompt = bounded reusable instruction.
- Workflow = recurring process with stages, states or decisions where material.
- Builder = turns the user's recurring need/process into a reusable artifact.
- Verification = explicit checking, not decoration.
- AI execution happens in the user's compatible AI assistant.

## 4. Visual direction

OFFICIAL direction name: Editorial Computational.

Desired impression:
- editorial;
- precise;
- structured;
- computational;
- calm;
- tactile;
- observable;
- premium.

Must not feel like:
- generic SaaS dashboard;
- prompt marketplace;
- cyberpunk/neon AI;
- “AI magic” marketing;
- a wall of equal cards;
- motion demo;
- developer-only product with decorative non-technical categories.

## 5. Proprietary visual grammar: Verlune Graph

GENERATED.

Semantic primitives:
- Node: input, source, artifact or state.
- Connection: valid relationship or flow.
- Decision: material branch.
- Fallback: safe alternate path.
- Verification: check or confirmed boundary.
- Unknown: unresolved information.
- Stop: cannot proceed safely.

Use the graph in:
- homepage hero;
- Prompt vs Workflow explanation;
- workflow previews;
- Builder explanation;
- selected loading/transition states;
- marketing screenshots.

Rule: every graph element must correspond to a real product concept or state. Never use it as decorative wallpaper.

## 6. Layout

Desktop:
- primary content max-width 1280px;
- wide visual moments may reach 1440px;
- prose width 620–720px;
- 12-column conceptual grid;
- 24px primary gutter;
- 96–144px major section spacing;
- 8px base rhythm.

Tablet:
- 8-column conceptual grid;
- preserve hierarchy before symmetry;
- diagrams may recompose vertically.

Mobile:
- one primary column;
- graph becomes vertical, never a miniature desktop diagram;
- no hover-only interaction;
- critical targets at least 44px.

## 7. Information hierarchy

- One dominant idea per viewport.
- Cards are not the default container.
- Prefer editorial rows, split layouts, diagrams, preview panels and grouped indexes.
- Builders receive higher hierarchy than ordinary Prompts.
- Categories are navigation, not decorative color coding.
- Use size and whitespace before heavy font weight.

## 8. Color

OBSERVED: current dark-neutral base + restrained mint accent works.

GENERATED candidate tokens:
- background 0: #090D0F
- background 1: #0D1316
- surface 1: #11191D
- surface 2: #172126
- surface 3: #1C282E
- text strong: #F4F6F5
- text: #D6DEDB
- muted: #92A19F
- line: #26353A
- line strong: #3A4D52
- accent: #BFE3D0
- accent soft: #8EB7A1
- warning: #E7C88E
- danger: #E4A8A0

Rules:
- mint is functional emphasis, not ambient glow;
- no rainbow category system;
- gradients only when they express depth or state transition;
- no large saturated reading surfaces.

## 9. Typography

Two voices:
1. Editorial sans for headlines, navigation and product copy.
2. System mono for IDs, evidence states, graph labels and metadata.

Candidate stack:
- sans: Inter, Segoe UI, Arial, sans-serif.
- mono: SFMono-Regular, Consolas, Liberation Mono, monospace.

Candidate scale:
- Display XL: 72–88 desktop / 46–56 mobile.
- Display: 56–72 desktop / 40–48 mobile.
- H2: 36–48.
- H3: 22–28.
- Body L: 18–20.
- Body: 15–17.
- Micro: 12–13.

## 10. Motion grammar

Motion must explain what changed.

OFFICIAL verbs:
- ENTER — content becomes available.
- ASSEMBLE — unstructured pieces become structured.
- TRANSFER — content moves from Verlune to the user's AI workflow.
- FOCUS — selected item gains hierarchy.
- EXPAND — progressive disclosure.
- VERIFY — a check resolves.
- REORDER — process/graph changes structure.

GENERATED timing candidates:
- fast: 120ms;
- normal UI: 180ms;
- flow: 260ms;
- scene: 420ms.

Forbidden:
- infinite particles;
- auto-playing carousels;
- scroll hijacking;
- ornamental parallax;
- bouncing primary actions;
- large simultaneous card animations;
- motion required to understand content.

Reduced-motion mode must preserve all content and state.

## 11. Homepage structure

Hero:
- eyebrow: STRUCTURED AI WORK;
- strong headline about recurring AI work;
- short supporting copy;
- primary CTA: Explore free;
- secondary CTA: See Premium / Builders;
- right side: living Verlune Graph.

Hero graph:
messy nodes labelled goal, context, constraints, evidence
→ ASSEMBLE
→ Prompt / Workflow
→ AI
→ Verify
→ Reuse.

Section 2: Use ours / Build yours.
Two parallel paths joined by the same graph grammar.

Section 3: Prompt is not Workflow.
Prompt shown as compact bounded structure.
Workflow shown as stages + decision + fallback + verification.
Understandable without interaction.

Section 4: Library preview.
No wall of equal cards.
Use category rail + featured artifact + compact supporting rows.

Section 5: Trust and evidence.
Progressive disclosure. Ordinary customer sees clear boundaries; deeper evidence remains one click away.

Section 6: Premium capability.
Emphasize deeper workflows, Builders, adaptation and evaluation—not prompt count.

## 12. Premium Library

Keep headline: Use ours. Build yours.

Replace five static instruction boxes with a compact process rail:
FIND — COPY — RUN — VERIFY — REUSE.

Desktop navigation:
- category rail;
- type filters: All / Prompts / Workflows / Builders / Toolkit.

Hierarchy:
1. Builders featured.
2. Workflows with mini process maps.
3. Prompts as compact editorial assets.
4. Toolkit as utility section.

Preview grammar:
- Prompt: INPUT → INSTRUCTION → OUTPUT → CHECK.
- Workflow: TRIGGER → STAGE → DECISION → FALLBACK → VERIFY.
- Builder: YOUR NEED → INTERVIEW → ARTIFACT → QUICK TEST.

## 13. Asset page

Goal: feel like a tool, not a raw Markdown viewer.

Structure:
- back to library;
- type/category;
- name + short purpose;
- persistent Copy action;
- mini structure map;
- How to use rail;
- high-quality asset reading surface;
- optional progressive disclosure for inputs, output, fallback, verification and trust notes.

Copy interaction:
- immediate visual confirmation;
- state changes to Copied;
- optional small TRANSFER animation;
- no unnecessary toast stack.

## 14. UX laws applied

Hick:
- few primary choices;
- progressive disclosure for evidence and advanced details.

Fitts:
- primary targets >=44px;
- large obvious Copy, Unlock, Explore Free and Builder actions.

Jakob:
- familiar navigation, forms, filters, accordions, copy controls and access settings.
- novelty lives in graph language and composition, not basic usability.

Tesler:
- do not force prompt/workflow design complexity onto users;
- Builders absorb that complexity.

Working memory:
- chunk long workflows;
- keep visible state labels;
- do not require memory of hidden previous steps.

Gestalt:
- proximity means relationship;
- connections represent real flow;
- similarity represents artifact type.

Selective attention:
- one dominant CTA and one dominant visual story per section.

## 15. Accessibility

Required:
- WCAG AA minimum;
- full keyboard flow;
- visible focus;
- semantic headings;
- no hover-only meaning;
- accessible copy confirmation;
- labelled forms/errors;
- textual alternative for diagrams;
- reduced-motion path;
- 44px critical targets;
- color never sole state indicator.

## 16. Responsive validation

Required:
- 390px;
- 768px;
- 1440px;
- 1920px;
- 200% zoom;
- long titles;
- browser text scaling;
- keyboard-only;
- reduced motion.

## 17. Performance

Candidate budgets:
- no mandatory WebGL;
- no large background video;
- hero graph should be CSS/SVG/DOM first;
- first frame communicates product without waiting for JS;
- compositor-friendly transforms/opacity where possible;
- no layout shift caused by graph initialization.

## 18. Component primitives

Candidate v2 set:
- VerluneGraph
- GraphNode
- GraphEdge
- GraphDecision
- GraphVerification
- EditorialHero
- CapabilitySplit
- PromptWorkflowCompare
- CategoryRail
- ArtifactRow
- ArtifactFeature
- ArtifactMiniMap
- BuilderFeature
- ProcessRail
- EvidenceDisclosure
- TrustBoundary
- AssetHeader
- AssetStructureMap
- AssetBody
- CopyAction
- UseGuide

Every component must define relevant default, hover, focus, active, disabled, loading, error and reduced-motion behavior.

## 19. Required mockups before implementation

1. Homepage desktop — 1440×1000.
2. Premium Library desktop — 1440×1000.
3. Asset Detail desktop — 1440×1000.
4. Homepage mobile — 390×844.

Mockups are visual hypotheses, not implementation authorization.

## 20. Mockup validation

Ask:
- Can a stranger explain Verlune from the first screen?
- Does the graph explain the product rather than decorate it?
- Is Prompt vs Workflow visually obvious?
- Are Builders visibly differentiated?
- Is Free/Premium value understandable without counting assets?
- Does motion have semantic purpose?
- Does the first frame work without motion?
- Does the design remain calm despite added depth?
- Does it feel credible outside developer use cases?

## 21. Non-goals

Do not add merely for novelty:
- 3D objects;
- fake AI terminals;
- invented activity streams;
- fake customer metrics;
- fake usage graphs;
- generic glowing orb;
- decorative code rain;
- endless marquees;
- irrelevant avatars/people;
- dashboards unrelated to the customer's workflow.

## 22. Gate

Current state:
- Visual Contract v2: CANDIDATE.
- Mockups: AUTHORIZED.
- Frontend redesign: FROZEN.
- Human Review H1-H11: required before implementation.

After Human Review, revise this contract with reviewer-derived evidence before converting candidate tokens/layouts into production components.
