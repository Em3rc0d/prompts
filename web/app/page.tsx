import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";
import { QuarryEngine } from "@/components/quarry-engine";

const pipeline = [
  ["01", "RAW → BRIEF", "Shape the task", "Make purpose, context, constraints, risk, and output expectations explicit."],
  ["02", "BRIEF → ASSET", "Engineer the workflow", "Turn a vague request into a reusable operating contract instead of clever wording."],
  ["03", "ASSET → VALID", "Guard the evidence", "Separate observation, inference, unknowns, and claims before packaging anything."],
  ["04", "VALID → PRODUCT", "Ship a governed artifact", "Version, fingerprint, license, deliver, and verify the customer-visible release."],
];

export default function HomePage() {
  return (
    <main>
      <section className="hero heroPremium">
        <div className="heroGridBackdrop" aria-hidden="true" />
        <div className="heroGlow heroGlowOne" aria-hidden="true" />
        <div className="wrap heroPremiumGrid">
          <div className="heroCopy">
            <div className="heroKicker"><span className="signalDot" />PROMPT QUARRY / DEVELOPER SYSTEM</div>
            <h1>Stop collecting random prompts.</h1>
            <p className="heroStatement">Build repeatable AI workflows with explicit context, constraints, output contracts, and evidence boundaries.</p>
            <div className="actions heroActions">
              <CommerceLink kind="free" className="btn btnPrimary btnHero">Get the Free Pack v1.1 <span>→</span></CommerceLink>
              <Link className="btn btnGhost btnHero" href="/developer-pack">Developer Pack status</Link>
            </div>
            <div className="heroProof">
              <div><strong>v1.1</strong><span>free release</span></div>
              <div><strong>03</strong><span>field-ready workflows</span></div>
              <div><strong>SHA-256</strong><span>runtime verified</span></div>
              <div><strong>HOLD</strong><span>paid pack hardening</span></div>
            </div>
            <p className="trust heroTrust"><span>◆</span> Built is not the same as proven. not observed == unknown.</p>
          </div>
          <QuarryEngine />
        </div>
      </section>

      <section className="section methodSection" id="method">
        <div className="wrap">
          <div className="sectionHeader splitHeader">
            <div><div className="eyebrow">01 / METHOD</div><h2>A prompt factory, not a prompt dump.</h2></div>
            <p className="sectionIntro">Prompt Quarry treats prompts as engineered artifacts: specify the task, govern evidence, package the result, and prove only what was actually observed.</p>
          </div>
          <div className="pipeline">
            {pipeline.map(([n, code, title, copy]) => <article className="pipelineStep" key={n}><div className="pipelineTop"><span>{n}</span><code>{code}</code></div><h3>{title}</h3><p>{copy}</p></article>)}
          </div>
          <div className="methodManifest"><div className="manifestLabel">OPERATING PRINCIPLE</div><p>AI proposes <span>/</span> Human decides <span>/</span> System executes <span>/</span> System proves</p></div>
        </div>
      </section>

      <section className="section freeSection" id="free">
        <div className="wrap freeLayout">
          <div className="freeCopy">
            <div className="eyebrow">02 / START FREE</div>
            <h2>Three workflows you can use on real work today.</h2>
            <p className="sectionIntro">Code Review, Bug Diagnosis, and Technical Decision include evidence labels, explicit processes, output contracts, fallbacks, and verification guidance.</p>
            <div className="actions"><CommerceLink kind="free" className="btn btnPrimary btnHero">Download v1.1 <span>→</span></CommerceLink></div>
            <p className="micro">7 customer files · 23,498 bytes · canonical SHA-256 verified before delivery</p>
          </div>
          <div className="promptStack">
            <article className="promptFile"><div className="promptFileTop"><span>PQ / 01</span><code>software</code></div><h3>Code Review</h3><p>Evidence-ranked findings, severity, verification, and an explicit ship decision.</p></article>
            <article className="promptFile"><div className="promptFileTop"><span>PQ / 02</span><code>debugging</code></div><h3>Bug Diagnosis</h3><p>Observation ledger, ranked hypotheses, discriminating checks, and fix status.</p></article>
            <article className="promptFile"><div className="promptFileTop"><span>PQ / 03</span><code>decision</code></div><h3>Technical Decision</h3><p>Hard constraints, evidence ledger, tradeoffs, reversibility, and decision status.</p></article>
          </div>
        </div>
      </section>

      <section className="section productSection" id="developer-pack">
        <div className="wrap"><div className="productFrame">
          <div className="productFrameTop"><span className="productEdition">PROMPT QUARRY / DEVELOPER PACK</span><span className="releaseBadge"><i /> DRAFT · v1.1 · NOT FOR SALE</span></div>
          <div className="productFrameGrid">
            <div className="productMain"><div className="eyebrow">03 / THE SYSTEM</div><h2>The paid pack is earning the upgrade.</h2><p>The next release is being hardened around reusable operating contracts, configurable policies, machine-readable schemas, team adaptation, worked transformations, and commercial value gates.</p></div>
            <aside className="purchasePanel"><span className="purchaseLabel">COMMERCIAL STATUS</span><h3>Checkout intentionally disabled.</h3><p>We will not sell until the v1.1 candidate, fingerprint, approval, delivery path, and Golden Path gates are observed.</p><Link className="btn btnSecondary" href="/developer-pack">Inspect status →</Link></aside>
          </div>
        </div></div>
      </section>

      <section className="section evidenceSection">
        <div className="wrap evidenceLayout"><div className="evidenceCopy"><div className="eyebrow">04 / EVIDENCE</div><h2>Every claim has a gate.</h2><p className="sectionIntro">The Free Pack delivery artifact is observed. Behavioral superiority, certification, portability, and paid-market validation remain separate evidence problems.</p><p className="evidenceRule">not observed <span>==</span> unknown</p></div><div className="evidenceLadder"><div className="evidenceRow active"><span>DELIVERY</span><strong>Free v1.1 integrity</strong><em>OBSERVED</em></div><div className="evidenceRow"><span>TESTED</span><strong>Behavioral F4</strong><em>SEPARATE GATE</em></div><div className="evidenceRow"><span>IMPROVED</span><strong>Comparative F5</strong><em>SEPARATE GATE</em></div><div className="evidenceRow"><span>CERTIFIED</span><strong>Repeated F6</strong><em>SEPARATE GATE</em></div></div></div>
      </section>

      <section className="cta premiumCta"><div className="ctaGridBackdrop" aria-hidden="true" /><div className="wrap premiumCtaInner"><div className="eyebrow">ENTER THE QUARRY</div><h2>Start with evidence.<br /><span>Upgrade when the system earns it.</span></h2><div className="actions ctaActions"><CommerceLink kind="free" className="btn btnPrimary btnHero">Get Free Pack v1.1 <span>→</span></CommerceLink><Link className="btn btnGhost btnHero" href="/developer-pack">Paid release status</Link></div></div></section>
    </main>
  );
}
