import type { Metadata } from "next";
import Link from "next/link";

import { requirePremiumSession } from "@/lib/verlune-auth.server";
import {
  PREMIUM_ASSETS,
  PREMIUM_CATEGORY_ORDER
} from "@/lib/verlune-premium-catalog";

export const metadata: Metadata = {
  title: "Premium Library",
  robots: { index: false, follow: false }
};

export const dynamic = "force-dynamic";

export default async function PremiumLibraryPage() {
  await requirePremiumSession("/app");

  return <main className="premiumApp">
    <section className="appHero">
      <div className="wrap">
        <div className="appTopline">
          <div>
            <div className="eyebrow">VERLUNE PREMIUM</div>
            <h1>Use ours. Build yours.</h1>
            <p className="lead">Choose a structured prompt or workflow, copy it into your AI assistant, or start with a Builder to create something reusable for your own recurring work.</p>
          </div>
          <Link className="btn btnSecondary" href="/app/access">Access settings</Link>
        </div>
        <ol className="appHowTo" aria-label="How to use Verlune Premium">
          <li><span>01</span><strong>Find</strong><small>Choose the job you need.</small></li>
          <li><span>02</span><strong>Copy</strong><small>Copy the complete asset.</small></li>
          <li><span>03</span><strong>Run</strong><small>Paste it into your AI.</small></li>
          <li><span>04</span><strong>Verify</strong><small>Use the asset's checks.</small></li>
          <li><span>05</span><strong>Reuse</strong><small>Change the per-run input.</small></li>
        </ol>
      </div>
    </section>

    <section className="section">
      <div className="wrap">
        {PREMIUM_CATEGORY_ORDER.map((category) => {
          const assets = PREMIUM_ASSETS.filter((asset) => asset.category === category);
          if (!assets.length) return null;
          return <section className="appCategory" key={category}>
            <div className="appCategoryHeading">
              <div>
                <div className="eyebrow">{assets[0].categoryLabel.toUpperCase()}</div>
                <h2>{category === "builders" ? "Start from your own recurring work." : assets[0].categoryLabel}</h2>
              </div>
              <span className="assetCount">{assets.length} {assets.length === 1 ? "asset" : "assets"}</span>
            </div>
            <div className="assetGrid">
              {assets.map((asset) => <article className={`assetCard assetCard${asset.type}`} key={asset.id}>
                <div className="assetCardMeta"><span>{asset.type}</span><span>{asset.id}</span></div>
                <h3>{asset.name}</h3>
                <p>{asset.summary}</p>
                <Link className="textLink" href={`/app/asset/${encodeURIComponent(asset.id)}`}>
                  Open asset →
                </Link>
              </article>)}
            </div>
          </section>;
        })}
      </div>
    </section>
  </main>;
}
