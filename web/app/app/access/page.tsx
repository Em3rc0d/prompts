import type { Metadata } from "next";
import Link from "next/link";

import { requirePremiumSession } from "@/lib/verlune-auth.server";

export const metadata: Metadata = {
  title: "Premium Access",
  robots: { index: false, follow: false }
};

export const dynamic = "force-dynamic";

function formatEpoch(value: number) {
  return new Date(value * 1000).toLocaleString("en-US", { dateStyle: "medium", timeStyle: "short", timeZone: "UTC" }) + " UTC";
}

const errorCopy: Record<string, string> = {
  "deactivation-failed": "The provider did not deactivate this browser. Your session is still active so you can retry.",
  "deactivation-unavailable": "The provider could not be reached. Your session and device activation were kept so you can retry."
};

export default async function PremiumAccessPage({
  searchParams
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  const session = await requirePremiumSession("/app/access");
  const params = await searchParams;
  const error = params.error ? errorCopy[params.error] : undefined;

  return <main className="premiumApp">
    <section className="pageHero">
      <div className="wrap narrowPage">
        <Link className="textLink" href="/app">← Premium Library</Link>
        <div className="eyebrow">PREMIUM ACCESS</div>
        <h1>This browser is unlocked.</h1>
        <p className="lead">The browser session contains a signed entitlement reference, not your raw license key. Verlune periodically re-checks the provider before continuing to serve Premium content.</p>

        {error ? <p className="notice">{error}</p> : null}

        <dl className="sessionFacts">
          <div><dt>Last entitlement check</dt><dd>{formatEpoch(session.validatedAt)}</dd></div>
          <div><dt>Session expires</dt><dd>{formatEpoch(session.expiresAt)}</dd></div>
          <div><dt>Provider instance</dt><dd><code>{session.instanceId}</code></dd></div>
        </dl>

        <div className="accessActions">
          <form action="/api/verlune/logout" method="post">
            <button className="btn btnSecondary" type="submit">Log out this browser</button>
          </form>
          <form action="/api/verlune/deactivate" method="post">
            <button className="btn btnSecondary" type="submit">Deactivate this browser</button>
          </form>
        </div>
        <p className="micro">Logging out removes authorization for this browser but keeps a signed, non-authorizing device reference so the same browser can reuse its activation later. Deactivating removes both the local session and the provider activation.</p>
      </div>
    </section>
  </main>;
}
