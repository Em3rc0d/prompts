# Verlune Hero V3 — preimplementation gap analysis

Date: 2026-09-24. Branch: `feat/verlune-product-model-v1-20260922-r2`.

Evidence: supplied approved homepage hero image (`10_57_23`) and other supplied visual mockups (`10_58_*`); current `web/app/page.tsx`, `web/components/verlune-visuals.tsx`, `web/app/globals.css`; Hero V3 spec and V2 contracts. The mockups' asset counts, ratings and other product claims are not product evidence. Current rendered browser screenshots are tracked separately from this source-level diagnosis.

| Dimension | V2 implementation gap | V3 technical response |
| --- | --- | --- |
| Composition | A bordered 520px graph box separates the illustration from the editorial page field. | Integrate a larger scene into the hero's right column, keep headline and CTAs in the left column. |
| Central object scale | The stack starts at 210px and its visible slabs are inset another 28px; cards compete for attention. | Make a dominant 3D core with visible body and deliberate card offsets. |
| Depth | CSS `translateZ` repositions surfaces without casting physical light or making side faces. | Real slab geometry with separated layers and perspective camera. |
| Geometry | Three rounded rectangles have zero modeled thickness or bevel profile. | Extruded rounded slabs, physical edge bevels and a raised seal. |
| Material | Layer gradients simulate opacity; no angle-dependent specular or glass edge response. | Transparent dark physical surfaces plus distinct rim/edge geometry. |
| Lighting | Mint glow is baked into shadows and radial gradients. | Mint key/rim, neutral specular fill and restrained low-level ambient. |
| Edge/specular | Uniform borders never change with face orientation. | Beveled lit faces and fine emissive rim lines, with bloom deferred. |
| Atmosphere | Two gradients and one grid sit effectively on the same panel. | Receding field, sparse planes and low-contrast distance cues. |
| Perspective field | CSS grid transform is local to the flat box. | 3D floor grid beneath the stack with camera-space convergence. |
| Orbit system | Two screen-centered CSS ellipses do not sit in object space. | Two or three thin 3D relation paths with sparse nodes aligned to card regions. |
| Floating semantic cards | Four readable cards have minor CSS rotation but little directional separation. | Keep real DOM text; give cards distinct positions, internal highlights and directional shadows. |
| Background layering | The background is essentially one gradient surface. | Sparse depth planes behind the core, subordinate to reading. |
| Visual hierarchy | Similar rectangular weights weaken the core silhouette. | Headline first; modeled central object second; CTAs third; cards and atmosphere follow. |
| Text legibility | Current DOM labels are readable; mockup glass would threaten legibility if copied literally. | Preserve actual headline/copy; use opaque-enough DOM cards and no WebGL text. |
| Responsive | V2 scales the same cluster to 150px and squeezes 132px cards into a 390px panel. | Compose a static vertical scene and card grid below 900px; desktop WebGL need not load. |

The approved hero image is visual direction, not an asset to embed. The V3 result requires an actual physical object before orbit lines or card styling can be judged. Baseline `npm run typecheck` and `npm run build` passed at branch head `60a82df612530fa9da4aca3ea8cfc09d2b5ebb28`; postbuild golden path, Premium and V2 audits passed. Browser capture is pending a working Chromium binary in this environment.
