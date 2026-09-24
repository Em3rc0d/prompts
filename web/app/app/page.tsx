import type { Metadata } from "next";
import Link from "next/link";

import { ArtifactMiniObject, VerluneGraph } from "@/components/verlune-visuals";
import { requirePremiumSession } from "@/lib/verlune-auth.server";
import { PREMIUM_ASSETS } from "@/lib/verlune-premium-catalog";

export const metadata: Metadata = {
  title: "Premium Library",
  robots: { index: false, follow: false }
};

export const dynamic = "force-dynamic";

export default async function PremiumLibraryPage() {
  await requirePremiumSession("/app");

  const builders = PREMIUM_ASSETS.filter((asset) => asset.type === "Builder");
  const workflows = PREMIUM_ASSETS.filter((asset) => asset.type === "Workflow");
  const prompts = PREMIUM_ASSETS.filter((asset) => asset.type === "Prompt");
  const toolkit = PREMIUM_ASSETS.filter((asset) => asset.type === "Toolkit");

  return <main className="premiumApp vPremiumLibrary">
    <section className="vPremiumHero">
      <div className="wrap vPremiumHeroGrid">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM</div>
          <h1>Use ours.<br /><em>Build yours.</em></h1>
          <p className="lead">Choose a structured prompt or workflow, copy it into your AI assistant, or start with a Builder to create something reusable for your own recurring work.</p>
          <div className="actions">
            <a className="btn btnPrimary" href="#builders">Start with a Builder <span aria-hidden="true">→</span></a>
            <Link className="btn btnSecondary" href="/app/access">Access settings</Link>
          </div>
        </div>
        <VerluneGraph variant="library" label="Premium library with prompts, workflows, Builders and toolkits connected around a structured Verlune core" />
      </div>
      <div className="wrap">
        <ol className="vProcessRail vProcessRailPremium" aria-label="How to use Verlune Premium">
          {[
            ["Find", "Choose the job you need."],
            ["Copy", "Take the complete asset."],
            ["Run", "Paste it into your AI."],
            ["Verify", "Use the built-in checks."],
            ["Reuse", "Change the per-run input."]
          ].map(([title, text], index) => <li key={title}>
            <span className="vProcessNumber">{String(index + 1).padStart(2, "0")}</span>
            <div><strong>{title}</strong><small>{text}</small></div>
            {index < 4 ? <span className="vProcessArrow" aria-hidden="true">→</span> : null}
          </li>)}
        </ol>
      </div>
    </section>

    <section className="section vLibrarySection">
      <div className="wrap vLibraryLayout">
        <aside className="vCategoryRail" aria-label="Premium library sections">
          <div className="vCategoryRailTitle">Sections</div>
          <a href="#builders"><span>Build Yours</span><small>{builders.length}</small></a>
          <a href="#workflows"><span>Workflows</span><small>{workflows.length}</small></a>
          <a href="#prompts"><span>Prompts</span><small>{prompts.length}</small></a>
          <a href="#toolkit"><span>Adapt & Evaluate</span><small>{toolkit.length}</small></a>
          <div className="vTypeKey">
            <span>BROWSE MODEL</span>
            <small>Sections navigate by asset type.</small>
            <small>Category labels remain visible on each asset.</small>
          </div>
        </aside>

        <div className="vLibraryMain">
          <section className="vLibraryGroup" id="builders">
            <div className="vLibraryGroupHeader">
              <div><div className="eyebrow">BUILD YOURS</div><h2>Start from your own recurring work.</h2></div>
              <span className="assetCount">{builders.length} Builders</span>
            </div>
            <div className="vBuilderGrid">
              {builders.map((asset) => <article className="vBuilderFeature" key={asset.id}>
                <div className="vBuilderContent">
                  <div className="assetCardMeta"><span>{asset.type}</span><span>{asset.id}</span></div>
                  <h3>{asset.name}</h3>
                  <p>{asset.summary}</p>
                  <div className="vMiniPipeline" aria-hidden="true">
                    <span>NEED</span><b>→</b><span>INTAKE</span><b>→</b><span>ARTIFACT</span><b>→</b><span>TEST</span>
                  </div>
                  <Link className="textLink" href={`/app/asset/${encodeURIComponent(asset.id)}`}>Open Builder →</Link>
                </div>
                <ArtifactMiniObject type="Builder" />
              </article>)}
            </div>
          </section>

          <section className="vLibraryGroup" id="workflows">
            <div className="vLibraryGroupHeader">
              <div><div className="eyebrow">WORKFLOWS</div><h2>Processes with stages, decisions and verification.</h2></div>
              <span className="assetCount">{workflows.length} workflows</span>
            </div>
            <div className="vWorkflowFeatureGrid">
              {workflows.map((asset) => <article className="vWorkflowFeature" key={asset.id}>
                <div className="vArtifactVisual"><ArtifactMiniObject type="Workflow" /></div>
                <div className="assetCardMeta"><span>{asset.categoryLabel}</span><span>{asset.id}</span></div>
                <h3>{asset.name}</h3>
                <p>{asset.summary}</p>
                <div className="vWorkflowMiniMap" aria-hidden="true"><span>TRIGGER</span><i /><span>STAGE</span><i /><span>VERIFY</span></div>
                <Link className="textLink" href={`/app/asset/${encodeURIComponent(asset.id)}`}>Open workflow →</Link>
              </article>)}
            </div>
          </section>

          <section className="vLibraryGroup" id="prompts">
            <div className="vLibraryGroupHeader">
              <div><div className="eyebrow">PROMPTS</div><h2>Bounded tasks with explicit inputs and checks.</h2></div>
              <span className="assetCount">{prompts.length} prompts</span>
            </div>
            <div className="vPromptList">
              {prompts.map((asset) => <article className="vPromptRow" id={asset.category} key={asset.id}>
                <div className="vPromptGlyph"><ArtifactMiniObject type="Prompt" /></div>
                <div className="vPromptRowBody">
                  <div className="assetCardMeta"><span>{asset.categoryLabel}</span><span>{asset.id}</span></div>
                  <h3>{asset.name}</h3>
                  <p>{asset.summary}</p>
                </div>
                <Link className="vRoundLink" aria-label={`Open ${asset.name}`} href={`/app/asset/${encodeURIComponent(asset.id)}`}>→</Link>
              </article>)}
            </div>
          </section>

          <section className="vLibraryGroup" id="toolkit">
            <div className="vLibraryGroupHeader">
              <div><div className="eyebrow">ADAPT & EVALUATE</div><h2>Keep structure when the context changes.</h2></div>
              <span className="assetCount">{toolkit.length} toolkit assets</span>
            </div>
            <div className="vToolkitGrid">
              {toolkit.map((asset) => <article className="vToolkitCard" key={asset.id}>
                <ArtifactMiniObject type="Toolkit" />
                <div><div className="assetCardMeta"><span>{asset.type}</span><span>{asset.id}</span></div><h3>{asset.name}</h3><p>{asset.summary}</p><Link className="textLink" href={`/app/asset/${encodeURIComponent(asset.id)}`}>Open toolkit →</Link></div>
              </article>)}
            </div>
          </section>
        </div>
      </div>
    </section>
  </main>;
}
