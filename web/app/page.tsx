import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";
import { QuarryEngine } from "@/components/quarry-engine";

const problems = [
  { index: "01", title: "Missing context", copy: "The model reviews code or makes technical decisions without enough system context to know what actually matters." },
  { index: "02", title: "Unclear output", copy: "Useful reasoning dissolves into generic prose when nobody defines the shape, depth, or evidence expected in the answer." },
  { index: "03", title: "False certainty", copy: "When prompts do not separate observation, inference, and unknowns, confident language can masquerade as evidence." },
];

const pipeline = [
  { n: "01", title: "Shape the task", code: "RAW → BRIEF", copy: "Turn an underspecified request into explicit purpose, context, constraints, risk, and output expectations." },
  { n: "02", title: "Engineer the prompt", code: "BRIEF → ASSET", copy: "Compose reusable prompt structure only where each section earns its place in the workflow." },
  { n: "03", title: "Guard the claims", code: "ASSET → VALID", copy: "Check structure, provenance, evidence boundaries, and what the artifact is — and is not — allowed to claim." },
  { n: "04", title: "Package the system", code: "VALID → PRODUCT", copy: "Version governed assets into a customer-visible product with licensing and release discipline." },
];

const freePrompts = [
  { number: "01", title: "Code Review", tag: "software", copy: "Review code for correctness, risk, maintainability, and evidence-backed findings." },
  { number: "02", title: "Bug Diagnosis", tag: "debugging", copy: "Separate symptoms, hypotheses, evidence, unknowns, and the next highest-value diagnostic step." },
  { number: "03", title: "Technical Decision", tag: "research", copy: "Compare options against explicit constraints and produce a decision that exposes trade-offs." },
];

const packAssets = [
  "Reusable prompt templates",
  "Architecture + evidence methodology",
  "Task and request contracts",
  "Worked technical example flows",
  "Static quality + release checklists",
  "Proprietary use-and-adapt license",
];

export default function HomePage() {
  return (
    <main>
      <section className="hero heroPremium">
        <div className="heroGridBackdrop" aria-hidden="true" />
        <div className="heroGlow heroGlowOne" aria-hidden="true" />
        <div className="heroGlow heroGlowTwo" aria-hidden="true" />
        <div className="wrap heroPremiumGrid">
          <div className="heroCopy">
            <div className="heroKicker">
              <span className="signalDot" />
              PROMPT QUARRY / DEVELOPER SYSTEM
            </div>
            <h1>Stop collecting random prompts.</h1>
            <p className="heroStatement">Build repeatable AI workflows with structure, constraints, output contracts, and evidence boundaries.</p>
            <div className="actions heroActions">
              <CommerceLink kind="free" className="btn btnPrimary btnHero">Get 3 Developer Prompts <span>→</span></CommerceLink>
              <Link className="btn btnGhost btnHero" href="/developer-pack">Explore Developer Pack v1</Link>
            </div>
            <div className="heroProof">
              <div><strong>03</strong><span>free prompts</span></div>
              <div><strong>21</strong><span>governed assets</span></div>
              <div><strong>VALID</strong><span>static maturity</span></div>
              <div><strong>READY</strong><span>commercial state</span></div>
            </div>
            <p className="trust heroTrust"><span>◆</span> No magic-prompt claims. No fake certification. Use the Free Pack before you buy.</p>
          </div>
          <QuarryEngine />
        </div>
        <div className="heroTicker" aria-hidden="true">
          <div>
            <span>STRUCTURE</span><b>◆</b><span>PROVENANCE</span><b>◆</b><span>EVIDENCE</span><b>◆</b><span>REUSE</span><b>◆</b><span>UNKNOWN = UNKNOWN</span><b>◆</b>
            <span>STRUCTURE</span><b>◆</b><span>PROVENANCE</span><b>◆</b><span>EVIDENCE</span><b>◆</b><span>REUSE</span><b>◆</b><span>UNKNOWN = UNKNOWN</span><b>◆</b>
          </div>
        </div>
      </section>

      <section className="section problemSection">
        <div className="wrap">
          <div className="sectionHeader splitHeader">
            <div>
              <div className="eyebrow">01 / WHY</div>
              <h2>Prompts fail before the model does.</h2>
            </div>
            <p className="sectionIntro">A longer prompt is not automatically a better prompt. Technical AI work breaks when the task itself is vague, the constraints are invisible, or certainty is allowed to outrun evidence.</p>
          </div>
          <div className="problemGrid">
            {problems.map((problem) => (
              <article className="problemCard" key={problem.index}>
                <div className="cardIndex">{problem.index}</div>
                <div className="problemGlyph" aria-hidden="true"><span /><span /><span /></div>
                <h3>{problem.title}</h3>
                <p>{problem.copy}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section methodSection" id="method">
        <div className="wrap">
          <div className="sectionHeader splitHeader">
            <div>
              <div className="eyebrow">02 / METHOD</div>
              <h2>A prompt factory, not a prompt dump.</h2>
            </div>
            <p className="sectionIntro">Prompt Quarry treats prompts as engineered artifacts. The goal is not to collect clever wording. The goal is to make repeated technical work easier to specify, inspect, adapt, and govern.</p>
          </div>
          <div className="pipeline">
            {pipeline.map((step) => (
              <article className="pipelineStep" key={step.n}>
                <div className="pipelineTop"><span>{step.n}</span><code>{step.code}</code></div>
                <h3>{step.title}</h3>
                <p>{step.copy}</p>
              </article>
            ))}
          </div>
          <div className="methodManifest">
            <div className="manifestLabel">OPERATING PRINCIPLE</div>
            <p>AI proposes <span>/</span> Human decides <span>/</span> System executes <span>/</span> System proves</p>
          </div>
        </div>
      </section>

      <section className="section freeSection" id="free">
        <div className="wrap freeLayout">
          <div className="freeCopy">
            <div className="eyebrow">03 / START FREE</div>
            <h2>Use it on real work before you buy.</h2>
            <p className="sectionIntro">Developer Starter Pack v1 is a deliberately small field kit: three finished prompts, a Quickstart, and clear use/adaptation rights. Enough to experience the method without giving away the whole factory.</p>
            <div className="actions">
              <CommerceLink kind="free" className="btn btnPrimary btnHero">Get the Free Starter Pack <span>→</span></CommerceLink>
            </div>
            <p className="micro">$0 · no account maze · designed for immediate use</p>
          </div>
          <div className="promptStack">
            {freePrompts.map((prompt) => (
              <article className="promptFile" key={prompt.number}>
                <div className="promptFileTop"><span>PQ / {prompt.number}</span><code>{prompt.tag}</code></div>
                <h3>{prompt.title}</h3>
                <p>{prompt.copy}</p>
                <div className="promptFileBottom"><span>.md</span><span>structured / reusable</span></div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section productSection" id="developer-pack">
        <div className="wrap">
          <div className="productFrame">
            <div className="productFrameTop">
              <span className="productEdition">PROMPT QUARRY / DEVELOPER PACK</span>
              <span className="releaseBadge"><i /> READY · v1.0.0</span>
            </div>
            <div className="productFrameGrid">
              <div className="productMain">
                <div className="eyebrow">04 / THE SYSTEM</div>
                <h2>The system behind the Starter Pack.</h2>
                <p>The Free Pack gives you finished prompts. Developer Pack v1 gives you the reusable architecture behind them: templates, methodology, contracts, examples, quality gates, and commercial use/adaptation rights.</p>
                <div className="assetGrid">
                  {packAssets.map((asset, index) => <div className="assetRow" key={asset}><span>{String(index + 1).padStart(2, "0")}</span><strong>{asset}</strong></div>)}
                </div>
              </div>
              <aside className="purchasePanel">
                <span className="purchaseLabel">LAUNCH LICENSE</span>
                <div className="priceLarge"><sup>$</sup>19</div>
                <p>One-time purchase. Versioned digital product.</p>
                <CommerceLink kind="paid" className="btn btnPrimary btnPurchase">Get Developer Pack v1 <span>→</span></CommerceLink>
                <ul>
                  <li><span>✓</span> 21 governed customer-visible assets</li>
                  <li><span>✓</span> Use + adapt in your own work/products</li>
                  <li><span>×</span> No resale or redistribution</li>
                </ul>
                <Link className="textLink" href="/developer-pack">Inspect the full pack →</Link>
              </aside>
            </div>
          </div>
        </div>
      </section>

      <section className="section evidenceSection">
        <div className="wrap evidenceLayout">
          <div className="evidenceCopy">
            <div className="eyebrow">05 / EVIDENCE</div>
            <h2>We separate what is built from what is proven.</h2>
            <p className="sectionIntro">Developer Pack v1 is commercially READY. Its included assets are statically VALID. Those labels do not magically become runtime evidence.</p>
            <p className="evidenceRule">not observed <span>==</span> unknown</p>
          </div>
          <div className="evidenceLadder">
            <div className="evidenceRow active"><span>VALID</span><strong>Static acceptance</strong><em>OBSERVED</em></div>
            <div className="evidenceRow"><span>TESTED</span><strong>Behavioral F4</strong><em>SEPARATE GATE</em></div>
            <div className="evidenceRow"><span>IMPROVED</span><strong>Comparative F5</strong><em>SEPARATE GATE</em></div>
            <div className="evidenceRow"><span>CERTIFIED</span><strong>Repeated F6</strong><em>SEPARATE GATE</em></div>
            <div className="evidenceRow"><span>PORTABLE</span><strong>Cross-provider F7</strong><em>SEPARATE GATE</em></div>
          </div>
        </div>
      </section>

      <section className="section licenseBand">
        <div className="wrap licenseBandInner">
          <div>
            <div className="eyebrow">06 / LICENSE</div>
            <h2>Use it. Adapt it. Build with it.</h2>
          </div>
          <div className="licenseRules">
            <span className="allowed">USE <b>YES</b></span>
            <span className="allowed">ADAPT <b>YES</b></span>
            <span className="allowed">INTEGRATE <b>YES</b></span>
            <span className="blocked">RESELL <b>NO</b></span>
            <span className="blocked">REDISTRIBUTE <b>NO</b></span>
          </div>
          <Link className="textLink" href="/license">Read license summary →</Link>
        </div>
      </section>

      <section className="section faqSection">
        <div className="wrap faqLayout">
          <div>
            <div className="eyebrow">07 / FAQ</div>
            <h2>Before you add it to your stack.</h2>
          </div>
          <div className="faq premiumFaq">
            <details><summary>Does this work only with ChatGPT?<span>+</span></summary><p>No universal portability claim is made. The assets are model-agnostic where practical, but cross-provider portability requires separate F7 evidence.</p></details>
            <details><summary>Are these prompts certified?<span>+</span></summary><p>No. Current included assets are statically VALID. CERTIFIED is reserved for F6 evidence.</p></details>
            <details><summary>Can I modify the prompts?<span>+</span></summary><p>Yes, for authorized work, workflows, products, and services under the included use-and-adapt license.</p></details>
            <details><summary>Can I resell the prompts or Pack?<span>+</span></summary><p>No. Resale, sublicensing, redistribution, and competing prompt-pack reconstruction are not granted.</p></details>
            <details><summary>Why buy if there is a Free Pack?<span>+</span></summary><p>The Free Pack gives three finished prompts. Developer Pack v1 gives the reusable system behind them.</p></details>
            <details><summary>Is this a subscription?<span>+</span></summary><p>No. Developer Pack v1 is a versioned one-time purchase.</p></details>
          </div>
        </div>
      </section>

      <section className="cta premiumCta">
        <div className="ctaGridBackdrop" aria-hidden="true" />
        <div className="wrap premiumCtaInner">
          <div className="eyebrow">ENTER THE QUARRY</div>
          <h2>Start free.<br /><span>Upgrade when the system earns it.</span></h2>
          <p>Three structured developer prompts are enough to test the idea on your own work.</p>
          <div className="actions ctaActions">
            <CommerceLink kind="free" className="btn btnPrimary btnHero">Get Free Starter Pack <span>→</span></CommerceLink>
            <CommerceLink kind="paid" className="btn btnGhost btnHero">Developer Pack v1 · $19</CommerceLink>
          </div>
        </div>
      </section>
    </main>
  );
}
