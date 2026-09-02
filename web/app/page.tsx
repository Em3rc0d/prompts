import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";
import { QuarryEngine } from "@/components/quarry-engine";

const outcomes = [
  ["01", "BUILD & SHIP", "Make technical work easier to repeat", "Review changes, diagnose problems, compare implementation options, and turn recurring technical tasks into explicit workflows."],
  ["02", "RESEARCH & DECIDE", "Move from information to a decision", "Structure evidence, preserve hard constraints, compare options consistently, and make uncertainty visible before committing."],
  ["03", "LEARN & CREATE", "Turn knowledge into useful work", "Use repeatable workflows to understand material, organize projects, transform information, and create deliverables without starting from zero."],
  ["04", "OPERATE & AUTOMATE", "Reduce repetitive operational work", "Identify routine tasks that can become explicit AI-assisted workflows with clear inputs, outputs, boundaries, and verification."],
];

const howItWorks = [
  ["01", "Choose the outcome", "Start with what you need to get done, not with a prompt format or a profession."],
  ["02", "Run the workflow", "Follow a reusable input, process, output, fallback, and verification contract instead of improvising every session."],
  ["03", "Inspect the boundaries", "See what is versioned, what has been checked, what remains unknown, and what the workflow must not claim."],
  ["04", "Upgrade when useful", "Use standalone workflows for free. Buy a collection when broader coverage, skills, examples, and adaptation guidance earn the upgrade."],
];

export default function HomePage() {
  return (
    <main>
      <section className="hero heroPremium">
        <div className="heroGridBackdrop" aria-hidden="true" />
        <div className="heroGlow heroGlowOne" aria-hidden="true" />
        <div className="wrap heroPremiumGrid">
          <div className="heroCopy">
            <div className="heroKicker"><span className="signalDot" />PROMPT MACHINE / AI WORKFLOW LIBRARY</div>
            <h1>Start with the task. Not a blank chat.</h1>
            <p className="heroStatement">Prompt Machine turns recurring work into reusable AI workflows you can discover by outcome, understand before using, and verify after the result.</p>
            <div className="actions heroActions">
              <CommerceLink kind="free" className="btn btnPrimary btnHero">Start with 3 free workflows <span>→</span></CommerceLink>
              <Link className="btn btnGhost btnHero" href="/collections">Explore collections</Link>
            </div>
            <div className="heroProof">
              <div><strong>$0</strong><span>useful free entry</span></div>
              <div><strong>03</strong><span>available workflows</span></div>
              <div><strong>$19</strong><span>paid launch hypothesis</span></div>
              <div><strong>TRACE</strong><span>version + evidence</span></div>
            </div>
            <p className="trust heroTrust"><span>◆</span> The customer sees the workflow. Prompt Quarry handles the engineering and evidence underneath.</p>
          </div>
          <QuarryEngine />
        </div>
      </section>

      <section className="section methodSection" id="workflows">
        <div className="wrap">
          <div className="sectionHeader splitHeader">
            <div><div className="eyebrow">01 / FIND YOUR JOB</div><h2>What are you trying to get done?</h2></div>
            <p className="sectionIntro">Prompt Machine is organized around outcomes. Your profession can help us recommend workflows later, but the task comes first.</p>
          </div>
          <div className="pipeline">
            {outcomes.map(([n, code, title, copy]) => <article className="pipelineStep" key={n}><div className="pipelineTop"><span>{n}</span><code>{code}</code></div><h3>{title}</h3><p>{copy}</p></article>)}
          </div>
          <div className="methodManifest"><div className="manifestLabel">DISCOVERY PRINCIPLE</div><p>goal <span>→</span> workflow <span>→</span> result <span>→</span> verify <span>→</span> reuse</p></div>
        </div>
      </section>

      <section className="section freeSection" id="free">
        <div className="wrap freeLayout">
          <div className="freeCopy">
            <div className="eyebrow">02 / FREE LIBRARY</div>
            <h2>The free version must be useful by itself.</h2>
            <p className="sectionIntro">Start with three structured developer workflows already available at $0. They are not crippled demos: each includes inputs, evidence rules, process, output contract, fallback behavior, and verification guidance.</p>
            <div className="actions"><CommerceLink kind="free" className="btn btnPrimary btnHero">Get the free workflows <span>→</span></CommerceLink></div>
            <p className="micro">Current delivery artifact: v1.1.0 · 7 customer files · archive integrity verified before delivery</p>
          </div>
          <div className="promptStack">
            <article className="promptFile"><div className="promptFileTop"><span>FREE / 01</span><code>build & ship</code></div><h3>Code Review</h3><p>Evidence-ranked findings, severity, verification guidance, and an explicit ship recommendation.</p></article>
            <article className="promptFile"><div className="promptFileTop"><span>FREE / 02</span><code>build & ship</code></div><h3>Bug Diagnosis</h3><p>Observation ledger, ranked hypotheses, discriminating checks, and a clear boundary between symptom, mitigation, and cause.</p></article>
            <article className="promptFile"><div className="promptFileTop"><span>FREE / 03</span><code>research & decide</code></div><h3>Technical Decision</h3><p>Hard constraints, evidence quality, tradeoffs, reversibility, and a next validation action.</p></article>
          </div>
        </div>
      </section>

      <section className="section productSection" id="collections">
        <div className="wrap"><div className="productFrame">
          <div className="productFrameTop"><span className="productEdition">PROMPT MACHINE / COLLECTION 01</span><span className="releaseBadge"><i /> CANDIDATE · NOT FOR SALE</span></div>
          <div className="productFrameGrid">
            <div className="productMain"><div className="eyebrow">03 / PAID COLLECTIONS</div><h2>Pay for a broader system, not for the missing half of a free prompt.</h2><p>The first commercial experiment is the Developer Workflow Collection: four governed workflow families, installable skill candidates, operating contracts, examples, adaptation guidance, and visible evidence boundaries.</p><p className="sectionIntro">Planned launch price: <strong>$19 one-time</strong>. This is a pricing hypothesis, not an active checkout.</p></div>
            <aside className="purchasePanel"><span className="purchaseLabel">DEVELOPER COLLECTION</span><h3>Checkout stays off until the release earns it.</h3><p>Behavioral testing, prompt/skill parity, delivery evidence, and the commercial canary remain separate gates. We will not label them complete before they are observed.</p><Link className="btn btnSecondary" href="/developer-pack">Inspect collection status →</Link></aside>
          </div>
        </div></div>
      </section>

      <section className="section methodSection" id="how-it-works">
        <div className="wrap">
          <div className="sectionHeader splitHeader">
            <div><div className="eyebrow">04 / HOW IT WORKS</div><h2>The product is the workflow experience.</h2></div>
            <p className="sectionIntro">Downloads, ZIPs, skills, and prompts are delivery surfaces. The customer experience is finding the right workflow, applying it correctly, and knowing what to trust.</p>
          </div>
          <div className="pipeline">
            {howItWorks.map(([n, title, copy]) => <article className="pipelineStep" key={n}><div className="pipelineTop"><span>{n}</span><code>STEP {n}</code></div><h3>{title}</h3><p>{copy}</p></article>)}
          </div>
        </div>
      </section>

      <section className="section evidenceSection" id="evidence">
        <div className="wrap evidenceLayout"><div className="evidenceCopy"><div className="eyebrow">05 / TRUST</div><h2>Useful first. Claims second.</h2><p className="sectionIntro">Prompt Machine exposes compact evidence states while Prompt Quarry keeps the deeper engineering receipts. A packaged workflow does not become tested or certified just because it looks professional.</p><p className="evidenceRule">marketing claim <span>≤</span> observed evidence</p></div><div className="evidenceLadder"><div className="evidenceRow active"><span>VERSIONED</span><strong>Exact customer artifact</strong><em>VISIBLE</em></div><div className="evidenceRow active"><span>STRUCTURE</span><strong>Contract and integrity checks</strong><em>VISIBLE</em></div><div className="evidenceRow"><span>RUNTIME</span><strong>Real execution evidence</strong><em>WHEN EARNED</em></div><div className="evidenceRow"><span>CERTIFIED</span><strong>Repeated governed evidence</strong><em>WHEN EARNED</em></div></div></div>
      </section>

      <section className="cta premiumCta"><div className="ctaGridBackdrop" aria-hidden="true" /><div className="wrap premiumCtaInner"><div className="eyebrow">START WITH VALUE</div><h2>Try a workflow on a real task.<br /><span>Upgrade only when it earns a place in your work.</span></h2><div className="actions ctaActions"><CommerceLink kind="free" className="btn btnPrimary btnHero">Start Free <span>→</span></CommerceLink><Link className="btn btnGhost btnHero" href="/collections">Explore Collections</Link></div></div></section>
    </main>
  );
}
