# Prompt Quarry Web v0

Status: `C1 NEXT.JS IMPLEMENTED / BUILD VERIFICATION PENDING`

Next.js App Router commercial surface for the `PQ-$1` funnel.

## Stack

- Next.js 16.3.3 Active LTS
- React 19.2
- TypeScript strict mode
- App Router
- Server Components by default
- CSS native design system
- client component only for commerce CTA telemetry/fail-closed behavior

## Routes

- `/` — commercial landing
- `/free/developer-starter-pack` — Free Pack acquisition page
- `/developer-pack` — paid Developer Pack v1 page
- `/license` — commercial license summary

## Configuration

Copy `.env.example` to `.env.local` when wiring real distribution:

```bash
NEXT_PUBLIC_FREE_PACK_URL=
NEXT_PUBLIC_DEVELOPER_PACK_CHECKOUT_URL=
NEXT_PUBLIC_ANALYTICS_MODE=off
```

Until C2/C3 provide real URLs, the Free CTA stays on the acquisition route and the paid CTA fails closed instead of pretending checkout exists.

## Local development

```bash
cd web
npm install
npm run dev
```

Production acceptance:

```bash
npm run typecheck
npm run build
```

## Deployment

`web/` is intended to deploy as the Prompt Quarry public application on Vercel. No authentication, CMS, customer account system, or custom commerce backend is required before `PQ-$1`.

## Boundaries

The surface may state that Developer Pack v1 is commercially `READY` and included assets are statically `VALID`. It must not claim F4 `TESTED`, F5 `IMPROVED`, F6 `CERTIFIED`, or F7 `PORTABLE` without corresponding evidence.
