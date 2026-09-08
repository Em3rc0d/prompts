import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Future Developer Collection | Verlune",
  description: "A future $19 Verlune developer-workflow hypothesis. Not a current release and not for sale.",
};

export default function DeveloperPackPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <span className="stateHold">FUTURE HYPOTHESIS · NOT FOR SALE</span>
      <div className="eyebrow">VERLUNE / FUTURE DEVELOPER COLLECTION</div>
      <h1>Broader coverage has to earn its own evidence.</h1>
      <p className="lead">The $19 Full collection remains a future hypothesis around Code Review, Bug Diagnosis, Technical Decision, and AI Workflow Design. It does not inherit certification or provider readiness from Verlune Code Review.</p>
      <div className="actions"><Link className="btn btnPrimary" href="/starter-collection">Inspect Verlune Code Review</Link><Link className="btn btnSecondary" href="/free/developer-starter-pack">Use 3 free workflows first</Link></div>
      <p className="notice"><strong>Planned price hypothesis: $19 one-time.</strong> This is not an active release. Each additional workflow or skill must earn its own scope, evidence, packaging, and release decision.</p>
    </div></section>

    <section className="section"><div className="wrap"><div className="grid2">
      <article className="card"><h3>What a Full collection would need to earn</h3><ul className="list">
        <li>Additional workflow families with their own behavioral evidence</li>
        <li>Skill surfaces only where trigger and workflow-parity evidence exists</li>
        <li>Technical Decision and AI Workflow Design coverage</li>
        <li>Coherent operating contracts, examples, and adaptation guidance</li>
        <li>Independent package and provider evidence for the resulting collection</li>
        <li>A clear starting point that does not turn breadth into complexity</li>
      </ul></article>
      <article className="card"><h3>Current boundary</h3><p><strong>FUTURE PRODUCT HYPOTHESIS</strong></p><p>The current paid-release effort is Verlune Code Review. The broader developer collection remains deliberately separate until its added scope earns evidence and customer value.</p><p><code>one product&apos;s evidence != another product&apos;s evidence</code></p></article>
    </div></div></section>

    <section className="section"><div className="wrap"><div className="sectionHeader splitHeader"><div><div className="eyebrow">UPGRADE PRINCIPLE</div><h2>Full should win on additional value, not artificial scarcity.</h2></div><p className="sectionIntro">The free workflows remain useful. Verlune Code Review must solve its focused job completely. A future $19 collection is only justified when broader coverage saves enough additional work to earn the upgrade.</p></div><div className="identity"><div><strong>$0</strong><span>Free Library</span></div><div><strong>$9</strong><span>Code Review hypothesis</span></div><div><strong>$19</strong><span>future Full hypothesis</span></div><div><strong>OFF</strong><span>checkout today</span></div></div></div></section>
  </main>;
}
