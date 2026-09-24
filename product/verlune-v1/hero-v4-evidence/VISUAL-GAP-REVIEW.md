# Verlune Hero V4 — cinematic material pass

HUMAN_VISUAL_ACCEPTANCE=OPEN

## Scope and evidence

The supplied approved homepage image is preserved as [art-direction-master.png](art-direction-master.png). Before is the committed V3 at eebff61; after is the V4 local build. These are browser viewport screenshots, not a claim of visual parity.

| Viewport | Before V3 | After V4 | Runtime |
| --- | --- | --- | --- |
| 1920×1080 | [before/1920.png](before/1920.png) | [after/1920.png](after/1920.png) | WebGL2 |
| 1440×1000 | [before/1440.png](before/1440.png) | [after/1440.png](after/1440.png) | WebGL2 |
| 1024×768 | [before/1024.png](before/1024.png) | [after/1024.png](after/1024.png) | WebGL2 |
| 390×844 | [before/390.png](before/390.png) | [after/390.png](after/390.png) | Static fallback |

The V3 1024 screenshot was generated from a detached worktree at eebff61 with the same software WebGL browser. The V3 canvas was present and painted, although the runtime's ready class had not yet appeared when the screenshot was taken. This is a capture-state limitation for that one comparison.

## Visual gap against the supplied master

| Criterion | V4 observation | Remaining gap |
| --- | --- | --- |
| Glass quality | Three thinner bevelled layers, selective physical transmission and clearcoat; top carries a subtle studio reflection texture. | The top reads as tinted solid glass rather than optically deep smoked glass; background refraction remains weak. |
| Specular response | Small point highlights, pale top rim and varied secondary rims are visible. | Few broad softbox reflections; bright edge hits are still too regular. No environment map is used. |
| Perceived depth | Larger vertical separation and fading lower layers give the stack more volume. | Underneath/floor reflection is subtle, and layers still read as flat planes in places. |
| Central hierarchy | The camera is closer and lower; the three-slab object fills more of the right half. | At 1024 the left edge crops heavily; at 1920 the object remains less dominant than in the master. |
| Atmospheric density | Translucent panels, distant traces, sparse particles, orbit nodes and a floor grid extend the scene. | Much of the environment stays low contrast and the horizon remains empty compared with the master. |
| Card integration | Four accessible DOM cards have glass styling, perspective, local highlights and short connectors. | They still read as UI overlays more than spatial objects; the connectors are intentionally subdued. |
| Lighting contrast | Mint key, neutral rim, low fill and localized underside light produce distinct highlights. | The scene lacks some broad white specular sweeps and reflected light seen in the master. |
| Photographic/cinematic quality | Closer framing and controlled contrast improve the previous diagram-like stack. | Still visibly computer-rendered, particularly in the uniform top plane and faint environment. |
| Resemblance to master | Preserves the dark mint palette, layer motif, four semantic cards and left-copy/right-scene layout. | Not visually equivalent to the approved master. Human art-direction review is required. |

Postprocessing was deliberately omitted: with these materials and software WebGL, bloom would enlarge the few hot pixels without repairing the missing environment reflections. The pass uses ACES tone mapping and restrained exposure instead.

## Verification boundary

- `npm run typecheck` and `npm run build` passed, including golden path, Premium, V2 and Hero V3 source audits.
- Browser captures at 1920, 1440 and 1024 contained a ready WebGL2 canvas; 390 used the static fallback. No page errors or Next error overlays were observed in these captures. [after/browser.json](after/browser.json) records the browser states.
- Reduced motion, forced WebGL2 unavailability and mobile each kept four DOM cards, semantic text and static fallback, with no page errors.
- Canvas remains dynamically imported, desktop gated, demand rendered with a finite entrance, and DPR capped at 1.6 (1.25 for medium width).
- Product copy, routes, pricing, claims, catalog and entitlement were not edited. No illustrative counts, ratings or popularity claims were introduced.

HUMAN_VISUAL_ACCEPTANCE=OPEN
