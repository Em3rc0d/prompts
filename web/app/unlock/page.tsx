import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { VerluneUnlockForm } from "@/components/verlune-unlock-form";
import { getVerluneEntitlementConfigState } from "@/lib/verlune-access";
import { getVerluneMercadoPagoConfigState } from "@/lib/verlune-mercado-pago";
import { readPremiumSession, safePremiumNextPath } from "@/lib/verlune-auth.server";

export const metadata: Metadata = {
  title: "Unlock Premium",
  robots: { index: false, follow: false }
};

const reasonCopy: Record<string, string> = {
  locked: "Premium is locked in this browser.",
  "session-invalid": "This Premium session is no longer valid. Enter your purchase details again.",
  "revalidation-unavailable": "We could not re-check Mercado Pago right now. Premium remains locked until validation succeeds.",
  "logged-out": "You are signed out of Premium on this browser.",
  deactivated: "Premium access was forgotten on this browser."
};

export default async function UnlockPage({
  searchParams
}: {
  searchParams: Promise<{ reason?: string; next?: string }>;
}) {
  const params = await searchParams;
  const existing = await readPremiumSession();
  const revalidationBlocked = params.reason === "revalidation-unavailable";
  if (existing && !revalidationBlocked) redirect("/app");

  const nextPath = safePremiumNextPath(params.next);
  const provider = getVerluneMercadoPagoConfigState();
  const access = getVerluneEntitlementConfigState();
  const accessReady = provider.ready && access.ready;
  const reason = params.reason ? reasonCopy[params.reason] : undefined;

  return <main className="accessPage">
    <section className="pageHero">
      <div className="wrap accessGrid">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM / PRIVATE ACCESS</div>
          <h1>Unlock the library you purchased.</h1>
          <p className="lead">Use the email from checkout and the single Verlune Access Key sent to that address. Verlune verifies the entitlement and re-checks its Mercado Pago payment before creating a private browser session.</p>
          <div className="accessTrust">
            <p><strong>One key per email.</strong> The same canonical Access Key works whenever you need to unlock Premium.</p>
            <p><strong>No hosted AI credits.</strong> Prompts, workflows and Builders run in your compatible AI assistant.</p>
            <p><strong>Fail closed.</strong> Wrong amount, wrong merchant, wrong environment, refunds or non-approved payments do not unlock Premium.</p>
          </div>
          <div className="accessActions"><Link className="textLink" href="/premium">← Explore Premium</Link><Link className="textLink" href="/">Back to Verlune</Link></div>
        </div>
        <div className="accessPanel">
          <div className="eyebrow">PURCHASE ACCESS</div>
          <h2>Email + Verlune Access Key</h2>
          {reason ? <p className="notice">{reason}</p> : null}
          {existing && revalidationBlocked
            ? <div>
                <p>Your signed browser session still exists, but Premium is locked until Mercado Pago can be checked again.</p>
                <div className="accessActions">
                  <Link className="btn btnPrimary" href={`/api/verlune/session/revalidate?next=${encodeURIComponent(nextPath)}`}>Retry payment check</Link>
                  <form action="/api/verlune/logout" method="post"><button className="btn btnSecondary" type="submit">Log out</button></form>
                </div>
              </div>
            : accessReady
              ? <VerluneUnlockForm nextPath={nextPath} />
              : <div className="notice"><strong>Premium access is not connected on this deployment yet.</strong><p>Configure the server-side entitlement store, Access Key secret, Mercado Pago credentials and Verlune session secrets before unlock can run.</p></div>}
        </div>
      </div>
    </section>
  </main>;
}
