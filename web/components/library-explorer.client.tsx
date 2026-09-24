"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

import type {
  LibraryCollection,
  LibraryDiscoveryAsset,
  LibraryDiscoveryType,
  LibraryTier
} from "@/lib/verlune-library-discovery";

const TYPE_ORDER: readonly LibraryDiscoveryType[] = ["Prompt", "Workflow", "Builder", "Toolkit"];

type Props = {
  assets: readonly LibraryDiscoveryAsset[];
  collections: readonly LibraryCollection[];
  fixedTier?: LibraryTier;
  initialCollectionId?: string;
  heading?: string;
  intro?: string;
};

export function LibraryExplorer({
  assets,
  collections,
  fixedTier,
  initialCollectionId,
  heading = "Find the job you need.",
  intro = "Search by task, narrow by tier, type or category, or start from a curated collection."
}: Props) {
  const availableIds = useMemo(() => new Set(assets.map((asset) => asset.id)), [assets]);
  const availableCollections = useMemo(
    () => collections
      .map((collection) => ({
        ...collection,
        assetIds: collection.assetIds.filter((id) => availableIds.has(id))
      }))
      .filter((collection) => collection.assetIds.length > 0),
    [collections, availableIds]
  );

  const validInitialCollection = initialCollectionId &&
    availableCollections.some((collection) => collection.id === initialCollectionId)
      ? initialCollectionId
      : "";

  const [query, setQuery] = useState("");
  const [tier, setTier] = useState<LibraryTier | "all">(fixedTier ?? "all");
  const [type, setType] = useState<LibraryDiscoveryType | "all">("all");
  const [category, setCategory] = useState("all");
  const [collectionId, setCollectionId] = useState(validInitialCollection);
  const [limit, setLimit] = useState(12);

  const categories = useMemo(() => {
    const pairs = new Map<string, string>();
    for (const asset of assets) pairs.set(asset.category, asset.categoryLabel);
    return [...pairs.entries()].sort((a, b) => a[1].localeCompare(b[1]));
  }, [assets]);

  const collection = availableCollections.find((item) => item.id === collectionId);
  const collectionIds = collection ? new Set(collection.assetIds) : null;
  const normalizedQuery = query.trim().toLowerCase();

  const matches = assets.filter((asset) => {
    if (fixedTier && asset.tier !== fixedTier) return false;
    if (!fixedTier && tier !== "all" && asset.tier !== tier) return false;
    if (type !== "all" && asset.type !== type) return false;
    if (category !== "all" && asset.category !== category) return false;
    if (collectionIds && !collectionIds.has(asset.id)) return false;
    if (normalizedQuery) {
      const haystack = [
        asset.name,
        asset.summary ?? "",
        asset.categoryLabel,
        asset.type,
        asset.tier,
        asset.id
      ].join(" ").toLowerCase();
      if (!haystack.includes(normalizedQuery)) return false;
    }
    return true;
  });

  const visible = matches.slice(0, limit);
  const hasFilters = Boolean(query) || (!fixedTier && tier !== "all") || type !== "all" ||
    category !== "all" || Boolean(collectionId);

  const reset = () => {
    setQuery("");
    setTier(fixedTier ?? "all");
    setType("all");
    setCategory("all");
    setCollectionId("");
    setLimit(12);
  };

  const changeCollection = (id: string) => {
    setCollectionId(id === collectionId ? "" : id);
    setLimit(12);
  };

  return <div className="vLibraryExplorer" id="library">
    <div className="vExplorerHeader">
      <div>
        <div className="eyebrow">DISCOVER</div>
        <h2>{heading}</h2>
        <p>{intro}</p>
      </div>
      <div className="vExplorerCount" aria-live="polite">
        <strong>{matches.length}</strong>
        <span>{matches.length === 1 ? "match" : "matches"}</span>
      </div>
    </div>

    <div className="vCollectionShelf" aria-label="Curated collections">
      <button
        type="button"
        className={!collectionId ? "isActive" : ""}
        aria-pressed={!collectionId}
        onClick={() => changeCollection("")}
      >
        <span>All assets</span>
        <small>{assets.length}</small>
      </button>
      {availableCollections.map((item) => <button
        type="button"
        key={item.id}
        className={collectionId === item.id ? "isActive" : ""}
        aria-pressed={collectionId === item.id}
        title={item.description}
        onClick={() => changeCollection(item.id)}
      >
        <span>{item.name}</span>
        <small>{item.assetIds.length}</small>
      </button>)}
    </div>

    {collection ? <div className="vCollectionContext">
      <span>CURATED COLLECTION</span>
      <strong>{collection.name}</strong>
      <p>{collection.description}</p>
    </div> : null}

    <div className="vExplorerControls">
      <label className="vSearchControl">
        <span>Search</span>
        <input
          type="search"
          value={query}
          placeholder="Try: code review, research, interview…"
          onChange={(event) => { setQuery(event.target.value); setLimit(12); }}
        />
      </label>

      {!fixedTier ? <fieldset className="vFilterGroup">
        <legend>Tier</legend>
        <div className="vFilterChips">
          {(["all", "free", "premium"] as const).map((value) => <button
            type="button"
            key={value}
            className={tier === value ? "isActive" : ""}
            aria-pressed={tier === value}
            onClick={() => { setTier(value); setLimit(12); }}
          >{value === "all" ? "All" : value === "free" ? "Free" : "Premium"}</button>)}
        </div>
      </fieldset> : null}

      <fieldset className="vFilterGroup">
        <legend>Type</legend>
        <div className="vFilterChips">
          <button
            type="button"
            className={type === "all" ? "isActive" : ""}
            aria-pressed={type === "all"}
            onClick={() => { setType("all"); setLimit(12); }}
          >All</button>
          {TYPE_ORDER.filter((candidate) => assets.some((asset) => asset.type === candidate)).map((candidate) => <button
            type="button"
            key={candidate}
            className={type === candidate ? "isActive" : ""}
            aria-pressed={type === candidate}
            onClick={() => { setType(candidate); setLimit(12); }}
          >{candidate}</button>)}
        </div>
      </fieldset>

      <label className="vCategoryControl">
        <span>Category</span>
        <select value={category} onChange={(event) => { setCategory(event.target.value); setLimit(12); }}>
          <option value="all">All categories</option>
          {categories.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
        </select>
      </label>

      {hasFilters ? <button type="button" className="vResetFilters" onClick={reset}>Clear filters</button> : null}
    </div>

    {matches.length ? <>
      <div className="vExplorerGrid">
        {visible.map((asset) => <article className={`vExplorerCard${asset.publicNameOnly ? " vExplorerCardNameOnly" : ""}`} key={asset.id}>
          <div className="vExplorerMeta">
            <span className={asset.tier === "free" ? "vTierBadge vTierBadgeFree" : "vTierBadge vTierBadgePremium"}>
              {asset.tier === "free" ? "FREE" : "PREMIUM"}
            </span>
            {!asset.publicNameOnly ? <span>{asset.type}</span> : null}
          </div>
          {!asset.publicNameOnly ? <div className="vExplorerCategory">{asset.categoryLabel}</div> : null}
          <h3>{asset.name}</h3>
          {!asset.publicNameOnly && asset.summary ? <p>{asset.summary}</p> : null}
          <div className="vExplorerCardFooter">
            {!asset.publicNameOnly ? <small>{asset.id}</small> : <span />}
            <Link className="textLink" href={asset.href}>{asset.cta} →</Link>
          </div>
        </article>)}
      </div>
      {visible.length < matches.length ? <div className="vShowMore">
        <span>Showing {visible.length} of {matches.length}</span>
        <button type="button" className="btn btnSecondary" onClick={() => setLimit((current) => current + 12)}>Show 12 more</button>
      </div> : null}
    </> : <div className="vExplorerEmpty">
      <strong>No assets match those filters.</strong>
      <p>Try removing one filter or searching for the job rather than the tool name.</p>
      <button type="button" className="textLink" onClick={reset}>Clear filters →</button>
    </div>}
  </div>;
}
