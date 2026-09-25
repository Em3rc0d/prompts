import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "License | Verlune",
  description: "Verlune commercial license summary for governed workflow products.",
};

export default function LicensePage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <span className="stateHold">PUBLIC CHECKOUT OFF · PRODUCT-SPECIFIC LICENSES APPLY AT RELEASE</span>
      <div className="eyebrow">VERLUNE / COMMERCIAL LICENSE</div>
      <h1>Use it. Adapt it. Build with it.</h1>
      <p className="lead">Verlune products are designed for authorized customers to use and adapt in their own work while reserving redistribution, sublicensing, and resale rights.</p>
      <p className="notice"><strong>Verlune Code Review is not publicly for sale yet.</strong> This page summarizes the intended license model; the exact <code>CUSTOMER-LICENSE.md</code> packaged with a released product governs that product when sale is enabled.</p>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="grid2">
        <article className="card"><h3>Intended permitted use</h3><ul className="list">
          <li>Use for personal, educational, professional, or internal business work</li>
          <li>Modify, customize, translate, combine, and adapt workflow materials</li>
          <li>Integrate adapted workflow logic into your own application or service when the product itself is not exposed or redistributed</li>
          <li>Use outputs from authorized use subject to applicable third-party terms</li>
        </ul></article>
        <article className="card"><h3>Rights not granted</h3><ul className="list">
          <li>Sell or resell the product itself</li>
          <li>Sublicense or redistribute it</li>
          <li>Publish or mirror substantial portions</li>
          <li>Offer lightly modified or substantially equivalent workflow libraries as competing standalone products</li>
          <li>Claim ownership of Verlune-authored customer materials</li>
        </ul></article>
      </div>
      <p className="notice">Commercial availability never implies that a workflow is behaviorally tested, certified, portable, or guaranteed unless the exact product evidence says so. Verlune Code Review currently carries a scoped certification for the exact declared workflow surface on <strong>Gemini 3.5 Flash</strong>; that is a model-specific claim, not a universal portability claim. Final provider validation of the Verlune-branded customer archive remains pending.</p>
      <div className="actions"><Link className="btn btnPrimary" href="/starter-collection">Inspect Verlune Code Review</Link><Link className="btn btnSecondary" href="/collections">Back to Products</Link></div>
    </div></section>
  </main>;
}
