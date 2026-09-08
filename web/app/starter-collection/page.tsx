import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Verlune Code Review | Release Status",
  description: "Current release identity, certification scope, package evidence, and provider boundary for the $9 Verlune Code Review hypothesis.",
};

export default function StarterCollectionPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <span className="stateHold">NOT FOR SALE · $9 PRICE HYPOTHESIS · PROVIDER VALIDATION PENDING</span>
      <div className="eyebrow">VERLUNE CODE REVIEW / BUILD & SHIP</div>
      <h1>One focused workflow. Exact evidence. No borrowed certainty.</h1>
      <p className="lead">Verlune Code Review is the first paid-product experiment: an evidence-first workflow for reviewing software changes while preserving uncertainty, distinguishing observed evidence from inference, and keeping the final ship decision human-controlled.</p>
      <div className="actions"><Link className="btn btnPrimary" href="/free/developer-starter-pack">Use the Free Library first</Link><Link className="btn btnSecondary" href="/collections">Back to Verlune workflows</Link></div>
      <p className="notice"><strong>Planned launch price: $9 one-time.</strong> The workflow and customer package have passed their current internal gates. Checkout remains off while the exact Verlune archive is revalidated in the commerce provider and Live custody/delivery remain unobserved.</p>
    </div></section>

    <section className="section"><div className="wrap"><div className="grid2">
      <article className="card"><h3>What you get</h3><ul className="list">
        <li>Exact Evidence-first Code Review v2.2 workflow</li>
        <li>Quickstart and operating guidance</li>
        <li>Evidence and certification-scope disclosure</li>
        <li>Customer license and product-specific sale terms</li>
        <li>Release notice and exact integrity manifest</li>
        <li>Human-controlled ship authority; no automatic approval</li>
      </ul></article>
      <article className="card"><h3>What the evidence supports</h3><p><strong>MODEL_SPECIFIC / PASS_FOR_EXACT_DECLARED_SCOPE</strong></p><p>The exact workflow completed the frozen four-case final regression matrix on <code>gemini-3.5-flash</code> with 4/4 human-review passes. That evidence does not establish universal model portability, automatic correctness, security, compliance, or customer outcomes.</p><p><code>marketing claim &lt;= observed evidence</code></p></article>
    </div></div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">EXACT ARTIFACT</div><h2>The customer package has a frozen identity.</h2></div><p className="sectionIntro">Branding changed the customer wrapper, not the certified workflow bytes. The archive is built twice deterministically and independently checked before provider upload.</p></div>
      <div className="identity"><div><strong>18,859</strong><span>archive bytes</span></div><div><strong>4d7def57…</strong><span>archive SHA-256</span></div><div><strong>77/77</strong><span>Pack QA</span></div><div><strong>8</strong><span>customer files</span></div></div>
      <p className="micro">Archive: <code>verlune-code-review-v1.0.0.zip</code> · Version 1.0.0</p>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">CERTIFIED WORKFLOW</div><h2>The workflow stayed byte-identical through the Verlune rebrand.</h2></div><p className="sectionIntro">The customer-facing brand and packaging changed. The exact workflow covered by the certification did not.</p></div>
      <div className="identity"><div><strong>25,295</strong><span>workflow bytes</span></div><div><strong>6739f9c3…</strong><span>workflow SHA-256</span></div><div><strong>4/4</strong><span>final regression cases</span></div><div><strong>HUMAN</strong><span>ship authority</span></div></div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">REMAINING RELEASE BOUNDARY</div><h2>Packaging PASS is not a sale.</h2></div><p className="sectionIntro">The historical Test integration proved that checkout → order → signed webhook works. The new Verlune archive still needs Test provider metadata validation, followed later by separate Live custody and delivery gates.</p></div>
      <div className="identity"><div><strong>PASS</strong><span>G11 certification scope</span></div><div><strong>PASS</strong><span>G12 deterministic build</span></div><div><strong>PASS</strong><span>G13 Pack QA</span></div><div><strong>OFF</strong><span>public checkout</span></div></div>
    </div></section>
  </main>;
}
