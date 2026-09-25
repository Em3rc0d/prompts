import type { Metadata } from "next";
import Link from "next/link";
import { cookies } from "next/headers";

import { LemonCheckoutLink } from "@/components/lemon-checkout-link";
import { currentCommerceMode } from "@/lib/commerce-mode";
import { getVerluneAccessConfigState } from "@/lib/verlune-access";
import {
  premiumTestSessionMatches,
  premiumTestSessionValue,
  VERLUNE_PREMIUM_TEST_SESSION_COOKIE,
} from "@/lib/verlune-premium-test-session";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Premium checkout test",
  robots: { index: false, follow: false },
};

export default async function PremiumCheckoutTestPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; authorized?: string }>;
}) {
  const params = await searchParams;
  const cookieStore = await cookies();
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const access = getVerluneAccessConfigState();
  const checkoutConfigured = Boolean(process.env.LEMONSQUEEZY_VERLUNE_PREMIUM_TEST_CHECKOUT_URL?.trim());
  const tokenConfigured = Boolean(process.env.VERLUNE_PREMIUM_PROVIDER_TEST_TOKEN?.trim());
  const sessionSigningConfigured = Boolean(premiumTestSessionValue());
  const authorized = premiumTestSessionMatches(cookieStore.get(VERLUNE_PREMIUM_TEST_SESSION_COOKIE)?.value);
  const ready = mode === "test"
    && !publicSaleLive
    && access.ready
    && checkoutConfigured
    && tokenConfigured
    && sessionSigningConfigured;

  return <main className="accessPage">
    <section className="pageHero">
      <div className="wrap accessGrid">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM / PROVIDER TEST</div>
          <h1>Test the real checkout flow without real money.</h1>
          <p className="lead">This private test surface uses the configured Lemon Squeezy Test checkout. Public Premium selling remains closed while this test gate is active.</p>
          <div className="accessTrust">
            <p><strong>Commerce mode:</strong> {mode}</p>
            <p><strong>Public sale:</strong> {publicSaleLive ? "LIVE — invalid for provider test" : "NOT_FOR_SALE"}</p>
            <p><strong>Premium access config:</strong> {access.ready ? "ready" : `missing: ${access.missing.join(", ")}`}</p>
            <p><strong>Test checkout URL:</strong> {checkoutConfigured ? "configured" : "missing"}</p>
            <p><strong>Provider test token:</strong> {tokenConfigured ? "configured" : "missing"}</p>
          </div>
          <div className="accessActions">
            <Link className="textLink" href="/premium">← Premium</Link>
            <Link className="textLink" href="/unlock">Unlock</Link>
          </div>
        </div>

        <div className="accessPanel">
          <div className="eyebrow">AUTHORIZED TEST SESSION</div>
          <h2>{authorized ? "Ready to open Lemon Squeezy Test checkout" : "Authorize this browser"}</h2>
          {params.error === "unauthorized" ? <p className="notice">The provider test token did not match.</p> : null}
          {params.error === "not-ready" ? <p className="notice">Provider test mode is not fully configured on this deployment.</p> : null}

          {!ready
            ? <div className="notice">
                <strong>Provider test is fail-closed.</strong>
                <p>Set VERLUNE_PREMIUM_COMMERCE_MODE=test, keep VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=NOT_FOR_SALE, and configure the Test checkout, Premium access credentials, session secrets, and provider test token.</p>
              </div>
            : authorized
              ? <div>
                  <p>This browser has a short-lived, HttpOnly test authorization. Opening checkout does not expose the provider test token to client JavaScript.</p>
                  <div className="accessActions">
                    <LemonCheckoutLink href="/api/commerce/verlune-premium/checkout">Open Premium TEST checkout →</LemonCheckoutLink>
                  </div>
                  <p className="micro">Use Lemon Squeezy test payment details only. Do not enter a real card in Test Mode.</p>
                </div>
              : <form action="/api/commerce/verlune-premium/test-session" method="post">
                  <label htmlFor="provider-test-token">Provider test token</label>
                  <input id="provider-test-token" name="token" type="password" autoComplete="off" required />
                  <div className="accessActions">
                    <button className="btn btnPrimary" type="submit">Authorize TEST checkout →</button>
                  </div>
                  <p className="micro">The token is submitted server-side over HTTPS and replaced by a 15-minute HttpOnly session cookie.</p>
                </form>}
        </div>
      </div>
    </section>
  </main>;
}
