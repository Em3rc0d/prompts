import type { Metadata } from "next";
import Link from "next/link";

import { LibraryExplorer } from "@/components/library-explorer.client";
import { VerluneGraph } from "@/components/verlune-visuals";
import { requirePremiumSession } from "@/lib/verlune-auth.server";
import {
  getPremiumLibraryDiscoveryAssets,
  LIBRARY_COLLECTIONS
} from "@/lib/verlune-library-discovery";

export const metadata: Metadata = {
  title: "Premium Library",
  robots: { index: false, follow: false }
};

export const dynamic = "force-dynamic";

export default async function PremiumLibraryPage() {
  await requirePremiumSession("/app");

  const assets = getPremiumLibraryDiscoveryAssets();
  const prompts = assets.filter((asset) => asset.type === "Prompt");
  const workflows = assets.filter((asset) => asset.type === "Workflow");
  const builders = assets.filter((asset) => asset.type === "Builder");
  const toolkit = assets.filter((asset) => asset.type === "Toolkit");

  return <main className="premiumApp vPremiumLibrary">
    <section className="vPremiumHero">
      <div className="wrap vPremiumHeroGrid">
        <div>
          <div className="eyebrow">VERLUNE PREMIUM</div>
          <h1>Use ours.<br /><em>Build yours.</em></h1>
          <p className="lead">Search the protected library by the job you need, open a structured asset, or use a Builder to turn recurring work into something reusable.</p>
          <div className="actions">
            <a className="btn btnPrimary" href="#library">Find an asset <span aria-hidden="true">↓</span></a>
            <Link className="btn btnSecondary" href="/app/access">Access settings</Link>
          </div>
          <p className="micro">{assets.length} Premium assets: {prompts.length} prompts, {workflows.length} workflows, {builders.length} Builders and {toolkit.length} toolkit assets.</p>
        </div>
        <VerluneGraph variant="library" label="Premium library with prompts, workflows, Builders and toolkits connected around a structured Verlune core" />
      </div>
      <div className="wrap">
        <ol className="vProcessRail vProcessRailPremium" aria-label="How to use Verlune Premium">
          {[
            ["Find", "Search by the job you need."],
            ["Open", "Choose the complete asset."],
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

    <section className="section vExplorerSection">
      <div className="wrap">
        <LibraryExplorer
          assets={assets}
          collections={LIBRARY_COLLECTIONS}
          fixedTier="premium"
          initialCollectionId="premium-essentials"
          heading="Find the Premium capability you need."
          intro="Search the protected Premium library, narrow by asset type or category, or begin with a curated collection. Every result opens the complete entitled asset."
        />
      </div>
    </section>
  </main>;
}
