# Prompt Quarry Web v0

Status: `C1 IMPLEMENTED / CI PENDING`

Zero-dependency static commercial surface for the `PQ-$1` funnel.

## Routes

- `/` — commercial landing
- `/free/developer-starter-pack/` — Free Pack acquisition page
- `/developer-pack/` — paid Developer Pack v1 page
- `/license/` — commercial license summary

## Configuration

External distribution URLs are intentionally not hard-coded into page copy. Configure them in `config.js`:

```js
window.PQ_CONFIG = {
  freePackUrl: "",
  developerPackCheckoutUrl: "",
  analyticsMode: "off"
};
```

Until C2/C3 provide real URLs, Free CTAs route to the Free Pack page and paid checkout CTAs fail closed with a visible `Checkout configuration pending` state.

## Local preview

From repository root:

```bash
python -m http.server 8080 -d web
```

Then open `http://localhost:8080`.

## Static acceptance

```bash
python tools/test_commercial_web_v0.py
```

The test guards required routes, responsive breakpoints, provider abstraction, and evidence-safe marketing boundaries.

## Boundaries

This surface may state that Developer Pack v1 is commercially `READY` and included assets are statically `VALID`. It must not claim F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE` without corresponding evidence.
