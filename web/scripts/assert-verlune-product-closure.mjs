import fs from "node:fs";
import path from "node:path";

const root = process.cwd();

const files = {
  premium: "app/premium/page.tsx",
  checkout: "app/api/commerce/verlune-premium/checkout/route.ts",
  layout: "app/layout.tsx",
  home: "app/page.tsx",
  free: "app/free/page.tsx",
  unlock: "app/unlock/page.tsx",
  licensePage: "app/license/page.tsx",
  freeLicense: "../product/verlune-v1/free/LICENSE.md",
  env: ".env.example",
  catalog: "lib/verlune-premium-catalog.ts"
};

function read(rel) {
  const absolute = path.resolve(root, rel);
  if (!fs.existsSync(absolute)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: missing ${rel}`);
  return fs.readFileSync(absolute, "utf8");
}

const premium = read(files.premium);
const checkout = read(files.checkout);
const layout = read(files.layout);
const home = read(files.home);
const free = read(files.free);
const unlock = read(files.unlock);
const licensePage = read(files.licensePage);
const freeLicense = read(files.freeLicense);
const env = read(files.env);
const catalog = read(files.catalog);

for (const marker of [
  "VERLUNE PREMIUM",
  "Already purchased? Unlock",
  "Purchasing not open yet",
  "getVerlunePremiumCommerceState",
  "/api/commerce/verlune-premium/checkout"
]) {
  if (!premium.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: Premium missing ${marker}`);
}

for (const marker of [
  'VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE"',
  'VERLUNE_PREMIUM_COMMERCE_MODE',
  'premium_access_not_configured',
  'provider_test_not_authorized',
  'live_canary_not_authorized',
  'checkout_url_not_allowed'
]) {
  if (!checkout.includes(marker)) throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: checkout missing ${marker}`);
}

if (!env.includes("VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=NOT_FOR_SALE")) {
  throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: Premium sale must default fail-closed");
}
if (env.includes("VERLUNE_PREMIUM_PUBLIC_SALE_STATUS=LIVE")) {
  throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: example config must not enable public Premium sale");
}

if (!layout.includes('href="/premium">Premium</')) {
  throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: primary navigation does not expose Premium discovery");
}
if (!layout.includes('href="/unlock">Unlock access')) {
  throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: unlock is not separated as existing-purchase access");
}

for (const [surface, source] of [["home", home], ["free", free]]) {
  if (!source.includes('href="/premium"')) {
    throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: ${surface} does not route Premium intent through /premium`);
  }
}

if (!unlock.includes('href="/premium">← Explore Premium')) {
  throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: unlock cannot return prospective buyers to Premium");
}

for (const marker of [
  "eleven launch-core assets",
  "eight structured prompts",
  "three structured workflows",
  "No resale or redistribution"
]) {
  if (!freeLicense.includes(marker)) {
    throw new Error(`VERLUNE PRODUCT CLOSURE AUDIT FAIL: Free license missing ${marker}`);
  }
}
if (!licensePage.includes("FREE_ASSETS.length") || !licensePage.includes("VERLUNE FREE LIBRARY")) {
  throw new Error("VERLUNE PRODUCT CLOSURE AUDIT FAIL: public license surface is not scoped to the full Free Library");
}

const promptIds = catalog.match(/id:\s*"VP-P-[^"]+"/g) ?? [];
const workflowIds = catalog.match(/id:\s*"VP-WF-[^"]+"/g) ?? [];
const builderIds = catalog.match(/id:\s*"VP-BUILDER-[^"]+"/g) ?? [];
const toolkitIds = catalog.match(/id:\s*"VP-TK-[^"]+"/g) ?? [];

if (promptIds.length !== 8 || workflowIds.length !== 5 || builderIds.length !== 2 || toolkitIds.length !== 2) {
  throw new Error(
    `VERLUNE PRODUCT CLOSURE AUDIT FAIL: Premium catalog expected 8/5/2/2, got ${promptIds.length}/${workflowIds.length}/${builderIds.length}/${toolkitIds.length}`
  );
}

console.log("VERLUNE PRODUCT CLOSURE P0 AUDIT: PASS");
console.log("premium_public_discovery=present");
console.log("premium_public_sale_default=NOT_FOR_SALE");
console.log("premium_checkout=fail_closed_gated");
console.log("unlock=existing_purchase_surface");
console.log("free_license_scope=11_assets");
console.log("premium_launch_core=17_assets");
console.log("boundary=source/build contract only; live commerce and human value review not implied");
