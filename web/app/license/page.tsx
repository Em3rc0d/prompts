import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "License | Prompt Machine",
  description: "Prompt Machine commercial license summary for governed workflow collections.",
};

export default function LicensePage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <span className="stateHold">PUBLIC CHECKOUT OFF · PRODUCT-SPECIFIC LICENSES APPLY AT RELEASE</span>
      <div className="eyebrow">PROMPT MACHINE / COMMERCIAL LICENSE</div>
      <h1>Use it. Adapt it. Build with it.</h1>
      <p className="lead">Prompt Machine's intended commercial model allows authorized customers to use and adapt collection materials in their own work while reserving redistribution, sublicensing, and resale rights.</p>
      <p className="notice"><strong>No paid collection is currently for sale.</strong> This page summarizes the intended license model; the exact <code>LICENSE.md</code> packaged with a released collection governs that collection when sale is enabled.</p>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="grid2">
        <article className="card"><h3>Intended permitted use</h3><ul className="list">
          <li>Use for personal, educational, professional, or internal business work</li>
          <li>Modify, customize, translate, combine, and adapt workflows</li>
          <li>Integrate adapted workflow logic into your own application or service when the collection itself is not exposed or redistributed</li>
          <li>Use outputs from authorized use subject to applicable third-party terms</li>
        </ul></article>
        <article className="card"><h3>Rights not granted</h3><ul className="list">
          <li>Sell or resell the collection itself</li>
          <li>Sublicense or redistribute it</li>
          <li>Publish or mirror substantial portions</li>
          <li>Offer lightly modified or substantially equivalent workflow libraries as competing standalone products</li>
          <li>Claim ownership of Prompt Machine-authored materials</li>
        </ul></article>
      </div>
      <p className="notice">Commercial availability never implies that a workflow is behaviorally tested, certified, portable, or guaranteed unless the exact product evidence states so. Starter currently has one preserved runtime observation whose effective classification is <strong>INCONCLUSIVE_PROTOCOL_CONTAMINATION</strong>, with 0 effective PASS and 0 effective FAIL; no clean independent Starter runtime observation exists yet.</p>
      <div className="actions"><Link className="btn btnPrimary" href="/starter-collection">Inspect Starter status</Link><Link className="btn btnSecondary" href="/collections">Back to Collections</Link></div>
    </div></section>
  </main>;
}
