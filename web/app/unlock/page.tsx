import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { VerluneUnlockForm } from "@/components/verlune-unlock-form";
import { getVerluneAccessConfigState } from "@/lib/verlune-access";
import { readPremiumSession, safePremiumNextPath } from "@/lib/verlune-auth.server";

export const metadata: Metadata = {
  title: "Unlock Premium",
  robots: { index: false, follow: false }
};

const reasonCopy: Record<string, string> = {
  locked: "Premium is locked in this browser.",
  "session-invalid": "This Premium session is no longer valid. Enter your purchase details again.",
  "revalidation-unavailable": "We could not re-check the license provider right now. Premium remains locked until validation succeeds.",
  "logged-out": "You are signed out of Premium on this browser.",
  deactivated: "This browser was deactivated from your Premium license."
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
  const config = getVerluneAccessConfigState();
  const reason = params.reason ? reasonCopy[params.reason] : undefined;

  return <main className="accessPage">
    <section className="pageHero">
      <div className="wrap accessGrid">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM / PRIVATE ACCESS</div>
          <h1>Unlock the library you purchased.</h1>
          <p className="lead">Use the checkout email and license key from your Lemon Squeezy receipt. Verlune validates the entitlement on the server and creates a private browser session.</p>
          <div className="accessTrust">
            <p><strong>No account password.</strong> Your purchase remains the entitlement.</p>
            <p><strong>No hosted AI credits.</strong> Prompts, workflows and Builders run in your compatible AI assistant.</p>
            <p><strong>Fail closed.</strong> Invalid, expired, disabled or mismatched licenses do not unlock Premium.</p>
            <p><strong>Three active browsers.</strong> A signed device reference lets the same browser reuse its existing activation after a session expires.</p>
          </div>
          <Link className="textLink" href="/">← Back to Verlune</Link>
        </div>
        <div className="accessPanel">
          <div className="eyebrow">PURCHASE ACCESS</div>
          <h2>License + checkout email</h2>
          {reason ? <p className="notice">{reason}</p> : null}
          {existing && revalidationBlocked
            ? <div>
                <p>Your signed browser session still exists, but Premium is locked until the entitlement provider can be checked again.</p>
                <div className="accessActions">
                  <Link className="btn btnPrimary" href={`/api/verlune/session/revalidate?next=${encodeURIComponent(nextPath)}`}>Retry license check</Link>
                  <form action="/api/verlune/logout" method="post"><button className="btn btnSecondary" type="submit">Log out</button></form>
                </div>
              </div>
            : config.ready
              ? <VerluneUnlockForm nextPath={nextPath} />
              : <div className="notice"><strong>Candidate access is not connected on this deployment yet.</strong><p>The customer surface is implemented, but provider credentials and the final Premium product identity must be configured before unlock can run.</p></div>}
        </div>
      </div>
    </section>
  </main>;
}
