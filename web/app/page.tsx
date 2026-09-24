import type { Metadata } from "next";
import Link from "next/link";
import { ArtifactMiniObject } from "@/components/verlune-visuals";
import { VerluneHeroScene } from "@/components/hero-v3/VerluneHeroScene";
import "@/components/hero-v3/hero-v3.css";

export const metadata: Metadata = {
  alternates: { canonical: "/" },
  title: "Structured AI work"
};

const categories = [
  ["Development & Tech", "Requirements, code review, debugging and technical work."],
  ["Study & Learning", "Preparation, guided study and durable understanding."],
  ["Research & Analysis", "Evidence, synthesis, scope control and bounded conclusions."],
  ["Business & Operations", "Decisions, SOPs, processes and recurring operational work."],
  ["Writing & Communication", "Audience-aware writing with factual boundaries."],
  ["Content & Marketing", "Strategy grounded in evidence, hypotheses and review loops."],
  ["Planning & Productivity", "Projects with dependencies, risks and validation."],
  ["Career & Job Search", "Role preparation without fabricated experience."],
] as const;

const process = [
  ["Find", "Choose the job you need."],
  ["Copy", "Take the complete structured asset."],
  ["Run", "Paste it into your compatible AI assistant."],
  ["Verify", "Use the asset's checks and boundaries."],
  ["Reuse", "Change the per-run input and run it again."],
] as const;

export default function HomePage() {
  return <main className="v2Home">
    <section className="v2Hero">
      <div className="wrap v2HeroGrid">
        <div className="v2HeroCopy">
          <div className="eyebrow">STRUCTURED AI WORK</div>
          <h1>Use ours.<br /><em>Build yours.</em><br />Work better with AI.</h1>
          <p className="lead">Verlune is a library and toolkit for structured AI work: reusable prompts, workflows and Builders that you run in your own compatible AI assistant.</p>
          <div className="actions">
            <Link className="btn btnPrimary" href="/free">Explore free <span aria-hidden="true">→</span></Link>
            <Link className="btn btnSecondary" href="/unlock">Premium access</Link>
          </div>
        </div>
        <div className="v2HeroVisual">
          <VerluneHeroScene />
        </div>
        <div className="vHeroProof" aria-label="What Verlune provides">
          <span><b>Prompts</b><small>bounded tasks</small></span>
          <span><b>Workflows</b><small>recurring processes</small></span>
          <span><b>Builders</b><small>your own reusable work</small></span>
        </div>
      </div>
    </section>

    <section className="vProcessBand">
      <div className="wrap">
        <div className="vProcessLabel"><span>FROM INPUT TO REUSE</span><small>A repeatable way to work with AI.</small></div>
        <ol className="vProcessRail">
          {process.map(([title, text], index) => <li key={title}>
            <span className="vProcessNumber">{String(index + 1).padStart(2, "0")}</span>
            <div><strong>{title}</strong><small>{text}</small></div>
            {index < process.length - 1 ? <span className="vProcessArrow" aria-hidden="true">→</span> : null}
          </li>)}
        </ol>
      </div>
    </section>

    <section className="section vCapabilitySection">
      <div className="wrap">
        <div className="splitHeader">
          <div><div className="eyebrow">USE OURS / BUILD YOURS</div><h2>Two paths.<br />One structured system.</h2></div>
          <p className="sectionIntro">Start with a ready-made asset, or turn your own recurring work into something reusable. Verlune keeps the boundary between the two explicit.</p>
        </div>
        <div className="vCapabilityGrid">
          <article className="vCapabilityCard">
            <div className="vCapabilityIcon"><ArtifactMiniObject type="Prompt" /></div>
            <div className="eyebrow">USE OURS</div>
            <h3>Start with a structured asset.</h3>
            <p>Choose a Prompt or Workflow, run it with your own context, verify the result, then reuse the same structure on the next task.</p>
            <Link className="textLink" href="/free">Explore free assets →</Link>
          </article>
          <article className="vCapabilityCard vCapabilityCardAccent">
            <div className="vCapabilityIcon"><ArtifactMiniObject type="Builder" /></div>
            <div className="eyebrow">BUILD YOURS</div>
            <h3>Turn recurring work into a reusable system.</h3>
            <p>Prompt Builder and Workflow Builder guide you from an ordinary-language need to a reusable artifact without requiring prompt-engineering vocabulary.</p>
            <Link className="textLink" href="/unlock">Explore Premium Builders →</Link>
          </article>
        </div>
      </div>
    </section>

    <section className="section vTaxonomySection">
      <div className="wrap">
        <div className="splitHeader">
          <div><div className="eyebrow">PROMPT ≠ WORKFLOW</div><h2>Different jobs need<br />different structure.</h2></div>
          <p className="sectionIntro">A Prompt handles a bounded task. A Workflow governs a recurring process with stages, decisions, fallback or verification where those things materially matter.</p>
        </div>
        <div className="vTaxonomyGrid">
          <article className="vTaxonomyCard">
            <div className="vTaxonomyTop"><span>PROMPT</span><ArtifactMiniObject type="Prompt" /></div>
            <h3>One bounded job.</h3>
            <div className="vInlineFlow"><span>INPUT</span><b>→</b><span>INSTRUCTION</span><b>→</b><span>OUTPUT</span><b>→</b><span>CHECK</span></div>
            <p>Reusable instructions for tasks such as rewriting, analysis, planning or preparation.</p>
          </article>
          <article className="vTaxonomyCard vTaxonomyWorkflow">
            <div className="vTaxonomyTop"><span>WORKFLOW</span><ArtifactMiniObject type="Workflow" /></div>
            <h3>A process with state.</h3>
            <div className="vWorkflowDiagram" aria-label="Trigger to stages, decision, fallback and verification">
              <span>TRIGGER</span><b>→</b><span>STAGE</span><b>→</b><span>DECISION</span><b>→</b><span>VERIFY</span>
              <i>↘ FALLBACK</i>
            </div>
            <p>Use when the task has stages, uncertainty, recurring decisions or a meaningful fallback path.</p>
          </article>
        </div>
      </div>
    </section>

    <section className="section vBrowseSection">
      <div className="wrap">
        <div className="vBrowseHeading">
          <div><div className="eyebrow">EXPLORE THE LIBRARY</div><h2>Structured work across real categories.</h2></div>
          <Link className="textLink" href="/unlock">Open Premium access →</Link>
        </div>
        <div className="vCategoryGrid">
          {categories.map(([name, summary], index) => <article className="vCategoryCard" key={name}>
            <span className="vCategoryIndex">{String(index + 1).padStart(2, "0")}</span>
            <div><h3>{name}</h3><p>{summary}</p></div>
            <span className="vCategoryArrow" aria-hidden="true">↗</span>
          </article>)}
        </div>
      </div>
    </section>

    <section className="section vTrustSection">
      <div className="wrap vTrustGrid">
        <div>
          <div className="eyebrow">STRUCTURE WITHOUT THE MAGIC ACT</div>
          <h2>Clear inputs.<br />Visible boundaries.</h2>
        </div>
        <div className="vTrustPoints">
          <p><strong>Your AI supplies the compute.</strong><span>Verlune does not sell hosted AI credits.</span></p>
          <p><strong>Generated is not certified.</strong><span>Builders create reusable artifacts; certification requires separate evidence.</span></p>
          <p><strong>Verification stays visible.</strong><span>Good output is something you can inspect, not just something that sounds polished.</span></p>
        </div>
      </div>
    </section>

    <section className="v2Closing">
      <div className="wrap v2ClosingInner">
        <div><div className="eyebrow">VERLUNE</div><h2>Use ours. Build yours.</h2><p>Start with something useful now. Keep the structure when the input changes.</p></div>
        <div className="actions"><Link className="btn btnPrimary" href="/free">Explore free →</Link><Link className="btn btnSecondary" href="/unlock">Premium access</Link></div>
      </div>
    </section>
  </main>;
}
