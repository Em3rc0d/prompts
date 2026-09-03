import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Full Developer Workflow Collection | Prompt Machine",
  description: "Current release status for Prompt Machine's $19 Full Developer Workflow Collection pricing hypothesis.",
};

export default function DeveloperPackPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <span className="stateHold">NOT FOR SALE · RELEASE HARDENING</span>
      <div className="eyebrow">FULL COLLECTION / BUILD & SHIP</div>
      <h1>Developer Workflow Collection</h1>
      <p className="lead">The $19 Full collection is the broader developer-system hypothesis: Code Review, Bug Diagnosis, Technical Decision, and AI Workflow Design. It is an upsell from the focused $9 Starter only when those additional jobs and reusable surfaces justify the extra cost.</p>
      <div className="actions"><Link className="btn btnPrimary" href="/starter-collection">Start with the $9 Starter candidate</Link><Link className="btn btnSecondary" href="/free/developer-starter-pack">Use 3 free workflows first</Link></div>
      <p className="notice"><strong>Planned price: $19 one-time.</strong> This remains a PRICE HYPOTHESIS. Checkout stays disabled until behavioral, parity, archive, delivery, and provider-canary evidence closes the release gates.</p>
    </div></section>

    <section className="section"><div className="wrap"><div className="grid2">
      <article className="card"><h3>What Full must earn beyond Starter</h3><ul className="list">
        <li>Four related workflow families instead of Starter's two</li>
        <li>Four installable skill candidates where supported</li>
        <li>Technical Decision and AI Workflow Design coverage</li>
        <li>Broader reusable operating contracts and adaptation guidance</li>
        <li>Examples and evidence boundaries across the complete collection</li>
        <li>A delivery experience that keeps the starting point obvious</li>
      </ul></article>
      <article className="card"><h3>Current evidence boundary</h3><p><strong>CANDIDATE / NOT FOR SALE</strong></p><p>Skill structure and test infrastructure have advanced, but real behavioral execution, improvement, certification, portability, and paid-market validation remain separate gates.</p><p><code>marketing claim &lt;= observed evidence</code></p></article>
    </div></div></section>

    <section className="section"><div className="wrap"><div className="sectionHeader splitHeader"><div><div className="eyebrow">UPGRADE PRINCIPLE</div><h2>Full must win on additional value, not artificial scarcity.</h2></div><p className="sectionIntro">The Free Library remains useful. Starter must solve its two jobs completely. Full is only worth $19 if the additional workflow families, skills, examples, and adaptation support save enough extra work to earn the upgrade.</p></div><div className="identity"><div><strong>$0</strong><span>Free Library</span></div><div><strong>$9</strong><span>Starter hypothesis</span></div><div><strong>$19</strong><span>Full hypothesis</span></div><div><strong>OFF</strong><span>checkout today</span></div></div></div></section>
  </main>;
}
