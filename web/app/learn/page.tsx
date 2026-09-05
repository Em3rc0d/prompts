import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Learn | Prompt Machine",
  description: "Practical notes on using AI workflows, verifying outputs, and building Prompt Machine in public.",
};

const guides = [
  {
    href: "/learn/workflows-not-random-prompts",
    label: "WORKFLOW DESIGN",
    title: "Why a reusable workflow is more useful than a random prompt",
    description: "A practical explanation of inputs, process, output contracts, fallbacks, and verification—and why the ZIP should never be the product experience.",
  },
  {
    href: "/learn/test-ai-workflows",
    label: "EVIDENCE",
    title: "How we test an AI workflow without pretending certainty",
    description: "What versioned, structurally checked, runtime tested, improved, and certified are allowed to mean inside Prompt Machine.",
  },
];

export default function LearnPage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <div className="eyebrow">PROMPT MACHINE / LEARN</div>
      <h1>Useful ideas before a purchase.</h1>
      <p className="lead">The Learning layer exists to help people use AI more deliberately, show how the product is built, and let trust accumulate before we ask anyone to buy a collection.</p>
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
      <div className="productMain"><div className="eyebrow">BUILDING IN PUBLIC</div><h2>The product is also a learning process.</h2><p>Prompt Machine is being built while its founder finishes Systems Engineering and turns real software, AI, university, and product-building experience into repeatable workflows. The useful parts of that process belong here: decisions, mistakes, evidence, examples, and what changed after testing.</p></div>
      <aside className="purchasePanel"><span className="purchaseLabel">CONTENT RULE</span><h3>Teach first. Sell second.</h3><p>A useful post should have a natural next step. Most of the time that should be “try the related free workflow,” not “buy now.”</p><Link className="btn btnSecondary" href="/free/developer-starter-pack">Try the free workflows →</Link></aside>
    </div></div></div></section>
  </main>;
}
