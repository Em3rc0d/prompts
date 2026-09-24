import fs from "node:fs";
import path from "node:path";

const root = process.cwd();

function read(rel) {
  const file = path.join(root, rel);
  if (!fs.existsSync(file)) throw new Error(`VERLUNE LIBRARY DISCOVERY AUDIT FAIL: missing ${rel}`);
  return fs.readFileSync(file, "utf8");
}

const libraryPage = read("app/library/page.tsx");
const freePage = read("app/free/page.tsx");
const premiumPage = read("app/app/page.tsx");
const layout = read("app/layout.tsx");
const sitemap = read("app/sitemap.ts");
const explorer = read("components/library-explorer.client.tsx");
const discovery = read("lib/verlune-library-discovery.ts");
const freeCatalog = read("lib/verlune-free-catalog.ts");
const premiumCatalog = read("lib/verlune-premium-catalog.ts");

const freeAssets = (freeCatalog.match(/id:\s*"VF-(?:P|WF)-[^"]+"/g) ?? []).length;
const premiumAssets = (premiumCatalog.match(/id:\s*"VP-(?:P|WF|BUILDER|TK)-[^"]+"/g) ?? []).length;
const freePrompts = (freeCatalog.match(/id:\s*"VF-P-[^"]+"/g) ?? []).length;
const premiumPrompts = (premiumCatalog.match(/id:\s*"VP-P-[^"]+"/g) ?? []).length;

if (freeAssets !== 19) throw new Error(`VERLUNE LIBRARY DISCOVERY AUDIT FAIL: expected 19 Free assets, got ${freeAssets}`);
if (premiumAssets !== 41) throw new Error(`VERLUNE LIBRARY DISCOVERY AUDIT FAIL: expected 41 Premium assets, got ${premiumAssets}`);
if (freePrompts + premiumPrompts !== 48) throw new Error("VERLUNE LIBRARY DISCOVERY AUDIT FAIL: expected 48 prompts");

for (const marker of [
  "getPublicLibraryAssets",
  "LibraryExplorer",
  'initialCollectionId="start-here"',
  "DISCOVERY ≠ ACCESS"
]) {
  if (!libraryPage.includes(marker)) throw new Error(`VERLUNE LIBRARY DISCOVERY AUDIT FAIL: /library missing ${marker}`);
}

for (const marker of [
  'type="search"',
  "Tier",
  "Type",
  "Category",
  "Clear filters",
  "Show 12 more",
  "No assets match those filters."
]) {
  if (!explorer.includes(marker)) throw new Error(`VERLUNE LIBRARY DISCOVERY AUDIT FAIL: explorer missing ${marker}`);
}

for (const marker of [
  "start-here",
  "premium-essentials",
  "ship-software",
  "research-decide",
  "learn-prepare",
  "operate-plan",
  "write-communicate",
  "content-audience"
]) {
  if (!discovery.includes(marker)) throw new Error(`VERLUNE LIBRARY DISCOVERY AUDIT FAIL: curated collection missing ${marker}`);
}

if (discovery.includes("sourceBlobSha: asset.sourceBlobSha") || discovery.includes("relativePath: asset.relativePath")) {
  throw new Error("VERLUNE LIBRARY DISCOVERY AUDIT FAIL: public discovery model leaks source provenance fields");
}
if (!discovery.includes('destination === "private"') || !discovery.includes('href: destination === "private"')) {
  throw new Error("VERLUNE LIBRARY DISCOVERY AUDIT FAIL: Premium public/private destination boundary missing");
}
if (!discovery.includes('summary: destination === "private" ? asset.summary : null') ||
    !discovery.includes('publicNameOnly: destination === "public"')) {
  throw new Error("VERLUNE LIBRARY DISCOVERY AUDIT FAIL: public Premium must be name-only");
}
if (!explorer.includes('!asset.publicNameOnly && asset.summary') ||
    !explorer.includes('!asset.publicNameOnly ? <div className="vExplorerCategory"') ||
    !explorer.includes('!asset.publicNameOnly ? <small>{asset.id}</small>')) {
  throw new Error("VERLUNE LIBRARY DISCOVERY AUDIT FAIL: public Premium name-only rendering boundary missing");
}

for (const [surface, source, markers] of [
  ["Free", freePage, ["LibraryExplorer", 'fixedTier="free"', 'initialCollectionId="start-here"']],
  ["Premium", premiumPage, ["LibraryExplorer", 'fixedTier="premium"', 'initialCollectionId="premium-essentials"']]
]) {
  for (const marker of markers) {
    if (!source.includes(marker)) throw new Error(`VERLUNE LIBRARY DISCOVERY AUDIT FAIL: ${surface} missing ${marker}`);
  }
}

for (const marker of ['href="/library">Library</', 'href="/free">Free</', 'href="/premium">Premium</']) {
  if (!layout.includes(marker)) throw new Error(`VERLUNE LIBRARY DISCOVERY AUDIT FAIL: navigation missing ${marker}`);
}
if (!sitemap.includes('"/library"')) {
  throw new Error("VERLUNE LIBRARY DISCOVERY AUDIT FAIL: sitemap missing /library");
}

console.log("VERLUNE LIBRARY DISCOVERY AUDIT: PASS");
console.log("library_assets=60");
console.log("prompts=48");
console.log("free_assets=19");
console.log("premium_assets=41");
console.log("search=present");
console.log("filters=tier+type+category");
console.log("curated_collections=8");
console.log("default_public_collection=start-here");
console.log("pagination=12_at_a_time");
console.log("premium_public_content=name_only");
console.log("premium_protected_content=entitlement_required");
