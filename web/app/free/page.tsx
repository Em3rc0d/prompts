import type { Metadata } from "next";
import Link from "next/link";

import { CommerceLink } from "@/components/commerce-link";
import { LibraryExplorer } from "@/components/library-explorer.client";
import { ArtifactMiniObject } from "@/components/verlune-visuals";
import {
  getFreeLibraryDiscoveryAssets,
  LIBRARY_COLLECTIONS
} from "@/lib/verlune-library-discovery";

export const metadata: Metadata = {
  title: "Free Library",
  description: "Useful standalone Verlune prompts and workflows across development, study, research, business, writing, content, planning, and career work.",
  alternates: { canonical: "/free" }
};

export default function FreePage() {
  const assets = getFreeLibraryDiscoveryAssets();
  const prompts = assets.filter((asset) => asset.type === "Prompt");
  const workflows = assets.filter((asset) => asset.type === "Workflow");

  return <main className="vFreeLibrary">
    <section className="vFreeHero">
      <div className="wrap vFreeHeroGrid">
        <div>
          <div className="eyebrow">VERLUNE FREE</div>
          <h1>Useful before<br />you pay anything.</h1>
          <p className="lead">Start with complete, reusable assets across real categories. Free is not a crippled demo: choose a task, run it in your compatible AI assistant, verify the result, and reuse the structure.</p>
          <div className="actions">
            <a className="btn btnPrimary" href="#library">Find a Free asset <span aria-hidden="true">↓</span></a>
            <Link className="btn btnSecondary" href="/library">Browse all 60 assets</Link>
          </div>
          <p className="micro">{assets.length} complete Free assets: {prompts.length} prompts and {workflows.length} workflows.</p>
        </div>
        <div className="vFreeHeroVisual" aria-label="Free prompts and workflows">
          <div className="vFreeObject vFreeObjectPrompt"><ArtifactMiniObject type="Prompt" /><span>PROMPTS</span></div>
          <div className="vFreeObject vFreeObjectWorkflow"><ArtifactMiniObject type="Workflow" /><span>WORKFLOWS</span></div>
          <div className="vFreeConnector" aria-hidden="true" />
        </div>
      </div>
    </section>

    <section className="vProcessBand">
      <div className="wrap">
        <div className="vProcessLabel"><span>NO PROMPT-ENGINEERING VOCABULARY REQUIRED</span><small>Bring your task. Keep the verification visible.</small></div>
        <ol className="vProcessRail">
          {[
            ["Choose", "Pick the task closest to your real need."],
            ["Copy", "Take the complete asset."],
            ["Run", "Use it in your AI assistant."],
            ["Check", "Inspect facts, assumptions and boundaries."],
            ["Reuse", "Swap the per-run input next time."]
          ].map(([title,text],index)=><li key={title}><span className="vProcessNumber">{String(index+1).padStart(2,"0")}</span><div><strong>{title}</strong><small>{text}</small></div>{index<4?<span className="vProcessArrow" aria-hidden="true">→</span>:null}</li>)}
        </ol>
      </div>
    </section>

    <section className="section vExplorerSection">
      <div className="wrap">
        <LibraryExplorer
          assets={assets}
          collections={LIBRARY_COLLECTIONS}
          fixedTier="free"
          initialCollectionId="start-here"
          heading="Find a Free asset by the job."
          intro="Search nineteen complete Free assets, narrow by type or category, or start from a curated collection."
        />
      </div>
    </section>

    <section className="section vDeveloperResource">
      <div className="wrap">
        <div className="productFrame"><div className="productFrameGrid">
          <div className="productMain">
            <div className="eyebrow">DEVELOPMENT & TECH / DOWNLOAD</div>
            <h2>Prefer a developer starter ZIP?</h2>
            <p>The governed developer starter pack remains available as a separate download for code-focused work. It is a delivery option for that developer resource, not the definition of the broader Free Library.</p>
          </div>
          <aside className="purchasePanel">
            <span className="purchaseLabel">DEVELOPER RESOURCE</span>
            <h3>Starter ZIP</h3>
            <p>Use the web library for the full nineteen-asset Verlune Free library, or download the existing developer starter archive.</p>
            <CommerceLink kind="free">Download developer starter ZIP ↓</CommerceLink>
          </aside>
        </div></div>
      </div>
    </section>

    <section className="section vFreeBoundary">
      <div className="wrap vTrustGrid">
        <div><div className="eyebrow">FREE ≠ THROWAWAY</div><h2>Standalone value.<br />Same truth boundary.</h2></div>
        <div className="vTrustPoints">
          <p><strong>Complete assets.</strong><span>Each free item is intended to be useful on its own, not artificially crippled to force an upgrade.</span></p>
          <p><strong>No universal model claim.</strong><span>Behavior can vary by assistant and model. Verify important outputs instead of assuming equivalence.</span></p>
          <p><strong>Premium adds capability.</strong><span>Builders, deeper workflows, adaptation, evaluation, and protected library access—not just longer prompts.</span></p>
        </div>
      </div>
    </section>

    <section className="v2Closing">
      <div className="wrap v2ClosingInner">
        <div><div className="eyebrow">READY FOR MORE STRUCTURE?</div><h2>Use ours. Build yours.</h2><p>Premium adds Builders, deeper workflows, adaptation, and evaluation tools.</p></div>
        <div className="actions"><Link className="btn btnPrimary" href="/premium">Explore Premium →</Link><Link className="btn btnSecondary" href="/library">Browse Library</Link></div>
      </div>
    </section>
  </main>;
}
