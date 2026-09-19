import type { Metadata } from "next";
import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";
import { CODE_REVIEW, FREE_WORKFLOWS, codeReviewPrice } from "@/lib/public-products";

export const metadata: Metadata = {
  title: FREE_WORKFLOWS.name,
  description: "Three free developer workflows for code review, bug diagnosis, and technical decisions. Clear inputs, structured results, and verification guidance.",
  alternates: { canonical: "/free" },
};

export default function FreePage() {
  return <main><section className="pageHero"><div className="wrap"><div className="eyebrow">{FREE_WORKFLOWS.name.toUpperCase()} / $0</div><h1>Make your next<br />AI session useful.</h1><p className="lead">Three complete workflows for recurring developer tasks. Bring a real change, a stubborn bug, or a technical decision—and leave with a result you can inspect.</p><div className="actions"><CommerceLink kind="free">Download the free workflows <span aria-hidden="true">↓</span></CommerceLink><a className="btn btnSecondary" href="#workflows">See the workflows</a></div><p className="micro">ZIP download · Code Review, Bug Diagnosis, Technical Decision · AI access separate</p></div></section>
    <section className="section" id="workflows"><div className="wrap"><div className="grid3">{FREE_WORKFLOWS.workflows.map((workflow, i) => <article className="card" key={workflow.name}><span className="stepNumber">0{i + 1}</span><h2>{workflow.name}</h2><p>{workflow.summary}</p></article>)}</div><p className="notice">Each workflow includes explicit inputs, a process, an output structure, fallback behavior, and verification guidance. They are useful standalone workflows, not time-limited demos.</p></div></section>
    <section className="section"><div className="wrap splitHeader"><div><div className="eyebrow">START SMALL. USE IT FOR REAL.</div><h2>Pick one task.<br />Follow it through.</h2></div><ol className="simpleSteps"><li>Download and extract the package; read its starting instructions.</li><li>Choose a workflow and add it to your AI session with the requested context.</li><li>Inspect the result, verify its claims, and adapt the workflow for your own use.</li></ol></div></section>
    <section className="section"><div className="wrap grid2"><article className="card"><h2>Inspect before you trust.</h2><p>A correct download establishes file integrity. It does not establish behavioral results on every model. The free workflows do not inherit the paid product’s model-specific evidence.</p><Link className="textLink" href="/learn/test-ai-workflows">Understand workflow evidence →</Link></article><article className="card"><h2>Need the focused review package?</h2><p>{CODE_REVIEW.name} combines the evidence-first review workflow with operating guidance and a disclosed test scope. {codeReviewPrice} USD {CODE_REVIEW.billingModel}.</p><Link className="textLink" href="/code-review">Explore Code Review →</Link></article></div><div className="wrap"><p className="micro">Free to use and adapt under the included proprietary license. Redistribution and resale of the workflow materials are restricted. <Link href="/license">Read the license summary.</Link></p></div></section>
  </main>;
}
