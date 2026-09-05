import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Why Workflows Beat Random Prompts | Prompt Machine",
  description: "A practical guide to turning one-off AI prompting into reusable workflows with explicit inputs, outputs, fallbacks, and verification.",
};

export default function WorkflowGuidePage() {
  return <main>
    <section className="pageHero"><div className="wrap">
      <div className="eyebrow">LEARN / WORKFLOW DESIGN</div>
      <h1>Why a reusable workflow is more useful than a random prompt</h1>
      <p className="lead">A good prompt can produce a useful answer once. A useful workflow makes the task easier to repeat, inspect, adapt, and verify.</p>
    </div></section>

    <section className="section"><div className="wrap"><div className="grid2">
      <article className="card"><h3>The random-prompt loop</h3><p>You open a blank chat, explain the task from memory, notice the answer missed something, add another instruction, repair the format, and repeat the same setup the next time.</p><p>The problem is not that natural-language prompting is bad. The problem is that the operating knowledge stays trapped inside one conversation.</p></article>
      <article className="card"><h3>The workflow loop</h3><p>A workflow makes the repeated parts explicit: what inputs matter, which steps should happen, what evidence can support a claim, what the output must contain, what happens when context is missing, and how the result can be checked.</p></article>
    </div></div></section>

    <section className="section"><div className="wrap">
      <div className="sectionHeader splitHeader"><div><div className="eyebrow">THE CONTRACT</div><h2>Five pieces make a workflow reusable.</h2></div><p className="sectionIntro">Not every task needs a giant template. These are the pieces that should become explicit when they materially improve repeatability.</p></div>
      <div className="pipeline">
        <article className="pipelineStep"><div className="pipelineTop"><span>01</span><code>INPUT</code></div><h3>Required context</h3><p>Define the information capable of changing the result. Do not ask for context merely because a form can contain it.</p></article>
        <article className="pipelineStep"><div className="pipelineTop"><span>02</span><code>PROCESS</code></div><h3>Repeatable steps</h3><p>Make the important reasoning or operating sequence stable enough that another run does not depend on remembering yesterday's chat.</p></article>
        <article className="pipelineStep"><div className="pipelineTop"><span>03</span><code>OUTPUT</code></div><h3>Observable deliverable</h3><p>Specify the fields, decision states, evidence, or structure the consumer actually needs instead of asking for a generically “good answer.”</p></article>
        <article className="pipelineStep"><div className="pipelineTop"><span>04</span><code>FALLBACK</code></div><h3>What happens when it cannot finish</h3><p>A useful workflow knows when to ask, continue with labeled unknowns, stop, or return a safe partial evidence summary.</p></article>
      </div>
      <div className="methodManifest"><div className="manifestLabel">05 / VERIFY</div><p>result <span>→</span> check evidence <span>→</span> expose unknowns <span>→</span> decide whether to act</p></div>
    </div></section>

    <section className="section"><div className="wrap"><div className="grid2">
      <article className="card"><h3>Why the ZIP is not the product</h3><p>A ZIP can transport files. It cannot tell a new customer which workflow matches their goal, where to start, what is free, what the paid collection adds, what has been tested, or how to use the workflow correctly. Delivery format and product experience are different problems.</p></article>
      <article className="card"><h3>What Prompt Machine changes</h3><p>The product starts from the job: choose an outcome, inspect the workflow, apply it, verify the result, and reuse it. Prompt Quarry handles the deeper engineering and evidence underneath.</p></article>
    </div></div></section>

    <section className="cta"><div className="wrap"><h2>Try the idea on a real task.</h2><p>The current Free Library has three structured developer workflows. Use one before deciding whether this approach is useful to you.</p><div className="actions"><Link className="btn btnPrimary" href="/free/developer-starter-pack">Open the Free Library →</Link><Link className="btn btnSecondary" href="/learn">Back to Learn</Link></div></div></section>
  </main>;
}
