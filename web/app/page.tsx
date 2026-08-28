import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";

const problems = [
  ["Missing context", "The model reviews code or makes technical decisions without enough system context."],
  ["Unclear output", "Useful reasoning gets buried in generic prose because the expected output contract was never defined."],
  ["False certainty", "The prompt does not tell the model how to distinguish observation, inference, and unknowns."],
];
const pillars = [
  ["Structure", "Purpose, context, constraints, process, output contract, and fallback behavior where useful."],
  ["Reuse", "Paid templates are designed to be adapted to repeated technical workflows."],
  ["Evidence discipline", "Static quality stays separate from behavioral evidence and certification."],
  ["Provenance", "Commercial assets are governed instead of blindly repackaging third-party prompt bodies."],
];

export default function HomePage() {
  return <main>
    <section className="hero"><div className="wrap heroGrid"><div>
      <div className="eyebrow">Prompt engineering for developers</div>
      <h1>Stop collecting random prompts.</h1>
      <p className="lead">Use structured developer prompts with explicit context, constraints, output contracts, and evidence boundaries.</p>
      <div className="actions"><CommerceLink kind="free">Get 3 Developer Prompts — Free</CommerceLink><Link className="btn btnSecondary" href="/developer-pack">Explore Developer Pack v1</Link></div>
      <p className="trust">No “magic prompt” claims. No fake certification. Use the Free Pack before you buy.</p>
    </div><div className="terminal"><pre>{`// random prompt\n"Review this code and improve it."\n\n// Prompt Quarry\nPURPOSE → CONTEXT → CONSTRAINTS\n→ PROCESS → OUTPUT CONTRACT\n→ UNKNOWN / EVIDENCE BOUNDARY`}</pre></div></div></section>

    <section className="section"><div className="wrap"><div className="eyebrow">The problem</div><h2>A longer prompt is not automatically a better prompt.</h2><p className="sectionIntro">Technical AI work breaks down when the task is underspecified, constraints are missing, outputs are vague, or certainty is invented.</p><div className="grid3">{problems.map(([h,p])=><article className="card" key={h}><h3>{h}</h3><p>{p}</p></article>)}</div></div></section>

    <section className="section" id="free"><div className="wrap"><div className="eyebrow">Free Starter Pack</div><h2>Try Prompt Quarry on a real task first.</h2><p className="sectionIntro">Developer Starter Pack v1 contains three ready-to-use prompts: Code Review, Bug Diagnosis, and Technical Decision, plus a Quickstart and use/adaptation license.</p><div className="actions"><CommerceLink kind="free">Get the Free Developer Starter Pack</CommerceLink></div><p className="micro">$0 · no paid commitment · designed to be useful immediately</p></div></section>

    <section className="section" id="method"><div className="wrap"><div className="eyebrow">Method</div><h2>Prompt Quarry is a prompt factory, not a prompt dump.</h2><div className="grid4">{pillars.map(([h,p])=><article className="card" key={h}><h3>{h}</h3><p>{p}</p></article>)}</div></div></section>

    <section className="section" id="developer-pack"><div className="wrap"><div className="badge">READY · v1.0.0</div><h2>The system behind the Starter Pack.</h2><p className="sectionIntro">The Free Pack gives you three finished prompts. Developer Pack v1 gives you reusable templates, methodology, examples, contracts, and quality gates so you can adapt the approach to your own technical work.</p><div className="productCard"><div><ul className="list"><li>21 governed customer-visible assets</li><li>Reusable prompt templates</li><li>Architecture, evidence, and evaluation methodology</li><li>Task/request contract examples</li><li>Code-review and technical-decision example flows</li><li>Static-quality and release-readiness checklists</li><li>Proprietary use-and-adapt license</li></ul></div><div><div className="price">$19</div><div className="micro">launch · one-time</div><div className="actions"><CommerceLink kind="paid">Get Developer Pack v1</CommerceLink></div></div></div></div></section>

    <section className="section"><div className="wrap"><h2>Use the Free Pack. Upgrade when you need the system.</h2><table className="comparison"><thead><tr><th>Capability</th><th>Starter</th><th>Developer Pack</th></tr></thead><tbody><tr><td>Price</td><td>Free</td><td>$19 launch</td></tr><tr><td>Finished prompts</td><td>3</td><td>Templates + examples</td></tr><tr><td>Reusable template system</td><td>—</td><td>Yes</td></tr><tr><td>Methodology</td><td>—</td><td>Yes</td></tr><tr><td>Contracts / worked flows</td><td>—</td><td>Yes</td></tr><tr><td>Quality checklists</td><td>—</td><td>Yes</td></tr><tr><td>Use/adapt rights</td><td>Yes</td><td>Yes</td></tr><tr><td>Resale/redistribution</td><td>No</td><td>No</td></tr></tbody></table></div></section>

    <section className="section"><div className="wrap"><div className="eyebrow">Evidence</div><h2>We separate what is built from what is proven.</h2><p className="sectionIntro">Developer Pack v1 is commercially READY. Included assets are statically VALID. That does not automatically make them behaviorally TESTED, IMPROVED, CERTIFIED, or PORTABLE.</p><div className="evidence"><span className="state stateStrong">READY · commercial</span><span className="state stateStrong">VALID · static</span><span className="state">TESTED · separate F4 evidence</span><span className="state">CERTIFIED · separate F6 evidence</span></div><p className="notice">You are buying a structured toolkit, not a guarantee that every model will produce the same result on every task.</p></div></section>

    <section className="section"><div className="wrap"><div className="eyebrow">License</div><h2>Use it. Adapt it. Build with it.</h2><p className="sectionIntro">Use and adapt the Pack for your own work, workflows, products, and services. Do not resell, sublicense, redistribute, publish, or reconstruct the Pack/templates as a standalone or competing prompt product.</p><div className="actions"><Link className="btn btnSecondary" href="/license">Read license summary</Link></div></div></section>

    <section className="section"><div className="wrap"><h2>FAQ</h2><div className="faq"><details><summary>Does this work only with ChatGPT?</summary><p>No universal portability claim is made. Cross-provider portability requires separate F7 evidence.</p></details><details><summary>Are these prompts certified?</summary><p>No. Current included assets are statically VALID. CERTIFIED is reserved for F6 evidence.</p></details><details><summary>Can I modify the prompts?</summary><p>Yes, for authorized work, workflows, products, and services under the included license.</p></details><details><summary>Can I resell the prompts or Pack?</summary><p>No. Resale, sublicensing, redistribution, and competing prompt-pack reconstruction are not granted.</p></details><details><summary>Why buy if there is a Free Pack?</summary><p>The Free Pack gives three finished prompts. The paid Pack gives the reusable system behind them.</p></details><details><summary>Is this a subscription?</summary><p>No. Developer Pack v1 is a versioned one-time purchase.</p></details></div></div></section>

    <section className="cta"><div className="wrap"><h2>Start free. Upgrade when the workflow proves useful.</h2><div className="actions" style={{justifyContent:"center"}}><CommerceLink kind="free">Get Free Starter Pack</CommerceLink><CommerceLink kind="paid" className="btn btnSecondary">Get Developer Pack v1 — $19</CommerceLink></div></div></section>
  </main>;
}
