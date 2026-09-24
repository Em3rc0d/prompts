import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { CopyPremiumAsset } from "@/components/copy-premium-asset";
import { ArtifactMiniObject, AssetStructureMap } from "@/components/verlune-visuals";
import { requirePremiumSession } from "@/lib/verlune-auth.server";
import { readPremiumAsset } from "@/lib/verlune-premium-assets.server";
import { getPremiumAssetMeta, PREMIUM_ASSETS } from "@/lib/verlune-premium-catalog";

export const dynamic = "force-dynamic";

function customerVisibleContent(source: string): string {
  return source
    .split("\n")
    .filter((line) => !/^Status:\s+`/.test(line))
    .join("\n")
    .replace(/\n{3,}/g, "\n\n");
}

export async function generateMetadata({
  params
}: {
  params: Promise<{ assetId: string }>;
}): Promise<Metadata> {
  const { assetId } = await params;
  const meta = getPremiumAssetMeta(assetId);
  return {
    title: meta?.name ?? "Premium Asset",
    robots: { index: false, follow: false }
  };
}

export default async function PremiumAssetPage({
  params
}: {
  params: Promise<{ assetId: string }>;
}) {
  const { assetId } = await params;
  const meta = getPremiumAssetMeta(assetId);
  if (!meta) notFound();

  const nextPath = `/app/asset/${encodeURIComponent(assetId)}`;
  await requirePremiumSession(nextPath);

  let asset: Awaited<ReturnType<typeof readPremiumAsset>>;
  try {
    asset = await readPremiumAsset(assetId);
  } catch {
    notFound();
  }

  const related = PREMIUM_ASSETS
    .filter((item) => item.id !== assetId && (item.category === asset.meta.category || item.type === asset.meta.type))
    .slice(0, 3);

  return <main className="premiumApp vAssetDetail">
    <section className="vAssetHero">
      <div className="wrap">
        <Link className="textLink vBackLink" href="/app">← Back to Premium Library</Link>
        <div className="vAssetHeroGrid">
          <div className="vAssetHeroCopy">
            <div className="assetCardMeta vAssetMetaTop"><span>{asset.meta.type}</span><span>{asset.meta.categoryLabel}</span><span>{asset.meta.id}</span></div>
            <h1>{asset.meta.name}</h1>
            <p className="lead">{asset.meta.summary}</p>
            <div className="actions"><CopyPremiumAsset content={asset.content} /><a className="btn btnSecondary" href="#full-asset">Read full asset</a></div>
            <p className="micro">Runs in your compatible AI assistant. Verlune supplies the structure and methodology.</p>
          </div>
          <div className="vAssetVisualPanel">
            <ArtifactMiniObject type={asset.meta.type} />
            <AssetStructureMap type={asset.meta.type} />
          </div>
        </div>
      </div>
    </section>

    <section className="vAssetGuideBand">
      <div className="wrap">
        <div className="vAssetGuideHeading"><span className="eyebrow">HOW TO USE</span><small>From structured asset to reusable work.</small></div>
        <ol className="vAssetGuideRail">
          {[
            ["Copy", "Take the complete asset."],
            ["Run", "Paste it before your task input."],
            ["Provide", "Add the inputs it asks for."],
            ["Verify", "Use the included checks."],
            ["Reuse", "Change the per-run context."]
          ].map(([title, text], index) => <li key={title}><span>{String(index + 1).padStart(2, "0")}</span><div><strong>{title}</strong><small>{text}</small></div></li>)}
        </ol>
      </div>
    </section>

    <section className="section" id="full-asset">
      <div className="wrap vAssetBodyGrid">
        <aside className="vAssetSide">
          <div className="vAssetSideCard">
            <div className="eyebrow">ASSET INFORMATION</div>
            <dl>
              <div><dt>Type</dt><dd>{asset.meta.type}</dd></div>
              <div><dt>Category</dt><dd>{asset.meta.categoryLabel}</dd></div>
              <div><dt>Asset ID</dt><dd><code>{asset.meta.id}</code></dd></div>
            </dl>
          </div>
          <div className="vAssetSideCard">
            <div className="eyebrow">BOUNDARY</div>
            <p>{asset.meta.type === "Builder"
              ? "The Builder creates a reusable artifact from your need. A generated result is not automatically Verlune Certified."
              : "This is structured methodology. Inspect the result and use the asset's verification guidance before acting."}</p>
          </div>
          <div className="vStickyCopy"><CopyPremiumAsset content={asset.content} /></div>
        </aside>

        <article className="vAssetReadingSurface">
          <div className="assetCodeHeader"><span>Full asset</span><code>{asset.meta.id}</code></div>
          <pre className="premiumAssetCode vPremiumAssetCode"><code>{customerVisibleContent(asset.content)}</code></pre>
        </article>
      </div>
    </section>

    {related.length ? <section className="section vRelatedSection">
      <div className="wrap">
        <div className="vLibraryGroupHeader"><div><div className="eyebrow">RELATED ASSETS</div><h2>Keep the structure moving.</h2></div><Link className="textLink" href="/app">View full library →</Link></div>
        <div className="vRelatedGrid">
          {related.map((item) => <article className="vRelatedCard" key={item.id}>
            <ArtifactMiniObject type={item.type} />
            <div className="assetCardMeta"><span>{item.type}</span><span>{item.id}</span></div>
            <h3>{item.name}</h3><p>{item.summary}</p>
            <Link className="textLink" href={`/app/asset/${encodeURIComponent(item.id)}`}>Open asset →</Link>
          </article>)}
        </div>
      </div>
    </section> : null}
  </main>;
}
