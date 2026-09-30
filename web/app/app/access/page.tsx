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
        <p className="lead">The browser holds a signed entitlement reference, not payment credentials. Verlune periodically re-checks Mercado Pago before continuing to serve Premium content.</p>
        <dl className="sessionFacts">
          <div><dt>Last entitlement check</dt><dd>{formatEpoch(session.validatedAt)}</dd></div>
          <div><dt>Session expires</dt><dd>{formatEpoch(session.expiresAt)}</dd></div>
          <div><dt>Access reference</dt><dd><code>{session.v === 3 ? session.entitlementId : session.v === 2 ? `MP ${session.paymentId}` : session.instanceId}</code></dd></div>
        </dl>
        <div className="accessActions">
          <form action="/api/verlune/logout" method="post"><button className="btn btnSecondary" type="submit">Log out this browser</button></form>
          <form action="/api/verlune/deactivate" method="post"><button className="btn btnSecondary" type="submit">Forget access on this browser</button></form>
        </div>
        <p className="micro">Recovery sends the same canonical Verlune Access Key back to the checkout email. A refunded, reversed, mismatched or non-approved payment still fails closed on the next provider check.</p>
      </div>
    </section>
  </main>;
}
