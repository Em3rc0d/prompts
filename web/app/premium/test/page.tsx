import type { Metadata } from "next";
import Link from "next/link";
import { cookies } from "next/headers";

import { MercadoPagoCheckout } from "@/components/mercado-pago-checkout";
import { currentCommerceMode } from "@/lib/commerce-mode";
import { getVerluneAccessConfigState } from "@/lib/verlune-access";
import { getVerluneMercadoPagoConfigState } from "@/lib/verlune-mercado-pago";
import {
  premiumTestSessionMatches,
  premiumTestSessionValue,
  VERLUNE_PREMIUM_TEST_SESSION_COOKIE
} from "@/lib/verlune-premium-test-session";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Premium checkout test",
  robots: { index: false, follow: false }
};

export default async function PremiumCheckoutTestPage({
  searchParams
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  const params = await searchParams;
  const cookieStore = await cookies();
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const provider = getVerluneMercadoPagoConfigState();
  const access = getVerluneAccessConfigState();
  const tokenConfigured = Boolean(process.env.VERLUNE_PREMIUM_PROVIDER_TEST_TOKEN?.trim());
  const sessionSigningConfigured = Boolean(premiumTestSessionValue());
  const authorized = premiumTestSessionMatches(cookieStore.get(VERLUNE_PREMIUM_TEST_SESSION_COOKIE)?.value);
  const ready = mode === "test"
    && !publicSaleLive
    && provider.ready
    && provider.environment === "test"
    && access.ready
    && tokenConfigured
    && sessionSigningConfigured;

  return <main className="accessPage">
    <section className="pageHero">
      <div className="wrap accessGrid">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM / MERCADO PAGO TEST</div>
          <h1>Test cards and Yape without real money.</h1>
          <p className="lead">This private surface uses Mercado Pago TEST credentials while the public Premium sale stays closed.</p>
          <div className="accessTrust">
            <p><strong>Commerce mode:</strong> {mode}</p>
            <p><strong>Provider environment:</strong> {provider.environment ?? "missing"}</p>
            <p><strong>Public sale:</strong> {publicSaleLive ? "LIVE — invalid for provider test" : "NOT_FOR_SALE"}</p>
            <p><strong>Mercado Pago config:</strong> {provider.ready ? "ready" : `missing: ${provider.missing.join(", ")}`}</p>
            <p><strong>Access + Resend config:</strong> {access.ready ? "ready" : `missing: ${access.missing.join(", ")}`}</p>
          </div>
          <div className="accessActions"><Link className="textLink" href="/premium">← Premium</Link><Link className="textLink" href="/unlock">Unlock</Link></div>
        </div>
        <div className="accessPanel">
          <div className="eyebrow">AUTHORIZED TEST SESSION</div>
          <h2>{authorized ? "Mercado Pago TEST checkout" : "Authorize this browser"}</h2>
          {params.error === "unauthorized" ? <p className="notice">The provider test token did not match.</p> : null}
          {params.error === "not-ready" ? <p className="notice">Provider test mode is not fully configured on this deployment.</p> : null}
          {!ready
            ? <div className="notice"><strong>Provider test is fail-closed.</strong><p>Set TEST Mercado Pago credentials plus the entitlement store, Access Key secret and Resend configuration; keep VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=NOT_FOR_SALE.</p></div>
            : authorized
              ? <MercadoPagoCheckout publicKey={provider.publicKey} pricePenMinor={provider.pricePenMinor} testMode />
              : <form action="/api/commerce/verlune-premium/test-session" method="post">
                  <label htmlFor="provider-test-token">Provider test token</label>
                  <input id="provider-test-token" name="token" type="password" autoComplete="off" required />
                  <div className="accessActions"><button className="btn btnPrimary" type="submit">Authorize TEST checkout →</button></div>
                  <p className="micro">The token is submitted server-side over HTTPS and replaced by a 15-minute HttpOnly session cookie.</p>
                </form>}
        </div>
      </div>
    </section>
  </main>;
}
