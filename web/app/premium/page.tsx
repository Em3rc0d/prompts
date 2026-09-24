import type { Metadata } from "next";
import Link from "next/link";
import { LemonCheckoutLink } from "@/components/lemon-checkout-link";

import { ArtifactMiniObject } from "@/components/verlune-visuals";
import {
  getVerlunePremiumCommerceState,
  VERLUNE_PREMIUM_CANDIDATE_PRICE_USD
} from "@/lib/verlune-premium-commerce";
import { PREMIUM_ASSETS } from "@/lib/verlune-premium-catalog";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Premium",
  description: "Explore Verlune Premium: deeper prompts and workflows, Prompt Builder, Workflow Builder, adaptation guidance, and evaluation tools.",
  alternates: { canonical: "/premium" },
  robots: { index: false, follow: true }
};

export default function PremiumPage() {
  const commerce = getVerlunePremiumCommerceState();
  const prompts = PREMIUM_ASSETS.filter((asset) => asset.type === "Prompt");
  const workflows = PREMIUM_ASSETS.filter((asset) => asset.type === "Workflow");
  const builders = PREMIUM_ASSETS.filter((asset) => asset.type === "Builder");
  const toolkit = PREMIUM_ASSETS.filter((asset) => asset.type === "Toolkit");

  return <main className="vPremiumPublic">
    <section className="pageHero">
      <div className="wrap productHero">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM</div>
          <h1>Go deeper.<br /><em>Build your own.</em></h1>
          <p className="lead">Premium extends the Verlune method with deeper structured assets, reusable Builders, adaptation guidance, and evaluation tools. You still run the work in your own compatible AI assistant.</p>
          <div className="actions">
            <Link className="btn btnSecondary" href="/library">Browse the Library</Link>
            {commerce.purchaseAvailable
              ? <LemonCheckoutLink href="/api/commerce/verlune-premium/checkout">Get Premium — {VERLUNE_PREMIUM_CANDIDATE_PRICE_USD} USD <span aria-hidden="true">→</span></LemonCheckoutLink>
              : <span className="btn btnPrimary vDisabledCta" aria-disabled="true">Purchasing not open yet</span>}
            <Link className="textLink" href="/unlock">Already purchased? Unlock →</Link>
          </div>
          <p className="micro">{commerce.purchaseAvailable
            ? "One-time purchase · License-based private access · AI-provider access and fees are separate."
            : "The Premium customer surface is available for review, but public purchasing remains closed until the remaining release gates are complete."}</p>
        </div>
        <aside className="reviewPromise vPremiumSummary">
          <span className="eyebrow">CURRENT PREMIUM LIBRARY</span>
          <h2>{PREMIUM_ASSETS.length} structured assets.<br />More than longer prompts.</h2>
          <ul className="checkList">
            <li>{prompts.length} Premium Prompts across the eight public categories</li>
            <li>{workflows.length} multi-stage Premium Workflows</li>
            <li>{builders.length} Builders for creating reusable prompts and workflows</li>
            <li>{toolkit.length} toolkit assets for adaptation and evaluation</li>
          </ul>
        </aside>
      </div>
    </section>

    <section className="section">
      <div className="wrap">
        <div className="splitHeader">
          <div><div className="eyebrow">WHY PREMIUM EXISTS</div><h2>Use Verlune.<br />Then extend it.</h2></div>
          <p className="sectionIntro">Free demonstrates the method on complete standalone tasks. Premium adds deeper task contracts, multi-stage processes, creation tools, adaptation, and evaluation—not an artificially crippled Free tier.</p>
        </div>
        <div className="grid2">
          <article className="vCapabilityCard">
            <div className="vCapabilityIcon"><ArtifactMiniObject type="Builder" /></div>
            <div className="eyebrow">BUILD YOURS</div>
            <h3>Prompt Builder + Workflow Builder</h3>
            <p>Start from an ordinary-language recurring need. The Builders guide you toward a reusable artifact with explicit inputs, boundaries, fallback behavior, and verification.</p>
          </article>
          <article className="vCapabilityCard">
            <div className="vCapabilityIcon"><ArtifactMiniObject type="Workflow" /></div>
            <div className="eyebrow">GO DEEPER</div>
            <h3>Five Premium Workflows</h3>
            <p>Use more structured processes for code review, deep research, decision analysis, learning, and content strategy where stages and verification materially matter.</p>
          </article>
          <article className="vCapabilityCard">
            <div className="vCapabilityIcon"><ArtifactMiniObject type="Prompt" /></div>
            <div className="eyebrow">EIGHT CATEGORIES</div>
            <h3>Four prompts per public category</h3>
            <p>Thirty-two structured Premium prompts span engineering, learning, research, operations, writing, content, planning, and career work.</p>
          </article>
          <article className="vCapabilityCard">
            <div className="vCapabilityIcon"><ArtifactMiniObject type="Toolkit" /></div>
            <div className="eyebrow">ADAPT & EVALUATE</div>
            <h3>Keep the boundary visible</h3>
            <p>Adaptation and evaluation tools help you change an asset for your context and inspect generated artifacts without treating polished output as proof.</p>
          </article>
        </div>
      </div>
    </section>

    <section className="section">
      <div className="wrap">
        <div className="splitHeader">
          <div><div className="eyebrow">PRIVATE ACCESS</div><h2>Purchase entitlement.<br />No new account password.</h2></div>
          <p className="sectionIntro">The v1 access model uses the purchase entitlement as the proof of access. Premium content stays behind server-side validation and a private browser session.</p>
        </div>
        <ol className="workflowRail fourSteps">
          <li><span className="stepNumber">01</span><h3>Purchase</h3><p>When public purchasing opens, complete checkout with the authorized Premium product.</p></li>
          <li><span className="stepNumber">02</span><h3>Receive license</h3><p>Your Lemon Squeezy receipt supplies the checkout email and license key.</p></li>
          <li><span className="stepNumber">03</span><h3>Unlock</h3><p>Verlune validates the entitlement server-side and activates the browser when allowed.</p></li>
          <li><span className="stepNumber">04</span><h3>Use Premium</h3><p>Open protected assets, copy the structure, run it in your AI assistant, and verify the result.</p></li>
        </ol>
      </div>
    </section>

    <section className="section vTrustSection">
      <div className="wrap vTrustGrid">
        <div><div className="eyebrow">WHAT PREMIUM DOES NOT CLAIM</div><h2>Capability without<br />the magic act.</h2></div>
        <div className="vTrustPoints">
          <p><strong>No hosted AI credits.</strong><span>Your compatible AI assistant supplies model execution.</span></p>
          <p><strong>No universal model guarantee.</strong><span>Compatibility and runtime evidence remain scoped claims.</span></p>
          <p><strong>Generated is not certified.</strong><span>A Builder-created artifact does not automatically inherit Verlune certification.</span></p>
          <p><strong>No promise of every future major release.</strong><span>The purchase covers the product and entitlement described at checkout.</span></p>
        </div>
      </div>
    </section>

    <section className="v2Closing">
      <div className="wrap v2ClosingInner">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM</div>
          <h2>Use ours. Build yours.</h2>
          <p>Explore the value now. Purchase only when the public sale gate is actually open.</p>
        </div>
        <div className="actions">
          {commerce.purchaseAvailable
            ? <LemonCheckoutLink href="/api/commerce/verlune-premium/checkout">Get Premium — {VERLUNE_PREMIUM_CANDIDATE_PRICE_USD} USD →</LemonCheckoutLink>
            : <Link className="btn btnPrimary" href="/free">Use Free first →</Link>}
          <Link className="btn btnSecondary" href="/unlock">Unlock existing purchase</Link>
        </div>
      </div>
    </section>
  </main>;
}
