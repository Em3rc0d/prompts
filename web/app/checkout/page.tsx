import type { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";

import { MercadoPagoCheckout } from "@/components/mercado-pago-checkout";
import { readPremiumSession } from "@/lib/verlune-auth.server";
import { getVerluneMercadoPagoConfigState, VERLUNE_PREMIUM_PRICE_USD } from "@/lib/verlune-mercado-pago";
import { getVerlunePremiumCommerceState } from "@/lib/verlune-premium-commerce";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Checkout",
  robots: { index: false, follow: false }
};

export default async function CheckoutPage() {
  if (await readPremiumSession()) redirect("/app");

  const commerce = getVerlunePremiumCommerceState();
  const provider = getVerluneMercadoPagoConfigState();

  return <main className="accessPage">
    <section className="pageHero">
      <div className="wrap accessGrid">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM / CHECKOUT</div>
          <h1>Premium for {VERLUNE_PREMIUM_PRICE_USD} USD.<br />Pay once.</h1>
          <p className="lead">The Peru checkout is charged as S/ {(provider.pricePenMinor / 100).toFixed(2)} through Mercado Pago. Premium unlocks immediately after Mercado Pago returns an approved payment.</p>
          <div className="accessTrust">
            <p><strong>No subscription.</strong> This is a one-time Verlune Premium purchase.</p>
            <p><strong>Cards + Yape.</strong> Payment details are tokenized by Mercado Pago.</p>
            <p><strong>Server-verified access.</strong> Verlune re-reads the Mercado Pago payment before granting Premium.</p>
          </div>
          <div className="accessActions"><Link className="textLink" href="/premium">← Premium</Link><Link className="textLink" href="/library">Browse Library</Link></div>
        </div>

        <div className="accessPanel">
          <div className="eyebrow">PAY WITH MERCADO PAGO</div>
          <h2>S/ {(provider.pricePenMinor / 100).toFixed(2)} · one time</h2>
          {commerce.purchaseAvailable
            ? <MercadoPagoCheckout publicKey={provider.publicKey} pricePenMinor={provider.pricePenMinor} />
            : <div className="notice"><strong>Public checkout is not open on this deployment.</strong><p>Mercado Pago must be configured in LIVE mode and the explicit Verlune public-sale gate must be enabled.</p></div>}
        </div>
      </div>
    </section>
  </main>;
}
