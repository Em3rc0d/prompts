import type { Metadata } from "next";
import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";

export const metadata: Metadata = {
  title: "Workflow Collections | Prompt Machine",
  description: "Browse Prompt Machine collections by the outcome you need, starting with the Developer Workflow Collection.",
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
      <p className="lead">Collections group reusable workflows around an outcome. The goal is not to give you more prompt files. It is to give you a broader system you can reuse across related tasks.</p>
      <div className="actions"><CommerceLink kind="free">Start with the Free Library →</CommerceLink><Link className="btn btnSecondary" href="/#how-it-works">How Prompt Machine works</Link></div>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="productFrame">
        <div className="productFrameTop"><span className="productEdition">COLLECTION 01 / BUILD & SHIP</span><span className="releaseBadge"><i /> CANDIDATE · CHECKOUT OFF</span></div>
        <div className="productFrameGrid">
          <div className="productMain">
            <div className="eyebrow">FIRST COMMERCIAL EXPERIMENT</div>
            <h2>Developer Workflow Collection</h2>
            <p>Designed for recurring software work: evidence-first code review, bug diagnosis, technical decisions, and AI workflow design.</p>
            <p className="sectionIntro">The paid candidate adds installable skill surfaces, reusable operating contracts, adaptation guidance, examples, and evidence receipts around the workflows.</p>
            <div className="identity"><div><strong>04</strong><span>workflow families</span></div><div><strong>04</strong><span>skill candidates</span></div><div><strong>$19</strong><span>launch price hypothesis</span></div><div><strong>HOLD</strong><span>not for sale yet</span></div></div>
          </div>
          <aside className="purchasePanel"><span className="purchaseLabel">WHY PAY?</span><h3>Because the collection must save more setup and trial-and-error than the free workflows alone.</h3><p>The upgrade is being tested against that standard. Checkout remains disabled until the evidence and delivery gates close.</p><CommerceLink kind="paid" className="btn btnSecondary">Check the $19 collection →</CommerceLink><p className="micro">While sale status is OFF, this records product interest and opens the release-status page. It does not create a purchase.</p></aside>
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
