import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { CopyPremiumAsset } from "@/components/copy-premium-asset";
import { requirePremiumSession } from "@/lib/verlune-auth.server";
import { readPremiumAsset } from "@/lib/verlune-premium-assets.server";
import { getPremiumAssetMeta } from "@/lib/verlune-premium-catalog";

export const dynamic = "force-dynamic";

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

  return <main className="premiumApp">
    <section className="assetPageHero">
      <div className="wrap">
        <Link className="textLink" href="/app">← Premium Library</Link>
        <div className="assetTitleRow">
          <div>
            <div className="eyebrow">{asset.meta.type.toUpperCase()} / {asset.meta.categoryLabel.toUpperCase()}</div>
            <h1>{asset.meta.name}</h1>
            <p className="lead">{asset.meta.summary}</p>
          </div>
          <CopyPremiumAsset content={asset.content} />
        </div>
      </div>
    </section>

    <section className="section">
      <div className="wrap assetUseGrid">
        <aside className="assetUseGuide">
          <div className="eyebrow">HOW TO USE</div>
          <ol className="simpleSteps">
            <li>Copy the complete asset.</li>
            <li>Open your AI assistant.</li>
            <li>Paste the asset before your task input.</li>
            <li>Provide the required inputs it asks for.</li>
            <li>Verify the result using the included checks.</li>
          </ol>
          {asset.meta.type === "Builder"
            ? <p className="notice">Builders start by asking about your recurring need. Answer in ordinary language; the Builder should ask only for material missing information.</p>
            : null}
          <p className="micro">This asset is structured methodology. AI execution happens in your assistant, not inside Verlune.</p>
        </aside>
        <div>
          <div className="assetCodeHeader"><span>Complete asset</span><code>{asset.meta.id}</code></div>
          <pre className="premiumAssetCode"><code>{asset.content}</code></pre>
        </div>
      </div>
    </section>
  </main>;
}
