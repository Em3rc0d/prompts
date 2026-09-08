import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Learn | Verlune",
  description: "Practical notes on reusable AI workflows, evidence, verification, and the engineering principles behind Verlune.",
};

const guides = [
  {
    href: "/learn/workflows-not-random-prompts",
    label: "WORKFLOW DESIGN",
    title: "Why a reusable workflow is more useful than a random prompt",
    description: "A practical explanation of inputs, process, output contracts, fallbacks, and verification—and why delivery format is not the product experience.",
  },
  {
    href: "/learn/test-ai-workflows",
    label: "EVIDENCE",
    title: "How we test an AI workflow without pretending certainty",
    description: "What versioned, structurally checked, runtime tested, improved, and certified are allowed to mean inside Verlune.",
  },
];

export default function LearnPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <div className="eyebrow">VERLUNE / LEARN</div>
      <h1>Useful ideas before a purchase.</h1>
      <p className="lead">Learn exists to help people use AI more deliberately, understand how Verlune workflows are built, and inspect the evidence before deciding whether a product belongs in their work.</p>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="grid2">
        {guides.map((guide) => <article className="card" key={guide.href}>
          <div className="eyebrow">{guide.label}</div>
          <h3>{guide.title}</h3>
          <p>{guide.description}</p>
          <Link href={guide.href}>Read guide →</Link>
        </article>)}
      </div>
    </div></section>

    <section className="section"><div className="wrap"><div className="productFrame"><div className="productFrameGrid">
      <div className="productMain"><div className="eyebrow">HOW VERLUNE IS BUILT</div><h2>Evidence is part of the product.</h2><p>Verlune turns recurring work into reusable workflow products with explicit inputs, process, boundaries, outputs, and verification. Prompt Machine and Prompt Quarry remain the internal engineering systems underneath; customers should not need to understand those systems to use the product.</p></div>
      <aside className="purchasePanel"><span className="purchaseLabel">CONTENT RULE</span><h3>Teach first. Sell second.</h3><p>A useful article should leave the reader with a better operating model even when they never buy anything.</p><Link className="btn btnSecondary" href="/free/developer-starter-pack">Try the free workflows →</Link></aside>
    </div></div></div></section>
  </main>;
}
