import type { Metadata } from "next";
import Link from "next/link";
import { CommerceLink } from "@/components/commerce-link";
import { ArtifactMiniObject } from "@/components/verlune-visuals";
import { FREE_ASSETS } from "@/lib/verlune-free-catalog";

export const metadata: Metadata = {
  title: "Free Library",
  description: "Useful standalone Verlune prompts and workflows across development, study, research, business, writing, content, planning, and career work.",
  alternates: { canonical: "/free" }
};

export default function FreePage() {
  const prompts = FREE_ASSETS.filter((asset) => asset.type === "Prompt");
  const workflows = FREE_ASSETS.filter((asset) => asset.type === "Workflow");

  return <main className="vFreeLibrary">
    <section className="vFreeHero">
      <div className="wrap vFreeHeroGrid">
        <div>
          <div className="eyebrow">VERLUNE FREE</div>
          <h1>Useful before<br />you pay anything.</h1>
          <p className="lead">Start with complete, reusable assets across real categories. Free is not a crippled demo: choose a task, run it in your compatible AI assistant, verify the result, and reuse the structure.</p>
          <div className="actions">
            <a className="btn btnPrimary" href="#free-assets">Explore free assets <span aria-hidden="true">↓</span></a>
            <CommerceLink kind="free">Download developer starter ZIP <span aria-hidden="true">↓</span></CommerceLink>
          </div>
          <p className="micro">The ZIP is the existing governed developer starter pack. The web library below exposes the broader Verlune v1 free launch-core assets individually.</p>
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

    <section className="section" id="free-assets">
      <div className="wrap">
        <div className="vLibraryGroupHeader">
          <div><div className="eyebrow">FREE PROMPTS</div><h2>Bounded tasks across eight categories.</h2></div>
          <span className="assetCount">{prompts.length} prompts</span>
        </div>
        <div className="vFreePromptGrid">
          {prompts.map((asset)=><article className="vFreeAssetCard" key={asset.id}>
            <div className="vFreeAssetVisual"><ArtifactMiniObject type="Prompt" /></div>
            <div className="assetCardMeta"><span>{asset.categoryLabel}</span><span>{asset.id}</span></div>
            <h3>{asset.name}</h3>
            <p>{asset.summary}</p>
            <Link className="textLink" href={`/free/asset/${encodeURIComponent(asset.id)}`}>Open free prompt →</Link>
          </article>)}
        </div>
      </div>
    </section>

    <section className="section vFreeWorkflowSection">
      <div className="wrap">
        <div className="vLibraryGroupHeader">
          <div><div className="eyebrow">FREE WORKFLOWS</div><h2>Use a process when one prompt is not enough.</h2></div>
          <span className="assetCount">{workflows.length} workflows</span>
        </div>
        <div className="vFreeWorkflowGrid">
          {workflows.map((asset)=><article className="vFreeWorkflowCard" key={asset.id}>
            <div className="vFreeWorkflowVisual"><ArtifactMiniObject type="Workflow" /></div>
            <div className="assetCardMeta"><span>{asset.categoryLabel}</span><span>{asset.id}</span></div>
            <h3>{asset.name}</h3>
            <p>{asset.summary}</p>
            <div className="vWorkflowMiniMap" aria-hidden="true"><span>START</span><i/><span>STAGES</span><i/><span>VERIFY</span></div>
            <Link className="textLink" href={`/free/asset/${encodeURIComponent(asset.id)}`}>Open free workflow →</Link>
          </article>)}
        </div>
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
        <div className="actions"><Link className="btn btnPrimary" href="/unlock">Premium access →</Link><Link className="btn btnSecondary" href="/">Back to Verlune</Link></div>
      </div>
    </section>
  </main>;
}
