import type { Metadata } from "next";
import Link from "next/link";

import { LibraryExplorer } from "@/components/library-explorer.client";
import {
  getPublicLibraryAssets,
  LIBRARY_COLLECTIONS
} from "@/lib/verlune-library-discovery";

export const metadata: Metadata = {
  title: "Library",
  description: "Browse Verlune prompts, workflows, Builders and toolkit assets by task, tier, type, category, or curated collection.",
  alternates: { canonical: "/library" }
};

export default function LibraryPage() {
  const assets = getPublicLibraryAssets();
  const freeCount = assets.filter((asset) => asset.tier === "free").length;
  const premiumCount = assets.filter((asset) => asset.tier === "premium").length;
  const promptCount = assets.filter((asset) => asset.type === "Prompt").length;

  return <main className="vLibraryPublic">
    <section className="vLibraryHero">
      <div className="wrap vLibraryHeroGrid">
        <div>
          <div className="eyebrow">VERLUNE LIBRARY</div>
          <h1>Find the work.<br /><em>Then use the structure.</em></h1>
          <p className="lead">Browse by the job you need to do—not by prompt-engineering vocabulary. Search all current Verlune assets, narrow the catalog, or start from a curated collection.</p>
          <div className="actions">
            <a className="btn btnPrimary" href="#library">Browse library <span aria-hidden="true">↓</span></a>
            <Link className="btn btnSecondary" href="/free">Start with Free</Link>
          </div>
        </div>
        <aside className="vLibraryStats" aria-label="Current Verlune library">
          <div><strong>{assets.length}</strong><span>assets</span></div>
          <div><strong>{promptCount}</strong><span>prompts</span></div>
          <div><strong>{freeCount}</strong><span>Free</span></div>
          <div><strong>{premiumCount}</strong><span>Premium</span></div>
        </aside>
      </div>
    </section>

    <section className="section vExplorerSection">
      <div className="wrap">
        <LibraryExplorer
          assets={assets}
          collections={LIBRARY_COLLECTIONS}
          initialCollectionId="start-here"
          heading="Start from the job, not the format."
          intro="Search all current Verlune assets. Tier tells you what you can open now; type tells you whether the job is best handled as a prompt, workflow, Builder or toolkit asset."
        />
      </div>
    </section>

    <section className="section vLibraryBoundary">
      <div className="wrap vTrustGrid">
        <div>
          <div className="eyebrow">DISCOVERY ≠ ACCESS</div>
          <h2>Browse everything.<br />Open what your tier includes.</h2>
        </div>
        <div className="vTrustPoints">
          <p><strong>Free assets open directly.</strong><span>The complete Free artifact is available without payment.</span></p>
          <p><strong>Premium metadata is public.</strong><span>Names and summaries help you evaluate the library; protected asset contents stay behind entitlement.</span></p>
          <p><strong>Structure checked is not certified.</strong><span>Catalog presence does not imply universal model compatibility or behavioral certification.</span></p>
        </div>
      </div>
    </section>
  </main>;
}
