import type { Metadata } from "next";
import Link from "next/link";
import { ReviewExample } from "@/components/review-example";
import { CODE_REVIEW, FREE_WORKFLOWS, codeReviewPrice } from "@/lib/public-products";

export const metadata: Metadata = { alternates: { canonical: "/" } };

export default function HomePage() {
  return <main>
    <section className="homeHero"><div className="wrap heroGrid">
      <div><div className="eyebrow">REUSABLE AI WORKFLOWS / FOR DEVELOPERS</div>
        <h1>Work that deserves more than a <em>blank chat.</em></h1>
        <p className="lead">Bring the context. Follow a repeatable workflow. Get a structured result you can inspect, verify, and use again.</p>
        <div className="actions"><Link className="btn btnPrimary" href="/code-review">Explore {CODE_REVIEW.name} <span aria-hidden="true">↗</span></Link><Link className="btn btnSecondary" href="/free">Try free workflows</Link></div>
        <p className="micro">Downloadable workflows. Your AI session. Your judgment.</p>
      </div>
      <div className="heroVisual"><div className="visualLabel"><span>FROM CHANGE TO DECISION</span><span>01 / CODE REVIEW</span></div><ReviewExample /></div>
    </div></section>

    <section className="section"><div className="wrap"><div className="splitHeader"><div><div className="eyebrow">A REPEATABLE WAY TO WORK</div><h2>Keep the process.<br />Change the input.</h2></div><p className="sectionIntro">Stop rebuilding your instructions with every task. Verlune makes the input, review process, expected result, and checks explicit—so polished wording doesn’t hide missing evidence.</p></div>
      <ol className="workflowRail">{[
        ["Input", "Give the task its context."], ["Workflow", "Follow a defined process."], ["Result", "Get a structured answer."], ["Verify", "Check claims and unknowns."], ["Reuse", "Repeat with the next task."],
      ].map(([title, text], i) => <li key={title}><span className="stepNumber">0{i + 1}</span><h3>{title}</h3><p>{text}</p></li>)}</ol>
    </div></section>

    <section className="section"><div className="wrap productFeature"><div><div className="eyebrow">THE FOCUSED REVIEW WORKFLOW</div><h2>{CODE_REVIEW.name}</h2><p className="lead">{CODE_REVIEW.summary}</p><p>Less setup. Consistent findings. Explicit unknowns. Verification you can act on before making a human-controlled ship decision.</p><Link className="textLink" href="/code-review">Explore the workflow <span aria-hidden="true">→</span></Link></div><div className="pricePanel"><span className="eyebrow">DIGITAL DOWNLOAD</span><div className="price">{codeReviewPrice}<span>USD</span></div><p>{CODE_REVIEW.billingModel} · Version {CODE_REVIEW.version}</p><div className="rule" /><p>Workflow, quickstart, operating guidance, evidence notes, license, and release information.</p><Link className="btn btnSecondary" href="/code-review#inside">See the complete package</Link></div></div></section>

    <section className="section"><div className="wrap"><div className="splitHeader"><div><div className="eyebrow">START WITH A REAL TASK</div><h2>Three useful workflows.<br />Free to use.</h2></div><div><p className="sectionIntro">Review a change, diagnose a bug, or make a technical decision. A practical introduction you can keep using.</p><Link className="textLink" href="/free">Explore {FREE_WORKFLOWS.name} →</Link></div></div><div className="grid3">{FREE_WORKFLOWS.workflows.map((workflow, i) => <article className="card" key={workflow.name}><span className="stepNumber">0{i + 1}</span><h3>{workflow.name}</h3><p>{workflow.summary}</p></article>)}</div></div></section>
  </main>;
}
