import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "How We Test AI Workflows | Verlune",
  description: "How Verlune separates structure checks, runtime evidence, improvements, certification, and portability without overstating what has been proven.",
};

export default function TestWorkflowGuidePage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <div className="eyebrow">VERLUNE / EVIDENCE</div>
      <h1>How we test an AI workflow without pretending certainty</h1>
      <p className="lead">A professional-looking prompt is not automatically a tested workflow. Verlune keeps different kinds of evidence separate so you can tell what has actually been observed.</p>
    </div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">THE LADDER</div><h2>Each label must earn a different claim.</h2></div><p className="sectionIntro">The internal program is more detailed, but the customer-facing idea is simple: stronger words require stronger evidence.</p></div>
      <div className="pipeline">
        <article className="pipelineStep"><div className="pipelineTop"><span>01</span><code>VERSIONED</code></div><h3>We know which artifact this is</h3><p>The workflow has an identifiable version or fingerprint so later changes cannot silently rewrite the evidence.</p></article>
        <article className="pipelineStep"><div className="pipelineTop"><span>02</span><code>STRUCTURE</code></div><h3>The contract can be inspected</h3><p>Required inputs, evidence boundaries, output structure, fallbacks, references, and packaging can be checked without claiming the model behaves correctly.</p></article>
        <article className="pipelineStep"><div className="pipelineTop"><span>03</span><code>RUNTIME</code></div><h3>A real model execution happened</h3><p>Frozen inputs are run against an identified real runtime, and the complete output is preserved. Synthetic examples cannot substitute for this evidence.</p></article>
        <article className="pipelineStep"><div className="pipelineTop"><span>04</span><code>IMPROVED</code></div><h3>A change beat its baseline</h3><p>An improved version needs a traceable failure, an explicit change, and a retest. “We edited the prompt” is not comparative evidence.</p></article>
      </div>
      <div className="methodManifest"><div className="manifestLabel">05 / CERTIFIED</div><p>repeated evidence <span>+</span> required gates <span>+</span> known limits <span>→</span> certification decision</p></div>
    </div></section>

    <section className="section"><div className="wrap"><div className="grid2">
      <article className="card"><h3>Why repeatability matters</h3><p>One successful answer can be luck, favorable wording, or an easy fixture. Repeated independent executions help show whether the workflow preserves its decision boundaries and output behavior.</p></article>
      <article className="card"><h3>Why portability is separate</h3><p>A workflow that behaves correctly on one named model or host is not automatically proven on every AI product. Support claims follow observed host evidence rather than assuming identical behavior everywhere.</p></article>
    </div></div></section>

    <section className="section"><div className="wrap"><div className="productFrame"><div className="productFrameGrid">
      <div className="productMain"><div className="eyebrow">CURRENT VERLUNE RULE</div><h2>Marketing claim ≤ observed evidence.</h2><p>Build success, archive integrity, a checkout test, provider custody, buyer delivery, and customer value are different claims. We do not silently collapse them into one stronger statement.</p></div>
      <aside className="purchasePanel"><span className="purchaseLabel">FIRST PAID PRODUCT</span><h3>Verlune Code Review</h3><p>The workflow has a scoped certification on Gemini 3.5 Flash and the customer archive has passed deterministic build and pack QA. Final provider validation for the Verlune-branded archive is still pending, so public checkout remains off.</p><Link className="btn btnSecondary" href="/starter-collection">Inspect current status →</Link></aside>
    </div></div></div></section>

    <section className="cta"><div className="wrap"><h2>Trust should be inspectable.</h2><p>Start with the free workflows, then judge whether the structure and evidence are useful on your own task.</p><div className="actions"><Link className="btn btnPrimary" href="/free/developer-starter-pack">Try the Free Library →</Link><Link className="btn btnSecondary" href="/learn">Back to Learn</Link></div></div></section>
  </main>;
}
