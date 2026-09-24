import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = rel => {
  const p = path.join(root, rel);
  if (!fs.existsSync(p)) throw new Error(`VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: missing ${rel}`);
  return fs.readFileSync(p, "utf8");
};

const home = read("app/page.tsx");
const free = read("app/free/page.tsx");
const premium = read("app/app/page.tsx");
const layout = read("app/layout.tsx");
const learn = read("app/learn/workflows-not-random-prompts/page.tsx");
const freeAsset = read("app/free/asset/[assetId]/page.tsx");
const robots = read("app/robots.ts");
const sitemap = read("app/sitemap.ts");
const env = read(".env.example");
const css = read("app/globals.css");

if (!home.includes("FREE_ASSETS") || !home.includes("vCategoryCardLink") || !home.includes("Explore ${name} in the Free Library")) {
  throw new Error("VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: Home category affordances are not actionable");
}

const freeHero = free.split('<section className="vProcessBand">')[0];
if (freeHero.includes("Download developer starter ZIP")) {
  throw new Error("VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: developer ZIP still competes in Free hero");
}
for (const marker of ["DEVELOPMENT & TECH / DOWNLOAD", "Download developer starter ZIP", "nineteen-asset Verlune Free library"]) {
  if (!free.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: Free resource boundary missing ${marker}`);
}

for (const marker of [
  "LibraryExplorer",
  'fixedTier="premium"',
  'initialCollectionId="premium-essentials"',
  "getPremiumLibraryDiscoveryAssets"
]) {
  if (!premium.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: Premium discovery missing ${marker}`);
}

for (const marker of ['className="mobileNav"', 'aria-label="Open navigation"', 'aria-label="Mobile"', 'href="/unlock">Unlock access']) {
  if (!layout.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: mobile navigation missing ${marker}`);
}
if (!css.includes(".mobileNav") || !css.includes("@media (max-width: 780px)")) {
  throw new Error("VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: mobile navigation responsive CSS missing");
}

for (const marker of ["nineteen complete assets", "sixteen prompts and three workflows", "Explore the Free Library"]) {
  if (!learn.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: Learn current-state copy missing ${marker}`);
}
if (learn.includes("current free workflows has three structured developer workflows")) {
  throw new Error("VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: stale Free Library copy remains");
}

for (const marker of ["NEXT_PUBLIC_INDEXING_MODE", 'disallow: "/"']) {
  if (!robots.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: robots fail-closed marker missing ${marker}`);
}
for (const marker of ["FREE_ASSETS", '"/library"', '"/free"', '"/premium"', '"/code-review"', '"/license"']) {
  if (!sitemap.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: sitemap missing ${marker}`);
}
if (!env.includes("NEXT_PUBLIC_INDEXING_MODE=off") || !env.includes("NEXT_PUBLIC_SITE_URL=")) {
  throw new Error("VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: indexing defaults are not fail-closed/configured");
}

if (!freeAsset.includes("description: meta?.summary") || !freeAsset.includes("canonical: `/free/asset/")) {
  throw new Error("VERLUNE PRODUCT CLOSURE P1 AUDIT FAIL: Free asset SEO metadata incomplete");
}

console.log("VERLUNE PRODUCT CLOSURE P1 UX AUDIT: PASS");
console.log("home_category_affordances=actionable");
console.log("free_hero=library_first");
console.log("developer_zip=secondary_resource");
console.log("premium_navigation=search_filter_discovery");
console.log("mobile_navigation=present");
console.log("learn_free_copy=current");
console.log("robots_and_sitemap=fail_closed_until_configured");
console.log("free_asset_metadata=canonical+description");
