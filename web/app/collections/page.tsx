import type { Metadata } from "next";
import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";

export const metadata: Metadata = {
  title: "Workflow Collections | Verlune",
  description: "Browse Verlune workflows by outcome, from the useful Free Library to the first focused $9 Code Review hypothesis and future broader collections.",
};

const futureCollections = [
  ["LEARN & CREATE", "Learning & Project Workflows", "Candidate demand area. No paid product is claimed yet."],
  ["OPERATE & AUTOMATE", "Operations Workflows", "Candidate demand area for repeatable administrative and business tasks. No paid product is claimed yet."],
  ["RESEARCH & DECIDE", "Research & Decision Workflows", "Candidate expansion area beyond the current technical-decision workflow. No paid product is claimed yet."],
];

export default function CollectionsPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <div className="eyebrow">VERLUNE / WORKFLOWS</div>
      <h1>Pay when the workflow earns repetition.</h1>
      <p className="lead">Start with useful free workflows. The first paid hypothesis is intentionally narrow: one evidence-first Code Review workflow at $9, with its exact scope and evidence visible before checkout is enabled.</p>
      <div className="actions"><CommerceLink kind="free">Start with the Free Library →</CommerceLink><Link className="btn btnSecondary" href="/#how-it-works">How Verlune works</Link></div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="productFrame">
        <div className="productFrameTop"><span className="productEdition">CODE REVIEW / BUILD & SHIP</span><span className="releaseBadge"><i /> FIRST PAID HYPOTHESIS · CHECKOUT OFF</span></div>
        <div className="productFrameGrid">
          <div className="productMain">
            <div className="eyebrow">FIRST PURCHASE EXPERIMENT</div>
            <h2>Verlune Code Review</h2>
            <p>One governed workflow for reviewing software changes with evidence-ranked findings, explicit unknowns, verification guidance, and human ship authority.</p>
            <p className="sectionIntro">The exact workflow is certified for its declared Gemini 3.5 Flash scope. The Verlune package passes deterministic rebuild and 77/77 Pack QA. Provider validation of the rebranded archive is still pending.</p>
            <div className="identity"><div><strong>01</strong><span>workflow</span></div><div><strong>$9</strong><span>price hypothesis</span></div><div><strong>77/77</strong><span>Pack QA</span></div><div><strong>HOLD</strong><span>not for sale</span></div></div>
          </div>
          <aside className="purchasePanel"><span className="purchaseLabel">LOWER-FRICTION ENTRY</span><h3>A focused paid workflow, not a padded bundle.</h3><p>The $9 experiment asks a simple question: does a rigorously packaged Code Review workflow save enough repeated setup and uncertainty to earn the purchase?</p><CommerceLink kind="starter" className="btn btnSecondary">Inspect Code Review →</CommerceLink><p className="micro">Checkout remains fail closed until provider validation and release gates close.</p></aside>
        </div>
      </div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="productFrame">
        <div className="productFrameTop"><span className="productEdition">FUTURE / BUILD & SHIP</span><span className="releaseBadge"><i /> $19 HYPOTHESIS · NOT A RELEASE</span></div>
        <div className="productFrameGrid">
          <div className="productMain">
            <div className="eyebrow">BROADER DEVELOPER SYSTEM</div>
            <h2>Verlune Developer Collection</h2>
            <p>A future broader hypothesis around Code Review, Bug Diagnosis, Technical Decision, and AI Workflow Design.</p>
            <p className="sectionIntro">This is not the current release. It must earn its own behavioral evidence, packaging, certification decisions, and provider gates rather than inheriting Code Review evidence.</p>
            <div className="identity"><div><strong>04</strong><span>candidate families</span></div><div><strong>$19</strong><span>price hypothesis</span></div><div><strong>FUTURE</strong><span>release state</span></div><div><strong>OFF</strong><span>checkout</span></div></div>
          </div>
          <aside className="purchasePanel"><span className="purchaseLabel">UPSELL ONLY WHEN EARNED</span><h3>Broader coverage must create broader value.</h3><p>The future collection should win because additional workflows are useful, not because the $9 product was artificially weakened.</p><CommerceLink kind="paid" className="btn btnSecondary">Inspect the future $19 hypothesis →</CommerceLink></aside>
        </div>
      </div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">NEXT / DEMAND FIRST</div><h2>No catalog for catalog&apos;s sake.</h2></div><p className="sectionIntro">Verlune can expand beyond software, but new collections should follow observed tasks, repeat usage, and buying intent.</p></div>
      <div className="grid3">
        {futureCollections.map(([code, title, copy]) => <article className="card" key={code}><code>{code}</code><h3>{title}</h3><p>{copy}</p></article>)}
      </div>
    </div></section>

    <section className="cta"><div className="wrap"><h2>Not sure what you need?</h2><p>Start with a real task and a free workflow. Usefulness comes before the catalog.</p><div className="actions"><CommerceLink kind="free">Use the Free Library →</CommerceLink></div></div></section>
  </main>;
}
