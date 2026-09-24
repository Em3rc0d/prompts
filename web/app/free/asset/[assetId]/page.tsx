import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { CopyPremiumAsset } from "@/components/copy-premium-asset";
import { ArtifactMiniObject, AssetStructureMap } from "@/components/verlune-visuals";
import { readFreeAsset } from "@/lib/verlune-free-assets.server";
import { FREE_ASSETS, getFreeAssetMeta } from "@/lib/verlune-free-catalog";

export const dynamic = "force-dynamic";

function customerVisibleContent(source: string): string {
  return source
    .split("\n")
    .filter((line) => !/^Status:\s+`/.test(line))
    .join("\n")
    .replace(/\n{3,}/g, "\n\n");
}

export async function generateMetadata({params}:{params:Promise<{assetId:string}>}):Promise<Metadata>{
  const {assetId}=await params;
  const meta=getFreeAssetMeta(assetId);
  return { title: meta?.name ?? "Free Asset", description: meta?.summary, alternates: meta ? { canonical: `/free/asset/${encodeURIComponent(meta.id)}` } : undefined, robots:{index:true,follow:true} };
}

export default async function FreeAssetPage({params}:{params:Promise<{assetId:string}>}){
  const {assetId}=await params;
  const meta=getFreeAssetMeta(assetId);
  if(!meta) notFound();

  let asset:Awaited<ReturnType<typeof readFreeAsset>>;
  try{ asset=await readFreeAsset(assetId); }catch{ notFound(); }

  const related=FREE_ASSETS.filter((item)=>item.id!==assetId&&(item.category===asset.meta.category||item.type===asset.meta.type)).slice(0,3);

  return <main className="vAssetDetail vFreeAssetDetail">
    <section className="vAssetHero">
      <div className="wrap">
        <Link className="textLink vBackLink" href="/free">← Free Library</Link>
        <div className="vAssetHeroGrid">
          <div className="vAssetHeroCopy">
            <div className="assetCardMeta vAssetMetaTop"><span>FREE {asset.meta.type.toUpperCase()}</span><span>{asset.meta.categoryLabel}</span><span>{asset.meta.id}</span></div>
            <h1>{asset.meta.name}</h1>
            <p className="lead">{asset.meta.summary}</p>
            <div className="actions"><CopyPremiumAsset content={asset.content}/><a className="btn btnSecondary" href="#full-asset">Read full asset</a></div>
            <p className="micro">Use in your compatible AI assistant. Important outputs still require verification.</p>
          </div>
          <div className="vAssetVisualPanel">
            <ArtifactMiniObject type={asset.meta.type}/>
            <AssetStructureMap type={asset.meta.type}/>
          </div>
        </div>
      </div>
    </section>

    <section className="vAssetGuideBand">
      <div className="wrap">
        <div className="vAssetGuideHeading"><span className="eyebrow">HOW TO USE</span><small>Copy the exact asset, provide its inputs, and inspect the result.</small></div>
        <ol className="vAssetGuideRail">
          {[
            ["Copy","Take the complete asset."],
            ["Run","Paste it in your AI assistant."],
            ["Provide","Add the inputs it requests."],
            ["Verify","Check claims and boundaries."],
            ["Reuse","Change the task input next time."]
          ].map(([title,text],index)=><li key={title}><span>{String(index+1).padStart(2,"0")}</span><div><strong>{title}</strong><small>{text}</small></div></li>)}
        </ol>
      </div>
    </section>

    <section className="section" id="full-asset">
      <div className="wrap vAssetBodyGrid">
        <aside className="vAssetSide">
          <div className="vAssetSideCard">
            <div className="eyebrow">FREE ASSET</div>
            <dl><div><dt>Type</dt><dd>{asset.meta.type}</dd></div><div><dt>Category</dt><dd>{asset.meta.categoryLabel}</dd></div><div><dt>Asset ID</dt><dd><code>{asset.meta.id}</code></dd></div></dl>
          </div>
          <div className="vAssetSideCard"><div className="eyebrow">BOUNDARY</div><p>This asset provides structure and verification guidance. It does not guarantee that an AI answer is correct or appropriate for every context.</p></div>
          <div className="vStickyCopy"><CopyPremiumAsset content={asset.content}/></div>
        </aside>
        <article className="vAssetReadingSurface">
          <div className="assetCodeHeader"><span>Full free asset</span><code>{asset.meta.id}</code></div>
          <pre className="premiumAssetCode vPremiumAssetCode"><code>{customerVisibleContent(asset.content)}</code></pre>
        </article>
      </div>
    </section>

    {related.length?<section className="section vRelatedSection"><div className="wrap">
      <div className="vLibraryGroupHeader"><div><div className="eyebrow">RELATED FREE ASSETS</div><h2>Keep going without changing the trust boundary.</h2></div><Link className="textLink" href="/free">View Free Library →</Link></div>
      <div className="vRelatedGrid">{related.map((item)=><article className="vRelatedCard" key={item.id}><ArtifactMiniObject type={item.type}/><div className="assetCardMeta"><span>{item.type}</span><span>{item.id}</span></div><h3>{item.name}</h3><p>{item.summary}</p><Link className="textLink" href={`/free/asset/${encodeURIComponent(item.id)}`}>Open asset →</Link></article>)}</div>
    </div></section>:null}
  </main>;
}
