# Verlune UI Contract v2

Status: `CONTRACT CANDIDATE / MOCKUP-BOUND / IMPLEMENTATION FROZEN UNTIL HUMAN REVIEW`

Date: 2026-09-23

Related:
- `DESIGN_V2.md`
- generated visual mockup: Editorial Computational / dark 3D semantic system

## 0. Contract intent

This document converts the approved mockup direction into an implementation-ready UI contract.

It does **not** authorize implementation yet.

It defines:
- screen architecture;
- component hierarchy;
- 3D/depth semantics;
- motion semantics;
- state behavior;
- data/copy boundaries;
- responsive transformations;
- accessibility constraints;
- performance constraints;
- mockup-to-product traceability.

The mockup is a **visual hypothesis**, not a factual source. Any invented copy, metrics, ratings, usage counts, support promises, or entitlement claims visible in the mockup are explicitly non-binding unless already supported by product evidence.

---

## 1. Provenance rules

Use:
- `OFFICIAL` — already approved product/brand fact.
- `OBSERVED` — directly present in current product/evidence.
- `GENERATED` — new UI direction from the mockup.
- `INFERRED` — derived from product architecture.
- `REJECTED_FROM_MOCKUP` — visually shown but not allowed as product truth.

### Mockup-derived visual decisions accepted

- dark editorial shell;
- strong typographic hierarchy;
- semantic 3D object system;
- mint functional accent;
- sparse but high-value cards;
- left navigation/filter rail in Premium;
- featured workflow/Builder surfaces;
- visual structure map on asset detail;
- compact process rail;
- restrained borders and layered depth.

### Mockup details explicitly rejected as factual product copy

The following mockup elements are **not approved product facts**:
- fake use counts such as “8.1k uses”;
- fake star ratings such as “4.8”;
- “Lifetime access” unless commerce policy later explicitly approves that claim;
- “Future updates” as an entitlement promise;
- “Priority support”;
- “community support”;
- fake popularity badges such as “Most popular”;
- invented asset names that do not map to the governed catalog;
- invented category counts;
- any fake analytics or usage telemetry.

The UI may reserve layout space for future real evidence, but must not render fabricated values.

---

## 2. UI design thesis

### OFFICIAL

Verlune is a library and toolkit for structured AI work.

### GENERATED UI thesis

The UI should visually demonstrate transformation:

```text
MESSY / UNSTRUCTURED NEED
        ↓
STRUCTURE
        ↓
PROMPT or WORKFLOW
        ↓
AI EXECUTION
        ↓
VERIFY
        ↓
REUSE
```

The product should feel:
- editorial in reading;
- computational in structure;
- tactile in interaction;
- premium in composition;
- trustworthy in evidence boundaries.

The primary differentiator is not “AI aesthetics”.
It is **visible structure**.

---

## 3. Global shell contract

### 3.1 Header

Desktop:
- height: 72–84px;
- left: Verlune mark + wordmark;
- center/right: Library, Builders, Learn;
- one commerce/access action at far right;
- no more than one dominant CTA.

Premium authenticated state:
- replace purchase CTA with `Access settings` / library state where appropriate.

Mobile:
- wordmark retained;
- compact menu;
- no multi-row desktop navigation;
- no critical action hidden behind hover.

### 3.2 Page canvas

- dark neutral background;
- max visual width: 1440px;
- content width: 1240–1280px;
- prose width: 620–720px;
- main sections separated by whitespace and/or a single line, not container-on-container stacking.

### 3.3 Depth layers

Depth has four semantic levels:

```text
Z0  page field
Z1  reading / navigation surface
Z2  interactive artifact / graph plane
Z3  focused semantic object
```

Depth is communicated with:
- offset;
- scale;
- border contrast;
- subtle directional light;
- restrained shadow;
- perspective only where semantic.

No blurred glass panels by default.

---

## 4. 3D semantic system

### 4.1 Principle

3D is allowed **only** when it explains structure, transformation, hierarchy, or state.

### 4.2 Allowed 3D object classes

#### StructureBlock
Represents:
- Prompt;
- Workflow;
- Builder-generated artifact;
- verification result;
- input bundle.

Visual form:
- extruded rectangular plane;
- 4–10px perceived depth;
- 4–8px radius;
- fine border;
- low-gloss surface;
- no plastic/toy appearance.

#### GraphPlane
Represents:
- process context;
- relation surface;
- coordinate field behind connected objects.

#### Connector
Represents:
- valid flow;
- dependency;
- transfer;
- fallback.

Must be attached to actual semantic nodes.

#### VerificationSeal
Represents:
- an actual verification step/state;
- never a decorative “quality” badge.

### 4.3 Hero 3D stack

Required hero scene:

```text
[ Messy request ]
       ↓
[ Structured Prompt ]
       ↓
[ Workflow map ]
       ↓
[ Verify ]
```

Optional side object:
- evidence/context block feeding into structure.

The scene should feel like a **physicalized graph**, not a floating card carousel.

### 4.4 Perspective

Desktop:
- mild perspective;
- no aggressive fisheye;
- object rotation <= ~8° on primary surfaces;
- z separation subtle enough that labels remain readable.

Mobile:
- reduce perspective;
- stack vertically;
- no interaction dependent on 3D rotation.

### 4.5 3D motion

Allowed:
- assemble;
- align;
- lift/focus;
- connect;
- verify.

Forbidden:
- continuous idle spinning;
- floating forever;
- physics bounce;
- camera fly-through;
- user-controlled orbit;
- decorative particles.

---

## 5. Homepage contract

Route: `/`

### 5.1 Hero

Layout:
- 5/12 columns text;
- 7/12 columns semantic 3D graph.

Left contract:
- eyebrow: structured AI work;
- headline: outcome/positioning;
- one supporting paragraph;
- primary CTA: Free;
- secondary CTA: Premium;
- optional evidence strip only if values are real.

Right contract:
- 3D semantic Verlune Graph;
- no fake metrics;
- labels must map to real product concepts.

First frame must explain Verlune without motion.

### 5.2 Use ours / Build yours

Two equal strategic pathways.

#### Use ours
Visual:
```text
LIBRARY → COPY → RUN → VERIFY → REUSE
```

#### Build yours
Visual:
```text
NEED → BUILDER → ARTIFACT → TEST → REUSE
```

Each path:
- one short description;
- one CTA;
- one semantic icon/mini-graph;
- no more than 2 nested levels.

### 5.3 Prompt vs Workflow

Required comparison:

Prompt:
```text
INPUT → INSTRUCTION → OUTPUT → CHECK
```

Workflow:
```text
TRIGGER → STAGE → DECISION
                 ↘ FALLBACK
        → VERIFY → OUTPUT
```

Contract:
- visible difference without hover;
- motion may animate the workflow branch after the static structure is understood.

### 5.4 How it works

Five states:
1. Find
2. Copy
3. Run
4. Verify
5. Reuse

Desktop:
- linear rail;
- selected state can animate a graph highlight.

Mobile:
- vertical stack.

### 5.5 Library preview

Structure:
- category selector;
- one featured asset;
- 2–4 compact supporting assets;
- CTA to full library.

Do not render all assets on the marketing home.

### 5.6 Premium capability section

Communicate:
- deeper workflows;
- Builders;
- adaptation;
- evaluation;
- protected library access.

Do not communicate value primarily as “more prompts”.

### 5.7 Purchase section

Allowed:
- `USD 9 one-time` only while that launch hypothesis remains the candidate commerce contract.
- product capability summary.
- test/purchase CTA when authorized.

Disallowed unless independently approved:
- lifetime;
- future updates;
- priority support;
- popularity badge;
- guaranteed savings/results.

---

## 6. Premium Library contract

Route: `/app`

### 6.1 Top section

Headline:
`Use ours. Build yours.`

Supporting copy:
- choose structured asset;
- copy into compatible AI assistant;
- or use Builder to create reusable work.

Secondary action:
- Access settings.

### 6.2 Process rail

Compact horizontal rail:
`Find → Copy → Run → Verify → Reuse`

Behavior:
- static first frame;
- optional focus animation on hover/focus;
- no autoplay dependency.

### 6.3 Navigation model

Desktop:
- left rail: categories;
- top row or secondary rail: type filters.

Category examples:
- Builders
- Development & Tech
- Study & Learning
- Research & Analysis
- Business & Operations
- Writing & Communication
- Content & Marketing
- Planning & Productivity
- Career & Job Search
- Adapt & Evaluate

Type filters:
- All
- Prompts
- Workflows
- Builders
- Toolkit

Mobile:
- category selector becomes horizontal scroll or disclosure;
- type filter becomes segmented control / select;
- no permanent 2-column rail.

### 6.4 Content ordering

Default hierarchy:
1. Builders
2. Featured/selected Workflows
3. Prompts
4. Toolkit

This hierarchy may change after Human Review evidence.

### 6.5 Artifact presentation rules

#### BuilderFeature
Large, high-priority surface.
Must show:
- name;
- outcome;
- mini-graph;
- “start from your own recurring work” meaning.

#### WorkflowFeature
Must show:
- name;
- one-sentence purpose;
- mini process structure;
- type/category;
- open action.

#### PromptRow / PromptCard
More compact.
Must show:
- name;
- bounded task;
- type/category;
- open action.

#### Toolkit
Utility treatment; less visual dominance.

### 6.6 No fake social proof

The library must not show:
- fake usage count;
- fake rating;
- fake trending state;
- fake popularity.

If real product analytics later exist, they require a separate evidence/privacy decision.

---

## 7. Asset Detail contract

Route: `/app/asset/[assetId]`

### 7.1 Header

Required:
- Back to library;
- type;
- category;
- exact governed asset name;
- summary;
- Copy full asset;
- asset ID as secondary metadata.

### 7.2 Structure map

A visual map above the full body.

By type:

Prompt:
`Input → Rules → Output → Verify`

Workflow:
`Trigger → Stages → Decision/Fallback → Verify → Output`

Builder:
`Need → Guided intake → Reusable artifact → Quick test`

Toolkit:
`Input → Method → Check → Adapt`

The map is illustrative of the exact asset semantics; do not invent stages that are not actually present.

### 7.3 Tabs / progressive disclosure

Candidate:
- Overview
- Structure
- Full asset
- Evidence / limits

Do **not** include Changelog unless a real customer-facing release history exists.

### 7.4 Full asset surface

- monospace;
- readable contrast;
- max comfortable line length;
- sticky copy action on desktop;
- no raw internal release status in visible preview;
- exact governed content remains copyable according to release policy.

### 7.5 Copy interaction

States:
- idle;
- hover;
- focus;
- copying;
- copied;
- error.

Copied state:
- visual confirmation within one frame;
- accessible live announcement;
- reset after 1.5–2.5s or on navigation.

---

## 8. Unlock / Access contract

Routes:
- `/unlock`
- `/app/access`

Visual direction:
- quieter than marketing;
- high trust;
- minimal 3D.

Allowed visual:
- one small semantic entitlement object / lock state diagram.

Disallowed:
- celebratory glow for successful access;
- complex graph distracting from license/email form.

Required states:
- locked;
- invalid entitlement;
- wrong email;
- activation limit reached;
- provider unavailable;
- session invalid;
- deactivated;
- active session;
- revalidation pending.

Every error:
- human readable;
- states what happened;
- states next safe action where possible;
- never exposes provider secrets/raw responses.

---

## 9. Pricing / purchase contract

The mockup's pricing composition is accepted **as a layout pattern**, not as approved copy.

Layout:
- Free panel;
- Premium panel;
- one clear comparison;
- Premium visually emphasized through border/depth, not fake popularity.

Allowed Premium claims:
- protected Premium library;
- Premium Prompts/Workflows;
- Prompt Builder;
- Workflow Builder;
- Adaptation Guide;
- Evaluation Toolkit;
- one-time candidate price USD 9, while frozen by commerce contract.

Disallowed until proven/approved:
- lifetime updates;
- priority support;
- community support;
- “most popular”;
- usage savings;
- ROI;
- guaranteed compatibility.

---

## 10. Motion contract

### Timing

- micro feedback: 100–140ms;
- standard UI: 160–200ms;
- graph transition: 240–320ms;
- hero assembly scene: 360–520ms max.

### Semantic mappings

`ENTER`
Opacity + small y movement.

`ASSEMBLE`
Nodes move into a valid structure; connectors draw after placement.

`TRANSFER`
A structured block moves directionally from library state toward execution representation.

`VERIFY`
Connector/state resolves to mint check state.

`FOCUS`
Focused object lifts 2–6px perceived z-depth; neighbors reduce contrast slightly.

`EXPAND`
Progressive disclosure opens using height/opacity with no large bounce.

### Motion accessibility

Reduced motion:
- no perspective shifts;
- no graph assembly movement;
- state changes use opacity/border only;
- information remains identical.

---

## 11. Component contracts

### Global
- SiteHeader
- SiteFooter
- EditorialSection
- Eyebrow
- PrimaryButton
- SecondaryButton
- TextLink

### Graph / 3D
- VerluneGraphScene
- GraphPlane
- StructureBlock
- GraphConnector
- GraphDecision
- GraphFallback
- VerificationSeal

### Marketing
- HeroV2
- CapabilitySplit
- PromptWorkflowCompare
- ProcessRail
- LibraryPreview
- PremiumCapability
- PurchaseComparison
- TrustBoundary

### Premium
- PremiumShell
- CategoryRail
- TypeFilter
- BuilderFeature
- WorkflowFeature
- PromptRow
- ToolkitRow
- AssetMiniMap

### Asset
- AssetHeader
- AssetTabs
- AssetStructureMap
- AssetBody
- StickyCopyAction
- AssetEvidenceDisclosure

Each component must specify:
- semantic purpose;
- content inputs;
- default;
- hover;
- focus;
- active;
- disabled;
- error;
- loading;
- reduced motion;
- mobile recomposition.

---

## 12. State contract

No component ships without explicit states.

### Buttons
- idle
- hover
- focus-visible
- pressed
- disabled
- loading
- success
- error where relevant

### Cards/features
- idle
- hover
- focus
- selected
- unavailable/locked if applicable

### Graph
- idle
- assembling
- connected
- focused
- verified
- fallback
- unknown
- stopped

### Access
- locked
- checking
- active
- invalid
- provider unavailable
- activation limit
- revoked
- deactivated

---

## 13. Responsive contract

### 1440 / 1920

- full 3D hero;
- split editorial compositions;
- visible category rail;
- sticky asset utility surfaces.

### 768

- simplify perspective;
- collapse category rail;
- reduce simultaneous graph nodes;
- preserve hierarchy;
- no more than 2 main columns.

### 390

- graph becomes vertical semantic stack;
- no 3D perspective needed;
- CTA full-width when useful;
- process rail vertical;
- asset actions remain above long content;
- filters scroll horizontally or use disclosure.

No mobile layout may be a scaled screenshot of desktop.

---

## 14. Accessibility contract

- WCAG AA minimum contrast;
- keyboard navigation for all controls;
- visible focus;
- 44px minimum critical targets;
- semantic heading order;
- diagrams get textual equivalent;
- 3D does not carry unique information;
- no hover-only details;
- copy success announced to assistive tech;
- reduced motion respected;
- color never sole state encoding.

---

## 15. Performance contract

3D implementation priority:

1. CSS 3D transforms + DOM
2. SVG + CSS
3. Canvas/WebGL only if a real implementation limitation is proven

The initial mockup does **not** justify WebGL by itself.

Budgets:
- no hero video;
- no large texture packs;
- no mandatory runtime 3D engine;
- first content paint must not wait for graph JS;
- no layout shift when graph hydrates;
- idle scene consumes negligible CPU after entry animation ends.

---

## 16. Visual regression contract

Required snapshots:
- 390×844
- 768×1024
- 1440×1000
- 1920×1080

Required routes:
- home;
- Premium Library;
- one Prompt;
- one Workflow;
- one Builder;
- unlock;
- access settings.

Required modes:
- default;
- keyboard focus;
- reduced motion;
- long text;
- error state.

---

## 17. Mockup traceability

### Panel 1 — Home
ADOPT:
- strong hero;
- semantic 3D stack;
- dual CTA;
- Use ours / Build yours.

REJECT:
- fake curated counts unless exact and useful;
- any invented “real workflows” metric.

### Panel 2 — Library
ADOPT:
- left category rail;
- featured large workflow;
- differentiated asset surfaces;
- search/filter affordance.

CONDITIONAL:
- search ships only if catalog size/usability justifies it.

REJECT:
- fake ratings;
- fake usage counts;
- fabricated category totals.

### Panel 3 — Asset Detail
ADOPT:
- visual workflow map;
- strong Copy action;
- structured content surface.

REJECT:
- invented title not matching governed catalog;
- Changelog unless real customer-visible history exists;
- fake ratings/use counts.

### Panel 4 — How it works
ADOPT:
- Find → Copy → Run → Verify → Reuse;
- semantic progressive rail.

### Panel 5 — Pricing
ADOPT:
- simple Free vs Premium comparison layout;
- Premium emphasis.

REJECT:
- lifetime access claim;
- future updates claim;
- priority/community support;
- “Most popular”.

### Panel 6 — visual flow
ADOPT:
- consistency across hero, process, library, asset and purchase surfaces.

### Design-system row
ADOPT:
- tokenized colors;
- typography roles;
- button variants;
- state matrix;
- artifact component pattern.

---

## 18. Implementation gate

Current state:

```text
DESIGN_V2.md              CANDIDATE
UI_CONTRACT_V2.md         MOCKUP-BOUND CANDIDATE
MOCKUP DIRECTION          APPROVED FOR EXPLORATION
FRONTEND IMPLEMENTATION   FROZEN
HUMAN REVIEW H1-H11       OPEN
```

Implementation begins only after the Human Review disposition authorizes redesign.

At that point:
1. update contract from reviewer evidence;
2. freeze tokens;
3. freeze component API;
4. build Home first;
5. build Premium Library;
6. build Asset Detail;
7. validate responsive/a11y/motion/performance;
8. run visual regression;
9. human visual acceptance.
