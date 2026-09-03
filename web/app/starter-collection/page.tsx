import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Starter Collection | Prompt Machine",
  description: "Release status and scope for Prompt Machine's $9 Starter Collection pricing hypothesis.",
};

export default function StarterCollectionPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <span className="stateHold">NOT FOR SALE · SCOPE FROZEN · RELEASE HARDENING</span>
      <div className="eyebrow">STARTER COLLECTION / BUILD & SHIP</div>
      <h1>A smaller paid step that still solves complete tasks.</h1>
      <p className="lead">The Starter Collection is Prompt Machine's primary first-purchase experiment. It focuses on two recurring developer jobs—reviewing a software change and diagnosing a bug—without intentionally crippling either workflow to force an upgrade.</p>
      <div className="actions"><Link className="btn btnPrimary" href="/free/developer-starter-pack">Use the Free Library first</Link><Link className="btn btnSecondary" href="/developer-pack">Compare the $19 full collection</Link></div>
      <p className="notice"><strong>Planned launch price: $9 one-time.</strong> This is a PRICE HYPOTHESIS, not an active checkout. The scope is frozen, but behavioral testing, governed customer surfaces, packaging, provider custody, and delivery evidence are still required before sale.</p>
    </div></section>

    <section className="section"><div className="wrap"><div className="grid2">
      <article className="card"><h3>Frozen Starter scope</h3><ul className="list">
        <li>Evidence-first Code Review workflow</li>
        <li>Evidence-first Bug Diagnosis workflow</li>
        <li><code>review-code-with-evidence</code> skill candidate</li>
        <li><code>diagnose-bugs-with-evidence</code> skill candidate</li>
        <li>START_HERE entrypoint and task chooser</li>
        <li>Worked examples and verification guidance</li>
        <li>Adaptation cheatsheet for recurring use</li>
      </ul></article>
      <article className="card"><h3>Current evidence boundary</h3><p><strong>SCOPE FROZEN / PRODUCT NOT READY</strong></p><p>The commercial contents are decided, but the final governed customer prompt surfaces are not complete. Scope freeze does not imply runtime testing, certification, portability, or readiness to sell.</p><p><code>scope frozen != behavior proven</code></p></article>
    </div></div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">WHY $9 EXISTS</div><h2>Reduce the first-purchase risk without reducing the usefulness.</h2></div><p className="sectionIntro">The free layer proves the method. Starter adds a more complete reusable setup around two high-frequency jobs. The $19 full collection remains the broader option for technical decisions, AI workflow design, four skill candidates, and the complete developer system.</p></div>
      <div className="identity"><div><strong>$0</strong><span>Free Library</span></div><div><strong>$9</strong><span>Starter hypothesis</span></div><div><strong>$19</strong><span>Full hypothesis</span></div><div><strong>OFF</strong><span>checkout today</span></div></div>
    </div></section>
  </main>;
}
