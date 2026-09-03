import type { Metadata } from "next";
import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";

export const metadata: Metadata = {
  title: "Workflow Collections | Prompt Machine",
  description: "Browse Prompt Machine collections by outcome, from the Free Library to the $9 Starter and $19 Full developer collection hypotheses.",
};

const futureCollections = [
  ["LEARN & CREATE", "Learning & Project Workflows", "Candidate demand area. No paid product is claimed yet."],
  ["OPERATE & AUTOMATE", "Operations Workflows", "Candidate demand area for repeatable administrative and business tasks. No paid product is claimed yet."],
  ["RESEARCH & DECIDE", "Research & Decision Workflows", "Candidate expansion area beyond the current technical-decision workflow. No paid product is claimed yet."],
];

export default function CollectionsPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <div className="eyebrow">PROMPT MACHINE / COLLECTIONS</div>
      <h1>Buy a collection when the problem repeats.</h1>
      <p className="lead">Collections group reusable workflows around an outcome. Start free, pay $9 when a focused reusable setup earns it, and move to the $19 full collection only when broader coverage is worth the upgrade.</p>
      <div className="actions"><CommerceLink kind="free">Start with the Free Library →</CommerceLink><Link className="btn btnSecondary" href="/#how-it-works">How Prompt Machine works</Link></div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="productFrame">
        <div className="productFrameTop"><span className="productEdition">STARTER / BUILD & SHIP</span><span className="releaseBadge"><i /> PRIMARY PAID HYPOTHESIS · CHECKOUT OFF</span></div>
        <div className="productFrameGrid">
          <div className="productMain">
            <div className="eyebrow">FIRST PURCHASE EXPERIMENT</div>
            <h2>Starter Collection</h2>
            <p>Two complete recurring developer jobs: evidence-first Code Review and Bug Diagnosis, delivered through a reusable customer experience around those workflows.</p>
            <p className="sectionIntro">The current governed archive is the 9-file workflow product: START_HERE, task selection, two workflows, worked examples, verification guidance, adaptation, evidence disclosure, and license. Two related skill surfaces are tracked separately as structural candidates; they are not supported or included in the current Starter archive unless they later earn trigger, forward-behavior, and workflow-parity evidence.</p>
            <div className="identity"><div><strong>02</strong><span>workflow families</span></div><div><strong>00</strong><span>supported skills today</span></div><div><strong>$9</strong><span>price hypothesis</span></div><div><strong>HOLD</strong><span>not for sale</span></div></div>
          </div>
          <aside className="purchasePanel"><span className="purchaseLabel">LOWER-FRICTION ENTRY</span><h3>Pay for a complete focused system, not an intentionally broken free tier.</h3><p>The Free Library remains useful by itself. Starter must earn $9 by reducing setup and repeat work around two high-frequency jobs.</p><CommerceLink kind="starter" className="btn btnSecondary">Check the $9 Starter →</CommerceLink><p className="micro">This records Starter intent and opens its release-status page. It cannot create a purchase while checkout is off.</p></aside>
        </div>
      </div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="productFrame">
        <div className="productFrameTop"><span className="productEdition">FULL / BUILD & SHIP</span><span className="releaseBadge"><i /> PREMIUM HYPOTHESIS · CHECKOUT OFF</span></div>
        <div className="productFrameGrid">
          <div className="productMain">
            <div className="eyebrow">BROADER DEVELOPER SYSTEM</div>
            <h2>Developer Workflow Collection</h2>
            <p>Extends the system to technical decisions and AI workflow design alongside Code Review and Bug Diagnosis.</p>
            <p className="sectionIntro">The full candidate targets four workflow families, four skill candidates, reusable operating contracts, examples, adaptation guidance, and visible evidence boundaries.</p>
            <div className="identity"><div><strong>04</strong><span>workflow families</span></div><div><strong>04</strong><span>skill candidates</span></div><div><strong>$19</strong><span>price hypothesis</span></div><div><strong>HOLD</strong><span>not for sale</span></div></div>
          </div>
          <aside className="purchasePanel"><span className="purchaseLabel">UPSELL ONLY WHEN EARNED</span><h3>The full collection should win on breadth, not artificial restrictions.</h3><p>A customer should be able to stay with Starter if those two jobs are enough. The $19 tier must justify itself with genuinely broader reusable coverage.</p><CommerceLink kind="paid" className="btn btnSecondary">Compare the $19 Full →</CommerceLink></aside>
        </div>
      </div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">NEXT / DEMAND FIRST</div><h2>We will not manufacture a catalog nobody asked for.</h2></div><p className="sectionIntro">Prompt Machine can expand beyond software, but new collections should follow observed tasks, repeat usage, and buying intent.</p></div>
      <div className="grid3">
        {futureCollections.map(([code, title, copy]) => <article className="card" key={code}><code>{code}</code><h3>{title}</h3><p>{copy}</p></article>)}
      </div>
    </div></section>

    <section className="cta"><div className="wrap"><h2>Not sure what collection you need?</h2><p>Start with a real task and a free workflow. Your usage tells us more than a demographic label ever could.</p><div className="actions"><CommerceLink kind="free">Use the Free Library →</CommerceLink></div></div></section>
  </main>;
}
