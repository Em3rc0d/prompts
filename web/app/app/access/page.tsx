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

export default async function PremiumAccessPage() {
  const session = await requirePremiumSession("/app/access");

  return <main className="premiumApp">
    <section className="pageHero">
      <div className="wrap narrowPage">
        <Link className="textLink" href="/app">← Premium Library</Link>
        <div className="eyebrow">PREMIUM ACCESS</div>
        <h1>This browser is unlocked.</h1>
        <p className="lead">The browser session contains a signed entitlement reference, not your raw license key. Verlune periodically re-checks the provider before continuing to serve Premium content.</p>

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
        <p className="micro">Logging out removes only the local browser session. Deactivating also releases this browser's Lemon Squeezy license instance when provider access is available.</p>
      </div>
    </section>
  </main>;
}
