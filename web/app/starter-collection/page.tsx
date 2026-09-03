import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Starter Collection | Prompt Machine",
  description: "Current release status and evidence boundary for Prompt Machine's $9 Starter Collection pricing hypothesis.",
};

export default function StarterCollectionPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <span className="stateHold">NOT FOR SALE · $9 PRICE HYPOTHESIS · RUNTIME EVIDENCE OPEN</span>
      <div className="eyebrow">STARTER COLLECTION / BUILD & SHIP</div>
      <h1>Two governed workflows. A complete customer payload. Runtime proof still to earn.</h1>
      <p className="lead">The Starter Collection is Prompt Machine's primary first-purchase experiment. It focuses on two recurring developer jobs—reviewing a software change and diagnosing a bug—without intentionally crippling either workflow to force an upgrade.</p>
      <div className="actions"><Link className="btn btnPrimary" href="/free/developer-starter-pack">Use the Free Library first</Link><Link className="btn btnSecondary" href="/developer-pack">Compare the $19 full collection</Link></div>
      <p className="notice"><strong>Planned launch price: $9 one-time.</strong> This is still a PRICE HYPOTHESIS, not an active checkout. Static contracts, executable surfaces, the 9-file customer payload, and deterministic packaging are complete; Starter-specific runtime behavior, provider custody, delivery, and real customer value remain separate open gates.</p>
    </div></section>

    <section className="section"><div className="wrap"><div className="grid2">
      <article className="card"><h3>Frozen Starter scope</h3><ul className="list">
        <li>Evidence-first Code Review workflow</li>
        <li>Evidence-first Bug Diagnosis workflow</li>
        <li><code>review-code-with-evidence</code> skill candidate — conditional on skill evidence</li>
        <li><code>diagnose-bugs-with-evidence</code> skill candidate — conditional on skill evidence</li>
        <li>START_HERE entrypoint and task chooser</li>
        <li>Two synthetic worked examples and verification guidance</li>
        <li>Adaptation cheatsheet, evidence disclosure, and collection license</li>
      </ul></article>
      <article className="card"><h3>Current evidence boundary</h3><p><strong>STATIC PRODUCT SURFACES + PACKAGING PASS / RUNTIME UNOBSERVED</strong></p><p>Two workflow contracts and two executable prompt surfaces are statically frozen. The required customer payload is 9/9 and its ZIP rebuild is byte-for-byte deterministic. None of that establishes Starter runtime behavior, certification, portability, provider delivery, or customer outcomes.</p><p><code>packaging evidence != behavioral evidence</code></p></article>
    </div></div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">CURRENT ARTIFACT</div><h2>The package has an exact identity before we ask anyone to pay.</h2></div><p className="sectionIntro">The current governed build contains exactly nine required customer files. Its deterministic identity is packaging evidence only and does not imply provider custody or customer delivery.</p></div>
      <div className="identity"><div><strong>9/9</strong><span>required assets</span></div><div><strong>50,918</strong><span>archive bytes</span></div><div><strong>4eceb1ee…</strong><span>SHA-256</span></div><div><strong>PASS</strong><span>byte-for-byte rebuild</span></div></div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">NEXT EVIDENCE</div><h2>Four product-specific canaries are prepared. None has been executed.</h2></div><p className="sectionIntro">Code Review and Bug Diagnosis each have a NORMAL and an EMBEDDED_OVERRIDE case with expected outcomes fixed outside runtime input. All four remain disarmed; the first permitted observation is one Code Review NORMAL run followed by human review when the inference budget is explicitly reopened.</p></div>
      <div className="identity"><div><strong>4</strong><span>prepared canaries</span></div><div><strong>4</strong><span>out-of-band reviews</span></div><div><strong>0</strong><span>Starter runtime observations</span></div><div><strong>OFF</strong><span>automatic execution</span></div></div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">WHY $9 EXISTS</div><h2>Reduce the first-purchase risk without reducing the usefulness.</h2></div><p className="sectionIntro">The free layer proves the method. Starter adds a coherent reusable setup around two high-frequency jobs. The $19 full collection remains the broader hypothesis for technical decisions, AI workflow design, additional skill candidates, and the complete developer system.</p></div>
      <div className="identity"><div><strong>$0</strong><span>Free Library</span></div><div><strong>$9</strong><span>Starter hypothesis</span></div><div><strong>$19</strong><span>Full hypothesis</span></div><div><strong>OFF</strong><span>checkout today</span></div></div>
    </div></section>
  </main>;
}
